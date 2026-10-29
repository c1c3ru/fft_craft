#!/usr/bin/env python3
"""A04: one-hop A32 direct-call inventory for ABI-argument R1 sources.

Input is the original ELF plus 48 previously classified R1 callsites. For
those whose R1 source traces to an incoming ABI argument, look for direct A32
BLs into their containing function symbol. Only structural evidence.
No proof of control-flow reachability, incoming string length or JNI inputs.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from elftools.elf.elffile import ELFFile
from semantic_a04_714a0_slot import SHA
from semantic_a04_b6620_xrefs import decode_arm_bl, scan_original
from semantic_a04_r1_sources import audit

ABI_KIND="incoming_abi_argument_candidate"


def direct_bl_to_targets(binary, entries):
    found={key:[] for key in entries}
    with binary.open("rb") as fh:
        elf=ELFFile(fh)
        if elf.elfclass!=32 or elf["e_machine"]!="EM_ARM":
            raise ValueError("Not the original ARM32 ELF")
        for seg in elf.iter_segments():
            if seg["p_type"]!="PT_LOAD" or not int(seg["p_flags"]) & 1:
                continue
            address=int(seg["p_vaddr"])
            length=int(seg["p_filesz"])
            fh.seek(int(seg["p_offset"]))
            blob=fh.read(length)
            if len(blob)!=length:
                raise ValueError("Truncated original executable PT_LOAD")
            for offset in range((-address)%4,len(blob)-3,4):
                pc=address+offset
                word=int.from_bytes(blob[offset:offset+4],"little")
                dest=decode_arm_bl(word,pc)
                if dest in found:
                    found[dest].append({"pc":f"{pc:08x}",
                                        "word_le":f"{word:08x}",
                                        "target":f"{dest:08x}",
                                        "static_only":True})
    return found


def one_hop(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original ELF changed")
    first=audit(binary)
    refs=scan_original(binary)["direct_bl_candidates"]
    ref_by_pc={x["callsite"]:x for x in refs if x["target"]=="000b6620"}
    targets={}
    for row in first["callsites"]:
        if row["candidate_source_kind"]!=ABI_KIND:
            continue
        owner=ref_by_pc[row["callsite"]]["symbol_owners"]
        if not owner:
            continue
        chosen=max(owner,key=lambda x:int(x["start"],16))
        entry=int(chosen["start"],16)
        targets.setdefault(entry,chosen["name"])
    matches=direct_bl_to_targets(binary,targets)
    records=[]
    for row in first["callsites"]:
        if row["candidate_source_kind"]!=ABI_KIND:
            continue
        owner=ref_by_pc[row["callsite"]]["symbol_owners"]
        if not owner:
            symbol=None; incoming=[]
        else:
            chosen=max(owner,key=lambda x:int(x["start"],16))
            symbol=chosen
            incoming=matches.get(int(chosen["start"],16),[])
        records.append({"downstream_callsite":row["callsite"],
                        "source_abi_register":row["r1_trace"]["terminal"],
                        "owner_function":symbol,
                        "one_hop_direct_a32_bl_count":len(incoming),
                        "sample_upstream_callers":incoming[:30],
                        "upstream_calls_truncated":len(incoming)>30,
                        "other_upstream_Thumb_indirect_or_dynamic_not_examined":True,
                        "incoming_string_nul_or_length_proven":False})
    if len(records)!=first["source_kinds"].get(ABI_KIND):
        raise ValueError("Original R1 argument baseline changed")
    no_direct=sum(x["one_hop_direct_a32_bl_count"]==0 for x in records)
    unique_targets=len(targets)
    return {"schema":1,"elf_sha256":SHA,
            "incoming_abi_downstream_calls":len(records),
            "unique_containing_function_entries":unique_targets,
            "sources_without_a32_upstream_caller":no_direct,
            "total_source_to_function_a32_edges":sum(x["one_hop_direct_a32_bl_count"]
                                                     for x in records),
            "records":records,
            "global_reachability_verified":False,
            "source_bound_or_nul_proven":0,
            "android_jni_upstream_calls_resolved":False,
            "new_certificates":0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--checkpoint",type=Path,required=True)
    a=p.parse_args()
    record=one_hop(a.binary)
    payload=json.dumps(record,indent=2,sort_keys=True)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=payload:
        raise ValueError("Original A04 one-hop provenance checkpoint drift")
    a.checkpoint.write_text(payload,encoding="utf-8")
    print("A04_R1_UPSTREAM_COUNTS="+json.dumps({
        k:record[k] for k in ("incoming_abi_downstream_calls",
            "unique_containing_function_entries","sources_without_a32_upstream_caller",
            "total_source_to_function_a32_edges")},sort_keys=True))
    for row in record["records"]:
        print("A04_R1_UPSTREAM "+row["downstream_callsite"]+" source="+
              str(row["source_abi_register"])+" symbol="+
              str(row["owner_function"]["name"] if row["owner_function"] else "unresolved")+
              " a32_direct_callers="+str(row["one_hop_direct_a32_bl_count"]))
    print("A04_R1_UPSTREAM_NUL_PROVEN=0")


if __name__=="__main__":
    main()
