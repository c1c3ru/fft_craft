# Three real ARM callees — initial machine-code audit

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Static instruction decoding alone does not establish reachability, effects of calls, ABI postconditions or equivalence.

## iOS_setV2Icon(V2ICON_DATA, int)

- Callsite: `0x25a2bc` — `bl #0x2b9cac`
- Candidate span: `0x2b9cac` through `0x2b9cc8` (32 bytes).

| Address | Original word | ARM decoding | Memory / flow observations |
|---|---|---|---|
| `0x2b9cac` | `0xe59f3014` | `ldr r3, [pc, #0x14]` | mem[pc,disp=20]; PC-relative literal at 0x2b9cc8 |
| `0x2b9cb0` | `0xe3500025` | `cmp r0, #0x25` | — |
| `0x2b9cb4` | `0xe08f3003` | `add r3, pc, r3` | — |
| `0x2b9cb8` | `0xe0830100` | `add r0, r3, r0, lsl #2` | — |
| `0x2b9cbc` | `0xe5801d04` | `str r1, [r0, #0xd04]` | mem[r0,disp=3332] |
| `0x2b9cc0` | `0x112fff1e` | `bxne lr` | control-flow candidate |
| `0x2b9cc4` | `0xeafffb0d` | `b #0x2b8900` | control-flow candidate |
| `0x2b9cc8` | `0x01721fc4` | `cmneq r2, r4, asr #31` | — |

Decoded entries can include embedded data after a return; the next phase must distinguish reachable code from literals and dynamically check memory reads/writes.

## sound_request(int)

- Callsite: `0x25a310` — `bl #0x26b374`
- Candidate span: `0x26b374` through `0x26b374` (4 bytes).

| Address | Original word | ARM decoding | Memory / flow observations |
|---|---|---|---|
| `0x26b374` | `0xeafead59` | `b #0x2168e0` | control-flow candidate |

Decoded entries can include embedded data after a return; the next phase must distinguish reachable code from literals and dynamically check memory reads/writes.

## iOS_clearOkNg()

- Callsite: `0x25a328` — `bl #0x282268`
- Candidate span: `0x282268` through `0x282270` (12 bytes).

| Address | Original word | ARM decoding | Memory / flow observations |
|---|---|---|---|
| `0x282268` | `0xe3a00031` | `mov r0, #0x31` | — |
| `0x28226c` | `0xe3a01000` | `mov r1, #0` | — |
| `0x282270` | `0xea00de8d` | `b #0x2b9cac` | control-flow candidate |

Decoded entries can include embedded data after a return; the next phase must distinguish reachable code from literals and dynamically check memory reads/writes.

## Planned bounded tests

Emulate each callee with controlled registers and memory. Verify the exact PC trace, link register, returns, read/write addresses, neighboring canaries and unresolved branch/call destinations. Compose only effects actually established by individual tests into the caller.

## Limitations

No full-function semantic equivalence, real runtime global state, caller effects or legitimate argument domains proven.
