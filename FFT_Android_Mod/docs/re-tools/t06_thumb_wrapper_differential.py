#!/usr/bin/env python3
"""T06 Thumb wrapper slices: exact-ELF CFG, controlled callee and C++ differential.

The original callee BODY is NOT executed. We verify only wrappers' conditional
call forwarding, stack/register restoration and controlled return; full malloc
semantics, ELF caller reachability and JNI/Android integration remain unknown.
"""
import argparse
import json
import subprocess
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from capstone.arm import ARM_INS_B, ARM_INS_BL, ARM_OP_IMM
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_PROT_ALL
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R3, UC_ARM_REG_SP,
)

import b01_overlap_elf_evidence as original

ROOT = Path(__file__).resolve().parents[2]
STACK_BASE = 0x70000000
STACK_INIT = STACK_BASE + 0x800
RETURN_PC = 0x00300000
SAVED_R3 = 0x13579BDF
PAGE = 0x1000

SLICES = (
    {
        "id": "operator_delete", "model": "delete", "entry": 0x002C9115,
        "start": 0x002C9114, "bytes": 12, "symbol_bytes": 12,
        "callee": 0x002CE07C,
        "mnemonics": ("push", "cmp", "beq", "bl", "pop"),
        "sizes": (2, 2, 2, 4, 2),
    },
    {
        "id": "operator_new_array", "model": "new_array", "entry": 0x002C9A25,
        "start": 0x002C9A24, "bytes": 8, "symbol_bytes": 20,
        "callee": 0x002C99B4,
        "mnemonics": ("push", "bl", "pop"),
        "sizes": (2, 4, 2),
    },
)


def read_slice(elf, stream, item):
    code, _ = original.read_executable(
        elf, stream, item["start"], item["bytes"])
    if code is None or len(code) != item["bytes"]:
        raise ValueError("Original wrapper is not in executable ELF segment")
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    decoder.detail = True
    insns = list(decoder.disasm(code, item["start"]))
    if (tuple(i.mnemonic for i in insns) != item["mnemonics"] or
            tuple(i.size for i in insns) != item["sizes"] or
            sum(i.size for i in insns) != item["bytes"]):
        raise ValueError("Unexpected instruction boundaries or Thumb opcodes")
    if (not insns[0].op_str.replace(" ", "") == "{r3,lr}" or
            "pc" not in insns[-1].op_str or
            not insns[-1].op_str.replace(" ", "") == "{r3,pc}"):
        raise ValueError("Thumb stack save/return mask differs from fixture")
    direct = {}
    for insn in insns:
        if insn.id in (ARM_INS_B, ARM_INS_BL):
            if (len(insn.operands) != 1 or
                    insn.operands[0].type != ARM_OP_IMM):
                raise ValueError("Indirect target within assumed wrapper")
            direct[insn.address] = int(insn.operands[0].imm) & 0xffffffff
    if (item["model"] == "delete" and
            (direct.get(item["start"] + 4) != item["start"] + 10 or
             direct.get(item["start"] + 6) != item["callee"])):
        raise ValueError("Delete guard or external destination changed")
    if (item["model"] == "new_array" and
            direct.get(item["start"] + 2) != item["callee"]):
        raise ValueError("Allocator call destination changed")
    return code, insns


def static_edges(item, insns):
    """Bounded 2-branch CFG; each external call is a modeled return assumption."""
    ends = {x.address for x in insns}
    links = []
    for insn in insns:
        next_addr = insn.address + insn.size
        if insn.mnemonic == "pop":
            links.append({
                "from": "0x%08x" % insn.address, "to": "caller_lr",
                "kind": "return_via_stack"})
        elif insn.mnemonic == "bl":
            links.append({
                "from": "0x%08x" % insn.address,
                "to": "0x%08x" % item["callee"],
                "kind": "external_callee_unmodeled"})
            links.append({
                "from": "0x%08x" % insn.address, "to": "0x%08x" % next_addr,
                "kind": "assumed_return_from_external_callee"})
        elif insn.mnemonic == "beq":
            links.extend([
                {"from": "0x%08x" % insn.address,
                 "to": "0x%08x" % (item["start"] + 10),
                 "kind": "taken_Z_equals_1"},
                {"from": "0x%08x" % insn.address,
                 "to": "0x%08x" % next_addr,
                 "kind": "fallthrough_Z_equals_0"},
            ])
        elif next_addr in ends:
            links.append({
                "from": "0x%08x" % insn.address,
                "to": "0x%08x" % next_addr, "kind": "fallthrough"})
        else:
            raise ValueError("Unexpected unmodeled exit before return")
    return links


def execute_wrapper(item, code, input_r0, mocked_result):
    """Microexecute the *actual original wrapper*, with a BX LR callee stub."""
    if not 0 <= input_r0 <= 0xffffffff or not 0 <= mocked_result <= 0xffffffff:
        raise ValueError("Expected explicit uint32_t arguments")
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    mapped = set()
    for address in (item["start"], item["callee"], RETURN_PC, STACK_BASE):
        page = address & ~(PAGE - 1)
        if page not in mapped:
            u.mem_map(page, PAGE, UC_PROT_ALL)
            mapped.add(page)
    u.mem_write(item["start"], code)
    u.mem_write(item["callee"], bytes.fromhex("7047"))  # bx lr, stub only.
    u.mem_write(RETURN_PC, bytes.fromhex("00bf"))  # Thumb NOP stop marker
    u.reg_write(UC_ARM_REG_CPSR, 0x30)
    u.reg_write(UC_ARM_REG_R0, input_r0)
    u.reg_write(UC_ARM_REG_R3, SAVED_R3)
    u.reg_write(UC_ARM_REG_SP, STACK_INIT)
    u.reg_write(UC_ARM_REG_LR, RETURN_PC | 1)
    record = {"calls": 0, "r0_arg": None, "callee_lr": None,
              "returned": False, "unexpected_pc": False}
    path = []
    writes = []

    def on_code(emu, addr, size, user):
        if addr == RETURN_PC:
            record["returned"] = True
            emu.emu_stop()
        elif addr == item["callee"]:
            record["calls"] += 1
            record["r0_arg"] = emu.reg_read(UC_ARM_REG_R0)
            record["callee_lr"] = emu.reg_read(UC_ARM_REG_LR)
            emu.reg_write(UC_ARM_REG_R0, mocked_result)
        elif item["start"] <= addr < item["start"] + item["bytes"]:
            path.append((addr, size))
        else:
            record["unexpected_pc"] = True
            emu.emu_stop()

    def on_write(emu, access, addr, size, value, user):
        writes.append((addr, size))

    u.hook_add(UC_HOOK_CODE, on_code)
    u.hook_add(UC_HOOK_MEM_WRITE, on_write)
    # The return sentinel is observed by the code hook, not by emu_start(until).
    u.emu_start(item["start"] | 1, 0xffffffff, timeout=2_000_000, count=20)
    expected_calls = (1 if (item["model"] == "new_array" or input_r0 != 0)
                      else 0)
    if not record["returned"] or record["unexpected_pc"]:
        raise AssertionError("Bounded original Thumb wrapper did not return")
    if record["calls"] != expected_calls:
        raise AssertionError("Original wrapper call count disagreed with CFG")
    if expected_calls:
        if (record["r0_arg"] != input_r0 or
                record["callee_lr"] !=
                ((item["start"] + item["bytes"] - 2) | 1)):
            raise AssertionError("Original callee argument or link register wrong")
    if (u.reg_read(UC_ARM_REG_SP) != STACK_INIT or
            u.reg_read(UC_ARM_REG_R3) != SAVED_R3 or
            (u.reg_read(UC_ARM_REG_PC) & ~1) != RETURN_PC):
        raise AssertionError("Thumb stack/PC/R3 return contract violated")
    # PUSH {r3,lr} and POP {r3,pc} preserve the two saved words on
    # the stack until overwritten by a future call.
    saved = bytes(u.mem_read(STACK_INIT - 8, 8))
    expected_saved = (SAVED_R3.to_bytes(4, "little") +
                      (RETURN_PC | 1).to_bytes(4, "little"))
    if saved != expected_saved:
        raise AssertionError("Original wrapper saved wrong stack words")
    if not writes or any(not (STACK_INIT - 8 <= addr and
                              addr + size <= STACK_INIT) for addr, size in writes):
        raise AssertionError("Unexpected memory write outside saved stack slots")
    if item["model"] == "new_array" and u.reg_read(UC_ARM_REG_R0) != mocked_result:
        raise AssertionError("Allocator stub R0 was not forwarded to wrapper return")
    return {
        "entry": "0x%08x" % item["entry"],
        "case_input_r0": input_r0,
        "external_call_count": record["calls"],
        "external_callee": "0x%08x" % item["callee"] if record["calls"] else None,
        "external_r0_argument": record["r0_arg"],
        "returned_r0": u.reg_read(UC_ARM_REG_R0) if item["model"] == "new_array" else None,
        "returned_to_original_caller": record["returned"],
        "original_stack_and_r3_restored": True,
        "observed_stack_write_events": len(writes),
        "observed_wrapper_instructions": len(path),
        "real_external_callee_executed": False,
        "memory_contract_limited_to_wrapper_stack": True,
    }


def cpp_reference(executable, item, input_r0, mocked_result):
    result = subprocess.run(
        [str(executable), item["model"], str(input_r0), str(mocked_result)],
        capture_output=True, text=True, timeout=5, check=True)
    parsed = json.loads(result.stdout)
    if set(parsed) != {"calls", "argument", "target", "returned_r0"}:
        raise ValueError("Unexpected host C++ model JSON")
    return parsed


def scenarios(item):
    if item["model"] == "delete":
        return [(0, 0), (1, 0), (0x12345678, 0)]
    return [(0, 0x12340000), (1, 0x12340000),
            (0x40, 0xABCDEF00), (0xFFFFFFFF, 0x12345678)]


def audit(binary, model_executable):
    if original.sha256(binary) != original.PINNED_ELF_SHA:
        raise ValueError("ELF provenance mismatch")
    if not model_executable.is_file():
        raise ValueError("Independent compiled C++ model missing")
    wrappers = []
    with binary.open("rb") as stream:
        elf = ELFFile(stream)
        if elf.elfclass != 32 or elf["e_machine"] != "EM_ARM" or not elf.little_endian:
            raise ValueError("Expected original little-endian ARM ELF32")
        for item in SLICES:
            code, insns = read_slice(elf, stream, item)
            cases = []
            for input_r0, mocked_result in scenarios(item):
                emulated = execute_wrapper(item, code, input_r0, mocked_result)
                host = cpp_reference(model_executable, item, input_r0, mocked_result)
                if host["calls"] != emulated["external_call_count"]:
                    raise AssertionError("C++ callback count not equivalent")
                if host["target"] != (item["callee"] if host["calls"] else 0):
                    raise AssertionError("Unexpected C++ modeled external target")
                if host["calls"] and host["argument"] != emulated["external_r0_argument"]:
                    raise AssertionError("C++ forwarded argument differs from ELF")
                if (item["model"] == "new_array" and
                        host["returned_r0"] != emulated["returned_r0"]):
                    raise AssertionError("C++ modeled allocator return differs")
                cases.append(emulated)
            wrappers.append({
                "name": item["id"],
                "marked_thumb_entry": "0x%08x" % item["entry"],
                "bounded_prefix_bytes": item["bytes"],
                "declared_symbol_bytes": item["symbol_bytes"],
                "unattributed_trailing_symbol_bytes": item["symbol_bytes"] - item["bytes"],
                "instructions": len(insns),
                "intra_wrapper_edges": static_edges(item, insns),
                "scenarios": cases, "external_callee_executed": False,
                "semantic_contract_scope": "wrapper_only_mock_external_callee",
                "new_semantic_certificates": 0,
            })
    return {
        "schema": 1, "original_elf_sha256": original.PINNED_ELF_SHA,
        "wrapper_slices_tested": len(wrappers),
        "differential_scenarios_passed": sum(len(r["scenarios"]) for r in wrappers),
        "wrappers": wrappers,
        "real_external_callees_untested": True,
        "all_callers_reconstructed": False,
        "memory_allocator_equivalence_proven": False,
        "new_semantic_certificates": 0,
        "new_structural_approvals": 0,
        "T06_done": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--cpp-exe", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = audit(args.binary.resolve(), args.cpp_exe.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print("T06_WRAPPER_DIFFERENTIAL_SCENARIOS_PASSED=" +
          str(result["differential_scenarios_passed"]))
    print("T06_WRAPPER_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
