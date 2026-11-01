# ARM semantic review triage

Unverified checkpoints: **53**; core targets: **36**.

These are structural observations, not semantic equivalence proofs.

| Review reason | Total | Core |
|---|---:|---:|
| coverage_below_95 | 19 | 11 |
| resolved_jump_table_check | 34 | 25 |

## Highest priority evidence collection

| Address | Function | Coverage | Reason | Next check |
|---|---|---:|---|---|
| `002b2448` | EnvSE_Play(int) | 77.17% | resolved_jump_table_check | Verify guard, all cases and default path |
| `0015813c` | unittoface(int) | 69.35% | resolved_jump_table_check | Verify guard, all cases and default path |
| `001ccc3c` | getTrapResultDamage(BWORK*, int) | 88.71% | resolved_jump_table_check | Verify guard, all cases and default path |
| `00159aac` | asm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 80.2% | resolved_jump_table_check | Verify guard, all cases and default path |
| `00162080` | wasm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 80.2% | resolved_jump_table_check | Verify guard, all cases and default path |
| `002031a4` | iOSsetCursorByTouch(int, int, int, int, int) | 57.14% | resolved_jump_table_check | Verify guard, all cases and default path |
| `002c9b11` | __gxx_personality_v0 | 90.21% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0027fe84` | Savedata_Load(unsigned char*, int*) | 94.79% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `0028e2e4` | CdControl | 68.75% | resolved_jump_table_check | Verify guard, all cases and default path |
| `001d972c` | get_shape2(BWORK*, unsigned char*) | 54.74% | resolved_jump_table_check | Verify guard, all cases and default path |
| `0022a6a4` | _ReadTMD(TMD_PRIM*) | 84.21% | resolved_jump_table_check | Verify guard, all cases and default path |
| `00210eac` | initMap(int, int) | 81.52% | resolved_jump_table_check | Verify guard, all cases and default path |
| `002b20f4` | onGotoNextMode(int) | 71.6% | resolved_jump_table_check | Verify guard, all cases and default path |
| `00289c1c` | pspFftDelete(int*) | 57.5% | resolved_jump_table_check | Verify guard, all cases and default path |
| `00203070` | setCursorByTouch(int, int, int) | 49.35% | resolved_jump_table_check | Verify guard, all cases and default path |
| `001d67a8` | get_mapid(int, int, int, int) | 75.0% | resolved_jump_table_check | Verify guard, all cases and default path |
| `002b3464` | Boot_Init() | 92.0% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `002899a0` | pspFftSave(int, FFT_SAVE_DATA*, int*) | 63.89% | resolved_jump_table_check | Verify guard, all cases and default path |
| `001a6410` | MessageDataSet(int) | 83.1% | resolved_jump_table_check | Verify guard, all cases and default path |
| `001dc944` | set_casting_status(BWORK*, unsigned char) | 85.29% | resolved_jump_table_check | Verify guard, all cases and default path |
| `001caa10` | set_ct_weapon(ACT*) | 67.74% | resolved_jump_table_check | Verify guard, all cases and default path |
| `0025b78c` | houkoku_talkunit(int) | 86.44% | resolved_jump_table_check | Verify guard, all cases and default path |
| `00285e50` | pspMsgGet(unsigned int) | 63.79% | resolved_jump_table_check | Verify guard, all cases and default path |
| `0021d544` | getNextSENo(int) | 80.0% | resolved_jump_table_check | Verify guard, all cases and default path |
| `002867a8` | getMovieEventNum(int) | 68.52% | resolved_jump_table_check | Verify guard, all cases and default path |
| `0015a65c` | siOS_TCurSucCheck(unsigned int) | 78.85% | resolved_jump_table_check | Verify guard, all cases and default path |
| `002cb0c0` | __gedf2 | 92.11% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `002cb4ac` | __aeabi_ul2f | 82.86% | coverage_below_95 | Disassemble uncovered blocks and side effects |
| `000d7e00` | load_replaceitems(int, int) | 56.67% | resolved_jump_table_check | Verify guard, all cases and default path |
| `000ff9ec` | Wload_replaceitems(int, int) | 56.67% | resolved_jump_table_check | Verify guard, all cases and default path |

Approval requires instruction-level control-flow evidence, input/output invariants, and ideally differential tests or execution traces. Do not change needs_review solely from these summaries.
