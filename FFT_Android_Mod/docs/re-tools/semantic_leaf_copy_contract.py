#!/usr/bin/env python3
"""Pilot complete *local* contracts for a second proof class beyond BX LR
(RE_COMPLETUDE_TASKS.md T12): a bounded, branch-free, call-free function that
only reads/writes fixed-offset memory fields -- "getters/setters" in T12's
wording. Scope name: pure_leaf_copy_v1.

Like semantic_bxlr_contract_pilot.py, this never claims full certification:
reviewer approval and the live gate re-check stay outside this module.
"""
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB

SCOPE = "pure_leaf_copy_v1"
CONTROL_FLOW_CLAIM = "no branches, no calls, no computed jumps -- single straight-line block ending in return"


def is_pure_leaf_copy(code: bytes, address: int, is_thumb: bool = False) -> bool:
    """Structural check: every byte decodes, zero bl/blx, zero branches
    other than the final return, zero computed jumps. This is what makes
    "no relevant callee" and "no branches" checkable, not just claimed.
    """
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB if is_thumb else CS_MODE_ARM)
    insns = list(md.disasm(code, address))
    consumed = sum(i.size for i in insns)
    if consumed != len(code):
        return False  # a gap means undecodable bytes or a stray data island
    if not insns:
        return False
    for i, insn in enumerate(insns):
        mnem, ops = insn.mnemonic, insn.op_str
        is_last = i == len(insns) - 1
        if mnem.startswith("bl"):
            return False  # bl/blx: a relevant callee, by definition excluded from this class
        if mnem == "bx" or (mnem.startswith("pop") and "pc" in ops):
            if not is_last:
                return False  # early return -- not a single straight-line block
            continue
        if mnem.startswith("b") and not mnem.startswith(("bic", "bfc", "bkpt")):
            return False  # any other branch, conditional or not
        if ("pc" in ops) and mnem in ("add", "ldr", "mov"):
            return False  # computed jump / direct PC write outside bx|pop{pc}
    last = insns[-1]
    if not (last.mnemonic == "bx" or (last.mnemonic.startswith("pop") and "pc" in last.op_str)):
        return False  # must end in an explicit return, not fall off the end
    return True
