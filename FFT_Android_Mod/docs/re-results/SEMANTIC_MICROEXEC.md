# Isolated ARM machine-instruction microexecution

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

**Scope:** only three ARM instructions at each listed address, executed with synthetic state in Unicorn. No branch, call, complete function or application has been emulated. This establishes a bounded instruction-level behavior check, **not** semantic equivalence or global reachability.

| ELF instruction address | Test inputs | Observed operation | Result |
|---|---:|---|---|
| `0x244254` | 32 | memory32 := memory32 & ~0x40; adjacent word unchanged | PASS |
| `0x2443b8` | 32 | memory32 := memory32 & ~0x40; adjacent word unchanged | PASS |

**Total verified machine micro-executions:** 64.

## Evidence boundaries

- The original ELF bytes were executed; the three-instruction patterns are independently matched before executing them.
- Deterministic examples are not exhaustive over the 32-bit state space.
- This does not prove that any function invocation reaches either site.
- Side effects, callee behavior, flags, aliasing, and external inputs outside the isolated snippets are not established.

Every affected function remains `needs_review`.
