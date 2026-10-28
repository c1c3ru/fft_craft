#!/usr/bin/env python3
"""Engineering loop: classify -> microexecute original A32 -> compare -> checkpoint.
Scope is partial instruction-level evidence; NEVER creates certificates.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import semantic_manifest_audit as manifest_audit

MASK = 0xffffffff
BX_LR = 0xe12fff1e
SEEDS = (0, 1, 0x100, 0x80000000, 0xffffffff, 0x12345678, 0xdeadbeef, 0xa5a5a5a5)
FLAGS = (0, 0x20000000, 0x40000000, 0x90000000)
OPS = {0: "and", 1: "eor", 2: "sub", 4: "add", 12: "orr", 13: "mov"}
BASE = 0x500100
RETURN = 0x710100
PAGE = 0x1000


def decode(raw, addr):
    if addr % 4 or len(raw) not in (4, 8):
        return None
    word = int.from_bytes(raw[:4], "little")
    if len(raw) == 4 and (word & 0xff000000) == 0xea000000:
        delta = word & 0xffffff
        if delta & 0x800000:
            delta -= 1 << 24
        target = (addr + 8 + delta * 4) & MASK
        return ({"kind": "branch_prefix", "target": target, "opcode": raw.hex()}
                if target != addr and target % 4 == 0 else None)
    if len(raw) != 8 or int.from_bytes(raw[4:], "little") != BX_LR or word >> 28 != 14:
        return None
    if ((word >> 25) & 7) == 1 and not (word & (1 << 20)):
        op, rn, rd = (word >> 21) & 15, (word >> 16) & 15, (word >> 12) & 15
        if op in OPS and rn == 0 and rd == 0:
            imm, rot = word & 255, 2 * ((word >> 8) & 15)
            if rot:
                imm = ((imm >> rot) | (imm << (32 - rot))) & MASK
            return {"kind": "leaf_return", "op": OPS[op], "imm": imm, "opcode": raw.hex()}
    if word == 0xe1a00001:
        return {"kind": "leaf_return", "op": "mov_r1", "opcode": raw.hex()}
    if ((word >> 26) & 3) == 1 and ((word >> 25) & 1) == 0:
        fields = tuple((word >> bit) & 1 for bit in (24, 23, 22, 21, 20))
        base, dest, off = (word >> 16) & 15, (word >> 12) & 15, word & 0xfff
        if fields == (1, 1, 0, 0, 1) and base in (0, 1) and dest == 0 and off <= 64 and off % 4 == 0:
            return {"kind": "leaf_return", "op": "ldr", "base": base,
                    "offset": off, "opcode": raw.hex()}
    return None


def model(spec, r0, r1, mem):
    op = spec["op"]
    if op == "ldr":
        return mem
    if op == "mov_r1":
        return r1
    n = spec["imm"]
    return {"mov": lambda: n, "add": lambda: (r0 + n) & MASK,
            "sub": lambda: (r0 - n) & MASK, "and": lambda: r0 & n,
            "orr": lambda: r0 | n, "eor": lambda: r0 ^ n}[op]()


def select(binary, rows, limit):
    import semantic_evidence
    candidates, skipped = [], Counter()
    for addr_text, size, _, _ in rows:
        addr = int(addr_text, 16)
        if size not in (4, 8) or addr % 4:
            skipped["out_of_scope"] += 1
            continue
        spec = decode(semantic_evidence.read_function(binary, addr, size), addr)
        if spec is None:
            skipped["unmodeled_opcode_or_effect"] += 1
            continue
        if spec["kind"] == "branch_prefix":
            try:
                semantic_evidence.read_function(binary, spec["target"], 4)
            except ValueError:
                skipped["branch_target_not_executable"] += 1
                continue
        candidates.append({**spec, "address": addr_text, "size": size})
    candidates.sort(key=lambda x: (x["kind"] != "leaf_return", x["address"]))
    return candidates[:limit], dict(sorted(skipped.items())), len(candidates)


def execute(binary, spec, seed, flags):
    import semantic_evidence
    from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                         UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
    from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                                   UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR,
                                   UC_ARM_REG_PC, UC_ARM_REG_CPSR)
    addr = int(spec["address"], 16)
    raw = semantic_evidence.read_function(binary, addr, spec["size"])
    if raw.hex() != spec["opcode"] or decode(raw, addr) != {
            k: v for k, v in spec.items() if k not in ("address", "size")}:
        raise ValueError("ELF opcode changed")
    target = spec.get("target", RETURN)
    dest = (semantic_evidence.read_function(binary, target, 4)
            if spec["kind"] == "branch_prefix" else bytes(4))
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    pages = set()
    for start, length in ((addr, len(raw)), (target, 4), (BASE, 0x500)):
        pages.update(range(start & ~(PAGE - 1),
                           ((start + length - 1) & ~(PAGE - 1)) + PAGE, PAGE))
    for page in sorted(pages):
        uc.mem_map(page, PAGE, UC_PROT_ALL)
    uc.mem_write(addr, raw)
    uc.mem_write(target, dest)
    mem = (seed ^ 0x5a39c471) & MASK
    mem_addr = BASE + spec.get("offset", 0)
    canary = bytes.fromhex("197dda3c89fe2011")
    uc.mem_write(mem_addr, mem.to_bytes(4, "little"))
    uc.mem_write(BASE + 0x400, canary)
    r0, r1 = seed, 0x22334455
    if spec.get("op") == "ldr":
        if spec["base"] == 0:
            r0 = BASE
        else:
            r1 = BASE
    regs = {UC_ARM_REG_R0: r0, UC_ARM_REG_R1: r1,
            UC_ARM_REG_R2: 0x13579bdf, UC_ARM_REG_R3: 0x2468ace0,
            UC_ARM_REG_SP: 0x700ffc, UC_ARM_REG_LR: RETURN}
    for reg, value in regs.items():
        uc.reg_write(reg, value)
    uc.reg_write(UC_ARM_REG_CPSR, flags | 0x10)
    trace, reads, writes = [], [], []

    def code_hook(emu, pc, size, user_data):
        trace.append(pc)
        if pc == target:
            emu.emu_stop()

    def read_hook(emu, access, pos, size, value, user_data):
        reads.append((pos, size))

    def write_hook(emu, access, pos, size, value, user_data):
        writes.append((pos, size))

    uc.hook_add(UC_HOOK_CODE, code_hook)
    uc.hook_add(UC_HOOK_MEM_READ, read_hook)
    uc.hook_add(UC_HOOK_MEM_WRITE, write_hook)
    uc.emu_start(addr, MASK, timeout=1000000, count=4)
    steps = 1 if spec["kind"] == "branch_prefix" else 2
    if trace != [addr + i * 4 for i in range(steps)] + [target]:
        raise AssertionError("unexpected A32 trace")
    if uc.reg_read(UC_ARM_REG_PC) != target:
        raise AssertionError("unexpected PC")
    wanted_reads = [(mem_addr, 4)] if spec.get("op") == "ldr" else []
    if reads != wanted_reads or writes:
        raise AssertionError("unexpected memory effect")
    if (bytes(uc.mem_read(mem_addr, 4)) != mem.to_bytes(4, "little") or
            bytes(uc.mem_read(BASE + 0x400, 8)) != canary):
        raise AssertionError("memory canary modified")
    expected = model(spec, r0, r1, mem) if spec["kind"] == "leaf_return" else r0
    for reg, old in regs.items():
        if uc.reg_read(reg) != (expected if reg == UC_ARM_REG_R0 else old):
            raise AssertionError("register differs from reference")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xf000003f) != ((flags | 0x10) & 0xf000003f):
        raise AssertionError("CPSR NZCV/mode changed")


def state(digest, inventory, selected, skipped, eligible, rounds):
    return {"schema": 1, "elf_sha256": digest, "inventory_sha256": inventory,
            "selected": selected, "skipped": skipped, "eligible": eligible,
            "rounds": rounds, "new_certificates": 0}


def render(record):
    lines = ["# Engenharia de loop — ELF original, 250 tarefas", "",
             "ELF SHA-256: " + record["elf_sha256"], "",
             "Ciclo: classificar -> selecionar -> executar ARM em Unicorn -> comparar "
             "modelo independente -> checkpoint.", "",
             f"Elegíveis: {record['eligible']}; selecionados: {len(record['selected'])}; "
             f"rodadas: {len(record['rounds'])}; "
             f"microexecuções diferenciais aprovadas: {sum(x['samples'] for x in record['rounds'])}.",
             "Novos certificados: 0.", "",
             "| Endereço | Classe | Operação / destino | Cenários |",
             "|---|---|---|---:|"]
    for group in record["rounds"]:
        for item in group["items"]:
            detail = item.get("op", "B 0x%08x" % item.get("target", 0))
            lines.append(f"| {item['address']} | {item['kind']} | {detail} | {item['samples']} |")
    lines += ["", "## Excluídos conservadoramente", ""]
    lines += [f"- {key}: {n}" for key, n in record["skipped"].items()]
    lines += ["", "## Limites", "",
              "Somente 1 salto A32 até ANTES do destino, ou até 2 instruções de retorno local.",
              "Estados de registradores/memória são sintéticos. Nenhum callee, escrita em memória,",
              "desvio condicional, função complexa ou comportamento integral foi certificado.",
              "Próximo ciclo: contratos para acessos à memória e fronteiras de chamadas.",
              "Os 303 certificados registrados não são alterados.", ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("binary", "manifests", "pilot", "checkpoint", "report"):
        p.add_argument("--" + name, type=Path, required=True)
    p.add_argument("--max-candidates", type=int, default=24)
    p.add_argument("--round-size", type=int, default=8)
    args = p.parse_args()
    if not (1 <= args.max_candidates <= 250 and 1 <= args.round_size <= 32):
        p.error("invalid iteration bounds")
    checked = manifest_audit.audit(args.binary, args.manifests, args.pilot)
    selected, skipped, eligible = select(args.binary, checked["rows"], args.max_candidates)
    inventory = hashlib.sha256(json.dumps(checked["rows"], sort_keys=True).encode()).hexdigest()
    rounds = []
    if args.checkpoint.is_file():
        old = json.loads(args.checkpoint.read_text())
        if old != state(checked["digest"], inventory, selected, skipped, eligible,
                        old.get("rounds", [])):
            raise ValueError("stale or tampered checkpoint")
        rounds = old["rounds"]
    batches = [selected[i:i + args.round_size] for i in range(0, len(selected), args.round_size)]
    if len(rounds) > len(batches):
        raise ValueError("surplus checkpoint iteration")
    for number, batch in enumerate(batches, 1):
        items = []
        for item in batch:
            for seed in SEEDS:
                for flags in FLAGS:
                    execute(args.binary, item, seed, flags)
            items.append({**item, "samples": len(SEEDS) * len(FLAGS)})
        record = {"iteration": number, "items": items,
                  "samples": len(items) * len(SEEDS) * len(FLAGS), "status": "bounded_pass"}
        if number <= len(rounds):
            if rounds[number - 1] != record:
                raise ValueError("checkpoint result changed")
        else:
            rounds.append(record)
            payload = state(checked["digest"], inventory, selected, skipped, eligible, rounds)
            args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
            tmp = args.checkpoint.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            tmp.replace(args.checkpoint)
    result = state(checked["digest"], inventory, selected, skipped, eligible, rounds)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render(result))
    print(f"LOOP_ELIGIBLE={eligible}")
    print(f"LOOP_SELECTED={len(selected)}")
    print(f"LOOP_ROUNDS={len(rounds)}")
    print(f"LOOP_DIFFERENTIAL_PASSED={sum(x['samples'] for x in rounds)}")
    print("LOOP_FAILED=0")
    print("LOOP_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
