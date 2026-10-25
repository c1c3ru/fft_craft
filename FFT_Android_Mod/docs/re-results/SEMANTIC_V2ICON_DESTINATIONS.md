# V2Icon caller — three post-return destinations and state effects

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Execution starts **mid-function** at `0x25a298`, runs the actual BL/getter/BX LR, then follows one of three caller branches through its original instructions. Each unknown BL is a **stop boundary**, not a stub; a return path executes the original POP and stops at a synthetic caller address.

| Verified stop boundary | Number of controlled cases | Observed state |
|---|---:|---|
| setter BL `0x25a2bc` | 24 | r0=0x34, r1=0, object[8]=1; callee NOT executed |
| status BL `0x25a310` | 132 | r0=2; for getter=1, object[8]=0 and global bit 0x20 set |
| followup BL `0x25a328` | 52 | for getter=1, object[8]=0 and global bit 0x20 set |
| real POP → synthetic return `0x710100` | 80 | registers and stack restored |

**Post-getter branch micro-executions: 288/288 PASS.**

The trace and read/write hooks check the exact call/return and branch path, PC-relative literal, global pointer, conditional state stores, stack restoration and adjacent-memory canaries.

## Limitations

- The getter's table contents, object, globals, and caller stack are synthetic controlled memory.
- The earlier function entry and all three external callees are outside this bounded experiment.
- A path stopped before BL demonstrates its pre-call state, not the effect of that call or whole-function equivalence.
