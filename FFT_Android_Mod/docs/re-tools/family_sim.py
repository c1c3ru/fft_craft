#!/usr/bin/env python3
"""Family-similarity confirmation: compare a candidate function's resolved
bl-catalog (by target address, via jtable.py's descent) against a reference
function already confirmed read_structural. If the overlap is >=90%
(Jaccard over bl target addresses), the candidate is "confirmed by
similarity" without a full structural write-up.

Usage: family_sim.py <so_path> <ref_start_hex> <ref_end_or_+len> \
           <cand_name:cand_start_hex:cand_end_or_+len> [more candidates...]
"""
import sys
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM


def load_sections(path):
    with open(path, 'rb') as f:
        elf = ELFFile(f)
        return [(s['sh_addr'], s['sh_size'], s['sh_offset'], s.name, s['sh_type'])
                for s in elf.iter_sections() if s['sh_addr'] != 0]


def va_to_off(secs, va):
    for addr, size, off, name, shtype in secs:
        if addr <= va < addr + size:
            return (None if shtype == 'SHT_NOBITS' else off + (va - addr)), name
    return None, None


def descend(md, data, start, end):
    """Same recursive-descent as jtable.py/struct_pass.py, minus jump-table
    resolution (we only need the bl catalog + coverage %, not full tables,
    for a similarity check)."""
    insns = {}
    worklist = [start]
    seen = set()
    unresolved_jt = 0
    while worklist:
        addr = worklist.pop()
        if addr in seen or addr < start or addr >= end:
            continue
        seen.add(addr)
        off = addr - start
        for insn in md.disasm(data[off:], addr):
            if insn.address in insns:
                break
            insns[insn.address] = insn
            m, ops = insn.mnemonic, insn.op_str
            if m == 'bx' or (m.startswith('pop') and 'pc' in ops):
                break
            first_op = ops.split(',')[0].strip() if ops else ''
            if m.startswith('add') and first_op == 'pc' and ', pc,' in ops:
                unresolved_jt += 1
                break
            if m.startswith('b') and not m.startswith('bic') and not m.startswith('bfc') and not m.startswith('bkpt'):
                if ops.startswith('#'):
                    try:
                        worklist.append(int(ops.split('#')[1], 16))
                    except ValueError:
                        pass
                    if m == 'b':
                        break
                else:
                    break
    return insns, unresolved_jt


def bl_catalog(insns):
    bl = set()
    for a, insn in insns.items():
        if insn.mnemonic == 'bl' and insn.op_str.startswith('#'):
            try:
                bl.add(int(insn.op_str[1:], 16))
            except ValueError:
                pass
    return bl


def analyze(md, data_full, base, md_start, start, end):
    off = start - base
    length = end - start
    data = data_full[off:off + length]
    insns, unresolved_jt = descend(md, data, start, end)
    n = len(insns)
    expected = max(length // 4, 1)
    return insns, bl_catalog(insns), n, expected, unresolved_jt


def main():
    path = sys.argv[1]
    ref_start = int(sys.argv[2], 16)
    ref_end = ref_start + int(sys.argv[3][1:], 0) if sys.argv[3].startswith('+') else int(sys.argv[3], 16)

    secs = load_sections(path)
    # load a single contiguous .text-ish region covering everything requested
    ref_off, _ = va_to_off(secs, ref_start)

    candidates = []
    for arg in sys.argv[4:]:
        name, s, e = arg.split(':')
        s = int(s, 16)
        e = s + int(e[1:], 0) if e.startswith('+') else int(e, 16)
        candidates.append((name, s, e))

    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

    # read each region independently (simpler, avoids cross-region offset math)
    def read_region(start, end):
        off, _ = va_to_off(secs, start)
        length = end - start
        with open(path, 'rb') as f:
            f.seek(off)
            return f.read(length)

    ref_data = read_region(ref_start, ref_end)
    ref_insns, ref_jt_unresolved = descend(md, ref_data, ref_start, ref_end)
    ref_bl = bl_catalog(ref_insns)
    ref_n = len(ref_insns)
    ref_expected = max((ref_end - ref_start) // 4, 1)
    print(f"=== reference 0x{ref_start:x}..0x{ref_end:x}: {ref_n}/{ref_expected} insns "
          f"({100*ref_n/ref_expected:.0f}%), {len(ref_bl)} distinct bl targets, "
          f"{ref_jt_unresolved} unresolved jump-table dispatch(es) ===\n")

    for name, s, e in candidates:
        data = read_region(s, e)
        insns, jt_unresolved = descend(md, data, s, e)
        bl = bl_catalog(insns)
        n = len(insns)
        expected = max((e - s) // 4, 1)
        inter = ref_bl & bl
        union = ref_bl | bl
        jacc = len(inter) / len(union) if union else 0.0
        extra = bl - ref_bl
        missing = ref_bl - bl
        verdict = "CONFIRMED-BY-SIMILARITY" if jacc >= 0.90 and jt_unresolved == 0 else "NEEDS-REVIEW"
        print(f"-- {name} 0x{s:x}..0x{e:x} ({e-s} B): {n}/{expected} insns "
              f"({100*n/expected:.0f}%), {len(bl)} bl targets, jaccard={jacc:.2f}, "
              f"jt_unresolved={jt_unresolved} -> {verdict}")
        if extra:
            print(f"     extra bl targets not in reference: {[hex(x) for x in sorted(extra)]}")
        if missing:
            print(f"     reference bl targets missing here: {[hex(x) for x in sorted(missing)]}")


if __name__ == '__main__':
    main()
