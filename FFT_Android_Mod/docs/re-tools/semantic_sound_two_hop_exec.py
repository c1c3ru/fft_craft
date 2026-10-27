#!/usr/bin/env python3
"""Bounded Unicorn execution of two original ARM sound_request branch hops.

Original ELF: 0x26b374 -> 0x2168e0 -> 0x271314.
Only the first two ARM words execute; the unknown destination is intercepted
BEFORE executing it. No sound behavior or complete function proof is claimed.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
    UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_CPSR,
)
import semantic_evidence

ELF_SHA256 = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
SOUND, RELAY, UNKNOWN = 0x26B374, 0x2168E0, 0x271314
MEMORY, PAGE_SIZE = 0x500000, 0x1000
CANARY = bytes.fromhex("76a1c30fe25b9874d610a5e1b2345678")
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
        UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
        UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
        UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR)
CPSR_STATES = (0x10, 0xF0000010)
R0_STATES = (0, 1, 0x40, 0xFFFFFFFF)


def validate(code):
    if len(code) != 2:
        raise ValueError("Expected two ARM A32 branches")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for raw, source, destination in zip(code, (SOUND, RELAY), (RELAY, UNKNOWN)):
        instructions = list(md.disasm(raw, source))
        if (len(raw) != 4 or len(instructions) != 1
                or instructions[0].size != 4
                or instructions[0].address != source
                or instructions[0].mnemonic != "b"
                or instructions[0].op_str != f"#0x{destination:x}"):
            raise ValueError(f"Original ARM branch signature changed at 0x{source:x}")
    return True


def original_code(binary):
    if hashlib.sha256(Path(binary).read_bytes()).hexdigest() != ELF_SHA256:
        raise ValueError("Original ELF identity changed")
    code = (semantic_evidence.read_function(binary, SOUND, 4),
            semantic_evidence.read_function(binary, RELAY, 4))
    validate(code)
    return code


def initial_registers(r0):
    if r0 not in R0_STATES:
        raise ValueError("Unapproved initial register sample")
    values = {reg: ((0x11223344 ^ ((i + 1) * 0x01010101)) & 0xFFFFFFFF)
              for i, reg in enumerate(REGS)}
    values[UC_ARM_REG_R0] = r0
    values[UC_ARM_REG_SP] = 0x701000
    values[UC_ARM_REG_LR] = 0x710100
    return values


def execute(code, r0, cpsr):
    validate(code)
    if cpsr not in CPSR_STATES:
        raise ValueError("Unapproved CPSR flags")
    emu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for address in (SOUND, RELAY, UNKNOWN, MEMORY):
        emu.mem_map(address & ~(PAGE_SIZE - 1), PAGE_SIZE, UC_PROT_ALL)
    emu.mem_write(SOUND, code[0])
    emu.mem_write(RELAY, code[1])
    emu.mem_write(UNKNOWN, bytes.fromhex("0000a0e1"))
    emu.mem_write(MEMORY, CANARY)
    regs = initial_registers(r0)
    emu.reg_write(UC_ARM_REG_CPSR, cpsr)
    for reg, word in regs.items():
        emu.reg_write(reg, word)
    trace, reads, writes = [], [], []

    def observe(uc, address, size, unused):
        trace.append(address)
        if address == UNKNOWN:
            uc.emu_stop()

    def mem_read(uc, access, address, size, value, unused):
        reads.append((address, size))

    def mem_write(uc, access, address, size, value, unused):
        writes.append((address, size, value))

    emu.hook_add(UC_HOOK_CODE, observe)
    emu.hook_add(UC_HOOK_MEM_READ, mem_read)
    emu.hook_add(UC_HOOK_MEM_WRITE, mem_write)
    emu.emu_start(SOUND, UNKNOWN + 4, timeout=1_000_000, count=3)
    if trace != [SOUND, RELAY, UNKNOWN]:
        raise AssertionError(f"Unexpected real ARM code trace: {trace}")
    if emu.reg_read(UC_ARM_REG_PC) != UNKNOWN:
        raise AssertionError("Wrong final branch target")
    if reads or writes or bytes(emu.mem_read(MEMORY, len(CANARY))) != CANARY:
        raise AssertionError("Unexpected data access or memory change")
    for reg, initial in regs.items():
        if emu.reg_read(reg) != initial:
            raise AssertionError("Unconditional branch modified register")
    if (emu.reg_read(UC_ARM_REG_CPSR) & 0xF000003F) != (cpsr & 0xF000003F):
        raise AssertionError("Unconditional branch modified CPSR NZCV/mode")
    return {"trace": tuple(trace), "end": UNKNOWN,
            "reads": tuple(reads), "writes": tuple(writes),
            "normal_return_verified": False}


def render(binary):
    code = original_code(binary)
    samples = [execute(code, r0, cpsr)
               for r0 in R0_STATES for cpsr in CPSR_STATES]
    return "\n".join([
        "# sound_request: dois saltos ARM executados no Unicorn", "",
        "ELF SHA-256: " + ELF_SHA256, "",
        "Janelas A32 originais executadas:",
        f"- 0x{SOUND:x} -> 0x{RELAY:x}: branch B original",
        f"- 0x{RELAY:x} -> 0x{UNKNOWN:x}: segundo branch B original",
        f"- 0x{UNKNOWN:x}: parada ANTES da instrucao; efeito posterior desconhecido", "",
        f"Microexecucoes Unicorn verificadas: {len(samples)} "
        f"({len(R0_STATES)} estados R0 x {len(CPSR_STATES)} estados CPSR).", "",
        "Os registradores, flags e memoria sentinela foram preservados.",
        "Nao houve leitura/escrita de dados nos dois saltos.",
        "Nenhuma equivalencia de funcao, efeitos de som ou retorno foi certificada.", "",
        "Limites: registros e memoria sinteticos; o destino final nao foi executado.",
    ]) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path,
                   default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--output", type=Path,
                   default=semantic_evidence.ROOT /
                   "docs/re-results/SEMANTIC_SOUND_TWO_HOP_EXEC.md")
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(args.binary), encoding="utf-8")
    print("SOUND_TWO_HOP_ARM_UNICORN_CASES=8")
    print("SOUND_TWO_HOP_CERTIFICATES=0")


if __name__ == "__main__":
    main()
