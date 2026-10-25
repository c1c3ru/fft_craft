# Isolated ARM conditional branch microexecution

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Only each original two-instruction CMP/B pair executes in Unicorn. The emulator stops before any destination instruction runs. This is not a full function trace, reachability proof, callee verification or proof of semantic equivalence.

| Branch address | Contract | Inputs × seed flags | Result |
|---|---|---:|---|
| `0x2442cc` | `signed_gt_43`: taken `0x2443c8`, else `0x2442d0` | 32 × 2 | PASS |
| `0x244310` | `equal_256`: taken `0x24438c`, else `0x244314` | 32 × 2 | PASS |
| `0x244384` | `not_equal_256`: taken `0x2442e0`, else `0x244388` | 32 × 2 | PASS |

**Total verified isolated branch executions:** 192.

## Limitations

- Signed versus unsigned interpretations are checked against the actual machine flags set by CMP in the two-instruction snippet.
- Two opposite initial NZCV patterns help detect reliance on stale flags.
- Values are sampled, not exhaustively enumerated.
- No surrounding predecessor instructions, globals, calls, exceptions or destination instructions are executed.
- The entire function remains `needs_review`.
