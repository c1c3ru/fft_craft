#!/usr/bin/env python3
"""Capture instruction-level ARM evidence for manual review; never certify semantics."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile

import jtable

ROOT = Path(__file__).resolve().parents[2]
DISCLAIMER = ("Static ARM-mode disassembly only. Reachability is heuristic; "
              "unvisited slots may be literal data. No semantic equivalence is proved.")


def read_function(binary, start, size):
    """Read one function from an executable, file-backed ELF LOAD segment."""
    if size <= 0 or size % 4 or start % 4:
        raise ValueError("ARM start and size must be nonzero multiples of four")
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


def evidence(record, data, limit_lines=70):
    start = int(record["address"], 16)
    seen, tables, unresolved = collect(data, start)
    slots = list(range(start, start + len(data), 4))
    gaps = [addr for addr in slots if addr not in seen]
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
             f'- Heuristically visited slots: {len(seen)}/{len(slots)}',
             f'- Unvisited 4-byte offsets: {len(gaps)} (not necessarily code)',
             f'- Candidate memory stores: {len(stores)}; calls: {len(calls)}',
             f'- Resolved jump dispatches: {len(tables)}; unresolved: {len(unresolved)}',
             "", "## Candidate dispatch destinations", ""]
    if not tables:
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
    lines.extend(["", "## Unvisited offsets (first 40)", "",
                  ", ".join(f'\x600x{a:x}\x60' for a in gaps[:40]) or "None",
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
        selected = list(csv.DictReader(stream))[:limit]
    output.mkdir(parents=True, exist_ok=True)
    index = ["# ARM review evidence index", "", DISCLAIMER, "",
             f"ELF SHA-256: \x60{digest}\x60", "",
             "| Address | Function | Evidence |",
             "|---|---|---|"]
    count = 0
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
        data = read_function(binary, int(addr, 16), int(record["size"]))
        (output / f"{addr}.md").write_text(evidence(record, data), encoding="utf-8")
        name = str(row["name"]).replace("|", "/")
        index.append(f'| \x60{addr}\x60 | {name} | [Evidence](semantic-evidence/{addr}.md) |')
        count += 1
    (results / "SEMANTIC_EVIDENCE_INDEX.md").write_text(
        "\n".join(index) + "\n", encoding="utf-8")
    print(f"Exported {count} evidence files (manual validation required)")


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
