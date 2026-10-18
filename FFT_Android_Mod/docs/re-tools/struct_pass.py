#!/usr/bin/env python3
"""Structural pass for a large function: disassemble [start,end) in ARM mode,
then summarize instead of dumping every instruction — bl targets (resolved
against .dynsym), branch targets classified as forward/backward (loop
candidates), and computed-jump-table patterns.

Usage: struct_pass.py <so_path> <start_hex> <end_hex_or_+len>
"""
import sys, subprocess, re
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
    joined = "\n".join(names)
    out = subprocess.run(['c++filt'], input=joined, capture_output=True, text=True).stdout
    return out.splitlines()


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
    md.detail = True

    addr2name = load_dynsyms(path)

    # Recursive-descent walk (like disasm_cfg.py): follow branch targets,
    # stop at bx/pop{pc} block-enders, so embedded literal pools / data
    # islands between basic blocks don't derail a naive linear decode.
    insns_by_addr = {}
    worklist = [start]
    seen_starts = set()
    unresolved_computed = []
    while worklist:
        addr = worklist.pop()
        if addr in seen_starts or addr < start or addr >= end:
            continue
        seen_starts.add(addr)
        off = addr - start
        for insn in md.disasm(data[off:], addr):
            if insn.address in insns_by_addr:
                break
            insns_by_addr[insn.address] = insn
            mnem, ops = insn.mnemonic, insn.op_str
            if mnem == 'bx' or (mnem.startswith('pop') and 'pc' in ops):
                break
            if mnem.startswith('b') and not mnem.startswith('bic') and not mnem.startswith('bfc') and not mnem.startswith('bkpt'):
                if ops.startswith('#'):
                    try:
                        target = int(ops.split('#')[1], 16)
                        worklist.append(target)
                    except ValueError:
                        pass
                    if mnem == 'b':
                        break
                else:
                    unresolved_computed.append((insn.address, mnem, ops))
                    break
            if mnem in ('ldr',) and ops.strip().startswith('pc,'):
                unresolved_computed.append((insn.address, mnem, ops))
                break

    insns = [insns_by_addr[a] for a in sorted(insns_by_addr)]
    n_insns = len(insns)
    expected = length // 4
    print(f"[recursive-descent reached {n_insns} of ~{expected} possible instruction slots; "
          f"gaps are literal pools/data or unresolved computed jumps]")
    if unresolved_computed:
        print(f"[{len(unresolved_computed)} block(s) ended on an unresolved computed branch/load-to-pc — needs manual jump-table extraction]")
        for a, m, o in unresolved_computed:
            print(f"    0x{a:x}: {m} {o}")
    print()
    bl_targets = {}
    branches = []
    computed_jumps = []
    cmp_before_branch = {}

    for i, insn in enumerate(insns):
        m, o, a = insn.mnemonic, insn.op_str, insn.address
        if m == 'bl' and o.startswith('#'):
            try:
                tgt = int(o[1:], 16)
            except ValueError:
                continue
            bl_targets.setdefault(tgt, []).append(a)
        elif (m.startswith('b') and not m.startswith('bic') and not m.startswith('bfc')
              and not m.startswith('bkpt') and o.startswith('#')):
            try:
                tgt = int(o[1:], 16)
            except ValueError:
                continue
            kind = 'back' if tgt < a else 'forward'
            branches.append((a, m, tgt, kind))
        elif m in ('add', 'ldr') and 'pc' in o and ('pc, pc' in f"{m} {o}" or o.strip().startswith('pc, [pc')):
            computed_jumps.append((a, m, o))

    print(f"=== Structural pass: 0x{start:x}..0x{end:x} ({length} bytes, {n_insns} instructions) ===\n")

    print(f"-- bl targets: {len(bl_targets)} distinct --")
    mangled_list = []
    tgt_list = sorted(bl_targets.keys())
    for tgt in tgt_list:
        name = addr2name.get(tgt, None)
        mangled_list.append(name if name else f"sub_{tgt:x}")
    demangled_list = demangle(mangled_list)
    for tgt, dname, callsites in zip(tgt_list, demangled_list, [bl_targets[t] for t in tgt_list]):
        in_range = start <= tgt < end
        tag = "LOCAL(no-dynsym)" if (addr2name.get(tgt) is None) else ""
        print(f"  0x{tgt:x} {'[internal]' if in_range else '':10s} x{len(callsites):<3d} {dname} {tag}")

    print(f"\n-- branches: {len(branches)} total, {sum(1 for b in branches if b[3]=='back')} backward (loop candidates) --")
    back = [b for b in branches if b[3] == 'back']
    for a, m, tgt, kind in back:
        print(f"  0x{a:x}: {m} -> 0x{tgt:x}  (back {a-tgt} bytes)")

    print(f"\n-- branches leaving the function range entirely (tail calls / tables?) --")
    outside = [b for b in branches if not (start <= b[2] < end)]
    for a, m, tgt, kind in outside:
        print(f"  0x{a:x}: {m} -> 0x{tgt:x} (outside range)")

    if computed_jumps:
        print(f"\n-- possible computed-jump-table instructions: {len(computed_jumps)} --")
        for a, m, o in computed_jumps:
            print(f"  0x{a:x}: {m} {o}")

    print(f"\n-- forward branch target histogram (merge points, candidate if/switch joins) --")
    from collections import Counter
    fwd_targets = Counter(b[2] for b in branches if b[3] == 'forward')
    for tgt, cnt in sorted(fwd_targets.items()):
        if cnt >= 2:
            print(f"  0x{tgt:x}: {cnt} branches converge here")


if __name__ == '__main__':
    main()
