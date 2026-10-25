# Reverse engineering progress

Binary SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

| Metric | Quantity |
|---|---:|
| Inventory total | 6,455 functions / 1,837,392 bytes |
| Previously analyzed in CSV | 3,373 functions / 1,513,492 bytes |
| JSON checkpoints (all statuses) | 739 |
| Newly accepted structurally | 403 functions / 116,616 bytes |
| Needs review | 336 functions |
| Core targets in inventory | 4,642 functions |
| Core targets checkpointed | 636 functions |
| Core accepted structurally | 320 functions |
| Core needs review | 316 functions |
| Core not yet checkpointed | 1,725 functions |
| Not yet checkpointed | 2,329 functions / 110,968 bytes |

## Checkpoint status

| Status | Functions |
|---|---:|
| auto_structural | 403 |
| needs_review | 336 |

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
| `0025f44c` | frmbuf_get() (needs_review) | 496 | 91.13 | 0 | 0 |
| `001ccc3c` | getTrapResultDamage(BWORK*, int) (needs_review) | 496 | 88.71 | 1 | 0 |
| `001bc87c` | UnitTableInit(short) (needs_review) | 496 | 86.29 | 0 | 0 |
| `0015813c` | unittoface(int) (needs_review) | 496 | 69.35 | 1 | 0 |
| `0015ad38` | iOSexecuteCurSlide() (needs_review) | 492 | 93.5 | 0 | 0 |
| `002472a8` | ctlsound_main(CTLINFO*) (needs_review) | 484 | 93.39 | 0 | 0 |
| `001569ac` | editdirect() (needs_review) | 484 | 91.74 | 0 | 0 |
| `0026c680` | ctltresure_main(CTLINFO*) (needs_review) | 480 | 92.5 | 0 | 0 |
| `00253f20` | ctlmap_init() (needs_review) | 480 | 90.0 | 0 | 0 |
| `0015596c` | worldmap_startinit() (needs_review) | 480 | 93.33 | 0 | 0 |
| `002553a8` | ctlhelp2_init(int, int) (needs_review) | 476 | 91.6 | 0 | 0 |
| `0027a974` | BattleRoutineInit() (needs_review) | 472 | 93.22 | 0 | 0 |
| `0027207c` | GetNearestUnit(int) (needs_review) | 472 | 92.37 | 1 | 0 |
| `0019dc10` | SttsEmploy() (needs_review) | 472 | 89.83 | 0 | 0 |
| `0026dd40` | ctlhentuto_init() (needs_review) | 464 | 92.24 | 0 | 0 |
| `001022ec` | Wtutorial_hookfunc() (needs_review) | 464 | 88.79 | 0 | 0 |
| `002608c0` | ctlokng_init(_POINT) (needs_review) | 460 | 92.17 | 0 | 0 |
| `0026b0f4` | wld_snpl() (needs_review) | 456 | 93.86 | 0 | 0 |
| `0025990c` | ctlhistory_main(CTLINFO*) (needs_review) | 456 | 92.11 | 0 | 0 |
| `001d8b58` | get_ability_address(int, ABILITY_COMMON_DATA**, void**) (needs_review) | 452 | 92.04 | 0 | 0 |
| `001b8c38` | sort_init() (needs_review) | 452 | 87.61 | 0 | 0 |
| `0024e91c` | ctlpersmes_init(int) (needs_review) | 448 | 91.96 | 0 | 0 |
| `0019d304` | DressSellStock() (needs_review) | 444 | 90.99 | 0 | 0 |
| `0020c264` | db_init(int, int, int, unsigned char, unsigned char, unsigned char) (needs_review) | 436 | 94.5 | 0 | 0 |
| `001eb124` | loadAbilityAnimation(tag_animation*, void*) (needs_review) | 436 | 94.5 | 0 | 0 |
| `0026abac` | timeevt_chk() (needs_review) | 432 | 87.96 | 0 | 0 |
| `0019df84` | AccountEmploy() (needs_review) | 432 | 91.67 | 0 | 0 |
| `00247884` | birthday_change(CTLINFO*) (needs_review) | 428 | 94.39 | 0 | 0 |
| `00276788` | CheckUnitActionOK(unsigned char*) (needs_review) | 424 | 94.34 | 0 | 0 |
| `00270520` | valnumwin_set(int, unsigned long, int, _POINT*) (needs_review) | 424 | 93.4 | 0 | 0 |
| `00267ad0` | ctlret_main(CTLINFO*) (needs_review) | 420 | 92.38 | 0 | 0 |
| `000aecb8` | CEGL2_SPRITE::ErrorGL(char const*, char const*, unsigned int) (needs_review) | 420 | 86.67 | 1 | 0 |
| `000ab4b0` | CEGL2_FBO::ErrorGL(char const*, char const*, unsigned int) (needs_review) | 420 | 89.52 | 1 | 0 |
| `0024f4e8` | ctltipsmes_init(int) (needs_review) | 416 | 93.27 | 0 | 0 |
| `0015a988` | sBattleTouchRotationMain() (needs_review) | 416 | 94.23 | 0 | 0 |
| `0024e734` | ctlperson_init() (needs_review) | 412 | 90.29 | 0 | 0 |
| `0019dde8` | BuyEmploy() (needs_review) | 412 | 92.23 | 0 | 0 |
| `00285f8c` | hockRead(void*, int, unsigned int) (needs_review) | 408 | 83.33 | 0 | 0 |
| `0021ef4c` | InitPermanentEffect() (needs_review) | 408 | 92.16 | 0 | 0 |
| `00162080` | wasm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) (needs_review) | 404 | 80.2 | 2 | 0 |
| `0015e5d4` | iOSShiftUnitGet() (needs_review) | 404 | 92.08 | 0 | 0 |
| `00159aac` | asm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) (needs_review) | 404 | 80.2 | 2 | 0 |
| `002b1600` | GX_Init(int) (needs_review) | 400 | 91.0 | 0 | 0 |
| `002595c0` | ctlhistory_init() (needs_review) | 400 | 90.0 | 0 | 0 |
| `002875a8` | Draw_Win(int) (needs_review) | 396 | 93.94 | 0 | 0 |
| `00259780` | ctlhismes_init(int) (needs_review) | 396 | 91.92 | 0 | 0 |
| `00256174` | ctlfsetnum_main(CTLINFO*) (needs_review) | 392 | 90.82 | 0 | 0 |
| `002031a4` | iOSsetCursorByTouch(int, int, int, int, int) (needs_review) | 392 | 57.14 | 1 | 0 |
| `001cd308` | check_learning(int, unsigned short*) (needs_review) | 392 | 94.9 | 0 | 0 |
| `002c9b11` | __gxx_personality_v0 (needs_review) | 388 | 7.22 | 0 | 0 |
| `00176b80` | bChrSort(int) (needs_review) | 388 | 92.78 | 0 | 0 |
| `0028e2e4` | CdControl (needs_review) | 384 | 68.75 | 1 | 0 |
| `00287734` | Draw_Lose(int) (needs_review) | 384 | 93.75 | 0 | 0 |
| `0027fe84` | Savedata_Load(unsigned char*, int*) (needs_review) | 384 | 94.79 | 0 | 0 |
| `0024581c` | movie_init(int, int, int, int, int, char*) (needs_review) | 384 | 88.54 | 0 | 0 |
| `002453a4` | fft_ending() (needs_review) | 384 | 91.67 | 0 | 0 |
| `00242498` | ctlendroll_init() (needs_review) | 384 | 87.5 | 0 | 0 |
| `001f4440` | InitAnimationInit() (needs_review) | 384 | 88.54 | 0 | 0 |
| `0022a6a4` | _ReadTMD(TMD_PRIM*) (needs_review) | 380 | 84.21 | 1 | 0 |
| `001d972c` | get_shape2(BWORK*, unsigned char*) (needs_review) | 380 | 54.74 | 1 | 0 |
| `001d205c` | check_trap(unsigned char, unsigned char, unsigned char) (needs_review) | 380 | 93.68 | 0 | 0 |
| `001b8e64` | TutrialInit(int) (needs_review) | 380 | 92.63 | 0 | 0 |
| `0019f798` | MainShop() (needs_review) | 380 | 89.47 | 0 | 0 |
| `0020fd1c` | InitializeAll() (needs_review) | 376 | 88.3 | 0 | 0 |
| `0026baec` | wldtown_init() (needs_review) | 372 | 91.4 | 0 | 0 |
| `0024f8c0` | ctltipsmes_main(CTLINFO*) (needs_review) | 372 | 93.55 | 0 | 0 |
| `00211a28` | SetChangePaletteData(unsigned short, unsigned short, unsigned short, unsigned short, unsigned short) (needs_review) | 368 | 91.3 | 0 | 0 |
| `00210eac` | initMap(int, int) (needs_review) | 368 | 81.52 | 1 | 0 |
| `0019d634` | MonsterNameInput() (needs_review) | 368 | 88.04 | 0 | 0 |
| `000ff2cc` | Wdisposetexture(RECT16*) (needs_review) | 368 | 93.48 | 0 | 0 |
| `000ff4b0` | Wallocatememorywait(int) (needs_review) | 364 | 92.31 | 0 | 0 |
| `0024b824` | ctlbar_exit(CTLINFO*) (needs_review) | 356 | 92.13 | 0 | 0 |
| `002878b4` | Draw_Draw(int) (needs_review) | 352 | 94.32 | 0 | 0 |
| `0015af24` | iOSexecuteScroll() (needs_review) | 352 | 92.05 | 0 | 0 |
| `002b582c` | Logo_Init() (needs_review) | 348 | 85.06 | 0 | 0 |
| `0024ac38` | vOpn_defscrwin_set(int, int, _POINT*, _POINT*) (needs_review) | 348 | 90.8 | 0 | 0 |
| `001e6368` | forecast_skill(BWORK*, BWORK*, ACT*) (needs_review) | 348 | 91.95 | 0 | 0 |
| `001597c0` | disp_worlddhelpmenu() (needs_review) | 348 | 91.95 | 0 | 0 |
| `002578d4` | ctlevtinfo_main(CTLINFO*) (needs_review) | 344 | 90.7 | 0 | 0 |
| `0020fe94` | InitializeHot() (needs_review) | 344 | 88.37 | 0 | 0 |
| `000d78f0` | allocatememorywait(int) (needs_review) | 344 | 91.86 | 0 | 0 |
| `00248cd0` | ctlcard_main(CTLINFO*) (needs_review) | 340 | 89.41 | 0 | 0 |
| `0026c27c` | ctltresure_init() (needs_review) | 336 | 91.67 | 0 | 0 |
| `00255a38` | ctlflagset_init() (needs_review) | 336 | 90.48 | 0 | 0 |
| `001d21d8` | get_stop_event(BWORK*) (needs_review) | 332 | 93.98 | 0 | 0 |
| `0026b724` | worldmap_new() (needs_review) | 328 | 87.8 | 0 | 0 |
| `002b20f4` | onGotoNextMode(int) (needs_review) | 324 | 71.6 | 2 | 0 |
| `00253d84` | ctltownset_main(CTLINFO*) (needs_review) | 324 | 92.59 | 0 | 0 |
| `002169d0` | InitSound() (needs_review) | 324 | 91.36 | 0 | 0 |
| `001612d0` | iOSsTchBtlInit() (needs_review) | 324 | 80.25 | 0 | 0 |
| `00289c1c` | pspFftDelete(int*) (needs_review) | 320 | 57.5 | 1 | 0 |
| `002b2d10` | Jingle_Play(int) (needs_review) | 312 | 93.59 | 0 | 0 |
| `0025a0f0` | ctlhoukmes_init(int) (needs_review) | 312 | 89.74 | 0 | 0 |
| `0020c418` | db_swap(unsigned long*, unsigned long*) (needs_review) | 312 | 89.74 | 0 | 0 |
| `001d2c10` | get_battlebonus(B_BONUS*) (needs_review) | 312 | 93.59 | 0 | 0 |
| `00162d5c` | iOS_IsInYellowMesh(int, int) (needs_review) | 312 | 92.31 | 0 | 0 |
| `00203070` | setCursorByTouch(int, int, int) (needs_review) | 308 | 49.35 | 1 | 0 |
| `000a7ec4` | CEGL2_IF::SetBlendMode(int) (needs_review) | 308 | 88.31 | 1 | 0 |
| `00225514` | MemoryMapper() (needs_review) | 304 | 88.16 | 0 | 0 |
| `001d67a8` | get_mapid(int, int, int, int) (needs_review) | 304 | 75.0 | 1 | 0 |
| `002b3464` | Boot_Init() (needs_review) | 300 | 92.0 | 0 | 0 |
| `00257af4` | ctlparty_main(CTLINFO*) (needs_review) | 300 | 90.67 | 0 | 0 |
| `00256ec8` | ctltownmenu_exit(CTLINFO*, int) (needs_review) | 300 | 92.0 | 0 | 0 |
| `00255054` | ctlmap_eventchk() (needs_review) | 300 | 93.33 | 0 | 0 |
| `002530b8` | ctlbrst_zodiac() (needs_review) | 300 | 93.33 | 0 | 0 |
| `0024717c` | ctlsound_init() (needs_review) | 300 | 90.67 | 0 | 0 |
| `001b2ac8` | SetJobName() (needs_review) | 296 | 90.54 | 0 | 0 |
| `002702f0` | scrwin_para_set(int, int, _POINT*, _POINT*) (needs_review) | 292 | 90.41 | 0 | 0 |
| `00200bb8` | eventZoomChange(int) (needs_review) | 292 | 93.15 | 0 | 0 |
| `002899a0` | pspFftSave(int, FFT_SAVE_DATA*, int*) (needs_review) | 288 | 63.89 | 1 | 0 |
| `00221d64` | RequestHitMarkEffect(long, EffectOrder*, long) (needs_review) | 288 | 93.06 | 0 | 0 |
| `000da35c` | event_init_memory() (needs_review) | 288 | 76.39 | 0 | 0 |
| `000c18cc` | disp_maptitle() (needs_review) | 288 | 94.44 | 0 | 0 |
| `001ccafc` | get_floor_damage(BWORK*) (needs_review) | 284 | 90.14 | 0 | 0 |
| `001a6410` | MessageDataSet(int) (needs_review) | 284 | 83.1 | 1 | 0 |
| `0019f914` | ExitShop() (needs_review) | 284 | 91.55 | 0 | 0 |
| `0024971c` | vOpn_key_rep(unsigned long) (needs_review) | 280 | 94.29 | 0 | 0 |
| `00200e2c` | eventFukanChange(int) (needs_review) | 280 | 92.86 | 0 | 0 |
| `00163bb4` | iOS_initTouchDisable(int) (needs_review) | 280 | 91.43 | 0 | 0 |
| `002b7378` | RENDER_TO_SCREEN(int, int, int*, int*) (needs_review) | 276 | 91.3 | 0 | 0 |
| `0029a2d8` | DrawOTag (needs_review) | 276 | 89.86 | 0 | 0 |
| `00291178` | MoveImage2 (needs_review) | 276 | 94.2 | 0 | 0 |
| `0026b904` | wldsymbol_init() (needs_review) | 276 | 91.3 | 0 | 0 |
| `001aec8c` | DrawEquipCategory(int, int, int) (needs_review) | 276 | 94.2 | 0 | 0 |
| `00101fe4` | Wevent_init_memory() (needs_review) | 276 | 76.81 | 0 | 0 |
| `000cbc3c` | TrapWindowTaskManager(int, int, short, int) (needs_review) | 276 | 94.2 | 0 | 0 |
| `002b7268` | SCREEN_TO_RENDER(int, int, int*, int*) (needs_review) | 272 | 91.18 | 0 | 0 |
| `0022588c` | NewObject(short, short) (needs_review) | 272 | 92.65 | 0 | 0 |
| `001e21f8` | getskillresult_first(int) (needs_review) | 272 | 91.18 | 0 | 0 |
| `001dc944` | set_casting_status(BWORK*, unsigned char) (needs_review) | 272 | 85.29 | 1 | 0 |
| `0015d748` | iOSCurSameOK() (needs_review) | 272 | 89.71 | 0 | 0 |
| `00155b4c` | worldmap_menuinit() (needs_review) | 272 | 89.71 | 0 | 0 |
| `002ca215` | __cxa_call_unexpected (needs_review) | 268 | 0.0 | 0 | 0 |
| `0028b738` | initTaskEmu() (needs_review) | 268 | 92.54 | 0 | 0 |
| `002557ac` | ctlhelp_main(CTLINFO*) (needs_review) | 268 | 85.07 | 0 | 0 |
| `00249ac0` | vOpn_padread() (needs_review) | 268 | 91.04 | 0 | 0 |
| `00200cdc` | startZoomChange(int) (needs_review) | 268 | 94.03 | 0 | 0 |
| `0025b8ec` | houkoku_mesput(CTLINFO*, int) (needs_review) | 264 | 92.42 | 0 | 0 |
| `0026a2cc` | snpl_scrdisp() (needs_review) | 260 | 93.85 | 0 | 0 |
| `00259ad4` | ctlhismes_main(CTLINFO*) (needs_review) | 260 | 90.77 | 0 | 0 |
| `00255654` | ctlhelp_init(int, int) (needs_review) | 260 | 87.69 | 0 | 0 |
| `00249174` | vOpn_parainit() (needs_review) | 260 | 78.46 | 0 | 0 |
| `001bad9c` | SeExec() (needs_review) | 260 | 92.31 | 0 | 0 |
| `0019d530` | FighterName() (needs_review) | 260 | 86.15 | 0 | 0 |
| `001537dc` | eventflaginit() (needs_review) | 260 | 81.54 | 0 | 0 |
| `00255180` | ctlmap_active(CTLINFO*) (needs_review) | 256 | 90.62 | 0 | 0 |
| `00225210` | DoPermanentEffect() (needs_review) | 256 | 89.06 | 0 | 0 |
| `00210c9c` | setMapVector(SVECTOR*, SVECTOR*) (needs_review) | 256 | 89.06 | 0 | 0 |
| `001cc9fc` | status_countdown(int) (needs_review) | 256 | 92.19 | 0 | 0 |
| `002b1ff8` | Debug_DrawFPS() (needs_review) | 252 | 90.48 | 0 | 0 |
| `00225790` | InitObjectManager() (needs_review) | 252 | 87.3 | 0 | 0 |
| `001bc334` | GetSttsApos(short) (needs_review) | 252 | 88.89 | 0 | 0 |
| `000e0fb8` | initdrmode(DR_MODE*, int) (needs_review) | 252 | 92.06 | 0 | 0 |
| `00253a68` | ctlcenter_main(CTLINFO*) (needs_review) | 248 | 87.1 | 0 | 0 |
| `001caa10` | set_ct_weapon(ACT*) (needs_review) | 248 | 67.74 | 1 | 0 |
| `00188348` | allitem_count() (needs_review) | 248 | 91.94 | 0 | 0 |
| `0010fa1c` | Winitdrmode(DR_MODE*, int) (needs_review) | 248 | 91.94 | 0 | 0 |
| `001b799c` | SystemWarningTime(int, int) (needs_review) | 244 | 90.16 | 0 | 0 |
| `0025c838` | ctlshogou_init() (needs_review) | 240 | 90.0 | 0 | 0 |
| `0025c3ac` | mkdaypt_calc() (needs_review) | 240 | 93.33 | 0 | 0 |
| `00211b98` | ExecuteChangePalette() (needs_review) | 240 | 90.0 | 0 | 0 |
| `00100844` | Wcheckkeyok() (needs_review) | 240 | 90.0 | 0 | 0 |
| `0025b78c` | houkoku_talkunit(int) (needs_review) | 236 | 86.44 | 1 | 0 |
| `002590e8` | wld_event(int, int) (needs_review) | 236 | 94.92 | 0 | 0 |
| `001f35dc` | EndAnimation(tag_animation*) (needs_review) | 236 | 94.92 | 0 | 0 |
| `0015ce74` | iOSMapIconModeSet(int) (needs_review) | 236 | 89.83 | 0 | 0 |
| `00101650` | Whook_jobmenu() (needs_review) | 236 | 89.83 | 0 | 0 |
| `000ef4f4` | hook_jobmenu() (needs_review) | 236 | 89.83 | 0 | 0 |
| `00285e50` | pspMsgGet(unsigned int) (needs_review) | 232 | 63.79 | 1 | 0 |
| `0028d6ec` | tlCheckHeap() (needs_review) | 228 | 92.98 | 0 | 0 |
| `001eb67c` | myInitShape() (needs_review) | 228 | 78.95 | 0 | 0 |
| `00264378` | ctlnblwldinfo_init() (needs_review) | 224 | 78.57 | 0 | 0 |
| `002541c4` | ctlcenter_init(int) (needs_review) | 224 | 85.71 | 0 | 0 |
| `001cea0c` | set_walker_result(BWORK*, REWARD*) (needs_review) | 224 | 94.64 | 0 | 0 |
| `0015a33c` | iOSsTchBtlEnd() (needs_review) | 224 | 76.79 | 0 | 0 |
| `0015588c` | title_menuinit() (needs_review) | 224 | 91.07 | 0 | 0 |
| `0014bd8c` | Cdisp_eventwaitwindow() (needs_review) | 224 | 92.86 | 0 | 0 |
| `00138234` | disp_eventwindow() (needs_review) | 224 | 92.86 | 0 | 0 |
| `00134fa0` | Wdisp_eventwaitwindow() (needs_review) | 224 | 92.86 | 0 | 0 |
| `0012cb3c` | disp_eventwaitwindow() (needs_review) | 224 | 92.86 | 0 | 0 |
| `001252d0` | Wdisp_eventwindow() (needs_review) | 224 | 92.86 | 0 | 0 |
| `00123994` | Edisp_eventwaitwindow() (needs_review) | 224 | 92.86 | 0 | 0 |
| `000d115c` | Ddisp_eventwaitwindow() (needs_review) | 224 | 92.86 | 0 | 0 |
| `002b54b4` | Link_Uninit() (needs_review) | 220 | 92.73 | 0 | 0 |
| `002b2ea0` | Jingle_FrameMove() (needs_review) | 220 | 92.73 | 0 | 0 |
| `002ab620` | GuEmu_ClearTexCache() (needs_review) | 220 | 94.55 | 0 | 0 |
| `0021d544` | getNextSENo(int) (needs_review) | 220 | 80.0 | 1 | 0 |
| `00187514` | TimeConvert(int) (needs_review) | 220 | 89.09 | 0 | 0 |
| `002867a8` | getMovieEventNum(int) (needs_review) | 216 | 68.52 | 1 | 0 |
| `000fef24` | Wdisposewindow(MESSAGEPACKET*) (needs_review) | 216 | 94.44 | 0 | 0 |
| `0025f280` | snpl_load(int) (needs_review) | 212 | 86.79 | 0 | 0 |
| `002531e4` | ctltuto_zodiac() (needs_review) | 212 | 90.57 | 0 | 0 |
| `0024b6bc` | ctlbar_active(CTLINFO*) (needs_review) | 212 | 94.34 | 0 | 0 |
| `00249f94` | vOpn_pacinit() (needs_review) | 212 | 86.79 | 0 | 0 |
| `001c02d4` | JobToAbiChg() (needs_review) | 212 | 92.45 | 0 | 0 |
| `002b2644` | EnvSE_Stop(int) (needs_review) | 208 | 94.23 | 0 | 0 |
| `00290cf0` | ResetGraph (needs_review) | 208 | 90.38 | 0 | 0 |
| `00255584` | ctlhelp2_main(CTLINFO*) (needs_review) | 208 | 86.54 | 0 | 0 |
| `001bab78` | GetIwaPadData() (needs_review) | 208 | 88.46 | 0 | 0 |
| `001a9158` | IsItem(int) (needs_review) | 208 | 94.23 | 0 | 0 |
| `0015a65c` | siOS_TCurSucCheck(unsigned int) (needs_review) | 208 | 78.85 | 1 | 0 |
| `00255e14` | ctlfsetnum_init(int, int) (needs_review) | 204 | 86.27 | 0 | 0 |
| `00228c74` | InitShape() (needs_review) | 204 | 82.35 | 0 | 0 |
| `002b1e70` | NowLoading_FrameMove() (needs_review) | 200 | 90.0 | 0 | 0 |
| `00257a2c` | ctlparty_init() (needs_review) | 200 | 86.0 | 0 | 0 |
| `0015a7d8` | iOSScrollButtonMove() (needs_review) | 200 | 90.0 | 0 | 0 |
| `00100df8` | Wget_cursoroffset(int) (needs_review) | 200 | 92.0 | 0 | 0 |
| `000d8fe0` | get_cursoroffset(int) (needs_review) | 200 | 92.0 | 0 | 0 |
| `0025e508` | person_year_up() (needs_review) | 196 | 93.88 | 0 | 0 |
| `00242268` | vOpn_arzpic_init(int) (needs_review) | 196 | 89.8 | 0 | 0 |
| `00211e50` | setPresentClutDataAsDefault(unsigned int, unsigned int, int) (needs_review) | 196 | 93.88 | 0 | 0 |
| `0021025c` | InitializePartyItem() (needs_review) | 196 | 93.88 | 0 | 0 |
| `00200f44` | startFukanChange() (needs_review) | 196 | 91.84 | 0 | 0 |
| `001383a4` | maptest() (needs_review) | 196 | 85.71 | 0 | 0 |
| `000da720` | tutorial_hookfunc() (needs_review) | 196 | 85.71 | 0 | 0 |
| `00269870` | snpl_syscur() (needs_review) | 192 | 89.58 | 0 | 0 |
| `00291098` | StoreImage2 (needs_review) | 188 | 93.62 | 0 | 0 |
| `00261b0c` | mouke_eventday_chg() (needs_review) | 188 | 93.62 | 0 | 0 |
| `0020f43c` | debugEffectWait() (needs_review) | 188 | 80.85 | 0 | 0 |
| `0020c19c` | fftVSyncCallback() (needs_review) | 188 | 87.23 | 0 | 0 |
| `000dfa94` | makemessagestructure() (needs_review) | 188 | 91.49 | 0 | 0 |
| `00254f9c` | ctltownset_init(int, int) (needs_review) | 184 | 86.96 | 0 | 0 |
| `00248c18` | ctlpremov_main(CTLINFO*) (needs_review) | 180 | 88.89 | 0 | 0 |
| `0021cf30` | InitEffect() (needs_review) | 180 | 86.67 | 0 | 0 |
| `00216308` | readMusic(int) (needs_review) | 180 | 93.33 | 0 | 0 |
| `002101a8` | loadPlayerPartyData(int) (needs_review) | 180 | 93.33 | 0 | 0 |
| `001cc89c` | check_hide_reset(BWORK*) (needs_review) | 180 | 93.33 | 0 | 0 |
| `001568fc` | worldmap_restart() (needs_review) | 176 | 81.82 | 0 | 0 |
| `002b1f3c` | Offscreen_ReadPixels(int, int, int, int) (needs_review) | 172 | 93.02 | 0 | 0 |
| `002aca7c` | GuEmu_FrameMove() (needs_review) | 172 | 93.02 | 0 | 0 |
| `002699bc` | snpl_putpara() (needs_review) | 172 | 83.72 | 0 | 0 |
| `0024998c` | vOpn_iwaprog() (needs_review) | 172 | 83.72 | 0 | 0 |
| `001cce2c` | get_trap_result(BWORK*) (needs_review) | 172 | 88.37 | 0 | 0 |
| `001cc950` | status_handle_main(BWORK*) (needs_review) | 172 | 93.02 | 0 | 0 |
| `001bd320` | UnitTableInitFirst(short) (needs_review) | 172 | 83.72 | 0 | 0 |
| `000da4ac` | event_init_light() (needs_review) | 172 | 88.37 | 0 | 0 |
| `002b3610` | Boot_FrameRender() (needs_review) | 168 | 88.1 | 0 | 0 |
| `00248b70` | ctlpremov_init(int, int, int, int, int, char*) (needs_review) | 168 | 88.1 | 0 | 0 |
| `00217e14` | InitEffectAnimation() (needs_review) | 168 | 92.86 | 0 | 0 |
| `002116f0` | padReadGenerate() (needs_review) | 168 | 88.1 | 0 | 0 |
| `0029a3ec` | DrawPrim (needs_review) | 164 | 90.24 | 0 | 0 |
| `00289ac0` | pspFftLoad(int, FFT_SAVE_DATA*, int*, int) (needs_review) | 164 | 92.68 | 0 | 0 |
| `001f4a88` | initEntryPlayerAnimations() (needs_review) | 164 | 87.8 | 0 | 0 |
| `001bb460` | SetSttsAbi(int) (needs_review) | 164 | 92.68 | 0 | 0 |
| `00261bc8` | endevent_count(int) (needs_review) | 160 | 92.5 | 0 | 0 |
| `00217ebc` | NewEffectAnimation(short) (needs_review) | 160 | 92.5 | 0 | 0 |
| `00211c88` | DisplayChangePalette() (needs_review) | 160 | 87.5 | 0 | 0 |
| `0020f728` | checkScrolling() (needs_review) | 160 | 87.5 | 0 | 0 |
| `00221028` | RequestBowEffect(long, EffectOrder*) (needs_review) | 156 | 94.87 | 0 | 0 |
| `001cd9b0` | inc_party_item(BWORK*, unsigned short, BWORK*) (needs_review) | 156 | 94.87 | 0 | 0 |
| `001bb224` | SetSttsEqu2(int) (needs_review) | 156 | 87.18 | 0 | 0 |
| `000da280` | recieve_statusinfo() (needs_review) | 156 | 92.31 | 0 | 0 |
| `002cb0c0` | __gedf2 (needs_review) | 152 | 92.11 | 0 | 0 |
| `00263254` | ctlmouketeam_deactive(CTLINFO*) (needs_review) | 152 | 94.74 | 0 | 0 |
| `0021f328` | GetPermanentObject() (needs_review) | 152 | 89.47 | 0 | 0 |
| `001bd3cc` | UnitListInit() (needs_review) | 152 | 89.47 | 0 | 0 |
| `0013819c` | recover_windows(int, int) (needs_review) | 152 | 92.11 | 0 | 0 |
| `00125238` | Wrecover_windows(int, int) (needs_review) | 152 | 92.11 | 0 | 0 |
| `002bb678` | iOSMenuOkCancelHelpGet(int, int) (needs_review) | 148 | 94.59 | 0 | 0 |
| `002b715c` | setPspDispNum(short, short, short) (needs_review) | 148 | 89.19 | 0 | 0 |
| `002b6b38` | Main_Uninit() (needs_review) | 148 | 94.59 | 0 | 0 |
| `00268ec4` | wldcenter_move() (needs_review) | 148 | 94.59 | 0 | 0 |
| `0015d6b4` | iOSTchCurUnitCheck() (needs_review) | 148 | 86.49 | 0 | 0 |
| `0015a744` | iOSScrollButtonAreaCheck() (needs_review) | 148 | 94.59 | 0 | 0 |
| `00102208` | Wexport_suc(int) (needs_review) | 148 | 91.89 | 0 | 0 |
| `000fe1a4` | Waddlocalprim(tagPOLY_FT4*) (needs_review) | 148 | 94.59 | 0 | 0 |
| `000e14f4` | statusfigprint10(int, int, char*, COPYFIELD*) (needs_review) | 148 | 91.89 | 0 | 0 |
| `000da63c` | export_suc(int) (needs_review) | 148 | 91.89 | 0 | 0 |
| `000d7d6c` | sttsback_blue(STTSWINDOWBACK*) (needs_review) | 148 | 94.59 | 0 | 0 |
| `000d665c` | addlocalprim(tagPOLY_FT4*) (needs_review) | 148 | 94.59 | 0 | 0 |
| `002abc8c` | sceGuTexFilter (needs_review) | 144 | 94.44 | 0 | 0 |
| `00292678` | __xpLibgpuDrawCallBack(int) (needs_review) | 144 | 83.33 | 0 | 0 |
| `0026dc2c` | ctltuto_active(CTLINFO*) (needs_review) | 144 | 94.44 | 0 | 0 |
| `00221e84` | RequestLandingEffect(EffectOrder*, VECTOR*) (needs_review) | 144 | 94.44 | 0 | 0 |
| `0020e228` | get2DPosition(SVECTOR*, SVECTOR*) (needs_review) | 144 | 86.11 | 0 | 0 |
| `00207d6c` | iOS_mapVectorLimit() (needs_review) | 144 | 91.67 | 0 | 0 |
| `001d6718` | get_mapstp(int, int, int) (needs_review) | 144 | 91.67 | 0 | 0 |
| `00153584` | Wtask_create(long, char*) (needs_review) | 144 | 94.44 | 0 | 0 |
| `001532c0` | task_create(long, char*) (needs_review) | 144 | 94.44 | 0 | 0 |
| `00138314` | extend_valuefield(int) (needs_review) | 144 | 91.67 | 0 | 0 |
| `001253b0` | Wextend_valuefield(int) (needs_review) | 144 | 91.67 | 0 | 0 |
| `000ff95c` | Wsttsback_blue(STTSWINDOWBACK*) (needs_review) | 144 | 94.44 | 0 | 0 |
| `000d7b24` | sttsback_normal(STTSWINDOWBACK*) (needs_review) | 144 | 94.44 | 0 | 0 |
| `00097b70` | _float32_pack (needs_review) | 144 | 88.89 | 0 | 0 |
| `002cb4ac` | __aeabi_ul2f (needs_review) | 140 | 82.86 | 0 | 0 |
| `002562fc` | sthelp_curpos_set(CTLINFO*) (needs_review) | 140 | 94.29 | 0 | 0 |
| `00245e38` | ctlstartmov_init(int, int, int, int) (needs_review) | 140 | 85.71 | 0 | 0 |
| `0021627c` | readMusicBuffer(int, int) (needs_review) | 140 | 94.29 | 0 | 0 |
| `001bb504` | SetSttsBoth(int) (needs_review) | 140 | 91.43 | 0 | 0 |
| `000ff718` | Wsttsback_normal(STTSWINDOWBACK*) (needs_review) | 140 | 94.29 | 0 | 0 |
| `002b8680` | RayPick_GT3(tagPOLY_GT3*, int, int) (needs_review) | 136 | 94.12 | 0 | 0 |
| `002b85f8` | RayPick_GT4(tagPOLY_GT4*, int, int) (needs_review) | 136 | 94.12 | 0 | 0 |
| `00228d40` | InitPermanentShape() (needs_review) | 136 | 82.35 | 0 | 0 |
| `000e5708` | disp_status2right() (needs_review) | 136 | 85.29 | 0 | 0 |
| `000e5680` | disp_status2() (needs_review) | 136 | 85.29 | 0 | 0 |
| `002b2714` | EnvSE_SetVol(int, int) (needs_review) | 132 | 90.91 | 0 | 0 |
| `0026dcbc` | ctltuto_deactive(CTLINFO*) (needs_review) | 132 | 93.94 | 0 | 0 |
| `001abb18` | MakeChr(short) (needs_review) | 132 | 93.94 | 0 | 0 |
| `0015dfbc` | iOSActiveUnitGet() (needs_review) | 132 | 93.94 | 0 | 0 |
| `0011c02c` | Wdisp_status2right() (needs_review) | 132 | 84.85 | 0 | 0 |
| `0011bfa8` | Wdisp_status2() (needs_review) | 132 | 84.85 | 0 | 0 |
| `0007da30` | fill_fopen64_filefunc (needs_review) | 132 | 78.79 | 0 | 0 |
| `0007d9ac` | fill_fopen_filefunc (needs_review) | 132 | 78.79 | 0 | 0 |
| `002b3590` | Boot_FrameMove() (needs_review) | 128 | 90.62 | 0 | 0 |
| `00266654` | add_winpac(unsigned long*, int*) (needs_review) | 128 | 93.75 | 0 | 0 |
| `0025f358` | psp_bk_load(int, void*) (needs_review) | 128 | 90.62 | 0 | 0 |
| `0025f168` | bk_load(int) (needs_review) | 128 | 87.5 | 0 | 0 |
| `0025f0b8` | pic_load(int) (needs_review) | 128 | 87.5 | 0 | 0 |
| `0024fd74` | pspCtltutonet_deactive(CTLINFO*) (needs_review) | 128 | 93.75 | 0 | 0 |
| `00249f14` | vOpn_dataload2() (needs_review) | 128 | 93.75 | 0 | 0 |
| `00245610` | strSetDefDecEnv(DECENV*, int, int, int, int) (needs_review) | 128 | 90.62 | 0 | 0 |
| `001bc520` | scroll_chk() (needs_review) | 128 | 87.5 | 0 | 0 |
| `0015df3c` | iOSTapCalcu() (needs_review) | 128 | 87.5 | 0 | 0 |
| `00101888` | Wwait_loaddata(int) (needs_review) | 128 | 90.62 | 0 | 0 |
| `001015a4` | Wwait_overlay(int) (needs_review) | 128 | 90.62 | 0 | 0 |
| `000d9988` | wait_loaddata(int) (needs_review) | 128 | 90.62 | 0 | 0 |
| `000d9790` | wait_overlay(int) (needs_review) | 128 | 90.62 | 0 | 0 |
| `0024a544` | vOpn_add_winpac(unsigned long*, int*) (needs_review) | 124 | 93.55 | 0 | 0 |
| `0020c550` | db_swap_generate(unsigned long*, unsigned long*) (needs_review) | 124 | 90.32 | 0 | 0 |
| `001baae8` | SttsAMovingChk() (needs_review) | 124 | 90.32 | 0 | 0 |
| `0016a14c` | ASURA_soundStop() (needs_review) | 124 | 90.32 | 0 | 0 |
| `00161ef8` | wasmTaskEntry() (needs_review) | 124 | 93.55 | 0 | 0 |
| `00105510` | Wwait_direc(int) (needs_review) | 124 | 93.55 | 0 | 0 |

> Structural acceptance does not establish semantic equivalence.
> Counts distinguish historical CSV statuses, new accepted checkpoints, and review cases.
