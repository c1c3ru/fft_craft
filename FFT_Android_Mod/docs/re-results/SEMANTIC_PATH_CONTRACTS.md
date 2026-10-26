# Priority ARM conditional-path contracts

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

These are locally observed CMP/TST -> conditional branch edges; they are not dominance claims, execution traces, complete path constraints or proof of semantic equivalence.

## `002b2448` — EnvSE_Play(int)

Observed direct compare/branch pairs: **1**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **98**; entry-reachable: **98**; unmodeled outgoing edges/transfers: **1**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x2b2464` cmp r0, #0; `0x2b2468` beq #0x2b25a0 | r0 == 0x0 → `0x2b25a0` | r0 != 0x0 → `0x2b246c` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `0015813c` — unittoface(int)

Observed direct compare/branch pairs: **7**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **86**; entry-reachable: **86**; unmodeled outgoing edges/transfers: **1**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

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


## `001ccc3c` — getTrapResultDamage(BWORK*, int)

Observed direct compare/branch pairs: **1**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **110**; entry-reachable: **110**; unmodeled outgoing edges/transfers: **1**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x1ccdd0` cmp r0, #0; `0x1ccdd4` beq #0x1cccbc | r0 == 0x0 → `0x1cccbc` | r0 != 0x0 → `0x1ccdd8` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `00159aac` — asm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long)

Observed direct compare/branch pairs: **1**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **81**; entry-reachable: **81**; unmodeled outgoing edges/transfers: **2**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x159ac8` cmp r4, #0; `0x159acc` bne #0x159af4 | r4 != 0x0 → `0x159af4` | r4 == 0x0 → `0x159ad0` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `00162080` — wasm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long)

Observed direct compare/branch pairs: **1**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **81**; entry-reachable: **81**; unmodeled outgoing edges/transfers: **2**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x16209c` cmp r4, #0; `0x1620a0` bne #0x1620c8 | r4 != 0x0 → `0x1620c8` | r4 == 0x0 → `0x1620a4` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `002031a4` — iOSsetCursorByTouch(int, int, int, int, int)

Observed direct compare/branch pairs: **3**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **56**; entry-reachable: **56**; unmodeled outgoing edges/transfers: **1**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x20321c` cmp r3, #0; `0x203220` bne #0x2032dc | r3 != 0x0 → `0x2032dc` | r3 == 0x0 → `0x203224` |
| `0x2032d4` cmp r3, #0; `0x2032d8` bne #0x2032fc | r3 != 0x0 → `0x2032fc` | r3 == 0x0 → `0x2032dc` |
| `0x2032f4` cmp fp, #0; `0x2032f8` beq #0x2032dc | fp == 0x0 → `0x2032dc` | fp != 0x0 → `0x2032fc` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `002c9b11` — __gxx_personality_v0

Thumb-tagged address: local ARM CMP/TST branch contract extraction not supported; no predicate is inferred.

## `0027fe84` — Savedata_Load(unsigned char*, int*)

Observed direct compare/branch pairs: **5**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **91**; entry-reachable: **91**; unmodeled outgoing edges/transfers: **1**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x27ff24` cmp r0, #1; `0x27ff28` beq #0x27ff44 | r0 == 0x1 → `0x27ff44` | r0 != 0x1 → `0x27ff2c` |
| `0x27ff3c` cmp r5, r0; `0x27ff40` beq #0x27ff98 | r5 == r0 → `0x27ff98` | r5 != r0 → `0x27ff44` |
| `0x27ff44` cmp r4, #0; `0x27ff48` beq #0x27ff5c | r4 == 0x0 → `0x27ff5c` | r4 != 0x0 → `0x27ff4c` |
| `0x27ff68` cmp r2, r3; `0x27ff6c` bne #0x27ffe8 | r2 != r3 → `0x27ffe8` | r2 == r3 → `0x27ff70` |
| `0x27ffc4` cmp r4, #0; `0x27ffc8` beq #0x27ffdc | r4 == 0x0 → `0x27ffdc` | r4 != 0x0 → `0x27ffcc` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `0028e2e4` — CdControl

Observed direct compare/branch pairs: **4**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **66**; entry-reachable: **66**; unmodeled outgoing edges/transfers: **1**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x28e2e4` cmp r2, #0; `0x28e2e8` beq #0x28e378 | r2 == 0x0 → `0x28e378` | r2 != 0x0 → `0x28e2ec` |
| `0x28e378` cmp r0, #0xe; `0x28e37c` beq #0x28e398 | r0 == 0xe → `0x28e398` | r0 != 0xe → `0x28e380` |
| `0x28e380` cmp r0, #0x1b; `0x28e384` bne #0x28e3b0 | r0 != 0x1b → `0x28e3b0` | r0 == 0x1b → `0x28e388` |
| `0x28e3b0` cmp r0, #2; `0x28e3b4` bne #0x28e370 | r0 != 0x2 → `0x28e370` | r0 == 0x2 → `0x28e3b8` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `001d972c` — get_shape2(BWORK*, unsigned char*)

Observed direct compare/branch pairs: **4**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **52**; entry-reachable: **52**; unmodeled outgoing edges/transfers: **1**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x1d9834` cmp r3, #0xa1; `0x1d9838` beq #0x1d989c | r3 == 0xa1 → `0x1d989c` | r3 != 0xa1 → `0x1d983c` |
| `0x1d983c` cmp r3, #0xa4; `0x1d9840` beq #0x1d989c | r3 == 0xa4 → `0x1d989c` | r3 != 0xa4 → `0x1d9844` |
| `0x1d9844` cmp r3, #0xa0; `0x1d9848` beq #0x1d9890 | r3 == 0xa0 → `0x1d9890` | r3 != 0xa0 → `0x1d984c` |
| `0x1d9874` cmp ip, #0x80; `0x1d9878` bls #0x1d9888 | ip <= (unsigned) 0x80 → `0x1d9888` | ip > (unsigned) 0x80 → `0x1d987c` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `0022a6a4` — _ReadTMD(TMD_PRIM*)

Observed direct compare/branch pairs: **0**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **80**; entry-reachable: **80**; unmodeled outgoing edges/transfers: **1**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| No directly adjacent CMP/TST-branch pair | — | — |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## `00210eac` — initMap(int, int)

Observed direct compare/branch pairs: **1**; local bitmask sequences: **0**.

Modeled ARM CFG nodes: **75**; entry-reachable: **75**; unmodeled outgoing edges/transfers: **1**.

Modeled dominators are calculated only for nodes reachable from the function entry. They do not establish dominance across unknown incoming edges, indirect transfers, exceptions or callees.

A route in this graph is a candidate, not a proven executable path. An absent route may be due to unresolved indirect jumps, callee effects, missing code or exceptional control flow.

| Compare / branch | Taken edge | Fallthrough edge |
|---|---|---|
| `0x210ef8` cmp r0, #2; `0x210efc` beq #0x210ef4 | r0 == 0x2 → `0x210ef4` | r0 != 0x2 → `0x210f00` |

### Local memory-bit effects and direct incoming edges

No conservative consecutive LDR/BIC-or-ORR/STR sequence identified.


## Verification still required

Inspect incomplete/unmodeled CFG predecessor sets, aliasing, effects of callees and compare behavior with execution traces before any semantic approval.
