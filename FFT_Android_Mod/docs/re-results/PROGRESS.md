# Reverse engineering progress

Binary SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

| Metric | Quantity |
|---|---:|
| Inventory total | 6,455 functions / 1,837,392 bytes |
| Previously analyzed in CSV | 3,451 functions / 1,551,512 bytes |
| JSON checkpoints (all statuses) | 3,002 |
| Newly accepted structurally | 2,887 functions / 282,496 bytes |
| Needs review | 115 functions |
| Core targets in inventory | 4,642 functions |
| Core targets checkpointed | 2,345 functions |
| Core accepted structurally | 2,272 functions |
| Core needs review | 73 functions |
| Core not yet checkpointed | 0 functions |
| Not yet checkpointed | 0 functions / 0 bytes |

## Checkpoint status

| Status | Functions |
|---|---:|
| auto_structural | 2,887 |
| needs_review | 115 |

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
| `002553a8` | ctlhelp2_init(int, int) (needs_review) | 476 | 91.6 | 0 | 0 |
| `0027207c` | GetNearestUnit(int) (needs_review) | 472 | 92.37 | 1 | 0 |
| `0019dc10` | SttsEmploy() (needs_review) | 472 | 89.83 | 0 | 0 |
| `0026dd40` | ctlhentuto_init() (needs_review) | 464 | 92.24 | 0 | 0 |
| `002608c0` | ctlokng_init(_POINT) (needs_review) | 460 | 92.17 | 0 | 0 |
| `0025990c` | ctlhistory_main(CTLINFO*) (needs_review) | 456 | 92.11 | 0 | 0 |
| `001d8b58` | get_ability_address(int, ABILITY_COMMON_DATA**, void**) (needs_review) | 452 | 92.04 | 0 | 0 |
| `0024e91c` | ctlpersmes_init(int) (needs_review) | 448 | 91.96 | 0 | 0 |
| `0019d304` | DressSellStock() (needs_review) | 444 | 90.99 | 0 | 0 |
| `0020c264` | db_init(int, int, int, unsigned char, unsigned char, unsigned char) (needs_review) | 436 | 94.5 | 0 | 0 |
| `001eb124` | loadAbilityAnimation(tag_animation*, void*) (needs_review) | 436 | 94.5 | 0 | 0 |
| `0026abac` | timeevt_chk() (needs_review) | 432 | 87.96 | 0 | 0 |
| `0019df84` | AccountEmploy() (needs_review) | 432 | 91.67 | 0 | 0 |
| `00247884` | birthday_change(CTLINFO*) (needs_review) | 428 | 94.39 | 0 | 0 |
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
| `00242498` | ctlendroll_init() (needs_review) | 384 | 87.5 | 0 | 0 |
| `0022a6a4` | _ReadTMD(TMD_PRIM*) (needs_review) | 380 | 84.21 | 1 | 0 |
| `001d972c` | get_shape2(BWORK*, unsigned char*) (needs_review) | 380 | 54.74 | 1 | 0 |
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
| `001dc944` | set_casting_status(BWORK*, unsigned char) (needs_review) | 272 | 85.29 | 1 | 0 |
| `002ca215` | __cxa_call_unexpected (needs_review) | 268 | 0.0 | 0 | 0 |
| `001caa10` | set_ct_weapon(ACT*) (needs_review) | 248 | 67.74 | 1 | 0 |
| `0025b78c` | houkoku_talkunit(int) (needs_review) | 236 | 86.44 | 1 | 0 |
| `00285e50` | pspMsgGet(unsigned int) (needs_review) | 232 | 63.79 | 1 | 0 |
| `0021d544` | getNextSENo(int) (needs_review) | 220 | 80.0 | 1 | 0 |
| `002867a8` | getMovieEventNum(int) (needs_review) | 216 | 68.52 | 1 | 0 |
| `0015a65c` | siOS_TCurSucCheck(unsigned int) (needs_review) | 208 | 78.85 | 1 | 0 |
| `002cb0c0` | __gedf2 (needs_review) | 152 | 92.11 | 0 | 0 |
| `002cb4ac` | __aeabi_ul2f (needs_review) | 140 | 82.86 | 0 | 0 |
| `000ff9ec` | Wload_replaceitems(int, int) (needs_review) | 120 | 56.67 | 1 | 0 |
| `000d7e00` | load_replaceitems(int, int) (needs_review) | 120 | 56.67 | 1 | 0 |
| `002cb830` | __gesf2 (needs_review) | 116 | 89.66 | 0 | 0 |
| `002cabdc` | __aeabi_ul2d (needs_review) | 116 | 75.86 | 0 | 0 |
| `002cd03c` | _Unwind_VRS_Set (needs_review) | 92 | 73.91 | 1 | 0 |
| `002ccfb8` | _Unwind_VRS_Get (needs_review) | 92 | 73.91 | 1 | 0 |
| `0019e134` | SuccessEmploy() (needs_review) | 84 | 90.48 | 0 | 0 |
| `002c99b5` | operator new(unsigned int) (needs_review) | 76 | 5.26 | 0 | 0 |
| `002ca195` | __cxa_begin_cleanup (needs_review) | 60 | 66.67 | 0 | 0 |
| `0028c288` | CFFT_STATE::GetBackdropColor(float*, float*, float*) (needs_review) | 56 | 57.14 | 1 | 0 |
| `002cb484` | __floatunsisf (needs_review) | 40 | 80.0 | 0 | 0 |
| `0029a834` | ClearImage (needs_review) | 36 | 77.78 | 0 | 0 |
| `0028c644` | CFFT_STATE::FaceIDToFID(int) (needs_review) | 36 | 88.89 | 0 | 0 |
| `00269b08` | snpl_effmode() (needs_review) | 36 | 88.89 | 0 | 0 |
| `00269774` | snpl_jp() (needs_review) | 36 | 88.89 | 0 | 0 |
| `002ccf98` | _Unwind_DeleteException (needs_review) | 32 | 62.5 | 0 | 0 |
| `0029ae70` | xpLib_GetTPage(int*) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0027f620` | iOS_ResumeGetData(unsigned char**, unsigned int*) (needs_review) | 32 | 75.0 | 0 | 0 |
| `00153714` | Wtask_status(long) (needs_review) | 32 | 87.5 | 0 | 0 |
| `00153450` | task_status(long) (needs_review) | 32 | 87.5 | 0 | 0 |
| `0029fea0` | rcos (needs_review) | 28 | 85.71 | 0 | 0 |
| `0028b034` | pspWorldDisableFlg(PSP_WORLD_FLG) (needs_review) | 28 | 85.71 | 0 | 0 |
| `0028b018` | pspWorldEnableFlg(PSP_WORLD_FLG) (needs_review) | 28 | 85.71 | 0 | 0 |
| `00269758` | snpl_startpage() (needs_review) | 28 | 85.71 | 0 | 0 |
| `0026973c` | snpl_endpage() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258b54` | evt_eqp() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258b38` | evt_item() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258ae4` | evt_skip2() (needs_review) | 28 | 85.71 | 0 | 0 |
| `00258ac8` | evt_skip1() (needs_review) | 28 | 85.71 | 0 | 0 |
| `0024b080` | wldbinEntry() (needs_review) | 28 | 85.71 | 0 | 0 |
| `000726e0` | JNI_OnLoad (needs_review) | 28 | 85.71 | 0 | 0 |
| `002a1324` | SetGeomOffset (needs_review) | 24 | 83.33 | 0 | 0 |
| `0029fe88` | rsin (needs_review) | 24 | 83.33 | 0 | 0 |
| `0028b050` | pspWorldCheckFlg(PSP_WORLD_FLG) (needs_review) | 24 | 83.33 | 0 | 0 |
| `00279ed4` | ClearForBattleRoutine() (needs_review) | 24 | 83.33 | 0 | 0 |
| `002a3120` | xpGetHeapSize (needs_review) | 20 | 80.0 | 0 | 0 |
| `0028a08c` | Savedata_GetAddr() (needs_review) | 20 | 80.0 | 0 | 0 |
| `000823d4` | zlibVersion (needs_review) | 16 | 75.0 | 0 | 0 |
| `002c9121` | operator delete[](void*) (needs_review) | 8 | 0.0 | 0 | 0 |

> Structural acceptance does not establish semantic equivalence.
> Counts distinguish historical CSV statuses, new accepted checkpoints, and review cases.
