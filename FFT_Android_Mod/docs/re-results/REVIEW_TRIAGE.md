# ARM semantic review triage

Unverified checkpoints: **889**; core targets: **747**.

These are structural observations, not semantic equivalence proofs.

| Review reason | Total | Core |
|---|---:|---:|
| coverage_below_95 | 855 | 722 |
| resolved_jump_table_check | 34 | 25 |

## Highest priority evidence collection

| Address | Function | Coverage | Reason | Next check |
|---|---|---:|---|---|
| `0028179c` | iOS_v2menuSetType(V2MENU_TYPE) | 94.81% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `00244200` | vEnd_rollproc() | 91.67% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `000df864` | event_status_set(unsigned short, unsigned short) | 93.13% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0025a228` | houkoku_okng(CTLINFO*) | 93.7% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `002b2448` | EnvSE_Play(int) | 77.17% | resolved_jump_table_check | Verify guard, all cases and default path |
| `0028bb88` | TE_asmTaskEntry(int) | 91.27% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0024eadc` | ctlperson_main(CTLINFO*) | 92.0% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `002576e0` | ctlevtinfo_init(int) | 92.0% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0015813c` | unittoface(int) | 69.35% | resolved_jump_table_check | Verify guard, all cases and default path |
| `001bc87c` | UnitTableInit(short) | 86.29% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `001ccc3c` | getTrapResultDamage(BWORK*, int) | 88.71% | resolved_jump_table_check | Verify guard, all cases and default path |
| `002472a8` | ctlsound_main(CTLINFO*) | 93.39% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `00253f20` | ctlmap_init() | 90.0% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0026c680` | ctltresure_main(CTLINFO*) | 92.5% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `002553a8` | ctlhelp2_init(int, int) | 91.6% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0019dc10` | SttsEmploy() | 89.83% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0026dd40` | ctlhentuto_init() | 92.24% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `002608c0` | ctlokng_init(_POINT) | 92.17% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0025990c` | ctlhistory_main(CTLINFO*) | 92.11% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `001d8b58` | get_ability_address(int, ABILITY_COMMON_DATA**, void**) | 92.04% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0024e91c` | ctlpersmes_init(int) | 91.96% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0019d304` | DressSellStock() | 90.99% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `001eb124` | loadAbilityAnimation(tag_animation*, void*) | 94.5% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0020c264` | db_init(int, int, int, unsigned char, unsigned char, unsigned char) | 94.5% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0019df84` | AccountEmploy() | 91.67% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0026abac` | timeevt_chk() | 87.96% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `00247884` | birthday_change(CTLINFO*) | 94.39% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `00270520` | valnumwin_set(int, unsigned long, int, _POINT*) | 93.4% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0024f4e8` | ctltipsmes_init(int) | 93.27% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0019dde8` | BuyEmploy() | 92.23% | coverage_below_95 | Disassemble uncovered blocks and side effects |

Approval requires instruction-level control-flow evidence, input/output invariants, and ideally differential tests or execution traces. Do not change needs_review solely from these summaries.
