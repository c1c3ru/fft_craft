#!/usr/bin/env python3
"""Trace A04 0x347d70 GOT-slot provenance in verified ELF and bounded Unicorn."""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_ADD, ARM_INS_LDR, ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG, ARM_REG_IP, ARM_REG_PC
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.elf.enums import ENUM_RELOC_TYPE_ARM
import semantic_evidence

SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
ENTRY, SLOT = 0x714a0, 0x347d70
NAMES = {v: k for k, v in ENUM_RELOC_TYPE_ARM.items() if isinstance(v, int)}


def decoded_slot(raw):
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    ins = list(cs.disasm(raw, ENTRY))
    if len(raw) != 12 or len(ins) != 3 or [i.id for i in ins] != [ARM_INS_ADD, ARM_INS_ADD, ARM_INS_LDR]:
        raise ValueError("Original A32 veneer changed")
    a, b, c = ins
    def add_imm(insn, reg):
        op = insn.operands
        if len(op) != 3 or op[0].type != ARM_OP_REG or op[0].reg != ARM_REG_IP or op[1].type != ARM_OP_REG or op[1].reg != reg or op[2].type != ARM_OP_IMM:
            raise ValueError("Original veneer ADD operands changed")
        return int(op[2].imm)
    d1, d2 = add_imm(a, ARM_REG_PC), add_imm(b, ARM_REG_IP)
    op = c.operands
    if len(op) != 2 or op[0].type != ARM_OP_REG or op[0].reg != ARM_REG_PC or op[1].type != ARM_OP_MEM or op[1].mem.base != ARM_REG_IP or op[1].mem.index or not c.writeback:
        raise ValueError("Original veneer LDR PC writeback changed")
    delta = int(op[1].mem.disp)
    result = (ENTRY + 8 + d1 + d2 + delta) & 0xffffffff
    if result != SLOT:
        raise ValueError("Unexpected veneer target slot")
    return {"slot": f"{result:08x}", "pc_plus_8": f"{ENTRY+8:08x}",
            "add1": d1, "add2": d2, "ldr_disp": delta,
            "instructions": [{"pc": f"{i.address:08x}", "hex": i.bytes.hex(),
                              "mnemonic": i.mnemonic, "operands": i.op_str} for i in ins]}


def elf_provenance(binary):
    with binary.open("rb") as fh:
        elf = ELFFile(fh)
        if elf.elfclass != 32 or elf["e_machine"] != "EM_ARM":
            raise ValueError("Expected 32-bit ARM original")
        owners = []
        initial = None
        for i, seg in enumerate(elf.iter_segments()):
            if seg["p_type"] != "PT_LOAD":
                continue
            base, mem, size = int(seg["p_vaddr"]), int(seg["p_memsz"]), int(seg["p_filesz"])
            if base <= SLOT < base + mem:
                backed = SLOT + 4 <= base + size
                owners.append({"index": i, "vaddr": f"{base:08x}",
                               "file_size": size, "mem_size": mem,
                               "flags": int(seg["p_flags"]), "file_backed": backed})
                if backed:
                    fh.seek(int(seg["p_offset"]) + SLOT - base)
                    word = fh.read(4)
                    if len(word) != 4:
                        raise ValueError("Short ELF slot word")
                    initial = {"raw_hex": word.hex(),
                               "le32": f"{int.from_bytes(word, 'little'):08x}"}
                else:
                    initial = {"raw_hex": None, "le32": None,
                               "note": "not file-backed; zero-fill/runtime memory"}
        if len(owners) != 1:
            raise ValueError(f"Expected 1 PT_LOAD owning 0x{SLOT:x}; found {len(owners)}")
        sections = []
        relocs, neighbors = [], []
        relsec_count = 0
        for sec in elf.iter_sections():
            start, size = int(sec["sh_addr"]), int(sec["sh_size"])
            if start <= SLOT < start + size and (int(sec["sh_flags"]) & 2):
                sections.append({"name": sec.name, "type": str(sec["sh_type"]),
                                 "start": f"{start:08x}", "slot_offset": SLOT-start})
            if not isinstance(sec, RelocationSection):
                continue
            relsec_count += 1
            symbols = elf.get_section(int(sec["sh_link"]))
            for rel in sec.iter_relocations():
                off = int(rel["r_offset"])
                if abs(off - SLOT) > 16:
                    continue
                sym_idx = int(rel["r_info_sym"])
                sym = symbols.get_symbol(sym_idx) if sym_idx and hasattr(symbols, "get_symbol") else None
                code = int(rel["r_info_type"])
                item = {"rel_section": sec.name, "offset": f"{off:08x}",
                        "type": NAMES.get(code, f"ARM_RELOC_{code}"), "type_id": code,
                        "format": "RELA" if sec.is_RELA() else "REL",
                        "addend": int(rel["r_addend"]) if sec.is_RELA() else None,
                        "symbol": None if sym is None else {
                            "name": sym.name, "shndx": str(sym["st_shndx"]),
                            "value": f"{int(sym['st_value']):08x}",
                            "kind": str(sym["st_info"]["type"]),
                            "binding": str(sym["st_info"]["bind"])}}
                (relocs if off == SLOT else neighbors).append(item)
        tags, needed = {}, []
        for seg in elf.iter_segments():
            if seg["p_type"] != "PT_DYNAMIC":
                continue
            for tag in seg.iter_tags():
                name = str(tag.entry.d_tag)
                if name == "DT_NEEDED":
                    needed.append(tag.needed)
                if name in {"DT_JMPREL","DT_PLTRELSZ","DT_PLTREL","DT_REL","DT_RELSZ",
                            "DT_RELA","DT_RELASZ","DT_PLTGOT","DT_SYMTAB"}:
                    try:
                        tags[name] = f"0x{int(tag.entry.d_val):x}"
                    except (TypeError, ValueError):
                        tags[name] = str(tag.entry)
        return {"pt_load_owners": owners, "sections": sections, "file_word": initial,
                "relocation_sections": relsec_count, "exact_relocations": relocs,
                "nearby_relocations": neighbors, "dynamic_tags": tags,
                "needed_libraries": needed, "runtime_value_verified": False}


def bounded_original(raw):
    from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                         UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
    from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_IP, UC_ARM_REG_CPSR,
                                   UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP, UC_ARM_REG_LR)
    cases = 0
    for target in (0x710000, 0x711000, 0x712000, 0x713000):
        for flags in (0, 0x20000000, 0x40000000, 0xf0000000):
            uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
            for page in {ENTRY & ~0xfff, SLOT & ~0xfff, target & ~0xfff}:
                uc.mem_map(page, 0x1000, UC_PROT_ALL)
            uc.mem_write(ENTRY, raw)
            uc.mem_write(SLOT, target.to_bytes(4, "little"))
            uc.reg_write(UC_ARM_REG_CPSR, flags | 0x10)
            registers = [(UC_ARM_REG_R0, 0x12345678), (UC_ARM_REG_R1, 0xaabbccdd),
                         (UC_ARM_REG_SP, 0x600ffc), (UC_ARM_REG_LR, 0x700000)]
            for reg, value in registers:
                uc.reg_write(reg, value)
            uc.reg_write(UC_ARM_REG_IP, 0xdeadbeef)
            pcs, reads, writes = [], [], []
            def code_hook(emu, pc, size, unused):
                pcs.append(pc)
                if pc == target:
                    emu.emu_stop()  # never execute external destination
            uc.hook_add(UC_HOOK_CODE, code_hook)
            uc.hook_add(UC_HOOK_MEM_READ, lambda emu, t, addr, n, val, u: reads.append((addr, n)))
            uc.hook_add(UC_HOOK_MEM_WRITE, lambda emu, t, addr, n, val, u: writes.append((addr, n)))
            uc.emu_start(ENTRY, target + 4, timeout=1000000, count=5)
            if pcs != [ENTRY, ENTRY+4, ENTRY+8, target]:
                raise AssertionError(f"Unexpected veneer PCs {pcs}")
            if reads != [(SLOT, 4)] or writes:
                raise AssertionError(f"Unexpected veneer read/write: {reads}, {writes}")
            if uc.reg_read(UC_ARM_REG_IP) != SLOT or uc.reg_read(UC_ARM_REG_PC) != target:
                raise AssertionError("A04 veneer indirect PC / IP writeback mismatch")
            if any(uc.reg_read(r) != v for r, v in registers):
                raise AssertionError("Veneer modified preserved registers")
            if (uc.reg_read(UC_ARM_REG_CPSR) & 0xf0000000) != flags:
                raise AssertionError("Veneer modified flags")
            cases += 1
    return cases


def audit(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ELF SHA-256 mismatch")
    raw = semantic_evidence.read_function(binary, ENTRY, 12)
    return {"schema": 1, "elf_sha256": SHA, "veneer": decoded_slot(raw),
            "provenance": elf_provenance(binary),
            "bounded_original_executions": bounded_original(raw),
            "unknown_target_executed": False, "new_certificates": 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    data = audit(args.binary)
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    if args.checkpoint.exists() and args.checkpoint.read_text(encoding="utf-8") != text:
        raise ValueError("Non-reproducible slot checkpoint")
    args.checkpoint.write_text(text, encoding="utf-8")
    lines = ["# A04 GOT-slot provenance 0x00347d70", "",
             "The original file word is not a verified Android runtime address.",
             "No external/unknown callee has been executed.", "",
             "~~~json", text.rstrip(), "~~~", "",
             "Next: identify symbol provider if exact relocation points to an import;",
             "otherwise inspect Android loaded relocation state; no complete-callee claim."]
    args.report.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print("A04_GOT_VENEER_SLOT=" + data["veneer"]["slot"])
    print("A04_GOT_INITIAL_WORD=" + json.dumps(data["provenance"]["file_word"]))
    print("A04_GOT_SECTIONS=" + json.dumps(data["provenance"]["sections"]))
    print("A04_GOT_EXACT_RELOCS=" + json.dumps(data["provenance"]["exact_relocations"]))
    print("A04_GOT_NEARBY_RELOCS=" + json.dumps(data["provenance"]["nearby_relocations"]))
    print("A04_GOT_DYNAMIC_TAGS=" + json.dumps(data["provenance"]["dynamic_tags"]))
    print("A04_GOT_NEEDED=" + json.dumps(data["provenance"]["needed_libraries"]))
    print("A04_GOT_BOUNDED_ORIGINAL_CASES=" + str(data["bounded_original_executions"]))
    print("A04_GOT_UNKNOWN_TARGET_EXECUTED=0")


if __name__ == "__main__":
    main()
