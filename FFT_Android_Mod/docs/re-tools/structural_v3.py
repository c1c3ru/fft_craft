"""Structural v3: instruction/data gap accounting and conservative ARM jump-table checks.

A PC-relative LDR reference is candidate literal data, never semantic proof.
Only exact, validated branch-table words are included as instruction slots.
An automatic structural pass requires NO unexplained instruction slots and NO
unresolved/unsafe transfers. Unknowns remain needs_review.
"""
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_B, ARM_INS_CMP, ARM_INS_ADD, ARM_OP_IMM, ARM_CC_AL

import semantic_evidence

VERSION = 3
TOOLS = Path(__file__).resolve().parent
RULES_FILES = ("structural_v3.py", "jtable.py", "semantic_evidence.py")


def fingerprint():
    digest = hashlib.sha256()
    for name in RULES_FILES:
        digest.update(name.encode("ascii"))
        digest.update((TOOLS / name).read_bytes())
    return digest.hexdigest()[:20]


def _table_validation(data, start, instructions, tables):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    end = start + len(data)
    accounted = set()
    findings = []
    safe = True
    for guard, dispatch, targets in tables:
        record = {"guard": f"0x{guard:x}", "dispatch": f"0x{dispatch:x}",
                  "cases": len(targets), "safe": False, "reason": ""}
        cmp_insn, jump = instructions.get(guard), instructions.get(dispatch)
        if not (cmp_insn and jump and cmp_insn.id == ARM_INS_CMP
                and jump.id == ARM_INS_ADD and jump.cc == ARM_CC_AL
                and len(cmp_insn.operands) == 2
                and cmp_insn.operands[1].type == ARM_OP_IMM
                and cmp_insn.operands[1].imm >= 0
                and cmp_insn.operands[1].imm + 1 == len(targets)
                and len(targets) <= 512
                and "pc, pc," in jump.op_str):
            record["reason"] = "missing or unbounded CMP/ADD dispatch"
        elif not (start <= dispatch + 8
                  and dispatch + 8 + 4 * len(targets) <= end):
            record["reason"] = "branch table exceeds function boundary"
        else:
            entries = []
            for i, expected in enumerate(targets):
                at = dispatch + 8 + i * 4
                word = data[at - start: at - start + 4]
                decoded = list(md.disasm(word, at))
                if (len(word) != 4 or len(decoded) != 1
                        or decoded[0].id != ARM_INS_B
                        or decoded[0].cc != ARM_CC_AL
                        or len(decoded[0].operands) != 1
                        or decoded[0].operands[0].type != ARM_OP_IMM
                        or decoded[0].operands[0].imm != expected
                        or expected not in instructions
                        or at in instructions):
                    record["reason"] = f"unsafe branch entry or target at 0x{at:x}"
                    break
                entries.append(at)
            else:
                if any(a in accounted for a in entries):
                    record["reason"] = "overlapping jump-table entry ranges"
                else:
                    record["safe"] = True
                    accounted.update(entries)
            if not record["safe"] and not record["reason"]:
                record["reason"] = "ambiguous branch table"
        safe &= record["safe"]
        findings.append(record)
    return safe, accounted, findings


def inspect(data, start):
    """Inspect one ARM function byte slice. Returns JSON-serializable facts."""
    if start % 4 or len(data) % 4 or not data:
        return {"status": "needs_review", "reason": "non_arm_aligned_or_empty",
                "code_slots": 0, "literal_slots": [], "unexplained_slots": [],
                "tables_safe": False, "tables": []}
    instructions, tables, unresolved = semantic_evidence.collect(data, start)
    table_safe, table_slots, table_records = _table_validation(
        data, start, instructions, tables)
    end = start + len(data)
    code_slots = set(instructions) | table_slots
    # Detect duplicate/partial instructions or unexpected overlaps.
    valid_code = (start in instructions
                  and all(i.size == 4 and a % 4 == 0
                          and start <= a < end for a, i in instructions.items()))
    literals = semantic_evidence.pc_relative_literals(instructions, start, data)
    valid_literals = sorted(a for a in literals
                            if a not in code_slots and a % 4 == 0)
    if any(a in code_slots for a in literals):
        valid_code = False
    slots = set(range(start, end, 4))
    gaps = slots - code_slots
    literal_gaps = sorted(gaps & set(valid_literals))
    unexplained = sorted(gaps - set(literal_gaps))
    # An LDR-relative reference is NOT by itself a proof that data are inert.
    # Keep a visible independent evidence class; automatic structural acceptance
    # requires all remaining slots accounted for, and every table independently safe.
    accepted = (valid_code and not unresolved and table_safe and not unexplained
                and (len(code_slots) + len(literal_gaps) == len(slots)))
    return {
        "status": "auto_structural" if accepted else "needs_review",
        "reason": ("all_slots_accounted" if accepted else
                   "unresolved_dispatch" if unresolved else
                   "unverified_jump_table" if not table_safe else
                   "instruction_conflict" if not valid_code else
                   "unexplained_code_slots"),
        "function_start": f"0x{start:x}",
        "total_slots": len(slots),
        "code_slots": len(code_slots),
        "instruction_slots": len(instructions),
        "table_entry_slots": len(table_slots),
        "literal_slots": [f"0x{a:x}" for a in literal_gaps],
        "unexplained_slots": [f"0x{a:x}" for a in unexplained[:80]],
        "unexplained_count": len(unexplained),
        "unresolved_dispatches": [f"0x{a:x}" for a in unresolved],
        "tables_safe": table_safe,
        "tables": table_records,
        "code_coverage_pct": round(100 * len(code_slots) /
                                   max(len(slots) - len(literal_gaps), 1), 2),
        "candidate_literal_data_not_proven": True,
    }


def inspect_binary(binary, start, size):
    if start % 4 or size % 4 or size <= 0:
        return inspect(b"", start)
    return inspect(semantic_evidence.read_function(binary, start, size), start)
