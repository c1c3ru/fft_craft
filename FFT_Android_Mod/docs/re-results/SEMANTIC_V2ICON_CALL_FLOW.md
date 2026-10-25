# ARM V2Icon BL and caller return-value branch microexecution

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Starts **mid-function** at `0x25a298`, with `r0 = 0x34` as set by the immediately preceding ARM MOV. Executes original `BL 0x2b7ccc`, the five-opcode getter and BX LR return, then the caller's comparisons. Each destination instruction is **not executed**.

ELF indexed getter word (for r0=0x34): `0x19dca54`.

| Getter return r0 | Caller target | Controlled tests |
|---|---|---:|
| 1 | `0x25a2c8` | 4 |
| 2 | `0x25a2ac` | 4 |
| Other sampled 32-bit words | `0x25a2f8` | 40 |

**Caller-and-callee micro-executions: 48/48 PASS.**

Verified exact original instruction trace through BL and BX LR, two getter memory reads, returned r0, untouched table data, and three post-call branch destinations.

## Limits

- The V2Icon table contents are **synthetic**, not observed live data.
- The caller's preceding blocks, branch-destination instructions and later calls are not part of these executions.
- This is bounded machine behavior, NOT complete-function semantic equivalence.
