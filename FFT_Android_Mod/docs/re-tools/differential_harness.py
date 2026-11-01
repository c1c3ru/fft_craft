#!/usr/bin/env python3
"""Reusable original-ELF vs. reference-implementation differential harness.

Generalizes the per-case Unicorn setup already repeated across
b01_bounded_caller_execution.py / b01_cond_pop_pc_differential.py /
semantic_microexec.py into one module any T14+ reconstruction task can
import, instead of hand-rolling register maps and memory pages again.

What this does NOT do (RE_COMPLETUDE_TASKS.md T10 scope): establish
whole-program reachability, model real game state, or certify semantic
equivalence by itself. A passing comparison here is evidence for the
exact inputs/memory tested, nothing more. A failed emulation (crash,
unmapped-memory fault, step-limit hit) is always reported as FAIL, never
silently treated as a pass -- there is no code path that turns an
execution error into ExecutionResult(ok=True).
"""
from __future__ import annotations

import dataclasses
from pathlib import Path

from elftools.elf.elffile import ELFFile
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_MODE_THUMB, UC_PROT_ALL,
                      UC_HOOK_MEM_WRITE, UC_HOOK_MEM_UNMAPPED, UcError)
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

REG_NAMES = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7",
             "r8", "r9", "r10", "r11", "r12", "sp", "lr", "pc"]


def _reg_const(name: str) -> int:
    import unicorn.arm_const as c
    return getattr(c, "UC_ARM_REG_" + name.upper())


@dataclasses.dataclass
class MemoryBuffer:
    """A named scratch region the caller controls the initial bytes of."""
    name: str
    address: int
    data: bytes


@dataclasses.dataclass
class ExecutionResult:
    ok: bool
    error: str | None
    returned_r0: int | None
    registers: dict[str, int]
    memory_writes: list[tuple[int, bytes]]  # (address, bytes) in execution order; evidence/debugging only
    final_buffers: dict[str, bytes]         # named buffer -> content AFTER execution; this is what compare() diffs
    calls_outside_range: list[int]          # BL/BLX targets outside [start, end)
    stubbed_calls: list[int]                # calls_outside_range that a stub covered
    instructions_executed: int


def run_original(so_path: Path, start: int, end: int,
                  initial_regs: dict[str, int],
                  buffers: list[MemoryBuffer],
                  stub_calls: dict[int, int] | None = None,
                  max_instructions: int = 20000) -> ExecutionResult:
    """Execute the real bytes at [start, end) from the ELF, under Unicorn.

    `stub_calls` maps a BL/BLX target address to the r0 value Unicorn
    should return with instead of actually following the call -- the ONLY
    way an external call is skipped. Every such skip is recorded in
    `stubbed_calls` so the result always shows what was NOT really
    executed. A call to any other out-of-range address aborts the run
    (ok=False) rather than silently continuing past unknown code.
    """
    stub_calls = stub_calls or {}
    is_thumb = bool(start & 1)
    start &= ~1
    with open(so_path, "rb") as f:
        elf = ELFFile(f)
        sections = [(s["sh_addr"], s["sh_size"], s["sh_offset"], s["sh_type"])
                    for s in elf.iter_sections() if s["sh_addr"] != 0]
        f.seek(0)
        elf_bytes = f.read()

    def va_to_off(va: int):
        for addr, size, off, shtype in sections:
            if addr <= va < addr + size:
                return None if shtype == "SHT_NOBITS" else off + (va - addr)
        return None

    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB if is_thumb else UC_MODE_ARM)

    # Map every ALLOC section that overlaps [start, end) at its real
    # address with its real bytes -- not just the one target function --
    # so internal/forward references inside the same page still resolve.
    PAGE = 0x1000
    code_pages = set()
    for addr, size, off, shtype in sections:
        if addr == 0 or not (addr < end and addr + size > start):
            continue
        first_page = addr & ~(PAGE - 1)
        last_page = (addr + size - 1) & ~(PAGE - 1)
        for p in range(first_page, last_page + PAGE, PAGE):
            code_pages.add(p)
    for p in sorted(code_pages):
        uc.mem_map(p, PAGE, UC_PROT_ALL)
    for addr, size, off, shtype in sections:
        if shtype == "SHT_NOBITS" or addr == 0:
            continue
        if addr < end and addr + size > start:
            uc.mem_write(addr, elf_bytes[off:off + size])

    for buf in buffers:
        page = buf.address & ~(PAGE - 1)
        span = ((len(buf.data) + (buf.address - page) + PAGE - 1) // PAGE) * PAGE
        uc.mem_map(page, max(span, PAGE), UC_PROT_ALL)
        uc.mem_write(buf.address, buf.data)

    STACK = 0x700000
    uc.mem_map(STACK, 0x4000, UC_PROT_ALL)
    RETURN_SENTINEL = 0x6ffff0
    uc.mem_map(RETURN_SENTINEL & ~(PAGE - 1), PAGE, UC_PROT_ALL)

    for name, value in initial_regs.items():
        uc.reg_write(_reg_const(name), value)
    uc.reg_write(UC_ARM_REG_SP, initial_regs.get("sp", STACK + 0x2000))
    uc.reg_write(UC_ARM_REG_LR, RETURN_SENTINEL)

    writes: list[tuple[int, bytes]] = []
    calls_outside: list[int] = []
    stubbed: list[int] = []
    state = {"error": None}

    def on_write(u, access, address, size, value, user):
        writes.append((address, (value & ((1 << (8 * size)) - 1)).to_bytes(size, "little")))

    def on_unmapped(u, access, address, size, value, user):
        state["error"] = f"unmapped memory access at {hex(address)} (access={access}) -- FAIL"
        return False

    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_unmapped)

    # Single-step so control leaving [start, end) can be caught and
    # classified (stub vs. unexplained escape) before another instruction
    # runs. count tracks real steps taken, independent of any hook.
    pc = start | (1 if is_thumb else 0)
    count = 0
    try:
        while True:
            count += 1
            if count > max_instructions:
                state["error"] = f"step limit ({max_instructions}) exceeded -- treated as FAIL, not a pass"
                break
            uc.emu_start(pc, pc + 4, count=1)
            if state["error"]:
                break
            pc = uc.reg_read(UC_ARM_REG_PC)
            if pc in (RETURN_SENTINEL, RETURN_SENTINEL | 1):
                break
            real_pc = pc & ~1
            if not (start <= real_pc < end):
                # Left the declared range without hitting the return
                # sentinel -- only acceptable if it is a stubbed call site
                # the caller explicitly whitelisted.
                if real_pc in stub_calls:
                    uc.reg_write(_reg_const("r0"), stub_calls[real_pc])
                    uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
                    stubbed.append(real_pc)
                    calls_outside.append(real_pc)
                    pc = uc.reg_read(UC_ARM_REG_PC)
                    continue
                state["error"] = f"control left [{hex(start)},{hex(end)}) at {hex(real_pc)} with no stub -- FAIL"
                break
    except UcError as exc:
        state["error"] = f"UcError: {exc} -- FAIL"

    def read_buffers():
        return {buf.name: bytes(uc.mem_read(buf.address, len(buf.data))) for buf in buffers}

    if state["error"]:
        return ExecutionResult(False, state["error"], None, {}, writes,
                                read_buffers(), calls_outside, stubbed, count)

    regs = {name: uc.reg_read(_reg_const(name)) for name in REG_NAMES}
    return ExecutionResult(True, None, regs["r0"], regs, writes,
                            read_buffers(), calls_outside, stubbed, count)


def compare(original: ExecutionResult, reference: ExecutionResult,
            tracked_registers: list[str] | None = None) -> dict:
    """Field-by-field diff. Any execution failure on either side is an
    automatic, unconditional mismatch -- never treated as inconclusive-pass.
    """
    if tracked_registers is None:
        tracked_registers = ["r0"]
    report = {"match": True, "fields": {}}
    if not original.ok or not reference.ok:
        report["match"] = False
        report["fields"]["execution"] = {
            "original_ok": original.ok, "original_error": original.error,
            "reference_ok": reference.ok, "reference_error": reference.error,
        }
        return report
    for reg in tracked_registers:
        a, b = original.registers.get(reg), reference.registers.get(reg)
        ok = a == b
        report["fields"][reg] = {"original": a, "reference": b, "match": ok}
        report["match"] &= ok
    # Compare FINAL memory content per named buffer, not the write-log.
    # Two implementations can legitimately take a different number/order
    # of store instructions (e.g. three separate bitfield merges vs. one
    # combined write) and still be semantically equivalent; what matters
    # is the resulting bytes, which is also what "observar... memória" in
    # T10's acceptance criterion is asking for.
    names = sorted(set(original.final_buffers) | set(reference.final_buffers))
    for name in names:
        a, b = original.final_buffers.get(name), reference.final_buffers.get(name)
        ok = a == b
        report["fields"][f"buffer:{name}"] = {
            "original": a.hex() if a is not None else None,
            "reference": b.hex() if b is not None else None,
            "match": ok,
        }
        report["match"] &= ok
    return report
