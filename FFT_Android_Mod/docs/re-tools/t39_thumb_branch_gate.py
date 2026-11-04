#!/usr/bin/env python3
"""T06: original ELF Thumb direct-branch microexecution against Capstone.

Runs exactly one instruction per scenario in a bounded Unicorn ARM context.
This proves instruction-local PC/LR behavior for controlled flags, not the
whole caller, objects, C++ equivalence or Android runtime.
"""
import argparse
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from capstone.arm import ARM_INS_B, ARM_INS_BL, ARM_OP_IMM
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_PROT_ALL, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC

import b01_overlap_elf_evidence as original

ROOT = Path(__file__).resolve().parents[2]
BRANCHES = (
    {"site": 0x002C9118, "kind": "beq", "length": 2,
     "target": 0x002C911E, "z": True},
    {"site": 0x002C911A, "kind": "bl", "length": 4,
     "target": 0x002CE07C, "z": False},
    {"site": 0x002C9A26, "kind": "bl", "length": 4,
     "target": 0x002C99B4, "z": False},
)
WORD_PAGE = 0x1000
CPSR_THUMB_USER = 0x30
CPSR_Z = 1 << 30


def original_instruction(elf, stream, case):
    site = case["site"]
    raw, _ = original.read_executable(elf, stream, site, case["length"])
    if raw is None or len(raw) != case["length"]:
        raise ValueError("Original branch not file-backed")
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    cs.detail = True
    insns = list(cs.disasm(raw, site))
    if len(insns) != 1 or insns[0].size != case["length"]:
        raise ValueError("Original Thumb opcode not fully decoded")
    insn = insns[0]
    if not ((case["kind"] == "beq" and insn.id == ARM_INS_B
             and insn.mnemonic == "beq")
            or (case["kind"] == "bl" and insn.id == ARM_INS_BL
                and insn.mnemonic == "bl")):
        raise ValueError("Original Thumb opcode class changed")
    if (len(insn.operands) != 1 or insn.operands[0].type != ARM_OP_IMM
            or (int(insn.operands[0].imm) & 0xffffffff) != case["target"]):
        raise ValueError("Capstone branch target differs from original ELF fixture")
    return raw


def execute_case(site, data, expected_pc, z, kind):
    if len(data) not in (2, 4) or site & 1 or expected_pc & 1:
        raise ValueError("Invalid aligned Thumb instruction/target")
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    pages = {site & ~(WORD_PAGE - 1), expected_pc & ~(WORD_PAGE - 1)}
    for page in pages:
        uc.mem_map(page, WORD_PAGE, UC_PROT_ALL)
    uc.mem_write(site, data)
    uc.reg_write(UC_ARM_REG_CPSR, CPSR_THUMB_USER | (CPSR_Z if z else 0))
    original_lr = 0x600001
    uc.reg_write(UC_ARM_REG_LR, original_lr)
    if not uc.reg_read(UC_ARM_REG_CPSR) & 0x20:
        raise AssertionError("ARM emulator started outside Thumb state")
    trace = []
    uc.hook_add(UC_HOOK_CODE, lambda u, addr, size, _: trace.append((addr, size)))
    uc.emu_start(site | 1, 0xffffffff, timeout=1_000_000, count=1)
    pc = uc.reg_read(UC_ARM_REG_PC) & ~1
    lr = uc.reg_read(UC_ARM_REG_LR)
    if trace != [(site, len(data))] or pc != expected_pc:
        raise AssertionError("Unicorn Thumb branch PC differs from Capstone reference")
    if not uc.reg_read(UC_ARM_REG_CPSR) & 0x20:
        raise AssertionError("Thumb state unexpectedly cleared")
    expected_lr = ((site + len(data)) | 1) if kind == "bl" else original_lr
    if lr != expected_lr:
        raise AssertionError("Thumb LR writeback differed from reference")
    return {
        "site": "0x%08x" % site,
        "instruction_size_bytes": len(data),
        "expected_pc": "0x%08x" % expected_pc,
        "unicorn_pc": "0x%08x" % pc,
        "expected_lr": "0x%08x" % expected_lr,
        "unicorn_lr": "0x%08x" % lr,
        "thumb_mode_preserved": True,
        "one_original_instruction_executed": True,
    }


def audit(binary):
    if original.sha256(binary) != original.PINNED_ELF_SHA:
        raise ValueError("Unrecognized original ELF")
    evidence = []
    with binary.open("rb") as stream:
        elf = ELFFile(stream)
        if elf.elfclass != 32 or elf["e_machine"] != "EM_ARM":
            raise ValueError("Expected ELF32 ARM")
        for case in BRANCHES:
            raw = original_instruction(elf, stream, case)
            evidence.append(execute_case(
                case["site"], raw, case["target"], case["z"], case["kind"]))
            if case["kind"] == "beq":
                # Conditional branch not taken: Z=0, fallthrough to next op.
                not_taken = execute_case(
                    case["site"], raw, case["site"] + case["length"], False, "beq")
                not_taken["scenario"] = "Z_zero_fallthrough"
                evidence.append(not_taken)
    return {
        "schema": 1, "elf_sha256": original.PINNED_ELF_SHA,
        "thumb_branch_scenarios": len(evidence), "results": evidence,
        "verified_under_controlled_emulator_state": True,
        "app_runtime_reachability_proven": False,
        "new_semantic_certificates": 0, "new_structural_approvals": 0,
        "T06_done": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = audit(args.binary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print("T06_THUMB_BRANCH_ORIGINAL_EMULATION_PASSED=" + str(len(result["results"])))
    print("T06_THUMB_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
