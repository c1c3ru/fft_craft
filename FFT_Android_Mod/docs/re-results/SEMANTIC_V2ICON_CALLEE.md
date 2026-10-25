# ARM callee boundary: iOS_getV2Icon

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Caller: `0x25a298`: `bl #0x2b7ccc`.
Callee: `0x2b7ccc`, 24 bytes, `iOS_getV2Icon(V2ICON_DATA)` (inventory identifier only).

## All six original ARM instructions

| Address | Instruction |
|---|---|
| `0x2b7ccc` | `ldr r3, [pc, #0xc]` |
| `0x2b7cd0` | `add r3, pc, r3` |
| `0x2b7cd4` | `add r0, r3, r0, lsl #2` |
| `0x2b7cd8` | `ldr r0, [r0, #0xd04]` |
| `0x2b7cdc` | `bx lr` |
| `0x2b7ce0` | `cmneq r2, r8, lsr #31` |

## Instruction-level register access (Capstone heuristic)

| Address | Read registers | Written registers |
|---|---|---|
| `0x2b7ccc` | pc | r3 |
| `0x2b7cd0` | pc, r3 | r3 |
| `0x2b7cd4` | r3, r0 | r0 |
| `0x2b7cd8` | r0 | r0 |
| `0x2b7cdc` | — | pc |
| `0x2b7ce0` | r2, r8 | cpsr |

Observed branch/call/return-like instructions: **1**.

## What remains unproven

The argument passed to the callee, result in r0, global/heap memory access, external call side effects and conditional status after the BL are not inferred solely from a symbol name or six disassembled instructions. No full-function equivalence is claimed.
