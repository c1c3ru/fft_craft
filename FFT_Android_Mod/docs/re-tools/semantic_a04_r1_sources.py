#!/usr/bin/env python3
"""A04: conservative source-R1 provenance triage for 48 original ARM callsites.

Evidence is linear A32 disassembly in bounded containing-symbol windows. The
trace is a candidate use-def chain only, NOT a reachability/alias or
interprocedural proof. No libc or unknown code executes. Never promote
candidate input origins to NUL or length guarantees.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
import semantic_evidence
from semantic_a04_714a0_slot import SHA
from semantic_a04_b6620_xrefs import scan_original

TARGET = "000b6620"
MAX_LOOKBACK_BYTES = 0x4000
MAX_TRACE_DEFINITIONS = 12
MAX_TRACE_INSTRUCTIONS = 1024
ALIASES = {"sb": "r9", "sl": "r10", "fp": "r11", "ip": "r12"}
VOLATILE = {"r0","r1","r2","r3","r12","lr"}
LANES = ("file-io", "shader", "other", "all")
LOADS = {"ldr","ldrb","ldrh","ldrsb","ldrsh"}
STORES = {"str","strb","strh","stm","stmdb","push"}
UNARY = {"mov","mvn","adr"}
BINARY = {"add","sub","orr","eor","bic","and"}
BRANCHES = {"b","bx","bl","blx","pop","ldm","ldmia"}
REGEX = re.compile(r"^(?:r(?:1[0-5]|[0-9])|sp|lr|pc|sb|sl|fp|ip)$")


def canon(s):
    v = s.strip().lower()
    return ALIASES.get(v, v)


def is_reg(s):
    return bool(REGEX.fullmatch(s.strip().lower()))


def split_operands(s):
    """Separate A32 operands without splitting memory terms at commas."""
    pieces, now, depth = [], [], 0
    for char in s:
        if char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
        if char == "," and depth == 0:
            pieces.append("".join(now).strip())
            now = []
        else:
            now.append(char)
    pieces.append("".join(now).strip())
    return pieces


def opcode_base(op):
    """A32 conditional suffix, preserving branch and memory instruction names."""
    base = op["mnemonic"].lower().split(".")[0]
    known = sorted(LOADS | STORES | UNARY | BINARY |
                   BRANCHES | {"cmp","cmn","tst","teq","mul","mla",
                               "nop","rsb","adc","sbc","addw","subw"}, key=len, reverse=True)
    for prefix in known:
        if base == prefix or (base.startswith(prefix) and base[len(prefix):] in
                             ("eq","ne","cs","cc","mi","pl","vs","vc",
                              "hi","ls","ge","lt","gt","le")):
            return prefix, bool(base != prefix)
    return base, False


def lane_for(row):
    owners = " ".join(x["name"] for x in row["symbol_owners"]).lower()
    if "shader" in owners:
        return "shader"
    if any(x in owners for x in ("file","loader","save","autosave","read","pcm")):
        return "file-io"
    return "other"


def last_derived_definition(rows, register="r1", limit=MAX_TRACE_INSTRUCTIONS):
    """Walk a single linear A32 slice backward; every result is a *candidate*.

    BL invalidates AAPCS volatile regs but leaves callee-preserved R4-R11.
    Conditional writes, branch joins, stack spills, or symbol truncation
    result in an explicit missing-proof reason.
    """
    needle = canon(register)
    examined = 0
    steps = []
    flags = set()
    branch_count = 0
    for ins in reversed(rows[-limit:]):
        examined += 1
        pc = ins["pc"]
        mnemonic, conditional = opcode_base(ins)
        ops = split_operands(ins["operands"])
        if mnemonic in ("b", "bx", "bl", "blx"):
            if mnemonic in ("bl", "blx") and needle in VOLATILE:
                return {"kind":"volatile_across_call_unknown", "terminal":"call_clobber",
                        "terminal_pc":pc,"source_register":needle,
                        "steps":steps,"flags":sorted(flags | {"call_barrier"}),
                        "inspected":examined,"no_length_or_nul_proof":True}
            branch_count += 1
            flags.add("linear_path_not_proven")
            continue
        if mnemonic in ("pop", "ldm", "ldmia"):
            flags.add("unmodeled_stack_restore")
            continue
        if mnemonic in STORES or mnemonic in ("cmp","cmn","tst","teq","nop"):
            continue
        if not ops or canon(ops[0]) != needle:
            continue
        step={"pc":pc,"mnemonic":ins["mnemonic"],"operands":ins["operands"],
              "tracked":needle}
        steps.append(step)
        if conditional:
            flags.add("conditional_def_may_not_execute")
            return {"kind":"conditional_definition_unknown","terminal":"conditional_assignment",
                    "terminal_pc":pc,"source_register":needle,"steps":steps,
                    "flags":sorted(flags),"inspected":examined,
                    "no_length_or_nul_proof":True}
        if mnemonic in UNARY and len(ops)>1:
            src=canon(ops[1])
            if is_reg(src):
                needle=src
                continue
            if src == "#0":
                return {"kind":"syntactic_null_constant","terminal":"literal_zero",
                        "terminal_pc":pc,"steps":steps,
                        "flags":sorted(flags),"inspected":examined,
                        "no_length_or_nul_proof":True}
            return {"kind":"immediate_or_literal_candidate","terminal":src,
                    "terminal_pc":pc,"steps":steps,"flags":sorted(flags),
                    "inspected":examined,"no_length_or_nul_proof":True}
        if mnemonic in LOADS and len(ops)>1:
            location=ops[1]
            family="stack_slot_candidate" if "sp" in location.lower() else (
                "object_or_global_load_candidate")
            return {"kind":family,"terminal":location,"terminal_pc":pc,
                    "steps":steps,"flags":sorted(flags | {"loaded_pointer_not_validated"}),
                    "inspected":examined,"no_length_or_nul_proof":True}
        if mnemonic in BINARY and len(ops)>=3:
            left=canon(ops[1])
            right=ops[2]
            if is_reg(left) and right.startswith("#"):
                steps[-1]["arithmetic_offset"]=right
                needle=left
                flags.add("pointer_arithmetic_needs_bounds")
                continue
            return {"kind":"arithmetic_or_computed_pointer_candidate",
                    "terminal":ins["operands"],"terminal_pc":pc,
                    "steps":steps,"flags":sorted(flags | {"pointer_arithmetic_needs_bounds"}),
                    "inspected":examined,"no_length_or_nul_proof":True}
        return {"kind":"unsupported_register_def","terminal":ins["operands"],
                "terminal_pc":pc,"steps":steps,
                "flags":sorted(flags | {"unsupported_opcode"}),
                "inspected":examined,"no_length_or_nul_proof":True}
    if examined >= limit:
        flags.add("bounded_trace_exhausted")
    if needle in ("r0","r1","r2","r3"):
        kind="incoming_abi_argument_candidate"
    elif needle == "sp":
        kind="stack_pointer_derived_candidate"
    else:
        kind="callee_saved_or_unknown_register"
    return {"kind":kind,"terminal":needle,"terminal_pc":None,
            "steps":steps,"flags":sorted(flags | {"symbol_entry_not_cfg_proven"}),
            "inspected":examined,"no_length_or_nul_proof":True}


def disassemble_to_site(binary, row):
    addr=int(row["callsite"],16)
    owners=row["symbol_owners"]
    candidates=[x for x in owners if int(x["start"],16)<=addr<int(x["end"],16)]
    begin=max((int(x["start"],16) for x in candidates),default=max(0,addr-0x180))
    truncated = False
    if addr-begin > MAX_LOOKBACK_BYTES:
        begin=addr-MAX_LOOKBACK_BYTES
        truncated=True
    if begin % 4 != addr % 4:
        raise ValueError("Nonaligned A32 symbolic beginning")
    data=semantic_evidence.read_function(binary,begin,addr-begin+4)
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    instructions=list(decoder.disasm(data,begin))
    verified=bool(instructions and instructions[-1].address == addr
                  and instructions[-1].mnemonic == "bl"
                  and instructions[-1].op_str=="#0xb6620")
    if not verified:
        # Do not silently claim a valid flow for undecodable data.
        return [],{"complete_to_callsite":False,"truncated":truncated,
                   "owner_start":f"{begin:08x}",
                   "reason":"linear_disassembly_did_not_reach_expected_BL"}
    out=[{"pc":f"{i.address:08x}","mnemonic":i.mnemonic,
          "operands":i.op_str,"hex":i.bytes.hex()} for i in instructions]
    return out,{"complete_to_callsite":True,"truncated":truncated,
                "owner_start":f"{begin:08x}","instruction_count":len(out),
                "reason":"linear_A32_not_reachable_CFG"}


def audit(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original A04 ELF SHA changed")
    refs=scan_original(binary)
    sites=[r for r in refs["direct_bl_candidates"] if r["target"]==TARGET]
    if len(sites)!=48 or len({r["callsite"] for r in sites})!=48:
        raise ValueError("Original 48 A32 callsites baseline changed")
    records=[]
    for row in sites:
        stream,scope=disassemble_to_site(binary,row)
        trace=last_derived_definition(stream[:-1]) if stream else {
            "kind":"undecodable_context","terminal":"unknown",
            "steps":[],"flags":["no_linear_disassembly"],
            "no_length_or_nul_proof":True}
        records.append({"callsite":row["callsite"],
                        "lane":lane_for(row),
                        "owner_symbols":[x["name"] for x in row["symbol_owners"]],
                        "scope":scope,"r1_trace":trace,
                        "candidate_source_kind":trace["kind"],
                        "max_content_bytes_proven":None,
                        "nul_within_first_260_bytes_proven":False,
                        "origin_readable_proven":False,
                        "aliasing_excluded":False,
                        "path_reachability_proven":False,
                        "status":"unresolved"})
    totals=dict(sorted(Counter(x["candidate_source_kind"] for x in records).items()))
    lanes=dict(sorted(Counter(x["lane"] for x in records).items()))
    return {"schema":1,"elf_sha256":SHA,"max_safe_content_bytes":259,
            "max_total_copy_bytes":260,"total_a32_direct_calls":48,
            "lanes":lanes,"source_kinds":totals,"callsites":records,
            "bounded_nul_sources_proven":0,
            "unsafe_sources_dynamically_reproduced":0,
            "jni_runtime_coverage_proven":False,
            "new_certificates":0}


def render_report(data):
    lines=["# A04 — R1 string-origin provenance, 48 A32 callers","",
           "Conservative bounded linear use-def *candidates*, not CFG proofs.",
           "Never infer NUL termination or a <=259-byte source from pointer provenance.",
           "","## Aggregates","",
           "~~~json",json.dumps({"lanes":data["lanes"],"source_kinds":data["source_kinds"],
             "total":data["total_a32_direct_calls"],
             "nul_bound_proven":data["bounded_nul_sources_proven"]},indent=2),"~~~",
           "", "## Per-caller source trace",""]
    for row in data["callsites"]:
        lines.append("### 0x"+row["callsite"]+" — "+row["lane"])
        lines.append("Owner: "+", ".join(row["owner_symbols"]))
        lines.append("Candidate: "+row["candidate_source_kind"]+
                     " / terminal "+str(row["r1_trace"]["terminal"]))
        for step in row["r1_trace"]["steps"]:
            lines.append("- 0x"+step["pc"]+": "+step["mnemonic"]+" "+step["operands"])
        lines.append("NUL <=259 bytes: **not demonstrated**. "+ 
                     "CFG / JNI / aliasing / runtime bounds: **not demonstrated**.")
        lines.append("")
    return "\n".join(lines)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",required=True,type=Path)
    p.add_argument("--lane",choices=LANES,default="all")
    p.add_argument("--checkpoint",required=True,type=Path)
    p.add_argument("--report",required=True,type=Path)
    a=p.parse_args()
    data=audit(a.binary)
    selected=[x for x in data["callsites"] if a.lane=="all" or x["lane"]==a.lane]
    if not selected:
        raise ValueError("A04 selected lane had no caller records")
    result={k:v for k,v in data.items() if k!="callsites"}
    result["selected_lane"]=a.lane
    result["selected_count"]=len(selected)
    result["callsites"]=selected
    content=json.dumps(result,indent=2,sort_keys=True)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=content:
        raise ValueError("Original ELF source lineage checkpoint drift")
    a.checkpoint.write_text(content,encoding="utf-8")
    a.report.write_text(render_report(result),encoding="utf-8")
    print("A04_R1_TOTAL="+str(data["total_a32_direct_calls"]))
    print("A04_R1_LANES="+json.dumps(data["lanes"],sort_keys=True))
    print("A04_R1_KINDS="+json.dumps(data["source_kinds"],sort_keys=True))
    print("A04_R1_SELECTED="+a.lane+":"+str(len(selected)))
    for row in selected:
        print("A04_R1_CALLSITE="+row["callsite"]+" "+row["lane"]+" "+
              row["candidate_source_kind"]+" terminal="+str(row["r1_trace"]["terminal"]))
    print("A04_R1_BOUNDED_NUL_PROVEN=0")
    print("A04_R1_NEW_CERTIFICATES=0")


if __name__=="__main__":
    main()
