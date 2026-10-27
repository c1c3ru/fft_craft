#!/usr/bin/env python3
"""Four-stage, scoped reconstruction of the actual SysSE_PlayDef A32 prefix.

Static A32 provenance -> live Unicorn observations -> independent C model ->
differential comparison. Stops BEFORE 0x2b2b7c. Never certifies full audio.
"""
import argparse
import ctypes
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

import semantic_evidence
import semantic_sound_three_entry_exec as upstream
import semantic_sound_icon_microexec as prior

ROOT = semantic_evidence.ROOT
SOURCE = Path(__file__).resolve().parent / "c-models/sound_playdef_prefix.c"
ENTRY = prior.SOUND_ENTRY
STOP = prior.SOUND_STOP
PREFIX_HEX = "0010a0e10000a0e39dffffea"
TRACE = (0x26B374, 0x2168E0, 0x271314, ENTRY, ENTRY + 4, ENTRY + 8, STOP)
DATA = 0x500000
CANARY = bytes.fromhex("afa0125ab2c34432cafed00d97891234")


class PrefixResult(ctypes.Structure):
    _fields_ = [("next_pc", ctypes.c_uint32),
                ("r0", ctypes.c_uint32),
                ("r1", ctypes.c_uint32)]


def original(binary):
    """All bytes from authenticated executable segments, never mock dispatches."""
    binary = Path(binary)
    if hashlib.sha256(binary.read_bytes()).hexdigest() != upstream.ELF_SHA256:
        raise ValueError("Wrong original ELF identity")
    sites = upstream.original_words(binary)
    prefix = semantic_evidence.read_function(binary, ENTRY, 12)
    validate(prefix)
    # Before this point only the predecessor's three original B instructions
    # were executed; these bytes extend the trace to the common sound body.
    return sites, prefix


def validate(prefix):
    if prefix.hex() != PREFIX_HEX:
        raise ValueError("SysSE_PlayDef original 3-instruction signature drift")
    prior.disasm_exact(prefix, ENTRY, prior.SOUND_SIGNATURE)
    return True


def execute(sites, prefix, arg, cpsr):
    """Observe ARM code at STOP without executing its first instruction."""
    upstream.validate(sites)
    validate(prefix)
    if arg not in upstream.R0_STATES or cpsr not in upstream.CPSR_STATES:
        raise ValueError("Unsupported differential sample")
    reg_before = upstream.seeded_registers(arg)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    pages = {addr & ~0xFFF for addr in (*sites, ENTRY, STOP, DATA)}
    for page in sorted(pages):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    for addr, word in sites.items():
        uc.mem_write(addr, word)
    uc.mem_write(ENTRY, prefix)
    # The STOP instruction is not executed and may be observed only by hook.
    uc.mem_write(DATA, CANARY)
    uc.reg_write(UC_ARM_REG_CPSR, cpsr)
    for reg, value in reg_before.items():
        uc.reg_write(reg, value)

    trace, reads, writes = [], [], []

    def code_hook(machine, address, size, unused):
        trace.append(address)
        if address == STOP:
            machine.emu_stop()

    uc.hook_add(UC_HOOK_CODE, code_hook)
    uc.hook_add(UC_HOOK_MEM_READ,
                lambda m, access, addr, size, value, u: reads.append((addr, size)))
    uc.hook_add(UC_HOOK_MEM_WRITE,
                lambda m, access, addr, size, value, u: writes.append((addr, size, value)))
    uc.emu_start(TRACE[0], 0xFFFFFFFF, timeout=1_000_000, count=10)

    if tuple(trace) != TRACE or uc.reg_read(UC_ARM_REG_PC) != STOP:
        raise AssertionError("Unexpected original A32 branch/control trace")
    if reads or writes or bytes(uc.mem_read(DATA, len(CANARY))) != CANARY:
        raise AssertionError("Unexpected data access in A32 forwarding prefix")
    for reg, value in reg_before.items():
        expected = 0 if reg == UC_ARM_REG_R0 else arg if reg == UC_ARM_REG_R1 else value
        if uc.reg_read(reg) != expected:
            raise AssertionError(f"Unexpected register mutation: {reg}")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xF000003F) != (cpsr & 0xF000003F):
        raise AssertionError("CPSR NZCV/mode changed")
    return (uc.reg_read(UC_ARM_REG_PC),
            uc.reg_read(UC_ARM_REG_R0),
            uc.reg_read(UC_ARM_REG_R1))


def build_model(directory):
    shared = Path(directory) / "libsound_prefix.so"
    cmd = [os.environ.get("CC", "cc"), "-std=c11", "-Wall", "-Wextra",
           "-Werror", "-O2", "-fPIC", "-shared", str(SOURCE), "-o", str(shared)]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    lib = ctypes.CDLL(str(shared))
    func = lib.fft_sound_playdef_prefix
    func.argtypes = (ctypes.c_uint32, ctypes.POINTER(PrefixResult))
    func.restype = ctypes.c_int
    return func


def model_output(function, arg):
    result = PrefixResult()
    if function(arg, ctypes.byref(result)) != 1:
        raise AssertionError("C model unexpectedly rejected a valid pointer")
    return result.next_pc, result.r0, result.r1


def verify(binary):
    sites, prefix = original(binary)
    failures = []
    count = 0
    with tempfile.TemporaryDirectory(prefix="fft-playdef-") as tmp:
        c_func = build_model(tmp)
        if c_func(0, None) != 0:
            raise AssertionError("C model accepted null output pointer")
        for r0 in upstream.R0_STATES:
            expected_c = model_output(c_func, r0)
            for cpsr in upstream.CPSR_STATES:
                arm = execute(sites, prefix, r0, cpsr)
                if arm != expected_c:
                    failures.append((r0, cpsr, arm, expected_c))
                count += 1
    if failures:
        raise AssertionError(f"Differential mismatch: {failures[:3]}")
    if count != 128:
        raise AssertionError(f"Expected 128 ARM/C differential cases, got {count}")
    return count, prefix


def render(binary):
    count, prefix = verify(binary)
    return "\n".join([
        "# Reconstrução funcional parcial: sound_request -> SysSE_PlayDef", "",
        f"ELF original SHA-256: `{upstream.ELF_SHA256}`.",
        f"Bytes A32 executados em SysSE_PlayDef: `{prefix.hex()}`.", "",
        "## 1. Desmontagem e estrutura verificadas", "",
        "| Endereço | Instrução | Observação |",
        "|---|---|---|",
        "| 0x26b374 / 0x2168e0 / 0x271314 | B | Três desvios originais encadeados |",
        "| 0x2b2cf8 | MOV R1,R0 | Copia identificador de entrada |",
        "| 0x2b2cfc | MOV R0,#0 | Define primeiro argumento do próximo corpo como zero |",
        "| 0x2b2d00 | B 0x2b2b7c | Desvio incondicional para corpo comum |", "",
        "## 2. Contrato semântico observado no Unicorn", "",
        f"- Rastros verificados: {count} (8 valores R0 x 16 configurações NZCV).",
        "- Na fronteira ANTES de 0x2b2b7c: PC=0x2b2b7c, R0=0, R1=R0 inicial.",
        "- R2-R14, SP, LR e flags NZCV preservados; nenhuma leitura/escrita de dados.",
        "- Precondições: A32 original, execução normal, estado e memória sintéticos.",
        "- Nenhuma instrução do destino 0x2b2b7c foi executada.", "",
        "## 3. Reimplementação independente em C", "",
        "- Fonte: `docs/re-tools/c-models/sound_playdef_prefix.c`.",
        "- Reimplementa somente o efeito observável deste prefixo; não reproduz áudio.", "",
        "## 4. Validação diferencial", "",
        f"- {count}/{count} estados comparados Unicorn x C: PASS.",
        "- Em todas as comparações: destino, R0 e R1 idênticos.",
        "- Os demais registradores, flags e memória são validados no lado ARM.",
        "- Nenhum certificado novo; não se demonstrou equivalência integral de SysSE_PlayDef.", "",
        "## Próxima etapa técnica", "",
        "- Desmontar e reconstruir o corpo comum em 0x2b2b7c.",
        "- Resolver a proveniência das referências globais e chamadas antes de executar",
        "  seus efeitos, controlando tabelas, estado e memória.", "",
    ])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--output", type=Path,
                   default=ROOT / "docs/re-results/SEMANTIC_SOUND_FUNCTIONAL_RECONSTRUCTION.md")
    args = p.parse_args()
    report = render(args.binary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print("SOUND_FUNCTIONAL_ARM_C_DIFFERENTIAL_CASES=128")
    print("SOUND_FUNCTIONAL_SCOPE=prefix_only")
    print("SOUND_FUNCTIONAL_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
