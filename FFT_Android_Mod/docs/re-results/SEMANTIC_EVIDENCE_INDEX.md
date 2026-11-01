# ARM review evidence index

Static ARM-mode disassembly only. Reachability is heuristic; unvisited slots may be literal data. No semantic equivalence is proved.

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Evidence collected: **53/53** pending functions.
Evidence schema: v2

These reports do not constitute semantic verification.

| Address | Function | Evidence |
|---|---|---|
| `002b2448` | EnvSE_Play(int) | [Evidence](semantic-evidence/002b2448.md) |
| `0015813c` | unittoface(int) | [Evidence](semantic-evidence/0015813c.md) |
| `001ccc3c` | getTrapResultDamage(BWORK*, int) | [Evidence](semantic-evidence/001ccc3c.md) |
| `00159aac` | asm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | [Evidence](semantic-evidence/00159aac.md) |
| `00162080` | wasm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | [Evidence](semantic-evidence/00162080.md) |
| `002031a4` | iOSsetCursorByTouch(int, int, int, int, int) | [Evidence](semantic-evidence/002031a4.md) |
| `002c9b11` | __gxx_personality_v0 | [Evidence](semantic-evidence/002c9b11.md) |
| `0027fe84` | Savedata_Load(unsigned char*, int*) | [Evidence](semantic-evidence/0027fe84.md) |
| `0028e2e4` | CdControl | [Evidence](semantic-evidence/0028e2e4.md) |
| `001d972c` | get_shape2(BWORK*, unsigned char*) | [Evidence](semantic-evidence/001d972c.md) |
| `0022a6a4` | _ReadTMD(TMD_PRIM*) | [Evidence](semantic-evidence/0022a6a4.md) |
| `00210eac` | initMap(int, int) | [Evidence](semantic-evidence/00210eac.md) |
| `002b20f4` | onGotoNextMode(int) | [Evidence](semantic-evidence/002b20f4.md) |
| `00289c1c` | pspFftDelete(int*) | [Evidence](semantic-evidence/00289c1c.md) |
| `00203070` | setCursorByTouch(int, int, int) | [Evidence](semantic-evidence/00203070.md) |
| `001d67a8` | get_mapid(int, int, int, int) | [Evidence](semantic-evidence/001d67a8.md) |
| `002b3464` | Boot_Init() | [Evidence](semantic-evidence/002b3464.md) |
| `002899a0` | pspFftSave(int, FFT_SAVE_DATA*, int*) | [Evidence](semantic-evidence/002899a0.md) |
| `001a6410` | MessageDataSet(int) | [Evidence](semantic-evidence/001a6410.md) |
| `001dc944` | set_casting_status(BWORK*, unsigned char) | [Evidence](semantic-evidence/001dc944.md) |
| `001caa10` | set_ct_weapon(ACT*) | [Evidence](semantic-evidence/001caa10.md) |
| `0025b78c` | houkoku_talkunit(int) | [Evidence](semantic-evidence/0025b78c.md) |
| `00285e50` | pspMsgGet(unsigned int) | [Evidence](semantic-evidence/00285e50.md) |
| `0021d544` | getNextSENo(int) | [Evidence](semantic-evidence/0021d544.md) |
| `002867a8` | getMovieEventNum(int) | [Evidence](semantic-evidence/002867a8.md) |
| `0015a65c` | siOS_TCurSucCheck(unsigned int) | [Evidence](semantic-evidence/0015a65c.md) |
| `002cb0c0` | __gedf2 | [Evidence](semantic-evidence/002cb0c0.md) |
| `002cb4ac` | __aeabi_ul2f | [Evidence](semantic-evidence/002cb4ac.md) |
| `000d7e00` | load_replaceitems(int, int) | [Evidence](semantic-evidence/000d7e00.md) |
| `000ff9ec` | Wload_replaceitems(int, int) | [Evidence](semantic-evidence/000ff9ec.md) |
| `002cabdc` | __aeabi_ul2d | [Evidence](semantic-evidence/002cabdc.md) |
| `002cb830` | __gesf2 | [Evidence](semantic-evidence/002cb830.md) |
| `002cb484` | __floatunsisf | [Evidence](semantic-evidence/002cb484.md) |
| `002c9a25` | operator new[](unsigned int) | [Evidence](semantic-evidence/002c9a25.md) |
| `002c9115` | operator delete(void*) | [Evidence](semantic-evidence/002c9115.md) |
| `002c9121` | operator delete[](void*) | [Evidence](semantic-evidence/002c9121.md) |
| `002cd594` | _Unwind_VRS_Pop | [Evidence](semantic-evidence/002cd594.md) |
| `002ca8a0` | __subdf3 | [Evidence](semantic-evidence/002ca8a0.md) |
| `002ca8a4` | __adddf3 | [Evidence](semantic-evidence/002ca8a4.md) |
| `002cac50` | __muldf3 | [Evidence](semantic-evidence/002cac50.md) |
| `00271ba4` | SetBaseTargetGroup(int, int) | [Evidence](semantic-evidence/00271ba4.md) |
| `0027207c` | GetNearestUnit(int) | [Evidence](semantic-evidence/0027207c.md) |
| `000ab4b0` | CEGL2_FBO::ErrorGL(char const*, char const*, unsigned int) | [Evidence](semantic-evidence/000ab4b0.md) |
| `000aecb8` | CEGL2_SPRITE::ErrorGL(char const*, char const*, unsigned int) | [Evidence](semantic-evidence/000aecb8.md) |
| `000a7ec4` | CEGL2_IF::SetBlendMode(int) | [Evidence](semantic-evidence/000a7ec4.md) |
| `002ca215` | __cxa_call_unexpected | [Evidence](semantic-evidence/002ca215.md) |
| `002ca125` | __cxa_type_match | [Evidence](semantic-evidence/002ca125.md) |
| `002ccfb8` | _Unwind_VRS_Get | [Evidence](semantic-evidence/002ccfb8.md) |
| `002cd03c` | _Unwind_VRS_Set | [Evidence](semantic-evidence/002cd03c.md) |
| `002c99b5` | operator new(unsigned int) | [Evidence](semantic-evidence/002c99b5.md) |
| `002ca195` | __cxa_begin_cleanup | [Evidence](semantic-evidence/002ca195.md) |
| `0028c288` | CFFT_STATE::GetBackdropColor(float*, float*, float*) | [Evidence](semantic-evidence/0028c288.md) |
| `002ccf98` | _Unwind_DeleteException | [Evidence](semantic-evidence/002ccf98.md) |
