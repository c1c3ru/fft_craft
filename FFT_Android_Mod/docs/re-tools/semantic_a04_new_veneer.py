#!/usr/bin/env python3
"""Prove original ARM veneer 0x2cdf6c branches to Thumb _Znwj.

Only the veneer executes. The actual operator new and its internal allocator
are never entered. This gate does not establish successful runtime allocation.
"""
import argparse
import hashlib
import json
from pathlib import Path

from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1,
                               UC_ARM_REG_SP, UC_ARM_REG_LR,
                               UC_ARM_REG_IP, UC_ARM_REG_PC, UC_ARM_REG_CPSR)
import semantic_evidence
from semantic_a04_714a0_slot import SHA
from semantic_a04_alloc_provenance import ALLOC, resolve_literal_veneer

THUMB_ENTRY = 0x2c99b5
WORD = 0xffffba3d
SYM = "_Znwj"
SIZE = 0x10c


def verify_target(row):
    names = [s["name"] for s in row["matching_function_symbols"]]
    if (not row["first_veneer_verified"] or row["literal_word_le"] != f"{WORD:08x}"
            or row["literal_addr"] != f"{ALLOC+12:08x}"
            or row["computed_destination"] != f"{THUMB_ENTRY:08x}"
            or row["thumb_state"] is not True or SYM not in names):
        raise ValueError("Original veneer does not resolve to Thumb _Znwj")
    return {"mangled_symbol": SYM, "semantic_symbol": "operator new(unsigned int)",
            "thumb_entry": f"{THUMB_ENTRY:08x}", "argument_size_bytes": SIZE}


def bounded_original_veneer(binary):
    data = semantic_evidence.read_function(binary, ALLOC, 16)
    target = THUMB_ENTRY & ~1
    cases = 0
    for size in (0, 0x108, 0x10c, 0x200):
        for nzcv in (0, 0xf0000000):
            uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
            uc.mem_map(ALLOC & ~0xfff, 0x1000, UC_PROT_ALL)
            uc.mem_map(target & ~0xfff, 0x1000, UC_PROT_ALL)
            uc.mem_write(ALLOC, data)
            uc.reg_write(UC_ARM_REG_CPSR, 0x10 | nzcv)
            before = [(UC_ARM_REG_R0, size), (UC_ARM_REG_R1, 0xabcdef12),
                      (UC_ARM_REG_SP, 0x600ffc), (UC_ARM_REG_LR, 0x730000)]
            for register, value in before:
                uc.reg_write(register, value)
            uc.reg_write(UC_ARM_REG_IP, 0x11111111)
            visited, reads, writes = [], [], []
            def on_code(emu, addr, width, unused):
                visited.append(addr)
                if addr == target:
                    emu.emu_stop()  # do NOT execute operator new
                elif addr not in (ALLOC, ALLOC+4, ALLOC+8):
                    raise AssertionError("Unknown original code reached")
            uc.hook_add(UC_HOOK_CODE,on_code)
            uc.hook_add(UC_HOOK_MEM_READ,
                        lambda e, t, addr, width, val, u: reads.append((addr,width)))
            uc.hook_add(UC_HOOK_MEM_WRITE,
                        lambda e, t, addr, width, val, u: writes.append((addr,width,val)))
            uc.emu_start(ALLOC, target + 2, count=8, timeout=1000000)
            if visited != [ALLOC, ALLOC+4, ALLOC+8, target]:
                raise AssertionError(f"Unexpected ARM veneer PC sequence: {visited}")
            if reads != [(ALLOC+12,4)] or writes:
                raise AssertionError("Unexpected original ARM veneer memory effects")
            if uc.reg_read(UC_ARM_REG_IP) != THUMB_ENTRY:
                raise AssertionError("Original ARM IP relative add was incorrect")
            if uc.reg_read(UC_ARM_REG_PC) != target:
                raise AssertionError("Original ARM indirect PC target changed")
            cpsr = uc.reg_read(UC_ARM_REG_CPSR)
            if not (cpsr & 0x20) or (cpsr & 0xf0000000) != nzcv:
                raise AssertionError("Original ARM-to-Thumb transition / flags incorrect")
            for register, value in before:
                if uc.reg_read(register) != value:
                    raise AssertionError("Original veneer modified preserved argument/register")
            cases += 1
    return cases


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    if hashlib.sha256(a.binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ELF digest changed")
    record=verify_target(resolve_literal_veneer(a.binary))
    record.update({"schema":1, "elf_sha256":SHA,
                   "bounded_original_veneer_cases":bounded_original_veneer(a.binary),
                   "operator_new_executed":False,
                   "transitive_allocator_executed":False,
                   "source_capacity_proven":False,
                   "new_certificates":0})
    payload=json.dumps(record, sort_keys=True, indent=2)+"\n"
    a.output.parent.mkdir(parents=True,exist_ok=True)
    if a.output.exists() and a.output.read_text(encoding="utf-8") != payload:
        raise ValueError("A04 ARM-to-Thumb evidence checkpoint drift")
    a.output.write_text(payload,encoding="utf-8")
    print("A04_NEW_VENEER="+json.dumps(record))
    print("A04_NEW_EXECUTED=0")


if __name__=="__main__":
    main()
