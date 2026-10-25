"""Bounded intra-function ARM control-flow graph for review evidence.

Edges are potential transfers between *decoded* instructions, not a proven
whole-program graph. Indirect jumps, missing decode, external transfers,
callee effects and exception/Thumb transitions remain unknown.
"""
from collections import deque

from capstone.arm import (
    ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_BX, ARM_INS_POP,
    ARM_INS_MOV, ARM_INS_LDR, ARM_INS_ADD,
    ARM_CC_AL, ARM_CC_INVALID, ARM_OP_IMM,
)


def _conditional(insn):
    return insn.cc not in (ARM_CC_AL, ARM_CC_INVALID)


def build_cfg(instructions, tables=()):
    """Return (successors, unknown), preserving branch-edge kinds."""
    successors = {a: [] for a in instructions}
    unknown = []
    table_targets = {dispatch: targets for _, dispatch, targets in tables}

    def edge(a, target, kind):
        if target in instructions:
            pair = (target, kind)
            if pair not in successors[a]:
                successors[a].append(pair)
        else:
            unknown.append((a, kind, target))

    for a, insn in sorted(instructions.items()):
        following = a + insn.size
        if insn.id == ARM_INS_B:
            if len(insn.operands) == 1 and insn.operands[0].type == ARM_OP_IMM:
                edge(a, insn.operands[0].imm, "taken")
            else:
                unknown.append((a, "indirect_branch", None))
            if _conditional(insn):
                edge(a, following, "not_taken")
        elif insn.id in (ARM_INS_BL, ARM_INS_BLX):
            # A call is not expanded; the only local modeled continuation
            # is return-to-next-instruction, assuming that it returns.
            edge(a, following, "call_returns")
        elif (insn.id == ARM_INS_POP and "pc" in insn.op_str
              or insn.id == ARM_INS_BX):
            # BX LR is usually a return. Other BX registers are unresolved.
            if insn.id == ARM_INS_BX and insn.op_str.strip() != "lr":
                unknown.append((a, "indirect_transfer", None))
            if _conditional(insn):
                edge(a, following, "not_taken")
        elif insn.id in (ARM_INS_ADD, ARM_INS_MOV, ARM_INS_LDR) and (
                insn.op_str.split(",", 1)[0].strip() == "pc"):
            if a in table_targets:
                for target in table_targets[a]:
                    edge(a, target, "jump_table")
            else:
                unknown.append((a, "pc_write", None))
            if _conditional(insn):
                edge(a, following, "not_taken")
        else:
            edge(a, following, "fallthrough")
    return successors, unknown


def predecessors(successors):
    backward = {a: [] for a in successors}
    for source, edges in successors.items():
        for dest, label in edges:
            backward[dest].append((source, label))
    for dest in backward:
        backward[dest].sort()
    return backward


def shortest_path(successors, source, dest):
    """One example modeled route; may loop, leave function, or be impossible."""
    if source not in successors or dest not in successors:
        return None
    queue = deque([(source, [source])])
    seen = {source}
    while queue:
        here, path = queue.popleft()
        if here == dest:
            return path
        for target, _ in successors[here]:
            if target not in seen:
                seen.add(target)
                queue.append((target, path + [target]))
    return None


def effect_routes(effects, guards, successors):
    """Find modeled paths from branch successors to candidate writes.

    Lack of a modeled path is NOT proof of semantic impossibility.
    """
    backward = predecessors(successors)
    results = []
    for effect in effects:
        entry = effect["addresses"][0]
        relevant = []
        for guard in guards:
            taken = shortest_path(successors, guard["taken_target"], entry)
            other = shortest_path(successors, guard["fallthrough_target"], entry)
            if taken is None and other is None:
                continue
            relevant.append({
                "compare": guard["compare"],
                "branch": guard["branch"],
                "taken_predicate": guard["taken_predicate"],
                "other_predicate": guard["fallthrough_predicate"],
                "taken_path": taken,
                "other_path": other,
                "modeled_exclusive": (taken is None) != (other is None),
            })
        results.append({
            **effect,
            "modeled_predecessors": backward.get(entry, []),
            "modeled_guard_routes": relevant,
        })
    return results
