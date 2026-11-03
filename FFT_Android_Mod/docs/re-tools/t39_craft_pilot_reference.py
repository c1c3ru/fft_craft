#!/usr/bin/env python3
"""T04/T06 cross-tool pilot reference: Capstone vs optional Craft Anything JSON.

Disassembly and ELF bytes are *not* proof of function identity, reachability,
runtime ABI, complete CFG, or semantic equivalence. Fail closed on provenance.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from elftools.elf.elffile import ELFFile

import b01_overlap_elf_evidence as original

ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_COMMIT = "b9ca099903aeef5d4b33a7e83e8e7062ab94c65a"
TARGETS = (
    {"name": "T06_operator_delete_thumb", "task": "T06",
     "entry": 0x002C9115, "isa": "thumb", "length": 20},
    {"name": "T06_operator_new_array_thumb", "task": "T06",
     "entry": 0x002C9A25, "isa": "thumb", "length": 20},
    {"name": "T04_init_gap_arm", "task": "T04",
     "entry": 0x00071C50, "isa": "arm", "length": 24},
    {"name": "B01_known_12byte_cpp_control", "task": "B01",
     "entry": 0x000B9F7C, "isa": "arm", "length": 12},
)


def check_targets(queue):
    if (queue.get("task_count") != 40 or queue.get("schema") != 1
            or queue.get("elf_sha256") != original.PINNED_ELF_SHA):
        raise ValueError("T39 queue does not match pinned ARM baseline")
    t04 = queue.get("t04", {})
    t06 = queue.get("t06", {})
    gaps = t04.get("candidates", [])
    reviews = t06.get("candidates", [])
    if (len(gaps) != t04.get("interval_count")
            or len(reviews) != t06.get("current_review_count")):
        raise ValueError("T04/T06 work queue truncated")
    starts = set()
    for item in gaps:
        addr = int(item["address"], 16)
        size = item["size"]
        if type(size) is not int or size <= 0:
            raise ValueError("T04 interval invalid")
        if addr in starts:
            raise ValueError("Duplicate T04 interval")
        starts.add(addr)
    review_addresses = [int(x["address"], 16) for x in reviews]
    if len(review_addresses) != len(set(review_addresses)):
        raise ValueError("Duplicate T06 review address")
    for target in TARGETS:
        if target["task"] == "T04" and target["entry"] not in starts:
            raise ValueError("T04 target absent from current unknown intervals")
        if target["task"] == "T06" and target["entry"] not in review_addresses:
            raise ValueError("T06 Thumb target absent from live review queue")
    return True


def analyze_window(data, entry, isa):
    if isa not in ("arm", "thumb") or not data:
        raise ValueError("Invalid disassembly window")
    physical = entry & ~1 if isa == "thumb" else entry
    if isa == "arm" and physical % 4:
        raise ValueError("A32 address not word aligned")
    if isa == "thumb" and not (entry & 1) and physical % 2:
        raise ValueError("Thumb address invalid")
    disasm = Cs(CS_ARCH_ARM, CS_MODE_THUMB if isa == "thumb" else CS_MODE_ARM)
    instructions = list(disasm.disasm(data, physical))
    seen = []
    for op in instructions:
        if len(seen) >= 8:
            break
        seen.append({
            "address": "0x%08x" % op.address,
            "size": op.size,
            "mnemonic": op.mnemonic,
            "instruction_bytes_sha256": hashlib.sha256(bytes(op.bytes)).hexdigest(),
        })
    return {
        "physical_entry": "0x%08x" % physical,
        "entry_isa": isa,
        "original_bytes_sha256": hashlib.sha256(data).hexdigest(),
        "requested_bytes": len(data),
        "decoded_prefix_bytes": sum(op.size for op in instructions),
        "first_instructions": seen,
        "linear_decode_not_a_cfg": True,
    }


def check_control(result):
    # B01 12-byte method already proved on an independent differential path;
    # this smoke only checks that the originally reviewed local pattern survives.
    rows = result["first_instructions"]
    if (result["entry_isa"] != "arm" or result["requested_bytes"] != 12
            or result["decoded_prefix_bytes"] != 12 or len(rows) != 3
            or [x["mnemonic"] for x in rows] != ["mov", "str", "bx"]):
        raise ValueError("Reviewed 12-byte B01 control pattern changed")


def audit(binary, queue, optional_bundle=None):
    check_targets(queue)
    if original.sha256(binary) != original.PINNED_ELF_SHA:
        raise ValueError("ELF SHA-256 differs from pinned baseline")
    targets = []
    with binary.open("rb") as stream:
        elf = ELFFile(stream)
        if elf.elfclass != 32 or elf["e_machine"] != "EM_ARM" or not elf.little_endian:
            raise ValueError("Expected little-endian original ELF32 ARM")
        for target in TARGETS:
            physical = target["entry"] & ~1 if target["isa"] == "thumb" else target["entry"]
            content, offset = original.read_executable(
                elf, stream, physical, target["length"])
            if content is None or offset is None:
                raise ValueError("Target lies outside file-backed executable PT_LOAD")
            decoded = analyze_window(content, target["entry"], target["isa"])
            if not decoded["first_instructions"]:
                raise ValueError("Undecodable start for reviewed target")
            if target["task"] == "B01":
                check_control(decoded)
            decoded.update({
                "name": target["name"], "task": target["task"],
                "declared_entry": "0x%08x" % target["entry"],
                "file_offset": offset,
                "original_elf_verified": True,
                "original_function_body_fully_verified": False,
                "run_inside_original_game_proven": False,
                "original_cpp_equivalence_newly_proven": False,
            })
            targets.append(decoded)
    reference = {
        "schema": 1, "study": "T04_T06_Craft_Anything_crosscheck_pilot",
        "elf_sha256": original.PINNED_ELF_SHA,
        "craft_anything_upstream_commit": UPSTREAM_COMMIT,
        "capstone_reference_targets": targets,
        "original_elf_executable_bytes_verified": len(targets),
        "craft_anything_runtime_executed": False,
        "craft_anything_disassembly_compared": False,
        "craft_evidence_queue_matches": None,
        "new_structural_approvals": 0,
        "new_semantic_certificates": 0,
        "tasks_closed": [],
        "next_step": "Obtain an actual local Craft Anything evidence bundle, then review ISA, instruction boundaries and xrefs independently",
    }
    if optional_bundle is not None:
        import t39_craft_anything_bridge as bridge
        # Only match *metadata*, never copy third-party pseudo-C/source/bytes.
        annotated = bridge.reconcile(queue, optional_bundle)
        reference["craft_evidence_queue_matches"] = annotated["queue_matches"]
        reference["craft_anything_disassembly_compared"] = False
        reference["third_party_evidence_ids_not_cryptographically_verified"] = True
    return reference


def markdown(report):
    lines = [
        "# Piloto T04/T06: referência ARM original para comparação externa", "",
        f"ELF original SHA-256: \`{report['elf_sha256']}\`", "",
        f"Craft Anything commit avaliado por código-fonte: \`{UPSTREAM_COMMIT}\`", "",
        "| Alvo | Entrada | ISA | Instruções iniciais (Capstone) |",
        "|---|---|---|---|",
    ]
    for x in report["capstone_reference_targets"]:
        ops = ", ".join(i["mnemonic"] for i in x["first_instructions"])
        lines.append(f"| {x['name']} | \`{x['declared_entry']}\` | "
                     f"{x['entry_isa']} | {ops} |")
    lines += ["", "Os endereços Thumb preservam o bit de ISA nas entradas; os bytes",
              "são lidos do endereço físico alinhado. Os SHA-256 são derivados",
              "exclusivamente do ELF original fixado.", "",
              "**Não foi executado o Craft Anything nesta medição.** A diferença",
              "entre duas desmontagens só poderá ser afirmada quando houver um",
              "bundle produzido separadamente no ambiente autorizado.", "",
              "Nenhuma função nova, checkpoint aprovado, equivalência C++ ou",
              "certificado semântico decorre desta referência.", ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--queue", type=Path, required=True)
    p.add_argument("--bundle", type=Path, default=None,
                   help="Optional locally exported Craft Anything v1 bundle, never uploaded to CI")
    p.add_argument("--json-output", type=Path, required=True)
    p.add_argument("--md-output", type=Path, required=True)
    args = p.parse_args()
    if args.bundle:
        import t39_craft_anything_bridge as bridge
        optional_bundle = bridge.load_limited(args.bundle)
    else:
        optional_bundle = None
    result = audit(args.binary, json.loads(args.queue.read_text(encoding="utf-8")),
                   optional_bundle=optional_bundle)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.md_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
    args.md_output.write_text(markdown(result), encoding="utf-8")
    print("T39_CRAFT_PILOT_ORIGINAL_WINDOWS=" + str(len(result["capstone_reference_targets"])))
    print("T39_CRAFT_PILOT_EXTERNAL_ANALYSIS_EXECUTED=0")
    print("T39_CRAFT_PILOT_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
