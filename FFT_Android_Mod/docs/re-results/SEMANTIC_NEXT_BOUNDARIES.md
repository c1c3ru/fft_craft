# ARM next-boundary inspection — sound and icon

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

These are file-backed ARM **linear decoding candidates**, not a demonstrated control-flow graph, dynamic executions or verified memory effects. Embedded data may be decoded as instructions.

## SysSE_Play(int,int) at `0x2b2b7c`

| PC | ELF word | Decoded ARM candidate | Operand hints |
|---|---|---|---|
| `0x2b2b7c` | `0xe92d47f0` | `push {r4, r5, r6, r7, r8, sb, sl, lr}` | — |
| `0x2b2b80` | `0xe59f3160` | `ldr r3, [pc, #0x160]` | memory through `pc` (disp=352) |
| `0x2b2b84` | `0xe24dd020` | `sub sp, sp, #0x20` | — |
| `0x2b2b88` | `0xe1a06000` | `mov r6, r0` | — |
| `0x2b2b8c` | `0xe1a05001` | `mov r5, r1` | — |
| `0x2b2b90` | `0xe79f0003` | `ldr r0, [pc, r3]` | memory through `pc` (disp=0) |
| `0x2b2b94` | `0xe3a01028` | `mov r1, #0x28` | — |
| `0x2b2b98` | `0xebff65e0` | `bl #0x28c320` | transfer to `0x28c320` |
| `0x2b2b9c` | `0xe3500000` | `cmp r0, #0` | — |
| `0x2b2ba0` | `0x0a000006` | `beq #0x2b2bc0` | transfer to `0x2b2bc0` |
| `0x2b2ba4` | `0xe2554001` | `subs r4, r5, #1` | — |
| `0x2b2ba8` | `0x3a000006` | `blo #0x2b2bc8` | transfer to `0x2b2bc8` |
| `0x2b2bac` | `0xeb003115` | `bl #0x2bf008` | transfer to `0x2bf008` |
| `0x2b2bb0` | `0xe2507000` | `subs r7, r0, #0` | — |
| `0x2b2bb4` | `0x1a000001` | `bne #0x2b2bc0` | transfer to `0x2b2bc0` |
| `0x2b2bb8` | `0xe3540fa7` | `cmp r4, #0x29c` | — |
| `0x2b2bbc` | `0x3a000005` | `blo #0x2b2bd8` | transfer to `0x2b2bd8` |
| `0x2b2bc0` | `0xe28dd020` | `add sp, sp, #0x20` | — |
| `0x2b2bc4` | `0xe8bd87f0` | `pop {r4, r5, r6, r7, r8, sb, sl, pc}` | — |
| `0x2b2bc8` | `0xe1a00006` | `mov r0, r6` | — |
| `0x2b2bcc` | `0xe28dd020` | `add sp, sp, #0x20` | — |
| `0x2b2bd0` | `0xe8bd47f0` | `pop {r4, r5, r6, r7, r8, sb, sl, lr}` | — |
| `0x2b2bd4` | `0xeaffffd7` | `b #0x2b2b38` | transfer to `0x2b2b38` |
| `0x2b2bd8` | `0xe59f310c` | `ldr r3, [pc, #0x10c]` | memory through `pc` (disp=268) |

## iOS_SetIconPosition() after prologue at `0x2b8928`

| PC | ELF word | Decoded ARM candidate | Operand hints |
|---|---|---|---|
| `0x2b8928` | `0xe7925003` | `ldr r5, [r2, r3]` | memory through `r2` (disp=0) |
| `0x2b892c` | `0xe08fa00a` | `add sl, pc, sl` | — |
| `0x2b8930` | `0xe24aad3a` | `sub sl, sl, #0xe80` | — |
| `0x2b8934` | `0xe1a00005` | `mov r0, r5` | — |
| `0x2b8938` | `0xebf7b97a` | `bl #0xa6f28` | transfer to `0xa6f28` |
| `0x2b893c` | `0xe28d2018` | `add r2, sp, #0x18` | — |
| `0x2b8940` | `0xe1a00005` | `mov r0, r5` | — |
| `0x2b8944` | `0xe28d1014` | `add r1, sp, #0x14` | — |
| `0x2b8948` | `0xebf7b9b9` | `bl #0xa7034` | transfer to `0xa7034` |
| `0x2b894c` | `0xe59f3fc0` | `ldr r3, [pc, #0xfc0]` | memory through `pc` (disp=4032) |
| `0x2b8950` | `0xe59d200c` | `ldr r2, [sp, #0xc]` | memory through `sp` (disp=12) |
| `0x2b8954` | `0xe08f9009` | `add sb, pc, sb` | — |
| `0x2b8958` | `0xe24a7006` | `sub r7, sl, #6` | — |
| `0x2b895c` | `0xe28a80da` | `add r8, sl, #0xda` | — |
| `0x2b8960` | `0xe28aa012` | `add sl, sl, #0x12` | — |
| `0x2b8964` | `0xe7926003` | `ldr r6, [r2, r3]` | memory through `r2` (disp=0) |
| `0x2b8968` | `0xe28990a4` | `add sb, sb, #0xa4` | — |
| `0x2b896c` | `0xe58da008` | `str sl, [sp, #8]` | memory through `sp` (disp=8) |
| `0x2b8970` | `0xe3a0001a` | `mov r0, #0x1a` | — |
| `0x2b8974` | `0xe1d640b0` | `ldrh r4, [r6]` | memory through `r6` (disp=0) |
| `0x2b8978` | `0xebffe638` | `bl #0x2b2260` | transfer to `0x2b2260` |
| `0x2b897c` | `0xe1a01000` | `mov r1, r0` | — |
| `0x2b8980` | `0xe1a00005` | `mov r0, r5` | — |
| `0x2b8984` | `0xebf7b988` | `bl #0xa6fac` | transfer to `0xa6fac` |

## Safety constraints for next step

- Only test verified entry-to-boundary instruction sequences.
- Model each indirect pointer and adjacent canary explicitly.
- Stop before an unmodeled BL, indirect branch or side effect.
- Do not claim complete-function semantic equivalence.
