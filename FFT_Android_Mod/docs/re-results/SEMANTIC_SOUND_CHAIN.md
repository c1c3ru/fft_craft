# sound_request — conservative ARM tail-branch chain

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Original executable ELF opcodes are followed only while each instruction is an unconditional ARM B with a direct target.

| PC | Opcode word | Direct destination |
|---|---|---|
| `0x26b374` | `0xeafead59` | `0x2168e0` |
| `0x2168e0` | `0xea016a8b` | `0x271314` |
| `0x271314` | `0xea010677` | `0x2b2cf8` |

Stop **before** `0x2b2cf8`: first non-B opcode: mov r1, r0.

**Sound tail-branch microexecutions: 10/10 PASS.**

## Verified scope and unknowns

- Only the direct-B trampoline opcodes are machine-executed; the boundary instruction is not run.
- Register r0, LR and initial NZCV, plus the absence of data reads and writes inside the trampoline, are tested.
- Actual sound playback, native APIs, system effects and the code past the boundary are **not proven**.
- Inputs and the return address are synthetic. No whole-function semantic equivalence is asserted.
