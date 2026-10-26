# ARM callee: iOS_getV2Icon — verified instruction/data split

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Caller: `0x25a298`: `bl #0x2b7ccc`.
Callee: `0x2b7ccc`, 24 bytes, `iOS_getV2Icon(V2ICON_DATA)`.

## Five executable ARM instructions

| Address | Instruction |
|---|---|
| `0x2b7ccc` | `ldr r3, [pc, #0xc]` |
| `0x2b7cd0` | `add r3, pc, r3` |
| `0x2b7cd4` | `add r0, r3, r0, lsl #2` |
| `0x2b7cd8` | `ldr r0, [r0, #0xd04]` |
| `0x2b7cdc` | `bx lr` |

## One PC-relative literal (data, not an executable opcode)

- Literal at `0x2b7ce0`: `0x01723fa8`.
- Indexed data address for argument `r0 = 0`: `0x19dc984`.
- The final 4-byte word must not be counted as a sixth ARM instruction simply because it decodes as one.

## Register accesses for five ARM instructions

| Address | Read registers | Written registers |
|---|---|---|
| `0x2b7ccc` | pc | r3 |
| `0x2b7cd0` | pc, r3 | r3 |
| `0x2b7cd4` | r3, r0 | r0 |
| `0x2b7cd8` | r0 | r0 |
| `0x2b7cdc` | — | pc |

The code calculates a PC-relative base, adds `r0 * 4`, loads a word at an additional `0xd04` displacement, and returns via `BX LR`. No store instruction is present.

## Evidence boundary

The actual table contents, valid index bounds, aliasing, caller argument provenance and complete function behavior are not established by disassembly. No semantic equivalence claimed.
