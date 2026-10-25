# ARM evidence: `000bceac` — CSOUND_LOADER_PCM::CSOUND_LOADER_PCM()

Static ARM-mode disassembly only. Reachability is heuristic; unvisited slots may be literal data. No semantic equivalence is proved.

- Binary address: `0xbceac`; size: 40 bytes
- Checkpoint status: `needs_review` (unchanged)
- Instruction set: ARM
- Scan method: ARM recursive descent (heuristic)
- Heuristically decoded instruction slots: 9/10
- Trailing bytes outside complete instructions: 0
- ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`
- Evidence schema: v2
- Unvisited 4-byte slots: 1 (not necessarily code)
- Unvisited slots referenced by PC-relative LDR: 1
- Other unvisited slots: 0
- Candidate memory stores: 4; true BL/BLX calls: 0
- Candidate local bitmask effects: 0
- Resolved ARM jump dispatches: 0; unresolved: 0

## Candidate dispatch destinations

None resolved by this pass.

## Potential memory writes (first 30)

- `0x000bceb4: str r2, [r0, #8]`
- `0x000bcec0: str r1, [r0]`
- `0x000bcec4: str r2, [r0, #0xc]`
- `0x000bcec8: strb r2, [r0, #0x20]`

## Candidate path-local bitmask effects

These sequences are instruction-local observations, not global postconditions, equivalence proofs, or executed traces.

None identified by conservative adjacent-instruction rules.

## Calls (first 30)

None identified.

## Candidate PC-relative literal words

A reference suggests data, not a proven classification; it may overlap code.

- `0xbced0`: 0x0028926c; referenced by 0xbceac

## Other unvisited instruction slots (first 40)

None

## Visited instructions (first 70)

```asm
0x000bceac: ldr r1, [pc, #0x1c]
0x000bceb0: mov r2, #0
0x000bceb4: str r2, [r0, #8]
0x000bceb8: ldr r1, [pc, r1]
0x000bcebc: add r1, r1, #8
0x000bcec0: str r1, [r0]
0x000bcec4: str r2, [r0, #0xc]
0x000bcec8: strb r2, [r0, #0x20]
0x000bcecc: bx lr
```

## Still required for semantic validation

- Verify control-flow paths, input/output invariants and memory side effects.
- Compare return values and state changes against a specification or executable reference.
- Perform differential tests or execution traces before marking semantic equivalence.
