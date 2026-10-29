#!/usr/bin/env python3
"""Batch classification of all direct A32 callers of original A04 0xb6620.

Classifies the original 34 strict MOV-only allocators and more syntactic
variants (MOV/STR/LDR); segregates shader callers with unproven pointer
provenance. It does not prove runtime reachability, successful allocation,
source termination, size bounds, or Android/JNI semantics.
"""
import argparse
import hashlib
import json
from pathlib import Path

from semantic_a04_714a0_slot import SHA
from semantic_a04_b6620_xrefs import scan_original
from semantic_a04_alloc_provenance import classify_candidate

TARGET = "000b6620"
SIZE = 0x10c
NEW = "#0x2cdf6c"

def is_r0_write(ins):
    op = ins["operands"].replace(" ", "")
    return (op.startswith("r0,") and
            ins["mnemonic"] not in ("str", "strb", "strh"))

def classify(row):
    lines = row["context_linear_not_cfg"]
    positions = [i for i, x in enumerate(lines) if x["pc"] == row["callsite"]]
    if len(positions) != 1:
        raise ValueError("Original BL callsite not found in bounded context")
    target = positions[0]
    strict = bool(classify_candidate(row)["matches_size_and_call"])
    matches = []
    for a in range(max(0, target-12), target-2):
        head = lines[a]
        if head["mnemonic"] != "mov" or head["operands"] != "r0, #0x10c":
            continue
        for b in range(a+1, min(a+7,target)):
            op = lines[b]
            if op["mnemonic"] != "bl" or op["operands"] != NEW:
                continue
            before = lines[a+1:b]
            if any(is_r0_write(x) or x["mnemonic"].startswith(("bl","b "))
                   for x in before):
                continue
            after = lines[b+1:target]
            if not after or len(after) > 6:
                continue
            if any(is_r0_write(x) or x["mnemonic"].startswith("bl")
                   or x["mnemonic"] in ("b", "bx") for x in after):
                continue
            # No R0 clobbering is enough to keep the *candidate* return
            # in R0 until the BL; check that R1 is populated locally.
            assigned_r1 = [x for x in after if
                           x["operands"].replace(" ","").startswith("r1,")
                           and x["mnemonic"] in ("mov","ldr","add")]
            if not assigned_r1:
                continue
            matches.append({"size_pc": head["pc"], "new_call_pc":op["pc"],
                            "source_setup":assigned_r1,
                            "post_alloc_instructions":after})
    if matches:
        if strict and not matches:
            raise AssertionError("Strict match excluded from broad match")
        return {"class": "new_0x10c_candidate",
                "strict_old_rule":strict,
                "candidate_allocations": matches,
                "actual_allocated_capacity_proven":False,
                "source_length_proven":False}
    if strict:
        raise AssertionError("Old strict allocator pattern was lost")
    pc = int(row["callsite"],16)
    if pc == 0xab6cc:
        category = "shader_stack_pointer_candidate"
    elif pc == 0xab6a4:
        category = "shader_carried_pointer_candidate"
    else:
        category = "unresolved_other_pointer_source"
    return {"class":category,"strict_old_rule":False,
            "candidate_allocations":[],
            "actual_allocated_capacity_proven":False,
            "source_length_proven":False}

def batch(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("Expected original ELF SHA-256")
    refs=scan_original(binary)
    rows=[x for x in refs["direct_bl_candidates"] if x["target"]==TARGET]
    results=[{"callsite":r["callsite"],
              "symbol_owners":r["symbol_owners"],
              "classification":classify(r)}
             for r in rows]
    buckets={}
    for row in results:
        name=row["classification"]["class"]
        buckets[name]=buckets.get(name,0)+1
    strict=sum(x["classification"]["strict_old_rule"] for x in results)
    expanded=sum(x["classification"]["class"]=="new_0x10c_candidate" for x in results)
    if len(rows)!=48 or strict!=34:
        raise ValueError("Previous fixed-ELF A04 callsite baseline drift")
    if expanded<strict or len({x["callsite"] for x in results})!=len(rows):
        raise ValueError("Expanded classifier regressed or duplicated calls")
    return {"schema":1,"elf_sha256":SHA,"callsites_total":len(results),
            "prior_strict_new":strict,
            "expanded_new_0x10c":expanded,
            "new_variants_over_old":expanded-strict,
            "remaining_non_0x10c":len(rows)-expanded,
            "buckets":buckets,"callsites":results,
            "reachable_calls_verified":False,
            "source_maximum_proven":False,
            "all_48_runtime_buffers_verified":False,
            "new_certificates":0}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--checkpoint",type=Path,required=True)
    p.add_argument("--report",type=Path,required=True)
    a=p.parse_args()
    data=batch(a.binary)
    payload=json.dumps(data,indent=2,sort_keys=True)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=payload:
        raise ValueError("A04 batch classification checkpoint drift")
    a.checkpoint.write_text(payload,encoding="utf-8")
    lines=["# A04 — batch of all 48 original A32 callers","",
           "Structural evidence only, not runtime proof.","",
           "## Counts","", "~~~json",
           json.dumps({k:data[k] for k in
           ("callsites_total","prior_strict_new","expanded_new_0x10c",
            "new_variants_over_old","remaining_non_0x10c","buckets")},indent=2),
           "~~~","", "## Caller classification",""]
    for row in data["callsites"]:
        lines.append("- "+row["callsite"]+" — "+row["classification"]["class"]+
                     " — "+", ".join(x["name"] for x in row["symbol_owners"]))
    lines.extend(["","Unresolved: original source lengths; success/error of new;",
                  "14 or fewer non-identical uses; reachability; JNI/Android checks.",""])
    a.report.write_text("\n".join(lines),encoding="utf-8")
    print("A04_BATCH_COUNTS="+json.dumps({k:data[k] for k in
          ("callsites_total","prior_strict_new","expanded_new_0x10c",
           "new_variants_over_old","remaining_non_0x10c","buckets")}))
    for x in data["callsites"]:
        if x["classification"]["class"]!="new_0x10c_candidate":
            print("A04_BATCH_REQUIRES_SEMANTICS="+x["callsite"]+" "+
                  x["classification"]["class"]+" "+
                  ",".join(y["name"] for y in x["symbol_owners"]))
    print("A04_BATCH_FULL_RUNTIME_COVERAGE=0")

if __name__=="__main__":
    main()
