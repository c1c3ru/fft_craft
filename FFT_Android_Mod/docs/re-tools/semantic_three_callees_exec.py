#!/usr/bin/env python3
"""Bounded Unicorn tests for three ARM callees and two real caller continuations.

No external implementation or unknown branch target is executed or stubbed.
All memory and saved registers are synthetic controlled inputs, not live state.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_SP,
)
import semantic_branch_microexec as branch
import semantic_evidence
import semantic_three_callees_audit as audit
import semantic_v2icon_destinations as previous

SETTER, SOUND, CLEAR = 0x2B9CAC, 0x26B374, 0x282268
SOUND_TARGET = 0x2168E0
SPECIAL_TARGET = 0x2B8900
SETTER_LITERAL = 0x01721FC4
SETTER_LITERAL_ADDR = 0x2B9CC8
MAIN_SETTER = 0x25A2AC
MAIN_SETTER_END = 0x25A2C8
MAIN_CLEAR = 0x25A328
MAIN_CLEAR_END = 0x25A334
RETURN_PC = 0x710100
OBJECT = 0x500000
STACK_TOP = 0x701000
SAVED = (0x11113333, 0x44447777, 0x55559999, RETURN_PC)
OBJECT_CANARY = 0xC3C3A5A5
SLOT_LEFT, SLOT_RIGHT = 0xDEADBEEF, 0xBEEFDEAD
VALUES = (0, 1, 0x40, 0xFFFFFFFF)
CPSR = branch.CPSR_STATES
MODES = ("setter", "clear", "sound", "caller_setter", "caller_clear_sound")
EXPECTED = {
    "setter": (
        ("ldr", "r3, [pc, #0x14]"),
        ("cmp", "r0, #0x25"),
        ("add", "r3, pc, r3"),
        ("add", "r0, r3, r0, lsl #2"),
        ("str", "r1, [r0, #0xd04]"),
        ("bxne", "lr"),
        ("b", "#0x2b8900"),
    ),
    "clear": (
        ("mov", "r0, #0x31"), ("mov", "r1, #0"),
        ("b", "#0x2b9cac"),
    ),
    "sound": (("b", "#0x2168e0"),),
    "caller_setter": (
        ("mov", "r4, #1"), ("str", "r4, [r5, #8]"),
        ("mov", "r0, #0x34"), ("mov", "r1, #0"),
        ("bl", "#0x2b9cac"), ("str", "r4, [r5, #0x14]"),
        ("pop", "{r3, r4, r5, pc}"),
    ),
    "caller_clear_sound": (
        ("bl", "#0x282268"), ("mov", "r0, #1"),
        ("bl", "#0x26b374"),
    ),
}


def read_code(binary):
    """Read all related executable words and one separately tagged literal."""
    results = {
        "setter": semantic_evidence.read_function(binary, SETTER, 32),
        "sound": semantic_evidence.read_function(binary, SOUND, 4),
        "clear": semantic_evidence.read_function(binary, CLEAR, 12),
        "caller_setter": semantic_evidence.read_function(
            binary, MAIN_SETTER, MAIN_SETTER_END - MAIN_SETTER),
        "caller_clear_sound": semantic_evidence.read_function(
            binary, MAIN_CLEAR, MAIN_CLEAR_END - MAIN_CLEAR),
    }
    validate(results)
    return results


def validate(code):
    if set(code) != set(EXPECTED):
        raise ValueError("Missing or extraneous ARM code segment")
    starts = {
        "setter": SETTER, "clear": CLEAR, "sound": SOUND,
        "caller_setter": MAIN_SETTER, "caller_clear_sound": MAIN_CLEAR,
    }
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for name, signature in EXPECTED.items():
        buf = code[name]
        count = len(signature)
        length = count * 4
        if len(buf) != length + (4 if name == "setter" else 0):
            raise ValueError(f"ARM segment size changed: {name}")
        insns = list(md.disasm(buf[:length], starts[name]))
        if ([(x.mnemonic, x.op_str) for x in insns] != list(signature)
                or [x.address for x in insns] !=
                list(range(starts[name], starts[name] + length, 4))):
            raise ValueError(f"ARM opcode/branch signature changed: {name}")
        if name == "setter" and int.from_bytes(buf[length:], "little") != SETTER_LITERAL:
            raise ValueError("Setter literal changed")
    return True


def table_slot(index):
    if not 0 <= index <= 0xFFFFFFFF:
        raise ValueError("Index is not a 32-bit unsigned word")
    # ADD r3,PC,r3 at 0x2b9cb4; the ARM PC is instruction address + 8.
    base = (0x2B9CB4 + 8 + SETTER_LITERAL) & 0xFFFFFFFF
    return (base + ((index * 4) & 0xFFFFFFFF) + 0xD04) & 0xFFFFFFFF


def expected_mode(mode, index):
    if mode == "setter":
        return ("special_external", SPECIAL_TARGET) if index == 37 else (
            "returned", RETURN_PC)
    if mode == "clear":
        return "returned", RETURN_PC
    if mode == "sound" or mode == "caller_clear_sound":
        return "sound_unresolved", SOUND_TARGET
    return "returned", RETURN_PC


def expected_pc_trace(mode, index):
    setter_end = (0x2B9CC4 if mode == "setter" and index == 37 else
                  0x2B9CC0)
    setter = list(range(SETTER, setter_end + 4, 4))
    if mode == "setter":
        return setter + [SPECIAL_TARGET if index == 37 else RETURN_PC]
    if mode == "clear":
        return list(range(CLEAR, CLEAR + 12, 4)) + list(
            range(SETTER, 0x2B9CC0 + 4, 4)) + [RETURN_PC]
    if mode == "sound":
        return [SOUND, SOUND_TARGET]
    if mode == "caller_setter":
        return list(range(MAIN_SETTER, 0x25A2BC+4, 4)) + setter + [
            0x25A2C0, 0x25A2C4, RETURN_PC]
    return ([MAIN_CLEAR] + list(range(CLEAR, CLEAR + 12, 4))
            + list(range(SETTER, 0x2B9CC0 + 4, 4))
            + [0x25A32C, 0x25A330, SOUND, SOUND_TARGET])


def execute(code, mode, initial_index, initial_value, cpsr):
    validate(code)
    if (mode not in MODES or initial_index not in (37, 49, 52)
            or initial_value not in VALUES or cpsr not in CPSR):
        raise ValueError("Unexpected sampled ARM mode, index, value or NZCV")
    index = (49 if mode in ("clear", "caller_clear_sound") else
             52 if mode == "caller_setter" else initial_index)
    desired = (0 if mode in ("clear", "caller_setter", "caller_clear_sound")
               else initial_value)
    slot = table_slot(index)
    assert slot % 4 == 0
    page = lambda a: a & ~0xFFF
    pages = {page(a) for a in (
        SETTER, SOUND, CLEAR, MAIN_SETTER, MAIN_CLEAR, SPECIAL_TARGET,
        SOUND_TARGET, RETURN_PC, OBJECT, STACK_TOP-16,
        slot-4, slot, slot+4)}
    if len(pages) != 10:
        raise ValueError(f"Unexpected page collision: {list(map(hex, sorted(pages)))}")
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for p in sorted(pages):
        uc.mem_map(p, 0x1000, UC_PROT_ALL)
    for name, start in (("setter", SETTER), ("sound", SOUND),
                        ("clear", CLEAR), ("caller_setter", MAIN_SETTER),
                        ("caller_clear_sound", MAIN_CLEAR)):
        uc.mem_write(start, code[name])
    for stop_pc in (RETURN_PC, SOUND_TARGET, SPECIAL_TARGET):
        uc.mem_write(stop_pc, bytes.fromhex("0000a0e1"))
    def seed(address, value):
        uc.mem_write(address, value.to_bytes(4, "little"))
    for address, value in (
        (slot-4, SLOT_LEFT), (slot, 0xCECECECE), (slot+4, SLOT_RIGHT),
        (OBJECT+4, OBJECT_CANARY), (OBJECT+8, 0xEEDDCCBB),
        (OBJECT+12, OBJECT_CANARY), (OBJECT+0x14, 0x11225588),
        (OBJECT+0x18, OBJECT_CANARY), (STACK_TOP-20, OBJECT_CANARY),
    ):
        seed(address, value)
    for k, v in enumerate(SAVED):
        seed(STACK_TOP - 16 + 4*k, v)
    uc.reg_write(UC_ARM_REG_CPSR, cpsr)
    uc.reg_write(UC_ARM_REG_LR, RETURN_PC)
    uc.reg_write(UC_ARM_REG_R0, initial_index)
    uc.reg_write(UC_ARM_REG_R1, initial_value)
    uc.reg_write(UC_ARM_REG_R2, 0x22223333)
    uc.reg_write(UC_ARM_REG_R3, 0x44445555)
    uc.reg_write(UC_ARM_REG_R4, 0x66667777)
    uc.reg_write(UC_ARM_REG_R5, OBJECT)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP-16)
    starts = {
        "setter": SETTER, "clear": CLEAR, "sound": SOUND,
        "caller_setter": MAIN_SETTER,
        "caller_clear_sound": MAIN_CLEAR,
    }
    expected_kind, endpoint = expected_mode(mode, index)
    trace, reads, writes = [], [], []
    def instruction(emu, addr, size, data):
        trace.append(addr)
        if addr in (RETURN_PC, SOUND_TARGET, SPECIAL_TARGET):
            emu.emu_stop()
    def read(emu, access, addr, size, value, data):
        reads.append((addr, size))
    def write(emu, access, addr, size, value, data):
        writes.append((addr, size, value & ((1 << (size*8))-1)))
    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_READ, read)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(starts[mode], 0x720000, timeout=1_000_000, count=32)

    if trace != expected_pc_trace(mode, index) or uc.reg_read(UC_ARM_REG_PC) != endpoint:
        raise AssertionError(f"Incorrect ARM trace: {list(map(hex,trace))}")
    expected_reads = ([] if mode == "sound" else [(SETTER_LITERAL_ADDR,4)])
    if mode == "caller_setter":
        expected_reads += [(STACK_TOP-16+4*i,4) for i in range(4)]
    if reads != expected_reads:
        raise AssertionError(f"Unexpected read locations: {reads}")
    expected_writes = ([] if mode == "sound" else
                       [(slot,4,desired)])
    if mode == "caller_setter":
        expected_writes = [(OBJECT+8,4,1), (slot,4,0), (OBJECT+0x14,4,1)]
    if writes != expected_writes:
        raise AssertionError(f"Unexpected stores: {writes}")
    def memory(address):
        return int.from_bytes(uc.mem_read(address,4),"little")
    checks = [(slot-4, SLOT_LEFT), (slot, desired if mode!="sound" else 0xCECECECE),
              (slot+4, SLOT_RIGHT), (OBJECT+4, OBJECT_CANARY),
              (OBJECT+8, 1 if mode=="caller_setter" else 0xEEDDCCBB),
              (OBJECT+12, OBJECT_CANARY),
              (OBJECT+0x14, 1 if mode=="caller_setter" else 0x11225588),
              (OBJECT+0x18, OBJECT_CANARY), (STACK_TOP-20, OBJECT_CANARY)]
    for addr, value in checks:
        if memory(addr) != value:
            raise AssertionError(f"State or canary mismatch 0x{addr:x}")
    if mode=="caller_setter":
        if (uc.reg_read(UC_ARM_REG_SP) != STACK_TOP or
                tuple(uc.reg_read(reg) for reg in (
                    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5)) != SAVED[:3]):
            raise AssertionError("Caller POP did not restore saved registers")
    elif uc.reg_read(UC_ARM_REG_SP) != STACK_TOP-16:
        raise AssertionError("Unexpected stack change")
    if mode in ("sound", "caller_clear_sound") and (
            uc.reg_read(UC_ARM_REG_R0) != (1 if mode=="caller_clear_sound" else initial_index)):
        raise AssertionError("Forwarded sound_request argument changed")
    return {"kind":expected_kind, "end":endpoint, "trace":trace,
            "reads":reads, "writes":writes, "slot":slot}


def run(binary, inventory):
    audit.validate_inventory(inventory)
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    code = read_code(binary)
    count = {mode:0 for mode in MODES}
    for mode in MODES:
        indices = (37,49,52) if mode in ("setter","sound") else (49,)
        for index in indices:
            for value in VALUES:
                for cpsr in CPSR:
                    execute(code, mode, index, value, cpsr)
                    count[mode]+=1
    total = sum(count.values())
    if total!=72:
        raise AssertionError(f"Expected 72 machine samples, not {total}")
    return "\n".join([
        "# Three callees and two caller continuations — original ARM execution", "",
        f"ELF SHA-256: `{digest}`", "",
        "| Route | Microexecutions | Measured boundary |",
        "|---|---:|---|",
        f'| iOS_setV2Icon direct | {count["setter"]} | '
        "Indexed word written; idx=37 branches to unknown 0x2b8900 |",
        f'| iOS_clearOkNg direct | {count["clear"]} | '
        "Sets index 49 to zero through original setter, returns via LR |",
        f'| sound_request direct | {count["sound"]} | '
        "Unconditional branch to unresolved 0x2168e0, no local writes |",
        f'| houkoku_okng setter continuation | {count["caller_setter"]} | '
        "Object fields +8 and +0x14 set to 1, setter table index 52 set to 0, POP return |",
        f'| houkoku_okng clear/sound continuation | '
        f'{count["caller_clear_sound"]} | '
        "Table index 49 cleared, then sound_request branch boundary |",
        "", f"**Three-callee and caller tests: {total}/{total} PASS.**", "",
        "Every test checks the actual instruction PC trace, real ARM "
        "BL/BX/B control flow, memory read/write hooks, adjacent word "
        "canaries, the stack, and a synthetic return address.", "",
        "## Unknown / deferred contracts", "",
        "- `sound_request(int)` only jumps to `0x2168e0`; that "
        "destination is not executed here. No sound effect has been proven.",
        "- `iOS_setV2Icon` at index 37 stores a word then branches to "
        "`0x2b8900`; the target is not executed, so its later effects "
        "and return are unknown.",
        "- Other callers, argument ranges, actual table contents, and "
        "aliasing remain unverified.",
        "- Starting at caller branch entries does not validate the entire "
        "`houkoku_okng()` function or establish semantic equivalence.",
        "- All registers, pointers and global table contents are synthetic "
        "test inputs; findings apply to these bounded machine paths only.", "",
    ])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,
                   default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    p.add_argument("--inventory",type=Path,
                   default=semantic_evidence.ROOT/"docs/RE_FUNCTION_INVENTORY.csv")
    p.add_argument("--results",type=Path,
                   default=semantic_evidence.ROOT/"docs/re-results")
    args=p.parse_args()
    report=args.results/"SEMANTIC_THREE_CALLEES_EXECUTION.md"
    report.write_text(run(args.binary,args.inventory),encoding="utf-8")
    print(f"Verified callee and caller ARM microexecution: {report}")


if __name__=="__main__":
    main()
