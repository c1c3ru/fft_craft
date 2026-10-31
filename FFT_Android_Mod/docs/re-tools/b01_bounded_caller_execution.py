#!/usr/bin/env python3
"""Execute bounded original-ELF caller->BL->12-byte callee->return traces.

Only controlled synthetic valid-memory states are tested; real game
reachability, complete object layout, and whole-function semantics stay open.
Fail closed if source bytes/opcodes, execution path, memory, or ABI drift.
"""
import argparse
import ctypes
import hashlib
import json
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL, ARM_OP_IMM
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC,
                               UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP)

import b01_overlap_elf_evidence as original
import b01_named_cpp_differential as cpp

# Audited original-ELF direct BL candidates, not declarations of live calls.
CASES = (
    {"caller": 0x000b9f88, "site": 0x000b9f90,
     "callee": 0x000b9f7c, "opcode": "f9ffffeb",
     "name": "CTHREAD::~CTHREAD -> RequestExit"},
    {"caller": 0x000be1e8, "site": 0x000be1f0,
     "callee": 0x000be1dc, "opcode": "f9ffffeb",
     "name": "CSTEP_BATCH::~CSTEP_BATCH -> Uninit"},
)
DATA = 0x600000
DATA_SIZE = 0x4000
STACK = 0x700000
STACK_SIZE = 0x4000
START_R0 = DATA + 0x1000
START_SP = STACK + 0x2000
REGS = [getattr(__import__("unicorn.arm_const", fromlist=["x"]),
                "UC_ARM_REG_R%d" % n) for n in range(13)]


def verify_callsite(raw, site, callee, opcode):
    if raw.hex() != opcode or len(raw) != 4:
        raise ValueError("Original ELF callsite opcode does not match reviewed bytes")
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    insns = list(decoder.disasm(raw, site))
    if len(insns) != 1 or insns[0].id != ARM_INS_BL:
        raise ValueError("Expected an unconditional A32 BL")
    ins = insns[0]
    if (ins.mnemonic != "bl" or len(ins.operands) != 1
            or ins.operands[0].type != ARM_OP_IMM
            or int(ins.operands[0].imm) != callee):
        raise ValueError("Original A32 BL destination is not the named callee")
    return True


def valid_this(this, offset):
    return (type(this) is int and type(offset) is int and
            DATA <= this and this + offset + 4 <= DATA + DATA_SIZE
            and this % 4 == 0)


def load_original(binary, inventory):
    if original.sha256(binary) != original.PINNED_ELF_SHA:
        raise ValueError("ELF changed from audited B01 reference")
    entries = {x["start"]: x for x in original.get_entries(inventory)}
    with binary.open("rb") as stream:
        elf = ELFFile(stream)
        if elf["e_machine"] != "EM_ARM" or elf.elfclass != 32 or not elf.little_endian:
            raise ValueError("Expected original ELF32 ARM little endian")
        original_bytes = []
        for case in CASES:
            owner = entries.get(case["caller"])
            child = entries.get(case["callee"])
            if (not owner or not child or child["size"] != 12
                    or not case["caller"] <= case["site"] <= owner["end"] - 4
                    or (case["site"] - owner["start"]) % 4):
                raise ValueError("Caller/child declared function bounds changed")
            body, _ = original.read_executable(
                elf, stream, owner["start"], owner["size"])
            callee, _ = original.read_executable(
                elf, stream, child["start"], 12)
            if body is None or callee is None:
                raise ValueError("Original executable code not file-backed")
            off = case["site"] - owner["start"]
            verify_callsite(body[off:off + 4], case["site"],
                            case["callee"], case["opcode"])
            cpp.check_opcode_contract(case["callee"], callee,
                                      Cs(CS_ARCH_ARM, CS_MODE_ARM))
            original_bytes.append((case, body, callee))
    return original_bytes


def execute_one(case, caller, callee, c_fn):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    mapped = set()
    for addr, raw in ((case["caller"], caller), (case["callee"], callee)):
        begin = addr & ~0xfff
        end = (addr + len(raw) + 0xfff) & ~0xfff
        for page in range(begin, end, 0x1000):
            if page not in mapped:
                uc.mem_map(page, 0x1000, UC_PROT_ALL)
                mapped.add(page)
        uc.mem_write(addr, raw)
    uc.mem_map(DATA, DATA_SIZE, UC_PROT_ALL)
    uc.mem_map(STACK, STACK_SIZE, UC_PROT_ALL)
    uc.mem_write(DATA, bytes((i * 37 + 11) % 256 for i in range(DATA_SIZE)))
    uc.mem_write(STACK, bytes((i * 7 + 19) % 256 for i in range(STACK_SIZE)))
    for idx, reg in enumerate(REGS):
        uc.reg_write(reg, START_R0 if idx == 0 else DATA + 0x1000 + idx * 0x80)
    uc.reg_write(UC_ARM_REG_SP, START_SP)
    uc.reg_write(UC_ARM_REG_LR, 0x720000)
    uc.reg_write(UC_ARM_REG_CPSR, 0x10)

    state = {"phase": "prefix", "trace": [], "writes": [], "problem": None}
    allowed = {case["site"], case["site"] + 4} | {
        case["callee"] + 4 * n for n in range(3)}
    def code_cb(engine, pc, width, _):
        if state["phase"] == "prefix":
            if pc == case["site"]:
                state["trace"].append(pc)
                engine.emu_stop()
                return
            if pc < case["caller"] or pc >= case["caller"] + len(caller):
                state["problem"] = "prefix escaped declared caller"
                engine.emu_stop()
                return
        else:
            if pc not in allowed:
                state["problem"] = "callee path escaped reviewed instructions"
                engine.emu_stop()
                return
        state["trace"].append(pc)
        if state["phase"] == "callee" and pc == case["site"] + 4:
            engine.emu_stop()

    def write_cb(engine, access, address, size, value, _):
        if state["phase"] == "callee":
            state["writes"].append((address, size, value))

    uc.hook_add(UC_HOOK_CODE, code_cb)
    uc.hook_add(UC_HOOK_MEM_WRITE, write_cb)
    uc.emu_start(case["caller"], case["site"] + 4, timeout=1_000_000, count=24)
    if state["problem"] or not state["trace"] or state["trace"][-1] != case["site"]:
        raise AssertionError(state["problem"] or "synthetic prefix did not reach reviewed BL")
    prefix = [f"{x:08x}" for x in state["trace"]]
    r0, r1 = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
    sp, flags = uc.reg_read(UC_ARM_REG_SP), uc.reg_read(UC_ARM_REG_CPSR)
    off, value = cpp.EXPECTED[case["callee"]]
    if not valid_this(r0, off):
        raise AssertionError("caller R0 does not point to safe synthetic object")

    before = bytes(uc.mem_read(DATA, DATA_SIZE))
    stack_before = bytes(uc.mem_read(STACK, STACK_SIZE))
    independent = (ctypes.c_uint8 * DATA_SIZE).from_buffer_copy(before)
    obj = ctypes.cast(ctypes.byref(independent, r0 - DATA),
                      ctypes.POINTER(ctypes.c_uint8))
    if c_fn(case["callee"], obj, DATA + DATA_SIZE - r0, r1) != 0:
        raise AssertionError("C++ contract rejected R0 object from caller")
    expected = bytes(independent)

    state.update(phase="callee", trace=[], writes=[], problem=None)
    uc.emu_start(case["site"], case["site"] + 8, timeout=1_000_000, count=8)
    expected_trace = [case["site"], case["callee"], case["callee"] + 4,
                      case["callee"] + 8, case["site"] + 4]
    if state["problem"] or state["trace"] != expected_trace:
        raise AssertionError(state["problem"] or "BL/callee/BX LR return path diverged")
    if state["writes"] != [(r0 + off, 4, value)]:
        raise AssertionError("Original callee memory-write footprint diverged")
    if (bytes(uc.mem_read(DATA, DATA_SIZE)) != expected
            or bytes(uc.mem_read(STACK, STACK_SIZE)) != stack_before):
        raise AssertionError("ARM memory effects differ from C++ on caller-derived R0")
    if (uc.reg_read(UC_ARM_REG_PC) != case["site"] + 4
            or uc.reg_read(UC_ARM_REG_LR) != case["site"] + 4
            or uc.reg_read(UC_ARM_REG_R0) != r0
            or uc.reg_read(UC_ARM_REG_SP) != sp
            or (uc.reg_read(UC_ARM_REG_CPSR) & 0xf000003f) !=
                (flags & 0xf000003f)):
        raise AssertionError("ABI return or CPSR/SP changed")
    return {
        "caller_entry": f"{case['caller']:08x}",
        "callsite": f"{case['site']:08x}",
        "callee_entry": f"{case['callee']:08x}",
        "name_hypothesis": case["name"],
        "prefix_original_elf_trace": prefix,
        "callee_original_elf_trace": [f"{x:08x}" for x in state["trace"]],
        "caller_r0_at_call": f"{r0:08x}",
        "caller_r1_at_call": f"{r1:08x}",
        "callee_effect": {"base": "caller_R0", "offset": off,
                          "width": 4, "value": value},
        "same_synthetic_memory_as_independent_cpp": True,
        "original_bl_to_bx_lr_return_executed": True,
        "in_game_reachability_proven": False,
        "real_game_object_layout_proven": False,
        "full_original_caller_body_executed": False,
        "whole_function_semantically_certified": False,
    }


def audit(binary, inventory, cpp_path):
    pairs = load_original(binary, inventory)
    with tempfile.TemporaryDirectory(prefix="b01-caller-path-") as temp:
        model = cpp.build_cpp(cpp_path, Path(temp) / "named.so")
        verified = [execute_one(case, caller, child, model)
                    for case, caller, child in pairs]
    return {
        "schema": 1, "task": "B01",
        "elf_sha256": original.PINNED_ELF_SHA,
        "cpp_sha256": hashlib.sha256(cpp_path.read_bytes()).hexdigest(),
        "bounded_caller_to_callee_returns": len(verified),
        "synthetic_controlled_reconstructions": verified,
        "original_process_executed": False,
        "real_caller_objects_proven": 0,
        "full_function_certificates_added": 0,
        "B01_done": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[2]
    parser.add_argument("--binary", type=Path,
                        default=root / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--inventory", type=Path,
                        default=root / "docs/RE_FUNCTION_INVENTORY.csv")
    parser.add_argument("--cpp-source", type=Path,
                        default=Path(__file__).parent / "c-models/b01_named_cpp_methods.cpp")
    parser.add_argument("--output", type=Path, required=True)
    a = parser.parse_args()
    outcome = audit(a.binary, a.inventory, a.cpp_source)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(outcome, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print("B01_BOUNDED_ORIGINAL_CALLS=" + str(outcome["bounded_caller_to_callee_returns"]))
    print("B01_NEW_FULL_SEMANTIC_CERTIFICATES=0")


if __name__ == "__main__":
    main()
