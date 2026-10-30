#!/usr/bin/env python3
"""B01: pair candidate A32 PUSH/P0P stack masks and enumerate external edges.

A textual path observed by a bounded recursive disassembler is not a
path-sensitive execution proof. Here every prologue link and callee remains
unverified pending a complete differential prologue -> epilogue.
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import b01_recursive_group_paths as recursive
import b01_overlap_elf_evidence as baseline

RETURN_REASON="return_via_stack_not_modeled"
EXTERNAL_REASONS=("out_of_group_direct_edge","callee_effects_and_return_unknown")


def push_mask(word):
    if (word & 0xffff0000)==0xe92d0000 and (word & 0x8000)==0 and (word & 0x2000)==0:
        return word & 0xffff
    return None


def pop_mask(word):
    if (word & 0x0fff0000)==0x08bd0000 and (word & 0x8000)!=0 and (word & 0x2000)==0 and (word >> 28)!=15:
        return word & 0xffff
    return None


def paired_prologue_candidates(steps, pop_addr, mask):
    """Match saved LR -> restored PC and all other restored registers."""
    expected=(mask & 0x7fff) | (1<<14)
    candidates=[]
    for step in steps:
        addr=int(step["pc"],16)
        if addr>=pop_addr:
            continue
        word=int.from_bytes(bytes.fromhex(step["bytes"]),"little")
        save=push_mask(word)
        if save is None:
            continue
        candidates.append({
            "push_address":step["pc"],"push_opcode":step["bytes"],
            "push_mask":f"{save:04x}",
            "restored_via_pop_mask":f"{mask:04x}",
            "same_saved_registers_except_lr_to_pc":save==expected,
            "required_saved_mask":f"{expected:04x}",
            "path_sensitive_and_stack_aliasing_proven":False})
    return candidates


def classify(state, entries):
    if state["elf_sha256"]!=baseline.PINNED_ELF_SHA:
        raise ValueError("Mismatch original ELF hash")
    declared={e["start"]:e for e in entries}
    ranges=sorted(entries,key=lambda e:e["start"])
    def potential_owners(addr):
        return [f"{e['start']:08x}" for e in ranges if e["start"]<=addr<e["end"]][:8]

    stack_sites=defaultdict(lambda: {"entries":set(),"candidates":[]})
    stack_occurrences=0
    external=[]
    for group in state["groups"]:
        for route in group["entry_witnesses"]:
            witness=route["entry"]
            steps=route["decoded"]
            for edge in route["unresolved_boundaries"]:
                kind=edge["reason"]
                if kind==RETURN_REASON:
                    stack_occurrences+=1
                    addr=int(edge["at"],16)
                    raw=next((s["bytes"] for s in steps if int(s["pc"],16)==addr),None)
                    if raw is None:
                        raise ValueError("Missing decoded POP PC bytes")
                    mask=pop_mask(int.from_bytes(bytes.fromhex(raw),"little"))
                    if mask is None:
                        raise ValueError("Expected explicit A32 POP PC opcode")
                    site=stack_sites[addr]
                    site["entries"].add(witness)
                    site["mask"]=mask
                    site["opcode"]=raw
                    site["candidates"].extend(
                        {"entrypoint":witness,**x}
                        for x in paired_prologue_candidates(steps,addr,mask))
                elif kind in EXTERNAL_REASONS:
                    # A direct edge has a concrete encoded target, but it is
                    # not a proven executable callee.
                    target=edge.get("target")
                    if not target:
                        raise ValueError("External edge lacks explicit target")
                    dest=int(target,16)
                    external.append({
                        "group_end":group["common_end"],
                        "entrypoint":witness,
                        "source":edge["at"],
                        "reason":kind,
                        "direct_immediate_target":target,
                        "target_at_declared_entry":dest in declared,
                        "possible_inventory_owners":potential_owners(dest),
                        "branch_predicate_and_callee_effects_proven":False,
                        "target_runtime_executed":False})
    out=[]
    for addr,s in sorted(stack_sites.items()):
        uniq={(c["entrypoint"],c["push_address"]):c for c in s["candidates"]}
        candidates=[v for _,v in sorted(uniq.items())]
        matched=sum(bool(c["same_saved_registers_except_lr_to_pc"]) for c in candidates)
        out.append({
            "pop_address":f"{addr:08x}","opcode_hex":s["opcode"],
            "register_mask":f"{s['mask']:04x}",
            "entrypoints_with_candidate_path":sorted(s["entries"]),
            "possible_preceding_pushes":candidates,
            "matching_push_masks_count":matched,
            "full_prologue_to_epilogue_execution_verified":False,
            "caller_frame_and_pc_restoration_proven":False})
    expected=state["boundary_reason_counts"]
    if len(out)!=14 or stack_occurrences!=28:
        raise ValueError("Original stack site baseline changed")
    if len(external)!=10 or (expected.get("out_of_group_direct_edge")!=6
                            or expected.get("callee_effects_and_return_unknown")!=4):
        raise ValueError("Original external-edge boundary baseline changed")
    return {"schema":1,"task":"B01","elf_sha256":baseline.PINNED_ELF_SHA,
            "recursive_group_count":state["group_count"],
            "stack_return_occurrences":stack_occurrences,
            "unique_stack_return_sites":len(out),
            "stack_returns":out,
            "external_boundary_occurrences":len(external),
            "external_boundaries":external,
            "external_boundary_kinds":dict(sorted(Counter(
                a["reason"] for a in external).items())),
            "stack_frames_verified":0,"external_callees_verified":0,
            "all_indirect_jumps_resolved":False,
            "new_semantic_certificates":0,"B01_done":False}


def audit(binary, inventory):
    state=recursive.audit(binary,inventory)
    return classify(state,baseline.get_entries(inventory))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--inventory",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    result=audit(a.binary,a.inventory)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("B01_STACK_RETURN_OCCURRENCES="+str(result["stack_return_occurrences"]))
    print("B01_STACK_RETURN_SITES="+str(result["unique_stack_return_sites"]))
    print("B01_EXTERNAL_BOUNDARIES="+str(result["external_boundary_occurrences"]))
    print("B01_PUSH_POP_MASK_MATCH_CANDIDATES="+str(sum(
        site["matching_push_masks_count"] for site in result["stack_returns"])))
    print("B01_STACK_FRAME_AND_CALLER_CERTIFICATES=0")


if __name__=="__main__":
    main()
