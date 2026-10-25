# Reverse engineering progress

Binary SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

| Metric | Quantity |
|---|---:|
| Inventory total | 6,455 functions / 1,837,392 bytes |
| Previously analyzed in CSV | 3,451 functions / 1,551,512 bytes |
| JSON checkpoints (all statuses) | 3,002 |
| Newly accepted structurally | 2,213 functions / 251,292 bytes |
| Needs review | 789 functions |
| Core targets in inventory | 4,642 functions |
| Core targets checkpointed | 2,345 functions |
| Core accepted structurally | 1,698 functions |
| Core needs review | 647 functions |
| Core not yet checkpointed | 0 functions |
| Not yet checkpointed | 0 functions / 0 bytes |

## Checkpoint status

| Status | Functions |
|---|---:|
| auto_structural | 2,213 |
| needs_review | 789 |

## Review queue (largest first)

| Address | Function | Bytes | Coverage % | Resolved tables | Unresolved tables |
|---|---|---:|---:|---:|---:|
| `002cd594` | _Unwind_VRS_Pop (needs_review) | 856 | 97.2 | 1 | 0 |
| `002ca8a0` | __subdf3 (needs_review) | 688 | 28.49 | 0 | 0 |
| `002ca8a4` | __adddf3 (needs_review) | 684 | 28.07 | 0 | 0 |
| `002cac50` | __muldf3 (needs_review) | 620 | 72.9 | 0 | 0 |
| `0028179c` | iOS_v2menuSetType(V2MENU_TYPE) (needs_review) | 540 | 94.81 | 0 | 0 |
| `00244200` | vEnd_rollproc() (needs_review) | 528 | 91.67 | 0 | 0 |
| `000df864` | event_status_set(unsigned short, unsigned short) (needs_review) | 524 | 93.13 | 0 | 0 |
| `002b2448` | EnvSE_Play(int) (needs_review) | 508 | 77.17 | 1 | 0 |
| `00271ba4` | SetBaseTargetGroup(int, int) (needs_review) | 508 | 89.76 | 2 | 0 |
| `0025a228` | houkoku_okng(CTLINFO*) (needs_review) | 508 | 93.7 | 0 | 0 |
| `0028bb88` | TE_asmTaskEntry(int) (needs_review) | 504 | 91.27 | 0 | 0 |
| `002576e0` | ctlevtinfo_init(int) (needs_review) | 500 | 92.0 | 0 | 0 |
| `0024eadc` | ctlperson_main(CTLINFO*) (needs_review) | 500 | 92.0 | 0 | 0 |
| `001ccc3c` | getTrapResultDamage(BWORK*, int) (needs_review) | 496 | 88.71 | 1 | 0 |
| `001bc87c` | UnitTableInit(short) (needs_review) | 496 | 86.29 | 0 | 0 |
| `0015813c` | unittoface(int) (needs_review) | 496 | 69.35 | 1 | 0 |
| `002472a8` | ctlsound_main(CTLINFO*) (needs_review) | 484 | 93.39 | 0 | 0 |
| `0026c680` | ctltresure_main(CTLINFO*) (needs_review) | 480 | 92.5 | 0 | 0 |
| `00253f20` | ctlmap_init() (needs_review) | 480 | 90.0 | 0 | 0 |
| `0015596c` | worldmap_startinit() (needs_review) | 480 | 93.33 | 0 | 0 |
| `002553a8` | ctlhelp2_init(int, int) (needs_review) | 476 | 91.6 | 0 | 0 |
| `0027a974` | BattleRoutineInit() (needs_review) | 472 | 93.22 | 0 | 0 |
| `0027207c` | GetNearestUnit(int) (needs_review) | 472 | 92.37 | 1 | 0 |
| `0019dc10` | SttsEmploy() (needs_review) | 472 | 89.83 | 0 | 0 |
| `0026dd40` | ctlhentuto_init() (needs_review) | 464 | 92.24 | 0 | 0 |
| `002608c0` | ctlokng_init(_POINT) (needs_review) | 460 | 92.17 | 0 | 0 |
| `0026b0f4` | wld_snpl() (needs_review) | 456 | 93.86 | 0 | 0 |
| `0025990c` | ctlhistory_main(CTLINFO*) (needs_review) | 456 | 92.11 | 0 | 0 |
| `001d8b58` | get_ability_address(int, ABILITY_COMMON_DATA**, void**) (needs_review) | 452 | 92.04 | 0 | 0 |
| `0024e91c` | ctlpersmes_init(int) (needs_review) | 448 | 91.96 | 0 | 0 |
| `0019d304` | DressSellStock() (needs_review) | 444 | 90.99 | 0 | 0 |
| `0020c264` | db_init(int, int, int, unsigned char, unsigned char, unsigned char) (needs_review) | 436 | 94.5 | 0 | 0 |
| `001eb124` | loadAbilityAnimation(tag_animation*, void*) (needs_review) | 436 | 94.5 | 0 | 0 |
| `0026abac` | timeevt_chk() (needs_review) | 432 | 87.96 | 0 | 0 |
| `0019df84` | AccountEmploy() (needs_review) | 432 | 91.67 | 0 | 0 |
| `00247884` | birthday_change(CTLINFO*) (needs_review) | 428 | 94.39 | 0 | 0 |
| `00276788` | CheckUnitActionOK(unsigned char*) (needs_review) | 424 | 94.34 | 0 | 0 |
| `00270520` | valnumwin_set(int, unsigned long, int, _POINT*) (needs_review) | 424 | 93.4 | 0 | 0 |
| `000aecb8` | CEGL2_SPRITE::ErrorGL(char const*, char const*, unsigned int) (needs_review) | 420 | 86.67 | 1 | 0 |
| `000ab4b0` | CEGL2_FBO::ErrorGL(char const*, char const*, unsigned int) (needs_review) | 420 | 89.52 | 1 | 0 |
| `0024f4e8` | ctltipsmes_init(int) (needs_review) | 416 | 93.27 | 0 | 0 |
| `0024e734` | ctlperson_init() (needs_review) | 412 | 90.29 | 0 | 0 |
| `0019dde8` | BuyEmploy() (needs_review) | 412 | 92.23 | 0 | 0 |
| `0021ef4c` | InitPermanentEffect() (needs_review) | 408 | 92.16 | 0 | 0 |
| `00162080` | wasm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) (needs_review) | 404 | 80.2 | 2 | 0 |
| `00159aac` | asm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) (needs_review) | 404 | 80.2 | 2 | 0 |
| `002595c0` | ctlhistory_init() (needs_review) | 400 | 90.0 | 0 | 0 |
| `00259780` | ctlhismes_init(int) (needs_review) | 396 | 91.92 | 0 | 0 |
| `00256174` | ctlfsetnum_main(CTLINFO*) (needs_review) | 392 | 90.82 | 0 | 0 |
| `002031a4` | iOSsetCursorByTouch(int, int, int, int, int) (needs_review) | 392 | 57.14 | 1 | 0 |
| `001cd308` | check_learning(int, unsigned short*) (needs_review) | 392 | 94.9 | 0 | 0 |
| `002c9b11` | __gxx_personality_v0 (needs_review) | 388 | 7.22 | 0 | 0 |
| `0028e2e4` | CdControl (needs_review) | 384 | 68.75 | 1 | 0 |
| `0027fe84` | Savedata_Load(unsigned char*, int*) (needs_review) | 384 | 94.79 | 0 | 0 |
| `0024581c` | movie_init(int, int, int, int, int, char*) (needs_review) | 384 | 88.54 | 0 | 0 |
| `00242498` | ctlendroll_init() (needs_review) | 384 | 87.5 | 0 | 0 |
| `0022a6a4` | _ReadTMD(TMD_PRIM*) (needs_review) | 380 | 84.21 | 1 | 0 |
| `001d972c` | get_shape2(BWORK*, unsigned char*) (needs_review) | 380 | 54.74 | 1 | 0 |
| `0026baec` | wldtown_init() (needs_review) | 372 | 91.4 | 0 | 0 |
| `00210eac` | initMap(int, int) (needs_review) | 368 | 81.52 | 1 | 0 |
| `0026c27c` | ctltresure_init() (needs_review) | 336 | 91.67 | 0 | 0 |
| `00255a38` | ctlflagset_init() (needs_review) | 336 | 90.48 | 0 | 0 |
| `002b20f4` | onGotoNextMode(int) (needs_review) | 324 | 71.6 | 2 | 0 |
| `00289c1c` | pspFftDelete(int*) (needs_review) | 320 | 57.5 | 1 | 0 |
| `0025a0f0` | ctlhoukmes_init(int) (needs_review) | 312 | 89.74 | 0 | 0 |
| `00203070` | setCursorByTouch(int, int, int) (needs_review) | 308 | 49.35 | 1 | 0 |
| `000a7ec4` | CEGL2_IF::SetBlendMode(int) (needs_review) | 308 | 88.31 | 1 | 0 |
| `001d67a8` | get_mapid(int, int, int, int) (needs_review) | 304 | 75.0 | 1 | 0 |
| `002b3464` | Boot_Init() (needs_review) | 300 | 92.0 | 0 | 0 |
| `0024717c` | ctlsound_init() (needs_review) | 300 | 90.67 | 0 | 0 |
| `002899a0` | pspFftSave(int, FFT_SAVE_DATA*, int*) (needs_review) | 288 | 63.89 | 1 | 0 |
| `001a6410` | MessageDataSet(int) (needs_review) | 284 | 83.1 | 1 | 0 |
| `0026b904` | wldsymbol_init() (needs_review) | 276 | 91.3 | 0 | 0 |
| `001e21f8` | getskillresult_first(int) (needs_review) | 272 | 91.18 | 0 | 0 |
| `001dc944` | set_casting_status(BWORK*, unsigned char) (needs_review) | 272 | 85.29 | 1 | 0 |
| `002ca215` | __cxa_call_unexpected (needs_review) | 268 | 0.0 | 0 | 0 |
| `0026a2cc` | snpl_scrdisp() (needs_review) | 260 | 93.85 | 0 | 0 |
| `001caa10` | set_ct_weapon(ACT*) (needs_review) | 248 | 67.74 | 1 | 0 |
| `0025b78c` | houkoku_talkunit(int) (needs_review) | 236 | 86.44 | 1 | 0 |
| `002590e8` | wld_event(int, int) (needs_review) | 236 | 94.92 | 0 | 0 |
| `00285e50` | pspMsgGet(unsigned int) (needs_review) | 232 | 63.79 | 1 | 0 |
| `00265fd8` | wldpac_init() (needs_review) | 224 | 87.5 | 0 | 0 |
| `0021d544` | getNextSENo(int) (needs_review) | 220 | 80.0 | 1 | 0 |
| `002867a8` | getMovieEventNum(int) (needs_review) | 216 | 68.52 | 1 | 0 |
| `0026ba18` | wldtown_draw() (needs_review) | 212 | 94.34 | 0 | 0 |
| `0025efe4` | wlddata_load() (needs_review) | 212 | 92.45 | 0 | 0 |
| `00216530` | activateMusic(int, int, int) (needs_review) | 212 | 94.34 | 0 | 0 |
| `001e2124` | afterskillhandle(BWORK*) (needs_review) | 212 | 86.79 | 0 | 0 |
| `0015a65c` | siOS_TCurSucCheck(unsigned int) (needs_review) | 208 | 78.85 | 1 | 0 |
| `002a37b0` | pspSaveBase::pspSaveBase() (needs_review) | 192 | 93.75 | 0 | 0 |
| `001ce950` | setskillresult_caster(int) (needs_review) | 188 | 87.23 | 0 | 0 |
| `002856fc` | pspItemGetWeaponData (needs_review) | 180 | 93.33 | 0 | 0 |
| `00290dc0` | DrawSync (needs_review) | 172 | 86.05 | 0 | 0 |
| `00258e70` | evt_town_cent() (needs_review) | 172 | 86.05 | 0 | 0 |
| `002b2a94` | SE_SetVol(int, int) (needs_review) | 164 | 92.68 | 0 | 0 |
| `00273d20` | IsNullUnit(int) (needs_review) | 156 | 94.87 | 0 | 0 |
| `00216458` | disposeMusic(int) (needs_review) | 156 | 94.87 | 0 | 0 |
| `002cb0c0` | __gedf2 (needs_review) | 152 | 92.11 | 0 | 0 |
| `0025f1e8` | wldmes_load(int) (needs_review) | 152 | 84.21 | 0 | 0 |
| `002766f4` | GetHightDistance(unsigned char*, BWORK*) (needs_review) | 148 | 94.59 | 0 | 0 |
| `00268be0` | wldcenter_set(_POINT*, SVECTOR*) (needs_review) | 148 | 94.59 | 0 | 0 |
| `0026640c` | wldpac_draw(GsOT*, unsigned long*, int) (needs_review) | 148 | 94.59 | 0 | 0 |
| `002161e0` | loadMusic(int) (needs_review) | 148 | 91.89 | 0 | 0 |
| `0025e204` | wldfade_mask() (needs_review) | 144 | 91.67 | 0 | 0 |
| `002cb4ac` | __aeabi_ul2f (needs_review) | 140 | 82.86 | 0 | 0 |
| `00216154` | loadMusicBuffer(int, int) (needs_review) | 140 | 91.43 | 0 | 0 |
| `00269798` | snpl_wait() (needs_review) | 136 | 88.24 | 0 | 0 |
| `0026a120` | snpl_rndjp() (needs_review) | 132 | 93.94 | 0 | 0 |
| `00269bc0` | snpl_timeset() (needs_review) | 124 | 83.87 | 0 | 0 |
| `0025da0c` | wldkey_repinit() (needs_review) | 124 | 83.87 | 0 | 0 |
| `00159924` | asmTaskEntry() (needs_review) | 124 | 93.55 | 0 | 0 |
| `000ff9ec` | Wload_replaceitems(int, int) (needs_review) | 120 | 56.67 | 1 | 0 |
| `000d7e00` | load_replaceitems(int, int) (needs_review) | 120 | 56.67 | 1 | 0 |
| `002cb830` | __gesf2 (needs_review) | 116 | 89.66 | 0 | 0 |
| `002cabdc` | __aeabi_ul2d (needs_review) | 116 | 75.86 | 0 | 0 |
| `00276c28` | CheckCrystalAndTresureBox() (needs_review) | 112 | 92.86 | 0 | 0 |
| `00269ec8` | snpl_mesput() (needs_review) | 108 | 92.59 | 0 | 0 |
| `002cba30` | __fixunsdfdi (needs_review) | 104 | 92.31 | 0 | 0 |
| `0026b5e4` | ssd_request(int, int) (needs_review) | 104 | 92.31 | 0 | 0 |
| `00269aa0` | snpl_chgpara() (needs_review) | 104 | 92.31 | 0 | 0 |
| `001e6938` | setskilldata(ACT*) (needs_review) | 104 | 92.31 | 0 | 0 |
| `002b29b4` | SE_StopAll() (needs_review) | 100 | 88.0 | 0 | 0 |
| `002775dc` | JudgeMovable(int) (needs_review) | 100 | 92.0 | 0 | 0 |
| `002cd03c` | _Unwind_VRS_Set (needs_review) | 92 | 73.91 | 1 | 0 |
| `002ccfb8` | _Unwind_VRS_Get (needs_review) | 92 | 73.91 | 1 | 0 |
| `0028c768` | CFFT_STATE::AttackTeamFaceIDToUnitATFID(int) (needs_review) | 88 | 90.91 | 0 | 0 |
| `00273cc8` | IsAlmostNullUnit(int) (needs_review) | 88 | 90.91 | 0 | 0 |
| `0025f63c` | wldlop_chk() (needs_review) | 88 | 86.36 | 0 | 0 |
| `001a6530` | ScriptRead(int, TUTRIAL*) (needs_review) | 88 | 90.91 | 0 | 0 |
| `0024b02c` | wldmapEntry(int) (needs_review) | 84 | 90.48 | 0 | 0 |
| `0019e134` | SuccessEmploy() (needs_review) | 84 | 90.48 | 0 | 0 |
| `0028c690` | CFFT_STATE::UnitIDToFID_SP2(int, int) (needs_review) | 80 | 90.0 | 0 | 0 |
| `0026a27c` | snpl_fadein() (needs_review) | 80 | 90.0 | 0 | 0 |
| `002c99b5` | operator new(unsigned int) (needs_review) | 76 | 5.26 | 0 | 0 |
| `0029ae00` | xpLibGetOffset(int*, int*) (needs_review) | 76 | 94.74 | 0 | 0 |
| `00270108` | wldmess_put(int, int, _POINT, unsigned long*) (needs_review) | 76 | 94.74 | 0 | 0 |
| `0026b694` | wldssd_wait() (needs_review) | 76 | 89.47 | 0 | 0 |
| `0026a5b0` | snpl_meswait() (needs_review) | 76 | 89.47 | 0 | 0 |
| `00258f1c` | evt_gil_high() (needs_review) | 76 | 94.74 | 0 | 0 |
| `0029b5d0` | GsSwapDispBuff (needs_review) | 72 | 94.44 | 0 | 0 |
| `0026b64c` | wldmusic_change(int) (needs_review) | 72 | 94.44 | 0 | 0 |
| `00259530` | evt_faith_high() (needs_review) | 72 | 94.44 | 0 | 0 |
| `002594a0` | evt_brave_high() (needs_review) | 72 | 94.44 | 0 | 0 |
| `002592b4` | evt_flag_low() (needs_review) | 72 | 94.44 | 0 | 0 |
| `0025926c` | evt_flag_high() (needs_review) | 72 | 94.44 | 0 | 0 |
| `00259224` | evt_flag() (needs_review) | 72 | 94.44 | 0 | 0 |
| `001d98c8` | check_status_data2(BWORK*, int) (needs_review) | 72 | 94.44 | 0 | 0 |
| `000bd4bc` | CSOUND_LOADER_OGG::~CSOUND_LOADER_OGG() (needs_review) | 72 | 88.89 | 0 | 0 |
| `00277640` | SetThisDestination(unsigned char*) (needs_review) | 68 | 94.12 | 0 | 0 |
| `0026b6e0` | iOSwldssd_wait() (needs_review) | 68 | 88.24 | 0 | 0 |
| `00258fb4` | evt_dead_high() (needs_review) | 68 | 94.12 | 0 | 0 |
| `0028be80` | _ps_test() (needs_review) | 64 | 87.5 | 0 | 0 |
| `00278440` | GetPanelUnderUnit(int, unsigned char*) (needs_review) | 64 | 93.75 | 0 | 0 |
| `00273b38` | SetSafePanelAhead(int) (needs_review) | 64 | 93.75 | 0 | 0 |
| `0026a570` | snpl_fadewait() (needs_review) | 64 | 81.25 | 0 | 0 |
| `00269b80` | snpl_keywait() (needs_review) | 64 | 81.25 | 0 | 0 |
| `0025ee30` | wldload_wait() (needs_review) | 64 | 93.75 | 0 | 0 |
| `000b9fe0` | timeGetTime() (needs_review) | 64 | 93.75 | 0 | 0 |
| `002ca195` | __cxa_begin_cleanup (needs_review) | 60 | 66.67 | 0 | 0 |
| `002b6fe0` | iOSReleaseButtonAreaCheck() (needs_review) | 60 | 93.33 | 0 | 0 |
| `002ab5cc` | GuEmu_Clear() (needs_review) | 60 | 86.67 | 0 | 0 |
| `0029b618` | iOSGsSwapDispBuff() (needs_review) | 60 | 93.33 | 0 | 0 |
| `0028bf7c` | _ps_cond() (needs_review) | 60 | 93.33 | 0 | 0 |
| `0028b6fc` | STEP_DISP(char const*) (needs_review) | 60 | 93.33 | 0 | 0 |
| `00289844` | pspClearSaveData() (needs_review) | 60 | 93.33 | 0 | 0 |
| `00284784` | ColorVectorDataBase(unsigned int) (needs_review) | 60 | 93.33 | 0 | 0 |
| `002819cc` | iOS_v2menuInit() (needs_review) | 60 | 93.33 | 0 | 0 |
| `0026ab70` | snpl_envsndreq() (needs_review) | 60 | 93.33 | 0 | 0 |
| `0026a3d0` | snpl_wordcol() (needs_review) | 60 | 93.33 | 0 | 0 |
| `00249bcc` | vOpn_loadwait() (needs_review) | 60 | 93.33 | 0 | 0 |
| `002431f0` | fRoll_fadeout(short*) (needs_review) | 60 | 86.67 | 0 | 0 |
| `002431b4` | fRoll_fadein(short*) (needs_review) | 60 | 86.67 | 0 | 0 |
| `002164f4` | inactivateMusic() (needs_review) | 60 | 93.33 | 0 | 0 |
| `00213e0c` | stopColorRotation(unsigned int) (needs_review) | 60 | 93.33 | 0 | 0 |
| `001d3d5c` | get_active_unit() (needs_review) | 60 | 93.33 | 0 | 0 |
| `001ca97c` | overlayMonomaneStack() (needs_review) | 60 | 93.33 | 0 | 0 |
| `001c7178` | SelectWindowClutEx(int, int) (needs_review) | 60 | 86.67 | 0 | 0 |
| `001b7bf0` | MenuSelVerticalWithSndDirect(unsigned short, unsigned char, int, int) (needs_review) | 60 | 86.67 | 0 | 0 |
| `001a7368` | IsDismiss(short) (needs_review) | 60 | 93.33 | 0 | 0 |
| `0016f738` | iOS_cacheFilesNameClear() (needs_review) | 60 | 93.33 | 0 | 0 |
| `0015e768` | iOSShiftUnitSet(int) (needs_review) | 60 | 86.67 | 0 | 0 |
| `00155e04` | changewindowamb(int, int, int) (needs_review) | 60 | 80.0 | 0 | 0 |
| `00153768` | Wsend_taskparamater4(long, long, long, long, long) (needs_review) | 60 | 93.33 | 0 | 0 |
| `001534a4` | send_taskparamater4(long, long, long, long, long) (needs_review) | 60 | 93.33 | 0 | 0 |
| `00101980` | Wsend_sttslinecol(char*) (needs_review) | 60 | 93.33 | 0 | 0 |
| `000ab9cc` | CEGL2_SHADER::CEGL2_SHADER() (needs_review) | 60 | 93.33 | 0 | 0 |
| `0009403c` | _vp_global_look (needs_review) | 60 | 93.33 | 0 | 0 |
| `002bf32c` | Debug_SetDebugDirectBtn(int) (needs_review) | 56 | 92.86 | 0 | 0 |
| `002b88c8` | iOS_StartMovie() (needs_review) | 56 | 85.71 | 0 | 0 |
| `002a2f60` | PCopen (needs_review) | 56 | 92.86 | 0 | 0 |
| `0029aa84` | OpenTIM (needs_review) | 56 | 85.71 | 0 | 0 |
| `0028daac` | tlGetHeapSize() (needs_review) | 56 | 92.86 | 0 | 0 |
| `0028da58` | tlDumpHeap() (needs_review) | 56 | 92.86 | 0 | 0 |
| `0028c288` | CFFT_STATE::GetBackdropColor(float*, float*, float*) (needs_review) | 56 | 57.14 | 1 | 0 |
| `00280558` | iOS_fftLoad(int) (needs_review) | 56 | 85.71 | 0 | 0 |
| `0027fc80` | cSaveFFT::Destroy() (needs_review) | 56 | 92.86 | 0 | 0 |
| `0027b4a4` | initCmdKind() (needs_review) | 56 | 85.71 | 0 | 0 |
| `0026a824` | snpl_snsndreq() (needs_review) | 56 | 92.86 | 0 | 0 |
| `00269d78` | snpl_clrlocal() (needs_review) | 56 | 85.71 | 0 | 0 |
| `00269d40` | snpl_setlocal() (needs_review) | 56 | 85.71 | 0 | 0 |
| `00269d08` | snpl_clrstat() (needs_review) | 56 | 85.71 | 0 | 0 |
| `00269cd0` | snpl_setstat() (needs_review) | 56 | 85.71 | 0 | 0 |
| `00269a68` | snpl_hidepara() (needs_review) | 56 | 85.71 | 0 | 0 |
| `00258c40` | evt_wldinfo() (needs_review) | 56 | 92.86 | 0 | 0 |
| `0021ce78` | IsPermanentEffect(long) (needs_review) | 56 | 92.86 | 0 | 0 |
| `0021b4a8` | GetSQLFrameRate(_EffectTCB*) (needs_review) | 56 | 92.86 | 0 | 0 |
| `0021b0d0` | InitEffectLoadAddress() (needs_review) | 56 | 85.71 | 0 | 0 |
| `00200b80` | endTrunAction() (needs_review) | 56 | 92.86 | 0 | 0 |
| `001f5f44` | iOS_resetAnimationIrowake() (needs_review) | 56 | 92.86 | 0 | 0 |
| `001d3d24` | gc_bwp(int) (needs_review) | 56 | 92.86 | 0 | 0 |
| `001d1ce8` | erase_unit_f(int) (needs_review) | 56 | 92.86 | 0 | 0 |
| `001ceca0` | _rand_() (needs_review) | 56 | 85.71 | 0 | 0 |
| `001cec24` | copy_target_table2(unsigned char*) (needs_review) | 56 | 92.86 | 0 | 0 |
| `0019f718` | iOSShopHelpStatusCheck() (needs_review) | 56 | 92.86 | 0 | 0 |
| `00100594` | Wpopmessagepacket() (needs_review) | 56 | 85.71 | 0 | 0 |
| `000ffac4` | Wgetvaluelength(int) (needs_review) | 56 | 92.86 | 0 | 0 |
| `000e0f68` | loadcsrc(int, int, int, int) (needs_review) | 56 | 92.86 | 0 | 0 |
| `000d88c4` | popmessagepacket() (needs_review) | 56 | 85.71 | 0 | 0 |
| `000d7ed8` | getvaluelength(int) (needs_review) | 56 | 92.86 | 0 | 0 |
| `002c5400` | Movie_FrameMove() (needs_review) | 52 | 92.31 | 0 | 0 |
| `002a242c` | RotColorDpq_nom (needs_review) | 52 | 92.31 | 0 | 0 |
| `002a0844` | ReadRotMatrix (needs_review) | 52 | 92.31 | 0 | 0 |
| `0027f14c` | iOS_ClearRectHitAll() (needs_review) | 52 | 92.31 | 0 | 0 |
| `0027b4dc` | setCmdKind(unsigned int) (needs_review) | 52 | 84.62 | 0 | 0 |
| `0026c3cc` | ctltresure_active(CTLINFO*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `002675c0` | ctlret_active(CTLINFO*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `002602c0` | ctlmouke_active(CTLINFO*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `00259e70` | ctlhouk_active(CTLINFO*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `00258e3c` | evt_town_clr() (needs_review) | 52 | 92.31 | 0 | 0 |
| `00258e08` | evt_town_set() (needs_review) | 52 | 92.31 | 0 | 0 |
| `0024e8d0` | ctlperson_active(CTLINFO*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `0024dc8c` | ctlkiroku_active(CTLINFO*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `00245b34` | o_ClearCardEvent_X() (needs_review) | 52 | 92.31 | 0 | 0 |
| `00245a74` | o_ClearCardEvent() (needs_review) | 52 | 92.31 | 0 | 0 |
| `00243014` | fRoll_exit(short*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `00228e64` | startShape() (needs_review) | 52 | 92.31 | 0 | 0 |
| `0021b474` | GetMSQFrameRate(_EffectTCB*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `002119f4` | PopChangePalette() (needs_review) | 52 | 84.62 | 0 | 0 |
| `002119c0` | PushChangePalette() (needs_review) | 52 | 84.62 | 0 | 0 |
| `0020f574` | getMapXYZ(SVECTOR*) (needs_review) | 52 | 76.92 | 0 | 0 |
| `0020eddc` | inactivateEventAnimation(int) (needs_review) | 52 | 92.31 | 0 | 0 |
| `0020da48` | pushBackColor() (needs_review) | 52 | 84.62 | 0 | 0 |
| `0020d808` | popMapAngle() (needs_review) | 52 | 84.62 | 0 | 0 |
| `0020d7d4` | pushMapAngle() (needs_review) | 52 | 84.62 | 0 | 0 |
| `001fd278` | startInterventionMode() (needs_review) | 52 | 84.62 | 0 | 0 |
| `001f36c8` | EndAllAnimation() (needs_review) | 52 | 92.31 | 0 | 0 |
| `001eb760` | myStartShape() (needs_review) | 52 | 84.62 | 0 | 0 |
| `001d9370` | get_joblevel(unsigned short) (needs_review) | 52 | 92.31 | 0 | 0 |
| `001cb030` | clear_setstatus(A_RESULT*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `001a63dc` | bak_read(int, void*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `00161e2c` | iOSIsCurMode() (needs_review) | 52 | 92.31 | 0 | 0 |
| `00153734` | Wsend_taskparamater(long, long, long, long) (needs_review) | 52 | 92.31 | 0 | 0 |
| `00153470` | send_taskparamater(long, long, long, long) (needs_review) | 52 | 92.31 | 0 | 0 |
| `0012f2a8` | iOSPersonalWinPos(int) (needs_review) | 52 | 84.62 | 0 | 0 |
| `000e7488` | getCodeLength(unsigned char*) (needs_review) | 52 | 92.31 | 0 | 0 |
| `000bd538` | CSOUND_LOADER_OGG::CSOUND_LOADER_OGG() (needs_review) | 52 | 92.31 | 0 | 0 |
| `002b23a8` | Music_Pause() (needs_review) | 48 | 91.67 | 0 | 0 |
| `002b2378` | Music_Stop() (needs_review) | 48 | 91.67 | 0 | 0 |
| `002b2260` | RETINA_SCALE(int) (needs_review) | 48 | 91.67 | 0 | 0 |
| `002a38a8` | pspSaveList::pspSaveList() (needs_review) | 48 | 91.67 | 0 | 0 |
| `002a2ff8` | xpInitHeap (needs_review) | 48 | 91.67 | 0 | 0 |
| `002a14a8` | ReadColorMatrix (needs_review) | 48 | 91.67 | 0 | 0 |
| `002a145c` | ReadLightMatrix (needs_review) | 48 | 91.67 | 0 | 0 |
| `0028e6a4` | xpInitVblankFunc() (needs_review) | 48 | 83.33 | 0 | 0 |
| `0028e538` | CdRead (needs_review) | 48 | 91.67 | 0 | 0 |
| `0028ba54` | TE_task_create(int, void (*)(), int) (needs_review) | 48 | 91.67 | 0 | 0 |
| `00289970` | pspIsNoneSaveData(int) (needs_review) | 48 | 91.67 | 0 | 0 |
| `0027fc48` | cSaveFFT::Create(char*) (needs_review) | 48 | 91.67 | 0 | 0 |
| `00270460` | curhis_get(int) (needs_review) | 48 | 83.33 | 0 | 0 |
| `00269e98` | snpl_exit() (needs_review) | 48 | 91.67 | 0 | 0 |
| `0026998c` | snpl_subpara() (needs_review) | 48 | 91.67 | 0 | 0 |
| `0026995c` | snpl_addpara() (needs_review) | 48 | 91.67 | 0 | 0 |
| `0025ffb0` | iOSSDNovelGetOT(int) (needs_review) | 48 | 83.33 | 0 | 0 |
| `0025f138` | townpic_load(int) (needs_review) | 48 | 91.67 | 0 | 0 |
| `0024ad94` | openEntry(int) (needs_review) | 48 | 91.67 | 0 | 0 |
| `0024932c` | vOpn_loopinit() (needs_review) | 48 | 83.33 | 0 | 0 |
| `002433ac` | fRoll_cdxafout(short*) (needs_review) | 48 | 91.67 | 0 | 0 |
| `0024337c` | fRoll_cdxafin(short*) (needs_review) | 48 | 91.67 | 0 | 0 |
| `00243184` | fRoll_scroll(short*) (needs_review) | 48 | 91.67 | 0 | 0 |
| `0021b860` | SetGravity(Vector*) (needs_review) | 48 | 91.67 | 0 | 0 |
| `00215d2c` | battleFileRead() (needs_review) | 48 | 83.33 | 0 | 0 |
| `00213e48` | stopAllColorRotation() (needs_review) | 48 | 91.67 | 0 | 0 |
| `00204298` | startRightTurn(int) (needs_review) | 48 | 91.67 | 0 | 0 |
| `00204268` | startLeftTurn(int) (needs_review) | 48 | 91.67 | 0 | 0 |
| `00202150` | standerdExecution() (needs_review) | 48 | 91.67 | 0 | 0 |
| `001eedf4` | getWpnSequenceAddress(unsigned short) (needs_review) | 48 | 83.33 | 0 | 0 |
| `001e4f0c` | get_fusui_ability(BWORK*) (needs_review) | 48 | 83.33 | 0 | 0 |
| `001dc914` | set_cco_SD(BWORK*) (needs_review) | 48 | 91.67 | 0 | 0 |
| `001d2e6c` | get_coord_address(BWORK*) (needs_review) | 48 | 91.67 | 0 | 0 |
| `001d1db8` | leave_unit_f(int) (needs_review) | 48 | 91.67 | 0 | 0 |
| `0015e068` | iOSNumberGet(int) (needs_review) | 48 | 91.67 | 0 | 0 |
| `001536e4` | Wwait_taskend(long) (needs_review) | 48 | 91.67 | 0 | 0 |
| `00153420` | wait_taskend(long) (needs_review) | 48 | 91.67 | 0 | 0 |
| `0010229c` | Wgeteventcategory() (needs_review) | 48 | 83.33 | 0 | 0 |
| `001020f8` | Wevent_init_system() (needs_review) | 48 | 91.67 | 0 | 0 |
| `000e0538` | import_localpad(int) (needs_review) | 48 | 83.33 | 0 | 0 |
| `000da6d0` | geteventcategory() (needs_review) | 48 | 83.33 | 0 | 0 |
| `000da47c` | event_init_system() (needs_review) | 48 | 91.67 | 0 | 0 |
| `002b23d8` | Music_Replay() (needs_review) | 44 | 90.91 | 0 | 0 |
| `002a0900` | MulRotMatrix0 (needs_review) | 44 | 90.91 | 0 | 0 |
| `0028baa4` | TE_task_stop(long) (needs_review) | 44 | 90.91 | 0 | 0 |
| `0028a054` | pspClearCurrentSystemFile() (needs_review) | 44 | 90.91 | 0 | 0 |
| `0028846c` | free_hight_font() (needs_review) | 44 | 90.91 | 0 | 0 |
| `00287044` | get_timing_true() (needs_review) | 44 | 90.91 | 0 | 0 |
| `00280590` | GetAbilityName(int) (needs_review) | 44 | 81.82 | 0 | 0 |
| `0027f180` | iOS_ClearRectHit(int) (needs_review) | 44 | 90.91 | 0 | 0 |
| `0027b53c` | LoadImage_menuData() (needs_review) | 44 | 90.91 | 0 | 0 |
| `0027334c` | SetDestUnit(int) (needs_review) | 44 | 90.91 | 0 | 0 |
| `00269e6c` | snpl_sndstop() (needs_review) | 44 | 90.91 | 0 | 0 |
| `00269930` | snpl_setpara() (needs_review) | 44 | 90.91 | 0 | 0 |
| `00256e9c` | ctltownmenu_deactive(CTLINFO*) (needs_review) | 44 | 90.91 | 0 | 0 |
| `00256e70` | ctltownmenu_active(CTLINFO*) (needs_review) | 44 | 90.91 | 0 | 0 |
| `00249474` | vOpn_fadein(int) (needs_review) | 44 | 90.91 | 0 | 0 |
| `00243560` | fRoll_xawait(short*) (needs_review) | 44 | 90.91 | 0 | 0 |
| `0021ceb0` | WhoUnlockEffect(long) (needs_review) | 44 | 90.91 | 0 | 0 |
| `0021b8c4` | PopGravity() (needs_review) | 44 | 90.91 | 0 | 0 |
| `001d951c` | get_effectdata(unsigned short) (needs_review) | 44 | 90.91 | 0 | 0 |
| `001d94f0` | get_rangedata(unsigned short) (needs_review) | 44 | 90.91 | 0 | 0 |
| `001d6404` | set_guard_status(int) (needs_review) | 44 | 90.91 | 0 | 0 |
| `001d2968` | get_bwp(int) (needs_review) | 44 | 90.91 | 0 | 0 |
| `001d1d8c` | disappare_unit_f(int) (needs_review) | 44 | 90.91 | 0 | 0 |
| `001cb878` | bcp_roll(BWORK*) (needs_review) | 44 | 90.91 | 0 | 0 |
| `0015df10` | iOSGT4_MapT9Get(unsigned long) (needs_review) | 44 | 90.91 | 0 | 0 |
| `00159a28` | asmGetActiveF() (needs_review) | 44 | 81.82 | 0 | 0 |
| `001599fc` | asmGetInput3() (needs_review) | 44 | 81.82 | 0 | 0 |
| `001599d0` | asmGetInput2() (needs_review) | 44 | 81.82 | 0 | 0 |
| `001021dc` | Wset_autobattletarget(int, int) (needs_review) | 44 | 90.91 | 0 | 0 |
| `00101624` | Whook_disp_option() (needs_review) | 44 | 90.91 | 0 | 0 |
| `000fea78` | Wallocatewindowinit() (needs_review) | 44 | 90.91 | 0 | 0 |
| `000da610` | set_autobattletarget(int, int) (needs_review) | 44 | 90.91 | 0 | 0 |
| `000d9810` | hook_disp_option() (needs_review) | 44 | 90.91 | 0 | 0 |
| `000d6f54` | allocatewindowinit() (needs_review) | 44 | 90.91 | 0 | 0 |
| `002cb484` | __floatunsisf (needs_review) | 40 | 80.0 | 0 | 0 |
| `002b7a34` | SetDisableMapTouchRect(RECT16*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `002b2404` | Music_SetVol(int, int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `002b2238` | IS_TEX_2X() (needs_review) | 40 | 90.0 | 0 | 0 |
| `002a25f8` | read_mt(long*, long*, long*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `002a1b1c` | read_rgb_fifo(long*, long*, long*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `002a1aac` | read_sxsy_fifo3(long*, long*, long*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0028dc30` | SetRCnt (needs_review) | 40 | 90.0 | 0 | 0 |
| `0028c668` | CFFT_STATE::UnitIDToFID_SPR(int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0028b3f0` | pspWorldDataRectSet(RECT16*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `002808b8` | iOS_initTransFace() (needs_review) | 40 | 90.0 | 0 | 0 |
| `0027fbc8` | iOS_WorldMapResumeGetData(unsigned char**, unsigned int*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0026b0b8` | snpl_musicreq() (needs_review) | 40 | 90.0 | 0 | 0 |
| `0026a64c` | snplinf_init(int) (needs_review) | 40 | 80.0 | 0 | 0 |
| `0026a1a4` | snpl_sndreq() (needs_review) | 40 | 90.0 | 0 | 0 |
| `00267340` | iOS_add_anmpac_max(int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0024adc4` | endEntry() (needs_review) | 40 | 90.0 | 0 | 0 |
| `002494a0` | vOpn_fadeout(int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `00246360` | ctlstartmov_main(CTLINFO*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `002231b0` | GetReachableHeight(int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `00218dcc` | InitCamera() (needs_review) | 40 | 90.0 | 0 | 0 |
| `0021695c` | stopAllEffect() (needs_review) | 40 | 90.0 | 0 | 0 |
| `0020f5a8` | getMapSize(SVECTOR*) (needs_review) | 40 | 80.0 | 0 | 0 |
| `0020d84c` | setMapAngle(SVECTOR*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0020d5d8` | setMapScale(VECTOR*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0020d2b8` | setMapScroll(VECTOR*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0020d060` | setMapScrollXYZ(VECTOR*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0020c99c` | initFileBuffer() (needs_review) | 40 | 90.0 | 0 | 0 |
| `0020c74c` | initSoundHeap() (needs_review) | 40 | 90.0 | 0 | 0 |
| `0020c600` | warningHandler(int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0020c5d8` | errorHandler(int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `001fd2c4` | endInterventionMode() (needs_review) | 40 | 80.0 | 0 | 0 |
| `001eedcc` | getWpnShapeAddress(unsigned short) (needs_review) | 40 | 80.0 | 0 | 0 |
| `001d8d28` | get_jobdata(int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `001d73ec` | clear_unitwork() (needs_review) | 40 | 90.0 | 0 | 0 |
| `001cebfc` | set_target_table2(unsigned char*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `001ceaec` | set_status_all_sp(int, int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `001cb7d4` | check_reaction_deny(BWORK*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `001ca954` | net_getknockback(unsigned char*, unsigned char*, unsigned char*) (needs_review) | 40 | 90.0 | 0 | 0 |
| `001baea0` | unitans_init() (needs_review) | 40 | 90.0 | 0 | 0 |
| `001a3eb4` | PoachUnit() (needs_review) | 40 | 90.0 | 0 | 0 |
| `001875f0` | GetSaveDataInit() (needs_review) | 40 | 90.0 | 0 | 0 |
| `0015ebf4` | iOSMapTouchCancel() (needs_review) | 40 | 80.0 | 0 | 0 |
| `0015e040` | iOSActUnitCurSet() (needs_review) | 40 | 90.0 | 0 | 0 |
| `001599a8` | asmGetInput1() (needs_review) | 40 | 80.0 | 0 | 0 |
| `00155cec` | tutorialstatusget(int) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0012f19c` | get_pitno() (needs_review) | 40 | 90.0 | 0 | 0 |
| `0010f8cc` | Wjobstts_call(unsigned long*, unsigned long) (needs_review) | 40 | 90.0 | 0 | 0 |
| `0010de7c` | Wimport_localpad(int) (needs_review) | 40 | 80.0 | 0 | 0 |
| `0010278c` | Wsettaskkind(int) (needs_review) | 40 | 80.0 | 0 | 0 |
| `001024bc` | Wreaded_mapchange() (needs_review) | 40 | 90.0 | 0 | 0 |
| `000e0eec` | jobstts_call(unsigned long*, unsigned long) (needs_review) | 40 | 90.0 | 0 | 0 |
| `000daac0` | settaskkind(int) (needs_review) | 40 | 80.0 | 0 | 0 |
| `000bceac` | CSOUND_LOADER_PCM::CSOUND_LOADER_PCM() (needs_review) | 40 | 90.0 | 0 | 0 |
| `000829ec` | oggpackB_writecopy (needs_review) | 40 | 90.0 | 0 | 0 |
| `000829c4` | oggpack_writecopy (needs_review) | 40 | 90.0 | 0 | 0 |
| `002a1408` | SetFogFar (needs_review) | 36 | 88.89 | 0 | 0 |
| `0029b654` | GsSetClip2D (needs_review) | 36 | 88.89 | 0 | 0 |
| `0029a834` | ClearImage (needs_review) | 36 | 77.78 | 0 | 0 |
| `00294e64` | GetDrawEnv (needs_review) | 36 | 88.89 | 0 | 0 |
| `0029128c` | MoveImage (needs_review) | 36 | 77.78 | 0 | 0 |
| `00291154` | StoreImage (needs_review) | 36 | 77.78 | 0 | 0 |
| `00291074` | PSX_LoadImage (needs_review) | 36 | 77.78 | 0 | 0 |
| `0028de4c` | DisableEvent (needs_review) | 36 | 88.89 | 0 | 0 |
| `0028de28` | EnableEvent (needs_review) | 36 | 88.89 | 0 | 0 |
| `0028d228` | tlPopHeap() (needs_review) | 36 | 77.78 | 0 | 0 |
| `0028c644` | CFFT_STATE::FaceIDToFID(int) (needs_review) | 36 | 88.89 | 0 | 0 |
| `0028bad0` | TE_is_task_end(long) (needs_review) | 36 | 88.89 | 0 | 0 |
| `00284494` | Clear_VectorDataBase() (needs_review) | 36 | 88.89 | 0 | 0 |
| `002806cc` | iOS_HookAddPrim() (needs_review) | 36 | 88.89 | 0 | 0 |
| `0027fbf0` | iOS_WorldMapResumeGetData2(unsigned char**, unsigned int*) (needs_review) | 36 | 88.89 | 0 | 0 |
| `0026c238` | iOSNovelModeBackup() (needs_review) | 36 | 88.89 | 0 | 0 |
| `00269b08` | snpl_effmode() (needs_review) | 36 | 88.89 | 0 | 0 |
| `00269774` | snpl_jp() (needs_review) | 36 | 88.89 | 0 | 0 |
| `00263fa8` | iOSSDNovelSysCurCheck() (needs_review) | 36 | 88.89 | 0 | 0 |
| `0021b244` | SetEditTSQPtr() (needs_review) | 36 | 77.78 | 0 | 0 |
| `0021b220` | SetEditANMPtr() (needs_review) | 36 | 77.78 | 0 | 0 |
| `00216860` | stopMusic() (needs_review) | 36 | 88.89 | 0 | 0 |
| `0020f514` | stopAnimation() (needs_review) | 36 | 88.89 | 0 | 0 |
| `0020d5a4` | popMapScale() (needs_review) | 36 | 77.78 | 0 | 0 |
| `0020d580` | pushMapScale() (needs_review) | 36 | 77.78 | 0 | 0 |
| `0020d284` | popMapScroll() (needs_review) | 36 | 77.78 | 0 | 0 |
| `0020d260` | pushMapScroll() (needs_review) | 36 | 77.78 | 0 | 0 |
| `0020d02c` | popMapScrollXYZ() (needs_review) | 36 | 77.78 | 0 | 0 |
| `0020d008` | pushMapScrollXYZ() (needs_review) | 36 | 77.78 | 0 | 0 |
| `001fd1dc` | nextTurnOrder() (needs_review) | 36 | 88.89 | 0 | 0 |
| `001f4a64` | initEntryEnemyAnimations(int) (needs_review) | 36 | 88.89 | 0 | 0 |
| `001eb2d8` | vramDeleteUsed() (needs_review) | 36 | 88.89 | 0 | 0 |
| `001ca580` | get_net_rival_weapon_range() (needs_review) | 36 | 88.89 | 0 | 0 |
| `001baac4` | event_warning(short, int) (needs_review) | 36 | 88.89 | 0 | 0 |
| `0018e334` | equans_init() (needs_review) | 36 | 88.89 | 0 | 0 |
| `00161d74` | iOSPosH(int) (needs_review) | 36 | 88.89 | 0 | 0 |
| `00161d50` | iOSPosW(int) (needs_review) | 36 | 88.89 | 0 | 0 |
| `0015deec` | iOSGT4_MapT9(unsigned long, long) (needs_review) | 36 | 88.89 | 0 | 0 |
| `0015391c` | check_eventtool(int, int) (needs_review) | 36 | 88.89 | 0 | 0 |
| `00153638` | Wtask_stop(long) (needs_review) | 36 | 88.89 | 0 | 0 |
| `00153614` | Wtask_start(long) (needs_review) | 36 | 88.89 | 0 | 0 |
| `00153374` | task_stop(long) (needs_review) | 36 | 88.89 | 0 | 0 |
| `00153350` | task_start(long) (needs_review) | 36 | 88.89 | 0 | 0 |
| `000da7e4` | readed_mapchange() (needs_review) | 36 | 88.89 | 0 | 0 |
| `002ccf98` | _Unwind_DeleteException (needs_review) | 32 | 62.5 | 0 | 0 |
| `002b871c` | iOS_isTouchBegan() (needs_review) | 32 | 87.5 | 0 | 0 |
| `002b2358` | Music_Play(int, int, int, int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `002b01e0` | GlTexEnv_GetTextureHandle_2X(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `002ae8e0` | GlTexEnv_GetTextureHandle(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `002ae8c0` | GlTexEnv_GetSprite(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `002a2ce0` | PCwrite (needs_review) | 32 | 87.5 | 0 | 0 |
| `002a2ca8` | PClseek (needs_review) | 32 | 87.5 | 0 | 0 |
| `002a2c70` | PCread (needs_review) | 32 | 87.5 | 0 | 0 |
| `002a1350` | ReadGeomOffset (needs_review) | 32 | 87.5 | 0 | 0 |
| `0029ae70` | xpLib_GetTPage(int*) (needs_review) | 32 | 87.5 | 0 | 0 |
| `00294e44` | GetDispEnv (needs_review) | 32 | 87.5 | 0 | 0 |
| `0028ce58` | sceCtrlPeekBufferPositive (needs_review) | 32 | 87.5 | 0 | 0 |
| `0028ba84` | TE_task_start(long) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0028b610` | initXpHeap() (needs_review) | 32 | 87.5 | 0 | 0 |
| `00288a58` | pspPrimDirectParamSet(int, RECT16*) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0028082c` | IOS_PSP2IOS_Y(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0028080c` | IOS_PSP2IOS_X(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0027f620` | iOS_ResumeGetData(unsigned char**, unsigned int*) (needs_review) | 32 | 75.0 | 0 | 0 |
| `00270500` | curhis_clr(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0026df10` | ctlhentuto_active(CTLINFO*) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0024f4b0` | ctltips_active(CTLINFO*) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0021f308` | PermanentEffectEndRequest(unsigned char) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0021cefc` | LockEffectCompelBreak() (needs_review) | 32 | 87.5 | 0 | 0 |
| `0021cedc` | UnlockEffect() (needs_review) | 32 | 87.5 | 0 | 0 |
| `0021b8a4` | PushGravity() (needs_review) | 32 | 87.5 | 0 | 0 |
| `002119a0` | ResetChangePalette() (needs_review) | 32 | 87.5 | 0 | 0 |
| `0020f8cc` | setFrameRate(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0020696c` | iOS_IsEnableFlicker() (needs_review) | 32 | 87.5 | 0 | 0 |
| `002064a8` | iOS_IsEnableMenuItemTouch() (needs_review) | 32 | 87.5 | 0 | 0 |
| `00202efc` | iOS_BattleEventCheck() (needs_review) | 32 | 87.5 | 0 | 0 |
| `001d66f8` | set_td(unsigned char*) (needs_review) | 32 | 87.5 | 0 | 0 |
| `001b9d84` | iOS_clearTutorialbreak() (needs_review) | 32 | 87.5 | 0 | 0 |
| `001adc48` | FadeCondition() (needs_review) | 32 | 87.5 | 0 | 0 |
| `0015c01c` | iOSTchHoseiControl() (needs_review) | 32 | 87.5 | 0 | 0 |
| `0015bf38` | iOSTchMovingModeCheck() (needs_review) | 32 | 87.5 | 0 | 0 |
| `0015a5ec` | siOS_TCurGet(unsigned int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0015832c` | rewrite_worldscroll(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `00155c8c` | stop_adventuremessage(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `00153c84` | iOS_updateDispCameraIconSetting() (needs_review) | 32 | 87.5 | 0 | 0 |
| `00153714` | Wtask_status(long) (needs_review) | 32 | 87.5 | 0 | 0 |
| `00153450` | task_status(long) (needs_review) | 32 | 87.5 | 0 | 0 |
| `001022cc` | Wchk_nexteventtype(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `001005ec` | Wstartmenutransfer() (needs_review) | 32 | 87.5 | 0 | 0 |
| `001005cc` | Wstopmenutransfer() (needs_review) | 32 | 87.5 | 0 | 0 |
| `000da700` | chk_nexteventtype(int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `000d891c` | startmenutransfer() (needs_review) | 32 | 87.5 | 0 | 0 |
| `000d88fc` | stopmenutransfer() (needs_review) | 32 | 87.5 | 0 | 0 |
| `000c8178` | tool_readsquare(int, int, int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `000c8158` | tool_writesquare(int, int, int) (needs_review) | 32 | 87.5 | 0 | 0 |
| `002befa0` | iOS_OrMenuTouchKeyInput(unsigned int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `002b7034` | iOSCancelButtonCheck() (needs_review) | 28 | 85.71 | 0 | 0 |
| `002b242c` | Music_IsPlaying() (needs_review) | 28 | 85.71 | 0 | 0 |
| `002b1bcc` | NowLoading_Bootup() (needs_review) | 28 | 71.43 | 0 | 0 |
| `002acb2c` | GuEmu_GetRAW(int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `002a2b10` | xpPadDebugSet (needs_review) | 28 | 85.71 | 0 | 0 |
| `002a2a4c` | xpPadKeyBufGet (needs_review) | 28 | 85.71 | 0 | 0 |
| `002a148c` | SetColorMatrix (needs_review) | 28 | 85.71 | 0 | 0 |
| `002a1440` | SetLightMatrix (needs_review) | 28 | 85.71 | 0 | 0 |
| `0029fed4` | PSX_ccos (needs_review) | 28 | 85.71 | 0 | 0 |
| `0029fea0` | rcos (needs_review) | 28 | 85.71 | 0 | 0 |
| `00290e6c` | DrawSyncCallback (needs_review) | 28 | 85.71 | 0 | 0 |
| `0028e6d4` | xpSetWaitVSyncFunc(int (*)()) (needs_review) | 28 | 85.71 | 0 | 0 |
| `0028e5c4` | VSyncCallback (needs_review) | 28 | 85.71 | 0 | 0 |
| `0028da90` | tlMallocErrorFunc(void (*)(TL_MALLOC_ERROR)) (needs_review) | 28 | 85.71 | 0 | 0 |
| `0028b034` | pspWorldDisableFlg(PSP_WORLD_FLG) (needs_review) | 28 | 85.71 | 0 | 0 |
| `0028b018` | pspWorldEnableFlg(PSP_WORLD_FLG) (needs_review) | 28 | 85.71 | 0 | 0 |
| `002885d4` | pspOpenEnableFlg(PSP_OPEN_FLG) (needs_review) | 28 | 85.71 | 0 | 0 |
| `002885b8` | pspOpenDisableFlg(PSP_OPEN_FLG) (needs_review) | 28 | 85.71 | 0 | 0 |
| `00281678` | iOS_v2menuGetItem() (needs_review) | 28 | 85.71 | 0 | 0 |
| `0026c25c` | iOSNovelModeRestore() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00269758` | snpl_startpage() (needs_review) | 28 | 85.71 | 0 | 0 |
| `0026973c` | snpl_endpage() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258b54` | evt_eqp() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258b38` | evt_item() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258b1c` | evt_skip4() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258b00` | evt_skip3() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258ae4` | evt_skip2() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258ac8` | evt_skip1() (needs_review) | 28 | 85.71 | 0 | 0 |
| `0024d948` | iOS_BRST_CHECK() (needs_review) | 28 | 85.71 | 0 | 0 |
| `0024b080` | wldbinEntry() (needs_review) | 28 | 85.71 | 0 | 0 |
| `0021f2ec` | GetPEffectStatus(unsigned char) (needs_review) | 28 | 85.71 | 0 | 0 |
| `001d751c` | erase_unit(int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `001d357c` | set_playerwork2(PENTRY*, unsigned char*) (needs_review) | 28 | 85.71 | 0 | 0 |
| `001ca938` | net_setknockback(unsigned char, unsigned char, unsigned char) (needs_review) | 28 | 85.71 | 0 | 0 |
| `001c7218` | TEST_TEST() (needs_review) | 28 | 85.71 | 0 | 0 |
| `001b70f4` | DrawMessageWithPosition(int, COMRECORD*, int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `001a8604` | Mituryo(short) (needs_review) | 28 | 85.71 | 0 | 0 |
| `00196ea0` | MenuSelSideDirect(unsigned char, unsigned char) (needs_review) | 28 | 85.71 | 0 | 0 |
| `0018378c` | fileclose(unsigned int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `00159a54` | asmGetActiveTask(int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `00155c5c` | ret_optionstatus() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00155870` | set_worldmoney(int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `00155854` | set_worldday(int, int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `00101fa4` | Wchangeflame(int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `0010155c` | WiOS_battle_scrollwindow_tap() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00101434` | Wsetplatetime(int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `000e62a8` | Set_bravebreak(unsigned short) (needs_review) | 28 | 85.71 | 0 | 0 |
| `000e628c` | Get_bravebreak() (needs_review) | 28 | 85.71 | 0 | 0 |
| `000d9748` | iOS_battle_scrollwindow_tap() (needs_review) | 28 | 85.71 | 0 | 0 |
| `000d961c` | setplatetime(int) (needs_review) | 28 | 85.71 | 0 | 0 |
| `000726e0` | JNI_OnLoad (needs_review) | 28 | 85.71 | 0 | 0 |
| `002c53e8` | Movie_Init() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002befbc` | iOS_ClearMenuTouchKeyInput() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002bef4c` | iOS_isExistResumeData() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002b7a74` | ClearDisableMapTouch() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002b7a5c` | SetDisableMapTouch() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002b701c` | iOSHelpButtonCheck() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002b376c` | Error_SetError(int, char*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002b36bc` | Error_Init() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002ab608` | GuEmu_SetLineInterval(int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2fb8` | PCcreat (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2b44` | xpPadKeyTblGet (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2b2c` | xpPadKeyTblSet (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2af8` | xpPadRepeatGet (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2ae0` | xpPadPspPadDataGet (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2ac8` | xpPadAnalogYGet (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2ab0` | xpPadAnalogXGet (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2a98` | xpPadGet (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2a80` | xpPadTriggerGet (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2a68` | xpPadWorkBufGet (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2a34` | xpPadUpdateData (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a2728` | xpPadAnalogAssign (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a25e0` | read_opz(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a25c8` | read_otz(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a1ba4` | read_p(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a1b8c` | read_flag(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a1b74` | read_rgb2(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a1b5c` | read_rgb1(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a1b44` | read_rgb0(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a1b04` | read_sxsy2(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a1aec` | read_sxsy1(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a1ad4` | read_sxsy0(long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a13f0` | SetFogNearFar (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a1324` | SetGeomOffset (needs_review) | 24 | 83.33 | 0 | 0 |
| `0029febc` | PSX_csin (needs_review) | 24 | 83.33 | 0 | 0 |
| `0029fe88` | rsin (needs_review) | 24 | 83.33 | 0 | 0 |
| `0029fe70` | InitGeom (needs_review) | 24 | 83.33 | 0 | 0 |
| `0029fdbc` | GteSetDataReg(long, long) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0029fd90` | GteGetDataReg(int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0029b6d0` | GsSetWorkBase (needs_review) | 24 | 83.33 | 0 | 0 |
| `0028d688` | tlFreeAll() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0028b3c4` | pspWorldDataBackBufGet(int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0028b068` | pspWorldCallBackSet(PSP_WORLD_CALLBACK_ID, void (*)()) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0028b050` | pspWorldCheckFlg(PSP_WORLD_FLG) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0028a114` | FFT_GetCurrentSystemFile() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00289880` | pspClearSaveEnv() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0028982c` | pspPrimReetWorkBuf_current() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00288f18` | pspgFreamBufCountCountReset() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002885a0` | pspOpenCheckFlg(PSP_OPEN_FLG) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00287588` | reset_g_NetIcon_DrawFlg() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002847c0` | new_ColorVectorDataBase(unsigned int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00283fb0` | mapclip_setpath(char*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0028164c` | iOS_v2menuSetScreenSize(int, int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002806f0` | iOS_clearDebugPrimNum() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00280540` | iOS_fftSave() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0027f608` | Resume_Get_WORK_MU_BWorkAnimationID() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0027f5f0` | Resume_Get_WORK_MU_BWorkFontID() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0027f5d8` | Resume_Get_WORK_MU_FontID() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0027d468` | disableCancelDisableArea() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00279ed4` | ClearForBattleRoutine() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00271284` | Ssd_Init(unsigned short) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0026ec30` | ctlsentuto_deactive(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0026df30` | ctlhentuto_deactive(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0026c400` | ctltresure_deactive(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002675f4` | ctlret_deactive(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `002602f4` | ctlmouke_deactive(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0025ffe0` | iOS_IsTutoStart() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0025e294` | mkadrtbl_calc(int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00259ea4` | ctlhouk_deactive(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00259768` | ctlhistory_deactive(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00259750` | ctlhistory_active(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0024e904` | ctlperson_deactive(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0024dcc0` | ctlkiroku_deactive(CTLINFO*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00248598` | iOS_TestDraw(unsigned long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0021b908` | PopAirDensity() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0021b8f0` | PushAirDensity() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00216848` | getMusicPointer(int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00216128` | iOS_resetTexCacheLine() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0020f8ec` | resetFrameRate() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0020f8a0` | finishAttackTeamSelect() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0020f538` | restartAnimation() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0020f4fc` | clearOverSpecCtr() (needs_review) | 24 | 83.33 | 0 | 0 |
| `001fd2ac` | resetTurnOrder() (needs_review) | 24 | 83.33 | 0 | 0 |
| `001eee48` | getShapeWaitType(unsigned short) (needs_review) | 24 | 83.33 | 0 | 0 |
| `001ed94c` | getDirectionVector(int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00161e60` | iOSSetRotMode() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0015a72c` | iOSScrollButtonDTap() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00155dec` | teach_onocursor(int, int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00155dd4` | active_worldstatus() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00155d70` | reactive_worldstatus() (needs_review) | 24 | 83.33 | 0 | 0 |
| `001556f0` | worldcursorposset(int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `001531cc` | ResetgMission_Successflg() (needs_review) | 24 | 83.33 | 0 | 0 |
| `001506d4` | SetgMission_Successflg() (needs_review) | 24 | 83.33 | 0 | 0 |
| `001506bc` | rsetNetErrorCutFlg() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00150690` | setNetErrorCutFlg() (needs_review) | 24 | 83.33 | 0 | 0 |
| `0010fa04` | Wloadcdst(int, int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `0010729c` | Wtutorial_padcontrol(int*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `001024e4` | Wwhatweather() (needs_review) | 24 | 83.33 | 0 | 0 |
| `00101578` | WiOS_set_status_pad(unsigned long*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `000e0fa0` | loadcdst(int, int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `000ddd48` | tutorial_padcontrol(int*) (needs_review) | 24 | 83.33 | 0 | 0 |
| `000da808` | whatweather() (needs_review) | 24 | 83.33 | 0 | 0 |
| `000da5f8` | return_actionstructure() (needs_review) | 24 | 83.33 | 0 | 0 |
| `000cbd78` | pspEntrySquareDataGet() (needs_review) | 24 | 83.33 | 0 | 0 |
| `000cbb30` | resetYLine() (needs_review) | 24 | 83.33 | 0 | 0 |
| `000c8198` | tool_squarecursor(int, int) (needs_review) | 24 | 83.33 | 0 | 0 |
| `000c8138` | return_pentry() (needs_review) | 24 | 83.33 | 0 | 0 |
| `000823ec` | zError (needs_review) | 24 | 83.33 | 0 | 0 |
| `002c53d4` | Main_SetPauseFlag(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002c53c0` | Main_GetPauseFlag() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002b87e8` | iOS_isInGameArea() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002b8708` | iOS_PressTime() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002b14d0` | Project_Archive_GetFile(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002ac000` | sceGuTexMode (needs_review) | 20 | 80.0 | 0 | 0 |
| `002abd20` | sceGuClutMode (needs_review) | 20 | 80.0 | 0 | 0 |
| `002ab9cc` | sceGuFinishId (needs_review) | 20 | 80.0 | 0 | 0 |
| `002ab8ec` | sceGuColor (needs_review) | 20 | 80.0 | 0 | 0 |
| `002ab6fc` | GPUCmd_GetGPUCmd_IP() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002a3138` | xpSetResume (needs_review) | 20 | 80.0 | 0 | 0 |
| `002a3120` | xpGetHeapSize (needs_review) | 20 | 80.0 | 0 | 0 |
| `002a2fd0` | xpInitSPAD (needs_review) | 20 | 80.0 | 0 | 0 |
| `002a2da4` | PCclose (needs_review) | 20 | 80.0 | 0 | 0 |
| `002a13b4` | InitClip (needs_review) | 20 | 80.0 | 0 | 0 |
| `002a1370` | ReadGeomScreen (needs_review) | 20 | 80.0 | 0 | 0 |
| `002a133c` | SetGeomScreen (needs_review) | 20 | 80.0 | 0 | 0 |
| `0029fda8` | GteSetCtrlReg(long, long) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0029fd7c` | GteGetCtrlReg(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0029b6e8` | GsGetWorkBase (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028df7c` | _card_info (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028dea8` | InitCARD (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028dcf0` | StartRCnt (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028d1b0` | tlGetHeap() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028ba40` | TE_setTaskType(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028ba2c` | getVSyncBlockCountTaskEmu() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028b3dc` | pspWorldDataRectGet() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028a12c` | FFT_GetSavedata() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028a08c` | Savedata_GetAddr() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00289818` | pspPrimGetWorkBuf_current() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028858c` | pspOpenDataIconBufGet() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00288578` | pspOpenDataBackBufGet(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00288558` | getTurnCount_CalcMissionPayPoint() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00288544` | setTurnCount_CalcMissionPayPoint(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00288530` | getMissionNo_CalcMissionPayPoint() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028851c` | setMissionNo_CalcMissionPayPoint(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002884e8` | getBattlePoint() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002884d4` | setBattlePoint(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002884b4` | Get_NonDrawTaikiIconFlg() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002884a0` | Set_NonDrawTaikiIconFlg(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00287a2c` | get_g_Soldier_Draw_flg() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00287a18` | set_g_Soldier_Draw_flg(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00287070` | get_rival() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00287030` | get_timing_flag() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00286dec` | GetNetmissionNo() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00286b20` | get_limit_turn_flg() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00286b0c` | set_limit_turn_flg(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00286ab4` | set_netdatamode(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00286aa0` | get_netdatamode() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002868a8` | set_gEventMovieNo(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00286894` | get_gEventMovieNo() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00286880` | getEventStatus() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00286794` | setEventStatus(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002862e8` | IsMapTexAsideLoad(unsigned int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00285f38` | pspMsgLzwBaseGet(FFTPSP_MSG_LZW) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002843a0` | new_VectorDataBase(unsigned int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00282274` | iOS_v2menuGetYline() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002819b8` | iOS_v2menuGetType() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002816a8` | iOS_v2menuGetDecide() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00281694` | iOS_v2menuSetDecide(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00281664` | iOS_v2menuGetAddr() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028051c` | iOS_fftDelete() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0027fc14` | chk_ucResumeDataSetAddr(unsigned char*) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0027b528` | getCmdKind(unsigned int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0027b514` | getCmdKindNum() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0027b480` | setDrawPrimNum(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0025f424` | iOSSDNovelHelpTrgGet() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0025f410` | iOSSDNovelHelpTrgSet(long) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0025f3fc` | iOSSnapshotSet(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0025f3d8` | iOS_wld_pad_trg(unsigned long) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0025691c` | IOSsTownModeSet(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00245a60` | o_SelectCard(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002450b0` | TEST_getClearOt() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0024509c` | TEST_setClearOt(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00228dd0` | GetShapePrimPtNow() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0021cf1c` | GetEffectStatus() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0021b890` | SetAirDensity(long) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0021b4e0` | GetPlugInFuncAdr(short) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002168e8` | callEnvEffect(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00216604` | checkActiveMusic() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0020f8b8` | getFrameTicks() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0020f428` | eventEffectExecute() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00204254` | setTurning(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002041fc` | getStartBattleFlg() (needs_review) | 20 | 80.0 | 0 | 0 |
| `002041e8` | setStartBattleFlg(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002010b8` | iOSmapVectorScrollCheck() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001fcdf0` | iOSgetCursorVisible() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001eee34` | getEffSequenceAddress() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001d15b0` | get_originalability() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001bab64` | GetSttsAMovingTime() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001b8e50` | get_tutrial_pad() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001b4c20` | IsDark(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `001aec78` | iOSItemTypeGet() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001aec64` | iOSItemTypeSet(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `001adc68` | FadeMask(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `001ac8b4` | dispFT4num() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001a4858` | iOSLearnTypeSet(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0018f994` | eStopGetPad(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00161958` | iOSHelpInputWaitSet(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00161944` | iOSHelpInputWaitGet() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0015fff4` | iOSGetTchRotDY() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0015da20` | iOSGetTchCurLimit() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0015a8a0` | iOSScrollgStatusModeGet() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0015a328` | iOSsTchBtlFlagSet(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0015a314` | iOSsTchBtlFlagGet() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0015a16c` | iOSTapTimeAreaGet() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001579c0` | regist_zodiacot(unsigned int*) (needs_review) | 20 | 80.0 | 0 | 0 |
| `001579ac` | worldcursormove(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00156550` | send_worldkeymask(unsigned long) (needs_review) | 20 | 80.0 | 0 | 0 |
| `00155c78` | ret_adventurestatus() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001531e4` | GetgMission_Successflg() (needs_review) | 20 | 80.0 | 0 | 0 |
| `001506a8` | getNetErrorCutFlg() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00142f4c` | WiOS_getOptionAddOfsMode() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00142840` | WiOS_getOptionAddOfsX() (needs_review) | 20 | 80.0 | 0 | 0 |
| `0012f2dc` | iOSPersonalWinPosSet(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `0012f214` | iOSpersonalWinPosClear(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `001021c8` | Wreturn_actionstructure() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00101fd0` | iOStorideflagGet() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00101590` | WiOS_getStatusAllgrayf() (needs_review) | 20 | 80.0 | 0 | 0 |
| `00101420` | Wget_padframe() (needs_review) | 20 | 80.0 | 0 | 0 |
| `000d9608` | get_padframe() (needs_review) | 20 | 80.0 | 0 | 0 |
| `000cbb1c` | getYLine() (needs_review) | 20 | 80.0 | 0 | 0 |
| `000c81b0` | tool_setarrowmode(int) (needs_review) | 20 | 80.0 | 0 | 0 |
| `002bef64` | ResumeData_GetHeapOffset() (needs_review) | 16 | 75.0 | 0 | 0 |
| `002b375c` | Error_GetErrorCode() (needs_review) | 16 | 75.0 | 0 | 0 |
| `002b1fe8` | Offscreen_Get() (needs_review) | 16 | 75.0 | 0 | 0 |
| `002a39b8` | sceGeEdramGetAddr (needs_review) | 16 | 75.0 | 0 | 0 |
| `002a2fe4` | xpGetSPADAddress (needs_review) | 16 | 75.0 | 0 | 0 |
| `002a2be8` | PCinit (needs_review) | 16 | 75.0 | 0 | 0 |
| `0028deec` | StopCARD (needs_review) | 16 | 75.0 | 0 | 0 |
| `0028decc` | StartCARD (needs_review) | 16 | 75.0 | 0 | 0 |
| `0027b494` | getDrawPrimNum() (needs_review) | 16 | 75.0 | 0 | 0 |
| `00263aac` | iOSNovelBrightStop() (needs_review) | 16 | 75.0 | 0 | 0 |
| `0025f3ec` | iOSSnapshotGet() (needs_review) | 16 | 75.0 | 0 | 0 |
| `0025690c` | IOSsTownModeGet() (needs_review) | 16 | 75.0 | 0 | 0 |
| `0020dac8` | getBackColor() (needs_review) | 16 | 75.0 | 0 | 0 |
| `0020d83c` | getMapAngle() (needs_review) | 16 | 75.0 | 0 | 0 |
| `0020d5c8` | getMapScale() (needs_review) | 16 | 75.0 | 0 | 0 |
| `0020d2a8` | getMapScroll() (needs_review) | 16 | 75.0 | 0 | 0 |
| `0020d050` | getMapScrollXYZ() (needs_review) | 16 | 75.0 | 0 | 0 |
| `001eee24` | getEffShapeAddress() (needs_review) | 16 | 75.0 | 0 | 0 |
| `001a6368` | iOSLearnTypeGet() (needs_review) | 16 | 75.0 | 0 | 0 |
| `0018377c` | fileopen(unsigned char*, unsigned int) (needs_review) | 16 | 75.0 | 0 | 0 |
| `00101fc0` | WgetStatusPad() (needs_review) | 16 | 75.0 | 0 | 0 |
| `000d6d98` | getStatusPad() (needs_review) | 16 | 75.0 | 0 | 0 |
| `000823d4` | zlibVersion (needs_review) | 16 | 75.0 | 0 | 0 |
| `00073c64` | get_crc_table (needs_review) | 16 | 75.0 | 0 | 0 |
| `002c9121` | operator delete[](void*) (needs_review) | 8 | 0.0 | 0 | 0 |

> Structural acceptance does not establish semantic equivalence.
> Counts distinguish historical CSV statuses, new accepted checkpoints, and review cases.
