# Priority ARM conditional-path contracts

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

These are locally observed CMP/TST -> conditional branch edges; they are not dominance claims, execution traces, complete path constraints or proof of semantic equivalence.

## `0028179c` — iOS_v2menuSetType(V2MENU_TYPE)

Observed direct compare/branch pairs: **2**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **128**; unmodeled outgoing edges/transfers: **0**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x281830` cmp r3, r4; `0x281834` bne #0x281810 | r3 != r4 → `0x281810` | r3 == r4 → `0x281838` |
| `0x281858` cmp r3, r2; `0x28185c` bne #0x281850 | r3 != r2 → `0x281850` | r3 == r2 → `0x281860` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `00244200` — vEnd_rollproc()

Observed direct compare/branch pairs: **3**; local bitmask sequences: **2**.

Modeled ARM CFG nodes: **121**; unmodeled outgoing edges/transfers: **0**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x2442c8` cmp r2, #0x2b; `0x2442cc` bgt #0x2443c8 | r2 > (signed) 0x2b → `0x2443c8` | r2 <= (signed) 0x2b → `0x2442d0` |
| `0x24430c` cmp r3, #0x100; `0x244310` beq #0x24438c | r3 == 0x100 → `0x24438c` | r3 != 0x100 → `0x244314` |
| `0x244380` cmp r3, #0x100; `0x244384` bne #0x2442e0 | r3 != 0x100 → `0x2442e0` | r3 == 0x100 → `0x244388` |

### Local memory-bit effects and direct incoming edges

- Candidate clears `0x40` at `[r4]`; sequence: `0x244254`, `0x244258`, `0x24425c`.
  - No direct CMP/TST-branch incoming edge demonstrated; entry condition remains unknown.
  - Modeled direct predecessors: `0x244250` (fallthrough).
  - Branch `0x244310` after compare `0x24430c`: [r3 == 0x100] → no route found in modeled graph; [r3 != 0x100] → 0x244314 → 0x244318 → 0x24431c → 0x244320 → 0x244324 → 0x244328 → 0x24432c → .... Only one modeled successor reaches the write; NOT a dominance or impossibility proof.
- Candidate clears `0x40` at `[r4]`; sequence: `0x2443b8`, `0x2443bc`, `0x2443c0`.
  - No direct CMP/TST-branch incoming edge demonstrated; entry condition remains unknown.
  - Modeled direct predecessors: `0x2443b4` (fallthrough).
  - Branch `0x244310` after compare `0x24430c`: [r3 == 0x100] → 0x24438c → 0x244390 → 0x244394 → 0x244398 → 0x24439c → 0x2443a0 → 0x2443a4 → ...; [r3 != 0x100] → no route found in modeled graph. Only one modeled successor reaches the write; NOT a dominance or impossibility proof.

## `000df864` — event_status_set(unsigned short, unsigned short)

Observed direct compare/branch pairs: **11**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **122**; unmodeled outgoing edges/transfers: **0**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0xdf8a8` cmp sb, #0; `0xdf8ac` beq #0xdf8b8 | sb == 0x0 → `0xdf8b8` | sb != 0x0 → `0xdf8b0` |
| `0xdf8cc` cmp r0, #0; `0xdf8d0` beq #0xdf8b0 | r0 == 0x0 → `0xdf8b0` | r0 != 0x0 → `0xdf8d4` |
| `0xdf91c` cmp r0, #0; `0xdf920` beq #0xdf8f8 | r0 == 0x0 → `0xdf8f8` | r0 != 0x0 → `0xdf924` |
| `0xdf94c` cmp r3, #0; `0xdf950` blt #0xdf970 | r3 < (signed) 0x0 → `0xdf970` | r3 >= (signed) 0x0 → `0xdf954` |
| `0xdf954` cmp r8, #0; `0xdf958` bne #0xdf9d4 | r8 != 0x0 → `0xdf9d4` | r8 == 0x0 → `0xdf95c` |
| `0xdf968` cmp r3, #0; `0xdf96c` beq #0xdf9e4 | r3 == 0x0 → `0xdf9e4` | r3 != 0x0 → `0xdf970` |
| `0xdf974` cmp r3, #0; `0xdf978` bne #0xdf8f8 | r3 != 0x0 → `0xdf8f8` | r3 == 0x0 → `0xdf97c` |
| `0xdf990` cmp r3, #0; `0xdf994` bne #0xdfa28 | r3 != 0x0 → `0xdfa28` | r3 == 0x0 → `0xdf998` |
| `0xdf998` cmp r8, #0; `0xdf99c` bne #0xdf8b0 | r8 != 0x0 → `0xdf8b0` | r8 == 0x0 → `0xdf9a0` |
| `0xdf9ec` cmp r0, #0; `0xdf9f0` beq #0xdf970 | r0 == 0x0 → `0xdf970` | r0 != 0x0 → `0xdf9f4` |
| `0xdfa38` tst r3, #1; `0xdfa3c` beq #0xdf998 | (r3 & 0x1) == 0 → `0xdf998` | (r3 & 0x1) != 0 → `0xdfa40` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `0025a228` — houkoku_okng(CTLINFO*)

Observed direct compare/branch pairs: **6**; local bitmask sequences: **1**.

Modeled ARM CFG nodes: **119**; unmodeled outgoing edges/transfers: **2**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x25a25c` cmp r2, #0; `0x25a260` ble #0x25a27c | r2 <= (signed) 0x0 → `0x25a27c` | r2 > (signed) 0x0 → `0x25a264` |
| `0x25a29c` cmp r0, #1; `0x25a2a0` beq #0x25a2c8 | r0 == 0x1 → `0x25a2c8` | r0 != 0x1 → `0x25a2a4` |
| `0x25a2a4` cmp r0, #2; `0x25a2a8` bne #0x25a2f8 | r0 != 0x2 → `0x25a2f8` | r0 == 0x2 → `0x25a2ac` |
| `0x25a2ec` tst r3, #0x20; `0x25a2f0` bne #0x25a328 | (r3 & 0x20) != 0 → `0x25a328` | (r3 & 0x20) == 0 → `0x25a2f4` |
| `0x25a304` tst r3, #0x40; `0x25a308` beq #0x25a2ec | (r3 & 0x40) == 0 → `0x25a2ec` | (r3 & 0x40) != 0 → `0x25a30c` |
| `0x25a338` cmp r1, #0; `0x25a33c` beq #0x25a3a4 | r1 == 0x0 → `0x25a3a4` | r1 != 0x0 → `0x25a340` |

### Local memory-bit effects and direct incoming edges

- Candidate sets `0x40` at `[r3]`; sequence: `0x25a270`, `0x25a274`, `0x25a278`.
  - No direct CMP/TST-branch incoming edge demonstrated; entry condition remains unknown.
  - Modeled direct predecessors: `0x25a26c` (fallthrough).
  - Branch `0x25a260` after compare `0x25a25c`: [r2 <= (signed) 0x0] → no route found in modeled graph; [r2 > (signed) 0x0] → 0x25a264 → 0x25a268 → 0x25a26c → 0x25a270. Only one modeled successor reaches the write; NOT a dominance or impossibility proof.

## `002b2448` — EnvSE_Play(int)

Observed direct compare/branch pairs: **1**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **98**; unmodeled outgoing edges/transfers: **1**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x2b2464` cmp r0, #0; `0x2b2468` beq #0x2b25a0 | r0 == 0x0 → `0x2b25a0` | r0 != 0x0 → `0x2b246c` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `0028bb88` — TE_asmTaskEntry(int)

Observed direct compare/branch pairs: **10**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **115**; unmodeled outgoing edges/transfers: **0**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x28bbfc` cmp r4, #0; `0x28bc00` beq #0x28bd24 | r4 == 0x0 → `0x28bd24` | r4 != 0x0 → `0x28bc04` |
| `0x28bc44` cmp r3, #0; `0x28bc48` beq #0x28bc1c | r3 == 0x0 → `0x28bc1c` | r3 != 0x0 → `0x28bc4c` |
| `0x28bc4c` cmp r4, r3; `0x28bc50` bne #0x28bc1c | r4 != r3 → `0x28bc1c` | r4 == r3 → `0x28bc54` |
| `0x28bc5c` cmp r3, r2; `0x28bc60` bne #0x28bc1c | r3 != r2 → `0x28bc1c` | r3 == r2 → `0x28bc64` |
| `0x28bc74` cmp r0, #0; `0x28bc78` beq #0x28bc1c | r0 == 0x0 → `0x28bc1c` | r0 != 0x0 → `0x28bc7c` |
| `0x28bcb8` cmp r0, #0; `0x28bcbc` bne #0x28bd10 | r0 != 0x0 → `0x28bd10` | r0 == 0x0 → `0x28bcc0` |
| `0x28bcc8` cmp r0, #0; `0x28bccc` bne #0x28bc7c | r0 != 0x0 → `0x28bc7c` | r0 == 0x0 → `0x28bcd0` |
| `0x28bcd8` cmp r3, #0; `0x28bcdc` beq #0x28bcc0 | r3 == 0x0 → `0x28bcc0` | r3 != 0x0 → `0x28bce0` |
| `0x28bce0` cmp r0, #0; `0x28bce4` beq #0x28bcc0 | r0 == 0x0 → `0x28bcc0` | r0 != 0x0 → `0x28bce8` |
| `0x28bd38` cmp r3, #0; `0x28bd3c` beq #0x28bc7c | r3 == 0x0 → `0x28bc7c` | r3 != 0x0 → `0x28bd40` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `0024eadc` — ctlperson_main(CTLINFO*)

Observed direct compare/branch pairs: **7**; local bitmask sequences: **1**.

Modeled ARM CFG nodes: **115**; unmodeled outgoing edges/transfers: **4**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x24eaf8` tst r3, #4; `0x24eafc` bne #0x24eb34 | (r3 & 0x4) != 0 → `0x24eb34` | (r3 & 0x4) == 0 → `0x24eb00` |
| `0x24eb0c` tst r3, #0x40; `0x24eb10` bne #0x24ec68 | (r3 & 0x40) != 0 → `0x24ec68` | (r3 & 0x40) == 0 → `0x24eb14` |
| `0x24eb14` tst r3, #0x100; `0x24eb18` bne #0x24ebc0 | (r3 & 0x100) != 0 → `0x24ebc0` | (r3 & 0x100) == 0 → `0x24eb1c` |
| `0x24eb1c` tst r3, #0x20; `0x24eb20` beq #0x24eb30 | (r3 & 0x20) == 0 → `0x24eb30` | (r3 & 0x20) != 0 → `0x24eb24` |
| `0x24eb28` cmp r3, #0; `0x24eb2c` bne #0x24ebe8 | r3 != 0x0 → `0x24ebe8` | r3 == 0x0 → `0x24eb30` |
| `0x24eb3c` cmp r0, #0; `0x24eb40` bne #0x24eb00 | r0 != 0x0 → `0x24eb00` | r0 == 0x0 → `0x24eb44` |
| `0x24ebc4` cmp r2, #0; `0x24ebc8` beq #0x24eb1c | r2 == 0x0 → `0x24eb1c` | r2 != 0x0 → `0x24ebcc` |

### Local memory-bit effects and direct incoming edges

- Candidate sets `0x4` at `[r5]`; sequence: `0x24ec08`, `0x24ec0c`, `0x24ec10`.
  - No direct CMP/TST-branch incoming edge demonstrated; entry condition remains unknown.
  - Modeled direct predecessors: `0x24ec04` (call_returns).
  - Branch `0x24eb10` after compare `0x24eb0c`: [(r3 & 0x40) != 0] → no route found in modeled graph; [(r3 & 0x40) == 0] → 0x24eb14 → 0x24eb18 → 0x24eb1c → 0x24eb20 → 0x24eb24 → 0x24eb28 → 0x24eb2c → .... Only one modeled successor reaches the write; NOT a dominance or impossibility proof.
  - Branch `0x24eb20` after compare `0x24eb1c`: [(r3 & 0x20) == 0] → no route found in modeled graph; [(r3 & 0x20) != 0] → 0x24eb24 → 0x24eb28 → 0x24eb2c → 0x24ebe8 → 0x24ebec → 0x24ebf0 → 0x24ebf4 → .... Only one modeled successor reaches the write; NOT a dominance or impossibility proof.
  - Branch `0x24eb2c` after compare `0x24eb28`: [r3 != 0x0] → 0x24ebe8 → 0x24ebec → 0x24ebf0 → 0x24ebf4 → 0x24ebf8 → 0x24ebfc → 0x24ec00 → ...; [r3 == 0x0] → no route found in modeled graph. Only one modeled successor reaches the write; NOT a dominance or impossibility proof.
  - Branch `0x24eb40` after compare `0x24eb3c`: [r0 != 0x0] → 0x24eb00 → 0x24eb04 → 0x24eb08 → 0x24eb0c → 0x24eb10 → 0x24eb14 → 0x24eb18 → ...; [r0 == 0x0] → no route found in modeled graph. Only one modeled successor reaches the write; NOT a dominance or impossibility proof.
  - Branch `0x24ebc8` after compare `0x24ebc4`: [r2 == 0x0] → 0x24eb1c → 0x24eb20 → 0x24eb24 → 0x24eb28 → 0x24eb2c → 0x24ebe8 → 0x24ebec → ...; [r2 != 0x0] → no route found in modeled graph. Only one modeled successor reaches the write; NOT a dominance or impossibility proof.
  - Branch `0x24eafc` after compare `0x24eaf8`: [(r3 & 0x4) != 0] → 0x24eb34 → 0x24eb38 → 0x24eb3c → 0x24eb40 → 0x24eb00 → 0x24eb04 → 0x24eb08 → ...; [(r3 & 0x4) == 0] → 0x24eb00 → 0x24eb04 → 0x24eb08 → 0x24eb0c → 0x24eb10 → 0x24eb14 → 0x24eb18 → .... Both modeled successors can reach the write.

## `002576e0` — ctlevtinfo_init(int)

Observed direct compare/branch pairs: **0**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **115**; unmodeled outgoing edges/transfers: **0**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| No directly adjacent CMP/TST-branch pair | — | — |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `0015813c` — unittoface(int)

Observed direct compare/branch pairs: **7**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **86**; unmodeled outgoing edges/transfers: **1**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x15814c` tst r3, #0x80; `0x158150` bne #0x1581e4 | (r3 & 0x80) != 0 → `0x1581e4` | (r3 & 0x80) == 0 → `0x158154` |
| `0x158174` cmp r3, #0x82; `0x158178` bne #0x158190 | r3 != 0x82 → `0x158190` | r3 == 0x82 → `0x15817c` |
| `0x158198` cmp r2, #1; `0x15819c` bhi #0x1581d4 | r2 > (unsigned) 0x1 → `0x1581d4` | r2 <= (unsigned) 0x1 → `0x1581a0` |
| `0x1581a4` cmp r2, #0xa1; `0x1581a8` beq #0x1582f0 | r2 == 0xa1 → `0x1582f0` | r2 != 0xa1 → `0x1581ac` |
| `0x1581ac` cmp r2, #0xa4; `0x1581b0` beq #0x1582f0 | r2 == 0xa4 → `0x1582f0` | r2 != 0xa4 → `0x1581b4` |
| `0x1581b4` cmp r2, #0xa0; `0x1581b8` bne #0x1581c8 | r2 != 0xa0 → `0x1581c8` | r2 == 0xa0 → `0x1581bc` |
| `0x1581d4` cmp r3, #0xa2; `0x1581d8` bne #0x1581c8 | r3 != 0xa2 → `0x1581c8` | r3 == 0xa2 → `0x1581dc` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `001bc87c` — UnitTableInit(short)

Observed direct compare/branch pairs: **2**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **107**; unmodeled outgoing edges/transfers: **0**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x1bc93c` cmp r4, #9; `0x1bc940` ble #0x1bc924 | r4 <= (signed) 0x9 → `0x1bc924` | r4 > (signed) 0x9 → `0x1bc944` |
| `0x1bc9d4` cmp r3, #0x20; `0x1bc9d8` bne #0x1bc9c8 | r3 != 0x20 → `0x1bc9c8` | r3 == 0x20 → `0x1bc9dc` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `001ccc3c` — getTrapResultDamage(BWORK*, int)

Observed direct compare/branch pairs: **1**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **110**; unmodeled outgoing edges/transfers: **1**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x1ccdd0` cmp r0, #0; `0x1ccdd4` beq #0x1cccbc | r0 == 0x0 → `0x1cccbc` | r0 != 0x0 → `0x1ccdd8` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `0025f44c` — frmbuf_get()

Observed direct compare/branch pairs: **0**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **113**; unmodeled outgoing edges/transfers: **0**.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| No directly adjacent CMP/TST-branch pair | — | — |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## Verification still required

Inspect incomplete/unmodeled CFG predecessor sets, aliasing, effects of callees and compare behavior with execution traces before any semantic approval.
