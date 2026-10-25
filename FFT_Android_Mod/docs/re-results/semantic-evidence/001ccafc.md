# ARM evidence: `001ccafc` — get_floor_damage(BWORK*)

Static ARM-mode disassembly only. Reachability is heuristic; unvisited slots may be literal data. No semantic equivalence is proved.

- Binary address: `0x1ccafc`; size: 284 bytes
- Checkpoint status: `needs_review` (unchanged)
- Instruction set: ARM
- Scan method: ARM recursive descent (heuristic)
- Heuristically decoded instruction slots: 64/71
- Trailing bytes outside complete instructions: 0
- ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`
- Evidence schema: v2
- Unvisited 4-byte slots: 7 (not necessarily code)
- Unvisited slots referenced by PC-relative LDR: 7
- Other unvisited slots: 0
- Candidate memory stores: 6; true BL/BLX calls: 4
- Candidate local bitmask effects: 0
- Resolved ARM jump dispatches: 0; unresolved: 0

## Candidate dispatch destinations

None resolved by this pass.

## Potential memory writes (first 30)

- `0x001ccafc: push {r4, r5, r6, lr}`
- `0x001ccb50: strb ip, [r0, #1]`
- `0x001ccb60: str r5, [r1]`
- `0x001ccb68: str r3, [r6]`
- `0x001ccbd8: strb r2, [r3, #0x20]`
- `0x001ccbf4: strb r2, [r3, #0x27]`

## Candidate path-local bitmask effects

These sequences are instruction-local observations, not global postconditions, equivalence proofs, or executed traces.

None identified by conservative adjacent-instruction rules.

## Calls (first 30)

- `0x001ccb04: bl #0x1c88f8`
- `0x001ccb6c: bl #0x1cb064`
- `0x001ccb74: bl #0x1d2e6c`
- `0x001ccbdc: bl #0x1ca5a4`

## Candidate PC-relative literal words

A reference suggests data, not a proven classification; it may overlap code.

- `0x1ccbfc`: 0x0017b23c; referenced by 0x1ccb08
- `0x1ccc00`: 0xfffff618; referenced by 0x1ccb38
- `0x1ccc04`: 0xfffff610; referenced by 0x1ccb40
- `0x1ccc08`: 0xfffff61c; referenced by 0x1ccb48
- `0x1ccc0c`: 0xffffec3c; referenced by 0x1ccb78
- `0x1ccc10`: 0xfffff664; referenced by 0x1ccb7c
- `0x1ccc14`: 0xffffefac; referenced by 0x1ccba4

## Other unvisited instruction slots (first 40)

None

## Visited instructions (first 70)

```asm
0x001ccafc: push {r4, r5, r6, lr}
0x001ccb00: mov r5, r0
0x001ccb04: bl #0x1c88f8
0x001ccb08: ldr r4, [pc, #0xec]
0x001ccb0c: cmp r0, #0
0x001ccb10: ldrb r3, [r5, #0x1a4]
0x001ccb14: add r4, pc, r4
0x001ccb18: bne #0x1ccb9c
0x001ccb1c: tst r3, #0x40
0x001ccb20: bne #0x1ccb9c
0x001ccb24: tst r3, #0x80
0x001ccb28: bne #0x1ccba4
0x001ccb2c: ldrb r3, [r5, #0x63]
0x001ccb30: tst r3, #0x40
0x001ccb34: bne #0x1ccb9c
0x001ccb38: ldr r3, [pc, #0xc0]
0x001ccb3c: ldrb ip, [r5, #0x1ac]
0x001ccb40: ldr r1, [pc, #0xbc]
0x001ccb44: ldr r0, [r4, r3]
0x001ccb48: ldr r2, [pc, #0xb8]
0x001ccb4c: add r3, r5, #0x1ac
0x001ccb50: strb ip, [r0, #1]
0x001ccb54: ldr r1, [r4, r1]
0x001ccb58: add r3, r3, #2
0x001ccb5c: mov r0, r3
0x001ccb60: str r5, [r1]
0x001ccb64: ldr r6, [r4, r2]
0x001ccb68: str r3, [r6]
0x001ccb6c: bl #0x1cb064
0x001ccb70: mov r0, r5
0x001ccb74: bl #0x1d2e6c
0x001ccb78: ldr r2, [pc, #0x8c]
0x001ccb7c: ldr r3, [pc, #0x8c]
0x001ccb80: ldr r2, [r4, r2]
0x001ccb84: ldr r3, [r4, r3]
0x001ccb88: ldrb r2, [r2, r0, lsl #3]
0x001ccb8c: and r2, r2, #0x3f
0x001ccb90: ldrsb r3, [r3, r2]
0x001ccb94: cmp r3, #0
0x001ccb98: blt #0x1ccbcc
0x001ccb9c: mov r0, #0
0x001ccba0: pop {r4, r5, r6, pc}
0x001ccba4: ldr r1, [pc, #0x68]
0x001ccba8: mov r2, #0x1e4
0x001ccbac: and r3, r3, #0x1f
0x001ccbb0: ldr r1, [r4, r1]
0x001ccbb4: add r2, r2, #2
0x001ccbb8: mla r2, r3, r2, r1
0x001ccbbc: ldrb r3, [r2, #0x63]
0x001ccbc0: tst r3, #0x40
0x001ccbc4: beq #0x1ccb38
0x001ccbc8: b #0x1ccb9c
0x001ccbcc: ldr r3, [r6]
0x001ccbd0: mvn r2, #0x7f
0x001ccbd4: mov r0, #0
0x001ccbd8: strb r2, [r3, #0x20]
0x001ccbdc: bl #0x1ca5a4
0x001ccbe0: cmp r0, #0
0x001ccbe4: beq #0x1ccb9c
0x001ccbe8: ldr r3, [r6]
0x001ccbec: mov r2, #8
0x001ccbf0: mov r0, #1
0x001ccbf4: strb r2, [r3, #0x27]
0x001ccbf8: pop {r4, r5, r6, pc}
```

## Still required for semantic validation

- Verify control-flow paths, input/output invariants and memory side effects.
- Compare return values and state changes against a specification or executable reference.
- Perform differential tests or execution traces before marking semantic equivalence.
