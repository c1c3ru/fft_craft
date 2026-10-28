#!/usr/bin/env python3
"""Conservative original-ELF audit and bounded entry execution at 0x2b2b7c.

Only linear A32 disassembly is claimed. Execution stops BEFORE the first
branch, memory access, PC-dependent or unmodelled instruction. This does NOT
certify playback, complete reachability, memory effects or return behavior.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_GRP_JUMP, CS_GRP_CALL, CS_GRP_RET
from capstone.arm import ARM_OP_MEM, ARM_OP_REG, ARM_REG_PC
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

import semantic_evidence
import semantic_sound_functional_reconstruction as upstream
import semantic_sound_three_entry_exec as regs

ENTRY = 0x2B2B7C
SIZE = 128
SAFE_MAX = 16
SENTINEL = 0x500000
SENTINEL_VALUE = bytes.fromhex("edb02f936a28a1c77a48fd239a009bd1")


def original(binary):
    binary = Path(binary)
    if hashlib.sha256(binary.read_bytes()).hexdigest() != regs.ELF_SHA256:
        raise ValueError("Original ELF identity differs")
    upstream.original(binary)  # proves exact predecessor prefix and final branch
    raw = semantic_evidence.read_function(binary, ENTRY, SIZE)
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(raw, ENTRY))
    if not instructions or instructions[0].address != ENTRY:
        raise ValueError("No original ARM instruction at body entry")
    decoded = sum(x.size for x in instructions)
    if decoded > SIZE or any(x.size != 4 for x in instructions):
        raise ValueError("Malformed original A32 instruction sequence")
    return raw, instructions


def unsafe_reason(insn):
    if (insn.group(CS_GRP_JUMP) or insn.group(CS_GRP_CALL)
            or insn.group(CS_GRP_RET)):
        return "branch/call/return"
    if any(op.type == ARM_OP_MEM for op in insn.operands):
        return "memory-reference"
    if any(op.type == ARM_OP_REG and op.reg == ARM_REG_PC
           for op in insn.operands):
        return "PC-register"
    if insn.mnemonic.startswith(("svc", "swi", "udf", "bkpt", "ldr", "str",
                                "ldm", "stm", "push", "pop", "mcr", "mrc")):
        return "unmodelled-side-effect"
    if insn.mnemonic.lower() in {"cps", "msr", "mrs", "setend", "rfe", "srs"}:
        return "mode-or-status-control"
    if insn.mnemonic.startswith(("v", "f", "swp", "ldrex", "strex")):
        return "unmodelled-extension"
    return ""


def boundary(insns):
    count = 0
    for insn in insns[:SAFE_MAX]:
        reason = unsafe_reason(insn)
        if reason:
            return count, insn.address, reason
        count += 1
    return count, ENTRY + 4 * count, "bounded-safe-prefix-limit"


def execute(raw, insns, arg, nzcv):
    if arg not in regs.R0_STATES or nzcv not in range(16):
        raise ValueError("Unexpected ARM sample")
    count, stop, reason = boundary(insns)
    if stop >= ENTRY + len(raw):
        raise ValueError("No mapped stop boundary")
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(ENTRY & ~0xFFF, 0x1000, UC_PROT_ALL)
    uc.mem_map(SENTINEL, 0x1000, UC_PROT_ALL)
    uc.mem_write(ENTRY, raw)
    uc.mem_write(SENTINEL, SENTINEL_VALUE)
    initial = regs.seeded_registers(arg)
    initial[UC_ARM_REG_R0] = 0
    initial[UC_ARM_REG_R1] = arg
    uc.reg_write(UC_ARM_REG_CPSR, (nzcv << 28) | 0x10)
    for reg, value in initial.items():
        uc.reg_write(reg, value)
    trace, reads, writes = [], [], []

    def hook_code(machine, addr, size, unused):
        trace.append(addr)
        if addr == stop:
            machine.emu_stop()

    uc.hook_add(UC_HOOK_CODE, hook_code)
    uc.hook_add(UC_HOOK_MEM_READ, lambda m, a, addr, size, value, u: reads.append((addr, size)))
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda m, a, addr, size, value, u: writes.append((addr, size)))
    uc.emu_start(ENTRY, ENTRY + len(raw), timeout=1_000_000, count=count + 1)
    expected = list(range(ENTRY, stop + 4, 4))
    if trace != expected or uc.reg_read(UC_ARM_REG_PC) != stop:
        raise AssertionError("Unapproved branch/PC transition before boundary")
    if reads or writes or bytes(uc.mem_read(SENTINEL, len(SENTINEL_VALUE))) != SENTINEL_VALUE:
        raise AssertionError("Unexpected data access in safe prefix")
    return {"executed_words": count, "boundary": stop, "reason": reason,
            "trace": tuple(trace), "r0": uc.reg_read(UC_ARM_REG_R0),
            "r1": uc.reg_read(UC_ARM_REG_R1), "fully_certified": False}


def render(binary):
    raw, insns = original(binary)
    prefix, stop, reason = boundary(insns)
    rows = [
        "# Corpo comum de som 0x2b2b7c — auditoria e execução limitada", "",
        "ELF original SHA-256: " + regs.ELF_SHA256,
        f"Janela: 0x{ENTRY:x}..0x{ENTRY+SIZE-1:x} ({SIZE} bytes).",
        "Janela SHA-256: " + hashlib.sha256(raw).hexdigest(), "",
        "## Desmontagem A32 linear; alcance ainda nao demonstrado", "",
        "| Endereço | Bytes do ELF | ARM | Risco de continuação |",
        "|---|---|---|---|",
    ]
    for insn in insns:
        off = insn.address - ENTRY
        rows.append(f"| 0x{insn.address:x} | {raw[off:off+4].hex()} | "
                    f"{insn.mnemonic} {insn.op_str} | {unsafe_reason(insn) or 'a avaliar'} |")
    rows += ["", "## Prefixo seguro observado", "",
             f"Primeira fronteira: 0x{stop:x}, motivo: {reason}.",
             f"Instruções elegíveis antes da fronteira: {prefix}.",
             "A instrução na fronteira NÃO é executada.",
             "O código C do prefixo anterior entrega R0=0 e R1=argumento; "
             "esses são estados sintéticos para o próximo corpo.", ""]
    tested = 0
    for r0 in regs.R0_STATES:
        for nzcv in range(16):
            result = execute(raw, insns, r0, nzcv)
            if result["executed_words"] != prefix:
                raise AssertionError("Variable prefix length was not anticipated")
            tested += 1
    rows += [
        f"Estados controlados verificados: {tested} (8 R1 x 16 NZCV).",
        f"Instruções originais executadas por estado: {prefix}.",
        "Sem leitura/escrita de memória de dados antes da fronteira.",
        "## Limites e próxima etapa", "",
        "- Não foi executada a primeira instrução com efeito potencialmente externo.",
        "- A janela linear pode conter dados inline e não prova fluxo além da fronteira.",
        "- A semântica do áudio, parâmetros globais, retornos e efeitos externos continuam desconhecidos.",
        "- Reconstituir explicitamente a primeira leitura/escrita ou chamada com "
        "memória mapeada e invariantes, antes de estender o contrato C.",
        "- Novos certificados semânticos nesta etapa: 0; os 303 BX LR permanecem intactos.", "",
    ]
    return "\n".join(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path,
                   default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--output", type=Path,
                   default=semantic_evidence.ROOT /
                   "docs/re-results/SEMANTIC_SOUND_COMMON_BODY_2B2B7C.md")
    args = p.parse_args()
    report = render(args.binary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print("SOUND_COMMON_BODY_WINDOW=128")
    print("SOUND_COMMON_BODY_TEST_STATES=128")
    print("SOUND_COMMON_BODY_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
