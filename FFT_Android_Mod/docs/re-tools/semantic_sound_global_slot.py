#!/usr/bin/env python3
"""Original-ELF data-slot provenance and isolated ARM LDR microexecution.

0x2b2b90: LDR R0,[PC,R3]. Prior original ARM prologue established
R3=*(0x2b2ce8)=0x000935c4. Therefore effective address is 0x34615c.
This tool examines ELF segment/relocation metadata and executes this ONE
original instruction using clearly SYNTHETIC, controlled slot contents.
It does NOT claim the original runtime global value or full audio behavior.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_R0,
                               UC_ARM_REG_R3, UC_ARM_REG_R5, UC_ARM_REG_R6,
                               UC_ARM_REG_SP)

import semantic_evidence
import semantic_sound_common_prologue as prologue
import semantic_sound_three_entry_exec as seed

ENTRY = 0x2B2B90
NEXT = ENTRY + 4
ORIGINAL_CODE = bytes.fromhex("03009fe72810a0e3")
SLOT_ADDR = 0x34615C
EXPECTED_LITERAL = 0x000935C4
VALUES = (0, 1, 0x12345678, 0xFFFFFFFF)
CANARY_ADDR = 0x500000
CANARY = bytes.fromhex("d01dce22beac487a2911fe09dd7915ee")


def provenance(binary):
    binary = Path(binary)
    if hashlib.sha256(binary.read_bytes()).hexdigest() != seed.ELF_SHA256:
        raise ValueError("Wrong original sound ELF")
    _, literal = prologue.original(binary)
    literal_value = int.from_bytes(literal, "little")
    if literal_value != EXPECTED_LITERAL:
        raise ValueError("Changed PC-relative sound literal")
    address = (ENTRY + 8 + literal_value) & 0xFFFFFFFF
    if address != SLOT_ADDR:
        raise ValueError("Unexpected global sound slot address")
    code = semantic_evidence.read_function(binary, ENTRY, 8)
    if code != ORIGINAL_CODE:
        raise ValueError("Changed original ARM LDR opcode")
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoded = [(x.mnemonic, x.op_str) for x in decoder.disasm(code, ENTRY)]
    if decoded != [("ldr", "r0, [pc, r3]"), ("mov", "r1, #0x28")]:
        raise ValueError("Original sound LDR instruction signature drift")
    return code, address, literal_value


def elf_slot_metadata(binary, address):
    """Read only file-backed bytes and relocation metadata; no dynamic linking."""
    with Path(binary).open("rb") as stream:
        elf = ELFFile(stream)
        matches = []
        for n, seg in enumerate(elf.iter_segments()):
            if (seg["p_type"] == "PT_LOAD" and
                    seg["p_vaddr"] <= address and
                    address + 4 <= seg["p_vaddr"] + seg["p_memsz"]):
                in_file = (address + 4 <= seg["p_vaddr"] + seg["p_filesz"])
                value = None
                if in_file:
                    stream.seek(seg["p_offset"] + address - seg["p_vaddr"])
                    raw = stream.read(4)
                    if len(raw) != 4:
                        raise ValueError("Short ELF file-backed slot")
                    value = int.from_bytes(raw, "little")
                matches.append({"index": n, "flags": int(seg["p_flags"]),
                                "file_backed": in_file, "file_value": value})
        if len(matches) != 1:
            raise ValueError("Indirect slot has no unique PT_LOAD backing")
        relocations = []
        for sec in elf.iter_sections():
            if not isinstance(sec, RelocationSection):
                continue
            for relocation in sec.iter_relocations():
                if int(relocation["r_offset"]) != address:
                    continue
                symbol_name = ""
                if relocation["r_info_sym"]:
                    symbols = elf.get_section(sec["sh_link"])
                    if symbols is not None:
                        symbol_name = symbols.get_symbol(
                            relocation["r_info_sym"]).name
                relocations.append({
                    "section": sec.name, "type": int(relocation["r_info_type"]),
                    "symbol": symbol_name,
                    "addend": int(relocation["r_addend"])
                    if sec.is_RELA() else None,
                })
        return matches[0], relocations


def initial_registers(arg, literal):
    before = seed.seeded_registers(arg)
    before[UC_ARM_REG_R0] = 0
    before[UC_ARM_REG_R3] = literal
    before[UC_ARM_REG_R5] = arg
    before[UC_ARM_REG_R6] = 0
    before[UC_ARM_REG_SP] = prologue.STACK_TOP - 64
    # R1 is the argument passed by the predecessor.
    from unicorn.arm_const import UC_ARM_REG_R1
    before[UC_ARM_REG_R1] = arg
    return before


def execute(code, address, literal, arg, flags, slot_value):
    if (code != ORIGINAL_CODE or address != SLOT_ADDR or
            literal != EXPECTED_LITERAL or arg not in seed.R0_STATES or
            flags not in range(16) or slot_value not in VALUES):
        raise ValueError("Unsupported original code/address/sample")
    m = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in {ENTRY & ~0xFFF, address & ~0xFFF, CANARY_ADDR}:
        m.mem_map(page, 0x1000, UC_PROT_ALL)
    m.mem_write(ENTRY, code)  # original instructions, next is not executed
    m.mem_write(address, slot_value.to_bytes(4, "little"))  # SYNTHETIC SLOT!
    m.mem_write(CANARY_ADDR, CANARY)
    before = initial_registers(arg, literal)
    cpsr = (flags << 28) | 0x10
    m.reg_write(UC_ARM_REG_CPSR, cpsr)
    for reg, value in before.items():
        m.reg_write(reg, value)
    trace, reads, writes = [], [], []

    def hook_code(uc, addr, size, unused):
        trace.append(addr)
        if addr == NEXT:
            uc.emu_stop()

    m.hook_add(UC_HOOK_CODE, hook_code)
    m.hook_add(UC_HOOK_MEM_READ,
               lambda uc, access, addr, size, value, unused:
               reads.append((addr, size)))
    m.hook_add(UC_HOOK_MEM_WRITE,
               lambda uc, access, addr, size, value, unused:
               writes.append((addr, size, value)))
    m.emu_start(ENTRY, NEXT + 4, timeout=1_000_000, count=2)
    if trace != [ENTRY, NEXT] or m.reg_read(UC_ARM_REG_PC) != NEXT:
        raise AssertionError("Wrong ARM global load branch/stop boundary")
    if reads != [(address, 4)] or writes:
        raise AssertionError("Wrong ARM global load memory effects")
    if m.reg_read(UC_ARM_REG_R0) != slot_value:
        raise AssertionError("Original ARM indirect LDR did not load slot")
    for reg, value in before.items():
        if reg != UC_ARM_REG_R0 and m.reg_read(reg) != value:
            raise AssertionError("Indirect LDR unexpectedly changed register")
    if ((m.reg_read(UC_ARM_REG_CPSR) & 0xF000003F) !=
            (cpsr & 0xF000003F)):
        raise AssertionError("ARM indirect LDR changed NZCV or mode")
    if bytes(m.mem_read(CANARY_ADDR, len(CANARY))) != CANARY:
        raise AssertionError("Indirect LDR wrote unrelated memory")
    return {"pc": NEXT, "r0": slot_value, "reads": tuple(reads),
            "writes": tuple(writes), "actual_runtime_value_proven": False,
            "new_certificate": False}


def render(binary):
    code, slot, literal = provenance(binary)
    backing, relocations = elf_slot_metadata(binary, slot)
    count = 0
    for arg in seed.R0_STATES:
        for flags in range(16):
            for fixture in VALUES:
                execute(code, slot, literal, arg, flags, fixture)
                count += 1
    file_word = (f"0x{backing['file_value']:08x}"
                 if backing["file_backed"] else "sem bytes no arquivo (BSS)")
    lines = [
        "# sound_request: proveniência da leitura global indireta ARM 0x2b2b90",
        "", f"ELF SHA-256: {seed.ELF_SHA256}", "",
        "## Proveniência do endereço", "",
        "- Opcode original: LDR R0,[PC,R3] em 0x2b2b90 (03009fe7).",
        "- R3 vem da leitura original em 0x2b2ce8: 0x000935c4.",
        f"- PC A32 efetivo: 0x{ENTRY+8:x}; endereço PC+R3 = 0x{slot:x}.",
        f"- Segmento PT_LOAD #{backing['index']}, flags={backing['flags']}, "
        f"file-backed={backing['file_backed']}.",
        f"- Palavra armazenada no arquivo ELF neste slot: {file_word}. "
        "Isso NAO garante o valor depois de relocação/runtime.", "",
        "## Registros de relocação exatamente no slot", "",
    ]
    if relocations:
        for r in relocations:
            lines.append(f"- {r['section']}: tipo {r['type']}, "
                         f"símbolo {r['symbol'] or '(não nomeado)'}, "
                         f"addend {r['addend']}.")
    else:
        lines.append("- Nenhuma relocação exatamente no slot encontrada nas "
                     "seções REL/RELA examinadas; não prova valor global fixo.")
    lines.extend([
        "", "## Microexecução controlada do opcode original", "",
        f"- {count} execuções Unicorn (8 entradas x 16 NZCV x 4 valores "
        "SINTÉTICOS para a palavra do slot).",
        f"- Memória observada: uma leitura de 4 bytes em 0x{slot:x}, "
        "nenhuma gravação de dados.",
        f"- R0 depois da instrução recebe a palavra sintética do slot; "
        f"PC avança para 0x{NEXT:x}; os outros registros e NZCV preservados.",
        "- Instrução seguinte em 0x2b2b94 NÃO executada.",
        "- Nenhum valor de memória do processo original foi medido em runtime.",
        "- Não há reconstrução completa da chamada, retorno ou efeitos de áudio.",
        "- Novos certificados semânticos: 0. Preservados os 303 BX LR anteriores.", "",
        "## Próximo passo", "",
        "- Resolver o estado global/relocação que popula o slot em runtime, "
        "com entradas e memória controladas, antes de executar chamadas "
        "ou substituir o ponteiro por um valor presumido.",
        "",
    ])
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_evidence.ROOT /
                   "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--output", type=Path, default=semantic_evidence.ROOT /
                   "docs/re-results/SEMANTIC_SOUND_GLOBAL_SLOT.md")
    args = p.parse_args()
    result = render(args.binary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    print("SOUND_GLOBAL_SLOT_EFFECTIVE_ADDRESS=0x34615c")
    print("SOUND_GLOBAL_SLOT_CONTROLLED_LDR_CASES=512")
    print("SOUND_GLOBAL_SLOT_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
