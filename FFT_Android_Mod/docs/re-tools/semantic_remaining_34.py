#!/usr/bin/env python3
"""Conservative original-ELF remaining-34 ARM store loop. Never certify semantics."""
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

import semantic_evidence
import semantic_manifest_audit as audit_tool
import semantic_loop_250 as prior

MASK = 0xffffffff
BASE = 0x500100
RET = 0x710100
CANARY = bytes.fromhex('197dda3c89fe2011')


def decode_store(raw, address):
    if address % 4 or len(raw) != 8:
        return None
    word = int.from_bytes(raw[:4], 'little')
    if int.from_bytes(raw[4:], 'little') != prior.BX_LR:
        return None
    if word >> 28 != 0xe or ((word >> 26) & 3) != 1 or (word >> 25) & 1:
        return None
    if tuple((word >> b) & 1 for b in (24,23,22,21,20)) != (1,1,0,0,0):
        return None
    base, source, disp = (word >> 16) & 15, (word >> 12) & 15, word & 0xfff
    if base > 3 or source > 3 or disp > 256 or disp % 4:
        return None
    return {'kind':'str_word_return', 'base':base, 'source':source, 'offset':disp, 'raw_hex':raw.hex()}


def catalog(binary, rows, previous):
    processed = {x['address'] for x in previous}
    if len(processed) != len(previous):
        raise ValueError('duplicate prior addresses')
    if not processed.issubset({r[0] for r in rows}):
        raise ValueError('stale prior checkpoint addresses')
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    output = []
    for address, size, _, _ in rows:
        if address in processed:
            continue
        start = int(address,16)
        raw = semantic_evidence.read_function(binary,start,size)
        instructions = list(dis.disasm(raw,start))
        spec = decode_store(raw,start)
        if spec and (len(instructions)!=2 or instructions[0].mnemonic!='str'
                     or instructions[1].mnemonic!='bx' or instructions[1].op_str!='lr'):
            raise ValueError(f'Capstone disagreement at {address}')
        output.append({'address':address,'size':size,'raw_hex':raw.hex(),
                       'assembly':[f'{x.mnemonic} {x.op_str}' for x in instructions],
                       'class':'safe_store_candidate' if spec else 'unmodeled_not_executed',
                       'contract':spec})
    return output


def reference(seed, contract):
    regs=[(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    regs[contract['base']]=BASE
    return regs, regs[contract['source']]


def execute(binary, row, seed, flags):
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
    from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
        UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5,
        UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12)
    spec=row['contract']
    if spec is None:
        raise ValueError('refusing unmodeled entry')
    addr=int(row['address'],16)
    raw=semantic_evidence.read_function(binary,addr,row['size'])
    if raw.hex()!=row['raw_hex'] or decode_store(raw,addr)!=spec:
        raise ValueError('changed original ELF words')
    regs,expected=reference(seed,spec)
    gprs=(UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,
          UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,
          UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12)
    target=BASE+spec['offset']
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for page in sorted({addr & ~0xfff,(addr+4) & ~0xfff,RET & ~0xfff,BASE & ~0xfff}):
        uc.mem_map(page,0x1000,UC_PROT_ALL)
    uc.mem_write(addr,raw)
    uc.mem_write(RET,bytes(4))
    original=(seed ^ 0x4af399c5)&MASK
    uc.mem_write(target,original.to_bytes(4,'little'))
    uc.mem_write(BASE+0x300,CANARY)
    uc.reg_write(UC_ARM_REG_CPSR,flags|0x10)
    for reg,value in zip(gprs,regs):
        uc.reg_write(reg,value)
    uc.reg_write(UC_ARM_REG_SP,0x700ffc)
    uc.reg_write(UC_ARM_REG_LR,RET)
    trace=[];reads=[];writes=[]
    def hook_code(emu,pc,size,ud):
        trace.append(pc)
        if pc==RET: emu.emu_stop()
    def hook_read(emu,access,pos,size,value,ud): reads.append((pos,size))
    def hook_write(emu,access,pos,size,value,ud): writes.append((pos,size,value&MASK))
    uc.hook_add(UC_HOOK_CODE,hook_code)
    uc.hook_add(UC_HOOK_MEM_READ,hook_read)
    uc.hook_add(UC_HOOK_MEM_WRITE,hook_write)
    try:
        uc.emu_start(addr,MASK,timeout=1_000_000,count=4)
    except Exception as exc:
        raise AssertionError(f'Unicorn failed for {row["address"]} trace {trace}') from exc
    if trace!=[addr,addr+4,RET] or uc.reg_read(UC_ARM_REG_PC)!=RET:
        raise AssertionError('unexpected ARM trace or PC')
    if reads or writes!=[(target,4,expected)]:
        raise AssertionError(f'unexpected memory effects: {reads} {writes}')
    if (int.from_bytes(uc.mem_read(target,4),'little')!=expected or
            bytes(uc.mem_read(BASE+0x300,8))!=CANARY):
        raise AssertionError('memory content differs from model')
    if any(uc.reg_read(r)!=v for r,v in zip(gprs,regs)):
        raise AssertionError('unmodeled register effect')
    if uc.reg_read(UC_ARM_REG_SP)!=0x700ffc or uc.reg_read(UC_ARM_REG_LR)!=RET:
        raise AssertionError('SP or LR changed')
    if uc.reg_read(UC_ARM_REG_CPSR)&0xf000003f != (flags|0x10)&0xf000003f:
        raise AssertionError('CPSR changed')


def build(digest,fingerprint,rows,rounds):
    return {'schema':1,'elf_sha256':digest,'audit_rows_sha256':fingerprint,
            'entries':rows,'rounds':rounds,'new_certificates':0}


def render(state):
    rows=state['entries'];tested=sum(len(x['addresses']) for x in state['rounds'])
    lines=['# Engenharia de loop: 34 entradas ARM ainda nao modeladas','',
           'ELF original SHA-256: '+state['elf_sha256'],'',
           f'Inventario: {len(rows)}; stores reconhecidos e microexecutados: {tested}; '
           f'cenarios diferenciais: {sum(x["samples"] for x in state["rounds"])}; '
           f'pendentes: {len(rows)-tested}; certificados novos: 0.','',
           '| Endereco | Bytes originais | Instrucoes A32 | Estado |','|---|---|---|---|']
    for row in rows:
        lines.append(f'| {row["address"]} | {row["raw_hex"]} | '+
                     '; '.join(row['assembly']).replace('|','/')+f' | {row["class"]} |')
    lines +=['','## Limites','',
             'Executamos apenas STR palavra, AL, deslocamento positivo, pre-indexado e sem writeback, seguido de BX LR.',
             'Memoria e registradores iniciais sao sinteticos; nao se provam reachability, aliasing real ou equivalencia integral.',
             'Outros opcodes permanecem sem execucao e exigem modelos separados.',
             'Certificados originais: inalterados.','']
    return '\n'.join(lines)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for item in ('binary','manifests','pilot','prior-checkpoint','checkpoint','report'):
        p.add_argument('--'+item,type=Path,required=True)
    p.add_argument('--expected-missing',type=int,default=34)
    p.add_argument('--round-size',type=int,default=8)
    a=p.parse_args()
    if not (1<=a.expected_missing<=250 and 1<=a.round_size<=16):
        p.error('invalid loop limits')
    audit=audit_tool.audit(a.binary,a.manifests,a.pilot)
    prior_state=json.loads(a.prior_checkpoint.read_text(encoding='utf-8'))
    if (prior_state.get('elf_sha256')!=audit['digest'] or
        prior_state.get('eligible')!=len(prior_state.get('selected',[])) or
        prior_state.get('new_certificates')!=0):
        raise ValueError('invalid prior checkpoint identity')
    entries=catalog(a.binary,audit['rows'],prior_state['selected'])
    if len(entries)!=a.expected_missing:
        raise ValueError(f'expected {a.expected_missing} remaining, found {len(entries)}')
    fingerprint=hashlib.sha256(json.dumps(audit['rows'],sort_keys=True).encode()).hexdigest()
    selected=[x for x in entries if x['contract']]
    rounds=[]
    if a.checkpoint.is_file():
        old=json.loads(a.checkpoint.read_text(encoding='utf-8'))
        if old!=build(audit['digest'],fingerprint,entries,old.get('rounds',[])):
            raise ValueError('stale or tampered checkpoint')
        rounds=old['rounds']
    batches=[selected[i:i+a.round_size] for i in range(0,len(selected),a.round_size)]
    if len(rounds)>len(batches):
        raise ValueError('surplus rounds in checkpoint')
    for index,batch in enumerate(batches,1):
        for entry in batch:
            for seed in prior.SEEDS:
                for flags in prior.FLAGS:
                    execute(a.binary,entry,seed,flags)
        record={'iteration':index,'addresses':[r['address'] for r in batch],
                'samples':len(batch)*len(prior.SEEDS)*len(prior.FLAGS), 'status':'bounded_pass'}
        if index<=len(rounds):
            if rounds[index-1]!=record: raise ValueError('replayed round mismatch')
        else:
            rounds.append(record)
            a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
            tmp=a.checkpoint.with_suffix('.json.tmp')
            tmp.write_text(json.dumps(build(audit['digest'],fingerprint,entries,rounds),
                                indent=2,sort_keys=True)+'\n',encoding='utf-8')
            tmp.replace(a.checkpoint)
    state=build(audit['digest'],fingerprint,entries,rounds)
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(render(state),encoding='utf-8')
    print(f'REMAINING_34_CATALOG={len(entries)}')
    print(f'REMAINING_34_STORE_TESTED={len(selected)}')
    print(f'REMAINING_34_DYNAMIC_CASES={len(selected)*len(prior.SEEDS)*len(prior.FLAGS)}')
    print(f'REMAINING_34_UNMODELED={len(entries)-len(selected)}')
    print('REMAINING_34_FAILED=0')
    print('REMAINING_34_NEW_CERTIFICATES=0')


if __name__=='__main__':
    main()
