#!/usr/bin/env python3
"""Trace original ARM 0x10c allocation-pattern callsites of A04.

Pattern recognition is structural, not proof of malloc semantics, actual
allocation success, source length, CFG reachability or JNI coverage.
"""
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
import semantic_evidence
from semantic_a04_b6620_xrefs import scan_original
from semantic_a04_714a0_slot import SHA

ALLOC = 0x2cdf6c
SIZE = 0x10c
TARGET = 0xb6620


def classify_candidate(row):
    seq = row["context_linear_not_cfg"]
    site = row["callsite"]
    indices = [i for i, ins in enumerate(seq) if ins["pc"] == site]
    if len(indices) != 1:
        raise ValueError("Callsite missing from linear A32 window")
    i = indices[0]
    # Look for immediate object-size mov followed by BL to 0x2cdf6c,
    # then only MOVs passing pointers up to the A04 callee.
    for j in range(max(0, i-7), i-1):
        a = seq[j]
        b = seq[j+1]
        between = seq[j+2:i]
        if (a["mnemonic"] == "mov" and a["operands"] == "r0, #0x10c"
                and b["mnemonic"] == "bl"
                and b["operands"] == "#0x2cdf6c"
                and 1 <= len(between) <= 4
                and all(x["mnemonic"] == "mov" for x in between)
                and any(x["operands"].startswith("r1, ") for x in between)
                and all(not x["operands"].startswith("r0, ") for x in between)):
            return {"matches_size_and_call": True,
                    "size": SIZE,
                    "size_immediate_pc": a["pc"],
                    "candidate_allocator_call": b["pc"],
                    "mov_before_target": between,
                    "candidate_source_in_r1": True,
                    "candidate_dest_is_result_r0": True,
                    "proven_allocation": False,
                    "proven_source_length": False}
    return {"matches_size_and_call": False,
            "proven_allocation": False, "proven_source_length": False}


def symbol_context(binary):
    matches = []
    with binary.open("rb") as stream:
        elf = ELFFile(stream)
        for section in elf.iter_sections():
            if not isinstance(section, SymbolTableSection):
                continue
            for sym in section.iter_symbols():
                if sym["st_info"]["type"] != "STT_FUNC":
                    continue
                addr = int(sym["st_value"]) & ~1
                length = int(sym["st_size"])
                if addr == ALLOC or (length and addr <= ALLOC < addr + length):
                    matches.append({"symbol_table": section.name, "name": sym.name,
                                    "start": f"{addr:08x}", "size": length,
                                    "binding": str(sym["st_info"]["bind"]),
                                    "type": str(sym["st_info"]["type"])})
    code = semantic_evidence.read_function(binary, ALLOC, 96)
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    ins = [{"pc": f"{x.address:08x}", "mnemonic": x.mnemonic,
            "operands": x.op_str, "hex": x.bytes.hex()}
           for x in decoder.disasm(code, ALLOC)]
    return {"address": f"{ALLOC:08x}", "symbol_matches": matches,
            "first_96_bytes_linear_not_cfg": ins,
            "allocation_semantics_proven": False}



def resolve_literal_veneer(binary):
    """Static A32 IP veneer: LDR ip,[pc,#4]; ADD ip,pc,ip; BX ip."""
    raw = semantic_evidence.read_function(binary, ALLOC, 16)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    ops = list(dis.disasm(raw[:12], ALLOC))
    signatures = [(i.mnemonic, i.op_str.replace(" ", "")) for i in ops]
    if signatures != [("ldr","ip,[pc,#4]"),("add","ip,pc,ip"),("bx","ip")]:
        raise ValueError(f"Unexpected original allocation-side veneer: {signatures}")
    literal = int.from_bytes(raw[12:16], "little")
    destination = (ALLOC + 12 + literal) & 0xffffffff
    aligned = destination & ~1
    functions = []
    with binary.open("rb") as fh:
        elf = ELFFile(fh)
        for section in elf.iter_sections():
            if not isinstance(section, SymbolTableSection):
                continue
            for sym in section.iter_symbols():
                if sym["st_info"]["type"] != "STT_FUNC":
                    continue
                start = int(sym["st_value"]) & ~1
                size = int(sym["st_size"])
                if start == aligned or (size and start <= aligned < start+size):
                    functions.append({"table": section.name, "name": sym.name,
                                      "start": f"{start:08x}", "size": size,
                                      "kind": str(sym["st_info"]["type"])})
    try:
        code = semantic_evidence.read_function(binary, aligned, 64)
    except ValueError:
        code = None
    decoded = []
    if code is not None:
        mode = CS_MODE_THUMB if destination & 1 else CS_MODE_ARM
        cap = Cs(CS_ARCH_ARM, mode)
        decoded = [{"pc":f"{i.address:08x}", "mnemonic":i.mnemonic,
                    "operands":i.op_str} for i in cap.disasm(code,aligned)]
    return {"first_veneer_verified": True,
            "literal_addr":f"{ALLOC+12:08x}",
            "literal_word_le":f"{literal:08x}",
            "computed_destination":f"{destination:08x}",
            "thumb_state":bool(destination & 1),
            "matching_function_symbols":functions,
            "destination_disasm_linear_not_cfg":decoded[:16],
            "transitive_runtime_allocator_verified":False}


def audit(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ELF digest does not match")
    refs = scan_original(binary)
    rows = []
    for r in refs["direct_bl_candidates"]:
        if r["target"] != f"{TARGET:08x}":
            continue
        rows.append({"callsite": r["callsite"],
                     "symbol_owners": r["symbol_owners"],
                     "structural_pattern": classify_candidate(r)})
    hits = [r for r in rows if r["structural_pattern"]["matches_size_and_call"]]
    if not hits:
        raise ValueError("No original 0x10c allocation pattern; do not infer buffer capacity")
    return {"schema": 1, "elf_sha256": SHA,
            "size_argument_bytes": SIZE,
            "required_bytes_for_field_0x104": 0x108,
            "candidate_allocator": symbol_context(binary),
            "literal_veneer": resolve_literal_veneer(binary),
            "target": f"{TARGET:08x}", "direct_a32_callsites": len(rows),
            "syntactic_size_and_return_chain_candidates": len(hits),
            "matching_callsites": hits, "runtime_allocation_verified": False,
            "source_length_verified": False, "jni_integration_verified": False,
            "new_certificates": 0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a=p.parse_args()
    record=audit(a.binary)
    payload=json.dumps(record, sort_keys=True, indent=2)+"\n"
    a.output.parent.mkdir(parents=True, exist_ok=True)
    if a.output.exists() and a.output.read_text(encoding="utf-8")!=payload:
        raise ValueError("A04 allocator evidence replay mismatch")
    a.output.write_text(payload, encoding="utf-8")
    print("A04_CANDIDATE_ALLOCATOR_SYMBOLS="+json.dumps(record["candidate_allocator"]["symbol_matches"]))
    for x in record["candidate_allocator"]["first_96_bytes_linear_not_cfg"][:14]:
        print("A04_ALLOCATOR_DISASM "+x["pc"]+" "+x["mnemonic"]+" "+x["operands"])
    print("A04_ALLOC_VENEER="+json.dumps(record["literal_veneer"]))
    print("A04_ALLOC_PATTERN_CALLS="+str(record["syntactic_size_and_return_chain_candidates"]))
    print("A04_ALLOC_PATTERN_TOTAL_CALLS="+str(record["direct_a32_callsites"]))
    for row in record["matching_callsites"]:
        print("A04_ALLOC_PATTERN_SITE="+row["callsite"]+" owner="+
              ",".join(x["name"] for x in row["symbol_owners"]))
    print("A04_ALLOC_PROVEN_IN_RUNTIME=0")
    print("A04_SOURCE_CAPACITY_PROVEN=0")


if __name__=="__main__":
    main()
