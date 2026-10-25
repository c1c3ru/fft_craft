"""Conservative, instruction-local ARM semantic observations.

These are candidate effects from adjacent decoded instructions, never
function-wide behavioral proofs or replacement implementations.
"""
from capstone.arm import (
    ARM_INS_BL, ARM_INS_BLX, ARM_INS_LDR, ARM_INS_STR, ARM_INS_BIC,
    ARM_INS_ORR, ARM_INS_TST, ARM_OP_MEM, ARM_OP_REG, ARM_OP_IMM,
    ARM_CC_AL, ARM_CC_INVALID,
)


def calls(instructions):
    """Distinguish BL/BLX calls from BLE/BLT conditional branches by opcode ID."""
    return [(address, insn) for address, insn in sorted(instructions.items())
            if insn.id in (ARM_INS_BL, ARM_INS_BLX)]


def _unconditional(insn):
    return insn.cc in (ARM_CC_AL, ARM_CC_INVALID)


def _mem(insn, index):
    if len(insn.operands) <= index:
        return None
    op = insn.operands[index]
    if op.type != ARM_OP_MEM or op.mem.index or getattr(insn, "writeback", False):
        return None
    return op.mem.base, op.mem.disp


def _match(seq):
    """Match LDR, optional TST, BIC/ORR, STR with no intervening instructions."""
    if len(seq) not in (3, 4):
        return None
    if any(seq[i].address + seq[i].size != seq[i + 1].address
           for i in range(len(seq) - 1)):
        return None
    load, *middle, store = seq
    op = middle[-1]
    test = middle[0] if len(middle) == 2 else None
    if (load.id != ARM_INS_LDR or store.id != ARM_INS_STR
            or op.id not in (ARM_INS_BIC, ARM_INS_ORR)
            or not _unconditional(load)
            or not _mem(load, 1) or _mem(load, 1) != _mem(store, 1)):
        return None
    if (len(load.operands) < 2 or len(store.operands) < 2
            or load.operands[0].type != ARM_OP_REG
            or store.operands[0].type != ARM_OP_REG
            or len(op.operands) != 3
            or op.operands[0].type != ARM_OP_REG
            or op.operands[1].type != ARM_OP_REG
            or op.operands[2].type != ARM_OP_IMM):
        return None
    reg = load.operands[0].reg
    if not (reg == store.operands[0].reg == op.operands[0].reg
            == op.operands[1].reg or op.cc != store.cc):
        return None
    if test is not None:
        if (test.id != ARM_INS_TST or not _unconditional(test)
                or len(test.operands) != 2
                or test.operands[0].type != ARM_OP_REG
                or test.operands[0].reg != reg
                or test.operands[1].type != ARM_OP_IMM):
            return None
    mask = int(op.operands[2].imm)
    if mask <= 0:
        return None
    base, displacement = _mem(store, 1)
    if not base:
        return None
    mem = f"[{store.reg_name(base)}"
    if displacement:
        mem += f", #{displacement}"
    mem += "]"
    conditional = not _unconditional(op)
    return {
        "kind": "clear_bits" if op.id == ARM_INS_BIC else "set_bits",
        "mask": mask, "memory": mem,
        "condition": op.mnemonic[-2:] if conditional else "always",
        "test_mask": int(test.operands[1].imm) if test is not None else None,
        "addresses": [i.address for i in seq],
        "qualification": "candidate path-local read-modify-write, not a function invariant",
    }


def bitmask_effects(instructions):
    """Consecutive sequences only; no guesses across a control-flow join."""
    seq = [x for _, x in sorted(instructions.items())]
    effects = []
    for i in range(len(seq)):
        for width in (4, 3):
            if i + width <= len(seq):
                match = _match(seq[i:i + width])
                if match:
                    effects.append(match)
                    break
    return effects
