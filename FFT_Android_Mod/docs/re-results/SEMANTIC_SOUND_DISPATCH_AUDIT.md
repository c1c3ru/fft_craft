# Original ARM boundaries — sound dispatcher and icon positioning

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

This report is a **static audit**, not a behavioral or equivalence claim. Linear disassembly can decode embedded data as code.

## Verified sound trampoline

| Address | Target |
|---|---|
| `0x26b374` | `0x2168e0` |
| `0x2168e0` | `0x271314` |
| `0x271314` | `0x2b2cf8` |

Stops at `0x2b2cf8`: first non-B opcode: mov r1, r0.

## SysSE_PlayDef(int) — 12-byte symbol

| Address | ELF word | ARM decoding | Observable operand category |
|---|---|---|---|
| `0x2b2cf8` | `0xe1a01000` | `mov r1, r0` | — |
| `0x2b2cfc` | `0xe3a00000` | `mov r0, #0` | — |
| `0x2b2d00` | `0xeaffff9d` | `b #0x2b2b7c` | direct branch/call 0x2b2b7c |

## Following 32 bytes, not assumed part of SysSE_PlayDef

| Address | ELF word | ARM decoding | Observable operand category |
|---|---|---|---|
| `0x2b2d04` | `0xe1a01000` | `mov r1, r0` | — |
| `0x2b2d08` | `0xe3a00001` | `mov r0, #1` | — |
| `0x2b2d0c` | `0xeaffff9a` | `b #0x2b2b7c` | direct branch/call 0x2b2b7c |
| `0x2b2d10` | `0xe92d43f0` | `push {r4, r5, r6, r7, r8, sb, lr}` | — |
| `0x2b2d14` | `0xe59f3118` | `ldr r3, [pc, #0x118]` | memory base pc displacement 280 |
| `0x2b2d18` | `0xe24dd024` | `sub sp, sp, #0x24` | — |
| `0x2b2d1c` | `0xe1a04000` | `mov r4, r0` | — |
| `0x2b2d20` | `0xe3a01028` | `mov r1, #0x28` | — |

## iOS_SetIconPosition() — first 96 bytes only

| Address | ELF word | ARM decoding | Observable operand category |
|---|---|---|---|
| `0x2b8900` | `0xe92d4ff0` | `push {r4, r5, r6, r7, r8, sb, sl, fp, lr}` | — |
| `0x2b8904` | `0xe59f3ff8` | `ldr r3, [pc, #0xff8]` | memory base pc displacement 4088 |
| `0x2b8908` | `0xe24dd024` | `sub sp, sp, #0x24` | — |
| `0x2b890c` | `0xe59faff4` | `ldr sl, [pc, #0xff4]` | memory base pc displacement 4084 |
| `0x2b8910` | `0xe08f3003` | `add r3, pc, r3` | — |
| `0x2b8914` | `0xe58d300c` | `str r3, [sp, #0xc]` | memory base sp displacement 12 |
| `0x2b8918` | `0xe59d200c` | `ldr r2, [sp, #0xc]` | memory base sp displacement 12 |
| `0x2b891c` | `0xe59f3fe8` | `ldr r3, [pc, #0xfe8]` | memory base pc displacement 4072 |
| `0x2b8920` | `0xe28d101c` | `add r1, sp, #0x1c` | — |
| `0x2b8924` | `0xe59f9fe4` | `ldr sb, [pc, #0xfe4]` | memory base pc displacement 4068 |
| `0x2b8928` | `0xe7925003` | `ldr r5, [r2, r3]` | memory base r2 displacement 0 |
| `0x2b892c` | `0xe08fa00a` | `add sl, pc, sl` | — |
| `0x2b8930` | `0xe24aad3a` | `sub sl, sl, #0xe80` | — |
| `0x2b8934` | `0xe1a00005` | `mov r0, r5` | — |
| `0x2b8938` | `0xebf7b97a` | `bl #0xa6f28` | direct branch/call 0xa6f28 |
| `0x2b893c` | `0xe28d2018` | `add r2, sp, #0x18` | — |
| `0x2b8940` | `0xe1a00005` | `mov r0, r5` | — |
| `0x2b8944` | `0xe28d1014` | `add r1, sp, #0x14` | — |
| `0x2b8948` | `0xebf7b9b9` | `bl #0xa7034` | direct branch/call 0xa7034 |
| `0x2b894c` | `0xe59f3fc0` | `ldr r3, [pc, #0xfc0]` | memory base pc displacement 4032 |
| `0x2b8950` | `0xe59d200c` | `ldr r2, [sp, #0xc]` | memory base sp displacement 12 |
| `0x2b8954` | `0xe08f9009` | `add sb, pc, sb` | — |
| `0x2b8958` | `0xe24a7006` | `sub r7, sl, #6` | — |
| `0x2b895c` | `0xe28a80da` | `add r8, sl, #0xda` | — |

## Next verification gate

Only emulate paths after checking direct and indirect transfers, stack setup and memory operands. Do not execute unresolved callees or branch targets. Do not classify a whole function by its entry prefix.

A bounded instruction sequence may be correct under controlled inputs without proving complete function behavior, runtime effects, or semantic equivalence.
