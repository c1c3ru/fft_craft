#!/usr/bin/env python3
"""Evidence-only original ELF direct A32 BL callsite inventory for A04.

Only immediate A32 BL encodings in executable PT_LOAD file-backed bytes.
No Thumb decoding, relocation-generated calls, or proof of reachability.
Local windows are candidates, possibly containing inline data.
"""
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL, ARM_OP_IMM
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
from semantic_a04_714a0_slot import SHA

TARGETS = (0xb6620, 0xb45d0)
MASK = 0xffffffff

def decode_arm_bl(word, pc):
    """Return direct A32 BL target, or None; excludes BLX immediate."""
    cond = word >> 28
    if cond == 0xf or ((word >> 25) & 0x7) != 0b101 or not (word & (1 << 24)):
        return None
    displacement = (word & 0xffffff) << 2
    if displacement & (1 << 25):
        displacement -= 1 << 26
    return (pc + 8 + displacement) & MASK

def encode_test_bl(pc, target):
    offset = target - (pc + 8)
    if offset % 4 or not -(1 << 25) <= offset < (1 << 25):
        raise ValueError("Non-encodable A32 BL displacement")
    return 0xeb000000 | ((offset >> 2) & 0xffffff)

def scan_original(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ELF SHA does not match A04")
    candidates, segments = [], []
    with binary.open("rb") as fh:
        elf = ELFFile(fh)
        if elf.elfclass != 32 or elf["e_machine"] != "EM_ARM":
            raise ValueError("Expected ARM32 ELF")
        symbols = []
        for sec in elf.iter_sections():
            if not isinstance(sec, SymbolTableSection):
                continue
            for sym in sec.iter_symbols():
                if sym["st_info"]["type"] != "STT_FUNC":
                    continue
                addr = int(sym["st_value"]) & ~1
                size = int(sym["st_size"])
                if size:
                    symbols.append((addr, addr+size, sym.name))
        md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        md.detail = True
        for seg_index, seg in enumerate(elf.iter_segments()):
            if seg["p_type"] != "PT_LOAD" or not (int(seg["p_flags"]) & 1):
                continue
            vaddr, file_size, offset = (int(seg["p_vaddr"]),
                                        int(seg["p_filesz"]), int(seg["p_offset"]))
            fh.seek(offset)
            raw = fh.read(file_size)
            if len(raw) != file_size:
                raise ValueError("Truncated executable PT_LOAD")
            segments.append({"index": seg_index, "vaddr": f"{vaddr:08x}",
                             "file_size": file_size, "scan": "aligned_A32_words_only"})
            first = (-vaddr) % 4
            for k in range(first, len(raw)-3, 4):
                pc = vaddr+k
                word = int.from_bytes(raw[k:k+4], "little")
                dest = decode_arm_bl(word, pc)
                if dest not in TARGETS:
                    continue
                parsed = list(md.disasm(raw[k:k+4], pc))
                if (len(parsed) != 1 or parsed[0].id != ARM_INS_BL
                        or not parsed[0].operands
                        or parsed[0].operands[0].type != ARM_OP_IMM
                        or int(parsed[0].operands[0].imm) != dest):
                    continue
                near = [n for n in symbols if n[0] <= pc < n[1]]
                start = max(first, k-32)
                context = [{"pc": f"{i.address:08x}", "mnemonic": i.mnemonic,
                            "operands": i.op_str, "hex": i.bytes.hex()}
                           for i in md.disasm(raw[start:min(len(raw), k+36)], vaddr+start)]
                candidates.append({"callsite": f"{pc:08x}", "target": f"{dest:08x}",
                                   "opcode": raw[k:k+4].hex(),
                                   "symbol_owners": [{"name": n[2], "start": f"{n[0]:08x}",
                                                       "end": f"{n[1]:08x}"} for n in near],
                                   "context_linear_not_cfg": context,
                                   "reachability_proven": False,
                                   "buffer_capacity_proven": False})
    candidates.sort(key=lambda a: (a["target"],a["callsite"]))
    return {"schema": 1, "elf_sha256": SHA, "targets": [f"{i:08x}" for i in TARGETS],
            "scope": "file_backed_executable_A32_BL_only_not_Thumb_or_indirect",
            "segments_scanned": segments,
            "direct_bl_candidates": candidates,
            "target_counts": {f"{target:08x}": sum(i["target"] == f"{target:08x}"
                                               for i in candidates) for target in TARGETS},
            "source_buffer_capacity_verified": False,
            "actual_jni_reachability_verified": False,
            "new_certificates": 0}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    result = scan_original(a.binary)
    data = json.dumps(result, sort_keys=True, indent=2)+"\n"
    a.output.parent.mkdir(parents=True, exist_ok=True)
    if a.output.exists() and a.output.read_text(encoding="utf-8") != data:
        raise ValueError("A04 callsite inventory replay mismatch")
    a.output.write_text(data, encoding="utf-8")
    lines = ["# A04 — direct A32 BL callsites from original ELF", "",
             "Static file-backed scan, not a reachable CFG or Android runtime proof.",
             "Indirect/Thumb calls remain out of scope.", "", "## Candidate callsites", ""]
    for row in result["direct_bl_candidates"]:
        lines.append(f"- {row['callsite']} -> {row['target']} "
                     f"symbol owners: {', '.join(x['name'] for x in row['symbol_owners']) or 'unknown'}")
        lines.extend(f"  - {i['pc']}: {i['mnemonic']} {i['operands']}"
                     for i in row["context_linear_not_cfg"])
    lines.extend(["", "## Unresolved checks", "",
                  "- Validate code/data boundaries, CFG paths, callers and pointer provenance.",
                  "- Find a proven allocation/capacity for R0 and a bounded NUL-terminated R1.",
                  "- Evaluate Thumb, indirect BLX, pointer aliases and JNI invocation separately.",
                  "- Do not infer buffer safety from a synthetic Unicorn allocation.", ""])
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text("\n".join(lines), encoding="utf-8")
    print("A04_A32_DIRECT_BL_COUNTS=" + json.dumps(result["target_counts"]))
    for row in result["direct_bl_candidates"]:
        print("A04_A32_CALLSITE " + row["callsite"] + " -> " + row["target"] +
              " symbol=" + ",".join(x["name"] for x in row["symbol_owners"]))
        for x in row["context_linear_not_cfg"]:
            print("A04_A32_CONTEXT " + x["pc"] + " " + x["mnemonic"] + " " + x["operands"])
    print("A04_REAL_BUFFER_PROVEN=0")

if __name__ == "__main__":
    main()
