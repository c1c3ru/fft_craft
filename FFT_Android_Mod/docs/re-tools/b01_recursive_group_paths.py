#!/usr/bin/env python3
"""B01: bounded recursive ARM CFG entry triage for the 9 co-terminal groups.

Bytes are verified against the exact original ELF, but recursive decode is not
runtime reachability: branch predicates, inline data, relocation and outside
call effects remain explicitly unknown. No semantic certificates are issued.
"""
import argparse
import hashlib
import json
from collections import deque, defaultdict
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import (
    ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_BX, ARM_INS_LDR,
    ARM_INS_MOV, ARM_INS_ADD, ARM_INS_POP, ARM_OP_IMM, ARM_CC_AL,
    ARM_CC_INVALID,
)
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

import b01_overlap_elf_evidence as baseline

MAX_STEPS_PER_ENTRY = 1024
MAX_OUT_EDGES = 4096


def h(x):
    return f"{x:08x}"


def non_al(insn):
    return insn.cc not in (ARM_CC_AL, ARM_CC_INVALID)


def relocations(elf):
    offsets = set()
    for section in elf.iter_sections():
        if isinstance(section, RelocationSection):
            for item in section.iter_relocations():
                offsets.add(int(item["r_offset"]))
    return offsets


def resolve_ldr_pc_slot(word, pc, elf, stream, reloc_sites):
    """Conservative A32 literal LDR PC candidate. A relocation blocks resolution."""
    if ((word >> 28) != 14 or ((word >> 26) & 3) != 1
            or ((word >> 25) & 1) or not ((word >> 24) & 1)
            or ((word >> 21) & 1) or not ((word >> 20) & 1)
            or ((word >> 16) & 15) != 15 or ((word >> 12) & 15) != 15):
        return {"classification": "unsupported_indirect_pc_write"}
    off = word & 0xfff
    slot = pc + 8 + (off if (word >> 23) & 1 else -off)
    if slot < 0 or slot % 4:
        return {"classification": "invalid_literal_slot"}
    raw, where = baseline.read_executable(elf, stream, slot, 4)
    if raw is None:
        # Many literal words are in read-only PT_LOAD rather than PF_X;
        # refuse to invent the answer when the auditor cannot read them.
        return {"classification": "literal_slot_outside_verified_exec_segment",
                "literal_slot": h(slot)}
    if slot in reloc_sites:
        return {"classification": "relocation_dependent_literal_slot",
                "literal_slot": h(slot)}
    val = int.from_bytes(raw, "little")
    return {"classification": "unrelocated_literal_target_candidate",
            "literal_slot": h(slot), "slot_file_offset": where,
            "slot_sha256": hashlib.sha256(raw).hexdigest(),
            "raw_target": h(val & ~1), "thumb_bit": bool(val & 1),
            "runtime_target_verified": False}


def walk(elf, stream, base, end, entry, md, reloc_sites):
    """Start at an actual declared entry and walk only direct A32 edges inside its group."""
    pending = deque([entry])
    visited = set()
    edges = []
    unknown = []
    returns = []
    decoded = []
    while pending:
        pc = pending.popleft()
        if pc in visited:
            continue
        if len(visited) >= MAX_STEPS_PER_ENTRY:
            unknown.append({"at": h(pc), "reason": "analysis_step_budget_exceeded"})
            break
        if pc < base or pc >= end or pc % 4:
            unknown.append({"at": h(pc), "reason": "outside_group_or_not_a32"})
            continue
        raw, _ = baseline.read_executable(elf, stream, pc, 4)
        if raw is None:
            unknown.append({"at": h(pc), "reason": "unmapped_executable_bytes"})
            continue
        inst = list(md.disasm(raw, pc))
        if len(inst) != 1 or inst[0].size != 4:
            unknown.append({"at": h(pc), "reason": "undecodable_a32_slot",
                            "raw_hex": raw.hex()})
            continue
        ins = inst[0]
        visited.add(pc)
        decoded.append({"pc":h(pc), "bytes":raw.hex(),
                        "mnemonic":ins.mnemonic,"operands":ins.op_str})
        conditional = non_al(ins)
        successors = []

        def direct(target, kind):
            if base <= target < end and target % 4 == 0:
                successors.append((target,kind))
            else:
                unknown.append({"at":h(pc),"reason":"out_of_group_direct_edge",
                                "kind":kind,"target":h(target & 0xffffffff)})

        def fall(kind="fallthrough"):
            direct(pc+4,kind)

        if ins.id == ARM_INS_B:
            if len(ins.operands) == 1 and ins.operands[0].type == ARM_OP_IMM:
                direct(int(ins.operands[0].imm) & 0xffffffff,"branch_taken_candidate")
            else:
                unknown.append({"at":h(pc),"reason":"non_immediate_branch"})
            if conditional:
                fall("branch_not_taken_candidate")
        elif ins.id in (ARM_INS_BL, ARM_INS_BLX):
            if len(ins.operands) == 1 and ins.operands[0].type == ARM_OP_IMM:
                unknown.append({"at":h(pc),"reason":"callee_effects_and_return_unknown",
                                "target":h(int(ins.operands[0].imm) & 0xffffffff)})
            else:
                unknown.append({"at":h(pc),"reason":"indirect_call_unresolved"})
            # A continuation can be explored but is an assumed-return edge.
            fall("call_return_assumed")
        elif ins.id == ARM_INS_BX:
            if ins.op_str.strip() == "lr":
                returns.append({"at":h(pc),"kind":"bx_lr_return_candidate"})
            else:
                unknown.append({"at":h(pc),"reason":"bx_indirect_unresolved",
                                "operands":ins.op_str})
            if conditional:
                fall("conditional_transfer_not_taken")
        elif ins.id == ARM_INS_POP and "pc" in ins.op_str:
            unknown.append({"at":h(pc),"reason":"return_via_stack_not_modeled"})
            if conditional:
                fall("conditional_transfer_not_taken")
        elif ins.id in (ARM_INS_LDR, ARM_INS_MOV, ARM_INS_ADD) and (
                ins.op_str.split(",",1)[0].strip() == "pc"):
            if ins.id == ARM_INS_LDR:
                detail = resolve_ldr_pc_slot(int.from_bytes(raw,"little"),pc,
                                             elf,stream,reloc_sites)
                unknown.append({"at":h(pc),"reason":"ldr_pc_indirect_not_runtime_verified",
                                "detail":detail})
            elif ins.id == ARM_INS_MOV and ins.op_str.strip() == "pc, lr":
                returns.append({"at":h(pc),"kind":"mov_pc_lr_return_candidate"})
            else:
                unknown.append({"at":h(pc),"reason":"other_pc_write_unresolved",
                                "operands":ins.op_str})
            if conditional:
                fall("conditional_transfer_not_taken")
        else:
            # If an exotic opcode can write PC, the whitelist above may miss
            # it. Do not claim this walk proves a complete control-flow graph.
            fall()
        for target,kind in successors:
            if len(edges) >= MAX_OUT_EDGES:
                unknown.append({"at":h(pc),"reason":"edge_budget_exceeded"})
                break
            edges.append({"from":h(pc),"to":h(target),"kind":kind})
            if target not in visited:
                pending.append(target)
    return {"entry":h(entry),"candidate_decoded_slots":len(visited),
            "candidate_decoded_bytes":4*len(visited),
            "decoded":decoded,
            "direct_edges":edges,"unresolved_boundaries":unknown,
            "candidate_returns":returns,
            "all_edges_proven":False,"runtime_reachable":False,
            "semantically_certified":False}


def audit(binary, inventory):
    if baseline.sha256(binary) != baseline.PINNED_ELF_SHA:
        raise ValueError("ELF SHA-256 mismatch")
    entries=baseline.get_entries(inventory)
    pairs=baseline.get_pairs(entries)
    if len(pairs)!=15:
        raise ValueError("Unexpected overlap count")
    groups=defaultdict(set)
    for left,right in pairs:
        if left["end"]!=right["end"]:
            raise ValueError("Non-co-terminal overlap")
        groups[left["end"]].update((left["start"],right["start"]))
    if len(groups)!=9:
        raise ValueError("Unexpected group count")
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.detail=True
    with binary.open("rb") as stream:
        elf=ELFFile(stream)
        if elf.elfclass!=32 or not elf.little_endian or elf["e_machine"]!="EM_ARM":
            raise ValueError("Expected original ARM ELF32")
        rel=relocations(elf)
        output=[]
        for end,starts in sorted(groups.items()):
            base=min(starts)
            paths=[walk(elf,stream,base,end,entry,md,rel)
                   for entry in sorted(starts)]
            output.append({
                "first_entry":h(base),"common_end":h(end),
                "entrypoints":[h(s) for s in sorted(starts)],
                "entry_witnesses":paths,
                "group_cfg_verified":False,"group_indirect_edges_resolved":False,
                "group_runtime_reachability_proven":False
            })
    paths=[p for g in output for p in g["entry_witnesses"]]
    return {"schema":1,"stage":"B01","elf_sha256":baseline.PINNED_ELF_SHA,
            "inventory_sha256":baseline.sha256(inventory),
            "groups":output,"group_count":len(output),"entrypoint_count":len(paths),
            "candidate_decoded_slots_total":sum(p["candidate_decoded_slots"] for p in paths),
            "indirect_unresolved_count":sum(
                "indirect" in u["reason"] or "pc_write" in u["reason"]
                for p in paths for u in p["unresolved_boundaries"]),
            "unknown_boundary_count":sum(len(p["unresolved_boundaries"]) for p in paths),
            "all_groups_cfg_proven":False,"all_indirect_edges_resolved":False,
            "new_semantic_certificates":0,"B01_done":False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--inventory",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    state=audit(args.binary,args.inventory)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(state,indent=2,sort_keys=True)+"\n",
                           encoding="utf-8")
    print("B01_RECURSIVE_GROUPS="+str(state["group_count"]))
    print("B01_RECURSIVE_ENTRIES="+str(state["entrypoint_count"]))
    print("B01_RECURSIVE_UNKNOWN_BOUNDARIES="+str(state["unknown_boundary_count"]))
    print("B01_RECURSIVE_INDIRECT_UNRESOLVED="+str(state["indirect_unresolved_count"]))
    print("B01_FULL_CFG_CERTIFICATES=0")


if __name__=="__main__":
    main()
