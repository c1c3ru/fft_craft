# Guarded ARM state-write microexecution

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Original ARM code and its PC-relative literal are verified before execution. The emulator begins **mid-function** at `0x25a25c` and stops **before** `0x25a27c`; no surrounding calls or whole-function effects are modeled.

| Path | Condition (signed r2) | State update |
|---|---|---|
| BLE taken | r2 <= 0 | no writes to either controlled field |
| BLE not taken | r2 > 0 | object field := entry r3; global flag |= 0x40 |

**Guarded block micro-executions:** 256/256 PASS.
**Write-active executions:** 144; **no-write executions:** 112.

## Boundaries

- Pointer slots, memory and registers are artificial controlled inputs.
- Executed exactly the original 8 ARM opcodes on the fallthrough path or CMP/BLE on the taken path, with two initial NZCV seeds.
- Both adjacent memory words were checked for unexpected modifications.
- The preceding path that initializes these registers was not executed.
- No guarantee that a live call reaches either path, no callee effects, and no functional equivalence established. Status remains `needs_review`.
