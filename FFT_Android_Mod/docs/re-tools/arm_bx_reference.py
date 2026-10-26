"""Independent pure-state reference for ARMv5/v7 A32 BX LR normal execution.

This models only the documented nonexceptional instruction transition.
It does not model external interrupts, instruction fetch faults, privilege
restrictions, unpredictable targets, or whole-program effects.
"""
ENCODING = bytes.fromhex("1eff2fe1")
THUMB_BIT = 1 << 5


def branch_exchange_lr(word: bytes, lr: int, cpsr: int) -> tuple[int, int]:
    """Normal A32 BX R14 transition, with valid aligned code return targets.

    The instruction selects instruction-set state from LR[0], and transfers
    to LR with bit 0 cleared. ARM returns must be word aligned, Thumb returns
    must be halfword aligned. Other CPSR bits are preserved in normal flow.
    """
    if word != ENCODING:
        raise ValueError("not the unconditional A32 BX LR opcode")
    if not 0 <= lr <= 0xFFFFFFFF or not 0 <= cpsr <= 0xFFFFFFFF:
        raise ValueError("register value outside 32 bits")
    if cpsr & THUMB_BIT:
        raise ValueError("precondition failed: execution must begin in ARM state")
    if not (cpsr & 0x1F) in (0x10, 0x1F):
        raise ValueError("unsupported execution mode for this reference")
    target = lr & ~1
    if not (lr & 1) and target & 3:
        raise ValueError("ARM return not word aligned")
    expected_cpsr = (cpsr & ~THUMB_BIT) | (THUMB_BIT if lr & 1 else 0)
    return target, expected_cpsr
