# ARM entry-to-return / first-call boundary evidence

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Original ELF instructions and four PC-relative literals from `houkoku_okng(CTLINFO*)` are executed or verified. The early branch executes the actual POP return; other paths stop **before the first external BL**, at `0x25a298`.

- Conditional next global slot: `0x67b2f8`.

| Path | Test cases | Observed bounded behavior |
|---|---:|---|
| Early return | 1024 | Actual POP restores r3/r4/r5 and stack pointer, returns to synthetic caller |
| Field <= 0 | 512 | No object/flag write; continuation may zero a separate nonzero global slot |
| Field > 0 | 512 | Object field := 0, global flag |= 0x40; continuation may zero that slot |

**Verified entry-to-boundary microexecutions: 2048/2048 PASS.**
**Conditional continuation slot clears:** 512.

The emulator checks every executed opcode, exact state writes, saved/restored ARM registers, return address, conditional STRNE and neighboring memory canaries.

## Deliberate uncertainty

- The first BL is **not executed or stubbed**. Its inputs, return value and side effects remain unknown.
- State addresses and caller return address are controlled synthetic data; no actual application process was executed.
- No subsequent function-wide branches, later calls or error paths have been proven equivalent.
