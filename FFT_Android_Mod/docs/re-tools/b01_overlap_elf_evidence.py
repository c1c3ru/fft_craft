#!/usr/bin/env python3
"""B01 ELF32/ARM evidence for overlapping declared function intervals.

Static-only: decoding bytes and bounded CFG cannot establish runtime
reachability, full function identity, or semantic equivalence.
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_OP_IMM
from elftools.elf.elffile import ELFFile

PINNED_ELF_SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
TOOL_SCHEMA = 1


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get_entries(path):
    groups = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = csv.DictReader(f)
        if list(rows.fieldnames or ()) != [
                "address", "size", "mangled", "demangled", "status", "section_ref"]:
            raise ValueError("Unexpected function inventory schema")
        for row in rows:
            address = row["address"]
            if len(address) != 8 or any(c not in "0123456789abcdefABCDEF" for c in address):
                raise ValueError("Invalid address")
            size = int(row["size"])
            addr = int(address, 16)
            if not 0 < size <= 0xFFFFFFFF - addr:
                raise ValueError("Invalid interval")
            groups[addr].append((size, row["mangled"], row["demangled"]))
    entries = []
    for addr, rows in groups.items():
        sizes = set(row[0] for row in rows)
        if len(sizes) != 1:
            raise ValueError("Conflicting sizes at one address")
        entries.append({"start": addr, "size": rows[0][0], "end": addr + rows[0][0],
                        "aliases": sorted(set(row[1] for row in rows))})
    return sorted(entries, key=lambda row: row["start"])


def get_pairs(entries):
    pairs = []
    for i, earlier in enumerate(entries):
        for later in entries[i+1:]:
            if later["start"] >= earlier["end"]:
                break
            pairs.append((earlier, later))
    return pairs


def read_executable(elf, stream, addr, length):
    for section in elf.iter_segments():
        if section["p_type"] != "PT_LOAD" or not (int(section["p_flags"]) & 1):
            continue
        start, offset, size = int(section["p_vaddr"]), int(section["p_offset"]), int(section["p_filesz"])
        if start <= addr and 0 <= length and addr+length <= start+size:
            stream.seek(offset+addr-start)
            data = stream.read(length)
            if len(data) != length:
                raise ValueError("Truncated file backed executable segment")
            return data, offset+addr-start
    return None, None


def inspect_entry(elf, f, decoder, row):
    start, length = row["start"], row["size"]
    evidence = {
        "address": f"{start:08x}", "declared_size": length,
        "aliases": row["aliases"], "mode": "A32_candidate",
        "decoded_full_interval": False, "executable_segment_verified": False,
        "first_instructions": [], "last_instruction": None,
        "unknown_cfg_or_reachability": True
    }
    if start % 4 or length % 4:
        evidence["reason"] = "unaligned_address_or_length_for_A32"
        return evidence
    data, offset = read_executable(elf, f, start, length)
    if data is None:
        evidence["reason"] = "not_in_file_backed_executable_load_segment"
        return evidence
    evidence["executable_segment_verified"] = True
    evidence["file_offset"] = offset
    evidence["interval_sha256"] = hashlib.sha256(data).hexdigest()
    decoded = list(decoder.disasm(data, start))
    consumed = sum(insn.size for insn in decoded)
    evidence["decoded_instructions"] = len(decoded)
    evidence["decoded_bytes"] = consumed
    evidence["decoded_full_interval"] = bool(decoded) and consumed == length
    if not evidence["decoded_full_interval"]:
        evidence["reason"] = "not_entirely_decodable_as_sequential_A32"
    evidence["first_instructions"] = [{
        "address": f"{insn.address:08x}", "bytes": insn.bytes.hex(),
        "mnemonic": insn.mnemonic, "operands": insn.op_str,
    } for insn in decoded[:4]]
    if decoded:
        last = decoded[-1]
        evidence["last_instruction"] = {"address": f"{last.address:08x}",
                                         "bytes": last.bytes.hex(),
                                         "mnemonic": last.mnemonic,
                                         "operands": last.op_str}
    evidence["internal_direct_branches"] = []
    addresses = {insn.address for insn in decoded}
    for insn in decoded:
        if insn.id in (ARM_INS_B, ARM_INS_BL, ARM_INS_BLX) and len(insn.operands) == 1:
            op = insn.operands[0]
            if op.type == ARM_OP_IMM:
                target = int(op.imm) & 0xFFFFFFFF
                if target in addresses:
                    evidence["internal_direct_branches"].append(
                        {"from": f"{insn.address:08x}", "to": f"{target:08x}",
                         "kind": insn.mnemonic})
    # Decoding a sequence is *not* control flow proof; inline data and
    # indirect transfers can still invalidate the interpretation.
    return evidence


def audit(binary, inventory):
    if sha256(binary) != PINNED_ELF_SHA:
        raise ValueError("Original ARM ELF SHA-256 mismatch")
    entries = get_entries(inventory)
    overlaps = get_pairs(entries)
    if len(overlaps) != 15:
        raise ValueError("Unexpected number of overlap pairs")
    relevant = {row["start"]: row for pair in overlaps for row in pair}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    with binary.open("rb") as stream:
        elf = ELFFile(stream)
        if elf["e_machine"] != "EM_ARM" or elf.elfclass != 32 or not elf.little_endian:
            raise ValueError("Expected ELF32 little-endian ARM")
        by_start = {f"{address:08x}": inspect_entry(elf, stream, decoder, row)
                    for address, row in sorted(relevant.items())}
        groups = defaultdict(list)
        pair_rows = []
        for left, right in overlaps:
            if left["end"] != right["end"]:
                raise ValueError("Unexpected non co-terminal overlap; review baseline first")
            a, b = f"{left['start']:08x}", f"{right['start']:08x}"
            first, second = by_start[a], by_start[b]
            groups[f"{left['end']:08x}"].extend((a, b))
            # The common suffix is literally identical because both ranges
            # refer to the same ELF bytes; this is NOT a proof that both
            # entrypoints execute that suffix or are valid function heads.
            suffix, _ = read_executable(elf, stream, right["start"], right["size"])
            pair_rows.append({
                "first": a, "second": b,
                "source_elf_sha256": PINNED_ELF_SHA,
                "common_end": f"{left['end']:08x}",
                "shared_suffix_sha256": hashlib.sha256(suffix).hexdigest() if suffix else None,
                "both_A32_ranges_decoded": first["decoded_full_interval"] and second["decoded_full_interval"],
                "classification": "co_terminal_candidate_requires_cfg_review",
                "evidence": [f"entry:{a}", f"entry:{b}", "same_file_backed_ELF_interval"],
                "needs_review": True,
                "instruction_semantic_equivalence_proven": False,
            })
    groups_out = []
    for end, values in sorted(groups.items()):
        starts = sorted(set(values))
        groups_out.append({"common_end": end, "entrypoints": starts,
                           "classification": "co_terminal_multiple_entry_candidates",
                           "cfg_verified": False, "runtime_reachability_verified": False})
    if len(groups_out) != 9:
        raise ValueError("Unexpected number of co-terminal groups")
    return {"schema": TOOL_SCHEMA, "stage": "B01",
            "elf_sha256": PINNED_ELF_SHA,
            "input_csv_sha256": sha256(inventory),
            "overlap_pairs_count": len(pair_rows),
            "co_terminal_groups_count": len(groups_out),
            "entries": by_start, "pairs": pair_rows, "groups": groups_out,
            "every_pair_has_disposition": True,
            "all_pairs_cfg_certified": False,
            "semantic_certificates_issued": 0, "B01_done": False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = audit(args.binary, args.inventory)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(f"B01_OVERLAP_PAIRS={report['overlap_pairs_count']}")
    print(f"B01_COTERMINAL_GROUPS={report['co_terminal_groups_count']}")
    print(f"B01_A32_FULLY_DECODED={sum(x['decoded_full_interval'] for x in report['entries'].values())}")
    print("B01_CFG_ALL_CERTIFIED=0")
    print("B01_SEMANTIC_CERTIFICATES_NEW=0")


if __name__ == "__main__":
    main()
