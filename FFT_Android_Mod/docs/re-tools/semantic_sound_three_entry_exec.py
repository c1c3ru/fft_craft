#!/usr/bin/env python3
"""Bounded original-ELF Unicorn traces of three ARM sound-dispatcher entry paths.

The direct sound_request path executes 0x26b374 -> 0x2168e0 -> 0x271314,
then STOPS before SysSE_PlayDef at 0x2b2cf8. Two alternate trampoline
entries execute separately and are NOT asserted reachable from sound_request.
No destination function, external effect, or full return is emulated.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_R0

import semantic_evidence
import semantic_sound_two_hop_exec as two_hops

ELF_SHA256 = two_hops.ELF_SHA256
REGS = two_hops.REGS
CANARY = bytes.fromhex("197dda3c89fe201134fda9e267c012b8")
DATA = 0x500000
PAGE_SIZE = 0x1000
R0_STATES = (0, 1, 2, 0x40, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x12345678)
CPSR_STATES = tuple((i << 28) | 0x10 for i in range(16))

# These are individual original A32 words previously inspected in
# SEMANTIC_SOUND_DESTINATION_271314.md. Reject any byte drift.
WORDS = {
    0x26B374: ("59adfeea", "b", "#0x2168e0"),
    0x2168E0: ("8b6a01ea", "b", "#0x271314"),
    0x2168E4: ("8c6a01ea", "b", "#0x27131c"),
    0x2168F4: ("876a01ea", "b", "#0x271318"),
    0x271314: ("770601ea", "b", "#0x2b2cf8"),
    0x271318: ("4a0401ea", "b", "#0x2b2448"),
    0x27131C: ("010040e2", "sub", "r0, r0, #1"),
    0x271320: ("3b0501ea", "b", "#0x2b2814"),
}

# Traces include the final address observed at the code hook,
# BEFORE its first instruction is executed.
DESTINATIONS = (0x2B2CF8, 0x2B2448, 0x2B2814)
PATHS = {
    "sound_request": (0x26B374, (0x26B374, 0x2168E0, 0x271314, 0x2B2CF8), False),
    "relay_f4": (0x2168F4, (0x2168F4, 0x271318, 0x2B2448), False),
    "relay_e4": (0x2168E4, (0x2168E4, 0x27131C, 0x271320, 0x2B2814), True),
}


def original_words(binary):
    if hashlib.sha256(Path(binary).read_bytes()).hexdigest() != ELF_SHA256:
        raise ValueError("Original ELF identity mismatch")
    sites = {address: semantic_evidence.read_function(binary, address, 4)
             for address in tuple(WORDS) + DESTINATIONS}
    validate(sites)
    return sites


def validate(sites):
    if set(sites) != (set(WORDS) | set(DESTINATIONS)):
        raise ValueError("Missing or unexpected ARM sound entry/destination words")
    if any(len(sites[address]) != 4 for address in DESTINATIONS):
        raise ValueError("Truncated original ARM sound destination opcode")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for address, (expected_hex, expected_name, expected_ops) in WORDS.items():
        raw = sites[address]
        instructions = list(md.disasm(raw, address))
        if (raw.hex() != expected_hex or len(instructions) != 1
                or instructions[0].address != address
                or instructions[0].mnemonic != expected_name
                or instructions[0].op_str != expected_ops):
            raise ValueError(f"Changed original ARM sound opcode at 0x{address:x}")
    return True


def seeded_registers(r0):
    if r0 not in R0_STATES:
        raise ValueError("Unsupported R0 test state")
    regs = {reg: (0x11223344 ^ ((i + 1) * 0x01010101)) & 0xFFFFFFFF
            for i, reg in enumerate(REGS)}
    regs[UC_ARM_REG_R0] = r0
    regs[two_hops.UC_ARM_REG_SP] = 0x701000
    regs[two_hops.UC_ARM_REG_LR] = 0x710100
    return regs


def execute(sites, mode, r0, cpsr):
    validate(sites)
    if mode not in PATHS or cpsr not in CPSR_STATES:
        raise ValueError("Unsupported ARM mode/flags")
    start, expected_trace, decrement = PATHS[mode]
    destination = expected_trace[-1]
    regs = seeded_registers(r0)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    pages = {address & ~(PAGE_SIZE - 1)
             for address in tuple(sites) + (destination, DATA)}
    for address in sorted(pages):
        uc.mem_map(address, PAGE_SIZE, UC_PROT_ALL)
    for address, raw in sites.items():
        uc.mem_write(address, raw)
    # Destination words are original ELF bytes but code hook stops before executing.
    uc.mem_write(DATA, CANARY)
    uc.reg_write(UC_ARM_REG_CPSR, cpsr)
    for reg, value in regs.items():
        uc.reg_write(reg, value)
    trace, reads, writes = [], [], []

    def on_code(emu, address, size, unused):
        trace.append(address)
        if address == destination:
            emu.emu_stop()

    def on_read(emu, access, address, size, value, unused):
        reads.append((address, size))

    def on_write(emu, access, address, size, value, unused):
        writes.append((address, size, value))

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_READ, on_read)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    uc.emu_start(start, destination + 4, timeout=1_000_000, count=6)
    if tuple(trace) != expected_trace or uc.reg_read(UC_ARM_REG_PC) != destination:
        raise AssertionError(f"Unexpected original ARM entry trace: {trace}")
    if reads or writes or bytes(uc.mem_read(DATA, len(CANARY))) != CANARY:
        raise AssertionError("Unexpected data access/side-effect in ARM entry")
    for reg, value in regs.items():
        expected = ((value - 1) & 0xFFFFFFFF
                    if reg == UC_ARM_REG_R0 and decrement else value)
        if uc.reg_read(reg) != expected:
            raise AssertionError(f"Unexpected ARM register change: {reg}")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xF000003F) != (cpsr & 0xF000003F):
        raise AssertionError("ARM entry modified CPSR NZCV/mode bits")
    return {"mode": mode, "trace": tuple(trace), "destination": destination,
            "r0": uc.reg_read(UC_ARM_REG_R0),
            "data_reads": tuple(reads), "data_writes": tuple(writes),
            "destination_executed": False, "fully_certified": False}


def render(binary):
    sites = original_words(binary)
    count = 0
    lines = [
        "# sound_request: três entradas A32 microexecutadas no ELF original", "",
        "ELF SHA-256: " + ELF_SHA256, "",
        "## Rotas de entrada verificadas ate antes do proximo destino", "",
        "| Estado de entrada | Instrucoes ARM originais executadas | Destino nao executado | R0 final | Testes |",
        "|---|---|---|---|---|",
    ]
    for mode, (start, trace, decrement) in PATHS.items():
        for r0 in R0_STATES:
            for cpsr in CPSR_STATES:
                execute(sites, mode, r0, cpsr)
                count += 1
        label = "(R0 - 1) & 0xffffffff" if decrement else "R0 preservado"
        chain = " -> ".join(f"0x{x:x}" for x in trace[:-1])
        lines.append(
            f"| {mode}, 0x{start:x} | {chain} | 0x{trace[-1]:x} | {label} | "
            f"{len(R0_STATES) * len(CPSR_STATES)} |")
    lines += [
        "", f"Microexecucoes Unicorn verificadas: {count} "
        f"({len(PATHS)} entradas x {len(R0_STATES)} R0 x {len(CPSR_STATES)} NZCV).",
        "Todos os casos verificaram fluxo, R0-R14, SP/LR, flags NZCV, "
        "memoria sentinela e ausencia de acesso a dados nestes prefixos.", "",
        "## Limites de evidencia", "",
        "- Somente a entrada chamada sound_request e confirmada como parte "
        "da cadeia que parte de 0x26b374.",
        "- As entradas relay_f4 e relay_e4 foram testadas isoladamente; "
        "nao foi provado que sound_request as alcance em tempo de execucao.",
        "- Destinos 0x2b2cf8, 0x2b2448, 0x2b2814 NAO foram executados; "
        "sem efeitos sonoros, sem retornos ou equivalencia global inferidos.",
        "- Novos certificados neste relatorio: 0. "
        "As 303 certificacoes da classe BX LR permanecem inalteradas.", "",
    ]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_evidence.ROOT /
                   "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--output", type=Path, default=semantic_evidence.ROOT /
                   "docs/re-results/SEMANTIC_SOUND_THREE_ENTRY_EXEC.md")
    a = p.parse_args()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(render(a.binary), encoding="utf-8")
    print(f"SOUND_ARM_ENTRY_MODES={len(PATHS)}")
    print(f"SOUND_ARM_ENTRY_UNICORN_CASES={len(PATHS) * len(R0_STATES) * len(CPSR_STATES)}")
    print("SOUND_ARM_ENTRY_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
