# Three callees and two caller continuations — original ARM execution

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

| Route | Microexecutions | Measured boundary |
|---|---:|---|
| iOS_setV2Icon direct | 24 | Indexed word written; idx=37 branches to unknown 0x2b8900 |
| iOS_clearOkNg direct | 8 | Sets index 49 to zero through original setter, returns via LR |
| sound_request direct | 24 | Unconditional branch to unresolved 0x2168e0, no local writes |
| houkoku_okng setter continuation | 8 | Object fields +8 and +0x14 set to 1, setter table index 52 set to 0, POP return |
| houkoku_okng clear/sound continuation | 8 | Table index 49 cleared, then sound_request branch boundary |

**Three-callee and caller tests: 72/72 PASS.**

Every test checks the actual instruction PC trace, real ARM BL/BX/B control flow, memory read/write hooks, adjacent word canaries, the stack, and a synthetic return address.

## Unknown / deferred contracts

- `sound_request(int)` only jumps to `0x2168e0`; that destination is not executed here. No sound effect has been proven.
- `iOS_setV2Icon` at index 37 stores a word then branches to `0x2b8900`; the target is not executed, so its later effects and return are unknown.
- Other callers, argument ranges, actual table contents, and aliasing remain unverified.
- Starting at caller branch entries does not validate the entire `houkoku_okng()` function or establish semantic equivalence.
- All registers, pointers and global table contents are synthetic test inputs; findings apply to these bounded machine paths only.
