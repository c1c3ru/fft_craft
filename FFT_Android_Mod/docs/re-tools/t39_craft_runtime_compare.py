#!/usr/bin/env python3
"""Run pinned Craft Anything CLI on original ARM ELF; compare bounded metadata.

External CLI is untrusted. Never execute generated code, import pseudo-C, or
publish raw evidence. The four selected targets must be revalidated with
Unicorn/C++ independently before any certificate is considered.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_OP_IMM
from elftools.elf.elffile import ELFFile

import b01_overlap_elf_evidence as original
import t39_craft_pilot_reference as pilot

CLI_VERSION = "0.3.0"
CLI_RELEASE_SHA256 = "674ec59ffbdaefbd577917e07c9d464562043b275a3889ba4f60239a12f03d53"
MAX_OUTPUT = 4 * 1024 * 1024
ADDR_RE = re.compile(r"^0x[0-9a-fA-F]{1,8}$")
MNEMONIC_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9._]{0,23}$")


def address(value):
    if isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 0xffffffff:
        return value
    if isinstance(value, str) and ADDR_RE.fullmatch(value):
        return int(value, 16)
    raise ValueError("Untrusted address outside ARM32 or malformed")


def sanitize_mnemonic(raw):
    return raw.lower() if isinstance(raw, str) and MNEMONIC_RE.fullmatch(raw) else "unknown"


def parse_tool(output, expected_operation):
    if not isinstance(output, dict) or output.get("operation") != expected_operation:
        raise ValueError("CLI did not produce requested evidence operation")
    r = output.get("result")
    if not isinstance(r, dict):
        raise ValueError("Malformed native evidence result")
    if expected_operation == "native_function_instructions_list":
        rows = r.get("instructions")
        if not isinstance(rows, list) or len(rows) > 20000:
            raise ValueError("Unbounded or missing instruction list")
    elif expected_operation == "native_instruction_show":
        rows = [r] if r.get("kind") == "instruction" else []
    else:
        raise ValueError("Unsupported operation")
    extracted = []
    for item in rows:
        if not isinstance(item, dict):
            raise ValueError("Unexpected instruction object")
        addr = address(item.get("address"))
        raw = item.get("bytes")
        length = item.get("length")
        if (not isinstance(raw, str) or len(raw) > 32
                or len(raw) % 2 or not re.fullmatch("[0-9a-fA-F]*", raw)
                or type(length) is not int or length not in (2, 4)
                or len(raw) != length * 2):
            raise ValueError("Bad reported instruction bytes/length")
        extracted.append({
            "address": addr, "length": length,
            "bytes_sha256": hashlib.sha256(bytes.fromhex(raw)).hexdigest(),
            "mnemonic": sanitize_mnemonic(item.get("mnemonic")),
            "flow": item.get("flow"),
        })
    return extracted


def call_cli(cli, binary, project, operation, param, timeout_sec):
    args = [str(cli), "--deep", "--project", str(project),
            operation.replace("_", "-"), str(binary),
            "--function" if operation == "native_function_instructions_list" else "--address",
            param]
    env = {k: v for k, v in os.environ.items()
           if k not in {"GH_TOKEN", "GITHUB_TOKEN", "GITHUB_API_URL",
                        "GITHUB_SERVER_URL", "SSH_AUTH_SOCK", "CI_JOB_TOKEN"}
           and not k.startswith(("AWS_", "AZURE_", "GOOGLE_", "OPENAI_", "ANTHROPIC_"))}
    env["HOME"] = str(project.parent / "home")
    env["XDG_CONFIG_HOME"] = str(project.parent / "config")
    Path(env["HOME"]).mkdir(parents=True, exist_ok=True)
    Path(env["XDG_CONFIG_HOME"]).mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(args, capture_output=True, text=True,
                                timeout=timeout_sec, env=env,
                                cwd=project.parent, check=False)
    except subprocess.TimeoutExpired:
        return "timeout", []
    if result.returncode:
        return "command_error", []
    if len(result.stdout) > MAX_OUTPUT:
        return "oversized_output", []
    try:
        doc = json.loads(result.stdout)
        return "success", parse_tool(doc, operation)
    except (ValueError, TypeError, KeyError):
        return "unparseable_output", []


def reference_branch_targets(binary, target):
    physical = int(target["physical_entry"], 16)
    length = target["requested_bytes"]
    with binary.open("rb") as f:
        elf = ELFFile(f)
        raw, _ = original.read_executable(elf, f, physical, length)
    if raw is None or hashlib.sha256(raw).hexdigest() != target["original_bytes_sha256"]:
        raise ValueError("Reference bytes changed or not in original executable segment")
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB
                 if target["entry_isa"] == "thumb" else CS_MODE_ARM)
    decoder.detail = True
    references = {}
    for instr in decoder.disasm(raw, physical):
        if (instr.id in (ARM_INS_B, ARM_INS_BL, ARM_INS_BLX)
                and len(instr.operands) == 1
                and instr.operands[0].type == ARM_OP_IMM):
            references[instr.address] = int(instr.operands[0].imm) & 0xffffffff
    return references


def external_branch_target(flow):
    # Rust serializes Flow enums by variant, e.g. {"Call":{"target":1234}}.
    # Never trust this as a proof that the target is reachable at runtime.
    if not isinstance(flow, dict):
        return None
    if "target" in flow:
        try:
            return address(flow["target"])
        except ValueError:
            return None
    for key in ("Call", "Jump", "Cond"):
        child = flow.get(key)
        if isinstance(child, dict) and "target" in child:
            try:
                return address(child["target"])
            except ValueError:
                return None
    return None


def compare_target(target, extracted, branch_reference, cli_status):
    low = int(target["physical_entry"], 16)
    high = low + target["requested_bytes"]
    by_addr = {}
    for item in extracted:
        addr = item["address"]
        if addr in by_addr:
            raise ValueError("Overlapping third-party instruction evidence")
        by_addr[addr] = item
    matches, disagreements, branch_checks = 0, [], []
    for expected in target["first_instructions"]:
        addr = int(expected["address"], 16)
        if not low <= addr < high:
            raise ValueError("Original expected instruction outside reviewed window")
        got = by_addr.get(addr)
        if got is None:
            disagreements.append({"address": expected["address"],
                                  "reason": "instruction_not_reported"})
            continue
        same_bytes = got["bytes_sha256"] == expected["instruction_bytes_sha256"]
        same_size = got["length"] == expected["size"]
        same_mnemonic = got["mnemonic"] == expected["mnemonic"].lower()
        if same_bytes and same_size and same_mnemonic:
            matches += 1
        else:
            disagreements.append({
                "address": expected["address"], "reason": "instruction_mismatch",
                "bytes_match": same_bytes, "size_match": same_size,
                "mnemonic_match": same_mnemonic,
                "external_mnemonic": got["mnemonic"],
            })
        if addr in branch_reference:
            tgt = external_branch_target(got["flow"])
            branch_checks.append({
                "site": expected["address"],
                "capstone_target": "0x%08x" % branch_reference[addr],
                "craft_target": ("0x%08x" % tgt if tgt is not None else None),
                "target_comparable": tgt is not None,
                "targets_match": tgt == branch_reference[addr] if tgt is not None else None,
            })
    return {
        "task": target["task"], "name": target["name"],
        "entry": target["declared_entry"], "isa": target["entry_isa"],
        "cli_status": cli_status,
        "reference_instructions": len(target["first_instructions"]),
        "third_party_instructions_in_window": len([
            x for x in extracted if low <= x["address"] < high]),
        "matched_instruction_boundaries_and_bytes": matches,
        "differences_or_not_reported": disagreements,
        "branch_target_comparison": branch_checks,
        "original_function_reachability_proven": False,
        "semantic_equivalence_proven": False,
    }


def report(binary, ref, cli, per_target_timeout=120):
    if original.sha256(binary) != original.PINNED_ELF_SHA:
        raise ValueError("ELF original mismatch")
    if (ref.get("elf_sha256") != original.PINNED_ELF_SHA
            or ref.get("schema") != 1
            or ref.get("craft_anything_runtime_executed") is not False):
        raise ValueError("Untrusted pilot reference")
    targets = ref.get("capstone_reference_targets")
    if not isinstance(targets, list) or len(targets) != 4:
        raise ValueError("Four reference windows required")
    if [x.get("name") for x in targets] != [x["name"] for x in pilot.TARGETS]:
        raise ValueError("Reference windows differ from reviewed target set")
    if not cli.is_file():
        raise ValueError("Pinned Craft Anything CLI executable unavailable")
    outcomes = []
    with tempfile.TemporaryDirectory(prefix="fft-craft-ca-") as d:
        study = Path(d)
        for target in targets:
            physical = target["physical_entry"]
            branch = reference_branch_targets(binary, target)
            status, insns = call_cli(
                cli, binary, study / "study.cany",
                "native_function_instructions_list", physical, per_target_timeout)
            if status != "success" or not insns:
                fallback, items = call_cli(
                    cli, binary, study / "study.cany",
                    "native_instruction_show", physical, per_target_timeout)
                if fallback == "success" and items:
                    status, insns = "first_instruction_only", items
                else:
                    status, insns = "unavailable_" + status + "_" + fallback, []
            outcomes.append(compare_target(target, insns, branch, status))
    return {
        "schema": 1, "elf_sha256": original.PINNED_ELF_SHA,
        "craft_anything_version": CLI_VERSION,
        "craft_anything_linux_release_sha256": CLI_RELEASE_SHA256,
        "craft_anything_runtime_executed": True,
        "targets": outcomes,
        "targets_with_at_least_one_comparable_instruction": sum(
            t["matched_instruction_boundaries_and_bytes"] > 0 for t in outcomes),
        "matched_instruction_count": sum(
            t["matched_instruction_boundaries_and_bytes"] for t in outcomes),
        "new_semantic_certificates": 0, "new_structural_approvals": 0,
        "tasks_closed": [], "comparisons_are_not_certifications": True,
    }


def render_md(data):
    lines = [
        "# Comparação real: Craft Anything CLI × ELF original (Capstone)", "",
        "ELF SHA-256: " + data["elf_sha256"], "",
        "Craft Anything versão: " + data["craft_anything_version"], "",
        "| Alvo | Estado da CLI | Instr. comparáveis | Coincidências |",
        "|---|---|---:|---:|",
    ]
    for row in data["targets"]:
        lines.append("| " + row["name"] + " | " + row["cli_status"] +
                     " | " + str(row["third_party_instructions_in_window"]) +
                     " | " + str(row["matched_instruction_boundaries_and_bytes"]) + " |")
    lines += ["", "## Limites", "",
              "Desmontagem e destinos de saltos são indícios técnicos, não",
              "prova de chamadores reais, contratos de memória ou equivalência.",
              "Entradas externas ausentes ficam como indisponíveis; não são",
              "classificadas como divergência comprovada.",
              "Sem certificados novos, sem atualização automática das 40 tarefas.",
              "O artefato não incorpora bytes, pseudocódigo nem saídas brutas de terceiros.", ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--reference", type=Path, required=True)
    p.add_argument("--cli", type=Path, required=True)
    p.add_argument("--json-output", type=Path, required=True)
    p.add_argument("--md-output", type=Path, required=True)
    p.add_argument("--timeout-per-target", type=int, default=120)
    a = p.parse_args()
    if not 1 <= a.timeout_per_target <= 240:
        raise ValueError("Time bound must be 1..240 seconds")
    data = report(a.binary.resolve(),
                  json.loads(a.reference.read_text(encoding="utf-8")),
                  a.cli.resolve(), a.timeout_per_target)
    a.json_output.parent.mkdir(parents=True, exist_ok=True)
    a.md_output.parent.mkdir(parents=True, exist_ok=True)
    a.json_output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
    a.md_output.write_text(render_md(data), encoding="utf-8")
    print("CRAFT_ACTUAL_TARGETS_WITH_COMPARABLE_INSTRUCTIONS=" +
          str(data["targets_with_at_least_one_comparable_instruction"]))
    print("CRAFT_ACTUAL_MATCHING_INSTRUCTIONS=" + str(data["matched_instruction_count"]))
    print("CRAFT_ACTUAL_NEW_CERTIFICATES=0")
    if not data["targets_with_at_least_one_comparable_instruction"]:
        raise SystemExit("No comparable third-party instruction was produced; review pilot output")


if __name__ == "__main__":
    main()
