#!/usr/bin/env python3
"""Find and microexecute exact four-byte ARM BX LR leaf functions in the ELF.

Original machine words, not synthetic replacements, are executed. These are
review candidates for a complete contract, NOT automatic certifications.
"""
import argparse
import hashlib
import json
from pathlib import Path

from unicorn import (
    Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE,
    UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE,
)
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
    UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_CPSR,
)

import semantic_coverage
import semantic_evidence

BX_LR = bytes.fromhex("1eff2fe1")  # 0xe12fff1e (ARM little-endian)
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
        UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR)
STOP = 0x710100
# Four independent test states; every LR is a valid ARM-aligned return address.
STATES = ((0, 0), (0xF0000000, 1), (0x60000000, 2),
          (0x90000000, 0xDEADBEEF))


def find_candidates(rows, binary, reader=semantic_evidence.read_function):
    """Return exact isolated ARM BX LR words from unique inventory entries."""
    inspected = 0
    found = []
    for row in rows:
        address = int(row["address"], 16)
        if row["size"] != 4 or address & 3:
            continue
        inspected += 1
        code = reader(binary, address, 4)
        if code == BX_LR:
            found.append(row)
    return inspected, sorted(found, key=lambda r: r["address"])


def verify_execution(address, code, states=STATES):
    """Execute a bounded original ARM word; check full visible register state."""
    if code != BX_LR or address & 3:
        raise ValueError("Not an aligned single-instruction ARM BX LR")
    for flags, seed in states:
        emulator = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        emulator.mem_map(address & ~0xFFF, 0x1000, UC_PROT_ALL)
        emulator.mem_map(STOP & ~0xFFF, 0x1000, UC_PROT_ALL)
        emulator.mem_write(address, code)
        emulator.mem_write(STOP, bytes.fromhex("0000a0e1"))
        before = {reg: ((seed + i * 0x11111111) & 0xFFFFFFFF)
                  for i, reg in enumerate(REGS)}
        before[UC_ARM_REG_SP] = 0x700100
        before[UC_ARM_REG_LR] = STOP
        emulator.reg_write(UC_ARM_REG_CPSR, 0x10 | flags)
        for reg, value in before.items():
            emulator.reg_write(reg, value)
        cpsr = emulator.reg_read(UC_ARM_REG_CPSR)
        trace, mem_access = [], []
        def on_instruction(uc, pc, size, unused):
            trace.append(pc)
            if pc == STOP:
                uc.emu_stop()
        def on_memory(uc, access, addr, size, value, unused):
            mem_access.append((access, addr, size, value))
        emulator.hook_add(UC_HOOK_CODE, on_instruction)
        emulator.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, on_memory)
        emulator.emu_start(address, STOP + 4, count=3, timeout=1_000_000)
        if trace != [address, STOP] or mem_access:
            raise AssertionError(f"Unexpected BX LR trace or data access at {address:08x}")
        if emulator.reg_read(UC_ARM_REG_PC) != STOP:
            raise AssertionError("BX LR did not return to LR")
        if emulator.reg_read(UC_ARM_REG_CPSR) != cpsr:
            raise AssertionError("CPSR modified by BX LR")
        if any(emulator.reg_read(reg) != value for reg, value in before.items()):
            raise AssertionError("BX LR modified an input register")
    return len(states)


def run(binary, inventory, output, report_path):
    digest = hashlib.sha256(Path(binary).read_bytes()).hexdigest()
    # Validate alias addresses/sizes and reuse the existing certification ledger.
    rows = semantic_coverage.ledger(Path(inventory), digest, {})
    scanned, candidates = find_candidates(rows, Path(binary))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    proofs = []
    for row in candidates:
        address = int(row["address"], 16)
        code = semantic_evidence.read_function(Path(binary), address, 4)
        count = verify_execution(address, code)
        record = {
            "address": row["address"], "name": row["name"],
            "binary_sha256": digest, "size": 4,
            "semantic_status": "partial", "certified": False,
            "evidence_class": "unicorn_complete_single_opcode_sampled_inputs",
            "machine_samples_passed": count, "machine_samples_failed": 0,
            "instruction_encoding": code.hex(),
            "verified_local_effects": [
                "branch_to_even_LR", "all_general_purpose_registers_unchanged",
                "CPSR_unchanged", "zero_data_memory_reads_or_writes"
            ],
            "contract_candidate": "ARM-state BX LR returns to even aligned LR, "
                                  "preserving general registers, flags, and data memory",
            "preconditions": ["ARM state", "even executable LR", "mapped instruction"],
            "unverified": ["complete_formal_input_domain", "caller_environment",
                           "reference_equivalence_review"],
        }
        (output / (row["address"] + ".json")).write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        proofs.append(record)
    lines = ["# Candidatas de contrato semântico: folhas ARM BX LR", "",
             f"ELF SHA-256: `{digest}`", "",
             f"- Entradas ARM de 4 bytes inspecionadas: **{scanned}**",
             f"- Candidatas com opcode exato `E12FFF1E`: **{len(proofs)}**",
             f"- Microexecuções Unicorn válidas: **{sum(p['machine_samples_passed'] for p in proofs)}**", "",
             "> Cada teste executa o opcode **original** do ELF e verifica PC, "
             "registradores, CPSR e ausência de acessos a dados. "
             "**Não constitui certificação semântica integral:** a cobertura "
             "formal dos estados e a revisão da equivalência continuam pendentes.", "",
             "| Endereço | Função | Testes |", "|---|---|---:|"]
    for item in proofs[:100]:
        lines.append(f"| `{item['address']}` | "
                     f"{item['name'].replace('|', '/')} | "
                     f"{item['machine_samples_passed']} |")
    if len(proofs) > 100:
        lines += ["", f"Demais {len(proofs)-100} registros: arquivos JSON por endereço."]
    lines += ["", "A fila de certificação deve revisar os contratos e "
              "seus domínios antes de promover qualquer candidato.", ""]
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"BXLR_FOUR_BYTE_ENTRIES_SCANNED={scanned}")
    print(f"BXLR_CANDIDATES={len(proofs)}")
    print(f"BXLR_SAMPLES_PASSED={sum(p['machine_samples_passed'] for p in proofs)}")
    print("BXLR_CERTIFIED=0")
    return proofs


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    p.add_argument("--inventory", type=Path, default=semantic_coverage.INVENTORY)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    run(args.binary, args.inventory, args.output, args.report)


if __name__ == "__main__":
    main()
