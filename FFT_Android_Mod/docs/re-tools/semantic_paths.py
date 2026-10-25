"""Extract strictly local conditional ARM branch evidence.

A CMP/TST immediately followed by B<cond> describes two local control-flow
edges. This is not a dominator analysis: paths can enter either instruction
from elsewhere, and the branch may not determine function-wide behavior.
"""
from capstone.arm import (
    ARM_INS_B, ARM_INS_CMP, ARM_INS_TST,
    ARM_OP_IMM, ARM_OP_REG, ARM_CC_AL, ARM_CC_INVALID,
)

CONDS = {"eq", "ne", "gt", "ge", "lt", "le",
         "hi", "hs", "cs", "lo", "cc", "ls", "mi", "pl", "vs", "vc"}
# These map the ARM NZCV conditions after a preceding CMP operation.
CMP_WORDING = {
    "eq": ("==", "!="), "ne": ("!=", "=="),
    "gt": ("> (signed)", "<= (signed)"),
    "ge": (">= (signed)", "< (signed)"),
    "lt": ("< (signed)", ">= (signed)"),
    "le": ("<= (signed)", "> (signed)"),
    "hi": ("> (unsigned)", "<= (unsigned)"),
    "ls": ("<= (unsigned)", "> (unsigned)"),
    "hs": (">= (unsigned)", "< (unsigned)"),
    "cs": (">= (unsigned)", "< (unsigned)"),
    "lo": ("< (unsigned)", ">= (unsigned)"),
    "cc": ("< (unsigned)", ">= (unsigned)"),
}


def _operand(insn, operand):
    if operand.type == ARM_OP_REG:
        return insn.reg_name(operand.reg)
    if operand.type == ARM_OP_IMM:
        return f"0x{operand.imm:x}" if operand.imm >= 0 else str(operand.imm)
    return None


def branch_guards(instructions):
    """Immediate CMP/TST -> conditional B pairs with both local successors."""
    found = []
    for addr, branch in sorted(instructions.items()):
        if branch.id != ARM_INS_B or branch.cc in (ARM_CC_AL, ARM_CC_INVALID):
            continue
        cond = branch.mnemonic.lower().removeprefix("b").replace(".w", "")
        if cond not in CONDS:
            continue
        previous = instructions.get(addr - 4)
        if (previous is None or previous.address + previous.size != addr
                or previous.id not in (ARM_INS_CMP, ARM_INS_TST)
                or previous.cc not in (ARM_CC_AL, ARM_CC_INVALID)
                or len(previous.operands) != 2
                or len(branch.operands) != 1
                or branch.operands[0].type != ARM_OP_IMM):
            continue
        lhs = _operand(previous, previous.operands[0])
        rhs = _operand(previous, previous.operands[1])
        if lhs is None or rhs is None:
            continue
        taken_desc = f"branch condition {cond} true"
        fall_desc = f"branch condition {cond} false"
        if previous.id == ARM_INS_CMP and cond in CMP_WORDING:
            t, f = CMP_WORDING[cond]
            taken_desc = f"{lhs} {t} {rhs}"
            fall_desc = f"{lhs} {f} {rhs}"
        elif previous.id == ARM_INS_TST and cond in ("eq", "ne"):
            base = f"({lhs} & {rhs})"
            taken_desc = base + (" == 0" if cond == "eq" else " != 0")
            fall_desc = base + (" != 0" if cond == "eq" else " == 0")
        found.append({
            "compare": previous.address,
            "compare_insn": f"{previous.mnemonic} {previous.op_str}",
            "branch": addr,
            "branch_insn": f"{branch.mnemonic} {branch.op_str}",
            "condition": cond,
            "taken_target": branch.operands[0].imm,
            "fallthrough_target": addr + branch.size,
            "taken_predicate": taken_desc,
            "fallthrough_predicate": fall_desc,
            "qualification": "local CMP/TST-B pair only; other incoming edges remain possible",
        })
    return found


def incoming_guard_edges(effects, guards):
    """Annotate directly incoming branch edges; never infer dominators."""
    annotated = []
    for effect in effects:
        entry = effect["addresses"][0]
        edges = []
        for guard in guards:
            if guard["taken_target"] == entry:
                edges.append({
                    "edge": "taken", "branch": guard["branch"],
                    "compare": guard["compare"],
                    "predicate": guard["taken_predicate"],
                })
            if guard["fallthrough_target"] == entry:
                edges.append({
                    "edge": "fallthrough", "branch": guard["branch"],
                    "compare": guard["compare"],
                    "predicate": guard["fallthrough_predicate"],
                })
        annotated.append({**effect, "incoming_guard_edges": edges})
    return annotated
