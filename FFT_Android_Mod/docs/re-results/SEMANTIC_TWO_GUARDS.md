# Two consecutive ARM guards — bounded machine execution

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Uses actual ARM instructions and a PC-relative literal from `houkoku_okng(CTLINFO*)`, beginning **mid-function** at `0x25a24c`. Only this bounded slice is executed, with synthetic registers, pointers, status and memory.

| Guarded path | Preconditions | Memory writes | Test cases |
|---|---|---|---:|
| Early BNE to `0x25a2f4` | status & 0x100 != 0 | None | 128 |
| BLE to `0x25a27c` | status & 0x100 == 0 and signed control <= 0 | None | 64 |
| Fallthrough | status & 0x100 == 0 and signed control > 0 | Object field := 0; global flag |= 0x40 | 64 |

**Two-guard machine executions: 256/256 PASS.**

Checks every instruction address on the bounded path, exact writes, status-slot immutability, adjacent memory canaries and object/table pointers.

## Limitations

- The statuses, field values and pointers were synthesized for testing.
- No predecessor path, live caller or subsequent exit instruction was executed.
- The early branch target and normal continuation are not executed.
- This does not prove whole-function reachability, behavior of callees or semantic equivalence. Structural status is independent of semantic approval.
