#!/usr/bin/env python3
"""A04: original A32 dispatcher with four real callers; bounded differential.

Executes exactly four original ARM caller instructions sequences ending at
the shared dispatcher plus its BX LR, or one independent LDR/BX LR leaf.
Does NOT enter any other CFG destination, and creates no certificates.
"""
import argparse
import hashlib
import json
from pathlib import Path

import semantic_a02_branch_11 as a02
import semantic_evidence
import semantic_loop_250 as prior

DIGEST = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
DISPATCHER = 0xb6c58
GETTER = 0xb8a18
DISPATCHER_HEX = "083090e5012182e0020193e71eff2fe1"
GETTER_HEX = "080090e51eff2fe1"
CALLERS = {
    0xb6c68: 0, 0xb6cd0: 1, 0xb6ee0: 2, 0xb6ee8: 3
}
BASE = 0x500100
ARRAY = 0x501100
RETURN = 0x710100
MASK = 0xffffffff


def actual_bytes(binary, address, expected):
    raw = semantic_evidence.read_function(binary, address, len(bytes.fromhex(expected)))
    if raw.hex() != expected:
        raise ValueError(f"Unexpected ELF ARM bytes 0x{address:x}")
    return raw


def assert_original(binary):
    actual_bytes(binary, DISPATCHER, DISPATCHER_HEX)
    actual_bytes(binary, GETTER, GETTER_HEX)
    for addr, constant in CALLERS.items():
        raw = actual_bytes(binary, addr, a02.EXPECTED[f"{addr:08x}"][0])
        spec = a02.decode(raw, addr)
        if spec is None or spec["op"] != ["mov_r2_zero", "mov_r2_one", "mov_r2_two", "mov_r2_three"][constant]:
            raise ValueError("Original caller does not select expected R2")
        if spec["target"] != DISPATCHER:
            raise ValueError("Original caller no longer branches to dispatcher")


def memory_model(seed):
    initial = bytearray((i * 17 + (seed & 255)) & 255 for i in range(0x100))
    table = bytearray(0x100)
    initial[8:12] = ARRAY.to_bytes(4, "little")
    for i in range(32):
        value = (seed ^ (0x9e3779b9 * (i+1))) & MASK
        table[4*i:4*i+4] = value.to_bytes(4, "little")
    return bytes(initial), bytes(table)


def reference(seed, index, row, kind):
    base, table = memory_model(seed)
    registers = [(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    registers[0] = BASE
    registers[1] = row
    if kind == "dispatcher":
        registers[3] = ARRAY
        registers[2] = index + (row << 2)
        addr = ARRAY + registers[2]*4
        registers[0] = int.from_bytes(table[(addr-ARRAY):(addr-ARRAY)+4], "little")
        reads = [(BASE+8, 4), (addr, 4)]
    elif kind == "getter":
        registers[0] = ARRAY
        reads = [(BASE+8, 4)]
    else:
        raise ValueError("Unknown A04 modeled code")
    return registers, base, table, reads


def execute(binary, kind, address, seed, row, flags):
    from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                         UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
    from unicorn.arm_const import (
        UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
        UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
        UC_ARM_REG_R12)
    if kind == "dispatcher":
        if address not in CALLERS:
            raise ValueError("Unlisted A04 caller")
        expected_index = CALLERS[address]
        source = actual_bytes(binary, address, a02.EXPECTED[f"{address:08x}"][0])
        dest = actual_bytes(binary, DISPATCHER, DISPATCHER_HEX)
        start = address
        model_regs, base, table, expected_reads = reference(seed, expected_index, row, kind)
        expected_pc = [address, address+4, DISPATCHER, DISPATCHER+4,
                       DISPATCHER+8, DISPATCHER+12, RETURN]
    elif kind == "getter":
        if address != GETTER:
            raise ValueError("Unlisted standalone getter")
        source = b""
        dest = actual_bytes(binary, GETTER, GETTER_HEX)
        start = GETTER
        model_regs, base, table, expected_reads = reference(seed, 0, row, kind)
        expected_pc = [GETTER, GETTER+4, RETURN]
    else:
        raise ValueError("Unknown kind")
    initial_regs = [(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    initial_regs[0] = BASE
    initial_regs[1] = row
    regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
            UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
            UC_ARM_REG_R11, UC_ARM_REG_R12)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in sorted({start & ~0xfff, address & ~0xfff, DISPATCHER & ~0xfff,
                        GETTER & ~0xfff, RETURN & ~0xfff, BASE & ~0xfff, ARRAY & ~0xfff}):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    if source:
        uc.mem_write(address, source)
    uc.mem_write(DISPATCHER if kind == "dispatcher" else GETTER, dest)
    uc.mem_write(RETURN, bytes(4))
    uc.mem_write(BASE, base)
    uc.mem_write(ARRAY, table)
    uc.reg_write(UC_ARM_REG_CPSR, flags | 0x10)
    for reg, val in zip(regs, initial_regs):
        uc.reg_write(reg, val)
    uc.reg_write(UC_ARM_REG_LR, RETURN)
    uc.reg_write(UC_ARM_REG_SP, 0x700ffc)
    code_trace, reads, writes = [], [], []

    def on_code(machine, pc, size, unused):
        code_trace.append(pc)
        if pc == RETURN:
            machine.emu_stop()

    def on_read(machine, access, position, size, value, unused):
        reads.append((position, size))

    def on_write(machine, access, position, size, value, unused):
        writes.append((position, size, value))

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_READ, on_read)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    try:
        uc.emu_start(start, MASK, timeout=1_000_000, count=8)
    except Exception as exc:
        raise AssertionError(f"A04 Unicorn error 0x{address:08x} trace={code_trace}") from exc
    if code_trace != expected_pc or uc.reg_read(UC_ARM_REG_PC) != RETURN:
        raise AssertionError(f"Wrong A04 original control flow {code_trace} != {expected_pc}")
    if reads != expected_reads or writes:
        raise AssertionError(f"Wrong A04 memory effects reads={reads} writes={writes}")
    if bytes(uc.mem_read(BASE, len(base))) != base or bytes(uc.mem_read(ARRAY, len(table))) != table:
        raise AssertionError("Unexpected original ARM memory mutation")
    if any(uc.reg_read(reg) != expected for reg, expected in zip(regs, model_regs)):
        raise AssertionError("Original ARM register differences vs independent model")
    if uc.reg_read(UC_ARM_REG_SP) != 0x700ffc or uc.reg_read(UC_ARM_REG_LR) != RETURN:
        raise AssertionError("SP or LR changed")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xf000003f) != ((flags | 0x10) & 0xf000003f):
        raise AssertionError("Unexpected flags or mode changes")


def snapshot(digest, static_sha, rounds):
    return {"schema": 1, "elf_sha256": digest,
            "a04_static_checkpoint_sha256": static_sha, "rounds": rounds,
            "new_certificates": 0}


def report(state):
    cases = sum(x["cases"] for x in state["rounds"])
    return "\n".join([
        "# A04: dispatcher and getter original ARM microexecution", "",
        "Original ELF SHA-256: " + state["elf_sha256"], "",
        f"Integrated dispatcher caller scenarios: {cases-32}; "
        "standalone getter scenarios: 32; total: " + str(cases) + ".", "",
        "Exact original dispatcher A32 at 0x000b6c58:",
        "~~~asm", "ldr r3, [r0, #8]",
        "add r2, r2, r1, lsl #2", "ldr r0, [r3, r2, lsl #2]", "bx lr", "~~~",
        "", "Independent model: table pointer at R0+8; row R1 (0..3), "
        "column R2 selected by four original MOV+B callers (0..3); "
        "index = column + 4*row, word offset = index*4. "
        "Value returned in R0; R2 and R3 reflect intermediate state.",
        "", "Secondary original getter 0x000b8a18 loads word R0+8 and returns.",
        "", "States: 8 deterministic memory seeds, four NZCV flag sets, four "
        "rows and four original callers; 32 getter states. "
        "Observed original ARM vs independent register/memory model, "
        "read addresses and width, PC trace, SP/LR, CPSR, and zero writes.",
        "", "Constraints: synthetic valid pointers/array; never a real Android "
        "runtime value. Only the enumerated inputs are tested. Other five "
        "external targets, calling conventions under real runtime, reachability "
        "and whole-function equivalence remain open. No new certificates.",
        ""])
    

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--a04-static-checkpoint", type=Path, required=True)
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    digest = hashlib.sha256(args.binary.read_bytes()).hexdigest()
    if digest != DIGEST:
        raise ValueError("Unexpected original ELF hash")
    static = json.loads(args.a04_static_checkpoint.read_text(encoding="utf-8"))
    audited = {t["address"]: t for t in static.get("targets", [])}
    if (static.get("elf_sha256") != DIGEST or static.get("unique_external_targets") != 7
            or len(audited) != 7 or "000b6c58" not in audited or "000b8a18" not in audited
            or static.get("destinations_executed") != 0
            or static.get("new_certificates") != 0
            or not audited["000b6c58"]["raw_hex"].startswith(DISPATCHER_HEX)
            or not audited["000b8a18"]["raw_hex"].startswith(GETTER_HEX)):
        raise ValueError("A04 original static evidence is stale")
    assert_original(args.binary)
    static_sha = hashlib.sha256(args.a04_static_checkpoint.read_bytes()).hexdigest()
    rounds = []
    if args.checkpoint.exists():
        prior_state = json.loads(args.checkpoint.read_text(encoding="utf-8"))
        if prior_state != snapshot(digest, static_sha, prior_state.get("rounds", [])):
            raise ValueError("A04 dynamic checkpoint mismatches audit identity")
        rounds = prior_state["rounds"]
    expected = [{"name": f"caller_{addr:08x}", "cases": len(prior.SEEDS)*len(prior.FLAGS)*4}
                for addr in CALLERS]
    expected.append({"name": "getter_b8a18", "cases": len(prior.SEEDS)*len(prior.FLAGS)})
    if len(rounds) > len(expected):
        raise ValueError("Unexpected excess rounds")
    for index, expected_record in enumerate(expected):
        if index < len(CALLERS):
            address = list(CALLERS)[index]
            for seed in prior.SEEDS:
                for flags in prior.FLAGS:
                    for row in range(4):
                        execute(args.binary, "dispatcher", address, seed, row, flags)
        else:
            for seed in prior.SEEDS:
                for flags in prior.FLAGS:
                    execute(args.binary, "getter", GETTER, seed, 0, flags)
        current = {"iteration": index+1, **expected_record, "status": "bounded_pass"}
        if index < len(rounds):
            if rounds[index] != current:
                raise ValueError("Checkpoint reexecution differs")
        else:
            rounds.append(current)
            args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
            tmp = args.checkpoint.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(snapshot(digest, static_sha, rounds),
                                      indent=2, sort_keys=True) + "\n", encoding="utf-8")
            tmp.replace(args.checkpoint)
    result = snapshot(digest, static_sha, rounds)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report(result), encoding="utf-8")
    cases = sum(r["cases"] for r in rounds)
    print("A04_DISPATCHER_CALLERS=4")
    print("A04_DISPATCHER_CASES=512")
    print("A04_GETTER_CASES=32")
    print(f"A04_DYNAMIC_CASES={cases}")
    print("A04_UNMODELED_TARGETS=5")
    print("A04_FAILED=0")
    print("A04_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
