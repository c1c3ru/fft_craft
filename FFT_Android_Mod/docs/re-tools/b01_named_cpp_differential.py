#!/usr/bin/env python3
"""B01: original ELF ARM method bodies vs independent nominal C++ memory API.

Bounded tests prove the specified 12-byte path's writes/return under synthetic
valid object buffers, NOT full class layout or in-game caller reachability.
"""
import argparse
import ctypes
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_PROT_ALL,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_CPSR

import b01_overlap_elf_evidence as original
import b01_seven_cpp_contracts as abi
import b01_three_op_c_differential as triple
import b01_two_op_c_differential as two

# Independently authored from reviewed original ELF ARM behavior, NOT from
# a generated disassembly file or the C++ implementation under test.
EXPECTED = {
    0x000b3518:(0x0,0),
    0x000b9f7c:(0x14,2),
    0x000b9fac:(0x14,8),
    0x000b9fb8:(0x14,1),
    0x000bdb60:(0x0,0),
    0x000be1dc:(0x20,0),
    0x0028de9c:(0x304,1)
}


def build_cpp(path, dest):
    subprocess.run(["c++","-std=c++17","-O2","-Wall","-Wextra",
                    "-Werror","-pedantic","-fPIC","-shared",
                    str(path),"-o",str(dest)],check=True,capture_output=True)
    library=ctypes.CDLL(str(dest))
    fn=library.fft_b01_named_cpp_method
    fn.argtypes=[ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint8),
                 ctypes.c_size_t,ctypes.c_uint32]
    fn.restype=ctypes.c_int
    return fn


def check_opcode_contract(addr, raw, decoder):
    spec=triple.eligible_three(raw,addr,decoder)
    if spec is None or spec["third_kind"]!="bx_lr":
        raise ValueError("ELF no longer has a recognized 12-byte return body")
    first=spec["first_two"]["first"]
    second=spec["first_two"]["second"]
    off,value=EXPECTED[addr]
    # Exact instruction-level contract: MOV immediate -> STR word [R0,#off].
    if (first["opcode"]!="mov" or not first["immediate"] or
            first["operand"]!=value or first["dest"]!=second["rt"] or
            second["load"] or second["width"]!=4 or second["offset"]!=off):
        raise ValueError("Original ARM MOV/STR opcode contract changed")
    return spec


def compare_case(addr, raw, field, value, cpp, shift, seed, flags, lr):
    if shift not in abi.SHIFTS or seed not in abi.SEEDS or flags not in abi.FLAGS or lr not in abi.LRS:
        raise ValueError("Unsupported scenario")
    registers, baseline_mem=two.sample_state(seed)
    registers[0]=two.DATA_BASE+shift
    buffer=(ctypes.c_uint8*two.MEM_SIZE).from_buffer_copy(baseline_mem)
    ptr=ctypes.cast(ctypes.byref(buffer,shift),ctypes.POINTER(ctypes.c_uint8))
    if cpp(addr,ptr,two.MEM_SIZE-shift,registers[1])!=0:
        raise AssertionError("Nominal C++ rejected valid object backing storage")
    expected=bytes(buffer)
    if expected[abi.CANARY_START:abi.CANARY_START+16]!=two.CANARY:
        raise AssertionError("C++ wrote outside synthetic bounded object")
    if int.from_bytes(expected[shift+field:shift+field+4],"little")!=value:
        raise AssertionError("Nominal C++ did not store expected field value")

    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for page in sorted({addr & ~0xfff,(addr+8)&~0xfff,two.DATA_BASE,lr}):
        uc.mem_map(page,0x1000,UC_PROT_ALL)
    uc.mem_write(addr,raw)
    uc.mem_write(two.DATA_BASE,bytes(baseline_mem))
    uc.mem_write(lr,bytes(4))
    uc.reg_write(UC_ARM_REG_CPSR,0x10|flags)
    uc.reg_write(UC_ARM_REG_SP,0x700ffc)
    uc.reg_write(UC_ARM_REG_LR,lr)
    for reg,val in zip(two.REGS,registers):
        uc.reg_write(reg,val)
    trace,reads,writes=[],[],[]
    def instr(u,pc,size,_):
        trace.append(pc)
        if pc==lr: u.emu_stop()
    uc.hook_add(UC_HOOK_CODE,instr)
    uc.hook_add(UC_HOOK_MEM_READ,lambda u,k,a,w,v,_:reads.append((a,w)))
    uc.hook_add(UC_HOOK_MEM_WRITE,lambda u,k,a,w,v,_:writes.append((a,w,v)))
    uc.emu_start(addr,lr+4,timeout=1_000_000,count=4)
    if trace!=[addr,addr+4,addr+8,lr]:
        raise AssertionError("Original ELF did not execute complete 12-byte body")
    if reads or writes!=[(two.DATA_BASE+shift+field,4,value)]:
        raise AssertionError("Original ELF's read/write footprint differs")
    if bytes(uc.mem_read(two.DATA_BASE,two.MEM_SIZE))!=expected:
        raise AssertionError("C++ reimplementation diverges from original ELF memory")
    if uc.reg_read(UC_ARM_REG_PC)!=lr or uc.reg_read(UC_ARM_REG_LR)!=lr:
        raise AssertionError("Return via LR changed")
    if uc.reg_read(UC_ARM_REG_SP)!=0x700ffc:
        raise AssertionError("Stack state changed")
    if (uc.reg_read(UC_ARM_REG_CPSR)&0xf000003f)!=(flags|0x10):
        raise AssertionError("Flags/mode changed")
    if uc.reg_read(two.REGS[0])!=two.DATA_BASE+shift:
        raise AssertionError("R0 pointer changed")
    for reg in range(1,13):
        if uc.reg_read(two.REGS[reg])!=(value if reg==((int.from_bytes(raw[:4],"little")>>12)&15) else registers[reg]):
            raise AssertionError("Unexpected scratch-register side effect")
    return True


def reject_invalid_object_buffers(cpp):
    rejected=0
    for entry,(field,_) in EXPECTED.items():
        for n in (0,field,field+1,field+2,field+3):
            data=(ctypes.c_uint8*0x400)(*([0xa5]*0x400))
            state=bytes(data)
            rc=cpp(entry,data,n,0xffffffff)
            if rc!=-1 or bytes(data)!=state:
                raise AssertionError("Invalid C++ object size was accepted or mutated")
            rejected+=1
        if cpp(entry,None,field+4,0)!=-1:
            raise AssertionError("C++ accepted nullptr")
        rejected+=1
    data=(ctypes.c_uint8*16)(*([0xa5]*16))
    if cpp(0xeeeeeeee,data,16,0)!=-2 or bytes(data)!=bytes([0xa5]*16):
        raise AssertionError("C++ accepted unknown function entry")
    return rejected+1


def audit(binary, inventory, cpp_path):
    if original.sha256(binary)!=original.PINNED_ELF_SHA:
        raise ValueError("ELF digest mismatch")
    if set(EXPECTED)!=set(abi.SEVEN):
        raise ValueError("Named contracts no longer cover all seven unique entries")
    entries={r["start"]:r for r in original.get_entries(inventory)}
    names=abi.names_by_entry(inventory)
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    pending=[]
    with binary.open("rb") as f:
        elf=ELFFile(f)
        if elf.elfclass!=32 or not elf.little_endian or elf["e_machine"]!="EM_ARM":
            raise ValueError("Invalid ARM ELF")
        for addr,(field,value) in sorted(EXPECTED.items()):
            if addr not in entries or entries[addr]["size"]!=12:
                raise ValueError("Declared body size changed")
            raw,off=original.read_executable(elf,f,addr,12)
            if raw is None:
                raise ValueError("Missing body bytes")
            check_opcode_contract(addr,raw,decoder)
            pending.append((addr,raw,off,field,value))
    with tempfile.TemporaryDirectory(prefix="b01-named-cpp-") as d:
        cpp=build_cpp(cpp_path,Path(d)/"nominal.so")
        negatives=reject_invalid_object_buffers(cpp)
        rows=[]
        for addr,raw,off,field,value in pending:
            count=0
            for shift in abi.SHIFTS:
                for seed in abi.SEEDS:
                    for flags in abi.FLAGS:
                        for lr in abi.LRS:
                            compare_case(addr,raw,field,value,cpp,shift,seed,flags,lr)
                            count+=1
            rows.append({"entry":f"{addr:08x}","aliases":names[addr],
                         "original_file_offset":off,
                         "original_12_bytes_hex":raw.hex(),
                         "original_12_bytes_sha256":hashlib.sha256(raw).hexdigest(),
                         "memory_effect":{"base":"r0","offset_bytes":field,
                                          "width_bytes":4,"value_u32":value},
                         "return":"BX LR","scenarios_passed":count,
                         "nominal_Cpp_method_implemented":True,
                         "concrete_class_layout_proven":False,
                         "original_game_callers_verified":False,
                         "full_function_semantic_certificate":False})
    return {"schema":1,"stage":"B01","elf_sha256":original.PINNED_ELF_SHA,
            "cpp_source_sha256":hashlib.sha256(cpp_path.read_bytes()).hexdigest(),
            "unique_methods":len(rows),"scenarios_per_method":abi.REPETITIONS,
            "original_elf_vs_named_cpp_differentials":sum(r["scenarios_passed"] for r in rows),
            "cpp_invalid_size_and_entry_cases_rejected":negatives,
            "entries":rows,"cpp_class_layout_proven":False,
            "whole_program_call_context_proven":False,
            "new_semantic_certificates":0,"B01_done":False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--inventory",type=Path,required=True)
    p.add_argument("--cpp",type=Path,default=Path(__file__).parent/"c-models/b01_named_cpp_methods.cpp")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    r=audit(a.binary,a.inventory,a.cpp)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("B01_NAMED_CPP_METHODS="+str(r["unique_methods"]))
    print("B01_NAMED_CPP_DIFFERENTIALS="+str(r["original_elf_vs_named_cpp_differentials"]))
    print("B01_CPP_INVALID_CASES_REJECTED="+str(r["cpp_invalid_size_and_entry_cases_rejected"]))
    print("B01_CPP_PROGRAM_LEVEL_CERTIFICATES=0")


if __name__=="__main__":
    main()
