# ARM function entry and state-transition microexecution

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Execution starts at the **original function entry** `0x25a228` and stops before the first unresolved return `0x25a2f4` or continuation `0x25a27c`. Original PC-relative literal words and instructions are checked before emulation.

- Computed PC-relative global anchor: `0x347d58`.
- Indexed status pointer slot: `0x3479b0`.
- Global bitmask pointer slot: `0x3479cc`.

| Path | Condition | Cases | State writes (excluding ARM stack prologue) |
|---|---|---:|---|
| Early BNE | status & 0x100 != 0 | 512 | None |
| BLE exit | bit clear, signed field <= 0 | 256 | None |
| State transition | bit clear, signed field > 0 | 256 | object field := 0; global flag |= 0x40 |

**Function-entry bounded micro-executions: 1024/1024 PASS.**

Verified status index multiplied by 0x38, PC-relative pointer derivations, all instruction addresses, register-save stack writes, object/global transitions and adjacent-memory canaries.

## Evidence boundaries

- This is **not a whole-function test**: both exit instructions and all later branches, calls and returns remain unexecuted.
- Registers, object state and global pointer slots are synthetic test inputs; no actual caller or real process state was modeled.
- Other array indices and pointer aliases may have different effects.
- No semantic equivalence of the complete function is asserted.
