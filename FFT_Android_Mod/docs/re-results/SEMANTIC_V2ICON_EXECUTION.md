# Isolated ARM V2Icon getter — machine-executed contract

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Callsite: `0x25a298` BL `0x2b7ccc` — `iOS_getV2Icon(V2ICON_DATA)`.

Original ELF literal at `0x2b7ce0`: `0x01723fa8`.

Under controlled aligned memory, five original ARM instructions read the literal, compute a word-table address indexed by r0, load r0 and return via BX LR.

| Checked contract | Result |
|---|---|
| Five executable instructions, sixth word treated as literal | PASS |
| Exact code trace, LR return and address selection | PASS |
| Exactly two 32-bit reads: literal and indexed table word | PASS |
| No memory writes, preserved adjacent table words | PASS |
| Return r0 equals initialized selected word | PASS |

**V2Icon isolated micro-executions: 120/120 PASS.**

## Boundaries of this evidence

- Original callee code and ELF literal are executed, but the table data and return PC are **synthetic**.
- A valid-index range or actual game-state table contents has not been established.
- The caller before/after BL, later branches, real runtime pointers and complete-function equivalence are not demonstrated.
