# First-level ARM call contracts: GetParam / GetScale

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Original executable ELF words are **linearly decoded**; a trailing word may be literal data even if Capstone gives it a mnemonic. No runtime call results or function-wide equivalence are asserted.

## CFFT_STATE::GetParam(int)

- Callsite: `0x2b2b98` (verified ARM BL).
- ELF span: `0x28c320`, 12 bytes.

| Word address | Raw ELF word | Linear ARM decoding | Memory/flow hints |
|---|---|---|---|
| `0x28c320` | `0xe281100e` | `add r1, r1, #0xe` | — |
| `0x28c324` | `0xe7900101` | `ldr r0, [r0, r1, lsl #2]` | mem via r0 displacement 0 |
| `0x28c328` | `0xe12fff1e` | `bx lr` | candidate control transfer |

Reachability and literal-vs-code classification require a separate control-flow check.

## CGX_SCREEN_CORRECT::GetScale(float*)

- Callsite: `0x2b8938` (verified ARM BL).
- ELF span: `0xa6f28`, 16 bytes.

| Word address | Raw ELF word | Linear ARM decoding | Memory/flow hints |
|---|---|---|---|
| `0xa6f28` | `0xe3510000` | `cmp r1, #0` | — |
| `0xa6f2c` | `0x15903004` | `ldrne r3, [r0, #4]` | mem via r0 displacement 4 |
| `0xa6f30` | `0x15813000` | `strne r3, [r1]` | mem via r1 displacement 0 |
| `0xa6f34` | `0xe12fff1e` | `bx lr` | candidate control transfer |

Reachability and literal-vs-code classification require a separate control-flow check.

## Next reproducible step

Verify exact opcode signatures and original PC-relative data. Emulate locally bounded inputs with Unicorn, checking reads, writes, registers, original return PC, memory neighbors and call boundaries.
Stop before indirect or external callees not yet modeled.

**Not proven:** true application state, pointer validity, actual sound output, UI placement, or complete semantic equivalence.
