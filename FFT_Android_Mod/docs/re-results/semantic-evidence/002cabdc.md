# ARM evidence: `002cabdc` — __aeabi_ul2d

Static ARM-mode disassembly only. Reachability is heuristic; unvisited slots may be literal data. No semantic equivalence is proved.

- Binary address: `0x2cabdc`; size: 116 bytes
- Checkpoint status: `needs_review` (unchanged)
- Instruction set: ARM
- Scan method: ARM recursive descent (heuristic)
- Heuristically decoded instruction slots: 22/29
- Trailing bytes outside complete instructions: 0
- ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`
- Evidence schema: v2
- Unvisited 4-byte slots: 7 (not necessarily code)
- Unvisited slots referenced by PC-relative LDR: 0
- Other unvisited slots: 7
- Candidate memory stores: 1; true BL/BLX calls: 0
- Candidate local bitmask effects: 0
- Resolved ARM jump dispatches: 0; unresolved: 0

## Candidate dispatch destinations

None resolved by this pass.

## Potential memory writes (first 30)

- `0x002cabe4: push {r4, r5, lr}`

## Candidate path-local bitmask effects

These sequences are instruction-local observations, not global postconditions, equivalence proofs, or executed traces.

None identified by conservative adjacent-instruction rules.

## Calls (first 30)

None identified.

## Candidate PC-relative literal words

A reference suggests data, not a proven classification; it may overlap code.

None identified.

## Other unvisited instruction slots (first 40)

`0x2cabf0`, `0x2cabf4`, `0x2cabf8`, `0x2cabfc`, `0x2cac00`, `0x2cac04`, `0x2cac08`

## Visited instructions (first 70)

```asm
0x002cabdc: orrs r2, r0, r1
0x002cabe0: bxeq lr
0x002cabe4: push {r4, r5, lr}
0x002cabe8: mov r5, #0
0x002cabec: b #0x2cac0c
0x002cac0c: mov r4, #0x400
0x002cac10: add r4, r4, #0x32
0x002cac14: lsrs ip, r1, #0x16
0x002cac18: beq #0x2ca990
0x002cac1c: mov r2, #3
0x002cac20: lsrs ip, ip, #3
0x002cac24: addne r2, r2, #3
0x002cac28: lsrs ip, ip, #3
0x002cac2c: addne r2, r2, #3
0x002cac30: add r2, r2, ip, lsr #3
0x002cac34: rsb r3, r2, #0x20
0x002cac38: lsl ip, r0, r3
0x002cac3c: lsr r0, r0, r2
0x002cac40: orr r0, r0, r1, lsl r3
0x002cac44: lsr r1, r1, r2
0x002cac48: add r4, r4, r2
0x002cac4c: b #0x2ca990
```

## Still required for semantic validation

- Verify control-flow paths, input/output invariants and memory side effects.
- Compare return values and state changes against a specification or executable reference.
- Perform differential tests or execution traces before marking semantic equivalence.
