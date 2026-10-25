# Structural analyzer v3 — migration and coverage

Automatic structural acceptance checks all ARM instruction slots, candidate PC-relative data words, unresolved flow and jump-table bounds/targets. It is **not semantic equivalence**.

| Metric | Count |
|---|---:|
| v3 checkpoints | 100 |
| Legacy checkpoint records unchanged | 2902 |
| v3 structurally accepted | 85 |
| v3 still under review | 15 |
| Archived v2 originals | 100 |
| Referenced candidate literal words | 702 |
| Unexplained instruction slots | 269 |
| Independently checked jump tables | 0 |
| Unsafe / unresolved checked tables | 13 |

## Remaining v3 review examples

| Address | Unexplained slots | Reason |
|---|---:|---|
| `001a6410` | 10 | unverified_jump_table |
| `001d67a8` | 17 | unverified_jump_table |
| `001d972c` | 43 | unverified_jump_table |
| `001dc944` | 10 | unverified_jump_table |
| `00203070` | 34 | unverified_jump_table |
| `002031a4` | 34 | unverified_jump_table |
| `00210eac` | 14 | unverified_jump_table |
| `0022a6a4` | 10 | unverified_jump_table |
| `0027fe84` | 0 | instruction_conflict |
| `002899a0` | 21 | unverified_jump_table |
| `00289c1c` | 28 | unverified_jump_table |
| `0028e2e4` | 28 | unverified_jump_table |
| `002b20f4` | 20 | unverified_jump_table |
| `002b3464` | 0 | instruction_conflict |
| `002c9b11` | 0 | non_arm_aligned_or_empty |

## Migration contract

Original v2 JSON checkpoints are archived in `structural-v2/` on first upgrade; unprocessed checkpoints remain untouched.
A ruleset fingerprint prevents repeating unchanged v3 checkpoints, but changed rules trigger selective reruns.
Missing instructions, ambiguous literal words and unsafe table targets remain in review.
