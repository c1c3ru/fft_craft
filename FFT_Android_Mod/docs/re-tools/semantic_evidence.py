#!/usr/bin/env python3
"""Capture instruction-level ARM evidence for manual review; never certify semantics."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_INS_LDR, ARM_OP_MEM, ARM_REG_PC
from elftools.elf.elffile import ELFFile

import jtable

ROOT = Path(__file__).resolve().parents[2]
DISCLAIMER = ("Static ARM-mode disassembly only. Reachability is heuristic; "
              "unvisited slots may be literal data. No semantic equivalence is proved.")


def read_function(binary, start, size):
    """Read one function from an executable, file-backed ELF LOAD segment."""
    if size <= 0 or start % 2:
        raise ValueError("Executable start must be halfword aligned and size positive")
    with binary.open("rb") as stream:
        elf = ELFFile(stream)
        for segment in elf.iter_segments():
            if (segment["p_type"] == "PT_LOAD" and segment["p_flags"] & 1
                    and segment["p_vaddr"] <= start
                    and start + size <= segment["p_vaddr"] + segment["p_filesz"]):
                stream.seek(segment["p_offset"] + start - segment["p_vaddr"])
                data = stream.read(size)
                if len(data) != size:
                    raise ValueError("Truncated executable segment")
                return data
    raise ValueError(f"No executable ELF segment covers 0x{start:x}+{size}")


def collect(data, start):
    """Reuse the structural walk and resolved dispatches as trace *candidates*."""
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    end = start + len(data)
    found = {}
    pending = [start]
    visited_dispatches = set()
    tables = []
    unresolved = set()
    for _ in range(32):
        if not pending:
            break
        decoded, dispatches = jtable.descend(md, data, start, end, pending)
        found.update(decoded)
        pending = []
        for target in dispatches:
            if target in visited_dispatches:
                continue
            visited_dispatches.add(target)
            count, destinations, guard = jtable.resolve_jump_table(
                md, data, start, found, target)
            if count is None:
                unresolved.add(target)
            else:
                tables.append((guard, target, destinations))
                pending.extend(x for x in destinations if start <= x < end)
    return found, tables, sorted(unresolved)


def collect_thumb(data, start):
    """Bounded Thumb linear scan, NOT a reachable-control-flow reconstruction.

    Thumb instructions are 2 or 4 bytes. Stop at a recognizable return; data
    may be interleaved with code, so no semantic validity is asserted.
    """
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    md.detail = True
    decoded = {}
    for insn in md.disasm(data, start):
        decoded[insn.address] = insn
        if ((insn.mnemonic in ("bx", "bx.w") and insn.op_str == "lr")
                or (insn.mnemonic.startswith("pop") and "pc" in insn.op_str)):
            break
    return decoded, [], []


def pc_relative_literals(instructions, start, data, thumb=False):
    """Identify in-range, PC-relative ARM LDR words as *candidate* literal pool data.

    This is not a semantic proof: referenced words may overlap code.
    """
    refs = {}
    end = start + len(data)
    for address, insn in sorted(instructions.items()):
        if insn.id != ARM_INS_LDR or len(insn.operands) < 2:
            continue
        operand = insn.operands[1]
        if (operand.type != ARM_OP_MEM or operand.mem.base != ARM_REG_PC
                or operand.mem.index):
            continue
        target = ((address + (4 if thumb else 8)) & ~3) + int(operand.mem.disp)
        if not (start <= target <= end - 4 and target % 4 == 0):
            continue
        offset = target - start
        refs.setdefault(target, {"value": int.from_bytes(data[offset:offset + 4], "little"),
                                 "load_sites": []})["load_sites"].append(address)
    return refs


def evidence(record, data, limit_lines=70, binary_sha256=None):
    tagged_start = int(record["address"], 16)
    thumb = bool(tagged_start & 1)
    start = tagged_start & ~1 if thumb else tagged_start
    seen, tables, unresolved = (collect_thumb(data, start) if thumb
                                else collect(data, start))
    alignment = 2 if thumb else 4
    slot_end = start + len(data) - (len(data) % alignment)
    slots = list(range(start, slot_end, alignment))
    observed = {ins.address + offset for ins in seen.values()
                for offset in range(0, ins.size, alignment)}
    gaps = [addr for addr in slots if addr not in observed]
    literals = pc_relative_literals(seen, start, data, thumb=thumb)
    referenced_gaps = [addr for addr in gaps if addr in literals]
    other_gaps = [addr for addr in gaps if addr not in literals]
    stores = [(addr, ins) for addr, ins in sorted(seen.items())
              if ins.mnemonic.startswith(("str", "stm", "vstr", "vstm", "strex", "swp"))
              or ins.mnemonic in ("push", "vpush")]
    calls = [(addr, ins) for addr, ins in sorted(seen.items())
             if ins.mnemonic.startswith(("bl", "blx"))]
    def line(addr, ins):
        return f"0x{addr:08x}: {ins.mnemonic} {ins.op_str}".rstrip()
    lines = [f'# ARM evidence: \x60{record["address"]}\x60 — {record["name"]}',
             "", DISCLAIMER, "",
             f'- Binary address: \x600x{start:x}\x60; size: {len(data)} bytes',
             f'- Checkpoint status: \x60{record["status"]}\x60 (unchanged)',
             f'- Instruction set: {"Thumb (tagged symbol address)" if thumb else "ARM"}',
             f'- Scan method: {"linear, stops at first recognized return; NOT a CFG" if thumb else "ARM recursive descent (heuristic)"}',
             f'- Heuristically decoded instruction slots: {len(observed)}/{len(slots)}',
             f'- Trailing bytes outside complete instructions: {len(data) % alignment}',
             f'- ELF SHA-256: `{binary_sha256 or "not supplied"}`',
             f'- Unvisited {alignment}-byte slots: {len(gaps)} (not necessarily code)',
             f'- Unvisited slots referenced by PC-relative LDR: {len(referenced_gaps)}',
             f'- Other unvisited slots: {len(other_gaps)}',
             f'- Candidate memory stores: {len(stores)}; calls: {len(calls)}',
             f'- Resolved ARM jump dispatches: {len(tables)}; unresolved: {len(unresolved)}',
             "", "## Candidate dispatch destinations", ""]
    if thumb:
        lines.append("Thumb jump-table analysis was not performed; unknown, not zero.")
    elif not tables:
        lines.append("None resolved by this pass.")
    for guard, dispatch, targets in tables:
        lines.append(f'- guard 0x{guard:x}, dispatch 0x{dispatch:x}, '
                     + f'targets: {", ".join(f"0x{x:x}" for x in targets)}')
    for addr in unresolved:
        lines.append(f'- unresolved dispatch 0x{addr:x}')
    lines.extend(["", "## Potential memory writes (first 30)", ""])
    lines += [f'- \x60{line(a, i)}\x60' for a, i in stores[:30]] or ["None identified."]
    lines.extend(["", "## Calls (first 30)", ""])
    lines += [f'- \x60{line(a, i)}\x60' for a, i in calls[:30]] or ["None identified."]
    lines.extend(["", "## Candidate PC-relative literal words", "",
                  "A reference suggests data, not a proven classification; it may overlap code.", ""])
    for addr in sorted(literals)[:40]:
        item = literals[addr]
        sites = ", ".join(f"0x{x:x}" for x in item["load_sites"])
        lines.append(f'- `0x{addr:x}`: 0x{item["value"]:08x}; referenced by {sites}')
    if not literals:
        lines.append("None identified.")
    lines.extend(["", "## Other unvisited instruction slots (first 40)", "",
                  ", ".join(f'`0x{a:x}`' for a in other_gaps[:40]) or "None",
                  "", f"## Visited instructions (first {limit_lines})", "",
                  "\x60\x60\x60asm"])
    lines += [line(a, i) for a, i in sorted(seen.items())[:limit_lines]]
    lines.extend(["\x60\x60\x60", "",
                  "## Still required for semantic validation", "",
                  "- Verify control-flow paths, input/output invariants and memory side effects.",
                  "- Compare return values and state changes against a specification or executable reference.",
                  "- Perform differential tests or execution traces before marking semantic equivalence.",
                  ""])
    return "\n".join(lines)


def run(binary, results, output, limit):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    queue = results / "REVIEW_QUEUE.csv"
    with queue.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    output.mkdir(parents=True, exist_ok=True)
    marker = f"ELF SHA-256: `{digest}`"

    def is_current(path):
        try:
            return path.is_file() and marker in path.read_text(encoding="utf-8")
        except OSError:
            return False

    selected = []
    for row in rows:
        address = row["address"].lower()
        if not is_current(output / f"{address}.md"):
            selected.append(row)
            if len(selected) >= limit:
                break

    for row in selected:
        addr = row["address"].lower()
        if len(addr) != 8 or any(c not in "0123456789abcdef" for c in addr):
            raise ValueError("Unexpected review address")
        checkpoint = results / f"{addr}.json"
        record = json.loads(checkpoint.read_text(encoding="utf-8"))
        if (record.get("address", "").lower() != addr
                or record.get("binary_sha256") != digest
                or record.get("status") != "needs_review"
                or record.get("pipeline_version") != 2):
            raise ValueError(f"Stale/invalid checkpoint {addr}")
        data = read_function(binary, int(addr, 16) & ~1, int(record["size"]))
        (output / f"{addr}.md").write_text(
            evidence(record, data, binary_sha256=digest), encoding="utf-8")

    index = ["# ARM review evidence index", "", DISCLAIMER, "",
             f"ELF SHA-256: `{digest}`", "",
             "These reports do not constitute semantic verification.", "",
             "| Address | Function | Evidence |",
             "|---|---|---|"]
    complete = 0
    for row in rows:
        addr = row["address"].lower()
        if is_current(output / f"{addr}.md"):
            name = str(row["name"]).replace("|", "/")
            index.append(f'| `{addr}` | {name} | [Evidence](semantic-evidence/{addr}.md) |')
            complete += 1
    index.insert(6, f"Evidence collected: **{complete}/{len(rows)}** pending functions.")
    (results / "SEMANTIC_EVIDENCE_INDEX.md").write_text(
        "\n".join(index) + "\n", encoding="utf-8")
    print(f"Evidence available for {complete}/{len(rows)} review functions")
    print(f"EVIDENCE_GENERATED={len(selected)}")



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=ROOT / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--results", type=Path, default=ROOT / "docs/re-results")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.limit <= 30:
        parser.error("--limit must be 1..30")
    run(args.binary, args.results, args.results / "semantic-evidence", args.limit)


if __name__ == "__main__":
    main()
