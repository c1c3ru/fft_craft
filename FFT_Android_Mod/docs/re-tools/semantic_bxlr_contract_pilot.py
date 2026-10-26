#!/usr/bin/env python3
"""Pilot complete *local* ARM BX LR contracts, without claiming full certification.

Uses the original four-byte ELF instruction, a structural ISA decode, and
independent ARM/Thumb return-path Unicorn checks. Global equivalence, external
effects and reviewer approval remain outside the proved scope.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
    UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_CPSR,
)

import semantic_coverage
import semantic_evidence
import semantic_leaf_bxlr as leaf
import arm_bx_reference as arm_model

FLAGS = tuple(n << 28 for n in range(16))  # Exhaustive 16 NZCV combinations
RETURN = 0x710100
RAM = 0x700000
RAM_MARKER = b"CHECKED-ARM-RETURN"
GENERAL = leaf.REGS


def isa_contract(code):
    """Check the complete unconditional ARM instruction and its sole operand."""
    if len(code) != 4 or int.from_bytes(code, "little") != 0xE12FFF1E:
        raise ValueError("Not the exact unconditional ARM BX LR encoding")
    insns = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(code, 0x1000))
    if len(insns) != 1 or (insns[0].mnemonic, insns[0].op_str) != ("bx", "lr"):
        raise ValueError("Disassembler disagrees with the ARM instruction encoding")
    return "BX LR: target=R14[31:1]:0; CPSR.T=R14[0]; R0-R14 and data memory preserved"


def verify_interworking(address, code, flags=FLAGS):
    """Differentially test ARM->ARM and ARM->Thumb with register and RAM canaries."""
    isa_contract(code)
    if address % 4 or (address & ~0xFFF) in (RETURN & ~0xFFF, RAM & ~0xFFF):
        raise ValueError("Invalid or overlapping executable address")
    samples = 0
    for thumb in (False, True):
        for sample_no, bits in enumerate(flags):
            uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
            uc.mem_map(address & ~0xFFF, 0x1000, UC_PROT_ALL)
            uc.mem_map(RETURN & ~0xFFF, 0x1000, UC_PROT_ALL)
            uc.mem_map(RAM, 0x1000, UC_PROT_ALL)
            uc.mem_write(address, code)
            uc.mem_write(RETURN, b"\x00\xbf\x00\xbf")
            uc.mem_write(RAM + 0x80, RAM_MARKER)
            expected = {reg: ((0x12345678 + sample_no * 0x10203 + i * 0x11111111)
                              & 0xFFFFFFFF) for i, reg in enumerate(GENERAL)}
            expected[UC_ARM_REG_SP] = RAM + 0x400
            expected[UC_ARM_REG_LR] = RETURN | int(thumb)
            uc.reg_write(UC_ARM_REG_CPSR, 0x10 | bits)
            for reg, value in expected.items():
                uc.reg_write(reg, value)
            start_cpsr = uc.reg_read(UC_ARM_REG_CPSR)
            pcs, accesses = [], []

            def on_code(emu, pc, size, user):
                pcs.append(pc)
                if pc == RETURN:
                    emu.emu_stop()

            def on_memory(emu, kind, location, size, value, user):
                accesses.append((kind, location))

            uc.hook_add(UC_HOOK_CODE, on_code)
            uc.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, on_memory)
            uc.emu_start(address, RETURN + 4, count=3, timeout=1_000_000)
            actual_pc = uc.reg_read(UC_ARM_REG_PC)
            actual_cpsr = uc.reg_read(UC_ARM_REG_CPSR)
            # ARM BX performs interworking via bit zero of LR, not arithmetic.
            expected_pc, target_cpsr = arm_model.branch_exchange_lr(
                code, expected[UC_ARM_REG_LR], start_cpsr)
            if pcs != [address, expected_pc] or actual_pc != expected_pc:
                raise AssertionError(f"incorrect ARM/Thumb return path at {address:08x}")
            if actual_cpsr != target_cpsr:
                raise AssertionError(f"unexpected CPSR after BX LR at {address:08x}")
            if any(uc.reg_read(reg) != val for reg, val in expected.items()):
                raise AssertionError(f"modified preserved register at {address:08x}")
            if accesses or bytes(uc.mem_read(RAM + 0x80, len(RAM_MARKER))) != RAM_MARKER:
                raise AssertionError(f"unexpected data memory access at {address:08x}")
            samples += 1
    return samples


def run(binary, inventory, output, report, limit=303):
    if not 1 <= limit <= 303:
        raise ValueError("pilot size must be 1..303")
    binary, inventory = Path(binary), Path(inventory)
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    rows = semantic_coverage.ledger(inventory, digest, {})
    inspected, candidates = leaf.find_candidates(rows, binary)
    chosen = candidates[:limit]
    if len(chosen) < limit:
        raise ValueError("not enough original ELF BX LR candidates for pilot")
    output, report = Path(output), Path(report)
    output.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    for row in chosen:
        addr = int(row["address"], 16)
        code = semantic_evidence.read_function(binary, addr, 4)
        contract = isa_contract(code)
        arm_model.branch_exchange_lr(code, RETURN, 0x10)
        arm_model.branch_exchange_lr(code, RETURN | 1, 0x10)
        samples = verify_interworking(addr, code)
        record = {
            "address": row["address"], "name": row["name"],
            "binary_sha256": digest, "size": 4,
            "instruction_sha256": hashlib.sha256(code).hexdigest(),
            "instruction_word": code.hex(),
            "semantic_status": "partial", "certified": False,
            "contract_stage": "local_isa_contract_checked_review_pending",
            "contract": contract,
            "preconditions": ["ARM state at entry", "executable mapped 4-byte instruction",
                              "valid mapped LR destination", "normal execution context"],
            "postconditions": ["PC=LR & ~1", "CPSR.T=LR & 1",
                               "other CPSR bits preserved", "R0-R14 preserved"],
            "memory_effects": ["none in the decoded function body"],
            "control_flow": ["only unconditional BX LR; no internal callees"],
            "machine_samples_passed": samples,
            "machine_samples_failed": 0,
            "verified_return_modes": ["ARM", "Thumb"],
            "test_evidence": ["original ELF instruction", "Capstone exact opcode",
                              "independent pure A32 BX LR transition model",
                              "Unicorn PC/CPSR/general-register/memory differential"],
            "reviewer": None,
            "test_oracle": "arm_bx_reference.branch_exchange_lr",
            "unverified": ["independent ISA-model review",
                           "environmental exception behavior",
                           "human verification of full-contract scope"],
        }
        (output / (row["address"] + ".json")).write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Validação dos contratos locais BX LR — todas as candidatas", "",
             f"ELF SHA-256: `{digest}`", "",
             f"- Entradas de 4 bytes ARM verificadas: **{inspected}**",
             f"- Folhas BX LR disponíveis: **{len(candidates)}**",
             f"- Contratos locais verificados neste lote: **{len(chosen)}**",
             f"- Testes diferenciais ARM/Thumb deste lote: **{2 * len(FLAGS) * len(chosen)}**", "",
             "**Status:** pronto para revisão; **0 novas certificações integrais**. "
             "As pós-condições cobrem o corpo de uma instrução no contexto ARM "
             "normal. A equivalência global, os casos de exceção e a aprovação "
             "de revisor permanecem pendentes.", "",
             "| Endereço | Símbolo | Corpo completo | ARM / Thumb |",
             "|---|---|---|---|"]
    for row in chosen:
        lines.append(f"| `{row['address']}` | {row['name'].replace('|','/')} "
                     "| `BX LR` | 4 + 4 testes |")
    lines += ["", "Arquivos individuais JSON no artifact do workflow. "
              "Eles não são inseridos automaticamente em `semantic-certificates.json`.", ""]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"BXLR_CONTRACT_PILOT_READY={len(chosen)}")
    print(f"BXLR_CONTRACT_PILOT_SAMPLES={len(chosen)*2*len(FLAGS)}")
    print("BXLR_CONTRACT_PILOT_CERTIFIED=0")
    return len(chosen)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    p.add_argument("--inventory", type=Path, default=semantic_coverage.INVENTORY)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--limit", type=int, default=303)
    a = p.parse_args()
    run(a.binary, a.inventory, a.output, a.report, a.limit)


if __name__ == "__main__":
    main()
