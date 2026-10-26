# GetParam/GetScale — next caller branches and arguments

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Original ARM BL/callee/BX LR and following caller instructions are microexecuted with synthetic table, object and stack state. The next unresolved calls or return blocks are **not executed**.

| Boundary reached | Sampled paths | Contract before boundary |
|---|---:|---|
| sound: `0x2b2bc0` | 6 | GetParam returns zero; BEQ selects early exit block |
| sound: `0x2b2bc8` | 6 | Nonzero parameter with r5=0; SUBS/BLO selects the alternate branch |
| sound: `0x2b2bac` | 12 | Nonzero parameter and r5>=1; next BL 0x2bf008 not executed |
| icon: `0x2b8948` | 8 | GetScale copied synthetic 32-bit word to SP+0x1c; next call r0=source, r1=SP+0x14, r2=SP+0x18 |

**Post-getter ARM microexecutions: 32/32 PASS.**

Every sample checks the actual instruction PC path, return address, memory reads/writes and neighboring word canaries.

## Limitations

- The table, pointed-to object and stack are controlled synthetic inputs.
- `SysSE_Play` exit blocks and its next BL are not executed.
- The next `iOS_SetIconPosition` BL at `0x2b8948` is not executed.
- No sound output, UI placement or whole-function equivalence is proven.
