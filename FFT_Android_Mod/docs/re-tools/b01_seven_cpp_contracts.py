#!/usr/bin/env python3
"""B01: reviewable, bounded C++-ABI hypotheses for seven 12-byte ARM bodies.

A name suggesting a C++ member is not proof of a live object layout. This
proves finite input-state differentials on exact ELF bytes only, never global
reachability or universal equivalence.
"""
import argparse
import ctypes
import hashlib
import json
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

import b01_overlap_elf_evidence as baseline
import b01_three_op_c_differential as triple
import b01_two_op_c_differential as two

SEVEN = (0x000b3518, 0x000b9f7c, 0x000b9fac, 0x000b9fb8,
         0x000bdb60, 0x000be1dc, 0x0028de9c)
SHIFTS = (0, 0x40, 0x100, 0x200)
SEEDS = (0, 1, 0x7fffffff, 0x80000000, 0xffffffff, 0x12345678)
FLAGS = (0, 0xf0000000)
LRS = (0x710000, 0x720000)
REPETITIONS = len(SHIFTS) * len(SEEDS) * len(FLAGS) * len(LRS)
CANARY_START = 0x780


def names_by_entry(path):
    import csv
    by = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            start = int(row["address"], 16)
            if start in SEVEN:
                if int(row["size"]) != 12:
                    raise ValueError("Seven candidate body sizes drifted")
                by.setdefault(start, set()).add(row["demangled"])
    if set(by) != set(SEVEN):
        raise ValueError("Missing named entries in reference inventory")
    return {k: sorted(v) for k, v in by.items()}


def compare_full_declared_body(addr, raw, spec, c_model, seed, flags, shift, lr):
    if shift not in SHIFTS or lr not in LRS:
        raise ValueError("Invalid synthetic object/return scenario")
    regs, memory = two.sample_state(seed)
    regs[0] = two.DATA_BASE + shift
    # Independent C operates on the same logical object starting at R0,
    # while the emulator maps the full surrounding memory including canaries.
    reg_buf = (ctypes.c_uint32 * 13)(*regs)
    buf = (ctypes.c_uint8 * two.MEM_SIZE).from_buffer_copy(memory)
    c_object = ctypes.cast(ctypes.byref(buf, shift),
                           ctypes.POINTER(ctypes.c_uint8))
    pc = ctypes.c_uint32()
    did_return = ctypes.c_int()
    words = [int.from_bytes(raw[n:n+4], "little") for n in (0,4,8)]
    result = c_model(*words, reg_buf, c_object, two.MEM_SIZE-shift,
                     addr, lr, ctypes.byref(pc), ctypes.byref(did_return))
    if result != 0 or did_return.value != 1 or pc.value != lr:
        raise AssertionError("Independent C body model rejected return")
    expected = list(reg_buf)
    final_mem = bytes(buf)
    if expected[0] != two.DATA_BASE+shift:
        raise AssertionError("Original C++ this pointer not preserved")
    if final_mem[CANARY_START:CANARY_START+16] != two.CANARY:
        raise AssertionError("C model wrote outside synthetic object")

    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for base in sorted({addr & ~0xfff, (addr+8) & ~0xfff,
                        two.DATA_BASE, lr}):
        uc.mem_map(base, 0x1000, UC_PROT_ALL)
    uc.mem_write(addr, raw)
    uc.mem_write(two.DATA_BASE, bytes(memory))
    uc.mem_write(lr, bytes(4))
    uc.reg_write(UC_ARM_REG_CPSR, 0x10 | flags)
    uc.reg_write(UC_ARM_REG_SP, 0x700ffc)
    uc.reg_write(UC_ARM_REG_LR, lr)
    for r,v in zip(two.REGS,regs):
        uc.reg_write(r,v)
    executed, reads, writes = [], [], []
    def code_cb(emu, address, size, _):
        executed.append(address)
        if address == lr:
            emu.emu_stop()
    uc.hook_add(UC_HOOK_CODE, code_cb)
    uc.hook_add(UC_HOOK_MEM_READ,
                lambda emu, action, a, width, val, userdata:
                reads.append((a,width)))
    uc.hook_add(UC_HOOK_MEM_WRITE,
                lambda emu, action, a, width, val, userdata:
                writes.append((a,width,val & ((1 << (width*8))-1))))
    uc.emu_start(addr, lr+4, timeout=1_000_000, count=4)
    if executed != [addr,addr+4,addr+8,lr]:
        raise AssertionError("Original ELF did not take exactly its declared body")
    if uc.reg_read(UC_ARM_REG_PC) != lr or uc.reg_read(UC_ARM_REG_LR) != lr:
        raise AssertionError("ELF BX LR return destination mismatch")
    if uc.reg_read(UC_ARM_REG_SP) != 0x700ffc:
        raise AssertionError("Stack pointer mutated")
    if (uc.reg_read(UC_ARM_REG_CPSR)&0xf000003f) != (flags|0x10):
        raise AssertionError("CPSR mutated")
    if [uc.reg_read(r) for r in two.REGS] != expected:
        raise AssertionError("ARM-vs-C divergence in R0..R12")
    if bytes(uc.mem_read(two.DATA_BASE,two.MEM_SIZE)) != final_mem:
        raise AssertionError("ARM-vs-C object memory or canary mismatch")
    field = spec["first_two"]["second"]
    address = two.DATA_BASE+shift+field["offset"]
    if field["load"]:
        if reads != [(address,field["width"])] or writes:
            raise AssertionError("Invalid LDR/LDRB footprint")
    else:
        if reads or len(writes)!=1 or writes[0][:2]!=(address,field["width"]):
            raise AssertionError("Invalid STR/STRB footprint")
        contents=int.from_bytes(final_mem[shift+field["offset"]:
                                    shift+field["offset"]+field["width"]],"little")
        if writes[0][2] != contents:
            raise AssertionError("STR memory value mismatch")
    return True


def audit(binary, inventory, c_base, c_three):
    if baseline.sha256(binary)!=baseline.PINNED_ELF_SHA:
        raise ValueError("ELF digest does not match pinned original")
    inventory_rows=baseline.get_entries(inventory)
    lookup={x["start"]:x for x in inventory_rows}
    names=names_by_entry(inventory)
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    candidates=[]
    with binary.open("rb") as file:
        elf=ELFFile(file)
        if elf.elfclass!=32 or not elf.little_endian or elf["e_machine"]!="EM_ARM":
            raise ValueError("Expected ELF32 little-endian ARM")
        for addr in SEVEN:
            item=lookup.get(addr)
            if not item or item["size"]!=12:
                raise ValueError("Missing exact 12-byte body")
            raw,off=baseline.read_executable(elf,file,addr,12)
            if raw is None:
                raise ValueError("Body is not in file-backed executable LOAD segment")
            contract=triple.eligible_three(raw,addr,md)
            if contract is None or contract["third_kind"]!="bx_lr":
                raise ValueError("Original body no longer matches safe ALU/memory/BX LR")
            spec=contract["first_two"]["second"]
            if max(SHIFTS)+spec["offset"]+spec["width"] > CANARY_START:
                raise ValueError("Field touches memory safety canary")
            candidates.append((addr,raw,off,contract))
    with tempfile.TemporaryDirectory(prefix="b01-seven-c-") as tmp:
        model=triple.build_model(c_base,c_three,Path(tmp)/"three.so")
        report=[]
        for addr,raw,off,contract in candidates:
            count=0
            for shift in SHIFTS:
                for seed in SEEDS:
                    for flags in FLAGS:
                        for lr in LRS:
                            compare_full_declared_body(
                                addr,raw,contract,model,seed,flags,shift,lr)
                            count+=1
            spec=contract["first_two"]["second"]
            report.append({
                "entrypoint":f"{addr:08x}",
                "symbol_aliases":names[addr],
                "declared_function_body_size":12,
                "file_offset":off,"original_bytes_sha256":hashlib.sha256(raw).hexdigest(),
                "original_bytes_hex":raw.hex(),
                "arm_abi_hypothesis":"AAPCS32_r0_this_for_nonstatic_member",
                "symbol_names_not_abi_proof":True,
                "this_r0_preserved_in_tested_scenarios":True,
                "object_field_access":{"base_register":"r0","offset_bytes":spec["offset"],
                    "width_bytes":spec["width"],
                    "operation":"read" if spec["load"] else "write",
                    "minimum_backing_storage_bytes":spec["offset"]+spec["width"]},
                "field_name_and_class_layout_verified":False,
                "raw_arm_opcode_contract":contract,
                "return_mechanism":"BX LR","return_value":"r0_remains_this_pointer",
                "scenarios_passed":count,
                "declared_body_executed_all_scenarios":True,
                "caller_reachability_proven":False,
                "universally_proven":False,
                "semantic_certificate_issued":False})
    return {"schema":1,"task":"B01","issue":494,
            "elf_sha256":baseline.PINNED_ELF_SHA,
            "inventory_sha256":baseline.sha256(inventory),
            "c11_model_hashes":[hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (c_base,c_three)],
            "verified_12_byte_entrypoints":len(report),
            "unique_entrypoints_not_symbols":True,
            "scenarios_per_entry":REPETITIONS,
            "bounded_original_vs_c_scenarios_passed":sum(x["scenarios_passed"] for x in report),
            "entrypoints":report,
            "object_layout_proven":False,
            "external_callers_verified":False,
            "whole_function_semantic_certificates_added":0,
            "B01_done":False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--inventory",type=Path,required=True)
    p.add_argument("--c-base",type=Path,default=Path(__file__).parent/"c-models/b01_two_op.c")
    p.add_argument("--c-three",type=Path,default=Path(__file__).parent/"c-models/b01_three_op.c")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    report=audit(a.binary,a.inventory,a.c_base,a.c_three)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("B01_CPP_CONTRACT_BODIES="+str(report["verified_12_byte_entrypoints"]))
    print("B01_CPP_CONTRACT_SCENARIOS="+str(report["bounded_original_vs_c_scenarios_passed"]))
    for row in report["entrypoints"]:
        f=row["object_field_access"]
        print("B01_CPP_FIELD_"+row["entrypoint"]+"="+f["operation"]+
              ":r0+"+hex(f["offset_bytes"])+"/"+str(f["width_bytes"]))
    print("B01_COMPLETE_CPP_OBJECT_LAYOUT_PROVEN=0")
    print("B01_NEW_WHOLE_FUNCTION_CERTIFICATES=0")


if __name__=="__main__":
    main()
