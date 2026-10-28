#!/usr/bin/env python3
"""Execute five real ARM sound-common-body prologue instructions and compare C.

The previous SysSE_PlayDef prefix passes R0=0/R1=input into 0x2b2b7c.
This experiment executes PUSH, PC literal LDR, SUB SP and two MOV instructions
under controlled memory/registers; STOPS BEFORE 0x2b2b90's indirect global LDR.
Never claims complete sound function semantics or issues certificates.
"""
import argparse
import ctypes
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
    UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
    UC_ARM_REG_SP, UC_ARM_REG_LR)

import semantic_evidence
import semantic_sound_functional_reconstruction as prior
import semantic_sound_three_entry_exec as seeds

ENTRY, STOP = 0x2B2B7C, 0x2B2B90
LITERAL_ADDR = 0x2B2CE8  # PC for 0x2b2b80 is 0x2b2b88; +0x160
STACK_TOP = 0x701000
CANARY_ADDR = 0x700F60
CANARY = bytes.fromhex("92011b88a9c45edf71743ca6d388bb40")
SOURCE = Path(__file__).resolve().parent / "c-models/sound_common_prologue.c"
PREFIX_HEX = "f0472de960319fe520d04de20060a0e10150a0e1"
STOP_HEX = "03009fe7"
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
         UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_LR)
SIGNATURE = (
    ("push", "{r4, r5, r6, r7, r8, sb, sl, lr}"),
    ("ldr", "r3, [pc, #0x160]"),
    ("sub", "sp, sp, #0x20"),
    ("mov", "r6, r0"),
    ("mov", "r5, r1"),
    ("ldr", "r0, [pc, r3]"),
)


class CResult(ctypes.Structure):
    _fields_ = [(key, ctypes.c_uint32) for key in
                ("next_pc", "sp", "r0", "r1", "r3", "r5", "r6")] + [
                ("saved", ctypes.c_uint32 * 8)]


def validate(code):
    if code.hex() != PREFIX_HEX + STOP_HEX:
        raise ValueError("Original common-prologue A32 signature changed")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    actual = [(ins.mnemonic, ins.op_str) for ins in md.disasm(code, ENTRY)]
    if actual != list(SIGNATURE):
        raise ValueError("Original common-prologue disassembly changed")
    if LITERAL_ADDR != (ENTRY + 4 + 8 + 0x160):
        raise ValueError("PC-relative literal address drift")
    return True


def original(binary):
    binary = Path(binary)
    if hashlib.sha256(binary.read_bytes()).hexdigest() != seeds.ELF_SHA256:
        raise ValueError("Wrong original ELF")
    prior.original(binary)  # full original wrapper and incoming branch provenance
    code = semantic_evidence.read_function(binary, ENTRY, STOP - ENTRY + 4)
    literal = semantic_evidence.read_function(binary, LITERAL_ADDR, 4)
    validate(code)
    return code, literal


def initial_state(arg):
    if arg not in seeds.R0_STATES:
        raise ValueError("Unsupported input sample")
    state = seeds.seeded_registers(arg)
    state[UC_ARM_REG_R0] = 0
    state[UC_ARM_REG_R1] = arg
    return state


def arm_execute(code, literal, arg, flags):
    validate(code)
    if len(literal) != 4 or flags not in range(16):
        raise ValueError("Invalid original literal or ARM flags")
    before = initial_state(arg)
    m = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    m.mem_map(ENTRY & ~0xFFF, 0x1000, UC_PROT_ALL)
    m.mem_map(0x700000, 0x1000, UC_PROT_ALL)
    m.mem_write(ENTRY, code)
    m.mem_write(LITERAL_ADDR, literal)
    m.mem_write(CANARY_ADDR, CANARY)
    cpsr = flags << 28 | 0x10
    m.reg_write(UC_ARM_REG_CPSR, cpsr)
    for reg, value in before.items():
        m.reg_write(reg, value)
    trace, reads, writes = [], [], []

    def on_code(uc, address, size, unused):
        trace.append(address)
        if address == STOP:
            uc.emu_stop()

    m.hook_add(UC_HOOK_CODE, on_code)
    m.hook_add(UC_HOOK_MEM_READ,
               lambda uc, a, address, size, value, unused:
               reads.append((address, size)))
    m.hook_add(UC_HOOK_MEM_WRITE,
               lambda uc, a, address, size, value, unused:
               writes.append((address, size, value & 0xFFFFFFFF)))
    m.emu_start(ENTRY, STOP + 4, count=6, timeout=1_000_000)

    if trace != list(range(ENTRY, STOP + 4, 4)) or m.reg_read(UC_ARM_REG_PC) != STOP:
        raise AssertionError("Unexpected ARM original prologue trace")
    if reads != [(LITERAL_ADDR, 4)]:
        raise AssertionError(f"Unexpected prologue memory reads: {reads}")
    saved = tuple(before[r] for r in SAVED)
    old_sp = before[UC_ARM_REG_SP]
    expected_writes = [(old_sp - 32 + 4*i, 4, saved[i]) for i in range(8)]
    if sorted(writes) != sorted(expected_writes):
        raise AssertionError(f"Wrong 8 ARM PUSH writes: {writes}")
    if m.reg_read(UC_ARM_REG_SP) != old_sp - 64:
        raise AssertionError("Incorrect original 64-byte stack frame")
    if bytes(m.mem_read(CANARY_ADDR, len(CANARY))) != CANARY:
        raise AssertionError("Stack underflow reached sentinel")
    for i, word in enumerate(saved):
        if int.from_bytes(m.mem_read(old_sp - 32 + i*4, 4), "little") != word:
            raise AssertionError("Saved ARM register differs from stack memory")
    literal_value = int.from_bytes(literal, "little")
    expected = {UC_ARM_REG_R3: literal_value, UC_ARM_REG_R5: arg,
                UC_ARM_REG_R6: 0, UC_ARM_REG_SP: old_sp - 64}
    for reg, value in before.items():
        if m.reg_read(reg) != expected.get(reg, value):
            raise AssertionError(f"Unexpected register effect in prologue: {reg}")
    if (m.reg_read(UC_ARM_REG_CPSR) & 0xF000003F) != (cpsr & 0xF000003F):
        raise AssertionError("Original A32 prologue modified CPSR flags or mode")
    return (m.reg_read(UC_ARM_REG_PC), m.reg_read(UC_ARM_REG_SP),
            m.reg_read(UC_ARM_REG_R0), m.reg_read(UC_ARM_REG_R1),
            m.reg_read(UC_ARM_REG_R3), m.reg_read(UC_ARM_REG_R5),
            m.reg_read(UC_ARM_REG_R6), saved)


def build_c_model(tmp):
    libpath = Path(tmp) / "libsound_common_prologue.so"
    subprocess.run([os.environ.get("CC", "cc"), "-std=c11", "-Wall", "-Wextra",
                    "-Werror", "-O2", "-fPIC", "-shared", str(SOURCE), "-o",
                    str(libpath)], check=True, capture_output=True, text=True)
    fn = ctypes.CDLL(str(libpath)).fft_sound_common_prologue
    fn.argtypes = (ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32,
                   ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(CResult))
    fn.restype = ctypes.c_int
    return fn


def c_execute(function, arg, literal):
    state = initial_state(arg)
    saved = (ctypes.c_uint32 * 8)(*(state[r] for r in SAVED))
    out = CResult()
    literal_value = int.from_bytes(literal, "little")
    if function(arg, STACK_TOP, literal_value, saved, ctypes.byref(out)) != 1:
        raise AssertionError("C model rejected valid arguments")
    return (out.next_pc, out.sp, out.r0, out.r1, out.r3, out.r5,
            out.r6, tuple(out.saved))


def verify(binary):
    code, literal = original(binary)
    count = 0
    with tempfile.TemporaryDirectory(prefix="fft-common-prologue-") as tmp:
        function = build_c_model(tmp)
        if function(0, STACK_TOP, 0, None, None) != 0:
            raise AssertionError("C model failed null-output guard")
        for arg in seeds.R0_STATES:
            reference = c_execute(function, arg, literal)
            for flags in range(16):
                actual = arm_execute(code, literal, arg, flags)
                if actual != reference:
                    raise AssertionError(
                        f"ARM/C common-prologue mismatch arg={arg:x},flags={flags:x}")
                count += 1
    if count != 128:
        raise AssertionError("Incomplete ARM/C prologue sample set")
    return count, literal


def render(binary):
    count, literal = verify(binary)
    return "\n".join([
        "# Corpo comum de som 0x2b2b7c: prólogo ARM e reconstrução C", "",
        "ELF SHA-256: " + seeds.ELF_SHA256, "",
        "## Instruções originais de 0x2b2b7c até 0x2b2b8c", "",
        "- PUSH {R4,R5,R6,R7,R8,R9,R10,LR}: 8 palavras / 32 bytes gravados na pilha.",
        f"- LDR R3,[PC,#0x160]: lê literal original em 0x{LITERAL_ADDR:x}; "
        f"valor=0x{int.from_bytes(literal,'little'):08x}.",
        "- SUB SP,SP,#0x20: 32 bytes adicionais, total de 64 bytes de profundidade.",
        "- MOV R6,R0 e MOV R5,R1: entradas do wrapper R0=0, R1=argumento.",
        "- Parada ANTES de 0x2b2b90: LDR R0,[PC,R3], acesso indireto a estado global.", "",
        "## Verificação real e modelo independente", "",
        f"- Microexecuções Unicorn das 5 instruções reais: {count}; "
        f"instruções ARM efetivamente executadas: {count*5}.",
        "- Verificados: PC/SP/R0/R1/R3/R5/R6, demais registradores, 8 gravações "
        "da pilha, 1 leitura literal original e NZCV.",
        "- Modelo C em docs/re-tools/c-models/sound_common_prologue.c, "
        "compilado com -std=c11 -Werror.",
        f"- Comparações diferenciais completas do prólogo ARM x C: {count}/{count} PASS.", "",
        "## Limites", "",
        "- Acesso indireto de 0x2b2b90 NAO foi executado; sem semântica de áudio, "
        "chamadas externas, retornos ou estado global comprovados.",
        "- Nenhuma função adicional certificada; permanecem 303 contratos BX LR "
        "preexistentes, sujeitos ao gate independente.",
        "- Próximo alvo: resolver proveniência e mapeamento seguro do ponteiro "
        "de 0x2b2b90 antes de executar sua leitura.", "",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=semantic_evidence.ROOT /
                        "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--output", type=Path, default=semantic_evidence.ROOT /
                        "docs/re-results/SEMANTIC_SOUND_COMMON_PROLOGUE.md")
    args = parser.parse_args()
    result = render(args.binary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    print("SOUND_COMMON_PROLOGUE_ARM_C_STATES=128")
    print("SOUND_COMMON_PROLOGUE_ARM_INSTRUCTIONS_EXECUTED=640")
    print("SOUND_COMMON_PROLOGUE_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
