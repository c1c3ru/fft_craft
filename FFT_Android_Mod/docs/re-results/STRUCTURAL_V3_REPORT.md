# Structural analyzer v3 — migration and coverage

Automatic structural acceptance checks all ARM instruction slots, candidate PC-relative data words, unresolved flow and jump-table bounds/targets. It is **not semantic equivalence**.

| Metric | Count |
|---|---:|
| v3 checkpoints | 1186 |
| Legacy checkpoint records unchanged | 1816 |
| v3 structurally accepted | 1143 |
| v3 still under review | 43 |
| Archived v2 originals | 1172 |
| Referenced candidate literal words | 2777 |
| Unexplained instruction slots | 729 |
| Independently checked jump tables | 0 |
| Unsafe / unresolved checked tables | 30 |

## Remaining v3 review examples

| Address | Unexplained slots | Reason |
|---|---:|---|
| `000a7ec4` | 9 | unverified_jump_table |
| `000ab4b0` | 7 | unverified_jump_table |
| `000aecb8` | 7 | unverified_jump_table |
| `000d7e00` | 13 | unverified_jump_table |
| `000ff9ec` | 13 | unverified_jump_table |
| `0015a65c` | 11 | unverified_jump_table |
| `001a6410` | 10 | unverified_jump_table |
| `001caa10` | 17 | unverified_jump_table |
| `001d67a8` | 17 | unverified_jump_table |
| `001d972c` | 43 | unverified_jump_table |
| `001dc944` | 10 | unverified_jump_table |
| `00203070` | 34 | unverified_jump_table |
| `002031a4` | 34 | unverified_jump_table |
| `00210eac` | 14 | unverified_jump_table |
| `0021d544` | 8 | unverified_jump_table |
| `0022a6a4` | 10 | unverified_jump_table |
| `0025b78c` | 5 | unverified_jump_table |
| `00271ba4` | 10 | unverified_jump_table |
| `0027fe84` | 0 | instruction_conflict |
| `00285e50` | 12 | unverified_jump_table |
| `002867a8` | 15 | unverified_jump_table |
| `002899a0` | 21 | unverified_jump_table |
| `00289c1c` | 28 | unverified_jump_table |
| `0028c288` | 6 | unverified_jump_table |
| `0028e2e4` | 28 | unverified_jump_table |
| `002b20f4` | 20 | unverified_jump_table |
| `002b3464` | 0 | instruction_conflict |
| `002c9121` | 0 | non_arm_aligned_or_empty |
| `002c99b5` | 0 | non_arm_aligned_or_empty |
| `002c9b11` | 0 | non_arm_aligned_or_empty |

## Migration contract

Original v2 JSON checkpoints are archived in `structural-v2/` on first upgrade; unprocessed checkpoints remain untouched.
A ruleset fingerprint prevents repeating unchanged v3 checkpoints, but changed rules trigger selective reruns.
Missing instructions, ambiguous literal words and unsafe table targets remain in review.
