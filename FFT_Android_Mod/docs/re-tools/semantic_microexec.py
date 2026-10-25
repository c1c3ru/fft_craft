#!/usr/bin/env python3
"""Execute isolated real ARM bit-clear sequences in Unicorn for local evidence.

This deliberately does NOT execute the whole function: it cannot establish
control-flow reachability, global side effects, aliasing, input contracts,
exception paths or semantic equivalence with a replacement implementation.
"""
import argparse
import hashlib
import random
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R4

import semantic_evidence
import semantic_facts

BIT_CLEAR_SITES = (0x244254, 0x2443B8)
MEMORY_ADDR = 0x500000
CODE_PAGE = 0x244000
UNTOUCHED_WORD = 0xA5A55A5A
MASK = 0x40


def inputs():
    """Boundary examples plus seeded values, identical on every run."""
    seed = [0, 1, 0x3F, 0x40, 0x41, 0x7F, 0x80, 0x80000000, 0x80000040,
            0xFFFFFFBF, 0xFFFFFFFF]
    rng = random.Random(0x244254)
    return seed + [rng.getrandbits(32) for _ in range(21)]


def check_instructions(data, address):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    decoded = list(md.disasm(data, address))
    if len(decoded) != 3 or [i.address for i in decoded] != [
            address, address + 4, address + 8]:
        raise ValueError(f"Expected three consecutive ARM instructions at 0x{address:x}")
    facts = semantic_facts.bitmask_effects({x.address: x for x in decoded})
    if not (len(facts) == 1 and facts[0]["kind"] == "clear_bits"
            and facts[0]["mask"] == MASK and facts[0]["memory"] == "[r4]"
            and facts[0]["condition"] == "always"):
        raise ValueError(f"Expected unconditional 0x40 clearing sequence at 0x{address:x}")
    return decoded


def microexecute(data, address, initial):
    """Run exactly 3 machine instructions, not their surrounding function."""
    assert len(data) == 12
    check_instructions(data, address)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(CODE_PAGE, 0x1000, UC_PROT_ALL)
    machine.mem_map(MEMORY_ADDR, 0x1000, UC_PROT_ALL)
    machine.mem_write(address, data)
    machine.mem_write(MEMORY_ADDR, initial.to_bytes(4, "little"))
    machine.mem_write(MEMORY_ADDR + 4, UNTOUCHED_WORD.to_bytes(4, "little"))
    machine.reg_write(UC_ARM_REG_R4, MEMORY_ADDR)
    machine.reg_write(UC_ARM_REG_R2, 0xBADC0DE)
    machine.emu_start(address, address + 12, timeout=1000000, count=3)
    result = int.from_bytes(machine.mem_read(MEMORY_ADDR, 4), "little")
    neighbor = int.from_bytes(machine.mem_read(MEMORY_ADDR + 4, 4), "little")
    assert machine.reg_read(UC_ARM_REG_R4) == MEMORY_ADDR, "r4 base pointer changed"
    assert machine.reg_read(UC_ARM_REG_R2) == result, "r2 differs from stored word"
    assert neighbor == UNTOUCHED_WORD, "Adjacent memory word was modified"
    return result


def run(binary):
    checksum = hashlib.sha256(binary.read_bytes()).hexdigest()
    report = [
        "# Isolated ARM machine-instruction microexecution", "",
        f"ELF SHA-256: \x60{checksum}\x60", "",
        "**Scope:** only three ARM instructions at each listed address, "
        "executed with synthetic state in Unicorn. No branch, call, "
        "complete function or application has been emulated. This establishes "
        "a bounded instruction-level behavior check, **not** semantic "
        "equivalence or global reachability.", "",
        "| ELF instruction address | Test inputs | Observed operation | Result |",
        "|---|---:|---|---|",
    ]
    n = 0
    for address in BIT_CLEAR_SITES:
        data = semantic_evidence.read_function(binary, address, 12)
        check_instructions(data, address)
        for initial in inputs():
            observed = microexecute(data, address, initial)
            expected = initial & (~MASK & 0xFFFFFFFF)
            if observed != expected:
                raise AssertionError(
                    f"0x{address:x}: input 0x{initial:x}, "
                    f"observed 0x{observed:x}, expected 0x{expected:x}")
            n += 1
        report.append(f"| \x600x{address:x}\x60 | {len(inputs())} | "
                      "memory32 := memory32 & ~0x40; adjacent word unchanged | PASS |")
    report += ["", f"**Total verified machine micro-executions:** {n}.", "",
               "## Evidence boundaries", "",
               "- The original ELF bytes were executed; the three-instruction "
               "patterns are independently matched before executing them.",
               "- Deterministic examples are not exhaustive over the 32-bit state space.",
               "- This does not prove that any function invocation reaches either site.",
               "- Side effects, callee behavior, flags, aliasing, and external inputs "
               "outside the isolated snippets are not established.", "",
               "Every affected function remains \x60needs_review\x60.", ""]
    return "\n".join(report)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path,
                   default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results", type=Path,
                   default=semantic_evidence.ROOT / "docs/re-results")
    args = p.parse_args()
    report = run(args.binary)
    dest = args.results / "SEMANTIC_MICROEXEC.md"
    dest.write_text(report, encoding="utf-8")
    print(f"Completed isolated ARM microexecution: {dest}")


if __name__ == "__main__":
    main()
