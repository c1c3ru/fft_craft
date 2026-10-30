#!/usr/bin/env python3
"""B01 3-op bounded ELF ARM vs independent C11; return is checked if BX LR.

Memory is synthetic; prefixes aren't proven globally reachable or complete
functions. No call/indirect targets other than exact BX LR are executed.
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
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE,
                     UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_PC,
                               UC_ARM_REG_SP, UC_ARM_REG_LR)

import b01_overlap_elf_evidence as original
import b01_two_op_c_differential as two
import b01_safe_alu_differential as alu

LR_SENTINEL = 0x710000
MAX_ENTRIES = 40
SEEDS = (0, 1, 0xffffffff, 0x7fffffff, 0x12345678, 0x80000000)
FLAGS = (0, 0xf0000000)
RETURN_OP = bytes.fromhex("1eff2fe1")


def eligible_three(raw, address, md):
    if len(raw) != 12:
        return None
    first=two.safe_pair(raw[:8], address, md)
    if first is None:
        return None
    third = "bx_lr" if raw[8:] == RETURN_OP else "alu" if alu.decode_safe(raw[8:]) else None
    if third is None:
        return None
    check = list(md.disasm(raw, address))
    if len(check) != 3 or sum(x.size for x in check) != 12:
        return None
    if third == "bx_lr" and (check[2].mnemonic != "bx" or check[2].op_str != "lr"):
        return None
    if third == "alu" and check[2].mnemonic != alu.decode_safe(raw[8:])["opcode"]:
        return None
    # ALU decoder can write R0; the C three-op deliberately rejects it.
    if third == "alu" and alu.decode_safe(raw[8:])["dest"] == 0:
        return None
    return {"first_two": first, "third_kind": third,
            "third_mnemonic": check[2].mnemonic}


def build_model(base, extra, output):
    subprocess.run(["cc","-std=c11","-O2","-Wall","-Wextra","-Werror",
                    "-pedantic","-fPIC","-shared",str(base),str(extra),
                    "-o",str(output)],check=True,capture_output=True)
    lib=ctypes.CDLL(str(output))
    fn=lib.b01_three_op_model
    fn.argtypes=([ctypes.c_uint32]*3 +
        [ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint8),
         ctypes.c_size_t,ctypes.c_uint32,ctypes.c_uint32,
         ctypes.POINTER(ctypes.c_uint32),ctypes.POINTER(ctypes.c_int)])
    fn.restype=ctypes.c_int
    return fn


def run_case(address, code, contract, c_model, seed, flags):
    regs, mem = two.sample_state(seed)
    before_mem=bytes(mem)
    rbuf=(ctypes.c_uint32*13)(*regs)
    mbuf=(ctypes.c_uint8*two.MEM_SIZE).from_buffer_copy(mem)
    opcodes=[int.from_bytes(code[i:i+4],"little") for i in (0,4,8)]
    out_pc=ctypes.c_uint32()
    did_return=ctypes.c_int()
    result=c_model(*opcodes,rbuf,mbuf,two.MEM_SIZE,
                   address, LR_SENTINEL, ctypes.byref(out_pc),
                   ctypes.byref(did_return))
    if result!=0:
        raise AssertionError("C11 refused whitelisted original ELF triple: "+str(result))
    expected_regs=list(rbuf)
    expected_bytes=bytes(mbuf)
    if expected_bytes[0x780:0x790]!=two.CANARY:
        raise AssertionError("C11 model violated canary")
    emu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for page in sorted({address & ~0xfff, (address+8) & ~0xfff,
                        two.DATA_BASE,LR_SENTINEL}):
        emu.mem_map(page,0x1000,UC_PROT_ALL)
    emu.mem_write(address,code)
    emu.mem_write(LR_SENTINEL,bytes(4))
    emu.mem_write(two.DATA_BASE,before_mem)
    emu.reg_write(UC_ARM_REG_CPSR,0x10|flags)
    for r,v in zip(two.REGS,regs):
        emu.reg_write(r,v)
    emu.reg_write(UC_ARM_REG_SP,0x700ffc)
    emu.reg_write(UC_ARM_REG_LR,LR_SENTINEL)
    trace,reads,writes=[],[],[]
    def record_code(uc,pc,size,_):
        trace.append(pc)
        if pc==LR_SENTINEL:
            uc.emu_stop()
    emu.hook_add(UC_HOOK_CODE,record_code)
    emu.hook_add(UC_HOOK_MEM_READ,lambda uc,access,a,size,val,_:reads.append((a,size)))
    emu.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,a,size,val,_:
                 writes.append((a,size,val&((1<<(size*8))-1))))
    limit = LR_SENTINEL+4 if contract["third_kind"]=="bx_lr" else address+12
    emu.emu_start(address,limit,timeout=1_000_000,count=4)
    expected_trace=[address,address+4,address+8]
    if contract["third_kind"]=="bx_lr":
        expected_trace.append(LR_SENTINEL)
    if trace!=expected_trace:
        raise AssertionError("Unexpected control trace "+str(trace))
    if emu.reg_read(UC_ARM_REG_PC)!=out_pc.value:
        raise AssertionError("ELF original PC differs from C modeled return/step")
    if did_return.value!=int(contract["third_kind"]=="bx_lr"):
        raise AssertionError("C return-state mismatch")
    if [emu.reg_read(r) for r in two.REGS]!=expected_regs:
        raise AssertionError("ELF vs C register divergence")
    if bytes(emu.mem_read(two.DATA_BASE,two.MEM_SIZE))!=expected_bytes:
        raise AssertionError("ELF vs C memory divergence")
    spec=contract["first_two"]["second"]
    expected_addr=two.DATA_BASE+spec["offset"]
    if spec["load"]:
        if reads!=[(expected_addr,spec["width"])] or writes:
            raise AssertionError("unexpected third-op memory effects")
    else:
        expected_val=expected_regs[spec["rt"]] & ((1<<(spec["width"]*8))-1)
        # Third ALU may change the source register AFTER the STR. Use the
        # register value from the original memory effects rather than final R.
        if len(writes)!=1 or writes[0][:2]!=(expected_addr,spec["width"]) or reads:
            raise AssertionError("unexpected store footprint")
        stored=int.from_bytes(expected_bytes[spec["offset"]:spec["offset"]+spec["width"]],"little")
        if writes[0][2]!=stored:
            raise AssertionError("unexpected stored value")
    if (emu.reg_read(UC_ARM_REG_SP)!=0x700ffc or
            emu.reg_read(UC_ARM_REG_LR)!=LR_SENTINEL):
        raise AssertionError("SP or LR changed")
    if (emu.reg_read(UC_ARM_REG_CPSR)&0xf000003f)!=(flags|0x10):
        raise AssertionError("CPSR changed")
    return True


def audit(binary, inventory, base_model, extra_model, limit=MAX_ENTRIES):
    if original.sha256(binary)!=original.PINNED_ELF_SHA:
        raise ValueError("Original ELF SHA mismatch")
    entries=original.get_entries(inventory)
    pairs=original.get_pairs(entries)
    if len(pairs)!=15:
        raise ValueError("Unexpected overlap baseline")
    overlap_addresses={row["start"] for pair in pairs for row in pair}
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    selected=[]
    with binary.open("rb") as stream:
        elf=ELFFile(stream)
        if elf.elfclass!=32 or not elf.little_endian or elf["e_machine"]!="EM_ARM":
            raise ValueError("ARM ELF32 required")
        for row in sorted(entries,key=lambda x:(x["start"] not in overlap_addresses,x["start"])):
            if row["size"]<12:
                continue
            raw,offset=original.read_executable(elf,stream,row["start"],12)
            if raw is None:
                continue
            contract=eligible_three(raw,row["start"],md)
            if contract:
                selected.append((row["start"],raw,contract,offset,row["size"]))
            if len(selected)==limit:
                break
    with tempfile.TemporaryDirectory(prefix="b01-three-op-") as temp:
        model=build_model(base_model,extra_model,Path(temp)/"model.so")
        results=[]
        for address,raw,contract,off,declared_size in selected:
            samples=0
            for seed in SEEDS:
                for flags in FLAGS:
                    run_case(address,raw,contract,model,seed,flags)
                    samples+=1
            results.append({
                "entry":f"{address:08x}","file_offset":off,
                "original_12_bytes":raw.hex(),
                "declared_entry_size_bytes":declared_size,
                "prefix_spans_declared_interval":declared_size==12,
                "modelled_return":contract["third_kind"]=="bx_lr",
                "contract":contract,"samples_passed":samples,
                "complete_original_function_contract":False,
                "runtime_entry_reachability_proven":False})
    return {"schema":1,"stage":"B01","original_elf_sha256":original.PINNED_ELF_SHA,
            "inventory_sha256":original.sha256(inventory),
            "c11_model_sha256":hashlib.sha256(extra_model.read_bytes()).hexdigest(),
            "unique_entries_scanned":len(entries),
            "three_opcode_eligible":len(results),
            "return_prefix_candidates":sum(x["modelled_return"] for x in results),
            "bounded_return_prefixes_covering_declared_interval":sum(
                x["modelled_return"] and x["prefix_spans_declared_interval"] for x in results),
            "samples_passed":sum(x["samples_passed"] for x in results),
            "entries":results,"whole_function_certificates":0,
            "indirect_non_lr_paths_executed":0,"B01_done":False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--inventory",type=Path,required=True)
    p.add_argument("--base-model",type=Path,default=Path(__file__).parent/"c-models/b01_two_op.c")
    p.add_argument("--extra-model",type=Path,default=Path(__file__).parent/"c-models/b01_three_op.c")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    r=audit(a.binary,a.inventory,a.base_model,a.extra_model)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("B01_ELF_ENTRIES_SCANNED="+str(r["unique_entries_scanned"]))
    print("B01_THREE_OPCODE_CANDIDATES="+str(r["three_opcode_eligible"]))
    print("B01_THREE_OPCODE_BXLR_CANDIDATES="+str(r["return_prefix_candidates"]))
    print("B01_BXLR_PREFIXES_COVERING_DECLARED_INTERVAL="+str(r["bounded_return_prefixes_covering_declared_interval"]))
    print("B01_THREE_OPCODE_ADDRESSES="+",".join(x["entry"] for x in r["entries"]))
    print("B01_THREE_OPCODE_DIFFERENTIAL_SAMPLES="+str(r["samples_passed"]))
    print("B01_WHOLE_FUNCTION_CERTIFICATES=0")


if __name__=="__main__":
    main()
