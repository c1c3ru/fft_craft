#!/usr/bin/env python3
"""Robust ARM jump-table resolver + full structural-pass summary in one tool.

Usage: jtable.py <so_path> <func_start_hex> <+len_or_end_hex>

Does a recursive-descent disasm from func_start, auto-detects every
`add{cond} pc, pc, rX, lsl #2` jump dispatch, finds the EXACT guarding
`cmp rX, #N` by scanning backward on the real instruction stream for
the nearest instruction that writes rX (must be that cmp - if it's
anything else, the table is reported unresolved rather than guessed),
decodes N+1 table entries as `b #addr`, reseeds the descent with them,
and repeats until no new code is discovered. Prints a summary: total
coverage, resolved tables with their full target lists, and the bl
catalog (resolved against .dynsym + demangled).
"""
import sys, subprocess
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


def load_dynsyms(path):
    out = subprocess.run(['readelf', '-W', '--dyn-syms', path], capture_output=True, text=True).stdout
    addr2name = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 8 and parts[3] == 'FUNC':
            try:
                addr = int(parts[1], 16)
            except ValueError:
                continue
            addr2name[addr] = parts[-1]
    return addr2name


def demangle(names):
    if not names:
        return []
    out = subprocess.run(['c++filt'], input="\n".join(names), capture_output=True, text=True).stdout
    return out.splitlines()


def reg_written(insn):
    """Registers this instruction writes, best-effort via capstone regs_access."""
    try:
        regs_read, regs_write = insn.regs_access()
        return {insn.reg_name(r) for r in regs_write}
    except Exception:
        return set()


def descend(md, data, start, end, seeds):
    insns = {}
    order = []  # addresses in the order first decoded, per block, for backward scan
    worklist = list(seeds)
    seen = set()
    jt_candidates = []  # addresses of add{cond} pc,pc,rX,lsl#2
    while worklist:
        addr = worklist.pop()
        if addr in seen or addr < start or addr >= end:
            continue
        seen.add(addr)
        off = addr - start
        block_order = []
        for insn in md.disasm(data[off:], addr):
            if insn.address in insns:
                break
            insns[insn.address] = insn
            block_order.append(insn.address)
            m, ops = insn.mnemonic, insn.op_str
            if m == 'bx' or (m.startswith('pop') and 'pc' in ops):
                break
            first_op = ops.split(',')[0].strip() if ops else ''
            if m.startswith('add') and first_op == 'pc' and ', pc,' in ops:
                jt_candidates.append(insn.address)
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
                    # Register-target branch (bx/blx reg). Only an
                    # UNCONDITIONAL one truly ends the block - a conditional
                    # variant (bxle, bxeq, ...) falls through to the next
                    # instruction when the condition is false. Plain 'bx' is
                    # already caught above; anything reaching here ending in
                    # a 2-letter ARM condition code is the conditional case.
                    cond_suffixes = ('eq', 'ne', 'cs', 'hs', 'cc', 'lo', 'mi',
                                      'pl', 'vs', 'vc', 'hi', 'ls', 'ge', 'lt',
                                      'gt', 'le')
                    if not (len(m) > 2 and m.endswith(cond_suffixes)):
                        break
        order.append(block_order)
    return insns, jt_candidates


def resolve_jump_table(md, data, start, insns, jt_addr):
    """Find the guard cmp by walking backward through the straight-line
    instruction stream immediately preceding jt_addr (re-disassembled
    fresh so we have true linear order right before the jump, not the
    worklist's visit order)."""
    jt_insn = insns[jt_addr]
    parts = jt_insn.op_str.split(',')
    if len(parts) < 3:
        return None, None, None
    reg = parts[2].strip().split()[0]

    # Walk backward linearly in the raw byte stream (4-byte-aligned ARM)
    for back in range(1, 40):
        cand_addr = jt_addr - back * 4
        if cand_addr < start:
            break
        off = cand_addr - start
        word = data[off:off + 4]
        decoded = list(md.disasm(word, cand_addr))
        if not decoded:
            continue
        cand = decoded[0]
        if cand.mnemonic == 'cmp' and cand.op_str.split(',')[0].strip() == reg:
            try:
                n = int(cand.op_str.split('#')[1], 0)
            except (IndexError, ValueError):
                return None, None, None
            table_start = jt_addr + 8
            entries = []
            toff = table_start - start
            for i in range(n + 1):
                w = data[toff + i * 4: toff + i * 4 + 4]
                dec = list(md.disasm(w, table_start + i * 4))
                if dec and dec[0].mnemonic == 'b' and dec[0].op_str.startswith('#'):
                    entries.append(int(dec[0].op_str[1:], 16))
                else:
                    return None, None, None  # not a clean b-table, bail honestly
            return n, entries, cand_addr
        if reg in reg_written(cand):
            # register was redefined before we found the cmp -> not safely resolvable this way
            return None, None, None
    return None, None, None


def main():
    path, start_s, end_s = sys.argv[1], sys.argv[2], sys.argv[3]
    start = int(start_s, 16)
    end = start + int(end_s[1:], 0) if end_s.startswith('+') else int(end_s, 16)
    secs = load_sections(path)
    off, _ = va_to_off(secs, start)
    length = end - start
    with open(path, 'rb') as f:
        f.seek(off)
        data = f.read(length)

    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    addr2name = load_dynsyms(path)

    all_insns = {}
    all_tables = []
    resolved_jt_addrs = set()
    unresolved_jt_addrs = set()
    seeds = [start]

    for _ in range(30):
        insns, jt_candidates = descend(md, data, start, end, seeds)
        new = False
        for a, i in insns.items():
            if a not in all_insns:
                all_insns[a] = i
                new = True
        next_seeds = []
        for jt in jt_candidates:
            if jt in resolved_jt_addrs or jt in unresolved_jt_addrs:
                continue
            n, entries, guard_addr = resolve_jump_table(md, data, start, all_insns, jt)
            if n is None:
                unresolved_jt_addrs.add(jt)
                print(f"[WARN] jump table at 0x{jt:x} could not be safely resolved (guard cmp not found or register clobbered)")
                continue
            resolved_jt_addrs.add(jt)
            all_tables.append((jt, guard_addr, n, entries))
            next_seeds.extend(entries)
        if not next_seeds and not new:
            break
        seeds = next_seeds if next_seeds else [s for s in seeds]
        if not next_seeds:
            break

    n_insns = len(all_insns)
    expected = length // 4
    print(f"=== jtable.py: 0x{start:x}..0x{end:x} ({length} bytes) ===")
    print(f"coverage: {n_insns} of ~{expected} instruction slots ({100*n_insns/max(expected,1):.0f}%)\n")

    print(f"-- jump tables resolved: {len(all_tables)} --")
    for jt, guard_addr, n, entries in all_tables:
        distinct = sorted(set(entries))
        print(f"  guard cmp @0x{guard_addr:x}, dispatch @0x{jt:x}: {n+1} cases, {len(distinct)} distinct handlers")
        print(f"    targets: {[hex(e) for e in entries]}")

    bl = {}
    branches = []
    for a, insn in all_insns.items():
        if insn.mnemonic == 'bl' and insn.op_str.startswith('#'):
            try:
                t = int(insn.op_str[1:], 16)
            except ValueError:
                continue
            bl.setdefault(t, []).append(a)
        elif (insn.mnemonic.startswith('b') and not insn.mnemonic.startswith('bic')
              and not insn.mnemonic.startswith('bl') and not insn.mnemonic.startswith('bfc')
              and not insn.mnemonic.startswith('bkpt') and insn.op_str.startswith('#')):
            try:
                t = int(insn.op_str[1:], 16)
                branches.append((a, insn.mnemonic, t))
            except ValueError:
                pass

    print(f"\n-- bl targets: {len(bl)} distinct --")
    tl = sorted(bl.keys())
    names = [addr2name.get(t) or f"sub_{t:x}" for t in tl]
    dem = demangle(names)
    for t, d in zip(tl, dem):
        tag = "LOCAL(no-dynsym)" if addr2name.get(t) is None else ""
        print(f"  0x{t:x} x{len(bl[t]):<3d} {d} {tag}")

    back = sum(1 for a, m, t in branches if t < a)
    print(f"\n-- branches: {len(branches)} total, {back} backward (loop candidates) --")


if __name__ == '__main__':
    main()
