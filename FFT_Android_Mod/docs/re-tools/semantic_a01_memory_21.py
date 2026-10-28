#!/usr/bin/env python3
"""A01: bounded A32 byte and displaced-word accesses for original ELF.

This loop only microexecutes a narrowly decoded opcode immediately followed by
BX LR. It compares original bytes in Unicorn to an independently written
state/memory model, and never changes formal semantic certificates.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
import semantic_evidence
import semantic_manifest_audit as manifest
import semantic_loop_250 as prior
import semantic_remaining_34 as store

MASK = 0xffffffff
BASE = 0x500100
RETURN = 0x710100
CANARY = bytes.fromhex("197dda3c89fe2011")
MEM_SIZE = 0x980


def decode(raw, address):
    """AL; ARM immediate positive pre-indexed; no writeback, PC or signed mode."""
    if address % 4 or len(raw) != 8:
        return None
    word = int.from_bytes(raw[:4], "little")
    if int.from_bytes(raw[4:], "little") != prior.BX_LR:
        return None
    if (word >> 28 != 0xe or (word >> 26) & 3 != 1
            or (word >> 25) & 1 != 0 or (word >> 24) & 1 != 1
            or (word >> 23) & 1 != 1 or (word >> 21) & 1 != 0):
        return None
    base, register, offset = (word >> 16) & 15, (word >> 12) & 15, word & 0xfff
    byte, load = (word >> 22) & 1, (word >> 20) & 1
    if base != 0 or offset > 0x600:
        return None
    if (byte, load, register) == (1, 0, 1):
        operation, width = "strb_r1", 1
    elif (byte, load, register) == (1, 1, 0):
        operation, width = "ldrb_r0", 1
    elif (byte, load, register) == (0, 1, 0) and offset > 64 and offset % 4 == 0:
        operation, width = "ldr_large_r0", 4
    else:
        return None
    return {"op": operation, "width": width, "offset": offset,
            "opcode": raw.hex()}


def classify(binary, previous_entries):
    """Check bytes and Capstone on every one of the 21 prior excluded entries."""
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    result = []
    for entry in previous_entries:
        if entry["contract"] is not None:
            continue
        address = int(entry["address"], 16)
        raw = semantic_evidence.read_function(binary, address, entry["size"])
        if raw.hex() != entry["raw_hex"]:
            raise ValueError("Original ELF disagrees with preceding checkpoint")
        spec = decode(raw, address)
        if spec:
            instructions = list(md.disasm(raw, address))
            expected = {"strb_r1": "strb", "ldrb_r0": "ldrb",
                        "ldr_large_r0": "ldr"}[spec["op"]]
            if (len(instructions) != 2 or instructions[0].mnemonic != expected
                    or instructions[1].mnemonic != "bx"
                    or instructions[1].op_str != "lr"):
                raise ValueError("Decoder disagrees with Capstone at " + entry["address"])
        result.append({"address": entry["address"], "size": entry["size"],
                       "raw_hex": entry["raw_hex"], "assembly": entry["assembly"],
                       "contract": spec,
                       "status": "bounded_candidate" if spec else "unmodeled_not_executed"})
    return result


def expected_effect(spec, seed):
    """Reference model: explicit byte-array mutation, independent of ARM emulator."""
    registers = [(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    registers[0] = BASE
    raw = bytearray((i * 29 + (seed & 255)) & 255 for i in range(MEM_SIZE))
    raw[0x900:0x908] = CANARY
    offset = spec["offset"]
    width = spec["width"]
    before = bytes(raw)
    value = int.from_bytes(raw[offset:offset + width], "little")
    if spec["op"] == "strb_r1":
        value = registers[1] & 255
        raw[offset] = value
        writes, reads = [(BASE + offset, 1, value)], []
    else:
        registers[0] = value
        reads, writes = [(BASE + offset, width)], []
    return registers, before, bytes(raw), reads, writes


def execute(binary, item, seed, flags):
    from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                         UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
    from unicorn.arm_const import (
        UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
        UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
        UC_ARM_REG_R12)
    spec = item["contract"]
    if spec is None:
        raise ValueError("Refusing execution without a bounded access contract")
    address = int(item["address"], 16)
    raw = semantic_evidence.read_function(binary, address, item["size"])
    if raw.hex() != item["raw_hex"] or decode(raw, address) != spec:
        raise ValueError("Changed original ELF or opcode decoding")
    wanted_regs, initial_memory, final_memory, reads_expected, writes_expected = expected_effect(spec, seed)
    initial_regs = [(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    initial_regs[0] = BASE
    gprs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
            UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
            UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
            UC_ARM_REG_R11, UC_ARM_REG_R12)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in sorted({address & ~0xfff, (address + 4) & ~0xfff,
                        RETURN & ~0xfff, BASE & ~0xfff}):
        machine.mem_map(page, 0x1000, UC_PROT_ALL)
    machine.mem_write(address, raw)
    machine.mem_write(RETURN, bytes(4))
    machine.mem_write(BASE, initial_memory)
    machine.reg_write(UC_ARM_REG_CPSR, flags | 0x10)
    for reg, value in zip(gprs, initial_regs):
        machine.reg_write(reg, value)
    machine.reg_write(UC_ARM_REG_SP, 0x700ffc)
    machine.reg_write(UC_ARM_REG_LR, RETURN)
    code_trace, reads, writes = [], [], []

    def code_hook(emu, pc, size, unused):
        code_trace.append(pc)
        if pc == RETURN:
            emu.emu_stop()

    def read_hook(emu, access, pos, size, value, unused):
        reads.append((pos, size))

    def write_hook(emu, access, pos, size, value, unused):
        writes.append((pos, size, value & ((1 << (8 * size)) - 1)))

    machine.hook_add(UC_HOOK_CODE, code_hook)
    machine.hook_add(UC_HOOK_MEM_READ, read_hook)
    machine.hook_add(UC_HOOK_MEM_WRITE, write_hook)
    try:
        machine.emu_start(address, MASK, timeout=1_000_000, count=4)
    except Exception as exc:
        raise AssertionError("Unicorn failed address=" + item["address"]
                             + " trace=" + str(code_trace)) from exc
    if code_trace != [address, address + 4, RETURN] or machine.reg_read(UC_ARM_REG_PC) != RETURN:
        raise AssertionError("Unexpected original ELF ARM control flow")
    if reads != reads_expected or writes != writes_expected:
        raise AssertionError("Memory access trace differs: reads="
                             + str(reads) + " writes=" + str(writes))
    if bytes(machine.mem_read(BASE, MEM_SIZE)) != final_memory:
        raise AssertionError("Unexpected byte mutation or memory canary corruption")
    if any(machine.reg_read(r) != value for r, value in zip(gprs, wanted_regs)):
        raise AssertionError("Original ARM registers differ from reference")
    if machine.reg_read(UC_ARM_REG_SP) != 0x700ffc or machine.reg_read(UC_ARM_REG_LR) != RETURN:
        raise AssertionError("SP/LR unexpectedly modified")
    if (machine.reg_read(UC_ARM_REG_CPSR) & 0xf000003f) != ((flags | 0x10) & 0xf000003f):
        raise AssertionError("CPSR flags or user mode unexpectedly changed")


def checkpoint(digest, inventory, prior_digest, entries, rounds):
    return {"schema": 1, "elf_sha256": digest,
            "inventory_sha256": inventory, "prior_checkpoint_sha256": prior_digest,
            "entries": entries, "rounds": rounds, "new_certificates": 0}


def render(data):
    entries = data["entries"]
    count = sum(len(r["addresses"]) for r in data["rounds"])
    lines = [
        "# A01: contratos A32 de byte e palavra deslocada — ELF original", "",
        "ELF SHA-256: " + data["elf_sha256"], "",
        "Entradas herdadas ainda não modeladas: " + str(len(entries)) + "; "
        + "novos candidatos microexecutados: " + str(count) + "; "
        + "novas microexecuções: " + str(sum(r["samples"] for r in data["rounds"])) + "; "
        + "pendentes: " + str(len(entries) - count) + "; certificados novos: 0.", "",
        "| Endereço | Instruções reais | Operação testada | Estado |",
        "|---|---|---|---|"]
    for item in entries:
        operation = item["contract"]["op"] if item["contract"] else "não modelada"
        lines.append("| " + item["address"] + " | " +
                     "; ".join(item["assembly"]).replace("|", "/") + " | "
                     + operation + " | " + item["status"] + " |")
    lines.extend([
        "", "## Garantias e fronteiras", "",
        "Somente AL A32 imediato positivo pré-indexado, sem writeback: STRB R1, "
        "LDRB R0 ou LDR R0 de deslocamento maior, seguido por BX LR.",
        "Memória inicial sintética, referência independente em bytearray, "
        "comparação de endereço/largura/valor dos acessos, R0-R12, SP/LR, "
        "CPSR, PC, trace e conteúdo integral de memória com canário.",
        "Endereços não reconhecidos (saltos, auto-loop, fluxos desconhecidos) "
        "não são executados; nenhum destino externo é chamado.",
        "Cenários amostrados não demonstram uso real de argumentos, "
        "aliasing fora do modelo, fluxo inteiro do jogo nem equivalência global.",
        "Os 303 certificados anteriores permanecem intactos.", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("binary", "manifests", "pilot", "full-checkpoint",
                "remaining-checkpoint", "checkpoint", "report"):
        parser.add_argument("--" + key, type=Path, required=True)
    parser.add_argument("--expected-prior", type=int, default=21)
    parser.add_argument("--round-size", type=int, default=5)
    args = parser.parse_args()
    if not (1 <= args.expected_prior <= 250 and 1 <= args.round_size <= 16):
        parser.error("Invalid loop bounds")
    audited = manifest.audit(args.binary, args.manifests, args.pilot)
    full = json.loads(args.full_checkpoint.read_text(encoding="utf-8"))
    original = json.loads(args.remaining_checkpoint.read_text(encoding="utf-8"))
    fingerprint = hashlib.sha256(json.dumps(audited["rows"], sort_keys=True).encode()).hexdigest()
    if (full.get("elf_sha256") != audited["digest"]
            or len(full.get("selected", [])) != full.get("eligible")
            or full.get("new_certificates") != 0):
        raise ValueError("Invalid prior ELF loop")
    verified_entries = store.catalog(args.binary, audited["rows"], full["selected"])
    expected_original = store.build(audited["digest"], fingerprint, verified_entries,
                                    original.get("rounds", []))
    if original != expected_original:
        raise ValueError("Stale 34-entry checkpoint or ELF mismatch")
    entries = classify(args.binary, original["entries"])
    if len(entries) != args.expected_prior:
        raise ValueError("Changed or incomplete prior excluded-entry set")
    old_content = args.remaining_checkpoint.read_bytes()
    previous_hash = hashlib.sha256(old_content).hexdigest()
    chosen = [item for item in entries if item["contract"]]
    rounds = []
    if args.checkpoint.is_file():
        previous = json.loads(args.checkpoint.read_text(encoding="utf-8"))
        if previous != checkpoint(audited["digest"], fingerprint, previous_hash,
                                  entries, previous.get("rounds", [])):
            raise ValueError("Stale or tampered A01 checkpoint")
        rounds = previous["rounds"]
    batches = [chosen[i:i + args.round_size] for i in range(0, len(chosen), args.round_size)]
    if len(rounds) > len(batches):
        raise ValueError("Too many prior A01 rounds")
    for index, batch in enumerate(batches, 1):
        for item in batch:
            for seed in prior.SEEDS:
                for flags in prior.FLAGS:
                    execute(args.binary, item, seed, flags)
        record = {"iteration": index, "addresses": [item["address"] for item in batch],
                  "samples": len(batch) * len(prior.SEEDS) * len(prior.FLAGS),
                  "status": "bounded_pass"}
        if index <= len(rounds):
            if rounds[index - 1] != record:
                raise ValueError("Changed A01 checkpoint reexecution")
        else:
            rounds.append(record)
            args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
            temp = args.checkpoint.with_suffix(".json.tmp")
            temp.write_text(json.dumps(checkpoint(audited["digest"], fingerprint, previous_hash,
                                                  entries, rounds), indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
            temp.replace(args.checkpoint)
    data = checkpoint(audited["digest"], fingerprint, previous_hash, entries, rounds)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render(data), encoding="utf-8")
    counts = {name: sum(x["contract"] is not None and x["contract"]["op"] == name
                        for x in entries)
              for name in ("strb_r1", "ldrb_r0", "ldr_large_r0")}
    print("A01_INPUT_UNMODELED=" + str(len(entries)))
    print("A01_STRB_TESTED=" + str(counts["strb_r1"]))
    print("A01_LDRB_TESTED=" + str(counts["ldrb_r0"]))
    print("A01_LDR_LARGE_TESTED=" + str(counts["ldr_large_r0"]))
    print("A01_NEW_ENTRIES=" + str(len(chosen)))
    print("A01_NEW_DYNAMIC_CASES=" + str(sum(x["samples"] for x in rounds)))
    print("A01_STILL_UNMODELED=" + str(len(entries) - len(chosen)))
    print("A01_FAILED=0")
    print("A01_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
