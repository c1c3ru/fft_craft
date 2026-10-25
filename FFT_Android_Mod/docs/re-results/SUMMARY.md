# Parallel reverse-engineering loop

Binary SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Analyzed in current binary: 3002
Automatically triaged: 203,736 bytes / 1,837,392 inventory bytes (11.09%); **this is newly triaged coverage, not total project coverage**.

| Address | Function | Size (B) | Coverage | Status |
|---|---|---:|---:|---|
| `002cdb20` | __gnu_unwind_execute | 892 | 100.0% | auto_structural |
| `000736ac` | adler32 | 856 | 99.53% | auto_structural |
| `002cd594` | _Unwind_VRS_Pop | 856 | 97.2% | needs_review |
| `000bc67c` | CSOUND_IF_SL::LoadOGG(int, char*, unsigned char*, unsigned int, unsigned int, int) | 776 | 100.0% | auto_structural |
| `0009c9a0` | drft_init | 764 | 98.95% | auto_structural |
| `00090e08` | mdct_init | 732 | 97.81% | auto_structural |
| `00076ef8` | deflateInit2_ | 724 | 97.79% | auto_structural |
| `002ca8a0` | __subdf3 | 688 | 28.49% | needs_review |
| `002ca8a4` | __adddf3 | 684 | 28.07% | needs_review |
| `00088978` | _ve_envelope_search | 636 | 100.0% | auto_structural |
| `002cac50` | __muldf3 | 620 | 72.9% | needs_review |
| `000ba9c8` | CSOUND_IF::Load(int, char*, unsigned char*, unsigned int, unsigned int, int, int, int, int, int, int) | 612 | 100.0% | auto_structural |
| `000bced4` | CSOUND_LOADER_PCM::Open(char*, unsigned char*, unsigned int, unsigned int) | 608 | 96.71% | auto_structural |
| `0009541c` | _vp_offset_and_mix | 588 | 95.24% | auto_structural |
| `000962d0` | res0_unpack | 568 | 100.0% | auto_structural |
| `0009734c` | res2_inverse | 568 | 100.0% | auto_structural |
| `00096508` | res0_look | 564 | 100.0% | auto_structural |
| `0009c55c` | drft_forward | 560 | 100.0% | auto_structural |
| `000753c0` | deflateSetDictionary | 544 | 100.0% | auto_structural |
| `0028179c` | iOS_v2menuSetType(V2MENU_TYPE) | 540 | 94.81% | needs_review |
| `0029a618` | ClearImage2 | 540 | 96.3% | auto_structural |
| `0009c78c` | drft_backward | 532 | 100.0% | auto_structural |
| `00279cc0` | GetDirectionOfAutoUnit() | 532 | 96.99% | auto_structural |
| `000aab58` | CEGL2_FBO::Save(_RECT_S32*, char*, int, _G2D_SAVE*) | 528 | 100.0% | auto_structural |
| `00244200` | vEnd_rollproc() | 528 | 91.67% | needs_review |
| `000df864` | event_status_set(unsigned short, unsigned short) | 524 | 93.13% | needs_review |
| `00088718` | _ve_envelope_init | 520 | 97.69% | auto_structural |
| `000dfebc` | event_init() | 520 | 96.15% | auto_structural |
| `00159e5c` | iosAsmBoxCopy(char*, char*, tCOPYFIELD*, tCOPYFIELD*) | 520 | 100.0% | auto_structural |
| `002494c8` | vOpn_fadeproc(unsigned long*) | 520 | 96.92% | auto_structural |
| `0028d854` | tlGarbageCollection() | 516 | 97.67% | auto_structural |
| `002caebc` | __divdf3 | 516 | 95.35% | auto_structural |
| `0021a9ec` | SetCameraWorkWithSchedule(short) | 512 | 96.09% | auto_structural |
| `00273910` | SetSafePanel(int, int) | 512 | 99.22% | auto_structural |
| `001a8914` | GetTotalAbilityList(short, int, short*) | 508 | 99.21% | auto_structural |
| `0025a228` | houkoku_okng(CTLINFO*) | 508 | 93.7% | needs_review |
| `00271ba4` | SetBaseTargetGroup(int, int) | 508 | 89.76% | needs_review |
| `002b2448` | EnvSE_Play(int) | 508 | 77.17% | needs_review |
| `0028bb88` | TE_asmTaskEntry(int) | 504 | 91.27% | needs_review |
| `0024eadc` | ctlperson_main(CTLINFO*) | 500 | 92.0% | needs_review |
| `002576e0` | ctlevtinfo_init(int) | 500 | 92.0% | needs_review |
| `000969bc` | res2_class | 496 | 100.0% | auto_structural |
| `0015813c` | unittoface(int) | 496 | 69.35% | needs_review |
| `001bc87c` | UnitTableInit(short) | 496 | 86.29% | needs_review |
| `001ccc3c` | getTrapResultDamage(BWORK*, int) | 496 | 88.71% | needs_review |
| `0025f44c` | frmbuf_get() | 496 | 91.13% | auto_structural |
| `0027070c` | pagewinmes_put(PAGEWININFO*, int) | 496 | 95.16% | auto_structural |
| `0028d498` | tlFree(void*) | 496 | 95.97% | auto_structural |
| `0015ad38` | iOSexecuteCurSlide() | 492 | 93.5% | auto_structural |
| `00280108` | cSaveFFT::Execute() | 488 | 98.36% | auto_structural |
| `0028d24c` | tlMallocAlign(unsigned int, unsigned int) | 488 | 96.72% | auto_structural |
| `000bbc4c` | CSOUND_IF_SL::Static_CreatePlayer(int, int, int) | 484 | 95.04% | auto_structural |
| `001569ac` | editdirect() | 484 | 91.74% | auto_structural |
| `001d6514` | set_md(unsigned char*) | 484 | 97.52% | auto_structural |
| `002472a8` | ctlsound_main(CTLINFO*) | 484 | 93.39% | needs_review |
| `0015596c` | worldmap_startinit() | 480 | 93.33% | needs_review |
| `0015667c` | world_extend_systemframe(int, int, char*) | 480 | 99.17% | auto_structural |
| `00253f20` | ctlmap_init() | 480 | 90.0% | needs_review |
| `0026c680` | ctltresure_main(CTLINFO*) | 480 | 92.5% | needs_review |
| `001e3324` | setexperience(int, REWARD*) | 476 | 97.48% | auto_structural |
| `002553a8` | ctlhelp2_init(int, int) | 476 | 91.6% | needs_review |
| `0025c4fc` | tokuseijob_check() | 476 | 97.48% | auto_structural |
| `00193c2c` | jDrawTex(RECT16*, short*, COLOR*, int, int) | 472 | 98.31% | auto_structural |
| `0019dc10` | SttsEmploy() | 472 | 89.83% | needs_review |
| `0027207c` | GetNearestUnit(int) | 472 | 92.37% | needs_review |
| `0027a974` | BattleRoutineInit() | 472 | 93.22% | needs_review |
| `0029c340` | GsSortFastSprite | 472 | 98.31% | auto_structural |
| `00077200` | deflateCopy | 468 | 100.0% | auto_structural |
| `001022ec` | Wtutorial_hookfunc() | 464 | 88.79% | auto_structural |
| `001d1a7c` | set_netplayerwork_common(int, int) | 464 | 99.14% | auto_structural |
| `0021c474` | s25_playObject(_EffectTCB*) | 464 | 98.28% | auto_structural |
| `0026dd40` | ctlhentuto_init() | 464 | 92.24% | needs_review |
| `00290ea4` | LoadImage2 | 464 | 95.69% | auto_structural |
| `002608c0` | ctlokng_init(_POINT) | 460 | 92.17% | needs_review |
| `000d8a34` | faceuvclut(tagPOLY_FT4*, int, int*) | 456 | 97.37% | auto_structural |
| `0024cda0` | ctlbrst_active(CTLINFO*) | 456 | 96.49% | auto_structural |
| `0025990c` | ctlhistory_main(CTLINFO*) | 456 | 92.11% | needs_review |
| `0026b0f4` | wld_snpl() | 456 | 93.86% | needs_review |
| `000bc0a4` | CSOUND_IF_SL::Play(int, int, int, int, int) | 452 | 100.0% | auto_structural |
| `001a7884` | SetChrListOne(int) | 452 | 100.0% | auto_structural |
| `001b8c38` | sort_init() | 452 | 87.61% | auto_structural |
| `001d8b58` | get_ability_address(int, ABILITY_COMMON_DATA**, void**) | 452 | 92.04% | needs_review |
| `000bbe7c` | CSOUND_IF_SL::LoadPCM(int, char*, unsigned char*, unsigned int, unsigned int, int) | 448 | 100.0% | auto_structural |
| `001abc4c` | GetShapeData(short, short*) | 448 | 95.54% | auto_structural |
| `0020ebc4` | loadEventAnimation(int, unsigned char*) | 448 | 99.11% | auto_structural |
| `0024e91c` | ctlpersmes_init(int) | 448 | 91.96% | needs_review |
| `00078390` | gzread | 444 | 99.1% | auto_structural |
| `0017c0c0` | UnitBakOne(int) | 444 | 97.3% | auto_structural |
| `0019d304` | DressSellStock() | 444 | 90.99% | needs_review |
| `001bd72c` | UnitBakTwo(int, int) | 444 | 97.3% | auto_structural |
| `0026d7ec` | wld_tutomenu_reset(CTLINFO*) | 444 | 96.4% | auto_structural |
| `000d7bb4` | initstatusback(RECT16*, STTSWINDOWBACK*) | 440 | 98.18% | auto_structural |
| `000ff7a4` | Winitstatusback(RECT16*, STTSWINDOWBACK*) | 440 | 98.18% | auto_structural |
| `0015047c` | setjoinus_net() | 436 | 99.08% | auto_structural |
| `001eb124` | loadAbilityAnimation(tag_animation*, void*) | 436 | 94.5% | needs_review |
| `0020c264` | db_init(int, int, int, unsigned char, unsigned char, unsigned char) | 436 | 94.5% | needs_review |
| `0026c860` | picsand_draw(GsIMAGE*, int) | 436 | 96.33% | auto_structural |
| `00077c18` | gzseek64 | 432 | 100.0% | auto_structural |
| `0019df84` | AccountEmploy() | 432 | 91.67% | needs_review |
| `0026abac` | timeevt_chk() | 432 | 87.96% | needs_review |
| `0027f680` | iOS_Suspend(IOS_RESUME_MODE) | 432 | 99.07% | auto_structural |
| `0020fb18` | db_init_all(int, int, int, unsigned char, unsigned char, unsigned char) | 428 | 96.26% | auto_structural |
| `00247884` | birthday_change(CTLINFO*) | 428 | 94.39% | needs_review |
| `00270520` | valnumwin_set(int, unsigned long, int, _POINT*) | 424 | 93.4% | needs_review |
| `00276788` | CheckUnitActionOK(unsigned char*) | 424 | 94.34% | needs_review |
| `00286140` | pspMapArrayOperate(unsigned int, unsigned char, unsigned char, unsigned int, short*, short*, short*, short*, short*, short*, short*, short*, short*, short*, short*, short*) | 424 | 99.06% | auto_structural |
| `000ab4b0` | CEGL2_FBO::ErrorGL(char const*, char const*, unsigned int) | 420 | 89.52% | needs_review |
| `000aecb8` | CEGL2_SPRITE::ErrorGL(char const*, char const*, unsigned int) | 420 | 86.67% | needs_review |
| `00267ad0` | ctlret_main(CTLINFO*) | 420 | 92.38% | auto_structural |
| `00274018` | ForChantedAction() | 420 | 98.1% | auto_structural |
| `0015a988` | sBattleTouchRotationMain() | 416 | 94.23% | auto_structural |
| `001d3e18` | get_comwindow_data(int) | 416 | 100.0% | auto_structural |
| `0024f4e8` | ctltipsmes_init(int) | 416 | 93.27% | needs_review |
| `002b2814` | SE_Play(int) | 416 | 95.19% | auto_structural |
| `0019dde8` | BuyEmploy() | 412 | 92.23% | needs_review |
| `00225074` | CheckEventGunResult(int, SVECTOR*, int) | 412 | 95.15% | auto_structural |
| `0024e734` | ctlperson_init() | 412 | 90.29% | needs_review |
| `0025bf88` | mkbasept_calc() | 412 | 96.12% | auto_structural |
| `002cb2e8` | __aeabi_frsub | 412 | 99.03% | auto_structural |
| `00123de0` | Wdisp_noframe() | 408 | 97.06% | auto_structural |
| `0013728c` | disp_noframe() | 408 | 97.06% | auto_structural |
| `001ab918` | AbilityLearning(short, short, short) | 408 | 98.04% | auto_structural |
| `0021ef4c` | InitPermanentEffect() | 408 | 92.16% | needs_review |
| `00285f8c` | hockRead(void*, int, unsigned int) | 408 | 83.33% | auto_structural |
| `002cb538` | __mulsf3 | 408 | 100.0% | auto_structural |
| `000e1118` | bgput(tagPOLY_FT4*, RECT16*, RECT16*, BGRECORD*) | 404 | 100.0% | auto_structural |
| `0010fb74` | Wbgput(tagPOLY_FT4*, RECT16*, RECT16*, BGRECORD*) | 404 | 100.0% | auto_structural |
| `00159aac` | asm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 404 | 80.2% | needs_review |
| `0015e5d4` | iOSShiftUnitGet() | 404 | 92.08% | auto_structural |
| `00162080` | wasm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 404 | 80.2% | needs_review |
| `00266a00` | infonumber_put_zero(int, int, GsSPRITE*, GsOT*, int) | 404 | 98.02% | auto_structural |
| `00280304` | Savedata_LoadGameCleared(unsigned char*, int*) | 404 | 95.05% | auto_structural |
| `00284144` | mapclip_load(int) | 404 | 100.0% | auto_structural |
| `002cb2f0` | __subsf3 | 404 | 100.0% | auto_structural |
| `00078d9c` | gzwrite | 400 | 99.0% | auto_structural |
| `000bad78` | CSOUND_IF::Play(int, int, int, int, unsigned char) | 400 | 99.0% | auto_structural |
| `002595c0` | ctlhistory_init() | 400 | 90.0% | needs_review |
| `002b1600` | GX_Init(int) | 400 | 91.0% | auto_structural |
| `002cb2f4` | __addsf3 | 400 | 100.0% | auto_structural |
| `0010d8ec` | Wevent_init() | 396 | 96.97% | auto_structural |
| `001d7538` | get_command_ability(int, int) | 396 | 96.97% | auto_structural |
| `00259780` | ctlhismes_init(int) | 396 | 91.92% | needs_review |
| `002875a8` | Draw_Win(int) | 396 | 93.94% | auto_structural |
| `000af818` | CEGL2_TEX_HYBRID::GL_Load(int, unsigned int*, unsigned int, int, int, int, int, unsigned char*) | 392 | 100.0% | auto_structural |
| `000da83c` | calceffectangle(int, int) | 392 | 96.94% | auto_structural |
| `001cd308` | check_learning(int, unsigned short*) | 392 | 94.9% | needs_review |
| `001d5640` | get_actwindow_data(int, unsigned char*, unsigned char*, unsigned char*) | 392 | 96.94% | auto_structural |
| `002031a4` | iOSsetCursorByTouch(int, int, int, int, int) | 392 | 57.14% | needs_review |
| `00256174` | ctlfsetnum_main(CTLINFO*) | 392 | 90.82% | needs_review |
| `0015daf4` | iOSQSort(short*, short*, short*, short*, int, int, int) | 388 | 100.0% | auto_structural |
| `00176b80` | bChrSort(int) | 388 | 92.78% | auto_structural |
| `001b6c00` | MakeTextureMessage2(unsigned char*, short*, RECT16*, int) | 388 | 100.0% | auto_structural |
| `00201798` | setActionDirection(tag_animation*, tag_animation*) | 388 | 100.0% | auto_structural |
| `0025c928` | ctlshogou_main(CTLINFO*) | 388 | 95.88% | auto_structural |
| `002c9b11` | __gxx_personality_v0 | 388 | 7.22% | needs_review |
| `00094cd4` | _vp_noisemask | 384 | 100.0% | auto_structural |
| `00102504` | Wcalceffectangle(int, int) | 384 | 96.88% | auto_structural |
| `001cced8` | get_ma_result(BWORK*) | 384 | 95.83% | auto_structural |
| `001f4440` | InitAnimationInit() | 384 | 88.54% | auto_structural |
| `00242498` | ctlendroll_init() | 384 | 87.5% | needs_review |
| `002453a4` | fft_ending() | 384 | 91.67% | auto_structural |
| `0024581c` | movie_init(int, int, int, int, int, char*) | 384 | 88.54% | needs_review |
| `0027fe84` | Savedata_Load(unsigned char*, int*) | 384 | 94.79% | needs_review |
| `00287734` | Draw_Lose(int) | 384 | 93.75% | auto_structural |
| `0028e2e4` | CdControl | 384 | 68.75% | needs_review |
| `002b78ac` | RayPick_FT4(tagPOLY_FT4*, int, int) | 384 | 97.92% | auto_structural |
| `00082704` | oggpackB_write | 380 | 98.95% | auto_structural |
| `000b68ac` | CFILE_DAT::Open(char*, int, int) | 380 | 100.0% | auto_structural |
| `0019f798` | MainShop() | 380 | 89.47% | auto_structural |
| `001b8e64` | TutrialInit(int) | 380 | 92.63% | auto_structural |
| `001d205c` | check_trap(unsigned char, unsigned char, unsigned char) | 380 | 93.68% | auto_structural |
| `001d972c` | get_shape2(BWORK*, unsigned char*) | 380 | 54.74% | needs_review |
| `0022a6a4` | _ReadTMD(TMD_PRIM*) | 380 | 84.21% | needs_review |
| `00283fc8` | mapclip_save(int) | 380 | 100.0% | auto_structural |
| `002b2b7c` | SysSE_Play(int, int) | 380 | 95.79% | auto_structural |
| `0020fd1c` | InitializeAll() | 376 | 88.3% | auto_structural |
| `00082578` | oggpack_write | 372 | 98.92% | auto_structural |
| `000d123c` | Ddisp_staticwindow2() | 372 | 97.85% | auto_structural |
| `00123a74` | Edisp_staticwindow2() | 372 | 97.85% | auto_structural |
| `001443b0` | Cdisp_staticwindow2() | 372 | 97.85% | auto_structural |
| `0024f8c0` | ctltipsmes_main(CTLINFO*) | 372 | 93.55% | auto_structural |
| `0026baec` | wldtown_init() | 372 | 91.4% | needs_review |
| `002b052c` | CAPP_INFO::Init(int) | 372 | 97.85% | auto_structural |
| `000ff2cc` | Wdisposetexture(RECT16*) | 368 | 93.48% | auto_structural |
| `0019d634` | MonsterNameInput() | 368 | 88.04% | auto_structural |
| `001d1204` | get_reflection_coord(BWORK*, int, int, int, int*, int*, int*) | 368 | 96.74% | auto_structural |
| `001d9d70` | get_item_number(unsigned short, int) | 368 | 96.74% | auto_structural |
| `00210eac` | initMap(int, int) | 368 | 81.52% | needs_review |
| `00211a28` | SetChangePaletteData(unsigned short, unsigned short, unsigned short, unsigned short, unsigned short) | 368 | 91.3% | auto_structural |
| `0007cf58` | inflateCopy | 364 | 100.0% | auto_structural |
| `000ff4b0` | Wallocatememorywait(int) | 364 | 92.31% | auto_structural |
| `00104a70` | Wdirec4(char*) | 360 | 96.67% | auto_structural |
| `0029c780` | GsSortBoxFill | 360 | 98.89% | auto_structural |
| `000785e8` | gzungetc | 356 | 98.88% | auto_structural |
| `0007874c` | gzgets | 356 | 100.0% | auto_structural |
| `000dc6ec` | direc4(char*) | 356 | 96.63% | auto_structural |
| `000e7da8` | seekcodeplus(int, int, int, int) | 356 | 97.75% | auto_structural |
| `00102f04` | Wseekcodeplus(int, int, int, int) | 356 | 97.75% | auto_structural |
| `001ab67c` | JobEquip(short, short, int) | 356 | 98.88% | auto_structural |
| `0024b824` | ctlbar_exit(CTLINFO*) | 356 | 92.13% | auto_structural |
| `00268220` | wldrute_tblget(WALKINFO*, int, int) | 356 | 98.88% | auto_structural |
| `000b6cd8` | CFILE_DAT::Load(int, int, int) | 352 | 100.0% | auto_structural |
| `0015af24` | iOSexecuteScroll() | 352 | 92.05% | auto_structural |
| `001d1de8` | set_unitcoord(int, unsigned char, unsigned char, unsigned char, unsigned char) | 352 | 96.59% | auto_structural |
| `002878b4` | Draw_Draw(int) | 352 | 94.32% | auto_structural |
| `0029ffac` | RotMatrix | 352 | 100.0% | auto_structural |
| `002cb6d0` | __divsf3 | 352 | 100.0% | auto_structural |
| `001597c0` | disp_worlddhelpmenu() | 348 | 91.95% | auto_structural |
| `001d4468` | check_game_cont() | 348 | 98.85% | auto_structural |
| `001da038` | initBdata() | 348 | 96.55% | auto_structural |
| `001e6368` | forecast_skill(BWORK*, BWORK*, ACT*) | 348 | 91.95% | auto_structural |
| `00244f18` | roll_autochange() | 348 | 97.7% | auto_structural |
| `0024ac38` | vOpn_defscrwin_set(int, int, _POINT*, _POINT*) | 348 | 90.8% | auto_structural |
| `0029aabc` | ReadTIM | 348 | 96.55% | auto_structural |
| `002b582c` | Logo_Init() | 348 | 85.06% | auto_structural |
| `000d78f0` | allocatememorywait(int) | 344 | 91.86% | auto_structural |
| `0012cc1c` | disp_staticwindow2() | 344 | 97.67% | auto_structural |
| `001d5188` | set_sanjutsuability3(int, unsigned char, short*) | 344 | 100.0% | auto_structural |
| `0020fe94` | InitializeHot() | 344 | 88.37% | auto_structural |
| `002578d4` | ctlevtinfo_main(CTLINFO*) | 344 | 90.7% | auto_structural |
| `0025ecd8` | iOSWorldPlayer_Hp_Mp(unsigned int, unsigned int) | 344 | 100.0% | auto_structural |
| `002b32e8` | musicPlayer_FrameMove() | 344 | 96.51% | auto_structural |
| `00248cd0` | ctlcard_main(CTLINFO*) | 340 | 89.41% | auto_structural |
| `00224650` | CheckBowReachable(unsigned char, unsigned char) | 336 | 98.81% | auto_structural |
| `00255a38` | ctlflagset_init() | 336 | 90.48% | needs_review |
| `0026c27c` | ctltresure_init() | 336 | 91.67% | needs_review |
| `00273b78` | MakeMoveAreaNearByDestination(int) | 336 | 98.81% | auto_structural |
| `00081494` | unzLocateFile | 332 | 100.0% | auto_structural |
| `000a6db4` | CGX_SCREEN_CORRECT::Init(int, int, int, int) | 332 | 100.0% | auto_structural |
| `000bac2c` | CSOUND_IF::FrameMove(int, float) | 332 | 98.8% | auto_structural |
| `000bb6e8` | CSOUND_IF_SL::EngineInit(int) | 332 | 97.59% | auto_structural |
| `001d21d8` | get_stop_event(BWORK*) | 332 | 93.98% | auto_structural |
| `00225644` | objectAnim(_EffectTCB*, _Object*) | 332 | 97.59% | auto_structural |
| `0015570c` | worldmap_faceload() | 328 | 95.12% | auto_structural |
| `00269fd8` | snpl_picput() | 328 | 96.34% | auto_structural |
| `0026b724` | worldmap_new() | 328 | 87.8% | auto_structural |
| `0007f240` | _tr_stored_block | 324 | 100.0% | auto_structural |
| `001612d0` | iOSsTchBtlInit() | 324 | 80.25% | auto_structural |
| `002169d0` | InitSound() | 324 | 91.36% | auto_structural |
| `00253d84` | ctltownset_main(CTLINFO*) | 324 | 92.59% | auto_structural |
| `00286600` | pspMapTexUVCorrect(unsigned int, unsigned char, unsigned int, unsigned char*, unsigned char*, unsigned char*, unsigned char*, unsigned char*, unsigned char*, unsigned char*, unsigned char*) | 324 | 98.77% | auto_structural |
| `002b20f4` | onGotoNextMode(int) | 324 | 71.6% | needs_review |
| `0007cdd8` | inflateSync | 320 | 100.0% | auto_structural |
| `00096190` | res0_pack | 320 | 100.0% | auto_structural |
| `00135080` | Wdisp_staticwindow2() | 320 | 97.5% | auto_structural |
| `00289c1c` | pspFftDelete(int*) | 320 | 57.5% | needs_review |
| `000c9504` | attackfaceuvclut(tagPOLY_FT4*, int) | 316 | 97.47% | auto_structural |
| `00100704` | Wfaceuvclut(tagPOLY_FT4*, int, int*) | 316 | 97.47% | auto_structural |
| `0021d408` | doSchedulePtclCommandOnce(unsigned short, unsigned char, _EffectTCB*) | 316 | 96.2% | auto_structural |
| `00243048` | fRoll_mesput(short*) | 316 | 98.73% | auto_structural |
| `0025eea8` | fftCdLoopTim(CDREC*) | 316 | 98.73% | auto_structural |
| `00162d5c` | iOS_IsInYellowMesh(int, int) | 312 | 92.31% | auto_structural |
| `001d2c10` | get_battlebonus(B_BONUS*) | 312 | 93.59% | auto_structural |
| `001dc778` | levelup_one(BWORK*, int) | 312 | 100.0% | auto_structural |
| `0020c418` | db_swap(unsigned long*, unsigned long*) | 312 | 89.74% | auto_structural |
| `002231d8` | GetBowReachableTangent(BowCheckWork*, int*, int*) | 312 | 100.0% | auto_structural |
| `0025a0f0` | ctlhoukmes_init(int) | 312 | 89.74% | needs_review |
| `0027add8` | MakeMapChantedAction() | 312 | 98.72% | auto_structural |
| `002a0eec` | OuterProduct0 | 312 | 100.0% | auto_structural |
| `002b2d10` | Jingle_Play(int) | 312 | 93.59% | auto_structural |
| `000a7ec4` | CEGL2_IF::SetBlendMode(int) | 308 | 88.31% | needs_review |
| `000a94c4` | CEGL2_IF::Draw(CEGL2_SPRITE*, float, float, float, float, float, float, unsigned int, int, int, int, int) | 308 | 100.0% | auto_structural |
| `001d8fd0` | levelup_eggmonster(UM_WORK*, int) | 308 | 98.7% | auto_structural |
| `001e31f0` | add_jobpointB(int, int, unsigned char, int) | 308 | 98.7% | auto_structural |
| `00203070` | setCursorByTouch(int, int, int) | 308 | 49.35% | needs_review |
| `00270b5c` | pageupdown_cursor(PAGEWININFO*) | 308 | 97.4% | auto_structural |
| `0029a490` | xpSetDrawMove | 308 | 100.0% | auto_structural |
| `001a9424` | GetItemType(short, short) | 304 | 98.68% | auto_structural |
| `001d67a8` | get_mapid(int, int, int, int) | 304 | 75.0% | needs_review |
| `0020ee48` | activateCompressedAnimation(int, int) | 304 | 97.37% | auto_structural |
| `00225514` | MemoryMapper() | 304 | 88.16% | auto_structural |
| `00244de8` | roll_bkfade() | 304 | 96.05% | auto_structural |
| `00255908` | ctlflag_winset(CTLINFO*) | 304 | 96.05% | auto_structural |
| `002bf1fc` | Main_Settings_DrawYesNo(int, int, int) | 304 | 96.05% | auto_structural |
| `0024717c` | ctlsound_init() | 300 | 90.67% | needs_review |
| `002530b8` | ctlbrst_zodiac() | 300 | 93.33% | auto_structural |
| `00255054` | ctlmap_eventchk() | 300 | 93.33% | auto_structural |
| `00256ec8` | ctltownmenu_exit(CTLINFO*, int) | 300 | 92.0% | auto_structural |
| `00257af4` | ctlparty_main(CTLINFO*) | 300 | 90.67% | auto_structural |
| `002b3464` | Boot_Init() | 300 | 92.0% | needs_review |
| `001ac3c4` | DrawF4(short*, COLOR*, int, int) | 296 | 97.3% | auto_structural |
| `001b2ac8` | SetJobName() | 296 | 90.54% | auto_structural |
| `001d40a8` | set_monsterability2(int, unsigned char, short*, int, unsigned char*) | 296 | 95.95% | auto_structural |
| `0027ec94` | iOS_CMenuTouchSaveLoad::exec(int*, int*) | 296 | 100.0% | auto_structural |
| `00200bb8` | eventZoomChange(int) | 292 | 93.15% | auto_structural |
| `0025e310` | sun_to_ivarisday(int*, int*) | 292 | 95.89% | auto_structural |
| `002702f0` | scrwin_para_set(int, int, _POINT*, _POINT*) | 292 | 90.41% | auto_structural |
| `002a3648` | pspSaveBase::Update() | 292 | 100.0% | auto_structural |
| `000758c8` | deflateBound | 288 | 100.0% | auto_structural |
| `00079058` | gzvprintf | 288 | 100.0% | auto_structural |
| `0007f388` | _tr_align | 288 | 100.0% | auto_structural |
| `000c18cc` | disp_maptitle() | 288 | 94.44% | auto_structural |
| `000da35c` | event_init_memory() | 288 | 76.39% | auto_structural |
| `00221d64` | RequestHitMarkEffect(long, EffectOrder*, long) | 288 | 93.06% | auto_structural |
| `00249da4` | vOpn_dataload() | 288 | 95.83% | auto_structural |
| `0026af98` | snpl_effcheck(int, int, int) | 288 | 97.22% | auto_structural |
| `002899a0` | pspFftSave(int, FFT_SAVE_DATA*, int*) | 288 | 63.89% | needs_review |
| `0019f914` | ExitShop() | 284 | 91.55% | auto_structural |
| `001a6410` | MessageDataSet(int) | 284 | 83.1% | needs_review |
| `001ccafc` | get_floor_damage(BWORK*) | 284 | 90.14% | auto_structural |
| `0027f904` | iOS_Resume() | 284 | 98.59% | auto_structural |
| `00076cf0` | deflateParams | 280 | 97.14% | auto_structural |
| `000bb38c` | CSOUND_IF::Pause(int, unsigned char) | 280 | 100.0% | auto_structural |
| `00163bb4` | iOS_initTouchDisable(int) | 280 | 91.43% | auto_structural |
| `001ac774` | DrawLineG3(RECT16*, COLOR*, int, int) | 280 | 97.14% | auto_structural |
| `00200e2c` | eventFukanChange(int) | 280 | 92.86% | auto_structural |
| `0024935c` | vOpn_swapbuff() | 280 | 95.71% | auto_structural |
| `0024971c` | vOpn_key_rep(unsigned long) | 280 | 94.29% | auto_structural |
| `000b5e38` | CUI_SCROLLBAR::FrameMove(float) | 276 | 100.0% | auto_structural |
| `000cbc3c` | TrapWindowTaskManager(int, int, short, int) | 276 | 94.2% | auto_structural |
| `00101fe4` | Wevent_init_memory() | 276 | 76.81% | auto_structural |
| `001aec8c` | DrawEquipCategory(int, int, int) | 276 | 94.2% | auto_structural |
| `00244418` | vEnd_rollline_put(unsigned long*, int) | 276 | 97.1% | auto_structural |
| `0026b904` | wldsymbol_init() | 276 | 91.3% | needs_review |
| `00291178` | MoveImage2 | 276 | 94.2% | auto_structural |
| `0029a2d8` | DrawOTag | 276 | 89.86% | auto_structural |
| `002b7378` | RENDER_TO_SCREEN(int, int, int*, int*) | 276 | 91.3% | auto_structural |
| `000d9638` | fade_eventlocal(ITEMPRIM*, int) | 272 | 95.59% | auto_structural |
| `000f38c4` | disp_plateorspell(ACT*, int, int) | 272 | 97.06% | auto_structural |
| `00155b4c` | worldmap_menuinit() | 272 | 89.71% | auto_structural |
| `00159c40` | iosAsmMUL64(long, long, long) | 272 | 98.53% | auto_structural |
| `0015d748` | iOSCurSameOK() | 272 | 89.71% | auto_structural |
| `001dc944` | set_casting_status(BWORK*, unsigned char) | 272 | 85.29% | needs_review |
| `001e21f8` | getskillresult_first(int) | 272 | 91.18% | needs_review |
| `001eb360` | defrost(char*, char*) | 272 | 98.53% | auto_structural |
| `0022588c` | NewObject(short, short) | 272 | 92.65% | auto_structural |
| `002b7268` | SCREEN_TO_RENDER(int, int, int*, int*) | 272 | 91.18% | auto_structural |
| `002c8ac4` | IS_SETTINGS_WND_SLIDER_AREA(int, int) | 272 | 97.06% | auto_structural |
| `000793e0` | inflateBackInit_ | 268 | 97.01% | auto_structural |
| `00082de4` | oggpackB_read | 268 | 100.0% | auto_structural |
| `000a7d1c` | CEGL2_IF::CEGL2_IF() | 268 | 98.51% | auto_structural |
| `00101450` | Wfade_eventlocal(ITEMPRIM*, int) | 268 | 95.52% | auto_structural |
| `0010d738` | Wdisp_plateorspell(ACT*, int, int) | 268 | 97.01% | auto_structural |
| `00159d50` | iosAsmMUL3232(long, long, long, long) | 268 | 98.51% | auto_structural |
| `001d93a4` | add_jobpoint(int, int) | 268 | 100.0% | auto_structural |
| `00200cdc` | startZoomChange(int) | 268 | 94.03% | auto_structural |
| `0022a820` | GetAnimationPosition(int, int, EffectOrder*, SVECTOR*) | 268 | 100.0% | auto_structural |
| `00249ac0` | vOpn_padread() | 268 | 91.04% | auto_structural |
| `002557ac` | ctlhelp_main(CTLINFO*) | 268 | 85.07% | auto_structural |
| `0026c12c` | townbtl_check(int, int*) | 268 | 95.52% | auto_structural |
| `0028b738` | initTaskEmu() | 268 | 92.54% | auto_structural |
| `002b7050` | Main_Novel_GetBtnRect(int*, int*, int*, int*, int*, int*) | 268 | 98.51% | auto_structural |
| `002ca215` | __cxa_call_unexpected | 268 | 0.0% | needs_review |
| `0007f138` | _tr_init | 264 | 98.48% | auto_structural |
| `0007fc50` | _tr_tally | 264 | 95.45% | auto_structural |
| `00088bf4` | _ve_envelope_mark | 264 | 100.0% | auto_structural |
| `000ba3a4` | CSOUND_IF::Init(unsigned int, int, char*, int) | 264 | 100.0% | auto_structural |
| `0015a064` | iosAsmKanjiCopy(char*, char*, tCOPYFIELD*, int) | 264 | 96.97% | auto_structural |
| `001c067c` | addlocalprim3(tagPOLY_FT4*, int) | 264 | 96.97% | auto_structural |
| `0025b8ec` | houkoku_mesput(CTLINFO*, int) | 264 | 92.42% | auto_structural |
| `00082ce0` | oggpack_read | 260 | 98.46% | auto_structural |
| `000bca88` | CSOUND_IF_SL::EngineUninit() | 260 | 100.0% | auto_structural |
| `001537dc` | eventflaginit() | 260 | 81.54% | auto_structural |
| `0019d530` | FighterName() | 260 | 86.15% | auto_structural |
| `001bad9c` | SeExec() | 260 | 92.31% | auto_structural |
| `001d9250` | get_job_change_flag(unsigned char*, unsigned char) | 260 | 100.0% | auto_structural |
| `00249174` | vOpn_parainit() | 260 | 78.46% | auto_structural |
| `00255654` | ctlhelp_init(int, int) | 260 | 87.69% | auto_structural |
| `00259ad4` | ctlhismes_main(CTLINFO*) | 260 | 90.77% | auto_structural |
| `0026a2cc` | snpl_scrdisp() | 260 | 93.85% | needs_review |
| `00280004` | cSaveFFT::Load() | 260 | 96.92% | auto_structural |
| `00282374` | DispClipedPolygonNo(int, int, int) | 260 | 96.92% | auto_structural |
| `0007b080` | inflateInit2_ | 256 | 96.88% | auto_structural |
| `000b1980` | CEGL_PACKET::Alloc(int) | 256 | 100.0% | auto_structural |
| `00137424` | statusfigprint0(int, int, char*, COPYFIELD*) | 256 | 95.31% | auto_structural |
| `001cc9fc` | status_countdown(int) | 256 | 92.19% | auto_structural |
| `001f5320` | displayCursor() | 256 | 96.88% | auto_structural |
| `00210c9c` | setMapVector(SVECTOR*, SVECTOR*) | 256 | 89.06% | auto_structural |
| `00225210` | DoPermanentEffect() | 256 | 89.06% | auto_structural |
| `0024988c` | vOpn_sun2ivaday(int*, int*) | 256 | 95.31% | auto_structural |
| `0024cf68` | ctlbrst_deactive(CTLINFO*) | 256 | 95.31% | auto_structural |
| `00255180` | ctlmap_active(CTLINFO*) | 256 | 90.62% | auto_structural |
| `00266900` | infonumber_put(int, int, GsSPRITE*, GsOT*) | 256 | 96.88% | auto_structural |
| `0027de0c` | iOS_CMenuTouchNum::exec(int*) | 256 | 100.0% | auto_structural |
| `000e0fb8` | initdrmode(DR_MODE*, int) | 252 | 92.06% | needs_review |
| `001bc334` | GetSttsApos(short) | 252 | 88.89% | needs_review |
| `001f5df8` | MydisplayCursor(int) | 252 | 96.83% | auto_structural |
| `0020c834` | mallocAddress(void*, unsigned int) | 252 | 96.83% | auto_structural |
| `00225790` | InitObjectManager() | 252 | 87.3% | needs_review |
| `0026a6d4` | fastpage_print(int, int) | 252 | 95.24% | auto_structural |
| `002b1ff8` | Debug_DrawFPS() | 252 | 90.48% | needs_review |
| `000ba138` | CompareLocalTime(_SYSTEMTIME*, _SYSTEMTIME*) | 248 | 100.0% | auto_structural |
| `0010fa1c` | Winitdrmode(DR_MODE*, int) | 248 | 91.94% | needs_review |
| `0018716c` | CardAccess3() | 248 | 95.16% | auto_structural |
| `00188348` | allitem_count() | 248 | 91.94% | needs_review |
| `001abe0c` | GetShapeNo(CHR_STTS*, int) | 248 | 96.77% | auto_structural |
| `001caa10` | set_ct_weapon(ACT*) | 248 | 67.74% | needs_review |
| `001f5d00` | DrawPanel(int, int, int, int) | 248 | 98.39% | auto_structural |
| `0021b920` | Dynamics(Physics*) | 248 | 98.39% | auto_structural |
| `00224d4c` | CheckGunReachable(unsigned char, unsigned char) | 248 | 98.39% | auto_structural |
| `0022541c` | Free(void*) | 248 | 95.16% | auto_structural |
| `00253a68` | ctlcenter_main(CTLINFO*) | 248 | 87.1% | needs_review |
| `0027ce58` | iOS_CMenuTouch::init(int, int, int, int, int, int, int, int) | 248 | 100.0% | auto_structural |
| `001a2a50` | initMenuTouch(iOS_CMenuTouch*, int) | 244 | 98.36% | auto_structural |
| `001ab824` | AbilityEquip(short, short, short, int) | 244 | 98.36% | auto_structural |
| `001b799c` | SystemWarningTime(int, int) | 244 | 90.16% | needs_review |
| `001d2874` | set_succession_data(BWORK*, int) | 244 | 96.72% | auto_structural |
| `00245720` | strCallback() | 244 | 96.72% | auto_structural |
| `0025c744` | shogou_check() | 244 | 95.08% | auto_structural |
| `00076e08` | deflateEnd | 240 | 100.0% | auto_structural |
| `000b3c24` | CINPUT_IF_TOUCH::Init() | 240 | 100.0% | auto_structural |
| `000dd360` | eventanmreq(char*) | 240 | 100.0% | auto_structural |
| `00100844` | Wcheckkeyok() | 240 | 90.0% | needs_review |
| `001069ac` | Weventanmreq(char*) | 240 | 100.0% | auto_structural |
| `001bc430` | UnitScroll(short*, short*) | 240 | 95.0% | auto_structural |
| `001bdb1c` | DrawShapeWithShadow(short*, COLOR*, int, int) | 240 | 95.0% | auto_structural |
| `00211b98` | ExecuteChangePalette() | 240 | 90.0% | needs_review |
| `0025c3ac` | mkdaypt_calc() | 240 | 93.33% | needs_review |
| `0025c838` | ctlshogou_init() | 240 | 90.0% | needs_review |
| `00266b94` | info_war_funds(GsOT*, GsSPRITE*, GsLINE*) | 240 | 96.67% | auto_structural |
| `0026bf68` | town_touch(_POINT, int*, int*) | 240 | 98.33% | auto_structural |
| `000b4f94` | CRECT::FrameMove(int, int) | 236 | 100.0% | auto_structural |
| `000ef4f4` | hook_jobmenu() | 236 | 89.83% | needs_review |
| `00101650` | Whook_jobmenu() | 236 | 89.83% | needs_review |
| `0015ce74` | iOSMapIconModeSet(int) | 236 | 89.83% | needs_review |
| `001f35dc` | EndAnimation(tag_animation*) | 236 | 94.92% | needs_review |
| `002590e8` | wld_event(int, int) | 236 | 94.92% | needs_review |
| `0025b78c` | houkoku_talkunit(int) | 236 | 86.44% | needs_review |
| `0026be7c` | town_find3(_POINT, int) | 236 | 96.61% | auto_structural |
| `00077598` | gz_error | 232 | 96.55% | auto_structural |
| `000ba8e0` | CSOUND_IF::SetVolume(int, int) | 232 | 98.28% | auto_structural |
| `000be2b4` | CSTEP_BATCH::FrameMove(float) | 232 | 100.0% | auto_structural |
| `000dc604` | eventsetchrcol(char*) | 232 | 100.0% | auto_structural |
| `001ceb14` | reset_status_forevent2(BWORK*) | 232 | 98.28% | auto_structural |
| `00285e50` | pspMsgGet(unsigned int) | 232 | 63.79% | needs_review |
| `00078f2c` | gzputc | 228 | 100.0% | auto_structural |
| `00079224` | gzsetparams | 228 | 100.0% | auto_structural |
| `001eb67c` | myInitShape() | 228 | 78.95% | needs_review |
| `0020f1d0` | getCharacterInfo(int, unsigned short*) | 228 | 98.25% | auto_structural |
| `00223310` | GetParabolaYPos(int, int) | 228 | 98.25% | auto_structural |
| `0028d6ec` | tlCheckHeap() | 228 | 92.98% | needs_review |
| `000813b4` | unzGoToNextFile | 224 | 100.0% | auto_structural |
| `000cbb48` | delTrapWindowTaskall() | 224 | 98.21% | auto_structural |
| `000d115c` | Ddisp_eventwaitwindow() | 224 | 92.86% | needs_review |
| `00123994` | Edisp_eventwaitwindow() | 224 | 92.86% | needs_review |
| `001252d0` | Wdisp_eventwindow() | 224 | 92.86% | needs_review |
| `0012cb3c` | disp_eventwaitwindow() | 224 | 92.86% | needs_review |
| `00134fa0` | Wdisp_eventwaitwindow() | 224 | 92.86% | needs_review |
| `00138234` | disp_eventwindow() | 224 | 92.86% | needs_review |
| `0014bd8c` | Cdisp_eventwaitwindow() | 224 | 92.86% | needs_review |
| `0015588c` | title_menuinit() | 224 | 91.07% | needs_review |
| `0015a33c` | iOSsTchBtlEnd() | 224 | 76.79% | needs_review |
| `001cea0c` | set_walker_result(BWORK*, REWARD*) | 224 | 94.64% | needs_review |
| `001dc29c` | set_eggmonster(int, int, int) | 224 | 96.43% | auto_structural |
| `002541c4` | ctlcenter_init(int) | 224 | 85.71% | needs_review |
| `00264378` | ctlnblwldinfo_init() | 224 | 78.57% | needs_review |
| `00265fd8` | wldpac_init() | 224 | 87.5% | needs_review |
| `00187514` | TimeConvert(int) | 220 | 89.09% | needs_review |
| `001b6d84` | MakeTextureChar(unsigned short, int, int, int) | 220 | 100.0% | auto_structural |
| `001d588c` | set_event_table_skill(BWORK*, ACT*, TURN_TABLE*) | 220 | 98.18% | auto_structural |
| `00218640` | AnimatePermanentObject(int) | 220 | 98.18% | auto_structural |
| `0021d544` | getNextSENo(int) | 220 | 80.0% | needs_review |
| `0025d930` | speed_calc(SPDINFO*, int) | 220 | 100.0% | auto_structural |
| `0026bda0` | town_find(_POINT) | 220 | 96.36% | auto_structural |
| `0027b3a4` | numaSaveDataLoad(unsigned char*) | 220 | 100.0% | auto_structural |
| `002ab620` | GuEmu_ClearTexCache() | 220 | 94.55% | needs_review |
| `002b2ea0` | Jingle_FrameMove() | 220 | 92.73% | needs_review |
| `002b54b4` | Link_Uninit() | 220 | 92.73% | needs_review |
| `002ca79c` | __divsi3 | 220 | 100.0% | auto_structural |
| `00079308` | gzclose_w | 216 | 100.0% | auto_structural |
| `00094bfc` | _vp_psy_clear | 216 | 100.0% | auto_structural |
| `00097970` | res2_forward | 216 | 100.0% | auto_structural |
| `000cb9e0` | readmaptitle() | 216 | 96.3% | auto_structural |
| `000fef24` | Wdisposewindow(MESSAGEPACKET*) | 216 | 94.44% | needs_review |
| `00201b84` | resetActionDirection(tag_animation*) | 216 | 100.0% | auto_structural |
| `00218cf4` | SetDefaultCamera() | 216 | 98.15% | auto_structural |
| `002867a8` | getMovieEventNum(int) | 216 | 68.52% | needs_review |
| `001c02d4` | JobToAbiChg() | 212 | 92.45% | needs_review |
| `001e2124` | afterskillhandle(BWORK*) | 212 | 86.79% | needs_review |
| `001fea38` | rideOnChokobo(tag_animation*, tag_animation*) | 212 | 100.0% | auto_structural |
| `00216530` | activateMusic(int, int, int) | 212 | 94.34% | needs_review |
| `00249f94` | vOpn_pacinit() | 212 | 86.79% | needs_review |
| `0024b6bc` | ctlbar_active(CTLINFO*) | 212 | 94.34% | needs_review |
| `002531e4` | ctltuto_zodiac() | 212 | 90.57% | needs_review |
| `0025e434` | mouke_app_chk(int, int) | 212 | 100.0% | auto_structural |
| `0025efe4` | wlddata_load() | 212 | 92.45% | needs_review |
| `0025f280` | snpl_load(int) | 212 | 86.79% | needs_review |
| `0026ba18` | wldtown_draw() | 212 | 94.34% | needs_review |
| `0027afdc` | IsNeedlessToFear(int) | 212 | 96.23% | auto_structural |
| `0029c518` | GsSortLine | 212 | 98.11% | auto_structural |
| `00082b14` | oggpackB_look | 208 | 100.0% | auto_structural |
| `000bb5fc` | CSOUND_IF_SL::CB_for_Stream(SLAndroidSimpleBufferQueueItf_ const* const*, void*) | 208 | 100.0% | auto_structural |
| `0015a65c` | siOS_TCurSucCheck(unsigned int) | 208 | 78.85% | needs_review |
| `001a9158` | IsItem(int) | 208 | 94.23% | needs_review |
| `001bab78` | GetIwaPadData() | 208 | 88.46% | needs_review |
| `00215adc` | initChangeClut() | 208 | 98.08% | auto_structural |
| `0021d2e0` | CreateEffectTask(char*, short, short) | 208 | 98.08% | auto_structural |
| `00255584` | ctlhelp2_main(CTLINFO*) | 208 | 86.54% | needs_review |
| `0026c05c` | townmenu_check(int, int*) | 208 | 98.08% | auto_structural |
| `00290cf0` | ResetGraph | 208 | 90.38% | needs_review |
| `002a1600` | ColorMatDpq | 208 | 100.0% | auto_structural |
| `002b2644` | EnvSE_Stop(int) | 208 | 94.23% | needs_review |
| `000755e0` | deflateResetKeep | 204 | 100.0% | auto_structural |
| `00082a48` | oggpack_look | 204 | 98.04% | auto_structural |
| `000bdc6c` | CSTEP::FrameMove(float, unsigned int) | 204 | 98.04% | auto_structural |
| `000dbba4` | eventsetstatus(int, int, int, int) | 204 | 96.08% | auto_structural |
| `00103ff4` | Weventsetstatus(int, int, int, int) | 204 | 96.08% | auto_structural |
| `0014bedc` | joinfaceuvclut(tagPOLY_FT4*, int, int*) | 204 | 96.08% | auto_structural |
| `00200a1c` | startKnockBack(tag_animation*, tag_animation*) | 204 | 100.0% | auto_structural |
| `00228c74` | InitShape() | 204 | 82.35% | needs_review |
| `00255e14` | ctlfsetnum_init(int, int) | 204 | 86.27% | needs_review |
| `00270224` | wldpicwin_set(int, RECT16, _POINT, int) | 204 | 98.04% | auto_structural |
| `00273f4c` | SetBMList() | 204 | 98.04% | auto_structural |
| `0027af10` | GetCountToNextTurn(BWORK*) | 204 | 98.04% | auto_structural |
| `0028a6a0` | pspTitleSaveCheck() | 204 | 98.04% | auto_structural |
| `0029c5ec` | GsSortClear | 204 | 96.08% | auto_structural |
| `002a103c` | TransRot_32 | 204 | 98.04% | auto_structural |
| `000d8fe0` | get_cursoroffset(int) | 200 | 92.0% | needs_review |
| `00100df8` | Wget_cursoroffset(int) | 200 | 92.0% | needs_review |
| `0015a7d8` | iOSScrollButtonMove() | 200 | 90.0% | needs_review |
| `0024232c` | vOpn_arzpic_main() | 200 | 98.0% | auto_structural |
| `0024a5c0` | vOpn_winopen_frmcalc(int, RECT16*, RECT16*) | 200 | 96.0% | auto_structural |
| `00257a2c` | ctlparty_init() | 200 | 86.0% | needs_review |
| `002666d4` | winopen_frmcalc(int, RECT16*, RECT16*) | 200 | 96.0% | auto_structural |
| `0029b42c` | GsInitGraph2 | 200 | 96.0% | auto_structural |
| `0029c6b8` | GsGetTimInfo | 200 | 100.0% | auto_structural |
| `002a16d0` | ColorMatCol | 200 | 100.0% | auto_structural |
| `002b1e70` | NowLoading_FrameMove() | 200 | 90.0% | needs_review |
| `000ad938` | CEGL2_SPRITE::Unload(int) | 196 | 100.0% | auto_structural |
| `000da720` | tutorial_hookfunc() | 196 | 85.71% | needs_review |
| `001383a4` | maptest() | 196 | 85.71% | needs_review |
| `001a8508` | GetCommandList(short, short*) | 196 | 97.96% | auto_structural |
| `00200f44` | startFukanChange() | 196 | 91.84% | needs_review |
| `0021025c` | InitializePartyItem() | 196 | 93.88% | needs_review |
| `00211e50` | setPresentClutDataAsDefault(unsigned int, unsigned int, int) | 196 | 93.88% | needs_review |
| `00242268` | vOpn_arzpic_init(int) | 196 | 89.8% | needs_review |
| `0025e508` | person_year_up() | 196 | 93.88% | needs_review |
| `0026ffc8` | wldwin_set(int, RECT16, int, unsigned long*) | 196 | 97.96% | auto_structural |
| `00279b70` | CheckAbilityGet(int, int, int) | 196 | 97.96% | auto_structural |
| `0028dae4` | tlMoveHeap(long long, int) | 196 | 97.96% | auto_structural |
| `002a0bc4` | ScaleMatrixL | 196 | 100.0% | auto_structural |
| `002b77e8` | RayPick_GT3_input(tagPOLY_GT3*, int, int, int, int) | 196 | 100.0% | auto_structural |
| `002cd0c4` | __gnu_Unwind_Backtrace | 196 | 100.0% | auto_structural |
| `0007fd58` | uncompress | 192 | 97.92% | auto_structural |
| `001d9f58` | get_setstatus_max(A_RESULT*) | 192 | 95.83% | auto_structural |
| `0020c774` | mallocForFile(unsigned int) | 192 | 95.83% | auto_structural |
| `0020f350` | callEventEffect(int, int, void*) | 192 | 100.0% | auto_structural |
| `0024a924` | vOpnwin_set(int, RECT16, int, unsigned long*) | 192 | 97.92% | auto_structural |
| `00269870` | snpl_syscur() | 192 | 89.58% | needs_review |
| `002a0b04` | ScaleMatrix | 192 | 100.0% | auto_structural |
| `002a37b0` | pspSaveBase::pspSaveBase() | 192 | 93.75% | needs_review |
| `000d8978` | itemuvclut(tagSPRT*, int) | 188 | 95.74% | auto_structural |
| `000dfa94` | makemessagestructure() | 188 | 91.49% | needs_review |
| `000ff61c` | Wdisposememory(char*) | 188 | 97.87% | auto_structural |
| `00100648` | Witemuvclut(tagSPRT*, int) | 188 | 95.74% | auto_structural |
| `001ce950` | setskillresult_caster(int) | 188 | 87.23% | needs_review |
| `0020c19c` | fftVSyncCallback() | 188 | 87.23% | needs_review |
| `0020c628` | mallocForSound(unsigned int) | 188 | 95.74% | auto_structural |
| `0020f43c` | debugEffectWait() | 188 | 80.85% | needs_review |
| `0025e6f8` | wld_dayread(unsigned long*, int, FINDDAY*) | 188 | 100.0% | auto_structural |
| `00261b0c` | mouke_eventday_chg() | 188 | 93.62% | needs_review |
| `0028b638` | FFT_Main(void*) | 188 | 97.87% | auto_structural |
| `00291098` | StoreImage2 | 188 | 93.62% | needs_review |
| `00291744` | SetDrawEnv | 188 | 100.0% | auto_structural |
| `002a0998` | ApplyMatrixLV | 188 | 97.87% | auto_structural |
| `002ab718` | sceGuEnable | 188 | 97.87% | auto_structural |
| `000bb05c` | CSOUND_IF::FadeVolume(int, int, int, int) | 184 | 100.0% | auto_structural |
| `000bcd0c` | CSOUND_LOADER_PCM::Read(void*, unsigned long, unsigned long*) | 184 | 100.0% | auto_structural |
| `001cd490` | set_learning(BWORK*) | 184 | 97.83% | auto_structural |
| `0020e314` | moveToPanel(int, SVECTOR*, int, int, int) | 184 | 100.0% | auto_structural |
| `00254f9c` | ctltownset_init(int, int) | 184 | 86.96% | needs_review |
| `0027efec` | iOS_CMenuTouchSaveLoad::init(int, int, int, int, int, int, int, int) | 184 | 100.0% | auto_structural |
| `0028d0f8` | tlInitHeap(void*, unsigned int) | 184 | 95.65% | auto_structural |
| `000756ac` | deflateReset | 180 | 97.78% | auto_structural |
| `001cc89c` | check_hide_reset(BWORK*) | 180 | 93.33% | needs_review |
| `001d1150` | resist_monomane_data(BWORK*) | 180 | 95.56% | auto_structural |
| `001ed964` | getTapedDirection() | 180 | 100.0% | auto_structural |
| `001ee1c4` | drawItem(tag_animation*) | 180 | 100.0% | auto_structural |
| `001f00f4` | NewWeaponEquip(int, tag_animation*) | 180 | 97.78% | auto_structural |
| `002101a8` | loadPlayerPartyData(int) | 180 | 93.33% | needs_review |
| `0021589c` | loadBackGradation() | 180 | 97.78% | auto_structural |
| `00215a28` | transferClutData() | 180 | 95.56% | auto_structural |
| `00216308` | readMusic(int) | 180 | 93.33% | needs_review |
| `0021cf30` | InitEffect() | 180 | 86.67% | needs_review |
| `00248c18` | ctlpremov_main(CTLINFO*) | 180 | 88.89% | needs_review |
| `0024ab84` | vOpnpicwin_set(int, RECT16, _POINT, int) | 180 | 97.78% | auto_structural |
| `002856fc` | pspItemGetWeaponData | 180 | 93.33% | needs_review |
| `0029c954` | sceVfpuVector4OuterProductXYZ(ScePspFVector4*, ScePspFVector4 const*, ScePspFVector4 const*) | 180 | 100.0% | auto_structural |
| `002ab7d4` | sceGuDisable | 180 | 97.78% | auto_structural |
| `000bd284` | CSOUND_LOADER_OGG::Read(void*, unsigned long, unsigned long*) | 176 | 100.0% | auto_structural |
| `001568fc` | worldmap_restart() | 176 | 81.82% | needs_review |
| `001abb9c` | GetJobShape(short, short, short*) | 176 | 95.45% | auto_structural |
| `001b6f14` | CountWidthMessage(unsigned char*) | 176 | 97.73% | auto_structural |
| `001d91a0` | init_entry_status(BWORK*) | 176 | 100.0% | auto_structural |
| `001e3988` | get_movetype(BWORK*) | 176 | 100.0% | auto_structural |
| `00201008` | iOSVectorNormal(VECTOR*) | 176 | 97.73% | auto_structural |
| `00249cf4` | vOpn_timload(unsigned long*) | 176 | 100.0% | auto_structural |
| `0025e5cc` | wldday_countup() | 176 | 97.73% | auto_structural |
| `002741bc` | SetMove() | 176 | 95.45% | auto_structural |
| `00285d6c` | pspJobGetTamanegiLevel(unsigned char (*) [3]) | 176 | 100.0% | auto_structural |
| `0029a92c` | LoadTPage | 176 | 100.0% | auto_structural |
| `000757e4` | deflatePrime | 172 | 100.0% | auto_structural |
| `0007ccf0` | inflateSetDictionary | 172 | 100.0% | auto_structural |
| `000af02c` | CEGL2_TEX_HYBRID::CEGL2_TEX_HYBRID() | 172 | 100.0% | auto_structural |
| `000bbb6c` | CSOUND_IF_SL::SetSLDataFormat(int, int, SLDataFormat_PCM_*) | 172 | 95.35% | auto_structural |
| `000da4ac` | event_init_light() | 172 | 88.37% | needs_review |
| `001049c4` | Weventsetchrcol(char*) | 172 | 100.0% | auto_structural |
| `001bd320` | UnitTableInitFirst(short) | 172 | 83.72% | needs_review |
| `001cc950` | status_handle_main(BWORK*) | 172 | 93.02% | needs_review |
| `001cce2c` | get_trap_result(BWORK*) | 172 | 88.37% | needs_review |
| `001d7340` | net_change_bwork() | 172 | 100.0% | auto_structural |
| `0021f0e4` | NewPEffectTCB() | 172 | 97.67% | auto_structural |
| `00225370` | Malloc(unsigned long, long) | 172 | 95.35% | auto_structural |
| `0024998c` | vOpn_iwaprog() | 172 | 83.72% | needs_review |
| `00258e70` | evt_town_cent() | 172 | 86.05% | needs_review |
| `0025903c` | evt_chr() | 172 | 97.67% | auto_structural |
| `002699bc` | snpl_putpara() | 172 | 83.72% | needs_review |
| `0026aeec` | snpl_mreqcore(int) | 172 | 95.35% | auto_structural |
| `00273ea0` | SetBestMoveAnywhereOK() | 172 | 97.67% | auto_structural |
| `00290dc0` | DrawSync | 172 | 86.05% | needs_review |
| `002919c0` | SetDrawMode | 172 | 100.0% | auto_structural |
| `002aca7c` | GuEmu_FrameMove() | 172 | 93.02% | needs_review |
| `002b1f3c` | Offscreen_ReadPixels(int, int, int, int) | 172 | 93.02% | needs_review |
| `00073a2c` | compress2 | 168 | 97.62% | auto_structural |
| `00097e9c` | _book_maptype1_quantvals | 168 | 100.0% | auto_structural |
| `000ab924` | CEGL2_SHADER::Uninit() | 168 | 100.0% | auto_structural |
| `000f39d4` | ask_event(int, int, int, SVECTOR*, int) | 168 | 100.0% | auto_structural |
| `0010d844` | Wask_event(int, int, int, SVECTOR*, int) | 168 | 100.0% | auto_structural |
| `001dbba0` | employ_from_entry(unsigned char*, int, int, int) | 168 | 100.0% | auto_structural |
| `001eec88` | forceChangeAnimation(int, int, tag_animation*) | 168 | 100.0% | auto_structural |
| `002116f0` | padReadGenerate() | 168 | 88.1% | needs_review |
| `00217e14` | InitEffectAnimation() | 168 | 92.86% | needs_review |
| `00248b70` | ctlpremov_init(int, int, int, int, int, char*) | 168 | 88.1% | needs_review |
| `00272598` | SetMoveAreaSafePanelOnly() | 168 | 97.62% | auto_structural |
| `00285cc4` | pspJobGetJobChangeFlag(unsigned char*, unsigned char, unsigned char (*) [3], int) | 168 | 97.62% | auto_structural |
| `002b3610` | Boot_FrameRender() | 168 | 88.1% | needs_review |
| `002ca6d4` | __udivsi3 | 168 | 100.0% | auto_structural |
| `0008b4f0` | floor1_interpolate_fit | 164 | 100.0% | auto_structural |
| `000ba094` | GetLocalTime(_SYSTEMTIME*) | 164 | 100.0% | auto_structural |
| `001bb460` | SetSttsAbi(int) | 164 | 92.68% | needs_review |
| `001f4a88` | initEntryPlayerAnimations() | 164 | 87.8% | needs_review |
| `0021669c` | fadeMusic(int, int) | 164 | 95.12% | auto_structural |
| `0024556c` | movie_exit(int) | 164 | 97.56% | auto_structural |
| `0025dd14` | iOSwldkey_repSet(unsigned long) | 164 | 95.12% | auto_structural |
| `0025e160` | fadeanb_calc(CVECTOR*, CVECTOR*) | 164 | 95.12% | auto_structural |
| `00276cd4` | JudgeStatus(int, BWORK*, int) | 164 | 100.0% | auto_structural |
| `00289ac0` | pspFftLoad(int, FFT_SAVE_DATA*, int*, int) | 164 | 92.68% | needs_review |
| `0029a3ec` | DrawPrim | 164 | 90.24% | needs_review |
| `002b2a94` | SE_SetVol(int, int) | 164 | 92.68% | needs_review |
| `002cce40` | __gnu_Unwind_RaiseException | 164 | 100.0% | auto_structural |
| `00081bb8` | unzCloseCurrentFile | 160 | 100.0% | auto_structural |
| `000960f0` | res0_free_look | 160 | 100.0% | auto_structural |
| `000aec18` | CEGL2_SPRITE::CEGL2_SPRITE() | 160 | 100.0% | auto_structural |
| `000b3d88` | CINPUT_IF_TOUCH::Clear(int) | 160 | 100.0% | auto_structural |
| `000be204` | CSTEP_BATCH::Init(_DATA_STEP_BATCH*, int, int, char*) | 160 | 100.0% | auto_structural |
| `000d6da8` | initpolyft4(tagPOLY_FT4*) | 160 | 100.0% | auto_structural |
| `000fe8cc` | Winitpolyft4(tagPOLY_FT4*) | 160 | 100.0% | auto_structural |
| `0015685c` | load_worldname() | 160 | 95.0% | auto_structural |
| `0015e3e4` | iOSAnimeIDCntGet(int, int) | 160 | 97.5% | auto_structural |
| `001d4008` | check_monsterup(BWORK*) | 160 | 100.0% | auto_structural |
| `0020de58` | resetAllAnimationDirection() | 160 | 97.5% | auto_structural |
| `0020f728` | checkScrolling() | 160 | 87.5% | needs_review |
| `00211c88` | DisplayChangePalette() | 160 | 87.5% | needs_review |
| `00215254` | loadClutData(unsigned short*, unsigned int, unsigned int, int) | 160 | 97.5% | auto_structural |
| `00217ebc` | NewEffectAnimation(short) | 160 | 92.5% | needs_review |
| `0024452c` | rollline_scroll() | 160 | 97.5% | auto_structural |
| `00261bc8` | endevent_count(int) | 160 | 92.5% | needs_review |
| `002631b4` | ctlmouketeam_active(CTLINFO*) | 160 | 95.0% | auto_structural |
| `002a21e8` | RotColorDpq3 | 160 | 100.0% | auto_structural |
| `002cb248` | __truncdfsf2 | 160 | 100.0% | auto_structural |
| `00078900` | gzclose_r | 156 | 100.0% | auto_structural |
| `0007af1c` | inflateResetKeep | 156 | 100.0% | auto_structural |
| `000bba00` | CSOUND_IF_SL::SetVolume(int, int) | 156 | 100.0% | auto_structural |
| `000da280` | recieve_statusinfo() | 156 | 92.31% | needs_review |
| `000db3a4` | envvolcontrol() | 156 | 100.0% | auto_structural |
| `001bb224` | SetSttsEqu2(int) | 156 | 87.18% | needs_review |
| `001cd9b0` | inc_party_item(BWORK*, unsigned short, BWORK*) | 156 | 94.87% | needs_review |
| `001d2d48` | clear_status_animation(BWORK*) | 156 | 100.0% | auto_structural |
| `001d9104` | set_status_counter(BWORK*, int, int) | 156 | 97.44% | auto_structural |
| `001ed8b0` | getBattleWorkAnimationHight(tag_animation*) | 156 | 100.0% | auto_structural |
| `00216458` | disposeMusic(int) | 156 | 94.87% | needs_review |
| `00221028` | RequestBowEffect(long, EffectOrder*) | 156 | 94.87% | needs_review |
| `00271504` | GetDirectionForPanel(signed char*, signed char*) | 156 | 100.0% | auto_structural |
| `00273d20` | IsNullUnit(int) | 156 | 94.87% | needs_review |
| `0027faa0` | iOS_SuspendWorldMap() | 156 | 97.44% | auto_structural |
| `00077b80` | gzrewind | 152 | 100.0% | auto_structural |
| `0007854c` | gzgetc | 152 | 100.0% | auto_structural |
| `0007afe8` | inflateReset2 | 152 | 100.0% | auto_structural |
| `00125238` | Wrecover_windows(int, int) | 152 | 92.11% | needs_review |
| `0013819c` | recover_windows(int, int) | 152 | 92.11% | needs_review |
| `0014dd4c` | addbpitem(int) | 152 | 100.0% | auto_structural |
| `0015e484` | iOSAnimeIDCntGet2(BWORK*, int) | 152 | 97.37% | auto_structural |
| `001a7404` | SetRyoteFlag(short*, int) | 152 | 100.0% | auto_structural |
| `001bd3cc` | UnitListInit() | 152 | 89.47% | needs_review |
| `001ed6fc` | getDestAnimationHight(tag_animation*) | 152 | 100.0% | auto_structural |
| `001ed818` | getOriginalAnimationHight(tag_animation*) | 152 | 100.0% | auto_structural |
| `0021f328` | GetPermanentObject() | 152 | 89.47% | needs_review |
| `002432e4` | fRoll_cdxareq(short*) | 152 | 97.37% | auto_structural |
| `0025f1e8` | wldmes_load(int) | 152 | 84.21% | needs_review |
| `00263254` | ctlmouketeam_deactive(CTLINFO*) | 152 | 94.74% | needs_review |
| `0026b86c` | wldsymbol_draw() | 152 | 97.37% | auto_structural |
| `0026ff30` | wldwintex_point(int, RECT16, _POINT*) | 152 | 100.0% | auto_structural |
| `002cb0c0` | __gedf2 | 152 | 92.11% | needs_review |
| `0007cc5c` | inflateGetDictionary | 148 | 100.0% | auto_structural |
| `000ac0a0` | CEGL2_SHADER::Unload(int) | 148 | 100.0% | auto_structural |
| `000b6588` | CCRYPT::Encrypt(unsigned char*, int, unsigned int) | 148 | 100.0% | auto_structural |
| `000d665c` | addlocalprim(tagPOLY_FT4*) | 148 | 94.59% | needs_review |
| `000d7d6c` | sttsback_blue(STTSWINDOWBACK*) | 148 | 94.59% | needs_review |
| `000da63c` | export_suc(int) | 148 | 91.89% | needs_review |
| `000e14f4` | statusfigprint10(int, int, char*, COPYFIELD*) | 148 | 91.89% | needs_review |
| `000fe1a4` | Waddlocalprim(tagPOLY_FT4*) | 148 | 94.59% | needs_review |
| `00102208` | Wexport_suc(int) | 148 | 91.89% | needs_review |
| `0015a1e8` | iOSLRChgSwype(int, int, int, int) | 148 | 100.0% | auto_structural |
| `0015a744` | iOSScrollButtonAreaCheck() | 148 | 94.59% | needs_review |
| `0015d6b4` | iOSTchCurUnitCheck() | 148 | 86.49% | needs_review |
| `0015da60` | iOSSwap(short*, short*, short*, short*, int, int) | 148 | 100.0% | auto_structural |
| `001d5968` | set_turn_end(int) | 148 | 97.3% | auto_structural |
| `001f5b50` | terminateAnimationSub(int, int, short, short, short) | 148 | 100.0% | auto_structural |
| `002161e0` | loadMusic(int) | 148 | 91.89% | needs_review |
| `0026640c` | wldpac_draw(GsOT*, unsigned long*, int) | 148 | 94.59% | needs_review |
| `00266544` | iOS_drawMenuAssist_wld(iOS_CMenuTouch*, GsOT*) | 148 | 100.0% | auto_structural |
| `00268be0` | wldcenter_set(_POINT*, SVECTOR*) | 148 | 94.59% | needs_review |
| `00268ec4` | wldcenter_move() | 148 | 94.59% | needs_review |
| `002766f4` | GetHightDistance(unsigned char*, BWORK*) | 148 | 94.59% | needs_review |
| `00290b54` | ClearOTag | 148 | 100.0% | auto_structural |
| `002b6b38` | Main_Uninit() | 148 | 94.59% | needs_review |
| `002b715c` | setPspDispNum(short, short, short) | 148 | 89.19% | needs_review |
| `002bb678` | iOSMenuOkCancelHelpGet(int, int) | 148 | 94.59% | needs_review |
| `00097b70` | _float32_pack | 144 | 88.89% | needs_review |
| `000b8ca4` | CSTR_UTIL::GetFile(char*, char*) | 144 | 100.0% | auto_structural |
| `000d7b24` | sttsback_normal(STTSWINDOWBACK*) | 144 | 94.44% | needs_review |
| `000ff95c` | Wsttsback_blue(STTSWINDOWBACK*) | 144 | 94.44% | needs_review |
| `0011d6b0` | TEST_read_eventflag(int) | 144 | 97.22% | auto_structural |
| `001253b0` | Wextend_valuefield(int) | 144 | 91.67% | needs_review |
| `00138314` | extend_valuefield(int) | 144 | 91.67% | needs_review |
| `001532c0` | task_create(long, char*) | 144 | 94.44% | needs_review |
| `00153584` | Wtask_create(long, char*) | 144 | 94.44% | needs_review |
| `001a8b94` | AbilityCompare(C_STTS*, short, short) | 144 | 100.0% | auto_structural |
| `001d6718` | get_mapstp(int, int, int) | 144 | 91.67% | needs_review |
| `00207d6c` | iOS_mapVectorLimit() | 144 | 91.67% | needs_review |
| `0020e228` | get2DPosition(SVECTOR*, SVECTOR*) | 144 | 86.11% | needs_review |
| `00221e84` | RequestLandingEffect(EffectOrder*, VECTOR*) | 144 | 94.44% | needs_review |
| `00245690` | strInit(int, void (*)()) | 144 | 97.22% | auto_structural |
| `0025e204` | wldfade_mask() | 144 | 91.67% | needs_review |
| `0026dc2c` | ctltuto_active(CTLINFO*) | 144 | 94.44% | needs_review |
| `00273e10` | CompareMove(MOVE*, MOVE*) | 144 | 97.22% | auto_structural |
| `00291824` | SetDrawLoad | 144 | 100.0% | auto_structural |
| `00292678` | __xpLibgpuDrawCallBack(int) | 144 | 83.33% | needs_review |
| `002abc8c` | sceGuTexFilter | 144 | 94.44% | needs_review |
| `002cb0c8` | __ledf2 | 144 | 97.22% | auto_structural |
| `000a9430` | CEGL2_IF::Init() | 140 | 97.14% | auto_structural |
| `000bc9fc` | CSOUND_IF_SL::Unload(int) | 140 | 100.0% | auto_structural |
| `000da9c4` | checkpara1(int) | 140 | 100.0% | auto_structural |
| `000dfb50` | recover_chrname() | 140 | 97.14% | auto_structural |
| `000ff718` | Wsttsback_normal(STTSWINDOWBACK*) | 140 | 94.29% | needs_review |
| `00102e14` | Wenvvolcontrol() | 140 | 100.0% | auto_structural |
| `0010c7fc` | Wrecover_chrname() | 140 | 97.14% | auto_structural |
| `001b6a74` | MessageMake(unsigned char*, unsigned char*, short*, int) | 140 | 100.0% | auto_structural |
| `001bb504` | SetSttsBoth(int) | 140 | 91.43% | needs_review |
| `001dc37c` | inc_dead_number(BWORK*) | 140 | 97.14% | auto_structural |
| `00216154` | loadMusicBuffer(int, int) | 140 | 91.43% | needs_review |
| `0021627c` | readMusicBuffer(int, int) | 140 | 94.29% | needs_review |
| `0022a618` | _OpenTMD(unsigned long*, int) | 140 | 97.14% | auto_structural |
| `00245e38` | ctlstartmov_init(int, int, int, int) | 140 | 85.71% | needs_review |
| `002562fc` | sthelp_curpos_set(CTLINFO*) | 140 | 94.29% | needs_review |
| `0025e7b4` | wldfrm_clr(int) | 140 | 97.14% | auto_structural |
| `00284314` | Init_VectorDataBaseObject(VECTOR_DATABASE_CONTAINER*, unsigned int) | 140 | 100.0% | auto_structural |
| `00284594` | new_Vector(VECTOR_DATABASE*, SVECTOR const*) | 140 | 100.0% | auto_structural |
| `002889cc` | pspOffScreenInit(RECT16*, RECT16*) | 140 | 97.14% | auto_structural |
| `0028e5e0` | pspNetPadRead | 140 | 97.14% | auto_structural |
| `0029b544` | GsClearOt | 140 | 100.0% | auto_structural |
| `002cb4ac` | __aeabi_ul2f | 140 | 82.86% | needs_review |
| `00080844` | unzStringFileNameCompare | 136 | 100.0% | auto_structural |
| `000db83c` | read_eventflag(int) | 136 | 97.06% | auto_structural |
| `000e5680` | disp_status2() | 136 | 85.29% | needs_review |
| `000e5708` | disp_status2right() | 136 | 85.29% | needs_review |
| `00103400` | Wread_eventflag(int) | 136 | 97.06% | auto_structural |
| `00161da4` | iOSGetStatuswindowTap() | 136 | 100.0% | auto_structural |
| `001d2de4` | init_status_animation(int) | 136 | 97.06% | auto_structural |
| `0020db18` | setBackColorOffset(short, short, short) | 136 | 97.06% | auto_structural |
| `00224cc4` | GetPermanentEffectAnimationAngle() | 136 | 97.06% | auto_structural |
| `00228d40` | InitPermanentShape() | 136 | 82.35% | needs_review |
| `002433dc` | fRoll_cdxastop(short*) | 136 | 97.06% | auto_structural |
| `00269798` | snpl_wait() | 136 | 88.24% | needs_review |
| `002715a0` | CountMap(unsigned short (*) [18]) | 136 | 97.06% | auto_structural |
| `002b85f8` | RayPick_GT4(tagPOLY_GT4*, int, int) | 136 | 94.12% | needs_review |
| `002b8680` | RayPick_GT3(tagPOLY_GT3*, int, int) | 136 | 94.12% | needs_review |
| `002cb0d0` | __eqdf2 | 136 | 100.0% | auto_structural |
| `0007d9ac` | fill_fopen_filefunc | 132 | 78.79% | needs_review |
| `0007da30` | fill_fopen64_filefunc | 132 | 78.79% | needs_review |
| `0011bfa8` | Wdisp_status2() | 132 | 84.85% | needs_review |
| `0011c02c` | Wdisp_status2right() | 132 | 84.85% | needs_review |
| `0015dfbc` | iOSActiveUnitGet() | 132 | 93.94% | needs_review |
| `001a8b10` | GetAbilityParameter(short, C_STTS*) | 132 | 100.0% | auto_structural |
| `001abb18` | MakeChr(short) | 132 | 93.94% | needs_review |
| `0021a5c4` | SearchNextScheduleDividePos(short, short, long*, long*) | 132 | 96.97% | auto_structural |
| `0024a414` | vOpn_pacdraw(unsigned long*, unsigned long*, int) | 132 | 96.97% | auto_structural |
| `0026a120` | snpl_rndjp() | 132 | 93.94% | needs_review |
| `0026dcbc` | ctltuto_deactive(CTLINFO*) | 132 | 93.94% | needs_review |
| `00280498` | cSaveFFT::Delete() | 132 | 100.0% | auto_structural |
| `0028d7d0` | tlHeapStat(tl_mem_stat_t*) | 132 | 96.97% | auto_structural |
| `00290be8` | ClearOTagR | 132 | 100.0% | auto_structural |
| `00290c6c` | AddPrim | 132 | 96.97% | auto_structural |
| `002a2740` | PadInitDirect | 132 | 96.97% | auto_structural |
| `002b2714` | EnvSE_SetVol(int, int) | 132 | 90.91% | needs_review |
| `002bf364` | Debug_SetMapPolyCheck(int) | 132 | 96.97% | auto_structural |
| `000d9790` | wait_overlay(int) | 128 | 90.62% | needs_review |
| `000d9988` | wait_loaddata(int) | 128 | 90.62% | needs_review |
| `000dc994` | movetopanelsub(char*) | 128 | 100.0% | auto_structural |
| `001015a4` | Wwait_overlay(int) | 128 | 90.62% | needs_review |
| `00101888` | Wwait_loaddata(int) | 128 | 90.62% | needs_review |
| `00103f50` | Wmovetopanelsub(char*) | 128 | 100.0% | auto_structural |
| `0015df3c` | iOSTapCalcu() | 128 | 87.5% | needs_review |
| `001bc520` | scroll_chk() | 128 | 87.5% | needs_review |
| `001d3d98` | check_act_ok(BWORK*) | 128 | 96.88% | auto_structural |
| `0020e3cc` | jumpToPanel(int, int, int) | 128 | 100.0% | auto_structural |
| `0020f7f4` | prepareForEventGun(int, int) | 128 | 100.0% | auto_structural |
| `00245610` | strSetDefDecEnv(DECENV*, int, int, int, int) | 128 | 90.62% | needs_review |
| `00249f14` | vOpn_dataload2() | 128 | 93.75% | needs_review |
| `0024ab04` | vOpnwin_noropen(int, RECT16, int, int, unsigned long*) | 128 | 96.88% | auto_structural |
| `0024fd74` | pspCtltutonet_deactive(CTLINFO*) | 128 | 93.75% | needs_review |
| `0025f0b8` | pic_load(int) | 128 | 87.5% | needs_review |
| `0025f168` | bk_load(int) | 128 | 87.5% | needs_review |
| `0025f358` | psp_bk_load(int, void*) | 128 | 90.62% | needs_review |
| `00266654` | add_winpac(unsigned long*, int*) | 128 | 93.75% | needs_review |
| `002701a4` | wldwin_noropen(int, RECT16, int, int, unsigned long*) | 128 | 96.88% | auto_structural |
| `0027b240` | GetCountToDeath(BWORK*) | 128 | 100.0% | auto_structural |
| `002b3590` | Boot_FrameMove() | 128 | 90.62% | needs_review |
| `000791a8` | gzflush | 124 | 100.0% | auto_structural |
| `000ba684` | CSOUND_IF::Stop(int) | 124 | 100.0% | auto_structural |
| `000ba774` | CSOUND_IF::IsPlaying(int, int) | 124 | 100.0% | auto_structural |
| `000bb8c8` | CSOUND_IF_SL::Pause(int) | 124 | 100.0% | auto_structural |
| `000daff0` | move_ambient() | 124 | 96.77% | auto_structural |
| `00102aa4` | Wmove_ambient() | 124 | 96.77% | auto_structural |
| `00105510` | Wwait_direc(int) | 124 | 93.55% | needs_review |
| `00159924` | asmTaskEntry() | 124 | 93.55% | needs_review |
| `00161ef8` | wasmTaskEntry() | 124 | 93.55% | needs_review |
| `0016a14c` | ASURA_soundStop() | 124 | 90.32% | needs_review |
| `001baae8` | SttsAMovingChk() | 124 | 90.32% | needs_review |
| `001dbc48` | init_entry_status0(BWORK*) | 124 | 100.0% | auto_structural |
| `0020c550` | db_swap_generate(unsigned long*, unsigned long*) | 124 | 90.32% | needs_review |
| `00210d9c` | NewEntry(int, int, int, short, short, short, short, BWORK*, int) | 124 | 96.77% | auto_structural |
| `0024a544` | vOpn_add_winpac(unsigned long*, int*) | 124 | 93.55% | needs_review |
| `0024a9e4` | vOpnwin_trans(int, unsigned long*) | 124 | 96.77% | auto_structural |
| `0025da0c` | wldkey_repinit() | 124 | 83.87% | needs_review |
| `002665d8` | add_anmpac(unsigned long*, int*) | 124 | 93.55% | needs_review |
| `00269bc0` | snpl_timeset() | 124 | 83.87% | needs_review |
| `0027008c` | wldwin_trans(int, unsigned long*) | 124 | 96.77% | auto_structural |
| `00271da0` | EvaluateAllUnitAction() | 124 | 96.77% | auto_structural |
| `00279eec` | SetTrapPanel(int, int, int) | 124 | 96.77% | auto_structural |
| `0027d6b4` | iOS_CMenuTouchNum::init(int, int, int, int, int, int, int, int, int) | 124 | 100.0% | auto_structural |
| `0028bec0` | TE_VSync(int) | 124 | 90.32% | needs_review |
| `0029a89c` | SetDefDrawEnv | 124 | 100.0% | auto_structural |
| `002b2798` | SE_CorrectFID(int) | 124 | 93.55% | needs_review |
| `002b2a18` | SE_StopVFX(int) | 124 | 90.32% | needs_review |
| `002b36dc` | Error_FrameRender() | 124 | 90.32% | needs_review |
| `002cb4bc` | __aeabi_l2f | 124 | 100.0% | auto_structural |
| `000b6834` | CFILE_DAT::CFILE_DAT() | 120 | 100.0% | auto_structural |
| `000d7e00` | load_replaceitems(int, int) | 120 | 56.67% | needs_review |
| `000dcc2c` | wait_direc(int) | 120 | 93.33% | needs_review |
| `000ff9ec` | Wload_replaceitems(int, int) | 120 | 56.67% | needs_review |
| `0015d2ac` | iOS_GameAreaCheck() | 120 | 83.33% | needs_review |
| `001789e0` | iOS_addPrim_graphic(tagPOLY_FT4*, short) | 120 | 96.67% | auto_structural |
| `001a47e0` | pspAbilityCompareSupport(short, short) | 120 | 90.0% | needs_review |
| `001a92f8` | ItemCheck() | 120 | 96.67% | auto_structural |
| `001ab104` | IsUntauchable(int) | 120 | 96.67% | auto_structural |
| `001adcec` | iOS_addPrim_window_graphics_unitlist(tagPOLY_FT4*, short) | 120 | 96.67% | auto_structural |
| `001d9ee0` | copy_entry_coord(BWORK*, EDATA*) | 120 | 100.0% | auto_structural |
| `001e4e94` | get_step_no(BWORK*) | 120 | 93.33% | needs_review |
| `001fd200` | setTurnOrder() | 120 | 96.67% | auto_structural |
| `0021e760` | doSequence(short) | 120 | 90.0% | needs_review |
| `00245aa8` | o_GetCardEvent() | 120 | 96.67% | auto_structural |
| `00245b78` | o_GetCardEvent_X() | 120 | 96.67% | auto_structural |
| `0024a4cc` | vOpn_add_anmpac(unsigned long*, int*) | 120 | 93.33% | needs_review |
| `00258c78` | evt_deep() | 120 | 96.67% | auto_structural |
| `0025e680` | wld_daywrite(unsigned long*, int, FINDDAY*) | 120 | 100.0% | auto_structural |
| `0028441c` | Clear_VectorDataBaseContainer(VECTOR_DATABASE_CONTAINER*) | 120 | 100.0% | auto_structural |
| `002918ec` | SetTexWindow | 120 | 100.0% | auto_structural |
| `002b1458` | Project_Core_Bootup() | 120 | 96.67% | auto_structural |
| `002c5434` | Movie_FrameRender() | 120 | 90.0% | needs_review |
| `00077524` | gzerror | 116 | 93.1% | needs_review |
| `00081660` | unzGoToFilePos64 | 116 | 100.0% | auto_structural |
| `00082ef0` | oggpack_read1 | 116 | 100.0% | auto_structural |
| `00082f64` | oggpackB_read1 | 116 | 100.0% | auto_structural |
| `00088cfc` | _ve_envelope_shift | 116 | 100.0% | auto_structural |
| `000aa8f8` | CEGL2_FBO::Delete() | 116 | 100.0% | auto_structural |
| `000b8b3c` | CLIST::Create(int, void*) | 116 | 100.0% | auto_structural |
| `000ba700` | CSOUND_IF::StopAll(unsigned char) | 116 | 100.0% | auto_structural |
| `000c81c4` | tool_squareinit() | 116 | 89.66% | needs_review |
| `000d8c00` | checkkeyok() | 116 | 89.66% | needs_review |
| `000e2b04` | statusnowprint(char*, COPYFIELD*) | 116 | 93.1% | needs_review |
| `000ff43c` | Wallocatememoryinit() | 116 | 93.1% | needs_review |
| `001b7ef4` | TruePadRead(int) | 116 | 93.1% | needs_review |
| `001cd058` | adjust_input_flag(BWORK*) | 116 | 100.0% | auto_structural |
| `001d43f4` | check_unit_active(BWORK*) | 116 | 100.0% | auto_structural |
| `001fd168` | setActivePanelFromAction(tag_animation*) | 116 | 89.66% | needs_review |
| `00201708` | setActionStartDirection(tag_animation*) | 116 | 93.1% | needs_review |
| `002042c8` | startTurnRelative(int) | 116 | 89.66% | needs_review |
| `0021cc10` | s1e_ifMetascheduleEnd(_EffectTCB*) | 116 | 93.1% | needs_review |
| `002492b8` | vEnd_init() | 116 | 96.55% | auto_structural |
| `0024c44c` | bgscrol_chk_x(_POINT*, VECTOR*) | 116 | 100.0% | auto_structural |
| `0024c4c0` | bgscrol_chk_y(_POINT*, VECTOR*) | 116 | 100.0% | auto_structural |
| `0024fd00` | pspCtltutonet_active(CTLINFO*) | 116 | 93.1% | needs_review |
| `00258bcc` | evt_exit_sel() | 116 | 96.55% | auto_structural |
| `0025b878` | houkokumes_select(int, int) | 116 | 100.0% | auto_structural |
| `0025d590` | directedit_chk() | 116 | 96.55% | auto_structural |
| `00276bb4` | GetUnitOnPanel(unsigned char*) | 116 | 96.55% | auto_structural |
| `002816bc` | iOS_v2menuSetEnable(V2_MENU_ITEM, int) | 116 | 93.1% | needs_review |
| `002cabdc` | __aeabi_ul2d | 116 | 75.86% | needs_review |
| `002cb830` | __gesf2 | 116 | 89.66% | needs_review |
| `002ccf00` | __gnu_Unwind_Resume | 116 | 100.0% | auto_structural |
| `0007b190` | inflatePrime | 112 | 100.0% | auto_structural |
| `00080a4c` | unzGoToFirstFile | 112 | 100.0% | auto_structural |
| `00082c38` | oggpack_adv | 112 | 100.0% | auto_structural |
| `00097a48` | res1_forward | 112 | 100.0% | auto_structural |
| `000b6e70` | CFILE_DAT::Decode(int, unsigned char*, int) | 112 | 100.0% | auto_structural |
| `000d7880` | allocatememoryinit() | 112 | 92.86% | needs_review |
| `000daa50` | checktaskkind(int) | 112 | 92.86% | needs_review |
| `000db77c` | write_eventflag(int, int) | 112 | 92.86% | needs_review |
| `000e05bc` | addlocalprim2(tagPOLY_FT4*) | 112 | 96.43% | auto_structural |
| `000feeb4` | Wdisposewindowbytask(int) | 112 | 92.86% | needs_review |
| `001026c4` | Wchecktaskkind(int) | 112 | 92.86% | needs_review |
| `00103340` | Wwrite_eventflag(int, int) | 112 | 92.86% | needs_review |
| `0010e0e4` | Waddlocalprim2(tagPOLY_FT4*) | 112 | 96.43% | auto_structural |
| `0015bfac` | iOSTchInputCheckCur() | 112 | 96.43% | auto_structural |
| `001d1f8c` | check_charge(BWORK*, int) | 112 | 96.43% | auto_structural |
| `001d2324` | get_mapitem(BWORK*) | 112 | 96.43% | auto_structural |
| `001eb0b4` | raiseAnimationPriority(int) | 112 | 96.43% | auto_structural |
| `001ed68c` | getTargetAnimationHight(tag_animation*, SVECTOR*) | 112 | 100.0% | auto_structural |
| `00241938` | fftCdRead2(CDREC*, int, int, int, unsigned long*) | 112 | 96.43% | auto_structural |
| `002419d4` | vOpn_arzmes_init(int, int, unsigned long*) | 112 | 96.43% | auto_structural |
| `00254100` | wldctl_init() | 112 | 82.14% | needs_review |
| `0026030c` | ctlmouke_exit(CTLINFO*) | 112 | 82.14% | needs_review |
| `00270490` | curhis_put(int, int, int) | 112 | 92.86% | needs_review |
| `002727fc` | StayAtSafePanel() | 112 | 96.43% | auto_structural |
| `00276c28` | CheckCrystalAndTresureBox() | 112 | 92.86% | needs_review |
| `0028d088` | tlSetHeap(void*) | 112 | 85.71% | needs_review |
| `0028e25c` | OpenEvent(unsigned long, long, long, long (*)()) | 112 | 92.86% | needs_review |
| `002a1798` | gteMIMefunc | 112 | 100.0% | auto_structural |
| `002a23bc` | RotColorDpq3_nom | 112 | 96.43% | auto_structural |
| `002a3240` | pspSaveAuto::pspSaveAuto() | 112 | 96.43% | auto_structural |
| `002ca125` | __cxa_type_match | 112 | 100.0% | auto_structural |
| `00095668` | _vp_ampmax_decay | 108 | 96.3% | auto_structural |
| `00096eb4` | res0_inverse | 108 | 96.3% | auto_structural |
| `00096f20` | res1_inverse | 108 | 96.3% | auto_structural |
| `0009cc9c` | drft_clear | 108 | 100.0% | auto_structural |
| `000b6a58` | CFILE_DAT::Close() | 108 | 100.0% | auto_structural |
| `000d6eac` | iOS_initsprt_num(tagSPRT*, int) | 108 | 100.0% | auto_structural |
| `000d8778` | import_localstatus(char*, char*, char*, char*) | 108 | 92.59% | needs_review |
| `000d9a14` | seekfacefile(int) | 108 | 96.3% | auto_structural |
| `000fe9d0` | WiOS_initsprt_num(tagSPRT*, int) | 108 | 100.0% | auto_structural |
| `00101914` | Wseekfacefile(int) | 108 | 96.3% | auto_structural |
| `0015d858` | iOSCurSameOKMove() | 108 | 92.59% | needs_review |
| `001a9370` | GetTotalItemBackup(short) | 108 | 92.59% | needs_review |
| `001b6e60` | GetCharAdr(unsigned char*, int) | 108 | 100.0% | auto_structural |
| `001d1d20` | appare_unit_f(int) | 108 | 96.3% | auto_structural |
| `0020c930` | freeForFile(void*) | 108 | 92.59% | needs_review |
| `0020f164` | setEventClut(int, int, int) | 108 | 96.3% | auto_structural |
| `0020f2e4` | eventEffectCall(int, int, SVECTOR*) | 108 | 100.0% | auto_structural |
| `002151e8` | resetClutData(unsigned int, unsigned int, int) | 108 | 92.59% | needs_review |
| `00215950` | loadAnbient() | 108 | 96.3% | auto_structural |
| `002159bc` | loadFlatColor() | 108 | 96.3% | auto_structural |
| `0021bf70` | s19_ifChildTaskEQU(_EffectTCB*) | 108 | 100.0% | auto_structural |
| `00245c0c` | o_GetCardState() | 108 | 88.89% | needs_review |
| `00249c58` | vOpn_bk_load(int, unsigned long*) | 108 | 88.89% | needs_review |
| `00259324` | evt_get_date(int*, int*, int*, int*) | 108 | 96.3% | auto_structural |
| `0025c6d8` | shogou_mesput(CTLINFO*) | 108 | 100.0% | auto_structural |
| `00269ec8` | snpl_mesput() | 108 | 92.59% | needs_review |
| `0026a504` | snpl_jparasmall() | 108 | 96.3% | auto_structural |
| `00281730` | iOS_v2menuGetEnable(V2_MENU_ITEM) | 108 | 92.59% | needs_review |
| `00282648` | wgte_color_set_vec(MATRIX const*, int, SVECTOR const*) | 108 | 100.0% | auto_structural |
| `002a2460` | RotColorMatDpq(SVECTOR*, SVECTOR*, CVECTOR*, long*, CVECTOR*, long, long*) | 108 | 100.0% | auto_structural |
| `002ab960` | sceGuGetMemory_for_iOS | 108 | 96.3% | auto_structural |
| `002b2f7c` | musicPlayer_Stop() | 108 | 92.59% | needs_review |
| `002cb838` | __ltsf2 | 108 | 96.3% | auto_structural |
| `00077ad0` | gzdopen | 104 | 96.15% | auto_structural |
| `00082360` | unzSetOffset64 | 104 | 100.0% | auto_structural |
| `000b8ad4` | CLIST::Delete(int) | 104 | 100.0% | auto_structural |
| `000ba51c` | CSOUND_IF::ClearSavedata(int) | 104 | 100.0% | auto_structural |
| `000bc03c` | CSOUND_IF_SL::Static_Load(int) | 104 | 100.0% | auto_structural |
| `0010044c` | Wimport_localstatus(char*, char*, char*, char*) | 104 | 92.31% | needs_review |
| `0015a180` | iOSLRChgTap(int, int, int, int) | 104 | 100.0% | auto_structural |
| `001d18e4` | Resume_MK_BSTR_IsLoaded(int) | 104 | 92.31% | needs_review |
| `001e0ec4` | check_invincible(int, int*) | 104 | 96.15% | auto_structural |
| `001e6938` | setskilldata(ACT*) | 104 | 92.31% | needs_review |
| `0020c6e4` | freeForSound(void*) | 104 | 92.31% | needs_review |
| `00213da4` | startColorRotation(int, int, int, int) | 104 | 96.15% | auto_structural |
| `0021cfe4` | GetEffectTCB() | 104 | 88.46% | needs_review |
| `00259390` | evt_date_high() | 104 | 96.15% | auto_structural |
| `002593f8` | evt_date_low() | 104 | 96.15% | auto_structural |
| `00269aa0` | snpl_chgpara() | 104 | 92.31% | needs_review |
| `00269e04` | snpl_mfadein() | 104 | 92.31% | needs_review |
| `0026a1cc` | snpl_musicstop() | 104 | 92.31% | needs_review |
| `0026b5e4` | ssd_request(int, int) | 104 | 92.31% | needs_review |
| `002738a8` | SetThresholdDoNothing() | 104 | 96.15% | auto_structural |
| `00281a2c` | iOS_v2menuIsInMenu(int, int) | 104 | 96.15% | auto_structural |
| `002a1c78` | RotNclip4 | 104 | 100.0% | auto_structural |
| `002cba30` | __aeabi_d2ulz | 104 | 92.31% | needs_review |
| `00077498` | gzoffset64 | 100 | 100.0% | auto_structural |
| `0007d0f4` | inflateMark | 100 | 100.0% | auto_structural |
| `0007d8b0` | call_zseek64 | 100 | 100.0% | auto_structural |
| `000b9644` | CSTR_UTIL::Find(char*, char*) | 100 | 100.0% | auto_structural |
| `000ba020` | timeGetTimeM() | 100 | 96.0% | auto_structural |
| `000ba5ac` | CSOUND_IF::Unload(int) | 100 | 100.0% | auto_structural |
| `000bd220` | COggMemMapFile::CallbackSeek(void*, long long, int) | 100 | 100.0% | auto_structural |
| `000cbab8` | createEndModeWindow() | 100 | 92.0% | needs_review |
| `000d6e48` | initsprt(tagSPRT*) | 100 | 100.0% | auto_structural |
| `000d8648` | getanimpos(int) | 100 | 96.0% | auto_structural |
| `000db440` | eventenvse() | 100 | 100.0% | auto_structural |
| `000f15a0` | disp_backtotitle_yesno() | 100 | 92.0% | needs_review |
| `000fe96c` | Winitsprt(tagSPRT*) | 100 | 100.0% | auto_structural |
| `00102ea0` | Weventenvse() | 100 | 100.0% | auto_structural |
| `0010638c` | Wdisp_backtotitle_yesno() | 100 | 92.0% | needs_review |
| `001d1a18` | set_playerwork_sp(PENTRY*, unsigned char*, int) | 100 | 92.0% | needs_review |
| `001e20c0` | dec_party_item(BWORK*, unsigned short, int) | 100 | 92.0% | needs_review |
| `001fecc0` | rideOffChokobo(tag_animation*) | 100 | 100.0% | auto_structural |
| `0020e498` | offsetAnimationPosition(int, SVECTOR*) | 100 | 100.0% | auto_structural |
| `0020e4fc` | setOffsetAnimationPosition(int, SVECTOR*) | 100 | 100.0% | auto_structural |
| `00215cbc` | fadeCharacterClut(int, int, unsigned short*) | 100 | 100.0% | auto_structural |
| `0022a268` | getAbsoluteMaximumOf3(short, short, short) | 100 | 100.0% | auto_structural |
| `0024358c` | fRoll_autochg(short*) | 100 | 96.0% | auto_structural |
| `0025e2ac` | mouke_tbl_get(MOUINFO*, int) | 100 | 100.0% | auto_structural |
| `002775dc` | JudgeMovable(int) | 100 | 92.0% | needs_review |
| `0028d1c4` | tlPushHeap(void*) | 100 | 84.0% | needs_review |
| `002a1204` | SquareSS12 | 100 | 100.0% | auto_structural |
| `002a2184` | RotColorDpq | 100 | 100.0% | auto_structural |
| `002b0200` | GlTexEnv_GetTextureSize(int, float*, float*, float*, float*) | 100 | 96.0% | auto_structural |
| `002b0264` | GlTexEnv_GetTextureSize_2X(int, float*, float*, float*, float*) | 100 | 96.0% | auto_structural |
| `002b0718` | CDebugPrint::EngineInit(char*, float) | 100 | 100.0% | auto_structural |
| `002b29b4` | SE_StopAll() | 100 | 88.0% | needs_review |
| `002bf020` | iOS_isInCursorRotate() | 100 | 96.0% | auto_structural |
| `002cb840` | __eqsf2 | 100 | 100.0% | auto_structural |
| `0007cbfc` | inflateEnd | 96 | 100.0% | auto_structural |
| `000a971c` | CEGL2_IF::DrawScrollBG(CEGL2_SPRITE*, float, float, _RECT_F32*, _RECT_F32*) | 96 | 100.0% | auto_structural |
| `000abb28` | CEGL2_SHADER::CompileShader(unsigned int&, void*, unsigned int) | 96 | 100.0% | auto_structural |
| `000b37c0` | CINPUT_DATA::GetUp(int, int) | 96 | 100.0% | auto_structural |
| `000b4e88` | CINPUT_IF_TOUCH::Begin(int, int) | 96 | 100.0% | auto_structural |
| `000b6c70` | CFILE_DAT::GetBuffer(int) | 96 | 100.0% | auto_structural |
| `000bb160` | CSOUND_IF::GetPlaySample(int) | 96 | 100.0% | auto_structural |
| `000bd3b4` | COggMemMapFile::Open(char const*, unsigned int, unsigned int) | 96 | 100.0% | auto_structural |
| `000d7e78` | serchmessagepointer(int) | 96 | 95.83% | auto_structural |
| `000ffa64` | Wserchmessagepointer(int) | 96 | 95.83% | auto_structural |
| `00100320` | Wgetanimpos(int) | 96 | 95.83% | auto_structural |
| `0010c79c` | Wmakemessagestructure() | 96 | 87.5% | needs_review |
| `00150630` | NetEndSyncProc() | 96 | 91.67% | needs_review |
| `0015b604` | iOSTchStatusModeGet() | 96 | 95.83% | auto_structural |
| `0015de8c` | iOSGT4_MapOTZGet(unsigned long, short) | 96 | 95.83% | auto_structural |
| `001a72d8` | ChgMoney(int) | 96 | 95.83% | auto_structural |
| `001a73a4` | ChrNameSet(short, unsigned char*) | 96 | 95.83% | auto_structural |
| `001ade40` | GetItemCategoryPos(int) | 96 | 83.33% | needs_review |
| `001baa18` | unit_isdark() | 96 | 91.67% | needs_review |
| `001bb1c4` | SetSttsA2(int) | 96 | 91.67% | needs_review |
| `001cd0cc` | set_calcmode_think() | 96 | 79.17% | needs_review |
| `001d1ffc` | check_item_left(int, int, int) | 96 | 91.67% | needs_review |
| `001d639c` | check_turn_end(int) | 96 | 95.83% | auto_structural |
| `0020f620` | getMapIDFromAnimationPosition(int) | 96 | 95.83% | auto_structural |
| `00225a68` | GetParentObject(short, short) | 96 | 95.83% | auto_structural |
| `00228de4` | NewShape2(unsigned char) | 96 | 91.67% | needs_review |
| `0024322c` | fRoll_wait(short*) | 96 | 95.83% | auto_structural |
| `00246300` | vOpn_ctlinit(int) | 96 | 91.67% | needs_review |
| `00258da8` | evt_rute_erase() | 96 | 95.83% | auto_structural |
| `0025c49c` | houkokuinf_init(int) | 96 | 87.5% | needs_review |
| `0025d20c` | world_exit() | 96 | 91.67% | needs_review |
| `0026a674` | op_search(int, int) | 96 | 91.67% | needs_review |
| `0029aa24` | AddPrims | 96 | 100.0% | auto_structural |
| `002a251c` | RotNclip3 | 96 | 100.0% | auto_structural |
| `002ab88c` | sceGuBlendFunc | 96 | 87.5% | needs_review |
| `002cabf0` | __floatdidf | 96 | 100.0% | auto_structural |
| `0007d950` | fill_zlib_filefunc64_32_def_from_filefunc32 | 92 | 100.0% | auto_structural |
| `000b5a6c` | CUI_SCROLLBAR::Create(_RECT_S32*, _RECT_S32*, int) | 92 | 100.0% | auto_structural |
| `000da59c` | initatchrrsvcursor(int) | 92 | 95.65% | auto_structural |
| `000e10b4` | initdrmode2(DR_MODE*, RECT16*) | 92 | 95.65% | auto_structural |
| `0010216c` | Winitatchrrsvcursor(int) | 92 | 95.65% | auto_structural |
| `00155d14` | reactive_worldwindow() | 92 | 91.3% | needs_review |
| `00156b90` | hook_tuto(int) | 92 | 86.96% | needs_review |
| `0018e358` | esys_warning(int, int) | 92 | 86.96% | needs_review |
| `001d52e0` | set_chargeability2(int, unsigned char, short*, unsigned char*, unsigned char*) | 92 | 100.0% | auto_structural |
| `00216884` | callMusic(int) | 92 | 95.65% | auto_structural |
| `00216900` | fadeSoundEffect(int, int) | 92 | 95.65% | auto_structural |
| `002423f4` | ctlendmov_init(int, int, int) | 92 | 86.96% | needs_review |
| `00258b70` | evt_exit_jump() | 92 | 95.65% | auto_structural |
| `00258cf0` | evt_fset_exit() | 92 | 95.65% | auto_structural |
| `00258d4c` | evt_rute_grow() | 92 | 95.65% | auto_structural |
| `0026adc0` | snpl_jpageflg_sub(int) | 92 | 91.3% | needs_review |
| `00277f1c` | SetBestMove() | 92 | 95.65% | auto_structural |
| `00288ebc` | pspGetpspPrimWorkBuf(int) | 92 | 91.3% | needs_review |
| `0028d43c` | tlGetAllocSize(void const*) | 92 | 95.65% | auto_structural |
| `00291964` | SetDrawTPage | 92 | 100.0% | auto_structural |
| `002a1174` | SquareSL12 | 92 | 100.0% | auto_structural |
| `002b1e14` | NowLoading_Init() | 92 | 86.96% | needs_review |
| `002b74d4` | IS_GAME_ROT_AREA(int, int) | 92 | 91.3% | needs_review |
| `002b7530` | IS_GAME_MOV_AREA(int, int) | 92 | 91.3% | needs_review |
| `002cb1ec` | __fixdfsi | 92 | 100.0% | auto_structural |
| `002cb92c` | __fixsfsi | 92 | 100.0% | auto_structural |
| `002ccfb8` | _Unwind_VRS_Get | 92 | 73.91% | needs_review |
| `002cd03c` | _Unwind_VRS_Set | 92 | 73.91% | needs_review |
| `00088920` | _ve_envelope_clear | 88 | 100.0% | auto_structural |
| `000ad800` | CEGL2_SPRITE::AddPacket(float, float, CEGL_PACKET*) | 88 | 100.0% | auto_structural |
| `000b942c` | CSTR_UTIL::Conv(char, char, char*) | 88 | 100.0% | auto_structural |
| `000bb838` | CSOUND_IF_SL::Stop(int) | 88 | 100.0% | auto_structural |
| `000c443c` | Aitemmenu_uvclut(short*, int) | 88 | 100.0% | auto_structural |
| `000d13b0` | Ditemmenu_uvclut(short*, int) | 88 | 100.0% | auto_structural |
| `0010fb14` | Winitdrmode2(DR_MODE*, RECT16*) | 88 | 95.45% | auto_structural |
| `00123be8` | Eitemmenu_uvclut(short*, int) | 88 | 100.0% | auto_structural |
| `0012cd74` | itemmenu_uvclut(short*, int) | 88 | 100.0% | auto_structural |
| `001351c0` | Witemmenu_uvclut(short*, int) | 88 | 100.0% | auto_structural |
| `0014be6c` | Citemmenu_uvclut(short*, int) | 88 | 100.0% | auto_structural |
| `00187658` | pspWindowCommonIsType(WINOBJ_TYPE, unsigned char, unsigned char, unsigned char, unsigned char) | 88 | 95.45% | auto_structural |
| `001a6530` | ScriptRead(int, TUTRIAL*) | 88 | 90.91% | needs_review |
| `001ab3b4` | UnitDismiss(short) | 88 | 95.45% | auto_structural |
| `001ca9b8` | reset_toumei_afterskill(BWORK*) | 88 | 90.91% | needs_review |
| `001d62ec` | set_move_end(int) | 88 | 95.45% | auto_structural |
| `001d6344` | set_act_end(int) | 88 | 95.45% | auto_structural |
| `001d8f78` | get_pmaxlevel() | 88 | 95.45% | auto_structural |
| `001dc8b0` | levelup_check(BWORK*) | 88 | 100.0% | auto_structural |
| `0020eadc` | inactivateAnimation(int) | 88 | 100.0% | auto_structural |
| `0020ed84` | activateEventAnimation(int) | 88 | 95.45% | auto_structural |
| `002163bc` | checkReadMusic() | 88 | 95.45% | auto_structural |
| `00218008` | ChangeEffectAnimation(effectAnimation*, unsigned char, short) | 88 | 95.45% | auto_structural |
| `0021b518` | LoadOverlayBin(long) | 88 | 86.36% | needs_review |
| `0021d3b0` | s2_startTask(_EffectTCB*) | 88 | 95.45% | auto_structural |
| `0022a210` | getRandom(short, short) | 88 | 100.0% | auto_structural |
| `0024328c` | fRoll_waitdot(short*) | 88 | 95.45% | auto_structural |
| `00243508` | fRoll_bkfadeout(short*) | 88 | 95.45% | auto_structural |
| `00245c78` | o_Wait_GetCardState(int) | 88 | 100.0% | auto_structural |
| `00249834` | wldbin_loadchk(int) | 88 | 95.45% | auto_structural |
| `0024aaac` | vOpnmess_frm(int, _POINT*) | 88 | 100.0% | auto_structural |
| `00253a10` | wldctl_active() | 88 | 81.82% | needs_review |
| `00253ec8` | wldctl_deactive() | 88 | 81.82% | needs_review |
| `0025f63c` | wldlop_chk() | 88 | 86.36% | needs_review |
| `0026b31c` | snplread_parcalc() | 88 | 90.91% | needs_review |
| `00270b04` | pagenext_cursor(PAGEWININFO*) | 88 | 90.91% | needs_review |
| `00273cc8` | IsAlmostNullUnit(int) | 88 | 90.91% | needs_review |
| `0028b844` | uninitTaskEmu() | 88 | 90.91% | needs_review |
| `0028c768` | CFFT_STATE::AttackTeamFaceIDToUnitATFID(int) | 88 | 90.91% | needs_review |
| `002916b8` | SetDrawArea | 88 | 100.0% | auto_structural |
| `0029b678` | GsSetDrawBuffClip | 88 | 95.45% | auto_structural |
| `002a126c` | TransRotPers3 | 88 | 100.0% | auto_structural |
| `002ab908` | sceGuStart | 88 | 90.91% | needs_review |
| `002b2290` | GX_ApplyVertexScaling(int) | 88 | 90.91% | needs_review |
| `002b2e48` | Jingle_Stop(int) | 88 | 86.36% | needs_review |
| `000824cc` | oggpackB_writetrunc | 84 | 95.24% | auto_structural |
| `000b89b0` | CLIST::DeleteAll() | 84 | 100.0% | auto_structural |
| `000e0568` | export_localpad(long*) | 84 | 90.48% | needs_review |
| `000e0f14` | iOS_assist_addlocalprim2(iOS_CMenuTouch*, int) | 84 | 100.0% | auto_structural |
| `000e2fbc` | statuskanjiprintadv(int, char*, COPYFIELD*) | 84 | 90.48% | needs_review |
| `0010dea4` | Wexport_localpad(long*) | 84 | 90.48% | needs_review |
| `0010f8f4` | WiOS_assist_addlocalprim2(iOS_CMenuTouch*, int) | 84 | 100.0% | auto_structural |
| `0010f948` | iOS_assist_addlocalprim3(iOS_CMenuTouch*, int, int) | 84 | 100.0% | auto_structural |
| `001531f8` | edit_smallpacket() | 84 | 90.48% | needs_review |
| `0019d7e8` | DrawUnits() | 84 | 85.71% | needs_review |
| `0019e134` | SuccessEmploy() | 84 | 90.48% | needs_review |
| `001eed30` | getShapeAddress(unsigned short) | 84 | 85.71% | needs_review |
| `0021c274` | s7_setEditorProc(_EffectTCB*) | 84 | 100.0% | auto_structural |
| `0021c2c8` | s8_mapScrollXYZ(_EffectTCB*) | 84 | 100.0% | auto_structural |
| `0021d1e8` | s3_killChildTask(_EffectTCB*) | 84 | 100.0% | auto_structural |
| `0022531c` | NewHeap(void*, long) | 84 | 95.24% | auto_structural |
| `0022a480` | getVariationAppearPosition(_ParticleParameter*, int, VECTOR*) | 84 | 100.0% | auto_structural |
| `0022a4d4` | getVariationAppearRange(_ParticleParameter*, int, VECTOR*) | 84 | 100.0% | auto_structural |
| `0022a528` | getVariationAppearVec(_ParticleParameter*, int, VECTOR*) | 84 | 100.0% | auto_structural |
| `0022a57c` | getVariationAppearVecRange(_ParticleParameter*, int, VECTOR*) | 84 | 100.0% | auto_structural |
| `002434b4` | fRoll_bkfadein(short*) | 84 | 95.24% | auto_structural |
| `00243bf4` | drawMessage(int) | 84 | 95.24% | auto_structural |
| `00243c48` | DeleteData(tagLIST_STAFFROLL*, tagSTAFFROLL*, tagSTAFFROLL*) | 84 | 100.0% | auto_structural |
| `002459ec` | strSync(DECENV*, int) | 84 | 100.0% | auto_structural |
| `00245cd0` | o_CardCheck() | 84 | 100.0% | auto_structural |
| `00245de4` | vOpn_ctlprog() | 84 | 80.95% | needs_review |
| `0024b02c` | wldmapEntry(int) | 84 | 90.48% | needs_review |
| `00255758` | iOSHelpCheck() | 84 | 90.48% | needs_review |
| `0025d53c` | world_init() | 84 | 100.0% | auto_structural |
| `00265f84` | iOSSDNovelBackLogCheck() | 84 | 90.48% | needs_review |
| `00269b2c` | snpl_jparae() | 84 | 95.24% | auto_structural |
| `00269db0` | snpl_mfadeout() | 84 | 90.48% | needs_review |
| `00269f84` | snpl_backput() | 84 | 95.24% | auto_structural |
| `0026a45c` | snpl_jparane() | 84 | 95.24% | auto_structural |
| `0026a4b0` | snpl_jparabig() | 84 | 95.24% | auto_structural |
| `0026a7d0` | snSound_play(int) | 84 | 95.24% | auto_structural |
| `0026ad5c` | snpl_je_sub(int) | 84 | 95.24% | auto_structural |
| `00273dbc` | CompareScore(SCORE*, SCORE*) | 84 | 100.0% | auto_structural |
| `00288e18` | pspPushScreenRect(RECT16*, RECT16*) | 84 | 95.24% | auto_structural |
| `00289fac` | pspLoadSystemFile() | 84 | 90.48% | needs_review |
| `002a0c88` | TransposeMatrix | 84 | 100.0% | auto_structural |
| `002b5e58` | Logo_Uninit() | 84 | 90.48% | needs_review |
| `002cb988` | __fixunssfsi | 84 | 100.0% | auto_structural |
| `002cdf18` | __aeabi_d2uiz | 84 | 100.0% | auto_structural |
| `00075794` | deflatePending | 80 | 100.0% | auto_structural |
| `000788b0` | gzdirect | 80 | 100.0% | auto_structural |
| `0008247c` | oggpack_writetrunc | 80 | 95.0% | auto_structural |
| `000aad68` | CEGL2_FBO::Begin(int, int) | 80 | 100.0% | auto_structural |
| `000ae4d0` | CEGL2_SPRITE::Draw(float, float) | 80 | 100.0% | auto_structural |
| `000d8830` | makemessagepacket(char*) | 80 | 90.0% | needs_review |
| `000db7ec` | tutorial_syscall(int) | 80 | 95.0% | auto_structural |
| `000e2b78` | statuskanjiprint(int, char*, COPYFIELD*) | 80 | 90.0% | needs_review |
| `00100500` | Wmakemessagepacket(char*) | 80 | 90.0% | needs_review |
| `001033b0` | Wtutorial_syscall(int) | 80 | 95.0% | auto_structural |
| `0015a60c` | siOS_TCurPosGet(unsigned int, int) | 80 | 90.0% | needs_review |
| `001d6430` | eacape_battlefield(int) | 80 | 95.0% | auto_structural |
| `001eee60` | getPositionFromPanel(tag_animation*) | 80 | 100.0% | auto_structural |
| `001f639c` | setLongPositionToPosition(tag_animation*) | 80 | 100.0% | auto_structural |
| `001fce04` | setActivePanelFromAnimation(tag_animation*) | 80 | 85.0% | needs_review |
| `0020c14c` | iOS_isIrobakeEffect() | 80 | 100.0% | auto_structural |
| `0020eb34` | checkJumpReset() | 80 | 95.0% | auto_structural |
| `0021584c` | loadClutDataCalc(unsigned short*, unsigned int, unsigned int, int, short, short, short, int) | 80 | 100.0% | auto_structural |
| `0021c35c` | sb_mapAngle(_EffectTCB*) | 80 | 100.0% | auto_structural |
| `00221f14` | RequestReboundEffect() | 80 | 90.0% | needs_review |
| `00228e98` | GetShapePrim(int) | 80 | 85.0% | needs_review |
| `00243464` | fRoll_bkput(short*) | 80 | 90.0% | needs_review |
| `0024599c` | strNext(DECENV*) | 80 | 100.0% | auto_structural |
| `00249ec4` | vEnd_dataload() | 80 | 90.0% | needs_review |
| `0025396c` | ctlmap_deactive(CTLINFO*) | 80 | 85.0% | needs_review |
| `002591d4` | evt_get_flgdt(int*, int*) | 80 | 95.0% | auto_structural |
| `00269820` | snpl_picclr() | 80 | 90.0% | needs_review |
| `00269c80` | snpl_selparacalc() | 80 | 95.0% | auto_structural |
| `00269f34` | snpl_mesput2() | 80 | 90.0% | needs_review |
| `0026a27c` | snpl_fadein() | 80 | 90.0% | needs_review |
| `0026a40c` | snpl_volchg() | 80 | 95.0% | auto_structural |
| `0026a5fc` | snplinf_clr(SNPLINFO*) | 80 | 100.0% | auto_structural |
| `0026ae2c` | snpl_jstatflg_sub(int) | 80 | 90.0% | needs_review |
| `0026ae8c` | snpl_jlocalflg_sub(int) | 80 | 90.0% | needs_review |
| `00270154` | wldmess_frm(int, _POINT*) | 80 | 100.0% | auto_structural |
| `00282478` | iOS_ClippedInit() | 80 | 95.0% | auto_structural |
| `00288e6c` | pspPopScreenRect(RECT16*, RECT16*) | 80 | 95.0% | auto_structural |
| `0028c690` | CFFT_STATE::UnitIDToFID_SP2(int, int) | 80 | 90.0% | needs_review |
| `002912f8` | LoadClut | 80 | 100.0% | auto_structural |
| `0029b4f4` | GsDefDispBuff | 80 | 95.0% | auto_structural |
| `002a30b0` | xpMallocAlign | 80 | 95.0% | auto_structural |
| `002bb53c` | Main_Suspend() | 80 | 95.0% | auto_structural |
| `00077400` | gzbuffer | 76 | 100.0% | auto_structural |
| `000b3bd8` | CINPUT_IF_TOUCH::CINPUT_IF_TOUCH() | 76 | 100.0% | auto_structural |
| `000bbe30` | CSOUND_IF_SL::Static_DeletePlayer(int) | 76 | 100.0% | auto_structural |
| `000bd998` | CFRAMERATE::CFRAMERATE(float, float) | 76 | 100.0% | auto_structural |
| `000d87e4` | export_localstatus(char*, char*, char*) | 76 | 94.74% | needs_review |
| `000e3010` | statuskanjiprintwithptr(char*, COPYFIELD*, char*) | 76 | 89.47% | needs_review |
| `001004b4` | Wexport_localstatus(char*, char*, char*) | 76 | 94.74% | needs_review |
| `00155d88` | active_worldwindow() | 76 | 94.74% | needs_review |
| `0015a27c` | iOSPressArea() | 76 | 89.47% | needs_review |
| `0015a2c8` | iOSTapArea() | 76 | 89.47% | needs_review |
| `0015ddf8` | iOSGT4_MapXYZ(unsigned long, long, long, long) | 76 | 84.21% | needs_review |
| `001baa78` | sys_warning(int, int) | 76 | 89.47% | needs_review |
| `001cb064` | init_target_result(A_RESULT*) | 76 | 100.0% | auto_structural |
| `001d4cf4` | set_itemitem(int, unsigned char, unsigned char*) | 76 | 100.0% | auto_structural |
| `001d4fc8` | set_katanaitem(int, unsigned char, unsigned char*) | 76 | 100.0% | auto_structural |
| `001d50f0` | set_sanjutsuability2(int, unsigned char, short*) | 76 | 100.0% | auto_structural |
| `001d513c` | set_sanjutsuability1(int, unsigned char, short*) | 76 | 100.0% | auto_structural |
| `001f0504` | resetTargetAnimation(tag_animation*) | 76 | 100.0% | auto_structural |
| `001feb0c` | rideOffChokoboS(tag_animation*) | 76 | 100.0% | auto_structural |
| `00200ae8` | startLeftTurnSub(int) | 76 | 78.95% | needs_review |
| `00200b34` | startRightTurnSub(int) | 76 | 78.95% | needs_review |
| `0020da7c` | popBackColor() | 76 | 89.47% | needs_review |
| `0020e44c` | rideOnChokoboForced(int, int) | 76 | 100.0% | auto_structural |
| `0020ea90` | activateAnimation(int) | 76 | 100.0% | auto_structural |
| `00210320` | InitializeGame(int) | 76 | 100.0% | auto_structural |
| `0021b570` | SeekEffect() | 76 | 89.47% | needs_review |
| `002233f4` | GetLinearPos(VECTOR*, int, int, VECTOR*) | 76 | 100.0% | auto_structural |
| `00243a14` | deleteMessage() | 76 | 89.47% | needs_review |
| `002496d0` | vOpn_key_repinit() | 76 | 84.21% | needs_review |
| `0024aa60` | vOpnmess_put(int, int, _POINT, unsigned long*) | 76 | 94.74% | needs_review |
| `00258f1c` | evt_gil_high() | 76 | 94.74% | needs_review |
| `00258f68` | evt_gil_low() | 76 | 94.74% | needs_review |
| `0025e888` | day_to_month(int, int*, int*) | 76 | 94.74% | needs_review |
| `00263abc` | iOSNovelBrightOn() | 76 | 94.74% | needs_review |
| `0026a5b0` | snpl_meswait() | 76 | 89.47% | needs_review |
| `0026b694` | wldssd_wait() | 76 | 89.47% | needs_review |
| `00270108` | wldmess_put(int, int, _POINT, unsigned long*) | 76 | 94.74% | needs_review |
| `00270414` | defscrwin_set(int, int, _POINT*, _POINT*) | 76 | 89.47% | needs_review |
| `0028469c` | ForEachVector(VECTOR_DATABASE*, short) | 76 | 100.0% | auto_structural |
| `0028bb3c` | TE_task_killmyself() | 76 | 100.0% | auto_structural |
| `0028d6a0` | tlSetMallocUserPointer(void**) | 76 | 94.74% | needs_review |
| `0029ad6c` | xpSetDrawOffset | 76 | 100.0% | auto_structural |
| `0029ae00` | xpLibGetOffset(int*, int*) | 76 | 94.74% | needs_review |
| `002a257c` | RotNclip3_nom | 76 | 94.74% | needs_review |
| `002c99b5` | operator new(unsigned int) | 76 | 5.26% | needs_review |
| `0007744c` | gztell64 | 72 | 100.0% | auto_structural |
| `00077b38` | gzclearerr | 72 | 100.0% | auto_structural |
| `00079010` | gzputs | 72 | 100.0% | auto_structural |
| `000acab8` | CEGL2_SPRITE::Create(int, int) | 72 | 100.0% | auto_structural |
| `000ba354` | CSOUND_IF::Resume() | 72 | 100.0% | auto_structural |
| `000bd474` | CSOUND_LOADER_OGG::Close() | 72 | 100.0% | auto_structural |
| `000bd4bc` | CSOUND_LOADER_OGG::~CSOUND_LOADER_OGG() | 72 | 88.89% | needs_review |
| `00101f3c` | Wrecieve_statusinfo() | 72 | 100.0% | auto_structural |
| `00153278` | task_wait_fast(long) | 72 | 100.0% | auto_structural |
| `001533d8` | task_init() | 72 | 88.89% | needs_review |
| `0015353c` | Wtask_wait_fast(long) | 72 | 100.0% | auto_structural |
| `0015369c` | Wtask_init() | 72 | 88.89% | needs_review |
| `0015de44` | iOSGT4_MapXYZClear(unsigned long) | 72 | 83.33% | needs_review |
| `0019f750` | DrawFunds() | 72 | 83.33% | needs_review |
| `001a93dc` | ChgShopStockItem(short, int) | 72 | 94.44% | needs_review |
| `001cb7fc` | check_reaction_deny2(BWORK*) | 72 | 94.44% | needs_review |
| `001d189c` | Resume_MK_BSTR_Init() | 72 | 88.89% | needs_review |
| `001d533c` | set_chargeability(int, unsigned char, short*) | 72 | 100.0% | auto_structural |
| `001d98c8` | check_status_data2(BWORK*, int) | 72 | 94.44% | needs_review |
| `001eed84` | getSequenceAddress(unsigned short) | 72 | 83.33% | needs_review |
| `00201c5c` | resetTargetDirection(tag_animation*) | 72 | 100.0% | auto_structural |
| `00216984` | stopEffect(int) | 72 | 94.44% | needs_review |
| `0021c154` | s22_addValue(_EffectTCB*) | 72 | 100.0% | auto_structural |
| `0021c19c` | s23_subValue(_EffectTCB*) | 72 | 100.0% | auto_structural |
| `0021c22c` | s6_setPersonalProc(_EffectTCB*) | 72 | 94.44% | needs_review |
| `0021c3ec` | se_mapScale(_EffectTCB*) | 72 | 100.0% | auto_structural |
| `00242450` | vEnd_ctlinit() | 72 | 88.89% | needs_review |
| `00248e24` | vEnd_exit() | 72 | 100.0% | auto_structural |
| `00249a38` | vOpn_month2day(int, int) | 72 | 94.44% | needs_review |
| `00259224` | evt_flag() | 72 | 94.44% | needs_review |
| `0025926c` | evt_flag_high() | 72 | 94.44% | needs_review |
| `002592b4` | evt_flag_low() | 72 | 94.44% | needs_review |
| `002594a0` | evt_brave_high() | 72 | 94.44% | needs_review |
| `002594e8` | evt_brave_low() | 72 | 94.44% | needs_review |
| `00259530` | evt_faith_high() | 72 | 94.44% | needs_review |
| `00259578` | evt_faith_low() | 72 | 94.44% | needs_review |
| `0025e840` | month_to_day(int, int) | 72 | 94.44% | needs_review |
| `0026a234` | snpl_fadeout() | 72 | 88.89% | needs_review |
| `0026b64c` | wldmusic_change(int) | 72 | 94.44% | needs_review |
| `0027d420` | setCancelDisableArea(int, int, int, int, int) | 72 | 88.89% | needs_review |
| `0028464c` | delete_Vector(VECTOR_DATABASE*, short) | 72 | 100.0% | auto_structural |
| `0028674c` | get_movie_filename(int) | 72 | 77.78% | needs_review |
| `0028baf4` | TE_task_get_no() | 72 | 94.44% | needs_review |
| `0028dd2c` | CloseEvent | 72 | 94.44% | needs_review |
| `0029a9dc` | LoadClut2 | 72 | 100.0% | auto_structural |
| `0029b5d0` | GsSwapDispBuff | 72 | 94.44% | needs_review |
| `002a2678` | set_trans_matrix(long, long, long) | 72 | 88.89% | needs_review |
| `002a3068` | xpMalloc | 72 | 94.44% | needs_review |
| `002b3258` | musicPlayer_Pause() | 72 | 88.89% | needs_review |
| `002b32a0` | musicPlayer_Replay() | 72 | 88.89% | needs_review |
| `002b748c` | isInRectUi(_RECT_UI*, int, int) | 72 | 100.0% | auto_structural |
| `002b8750` | iOS_isMovedDist() | 72 | 94.44% | needs_review |
| `000816d4` | unzGoToFilePos | 68 | 100.0% | auto_structural |
| `00081c58` | unzClose | 68 | 100.0% | auto_structural |
| `000910e4` | mdct_clear | 68 | 100.0% | auto_structural |
| `00097c00` | _float32_unpack | 68 | 100.0% | auto_structural |
| `000ba310` | CSOUND_IF::Suspend() | 68 | 100.0% | auto_structural |
| `000bb9b4` | CSOUND_IF_SL::IsPlaying(int) | 68 | 100.0% | auto_structural |
| `000bd1dc` | COggMemMapFile::CallbackRead(void*, unsigned int, unsigned int, void*) | 68 | 100.0% | auto_structural |
| `000bd334` | CSOUND_LOADER_OGG::Seek(unsigned long) | 68 | 100.0% | auto_structural |
| `000d8880` | pushmessagepacket() | 68 | 88.24% | needs_review |
| `000da558` | event_start() | 68 | 88.24% | needs_review |
| `00100550` | Wpushmessagepacket() | 68 | 88.24% | needs_review |
| `0010f9c0` | Wloadcsrc(int, int, int, int) | 68 | 94.12% | needs_review |
| `0019d7a4` | DrawPrice() | 68 | 82.35% | needs_review |
| `001ab7e0` | IsUntauchableAbility(int) | 68 | 94.12% | needs_review |
| `001cab08` | clear_addeffect() | 68 | 88.24% | needs_review |
| `001cd16c` | get_weatherdata() | 68 | 94.12% | needs_review |
| `001cec5c` | setCasterDirection(int, unsigned char) | 68 | 82.35% | needs_review |
| `001dc408` | set_temp_status(BWORK*, int, unsigned char, int) | 68 | 100.0% | auto_structural |
| `001e0384` | check_chokobo(BWORK*) | 68 | 100.0% | auto_structural |
| `001e207c` | getskilldata(int) | 68 | 94.12% | needs_review |
| `001f37e4` | ExecuteAnimations() | 68 | 94.12% | needs_review |
| `001f6d4c` | resetCharacterPanelPosition(tag_animation*) | 68 | 100.0% | auto_structural |
| `002016c4` | reserveCharacterPosition(tag_animation*) | 68 | 100.0% | auto_structural |
| `00204210` | iOS_isCursorOnUnit() | 68 | 82.35% | needs_review |
| `0020e7fc` | getBattleWorkIDFromAnimation(unsigned int) | 68 | 100.0% | auto_structural |
| `00210960` | MenuTest() | 68 | 88.24% | needs_review |
| `00216414` | readMusicBlock(int) | 68 | 94.12% | needs_review |
| `00216618` | effectFadeoutMusic(int, int) | 68 | 94.12% | needs_review |
| `00216740` | tempoMusic(int, int) | 68 | 94.12% | needs_review |
| `00216784` | pitchMusic(int, int) | 68 | 94.12% | needs_review |
| `002167c8` | panpotMusic(int, int) | 68 | 94.12% | needs_review |
| `0021c0cc` | s20_countUp(_EffectTCB*) | 68 | 100.0% | auto_structural |
| `0021c110` | s21_countDown(_EffectTCB*) | 68 | 100.0% | auto_structural |
| `0022a5d0` | efrand(int, int) | 68 | 100.0% | auto_structural |
| `00242618` | ctlendmov_main(CTLINFO*) | 68 | 88.24% | needs_review |
| `0024a068` | vOpn_pacloop() | 68 | 82.35% | needs_review |
| `00258fb4` | evt_dead_high() | 68 | 94.12% | needs_review |
| `00258ff8` | evt_dead_low() | 68 | 94.12% | needs_review |
| `00268b9c` | wldcenter_calc(SVECTOR*, VECTOR*) | 68 | 100.0% | auto_structural |
| `00269c3c` | snpl_mesput3() | 68 | 94.12% | needs_review |
| `0026b6e0` | iOSwldssd_wait() | 68 | 88.24% | needs_review |
| `002706c8` | pageanmpac_reset(int, int, int) | 68 | 94.12% | needs_review |
| `00273864` | GetDestinationRange() | 68 | 94.12% | needs_review |
| `00277640` | SetThisDestination(unsigned char*) | 68 | 94.12% | needs_review |
| `00291348` | GetTPage | 68 | 100.0% | auto_structural |
| `0029a858` | SetDefDispEnv | 68 | 100.0% | auto_structural |
| `0029fef0` | ratan2 | 68 | 94.12% | needs_review |
| `002a0878` | PushMatrix | 68 | 88.24% | needs_review |
| `002a08bc` | PopMatrix | 68 | 88.24% | needs_review |
| `002b2b38` | SysSE_Stop(int) | 68 | 88.24% | needs_review |
| `002b758c` | IS_ICON_AREA(int) | 68 | 88.24% | needs_review |
| `002cb9ec` | __fixdfdi | 68 | 100.0% | auto_structural |
| `0007a720` | inflateBackEnd | 64 | 100.0% | auto_structural |
| `0007cf18` | inflateSyncPoint | 64 | 100.0% | auto_structural |
| `000b41ec` | CINPUT_IF_TOUCH::GetTouchCount() | 64 | 100.0% | auto_structural |
| `000b9fe0` | timeGetTime() | 64 | 93.75% | needs_review |
| `000d7ae4` | addstatusback(STTSWINDOWBACK*) | 64 | 100.0% | auto_structural |
| `000d9a80` | send_sttslinecol(char*) | 64 | 93.75% | needs_review |
| `000d9eec` | extend_endornot() | 64 | 93.75% | needs_review |
| `000f1560` | disp_resume_yesno() | 64 | 93.75% | needs_review |
| `000fb554` | chkMessagepacket() | 64 | 93.75% | needs_review |
| `000ff6d8` | Waddstatusback(STTSWINDOWBACK*) | 64 | 100.0% | auto_structural |
| `00101ba8` | Wextend_endornot() | 64 | 93.75% | needs_review |
| `0010212c` | Wevent_start() | 64 | 87.5% | needs_review |
| `00102684` | Wcheckpara1(int) | 64 | 100.0% | auto_structural |
| `0010634c` | Wdisp_resume_yesno() | 64 | 93.75% | needs_review |
| `00153398` | task_killmyself() | 64 | 87.5% | needs_review |
| `0015365c` | Wtask_killmyself() | 64 | 87.5% | needs_review |
| `00155cac` | world_stopnoend(int) | 64 | 93.75% | needs_review |
| `0015d9e0` | iOSTchCurLimit(int) | 64 | 93.75% | needs_review |
| `00187618` | GetLocalJobNumber(short) | 64 | 100.0% | auto_structural |
| `001adea0` | GetItemPos(int) | 64 | 87.5% | needs_review |
| `001cd12c` | reset_calcmode_think() | 64 | 81.25% | needs_review |
| `001d584c` | get_turn_unit(int) | 64 | 100.0% | auto_structural |
| `001d94b0` | adjust_joblevel(unsigned short*, unsigned char*) | 64 | 100.0% | auto_structural |
| `001e7420` | iOS_AddClearItem() | 64 | 87.5% | needs_review |
| `001eb074` | countCrystalAnimation() | 64 | 93.75% | needs_review |
| `001eb794` | iOSmyGetShapePrim() | 64 | 93.75% | needs_review |
| `0020dad8` | setBackColor(unsigned char, unsigned char, unsigned char) | 64 | 93.75% | needs_review |
| `0020e880` | getFontIDFormBattleWork(int) | 64 | 93.75% | needs_review |
| `0020ef78` | inactivateCompressedAnimation(int) | 64 | 93.75% | needs_review |
| `0021665c` | effectFadeinMusic(int) | 64 | 93.75% | needs_review |
| `0021bd20` | s5_setSequenceID(_EffectTCB*) | 64 | 93.75% | needs_review |
| `0021bd60` | s10_setValue(_EffectTCB*) | 64 | 100.0% | auto_structural |
| `0021bda0` | s11_ifEQU(_EffectTCB*) | 64 | 100.0% | auto_structural |
| `0021bde0` | s12_ifGE(_EffectTCB*) | 64 | 100.0% | auto_structural |
| `0021be20` | s13_ifGT(_EffectTCB*) | 64 | 100.0% | auto_structural |
| `0021be60` | s14_ifLE(_EffectTCB*) | 64 | 100.0% | auto_structural |
| `0021bea0` | s15_ifLT(_EffectTCB*) | 64 | 100.0% | auto_structural |
| `0021c04c` | s1c_ifNotEQU(_EffectTCB*) | 64 | 100.0% | auto_structural |
| `0021c08c` | s1f_ifNumTargetEQU(_EffectTCB*) | 64 | 93.75% | needs_review |
| `0021c644` | s26_createObjectWithTable(_EffectTCB*) | 64 | 100.0% | auto_structural |
| `0021c684` | s27_setEnvironmentWithTable(_EffectTCB*) | 64 | 93.75% | needs_review |
| `0021cbd0` | s1d_ifScheduleEnd(_EffectTCB*) | 64 | 93.75% | needs_review |
| `0024552c` | cdxa_stop() | 64 | 93.75% | needs_review |
| `00249278` | vOpn_init(int) | 64 | 93.75% | needs_review |
| `00249a80` | vOpn_SetCDVolume(int, int) | 64 | 100.0% | auto_structural |
| `00259460` | get_ramza_savework() | 64 | 100.0% | auto_structural |
| `0025ee30` | wldload_wait() | 64 | 93.75% | needs_review |
| `00269b80` | snpl_keywait() | 64 | 81.25% | needs_review |
| `0026a570` | snpl_fadewait() | 64 | 81.25% | needs_review |
| `0026ebf0` | ctlsentuto_active(CTLINFO*) | 64 | 93.75% | needs_review |
| `00273b38` | SetSafePanelAhead(int) | 64 | 93.75% | needs_review |
| `00278440` | GetPanelUnderUnit(int, unsigned char*) | 64 | 93.75% | needs_review |
| `0028b080` | pspWorldCallBackExec() | 64 | 87.5% | needs_review |
| `0028be80` | _ps_test() | 64 | 87.5% | needs_review |
| `002a0aa0` | ApplyRotMatrixLV | 64 | 100.0% | auto_structural |
| `002a3028` | xpFree | 64 | 93.75% | needs_review |
| `002b8888` | iOS_InitMovie(int) | 64 | 87.5% | needs_review |
| `002cab9c` | __extendsfdf2 | 64 | 100.0% | auto_structural |
| `002cde9c` | __gnu_unwind_frame | 64 | 100.0% | auto_structural |
| `0007cd9c` | inflateGetHeader | 60 | 100.0% | auto_structural |
| `0007d914` | call_ztell64 | 60 | 100.0% | auto_structural |
| `0009403c` | _vp_global_look | 60 | 93.33% | needs_review |
| `000a6d60` | CGX_SCREEN_CORRECT::SetEnable(int) | 60 | 100.0% | auto_structural |
| `000ab9cc` | CEGL2_SHADER::CEGL2_SHADER() | 60 | 93.33% | needs_review |
| `000b52a0` | CRECT::SetRect(int, _RECT_S32*) | 60 | 100.0% | auto_structural |
| `000b52dc` | CRECT::SetRect16(int, _RECT_S16*) | 60 | 100.0% | auto_structural |
| `000bcdc4` | CSOUND_LOADER_PCM::Close() | 60 | 100.0% | auto_structural |
| `000bd414` | COggMemMapFile::Close() | 60 | 100.0% | auto_structural |
| `000be0fc` | CSTEP::GetData() | 60 | 100.0% | auto_structural |
| `000d6f18` | initsprtfield(tagSPRT*, int, int) | 60 | 100.0% | auto_structural |
| `000fea3c` | Winitsprtfield(tagSPRT*, int, int) | 60 | 100.0% | auto_structural |
| `00101980` | Wsend_sttslinecol(char*) | 60 | 93.33% | needs_review |
| `001534a4` | send_taskparamater4(long, long, long, long, long) | 60 | 93.33% | needs_review |
| `00153768` | Wsend_taskparamater4(long, long, long, long, long) | 60 | 93.33% | needs_review |
| `00155e04` | changewindowamb(int, int, int) | 60 | 80.0% | needs_review |
| `0015e768` | iOSShiftUnitSet(int) | 60 | 86.67% | needs_review |
| `0016f738` | iOS_cacheFilesNameClear() | 60 | 93.33% | needs_review |
| `001a7368` | IsDismiss(short) | 60 | 93.33% | needs_review |
| `001b6fc4` | GetFontCode(unsigned char*, short, int) | 60 | 100.0% | auto_structural |
| `001b7bf0` | MenuSelVerticalWithSndDirect(unsigned short, unsigned char, int, int) | 60 | 86.67% | needs_review |
| `001c7178` | SelectWindowClutEx(int, int) | 60 | 86.67% | needs_review |
| `001ca97c` | overlayMonomaneStack() | 60 | 93.33% | needs_review |
| `001d3d5c` | get_active_unit() | 60 | 93.33% | needs_review |
| `001d45c4` | check_turn_frozen(BWORK*) | 60 | 100.0% | auto_structural |
| `00202f20` | set_direction_sub(tag_animation*, int) | 60 | 100.0% | auto_structural |
| `00213e0c` | stopColorRotation(unsigned int) | 60 | 93.33% | needs_review |
| `002164f4` | inactivateMusic() | 60 | 93.33% | needs_review |
| `002431b4` | fRoll_fadein(short*) | 60 | 86.67% | needs_review |
| `002431f0` | fRoll_fadeout(short*) | 60 | 86.67% | needs_review |
| `00244938` | numword_chk(int) | 60 | 100.0% | auto_structural |
| `00249bcc` | vOpn_loadwait() | 60 | 93.33% | needs_review |
| `00249c08` | vOpn_CdRead(CDREC*, int, int, unsigned long*) | 60 | 100.0% | auto_structural |
| `0026a3d0` | snpl_wordcol() | 60 | 93.33% | needs_review |
| `0026ab70` | snpl_envsndreq() | 60 | 93.33% | needs_review |
| `002819cc` | iOS_v2menuInit() | 60 | 93.33% | needs_review |
| `00283ed8` | GLIVON_FT4(unsigned long*, tagPOLY_GT4*, short, unsigned long*, unsigned short*) | 60 | 100.0% | auto_structural |
| `00283f14` | GLIVON_FT3(unsigned long*, tagPOLY_GT3*, short, unsigned long*, unsigned short*) | 60 | 100.0% | auto_structural |
| `00284784` | ColorVectorDataBase(unsigned int) | 60 | 93.33% | needs_review |
| `00289844` | pspClearSaveData() | 60 | 93.33% | needs_review |
| `0028af88` | __bpResetBinpackData | 60 | 100.0% | auto_structural |
| `0028afdc` | __bpGetAllBinarySize | 60 | 100.0% | auto_structural |
| `0028b6fc` | STEP_DISP(char const*) | 60 | 93.33% | needs_review |
| `0028bf7c` | _ps_cond() | 60 | 93.33% | needs_review |
| `0029b618` | iOSGsSwapDispBuff() | 60 | 93.33% | needs_review |
| `002ab5cc` | GuEmu_Clear() | 60 | 86.67% | needs_review |
| `002b6fe0` | iOSReleaseButtonAreaCheck() | 60 | 93.33% | needs_review |
| `002ca195` | __cxa_begin_cleanup | 60 | 66.67% | needs_review |
| `000724b0` | _JNIEnv::NewObject(_jclass*, _jmethodID*, ...) | 56 | 100.0% | auto_structural |
| `00072638` | _JNIEnv::CallStaticObjectMethod(_jclass*, _jmethodID*, ...) | 56 | 100.0% | auto_structural |
| `00072670` | _JNIEnv::CallStaticIntMethod(_jclass*, _jmethodID*, ...) | 56 | 100.0% | auto_structural |
| `000726a8` | _JNIEnv::CallStaticVoidMethod(_jclass*, _jmethodID*, ...) | 56 | 100.0% | auto_structural |
| `00075890` | deflateTune | 56 | 100.0% | auto_structural |
| `00082414` | oggpack_writeinit | 56 | 100.0% | auto_structural |
| `000b35ac` | CINPUT_DATA::SetKeyWait(int, int, unsigned int, unsigned int) | 56 | 100.0% | auto_structural |
| `000b6e38` | CFILE_DAT::Decrypt(int, unsigned int) | 56 | 100.0% | auto_structural |
| `000b9f44` | CTHREAD::Sync() | 56 | 100.0% | auto_structural |
| `000bb890` | CSOUND_IF_SL::StopAll() | 56 | 100.0% | auto_structural |
| `000bdae0` | CFRAMERATE::GetRate() | 56 | 100.0% | auto_structural |
| `000d7ed8` | getvaluelength(int) | 56 | 92.86% | needs_review |
| `000d86d8` | getanimpos3d(int, short*) | 56 | 100.0% | auto_structural |
| `000d8740` | checkstatusscroll(int) | 56 | 100.0% | auto_structural |
| `000d88c4` | popmessagepacket() | 56 | 85.71% | needs_review |
| `000e0f68` | loadcsrc(int, int, int, int) | 56 | 92.86% | needs_review |
| `000e8010` | iOS_clearFLAGeventdirect() | 56 | 100.0% | auto_structural |
| `000e8048` | iOS_clearFLAGmonsentry() | 56 | 100.0% | auto_structural |
| `000ffac4` | Wgetvaluelength(int) | 56 | 92.86% | needs_review |
| `001003ac` | Wgetanimpos3d(int, short*) | 56 | 100.0% | auto_structural |
| `00100414` | Wcheckstatusscroll(int) | 56 | 100.0% | auto_structural |
| `00100594` | Wpopmessagepacket() | 56 | 85.71% | needs_review |
| `001534e0` | taskActiveCheck() | 56 | 100.0% | auto_structural |
| `001537a4` | WtaskActiveCheck() | 56 | 100.0% | auto_structural |
| `0019f718` | iOSShopHelpStatusCheck() | 56 | 92.86% | needs_review |
| `001c03a8` | DrawSingleUnit(short) | 56 | 100.0% | auto_structural |
| `001cec24` | copy_target_table2(unsigned char*) | 56 | 92.86% | needs_review |
| `001ceca0` | _rand_() | 56 | 85.71% | needs_review |
| `001d1ce8` | erase_unit_f(int) | 56 | 92.86% | needs_review |
| `001d3d24` | gc_bwp(int) | 56 | 92.86% | needs_review |
| `001f5f44` | iOS_resetAnimationIrowake() | 56 | 92.86% | needs_review |
| `00200b80` | endTrunAction() | 56 | 92.86% | needs_review |
| `0020c114` | iOS_GaryutenseiCheck() | 56 | 100.0% | auto_structural |
| `0020e8dc` | checkCharacterMove(int) | 56 | 100.0% | auto_structural |
| `0021b0d0` | InitEffectLoadAddress() | 56 | 85.71% | needs_review |
| `0021b4a8` | GetSQLFrameRate(_EffectTCB*) | 56 | 92.86% | needs_review |
| `0021bfdc` | s1a_ifChildTaskExist(_EffectTCB*) | 56 | 100.0% | auto_structural |
| `0021c014` | s1b_ifChildTaskNonExist(_EffectTCB*) | 56 | 100.0% | auto_structural |
| `0021ce78` | IsPermanentEffect(long) | 56 | 92.86% | needs_review |
| `00254170` | iOSMapNaviCurSet(unsigned long) | 56 | 100.0% | auto_structural |
| `00258c40` | evt_wldinfo() | 56 | 92.86% | needs_review |
| `0025ee70` | wldCdRead(CDREC*, int, int, int, unsigned long*) | 56 | 100.0% | auto_structural |
| `00269a68` | snpl_hidepara() | 56 | 85.71% | needs_review |
| `00269cd0` | snpl_setstat() | 56 | 85.71% | needs_review |
| `00269d08` | snpl_clrstat() | 56 | 85.71% | needs_review |
| `00269d40` | snpl_setlocal() | 56 | 85.71% | needs_review |
| `00269d78` | snpl_clrlocal() | 56 | 85.71% | needs_review |
| `0026a824` | snpl_snsndreq() | 56 | 92.86% | needs_review |
| `00279c88` | MemClearDW(int*, int) | 56 | 100.0% | auto_structural |
| `0027b4a4` | initCmdKind() | 56 | 85.71% | needs_review |
| `0027fc80` | cSaveFFT::Destroy() | 56 | 92.86% | needs_review |
| `00280558` | iOS_fftLoad(int) | 56 | 85.71% | needs_review |
| `00285f4c` | pspFileManager::hockSeek(int) | 56 | 100.0% | auto_structural |
| `00287a40` | load_hight_font() | 56 | 100.0% | auto_structural |
| `0028c288` | CFFT_STATE::GetBackdropColor(float*, float*, float*) | 56 | 57.14% | needs_review |
| `0028c5d4` | CFFT_STATE::Suspend(_FFT_STATE_RESUME*) | 56 | 100.0% | auto_structural |
| `0028c60c` | CFFT_STATE::Resume(_FFT_STATE_RESUME*) | 56 | 100.0% | auto_structural |
| `0028da58` | tlDumpHeap() | 56 | 92.86% | needs_review |
| `0028daac` | tlGetHeapSize() | 56 | 92.86% | needs_review |
| `002918b4` | SetDrawStp | 56 | 100.0% | auto_structural |
| `0029aa84` | OpenTIM | 56 | 85.71% | needs_review |
| `0029ff5c` | PSX_csqrt | 56 | 100.0% | auto_structural |
| `002a1594` | DpqColor3 | 56 | 100.0% | auto_structural |
| `002a2f60` | PCopen | 56 | 92.86% | needs_review |
| `002b88c8` | iOS_StartMovie() | 56 | 85.71% | needs_review |
| `002bf32c` | Debug_SetDebugDirectBtn(int) | 56 | 92.86% | needs_review |
| `00075760` | deflateSetHeader | 52 | 100.0% | auto_structural |
| `000771cc` | deflateInit_ | 52 | 100.0% | auto_structural |
| `00081abc` | unzeof | 52 | 100.0% | auto_structural |
| `000b8a20` | CLIST::GetData(int) | 52 | 100.0% | auto_structural |
| `000ba230` | CSOUND_IF::CSOUND_IF(int) | 52 | 100.0% | auto_structural |
| `000bd538` | CSOUND_LOADER_OGG::CSOUND_LOADER_OGG() | 52 | 92.31% | needs_review |
| `000e7488` | getCodeLength(unsigned char*) | 52 | 92.31% | needs_review |
| `0012f2a8` | iOSPersonalWinPos(int) | 52 | 84.62% | needs_review |
| `00153470` | send_taskparamater(long, long, long, long) | 52 | 92.31% | needs_review |
| `00153734` | Wsend_taskparamater(long, long, long, long) | 52 | 92.31% | needs_review |
| `00159a78` | asmSerchMessagePointer(char*, int) | 52 | 100.0% | auto_structural |
| `00161e2c` | iOSIsCurMode() | 52 | 92.31% | needs_review |
| `0016204c` | wasmSerchMessagePointer(char*, int) | 52 | 100.0% | auto_structural |
| `001a63dc` | bak_read(int, void*) | 52 | 92.31% | needs_review |
| `001cb030` | clear_setstatus(A_RESULT*) | 52 | 92.31% | needs_review |
| `001cb844` | check_reaction_deny_all(BWORK*) | 52 | 100.0% | auto_structural |
| `001d9370` | get_joblevel(unsigned short) | 52 | 92.31% | needs_review |
| `001eb760` | myStartShape() | 52 | 84.62% | needs_review |
| `001f36c8` | EndAllAnimation() | 52 | 92.31% | needs_review |
| `001fd278` | startInterventionMode() | 52 | 84.62% | needs_review |
| `0020d7d4` | pushMapAngle() | 52 | 84.62% | needs_review |
| `0020d808` | popMapAngle() | 52 | 84.62% | needs_review |
| `0020da48` | pushBackColor() | 52 | 84.62% | needs_review |
| `0020dd44` | getUnitRelativeDirection(unsigned int) | 52 | 100.0% | auto_structural |
| `0020eddc` | inactivateEventAnimation(int) | 52 | 92.31% | needs_review |
| `0020f574` | getMapXYZ(SVECTOR*) | 52 | 76.92% | needs_review |
| `002119c0` | PushChangePalette() | 52 | 84.62% | needs_review |
| `002119f4` | PopChangePalette() | 52 | 84.62% | needs_review |
| `0021b474` | GetMSQFrameRate(_EffectTCB*) | 52 | 92.31% | needs_review |
| `00228e64` | startShape() | 52 | 92.31% | needs_review |
| `00243014` | fRoll_exit(short*) | 52 | 92.31% | needs_review |
| `00245a74` | o_ClearCardEvent() | 52 | 92.31% | needs_review |
| `00245b34` | o_ClearCardEvent_X() | 52 | 92.31% | needs_review |
| `0024a498` | iOS_vOpn_touchNum_addprim(iOS_CMenuTouchNum*, unsigned long*, int) | 52 | 100.0% | auto_structural |
| `0024dc8c` | ctlkiroku_active(CTLINFO*) | 52 | 92.31% | needs_review |
| `0024e8d0` | ctlperson_active(CTLINFO*) | 52 | 92.31% | needs_review |
| `00258e08` | evt_town_set() | 52 | 92.31% | needs_review |
| `00258e3c` | evt_town_clr() | 52 | 92.31% | needs_review |
| `00259e70` | ctlhouk_active(CTLINFO*) | 52 | 92.31% | needs_review |
| `002602c0` | ctlmouke_active(CTLINFO*) | 52 | 92.31% | needs_review |
| `00266efc` | pspGetWarFundsOfs(short*, short*) | 52 | 100.0% | auto_structural |
| `002675c0` | ctlret_active(CTLINFO*) | 52 | 92.31% | needs_review |
| `0026c3cc` | ctltresure_active(CTLINFO*) | 52 | 92.31% | needs_review |
| `0027b4dc` | setCmdKind(unsigned int) | 52 | 84.62% | needs_review |
| `0027f14c` | iOS_ClearRectHitAll() | 52 | 92.31% | needs_review |
| `00284714` | CalcVectorFromID(VECTOR_DATABASE*, short) | 52 | 100.0% | auto_structural |
| `0028af54` | __bpInitBinpackData | 52 | 100.0% | auto_structural |
| `00291710` | SetDrawOffset | 52 | 100.0% | auto_structural |
| `002a0844` | ReadRotMatrix | 52 | 92.31% | needs_review |
| `002a0cdc` | ApplyTransposeMatrixLV | 52 | 100.0% | auto_structural |
| `002a11d0` | SquareSS0 | 52 | 100.0% | auto_structural |
| `002a14d8` | ColorDpq | 52 | 100.0% | auto_structural |
| `002a15cc` | DpqColorLight | 52 | 100.0% | auto_structural |
| `002a242c` | RotColorDpq_nom | 52 | 92.31% | needs_review |
| `002ae88c` | GuEmu_GetCLUTAddress(unsigned short, int*, int*) | 52 | 100.0% | auto_structural |
| `002c5400` | Movie_FrameMove() | 52 | 92.31% | needs_review |
| `00079178` | gzprintf | 48 | 100.0% | auto_structural |
| `0007afb8` | inflateReset | 48 | 100.0% | auto_structural |
| `0007d0c4` | inflateUndermine | 48 | 100.0% | auto_structural |
| `00082cac` | oggpack_adv1 | 48 | 100.0% | auto_structural |
| `000b3694` | CINPUT_DATA::Clear(int) | 48 | 100.0% | auto_structural |
| `000b6a28` | CFILE_DAT::Unload() | 48 | 100.0% | auto_structural |
| `000b9d5c` | CWORK_MEM::Delete(int) | 48 | 100.0% | auto_structural |
| `000b9da4` | CWORK_MEM::New(int) | 48 | 100.0% | auto_structural |
| `000bd968` | CFRAMERATE::Clear() | 48 | 100.0% | auto_structural |
| `000da47c` | event_init_system() | 48 | 91.67% | needs_review |
| `000da6d0` | geteventcategory() | 48 | 83.33% | needs_review |
| `000e0538` | import_localpad(int) | 48 | 83.33% | needs_review |
| `001020f8` | Wevent_init_system() | 48 | 91.67% | needs_review |
| `0010229c` | Wgeteventcategory() | 48 | 83.33% | needs_review |
| `00153420` | wait_taskend(long) | 48 | 91.67% | needs_review |
| `001536e4` | Wwait_taskend(long) | 48 | 91.67% | needs_review |
| `0015e068` | iOSNumberGet(int) | 48 | 91.67% | needs_review |
| `001d1db8` | leave_unit_f(int) | 48 | 91.67% | needs_review |
| `001d1f48` | check_move_ability(BWORK*) | 48 | 100.0% | auto_structural |
| `001d2e6c` | get_coord_address(BWORK*) | 48 | 91.67% | needs_review |
| `001d9548` | check_prob(int, int) | 48 | 100.0% | auto_structural |
| `001dc914` | set_cco_SD(BWORK*) | 48 | 91.67% | needs_review |
| `001e4f0c` | get_fusui_ability(BWORK*) | 48 | 83.33% | needs_review |
| `001eedf4` | getWpnSequenceAddress(unsigned short) | 48 | 83.33% | needs_review |
| `001f1650` | setMovingAnimationShape() | 48 | 100.0% | auto_structural |
| `00202150` | standerdExecution() | 48 | 91.67% | needs_review |
| `00204268` | startLeftTurn(int) | 48 | 91.67% | needs_review |
| `00204298` | startRightTurn(int) | 48 | 91.67% | needs_review |
| `0020e560` | getOffsetAnimationPosition(int) | 48 | 100.0% | auto_structural |
| `00213e48` | stopAllColorRotation() | 48 | 91.67% | needs_review |
| `00215d2c` | battleFileRead() | 48 | 83.33% | needs_review |
| `0021b860` | SetGravity(Vector*) | 48 | 91.67% | needs_review |
| `0021bee0` | s16_ifObjNumEQU(_EffectTCB*) | 48 | 100.0% | auto_structural |
| `0021bf10` | s17_ifObjNumGT(_EffectTCB*) | 48 | 100.0% | auto_structural |
| `0021bf40` | s18_ifObjNumLT(_EffectTCB*) | 48 | 100.0% | auto_structural |
| `0021d23c` | initScheduleControl(_EffectTCB*, short) | 48 | 100.0% | auto_structural |
| `0021d290` | initMetascheduleControl(_EffectTCB*) | 48 | 100.0% | auto_structural |
| `0022a92c` | GetAnimationPositionFromBattleID(int, int, EffectOrder*, SVECTOR*) | 48 | 100.0% | auto_structural |
| `00243184` | fRoll_scroll(short*) | 48 | 91.67% | needs_review |
| `0024337c` | fRoll_cdxafin(short*) | 48 | 91.67% | needs_review |
| `002433ac` | fRoll_cdxafout(short*) | 48 | 91.67% | needs_review |
| `0024932c` | vOpn_loopinit() | 48 | 83.33% | needs_review |
| `00249cc4` | vEnd_CdReady_Chk() | 48 | 100.0% | auto_structural |
| `0024ad94` | openEntry(int) | 48 | 91.67% | needs_review |
| `0025f138` | townpic_load(int) | 48 | 91.67% | needs_review |
| `0025ffb0` | iOSSDNovelGetOT(int) | 48 | 83.33% | needs_review |
| `0026995c` | snpl_addpara() | 48 | 91.67% | needs_review |
| `0026998c` | snpl_subpara() | 48 | 91.67% | needs_review |
| `00269e98` | snpl_exit() | 48 | 91.67% | needs_review |
| `00270460` | curhis_get(int) | 48 | 83.33% | needs_review |
| `00271e1c` | GetDistance(BWORK*, BWORK*) | 48 | 100.0% | auto_structural |
| `00279c34` | MemCpyW(unsigned short*, unsigned short const*, int) | 48 | 100.0% | auto_structural |
| `0027fc48` | cSaveFFT::Create(char*) | 48 | 91.67% | needs_review |
| `00283f50` | GLIVON_F3(unsigned long*, tagPOLY_F3*, short, unsigned long*) | 48 | 100.0% | auto_structural |
| `00283f80` | GLIVON_F4(unsigned long*, tagPOLY_F4*, short, unsigned long*) | 48 | 100.0% | auto_structural |
| `00289970` | pspIsNoneSaveData(int) | 48 | 91.67% | needs_review |
| `0028ba54` | TE_task_create(int, void (*)(), int) | 48 | 91.67% | needs_review |
| `0028bf4c` | _ps_wait() | 48 | 100.0% | auto_structural |
| `0028e538` | CdRead | 48 | 91.67% | needs_review |
| `0028e6a4` | xpInitVblankFunc() | 48 | 83.33% | needs_review |
| `0029138c` | GetClut | 48 | 100.0% | auto_structural |
| `0029c8e8` | xpLibgsAddOt | 48 | 100.0% | auto_structural |
| `002a12c4` | AverageZ3 | 48 | 100.0% | auto_structural |
| `002a12f4` | AverageZ4 | 48 | 100.0% | auto_structural |
| `002a145c` | ReadLightMatrix | 48 | 91.67% | needs_review |
| `002a14a8` | ReadColorMatrix | 48 | 91.67% | needs_review |
| `002a2ff8` | xpInitHeap | 48 | 91.67% | needs_review |
| `002a38a8` | pspSaveList::pspSaveList() | 48 | 91.67% | needs_review |
| `002b2260` | RETINA_SCALE(int) | 48 | 91.67% | needs_review |
| `002b2378` | Music_Stop() | 48 | 91.67% | needs_review |
| `002b23a8` | Music_Pause() | 48 | 91.67% | needs_review |
| `002b8348` | Main_IsTitle() | 48 | 100.0% | auto_structural |
| `002cb158` | __aeabi_cdrcmple | 48 | 100.0% | auto_structural |
| `000773d4` | gzclose | 44 | 100.0% | auto_structural |
| `0008254c` | oggpack_writeclear | 44 | 100.0% | auto_structural |
| `00082a18` | oggpack_readinit | 44 | 100.0% | auto_structural |
| `00082c0c` | oggpackB_look1 | 44 | 100.0% | auto_structural |
| `000960c4` | res0_free_info | 44 | 100.0% | auto_structural |
| `000aba20` | CEGL2_SHADER::SetMatrix4(int, math::MATRIX4 const&) | 44 | 100.0% | auto_structural |
| `000b3728` | CINPUT_DATA::GetPress(int, int) | 44 | 100.0% | auto_structural |
| `000b3754` | CINPUT_DATA::GetDown(int, int) | 44 | 100.0% | auto_structural |
| `000b384c` | CINPUT_DATA::GetRepeat(int, int) | 44 | 100.0% | auto_structural |
| `000bba9c` | CSOUND_IF_SL::GetPlaySample(int) | 44 | 100.0% | auto_structural |
| `000d6f54` | allocatewindowinit() | 44 | 90.91% | needs_review |
| `000d86ac` | getanimpos2d(int, SVECTOR*) | 44 | 100.0% | auto_structural |
| `000d9810` | hook_disp_option() | 44 | 90.91% | needs_review |
| `000da610` | set_autobattletarget(int, int) | 44 | 90.91% | needs_review |
| `000f1484` | disp_okng() | 44 | 100.0% | auto_structural |
| `000f14b0` | disp_yesno() | 44 | 100.0% | auto_structural |
| `000f14dc` | disp_attackng() | 44 | 100.0% | auto_structural |
| `000f1508` | disp_coverng() | 44 | 100.0% | auto_structural |
| `000f1534` | disp_executeng() | 44 | 100.0% | auto_structural |
| `000f1604` | disp_dismiss_yesno() | 44 | 100.0% | auto_structural |
| `000f1630` | disp_yameru_yesno() | 44 | 100.0% | auto_structural |
| `000f586c` | attackteam_call(unsigned long*, unsigned long) | 44 | 100.0% | auto_structural |
| `000fea78` | Wallocatewindowinit() | 44 | 90.91% | needs_review |
| `00100380` | Wgetanimpos2d(int, SVECTOR*) | 44 | 100.0% | auto_structural |
| `00101624` | Whook_disp_option() | 44 | 90.91% | needs_review |
| `001021dc` | Wset_autobattletarget(int, int) | 44 | 90.91% | needs_review |
| `00106270` | Wdisp_okng() | 44 | 100.0% | auto_structural |
| `0010629c` | Wdisp_yesno() | 44 | 100.0% | auto_structural |
| `001062c8` | Wdisp_attackng() | 44 | 100.0% | auto_structural |
| `001062f4` | Wdisp_coverng() | 44 | 100.0% | auto_structural |
| `00106320` | Wdisp_executeng() | 44 | 100.0% | auto_structural |
| `001063f0` | Wdisp_dismiss_yesno() | 44 | 100.0% | auto_structural |
| `0010641c` | Wdisp_yameru_yesno() | 44 | 100.0% | auto_structural |
| `001599d0` | asmGetInput2() | 44 | 81.82% | needs_review |
| `001599fc` | asmGetInput3() | 44 | 81.82% | needs_review |
| `00159a28` | asmGetActiveF() | 44 | 81.82% | needs_review |
| `0015da34` | iOSCurSameProcs(ActionRequest*) | 44 | 100.0% | auto_structural |
| `0015df10` | iOSGT4_MapT9Get(unsigned long) | 44 | 90.91% | needs_review |
| `001cb878` | bcp_roll(BWORK*) | 44 | 90.91% | needs_review |
| `001d1d8c` | disappare_unit_f(int) | 44 | 90.91% | needs_review |
| `001d2968` | get_bwp(int) | 44 | 90.91% | needs_review |
| `001d6404` | set_guard_status(int) | 44 | 90.91% | needs_review |
| `001d94f0` | get_rangedata(unsigned short) | 44 | 90.91% | needs_review |
| `001d951c` | get_effectdata(unsigned short) | 44 | 90.91% | needs_review |
| `0020e914` | eventWeaponEquip(int, int) | 44 | 100.0% | auto_structural |
| `0020f7c8` | setCurrentPanel(int) | 44 | 100.0% | auto_structural |
| `0020f874` | eventWarpEffect(int) | 44 | 100.0% | auto_structural |
| `0021b8c4` | PopGravity() | 44 | 90.91% | needs_review |
| `0021ceb0` | WhoUnlockEffect(long) | 44 | 90.91% | needs_review |
| `00243560` | fRoll_xawait(short*) | 44 | 90.91% | needs_review |
| `00249474` | vOpn_fadein(int) | 44 | 90.91% | needs_review |
| `00256e70` | ctltownmenu_active(CTLINFO*) | 44 | 90.91% | needs_review |
| `00256e9c` | ctltownmenu_deactive(CTLINFO*) | 44 | 90.91% | needs_review |
| `0025d7f0` | wldfrm_rect(int, RECT16*) | 44 | 100.0% | auto_structural |
| `00269930` | snpl_setpara() | 44 | 90.91% | needs_review |
| `00269e6c` | snpl_sndstop() | 44 | 90.91% | needs_review |
| `0027134c` | Ssd_StopEffect(long) | 44 | 100.0% | auto_structural |
| `0027334c` | SetDestUnit(int) | 44 | 90.91% | needs_review |
| `0027b53c` | LoadImage_menuData() | 44 | 90.91% | needs_review |
| `0027f180` | iOS_ClearRectHit(int) | 44 | 90.91% | needs_review |
| `00280590` | GetAbilityName(int) | 44 | 81.82% | needs_review |
| `00284620` | new_VectorXYZ(VECTOR_DATABASE*, short, short, short) | 44 | 100.0% | auto_structural |
| `00287044` | get_timing_true() | 44 | 90.91% | needs_review |
| `0028846c` | free_hight_font() | 44 | 90.91% | needs_review |
| `0028a054` | pspClearCurrentSystemFile() | 44 | 90.91% | needs_review |
| `0028baa4` | TE_task_stop(long) | 44 | 90.91% | needs_review |
| `002a0900` | MulRotMatrix0 | 44 | 90.91% | needs_review |
| `002a096c` | ApplyMatrix | 44 | 100.0% | auto_structural |
| `002a0a54` | ApplyMatrixSV | 44 | 100.0% | auto_structural |
| `002a1148` | SquareSL0 | 44 | 100.0% | auto_structural |
| `002a2620` | RotTrans | 44 | 100.0% | auto_structural |
| `002a264c` | RotTransSV | 44 | 100.0% | auto_structural |
| `002b23d8` | Music_Replay() | 44 | 90.91% | needs_review |
| `002bef74` | PIE_OFFSET(unsigned int) | 44 | 100.0% | auto_structural |
| `00081a94` | unztell64 | 40 | 100.0% | auto_structural |
| `00082450` | oggpack_writecheck | 40 | 100.0% | auto_structural |
| `00082520` | oggpack_reset | 40 | 100.0% | auto_structural |
| `000829c4` | oggpack_writecopy | 40 | 90.0% | needs_review |
| `000829ec` | oggpackB_writecopy | 40 | 90.0% | needs_review |
| `00082be4` | oggpack_look1 | 40 | 100.0% | auto_structural |
| `00094078` | _vp_global_free | 40 | 100.0% | auto_structural |
| `000940a0` | _vi_gpsy_free | 40 | 100.0% | auto_structural |
| `000940c8` | _vi_psy_free | 40 | 100.0% | auto_structural |
| `000a85fc` | CEGL2_IF::Term() | 40 | 100.0% | auto_structural |
| `000b1880` | CEGL_PACKET::CEGL_PACKET() | 40 | 100.0% | auto_structural |
| `000b364c` | CINPUT_DATA::SetKeyDelay(int, int, unsigned int) | 40 | 100.0% | auto_structural |
| `000b45f4` | CINPUT_IF_TOUCH::GetData(int) | 40 | 100.0% | auto_structural |
| `000b50c0` | CRECT::Init() | 40 | 100.0% | auto_structural |
| `000bceac` | CSOUND_LOADER_PCM::CSOUND_LOADER_PCM() | 40 | 90.0% | needs_review |
| `000bd378` | CSOUND_LOADER_OGG::Tell() const | 40 | 100.0% | auto_structural |
| `000be1b4` | CSTEP_BATCH::CSTEP_BATCH() | 40 | 100.0% | auto_structural |
| `000daac0` | settaskkind(int) | 40 | 80.0% | needs_review |
| `000e0eec` | jobstts_call(unsigned long*, unsigned long) | 40 | 90.0% | needs_review |
| `001024bc` | Wreaded_mapchange() | 40 | 90.0% | needs_review |
| `0010278c` | Wsettaskkind(int) | 40 | 80.0% | needs_review |
| `0010de7c` | Wimport_localpad(int) | 40 | 80.0% | needs_review |
| `0010f8cc` | Wjobstts_call(unsigned long*, unsigned long) | 40 | 90.0% | needs_review |
| `0012f19c` | get_pitno() | 40 | 90.0% | needs_review |
| `00155cec` | tutorialstatusget(int) | 40 | 90.0% | needs_review |
| `001599a8` | asmGetInput1() | 40 | 80.0% | needs_review |
| `0015e040` | iOSActUnitCurSet() | 40 | 90.0% | needs_review |
| `0015ebf4` | iOSMapTouchCancel() | 40 | 80.0% | needs_review |
| `001875f0` | GetSaveDataInit() | 40 | 90.0% | needs_review |
| `001a3eb4` | PoachUnit() | 40 | 90.0% | needs_review |
| `001baea0` | unitans_init() | 40 | 90.0% | needs_review |
| `001ca954` | net_getknockback(unsigned char*, unsigned char*, unsigned char*) | 40 | 90.0% | needs_review |
| `001cb7d4` | check_reaction_deny(BWORK*) | 40 | 90.0% | needs_review |
| `001ceaec` | set_status_all_sp(int, int) | 40 | 90.0% | needs_review |
| `001cebfc` | set_target_table2(unsigned char*) | 40 | 90.0% | needs_review |
| `001d73ec` | clear_unitwork() | 40 | 90.0% | needs_review |
| `001d8d28` | get_jobdata(int) | 40 | 90.0% | needs_review |
| `001dbcc4` | unitwork_init2all(BWORK*, int) | 40 | 100.0% | auto_structural |
| `001dc44c` | adjust_entry_status(BWORK*) | 40 | 100.0% | auto_structural |
| `001eedcc` | getWpnShapeAddress(unsigned short) | 40 | 80.0% | needs_review |
| `001f6374` | setPositionToLongPosition(tag_animation*) | 40 | 100.0% | auto_structural |
| `001fd2c4` | endInterventionMode() | 40 | 80.0% | needs_review |
| `0020c5d8` | errorHandler(int) | 40 | 90.0% | needs_review |
| `0020c600` | warningHandler(int) | 40 | 90.0% | needs_review |
| `0020c74c` | initSoundHeap() | 40 | 90.0% | needs_review |
| `0020c99c` | initFileBuffer() | 40 | 90.0% | needs_review |
| `0020d060` | setMapScrollXYZ(VECTOR*) | 40 | 90.0% | needs_review |
| `0020d2b8` | setMapScroll(VECTOR*) | 40 | 90.0% | needs_review |
| `0020d5d8` | setMapScale(VECTOR*) | 40 | 90.0% | needs_review |
| `0020d84c` | setMapAngle(SVECTOR*) | 40 | 90.0% | needs_review |
| `0020f5a8` | getMapSize(SVECTOR*) | 40 | 80.0% | needs_review |
| `0020f5d0` | getMapIDFromAnimationID(int) | 40 | 100.0% | auto_structural |
| `0020f5f8` | getMapIDFromBattleID(int) | 40 | 100.0% | auto_structural |
| `0021695c` | stopAllEffect() | 40 | 90.0% | needs_review |
| `00218dcc` | InitCamera() | 40 | 90.0% | needs_review |
| `002231b0` | GetReachableHeight(int) | 40 | 90.0% | needs_review |
| `0022a994` | EqualRShift12VECTORToVECTOR(VECTOR*, VECTOR*) | 40 | 100.0% | auto_structural |
| `0022a9bc` | EqualLShift12VECTORToVECTOR(VECTOR*, VECTOR*) | 40 | 100.0% | auto_structural |
| `0022a9e4` | EqualAnd0xfffSVECTORToSVECTOR(SVECTOR*, SVECTOR*) | 40 | 100.0% | auto_structural |
| `00246360` | ctlstartmov_main(CTLINFO*) | 40 | 90.0% | needs_review |
| `002494a0` | vOpn_fadeout(int) | 40 | 90.0% | needs_review |
| `0024adc4` | endEntry() | 40 | 90.0% | needs_review |
| `002592fc` | evt_flagset() | 40 | 100.0% | auto_structural |
| `0025bc50` | jobnumber_conv(int) | 40 | 100.0% | auto_structural |
| `00267340` | iOS_add_anmpac_max(int) | 40 | 90.0% | needs_review |
| `0026a1a4` | snpl_sndreq() | 40 | 90.0% | needs_review |
| `0026a64c` | snplinf_init(int) | 40 | 80.0% | needs_review |
| `0026b0b8` | snpl_musicreq() | 40 | 90.0% | needs_review |
| `0027383c` | ClearMove(MOVE*) | 40 | 100.0% | auto_structural |
| `00273b10` | SetSafePanelInRange(int) | 40 | 100.0% | auto_structural |
| `0027fbc8` | iOS_WorldMapResumeGetData(unsigned char**, unsigned int*) | 40 | 90.0% | needs_review |
| `002808b8` | iOS_initTransFace() | 40 | 90.0% | needs_review |
| `0028b3f0` | pspWorldDataRectSet(RECT16*) | 40 | 90.0% | needs_review |
| `0028c668` | CFFT_STATE::UnitIDToFID_SPR(int) | 40 | 90.0% | needs_review |
| `0028dc30` | SetRCnt | 40 | 90.0% | needs_review |
| `0028e66c` | PadInit | 40 | 100.0% | auto_structural |
| `00291428` | SetPolyFT4 | 40 | 100.0% | auto_structural |
| `0029ff34` | cln | 40 | 100.0% | auto_structural |
| `002a081c` | SetMulMatrix | 40 | 100.0% | auto_structural |
| `002a092c` | SetMulRotMatrix | 40 | 100.0% | auto_structural |
| `002a13c8` | Intpl | 40 | 100.0% | auto_structural |
| `002a150c` | ColorCol | 40 | 100.0% | auto_structural |
| `002a156c` | DpqColor | 40 | 100.0% | auto_structural |
| `002a1aac` | read_sxsy_fifo3(long*, long*, long*) | 40 | 90.0% | needs_review |
| `002a1b1c` | read_rgb_fifo(long*, long*, long*) | 40 | 90.0% | needs_review |
| `002a25f8` | read_mt(long*, long*, long*) | 40 | 90.0% | needs_review |
| `002a2b5c` | xpLibSN::Init() | 40 | 100.0% | auto_structural |
| `002b2238` | IS_TEX_2X() | 40 | 90.0% | needs_review |
| `002b2404` | Music_SetVol(int, int) | 40 | 90.0% | needs_review |
| `002b7a34` | SetDisableMapTouchRect(RECT16*) | 40 | 90.0% | needs_review |
| `002cab74` | __floatsidf | 40 | 100.0% | auto_structural |
| `002cb484` | __floatunsisf | 40 | 80.0% | needs_review |
| `00077500` | gzeof | 36 | 100.0% | auto_structural |
| `00081a70` | unztell | 36 | 100.0% | auto_structural |
| `000aa8d4` | CEGL2_FBO::CEGL2_FBO() | 36 | 100.0% | auto_structural |
| `000b8be4` | CSTR_UTIL::IsLeadByte(unsigned char) | 36 | 100.0% | auto_structural |
| `000b9f88` | CTHREAD::~CTHREAD() | 36 | 100.0% | auto_structural |
| `000bd194` | CSOUND_LOADER_OGG::GetTotalDecoded() const | 36 | 100.0% | auto_structural |
| `000d8710` | getanimpos3dl(int, long*) | 36 | 100.0% | auto_structural |
| `000da7e4` | readed_mapchange() | 36 | 88.89% | needs_review |
| `000dfa70` | wait_anmend(int) | 36 | 100.0% | auto_structural |
| `001003e4` | Wgetanimpos3dl(int, long*) | 36 | 100.0% | auto_structural |
| `00108e28` | Wwait_anmend(int) | 36 | 100.0% | auto_structural |
| `0010f99c` | WiOS_touchNum_addlocalprim2(iOS_CMenuTouchNum*) | 36 | 100.0% | auto_structural |
| `0011dd64` | extend_windowframe(int, int, RECT16*, int, int) | 36 | 100.0% | auto_structural |
| `0011e668` | Wextend_windowframe(int, int, RECT16*, int, int) | 36 | 100.0% | auto_structural |
| `00153254` | task_wait(long) | 36 | 100.0% | auto_structural |
| `00153350` | task_start(long) | 36 | 88.89% | needs_review |
| `00153374` | task_stop(long) | 36 | 88.89% | needs_review |
| `00153518` | Wtask_wait(long) | 36 | 100.0% | auto_structural |
| `00153614` | Wtask_start(long) | 36 | 88.89% | needs_review |
| `00153638` | Wtask_stop(long) | 36 | 88.89% | needs_review |
| `0015391c` | check_eventtool(int, int) | 36 | 88.89% | needs_review |
| `0015b664` | iOSTchInputCheck() | 36 | 100.0% | auto_structural |
| `0015deec` | iOSGT4_MapT9(unsigned long, long) | 36 | 88.89% | needs_review |
| `00161d50` | iOSPosW(int) | 36 | 88.89% | needs_review |
| `00161d74` | iOSPosH(int) | 36 | 88.89% | needs_review |
| `0018e334` | equans_init() | 36 | 88.89% | needs_review |
| `001baac4` | event_warning(short, int) | 36 | 88.89% | needs_review |
| `001ca580` | get_net_rival_weapon_range() | 36 | 88.89% | needs_review |
| `001ccc18` | get_trap_no(BWORK*) | 36 | 100.0% | auto_structural |
| `001eb2d8` | vramDeleteUsed() | 36 | 88.89% | needs_review |
| `001f4a64` | initEntryEnemyAnimations(int) | 36 | 88.89% | needs_review |
| `001f5be4` | terminateAnimation(int) | 36 | 100.0% | auto_structural |
| `001fd1dc` | nextTurnOrder() | 36 | 88.89% | needs_review |
| `0020d008` | pushMapScrollXYZ() | 36 | 77.78% | needs_review |
| `0020d02c` | popMapScrollXYZ() | 36 | 77.78% | needs_review |
| `0020d260` | pushMapScroll() | 36 | 77.78% | needs_review |
| `0020d284` | popMapScroll() | 36 | 77.78% | needs_review |
| `0020d580` | pushMapScale() | 36 | 77.78% | needs_review |
| `0020d5a4` | popMapScale() | 36 | 77.78% | needs_review |
| `0020f514` | stopAnimation() | 36 | 88.89% | needs_review |
| `00215c98` | fadeMapClut(int, unsigned short*) | 36 | 100.0% | auto_structural |
| `00216860` | stopMusic() | 36 | 88.89% | needs_review |
| `0021b220` | SetEditANMPtr() | 36 | 77.78% | needs_review |
| `0021b244` | SetEditTSQPtr() | 36 | 77.78% | needs_review |
| `0021d26c` | s2a_initScheduleControl(_EffectTCB*) | 36 | 100.0% | auto_structural |
| `0021eb8c` | DoEffect() | 36 | 100.0% | auto_structural |
| `00263fa8` | iOSSDNovelSysCurCheck() | 36 | 88.89% | needs_review |
| `00269774` | snpl_jp() | 36 | 88.89% | needs_review |
| `00269b08` | snpl_effmode() | 36 | 88.89% | needs_review |
| `0026c238` | iOSNovelModeBackup() | 36 | 88.89% | needs_review |
| `00279c64` | MemCpyB(unsigned char*, unsigned char const*, int) | 36 | 100.0% | auto_structural |
| `0027fbf0` | iOS_WorldMapResumeGetData2(unsigned char**, unsigned int*) | 36 | 88.89% | needs_review |
| `002806cc` | iOS_HookAddPrim() | 36 | 88.89% | needs_review |
| `00281a08` | iOS_v2menuCheckSEError() | 36 | 100.0% | auto_structural |
| `00284494` | Clear_VectorDataBase() | 36 | 88.89% | needs_review |
| `00285e1c` | pspJobIsSpecialJob(int) | 36 | 100.0% | auto_structural |
| `0028bad0` | TE_is_task_end(long) | 36 | 88.89% | needs_review |
| `0028c644` | CFFT_STATE::FaceIDToFID(int) | 36 | 88.89% | needs_review |
| `0028d228` | tlPopHeap() | 36 | 77.78% | needs_review |
| `0028de28` | EnableEvent | 36 | 88.89% | needs_review |
| `0028de4c` | DisableEvent | 36 | 88.89% | needs_review |
| `0028e470` | CdIntToPos | 36 | 100.0% | auto_structural |
| `0028e494` | CdPosToInt | 36 | 100.0% | auto_structural |
| `00291074` | PSX_LoadImage | 36 | 77.78% | needs_review |
| `00291154` | StoreImage | 36 | 77.78% | needs_review |
| `0029128c` | MoveImage | 36 | 77.78% | needs_review |
| `002914e4` | SetSprt | 36 | 100.0% | auto_structural |
| `00291508` | SetSprt16 | 36 | 100.0% | auto_structural |
| `0029152c` | SetSprt8 | 36 | 100.0% | auto_structural |
| `00291628` | SetTile | 36 | 100.0% | auto_structural |
| `0029164c` | SetTile1 | 36 | 100.0% | auto_structural |
| `00291670` | SetTile16 | 36 | 100.0% | auto_structural |
| `00291694` | SetTile8 | 36 | 100.0% | auto_structural |
| `00291800` | SetDrawMove | 36 | 100.0% | auto_structural |
| `00294e64` | GetDrawEnv | 36 | 88.89% | needs_review |
| `0029a834` | ClearImage | 36 | 77.78% | needs_review |
| `0029b654` | GsSetClip2D | 36 | 88.89% | needs_review |
| `002a0ae0` | TransMatrix | 36 | 100.0% | auto_structural |
| `002a1408` | SetFogFar | 36 | 88.89% | needs_review |
| `002cab50` | __aeabi_ui2d | 36 | 100.0% | auto_structural |
| `002cb8a4` | __aeabi_cfrcmple | 36 | 100.0% | auto_structural |
| `002cd9e0` | ___Unwind_RaiseException | 36 | 100.0% | auto_structural |
| `002cda04` | ___Unwind_Resume | 36 | 100.0% | auto_structural |
| `002cda28` | ___Unwind_Resume_or_Rethrow | 36 | 100.0% | auto_structural |
| `002cda4c` | ___Unwind_ForcedUnwind | 36 | 100.0% | auto_structural |
| `002cda70` | _Unwind_Backtrace | 36 | 100.0% | auto_structural |
| `000ab654` | CEGL2_SHADER::Init() | 32 | 100.0% | auto_structural |
| `000b1bc8` | CEGL_PACKET::GetVBOBufferCurrent() | 32 | 100.0% | auto_structural |
| `000c8158` | tool_writesquare(int, int, int) | 32 | 87.5% | needs_review |
| `000c8178` | tool_readsquare(int, int, int) | 32 | 87.5% | needs_review |
| `000d88fc` | stopmenutransfer() | 32 | 87.5% | needs_review |
| `000d891c` | startmenutransfer() | 32 | 87.5% | needs_review |
| `000da700` | chk_nexteventtype(int) | 32 | 87.5% | needs_review |
| `001005cc` | Wstopmenutransfer() | 32 | 87.5% | needs_review |
| `001005ec` | Wstartmenutransfer() | 32 | 87.5% | needs_review |
| `001022cc` | Wchk_nexteventtype(int) | 32 | 87.5% | needs_review |
| `00153450` | task_status(long) | 32 | 87.5% | needs_review |
| `00153714` | Wtask_status(long) | 32 | 87.5% | needs_review |
| `00153c84` | iOS_updateDispCameraIconSetting() | 32 | 87.5% | needs_review |
| `00155c8c` | stop_adventuremessage(int) | 32 | 87.5% | needs_review |
| `0015832c` | rewrite_worldscroll(int) | 32 | 87.5% | needs_review |
| `0015a5ec` | siOS_TCurGet(unsigned int) | 32 | 87.5% | needs_review |
| `0015ad18` | iOSCurIsInGame(int, int) | 32 | 100.0% | auto_structural |
| `0015bf38` | iOSTchMovingModeCheck() | 32 | 87.5% | needs_review |
| `0015c01c` | iOSTchHoseiControl() | 32 | 87.5% | needs_review |
| `001adc48` | FadeCondition() | 32 | 87.5% | needs_review |
| `001b9d84` | iOS_clearTutorialbreak() | 32 | 87.5% | needs_review |
| `001d66f8` | set_td(unsigned char*) | 32 | 87.5% | needs_review |
| `001d98a8` | get_shape2_plus(BWORK*, unsigned char*) | 32 | 100.0% | auto_structural |
| `001d9910` | get_ability_flag(BWORK*, int) | 32 | 100.0% | auto_structural |
| `001d9948` | copy_struct_data(void const*, void*, int) | 32 | 100.0% | auto_structural |
| `001da018` | clear_cmemory(void*, int) | 32 | 100.0% | auto_structural |
| `001ffb30` | callAnimationSound(tag_animation*, int) | 32 | 100.0% | auto_structural |
| `00202efc` | iOS_BattleEventCheck() | 32 | 87.5% | needs_review |
| `002044e0` | iOSpreCommandInit() | 32 | 100.0% | auto_structural |
| `002064a8` | iOS_IsEnableMenuItemTouch() | 32 | 87.5% | needs_review |
| `0020696c` | iOS_IsEnableFlicker() | 32 | 87.5% | needs_review |
| `0020e720` | resetAnimationHFlip(int) | 32 | 100.0% | auto_structural |
| `0020f6c0` | startModelAnimation(int, int) | 32 | 100.0% | auto_structural |
| `0020f6f4` | startVRAMAnimation(int, int) | 32 | 100.0% | auto_structural |
| `0020f8cc` | setFrameRate(int) | 32 | 87.5% | needs_review |
| `002119a0` | ResetChangePalette() | 32 | 87.5% | needs_review |
| `0021b8a4` | PushGravity() | 32 | 87.5% | needs_review |
| `0021bcd8` | s0_end(_EffectTCB*) | 32 | 100.0% | auto_structural |
| `0021bcf8` | s1_goto(_EffectTCB*) | 32 | 100.0% | auto_structural |
| `0021c31c` | s9_pushMapScrollXYZ(_EffectTCB*) | 32 | 100.0% | auto_structural |
| `0021c33c` | sa_popMapScrollXYZ(_EffectTCB*) | 32 | 100.0% | auto_structural |
| `0021c3ac` | sc_pushMapAngle(_EffectTCB*) | 32 | 100.0% | auto_structural |
| `0021c3cc` | sd_popMapAngle(_EffectTCB*) | 32 | 100.0% | auto_structural |
| `0021c434` | sf_pushMapScale(_EffectTCB*) | 32 | 100.0% | auto_structural |
| `0021c454` | s24_popMapScale(_EffectTCB*) | 32 | 100.0% | auto_structural |
| `0021cedc` | UnlockEffect() | 32 | 87.5% | needs_review |
| `0021cefc` | LockEffectCompelBreak() | 32 | 87.5% | needs_review |
| `0021d2c0` | s2b_initMetascheduleControl(_EffectTCB*) | 32 | 100.0% | auto_structural |
| `0021f308` | PermanentEffectEndRequest(unsigned char) | 32 | 87.5% | needs_review |
| `0022a2cc` | getAbsoluteMaximumOf2(short, short) | 32 | 100.0% | auto_structural |
| `0024c534` | bgscrol_chk(_POINT*, VECTOR*) | 32 | 100.0% | auto_structural |
| `0024f4b0` | ctltips_active(CTLINFO*) | 32 | 87.5% | needs_review |
| `002657d8` | backpage_put(CTLINFO*, int) | 32 | 100.0% | auto_structural |
| `0026df10` | ctlhentuto_active(CTLINFO*) | 32 | 87.5% | needs_review |
| `00270500` | curhis_clr(int) | 32 | 87.5% | needs_review |
| `0027f620` | iOS_ResumeGetData(unsigned char**, unsigned int*) | 32 | 75.0% | needs_review |
| `0028080c` | IOS_PSP2IOS_X(int) | 32 | 87.5% | needs_review |
| `0028082c` | IOS_PSP2IOS_Y(int) | 32 | 87.5% | needs_review |
| `00288a58` | pspPrimDirectParamSet(int, RECT16*) | 32 | 87.5% | needs_review |
| `0028b610` | initXpHeap() | 32 | 87.5% | needs_review |
| `0028ba84` | TE_task_start(long) | 32 | 87.5% | needs_review |
| `0028ce58` | sceCtrlPeekBufferPositive | 32 | 87.5% | needs_review |
| `00294e44` | GetDispEnv | 32 | 87.5% | needs_review |
| `0029ae70` | xpLib_GetTPage(int*) | 32 | 87.5% | needs_review |
| `0029c934` | sceVfpuVector4Set(ScePspFVector4*, float, float, float, float) | 32 | 100.0% | auto_structural |
| `002a0a80` | ApplyRotMatrix | 32 | 100.0% | auto_structural |
| `002a1108` | Square0 | 32 | 100.0% | auto_structural |
| `002a1128` | Square12 | 32 | 100.0% | auto_structural |
| `002a1350` | ReadGeomOffset | 32 | 87.5% | needs_review |
| `002a2c70` | PCread | 32 | 87.5% | needs_review |
| `002a2ca8` | PClseek | 32 | 87.5% | needs_review |
| `002a2ce0` | PCwrite | 32 | 87.5% | needs_review |
| `002ae8c0` | GlTexEnv_GetSprite(int) | 32 | 87.5% | needs_review |
| `002ae8e0` | GlTexEnv_GetTextureHandle(int) | 32 | 87.5% | needs_review |
| `002b01e0` | GlTexEnv_GetTextureHandle_2X(int) | 32 | 87.5% | needs_review |
| `002b0400` | CAPP_INFO::CAPP_INFO() | 32 | 100.0% | auto_structural |
| `002b06d4` | CDebugPrint::EngineUninit() | 32 | 100.0% | auto_structural |
| `002b2358` | Music_Play(int, int, int, int) | 32 | 87.5% | needs_review |
| `002b871c` | iOS_isTouchBegan() | 32 | 87.5% | needs_review |
| `002ca77c` | __aeabi_uidivmod | 32 | 100.0% | auto_structural |
| `002ca878` | __aeabi_idivmod | 32 | 100.0% | auto_structural |
| `002cb48c` | __aeabi_i2f | 32 | 100.0% | auto_structural |
| `002ccf74` | __gnu_Unwind_Resume_or_Rethrow | 32 | 100.0% | auto_structural |
| `002ccf98` | _Unwind_DeleteException | 32 | 62.5% | needs_review |
| `000726e0` | JNI_OnLoad | 28 | 85.71% | needs_review |
| `00073ad4` | compress | 28 | 100.0% | auto_structural |
| `0007d894` | call_zopen64 | 28 | 100.0% | auto_structural |
| `00082fd8` | oggpack_bytes | 28 | 100.0% | auto_structural |
| `000af9a0` | CCAMERA::Init(float, float) | 28 | 100.0% | auto_structural |
| `000b61e4` | CCOMP_Z_DEC::CCOMP_Z_DEC() | 28 | 100.0% | auto_structural |
| `000b63b0` | CCOMP_Z_ENC::CCOMP_Z_ENC() | 28 | 100.0% | auto_structural |
| `000b9e78` | CTHREAD::CTHREAD() | 28 | 100.0% | auto_structural |
| `000b9e94` | CTHREAD::Create(int) | 28 | 100.0% | auto_structural |
| `000bd170` | CSOUND_LOADER_OGG::GetFormatDecoded() const | 28 | 100.0% | auto_structural |
| `000bd504` | CSOUND_LOADER_OGG::~CSOUND_LOADER_OGG() | 28 | 100.0% | auto_structural |
| `000bdd38` | CSTEP::Pause(int) | 28 | 100.0% | auto_structural |
| `000bdd54` | CSTEP::Uninit() | 28 | 100.0% | auto_structural |
| `000d961c` | setplatetime(int) | 28 | 85.71% | needs_review |
| `000d9748` | iOS_battle_scrollwindow_tap() | 28 | 85.71% | needs_review |
| `000daae8` | hook_wipe() | 28 | 100.0% | auto_structural |
| `000e628c` | Get_bravebreak() | 28 | 85.71% | needs_review |
| `000e62a8` | Set_bravebreak(unsigned short) | 28 | 85.71% | needs_review |
| `00101434` | Wsetplatetime(int) | 28 | 85.71% | needs_review |
| `0010155c` | WiOS_battle_scrollwindow_tap() | 28 | 85.71% | needs_review |
| `00101fa4` | Wchangeflame(int) | 28 | 85.71% | needs_review |
| `00155854` | set_worldday(int, int) | 28 | 85.71% | needs_review |
| `00155870` | set_worldmoney(int) | 28 | 85.71% | needs_review |
| `00155c5c` | ret_optionstatus() | 28 | 85.71% | needs_review |
| `00159a54` | asmGetActiveTask(int) | 28 | 85.71% | needs_review |
| `0018378c` | fileclose(unsigned int) | 28 | 85.71% | needs_review |
| `00196ea0` | MenuSelSideDirect(unsigned char, unsigned char) | 28 | 85.71% | needs_review |
| `001a8604` | Mituryo(short) | 28 | 85.71% | needs_review |
| `001b70f4` | DrawMessageWithPosition(int, COMRECORD*, int) | 28 | 85.71% | needs_review |
| `001c7218` | TEST_TEST() | 28 | 85.71% | needs_review |
| `001ca938` | net_setknockback(unsigned char, unsigned char, unsigned char) | 28 | 85.71% | needs_review |
| `001d357c` | set_playerwork2(PENTRY*, unsigned char*) | 28 | 85.71% | needs_review |
| `001d751c` | erase_unit(int) | 28 | 85.71% | needs_review |
| `001d9354` | set_jcflag(unsigned char*, int) | 28 | 100.0% | auto_structural |
| `0020177c` | reserveActionDirection(tag_animation*) | 28 | 100.0% | auto_structural |
| `00202ee0` | isInputEnable() | 28 | 100.0% | auto_structural |
| `0020e694` | checkAnimationExist(int) | 28 | 100.0% | auto_structural |
| `0021f2ec` | GetPEffectStatus(unsigned char) | 28 | 85.71% | needs_review |
| `0022a95c` | EqualSVectorToVECTOR(SVector*, VECTOR*) | 28 | 100.0% | auto_structural |
| `0022a978` | EqualSVectorToSVECTOR(SVector*, SVECTOR*) | 28 | 100.0% | auto_structural |
| `002419a8` | doublespeed_chk(CDREC*) | 28 | 100.0% | auto_structural |
| `0024b080` | wldbinEntry() | 28 | 85.71% | needs_review |
| `0024d948` | iOS_BRST_CHECK() | 28 | 85.71% | needs_review |
| `00258ac8` | evt_skip1() | 28 | 85.71% | needs_review |
| `00258ae4` | evt_skip2() | 28 | 85.71% | needs_review |
| `00258b00` | evt_skip3() | 28 | 85.71% | needs_review |
| `00258b1c` | evt_skip4() | 28 | 85.71% | needs_review |
| `00258b38` | evt_item() | 28 | 85.71% | needs_review |
| `00258b54` | evt_eqp() | 28 | 85.71% | needs_review |
| `0026973c` | snpl_endpage() | 28 | 85.71% | needs_review |
| `00269758` | snpl_startpage() | 28 | 85.71% | needs_review |
| `0026c25c` | iOSNovelModeRestore() | 28 | 85.71% | needs_review |
| `00271324` | Ssd_PlayEffects01(long, long) | 28 | 100.0% | auto_structural |
| `00279f68` | JudgeTimeOut() | 28 | 100.0% | auto_structural |
| `00281678` | iOS_v2menuGetItem() | 28 | 85.71% | needs_review |
| `002885b8` | pspOpenDisableFlg(PSP_OPEN_FLG) | 28 | 85.71% | needs_review |
| `002885d4` | pspOpenEnableFlg(PSP_OPEN_FLG) | 28 | 85.71% | needs_review |
| `0028b018` | pspWorldEnableFlg(PSP_WORLD_FLG) | 28 | 85.71% | needs_review |
| `0028b034` | pspWorldDisableFlg(PSP_WORLD_FLG) | 28 | 85.71% | needs_review |
| `0028da90` | tlMallocErrorFunc(void (*)(TL_MALLOC_ERROR)) | 28 | 85.71% | needs_review |
| `0028e5c4` | VSyncCallback | 28 | 85.71% | needs_review |
| `0028e6d4` | xpSetWaitVSyncFunc(int (*)()) | 28 | 85.71% | needs_review |
| `00290e6c` | DrawSyncCallback | 28 | 85.71% | needs_review |
| `00291bc0` | PutDrawEnv | 28 | 100.0% | auto_structural |
| `0029b3f0` | GsClearDispArea | 28 | 100.0% | auto_structural |
| `0029fea0` | rcos | 28 | 85.71% | needs_review |
| `0029fed4` | PSX_ccos | 28 | 85.71% | needs_review |
| `002a1440` | SetLightMatrix | 28 | 85.71% | needs_review |
| `002a148c` | SetColorMatrix | 28 | 85.71% | needs_review |
| `002a1534` | LightColor | 28 | 100.0% | auto_structural |
| `002a1550` | LocalLight | 28 | 100.0% | auto_structural |
| `002a2a4c` | xpPadKeyBufGet | 28 | 85.71% | needs_review |
| `002a2b10` | xpPadDebugSet | 28 | 85.71% | needs_review |
| `002acb2c` | GuEmu_GetRAW(int) | 28 | 85.71% | needs_review |
| `002b1bcc` | NowLoading_Bootup() | 28 | 71.43% | needs_review |
| `002b242c` | Music_IsPlaying() | 28 | 85.71% | needs_review |
| `002b7034` | iOSCancelButtonCheck() | 28 | 85.71% | needs_review |
| `002befa0` | iOS_OrMenuTouchKeyInput(unsigned int) | 28 | 85.71% | needs_review |
| `002ccee4` | __gnu_Unwind_ForcedUnwind | 28 | 100.0% | auto_structural |
| `002cdeec` | _Unwind_GetLanguageSpecificData | 28 | 100.0% | auto_structural |
| `000823ec` | zError | 24 | 83.33% | needs_review |
| `000826ec` | oggpack_writealign | 24 | 100.0% | auto_structural |
| `00082880` | oggpackB_writealign | 24 | 100.0% | auto_structural |
| `000a6d9c` | CGX_SCREEN_CORRECT::CGX_SCREEN_CORRECT() | 24 | 100.0% | auto_structural |
| `000b9d8c` | CWORK_MEM::~CWORK_MEM() | 24 | 100.0% | auto_structural |
| `000c8138` | return_pentry() | 24 | 83.33% | needs_review |
| `000c8198` | tool_squarecursor(int, int) | 24 | 83.33% | needs_review |
| `000cbb30` | resetYLine() | 24 | 83.33% | needs_review |
| `000cbd78` | pspEntrySquareDataGet() | 24 | 83.33% | needs_review |
| `000da5f8` | return_actionstructure() | 24 | 83.33% | needs_review |
| `000da808` | whatweather() | 24 | 83.33% | needs_review |
| `000ddd48` | tutorial_padcontrol(int*) | 24 | 83.33% | needs_review |
| `000e0fa0` | loadcdst(int, int) | 24 | 83.33% | needs_review |
| `00101578` | WiOS_set_status_pad(unsigned long*) | 24 | 83.33% | needs_review |
| `001024e4` | Wwhatweather() | 24 | 83.33% | needs_review |
| `0010729c` | Wtutorial_padcontrol(int*) | 24 | 83.33% | needs_review |
| `0010fa04` | Wloadcdst(int, int) | 24 | 83.33% | needs_review |
| `00150690` | setNetErrorCutFlg() | 24 | 83.33% | needs_review |
| `001506bc` | rsetNetErrorCutFlg() | 24 | 83.33% | needs_review |
| `001506d4` | SetgMission_Successflg() | 24 | 83.33% | needs_review |
| `001531cc` | ResetgMission_Successflg() | 24 | 83.33% | needs_review |
| `001556f0` | worldcursorposset(int) | 24 | 83.33% | needs_review |
| `00155d70` | reactive_worldstatus() | 24 | 83.33% | needs_review |
| `00155dd4` | active_worldstatus() | 24 | 83.33% | needs_review |
| `00155dec` | teach_onocursor(int, int) | 24 | 83.33% | needs_review |
| `0015a72c` | iOSScrollButtonDTap() | 24 | 83.33% | needs_review |
| `0015ff88` | iOSCircleCtrl(unsigned short) | 24 | 100.0% | auto_structural |
| `00161e60` | iOSSetRotMode() | 24 | 83.33% | needs_review |
| `001a9228` | GetItemPrice(short) | 24 | 100.0% | auto_structural |
| `001d9930` | copyACTst(ACT*, ACT*) | 24 | 100.0% | auto_structural |
| `001ed94c` | getDirectionVector(int) | 24 | 83.33% | needs_review |
| `001eee48` | getShapeWaitType(unsigned short) | 24 | 83.33% | needs_review |
| `001fd2ac` | resetTurnOrder() | 24 | 83.33% | needs_review |
| `0020f4fc` | clearOverSpecCtr() | 24 | 83.33% | needs_review |
| `0020f538` | restartAnimation() | 24 | 83.33% | needs_review |
| `0020f8a0` | finishAttackTeamSelect() | 24 | 83.33% | needs_review |
| `0020f8ec` | resetFrameRate() | 24 | 83.33% | needs_review |
| `0020ffec` | iOS_InitializeHot2() | 24 | 100.0% | auto_structural |
| `002160f4` | ps_main() | 24 | 100.0% | auto_structural |
| `00216128` | iOS_resetTexCacheLine() | 24 | 83.33% | needs_review |
| `00216848` | getMusicPointer(int) | 24 | 83.33% | needs_review |
| `00218628` | SetAnimationMode(effectAnimation*, short) | 24 | 100.0% | auto_structural |
| `0021b4f4` | largeFileRead(long, char*, unsigned long) | 24 | 100.0% | auto_structural |
| `0021b8f0` | PushAirDensity() | 24 | 83.33% | needs_review |
| `0021b908` | PopAirDensity() | 24 | 83.33% | needs_review |
| `0021c1e4` | s2c_samplingMSQFrame(_EffectTCB*) | 24 | 100.0% | auto_structural |
| `0021c1fc` | s2d_samplingSQLFrame(_EffectTCB*) | 24 | 100.0% | auto_structural |
| `0021c214` | dmyFnc(_EffectTCB*) | 24 | 100.0% | auto_structural |
| `00228c44` | CreateObjectWithTableWithParentData(short, int, int, int, _Object*) | 24 | 100.0% | auto_structural |
| `00228c5c` | OgataInit() | 24 | 100.0% | auto_structural |
| `00245a40` | strKickCD(CdlLOC*) | 24 | 100.0% | auto_structural |
| `00248598` | iOS_TestDraw(unsigned long*) | 24 | 83.33% | needs_review |
| `0024dcc0` | ctlkiroku_deactive(CTLINFO*) | 24 | 83.33% | needs_review |
| `0024e904` | ctlperson_deactive(CTLINFO*) | 24 | 83.33% | needs_review |
| `00259750` | ctlhistory_active(CTLINFO*) | 24 | 83.33% | needs_review |
| `00259768` | ctlhistory_deactive(CTLINFO*) | 24 | 83.33% | needs_review |
| `00259ea4` | ctlhouk_deactive(CTLINFO*) | 24 | 83.33% | needs_review |
| `0025e294` | mkadrtbl_calc(int) | 24 | 83.33% | needs_review |
| `0025ffe0` | iOS_IsTutoStart() | 24 | 83.33% | needs_review |
| `002602f4` | ctlmouke_deactive(CTLINFO*) | 24 | 83.33% | needs_review |
| `002675f4` | ctlret_deactive(CTLINFO*) | 24 | 83.33% | needs_review |
| `0026a85c` | envSound_play(int) | 24 | 100.0% | auto_structural |
| `0026c400` | ctltresure_deactive(CTLINFO*) | 24 | 83.33% | needs_review |
| `0026df30` | ctlhentuto_deactive(CTLINFO*) | 24 | 83.33% | needs_review |
| `0026ec30` | ctlsentuto_deactive(CTLINFO*) | 24 | 83.33% | needs_review |
| `00271284` | Ssd_Init(unsigned short) | 24 | 83.33% | needs_review |
| `00279ed4` | ClearForBattleRoutine() | 24 | 83.33% | needs_review |
| `0027d468` | disableCancelDisableArea() | 24 | 83.33% | needs_review |
| `0027f5d8` | Resume_Get_WORK_MU_FontID() | 24 | 83.33% | needs_review |
| `0027f5f0` | Resume_Get_WORK_MU_BWorkFontID() | 24 | 83.33% | needs_review |
| `0027f608` | Resume_Get_WORK_MU_BWorkAnimationID() | 24 | 83.33% | needs_review |
| `0027fc30` | cSaveFFT::cSaveFFT(char*) | 24 | 100.0% | auto_structural |
| `00280540` | iOS_fftSave() | 24 | 83.33% | needs_review |
| `002806f0` | iOS_clearDebugPrimNum() | 24 | 83.33% | needs_review |
| `0028164c` | iOS_v2menuSetScreenSize(int, int) | 24 | 83.33% | needs_review |
| `00283fb0` | mapclip_setpath(char*) | 24 | 83.33% | needs_review |
| `002847c0` | new_ColorVectorDataBase(unsigned int) | 24 | 83.33% | needs_review |
| `00287588` | reset_g_NetIcon_DrawFlg() | 24 | 83.33% | needs_review |
| `002885a0` | pspOpenCheckFlg(PSP_OPEN_FLG) | 24 | 83.33% | needs_review |
| `00288f18` | pspgFreamBufCountCountReset() | 24 | 83.33% | needs_review |
| `0028982c` | pspPrimReetWorkBuf_current() | 24 | 83.33% | needs_review |
| `00289880` | pspClearSaveEnv() | 24 | 83.33% | needs_review |
| `0028a114` | FFT_GetCurrentSystemFile() | 24 | 83.33% | needs_review |
| `0028b050` | pspWorldCheckFlg(PSP_WORLD_FLG) | 24 | 83.33% | needs_review |
| `0028b068` | pspWorldCallBackSet(PSP_WORLD_CALLBACK_ID, void (*)()) | 24 | 83.33% | needs_review |
| `0028b3c4` | pspWorldDataBackBufGet(int) | 24 | 83.33% | needs_review |
| `0028c2c0` | CFFT_STATE::GetMenuBarVisible() | 24 | 100.0% | auto_structural |
| `0028d688` | tlFreeAll() | 24 | 83.33% | needs_review |
| `00291a6c` | SetSemiTrans | 24 | 100.0% | auto_structural |
| `00291a84` | SetShadeTex | 24 | 100.0% | auto_structural |
| `0029b6d0` | GsSetWorkBase | 24 | 83.33% | needs_review |
| `0029fd90` | GteGetDataReg(int) | 24 | 83.33% | needs_review |
| `0029fdbc` | GteSetDataReg(long, long) | 24 | 83.33% | needs_review |
| `0029fe70` | InitGeom | 24 | 83.33% | needs_review |
| `0029fe88` | rsin | 24 | 83.33% | needs_review |
| `0029febc` | PSX_csin | 24 | 83.33% | needs_review |
| `002a0954` | MulRotMatrix | 24 | 100.0% | auto_structural |
| `002a1324` | SetGeomOffset | 24 | 83.33% | needs_review |
| `002a13f0` | SetFogNearFar | 24 | 83.33% | needs_review |
| `002a1ad4` | read_sxsy0(long*) | 24 | 83.33% | needs_review |
| `002a1aec` | read_sxsy1(long*) | 24 | 83.33% | needs_review |
| `002a1b04` | read_sxsy2(long*) | 24 | 83.33% | needs_review |
| `002a1b44` | read_rgb0(long*) | 24 | 83.33% | needs_review |
| `002a1b5c` | read_rgb1(long*) | 24 | 83.33% | needs_review |
| `002a1b74` | read_rgb2(long*) | 24 | 83.33% | needs_review |
| `002a1b8c` | read_flag(long*) | 24 | 83.33% | needs_review |
| `002a1ba4` | read_p(long*) | 24 | 83.33% | needs_review |
| `002a25c8` | read_otz(long*) | 24 | 83.33% | needs_review |
| `002a25e0` | read_opz(long*) | 24 | 83.33% | needs_review |
| `002a2728` | xpPadAnalogAssign | 24 | 83.33% | needs_review |
| `002a2a34` | xpPadUpdateData | 24 | 83.33% | needs_review |
| `002a2a68` | xpPadWorkBufGet | 24 | 83.33% | needs_review |
| `002a2a80` | xpPadTriggerGet | 24 | 83.33% | needs_review |
| `002a2a98` | xpPadGet | 24 | 83.33% | needs_review |
| `002a2ab0` | xpPadAnalogXGet | 24 | 83.33% | needs_review |
| `002a2ac8` | xpPadAnalogYGet | 24 | 83.33% | needs_review |
| `002a2ae0` | xpPadPspPadDataGet | 24 | 83.33% | needs_review |
| `002a2af8` | xpPadRepeatGet | 24 | 83.33% | needs_review |
| `002a2b2c` | xpPadKeyTblSet | 24 | 83.33% | needs_review |
| `002a2b44` | xpPadKeyTblGet | 24 | 83.33% | needs_review |
| `002a2fb8` | PCcreat | 24 | 83.33% | needs_review |
| `002ab608` | GuEmu_SetLineInterval(int) | 24 | 83.33% | needs_review |
| `002b36bc` | Error_Init() | 24 | 83.33% | needs_review |
| `002b376c` | Error_SetError(int, char*) | 24 | 83.33% | needs_review |
| `002b701c` | iOSHelpButtonCheck() | 24 | 83.33% | needs_review |
| `002b7a5c` | SetDisableMapTouch() | 24 | 83.33% | needs_review |
| `002b7a74` | ClearDisableMapTouch() | 24 | 83.33% | needs_review |
| `002bef4c` | iOS_isExistResumeData() | 24 | 83.33% | needs_review |
| `002befbc` | iOS_ClearMenuTouchKeyInput() | 24 | 83.33% | needs_review |
| `002bf008` | chkSeDouble() | 24 | 100.0% | auto_structural |
| `002c53e8` | Movie_Init() | 24 | 83.33% | needs_review |
| `00073a04` | adler32_combine | 20 | 100.0% | auto_structural |
| `00073a18` | adler32_combine64 | 20 | 100.0% | auto_structural |
| `00073af0` | compressBound | 20 | 100.0% | auto_structural |
| `000acec4` | CEGL2_SPRITE::GetTextureSize(float*, float*) | 20 | 100.0% | auto_structural |
| `000b1950` | CEGL_PACKET::Clear() | 20 | 100.0% | auto_structural |
| `000b1ba0` | CEGL_PACKET::SetExtraCurrent(int, int) | 20 | 100.0% | auto_structural |
| `000b546c` | CRECT::SetEnable(int, int) | 20 | 100.0% | auto_structural |
| `000b8980` | CLIST::Init() | 20 | 100.0% | auto_structural |
| `000b8994` | CLIST::CLIST() | 20 | 100.0% | auto_structural |
| `000b9d48` | CWORK_MEM::CWORK_MEM() | 20 | 100.0% | auto_structural |
| `000b9ddc` | CWORK_MEM::GetTail(unsigned int) | 20 | 100.0% | auto_structural |
| `000bbc18` | CSOUND_IF_SL::GetSLFormat(int) | 20 | 100.0% | auto_structural |
| `000bd154` | CSOUND_LOADER_OGG::GetFormat() const | 20 | 100.0% | auto_structural |
| `000bd1c8` | CSOUND_LOADER_OGG::GetLoopOut() const | 20 | 100.0% | auto_structural |
| `000bd3a0` | COggMemMapFile::COggMemMapFile() | 20 | 100.0% | auto_structural |
| `000bd450` | COggMemMapFile::~COggMemMapFile() | 20 | 100.0% | auto_structural |
| `000c81b0` | tool_setarrowmode(int) | 20 | 80.0% | needs_review |
| `000cbb1c` | getYLine() | 20 | 80.0% | needs_review |
| `000cbc28` | TrapWindow_Taskchk(int) | 20 | 100.0% | auto_structural |
| `000d9608` | get_padframe() | 20 | 80.0% | needs_review |
| `00101420` | Wget_padframe() | 20 | 80.0% | needs_review |
| `00101590` | WiOS_getStatusAllgrayf() | 20 | 80.0% | needs_review |
| `00101fd0` | iOStorideflagGet() | 20 | 80.0% | needs_review |
| `001021c8` | Wreturn_actionstructure() | 20 | 80.0% | needs_review |
| `0010f110` | Wattackteam_call(unsigned long*, unsigned long) | 20 | 100.0% | auto_structural |
| `0012f214` | iOSpersonalWinPosClear(int) | 20 | 80.0% | needs_review |
| `0012f2dc` | iOSPersonalWinPosSet(int) | 20 | 80.0% | needs_review |
| `00142840` | WiOS_getOptionAddOfsX() | 20 | 80.0% | needs_review |
| `00142f4c` | WiOS_getOptionAddOfsMode() | 20 | 80.0% | needs_review |
| `0014bec8` | disp_requirement() | 20 | 100.0% | auto_structural |
| `001506a8` | getNetErrorCutFlg() | 20 | 80.0% | needs_review |
| `001531e4` | GetgMission_Successflg() | 20 | 80.0% | needs_review |
| `00155c78` | ret_adventurestatus() | 20 | 80.0% | needs_review |
| `00156550` | send_worldkeymask(unsigned long) | 20 | 80.0% | needs_review |
| `001579ac` | worldcursormove(int) | 20 | 80.0% | needs_review |
| `001579c0` | regist_zodiacot(unsigned int*) | 20 | 80.0% | needs_review |
| `0015a16c` | iOSTapTimeAreaGet() | 20 | 80.0% | needs_review |
| `0015a314` | iOSsTchBtlFlagGet() | 20 | 80.0% | needs_review |
| `0015a328` | iOSsTchBtlFlagSet(int) | 20 | 80.0% | needs_review |
| `0015a8a0` | iOSScrollgStatusModeGet() | 20 | 80.0% | needs_review |
| `0015da20` | iOSGetTchCurLimit() | 20 | 80.0% | needs_review |
| `0015fff4` | iOSGetTchRotDY() | 20 | 80.0% | needs_review |
| `00161944` | iOSHelpInputWaitGet() | 20 | 80.0% | needs_review |
| `00161958` | iOSHelpInputWaitSet(int) | 20 | 80.0% | needs_review |
| `0018f994` | eStopGetPad(int) | 20 | 80.0% | needs_review |
| `001a4858` | iOSLearnTypeSet(int) | 20 | 80.0% | needs_review |
| `001a9240` | GetItemSellPrice(short) | 20 | 100.0% | auto_structural |
| `001ac8b4` | dispFT4num() | 20 | 80.0% | needs_review |
| `001adc68` | FadeMask(int) | 20 | 80.0% | needs_review |
| `001aec64` | iOSItemTypeSet(int) | 20 | 80.0% | needs_review |
| `001aec78` | iOSItemTypeGet() | 20 | 80.0% | needs_review |
| `001b4c20` | IsDark(int) | 20 | 80.0% | needs_review |
| `001b8e50` | get_tutrial_pad() | 20 | 80.0% | needs_review |
| `001bab64` | GetSttsAMovingTime() | 20 | 80.0% | needs_review |
| `001d15b0` | get_originalability() | 20 | 80.0% | needs_review |
| `001d1f78` | charge_break(BWORK*) | 20 | 100.0% | auto_structural |
| `001d6480` | clear_actendflag(BWORK*) | 20 | 100.0% | auto_structural |
| `001eee34` | getEffSequenceAddress() | 20 | 80.0% | needs_review |
| `001fcdf0` | iOSgetCursorVisible() | 20 | 80.0% | needs_review |
| `002010b8` | iOSmapVectorScrollCheck() | 20 | 80.0% | needs_review |
| `002041e8` | setStartBattleFlg(int) | 20 | 80.0% | needs_review |
| `002041fc` | getStartBattleFlg() | 20 | 80.0% | needs_review |
| `00204254` | setTurning(int) | 20 | 80.0% | needs_review |
| `0020ea7c` | loadNewAnimation() | 20 | 100.0% | auto_structural |
| `0020f410` | eventEffectWait() | 20 | 100.0% | auto_structural |
| `0020f428` | eventEffectExecute() | 20 | 80.0% | needs_review |
| `0020f6e0` | checkModelAnimation(int) | 20 | 100.0% | auto_structural |
| `0020f714` | checkVRAMAnimation(int) | 20 | 100.0% | auto_structural |
| `0020f8b8` | getFrameTicks() | 20 | 80.0% | needs_review |
| `00215bac` | stopMapPaletteAnimation() | 20 | 100.0% | auto_structural |
| `00215bc0` | restertMapPaletteAnimation() | 20 | 100.0% | auto_structural |
| `00216604` | checkActiveMusic() | 20 | 80.0% | needs_review |
| `002168e8` | callEnvEffect(int) | 20 | 80.0% | needs_review |
| `0021b4e0` | GetPlugInFuncAdr(short) | 20 | 80.0% | needs_review |
| `0021b890` | SetAirDensity(long) | 20 | 80.0% | needs_review |
| `0021cf1c` | GetEffectStatus() | 20 | 80.0% | needs_review |
| `00228dd0` | GetShapePrimPtNow() | 20 | 80.0% | needs_review |
| `0024509c` | TEST_setClearOt(int) | 20 | 80.0% | needs_review |
| `002450b0` | TEST_getClearOt() | 20 | 80.0% | needs_review |
| `00245a60` | o_SelectCard(int) | 20 | 80.0% | needs_review |
| `00245b20` | o_WaitCardEvent() | 20 | 100.0% | auto_structural |
| `00245bf0` | o_WaitCardEvent_X() | 20 | 100.0% | auto_structural |
| `00249c44` | numa_vOpn_CdRead(CDREC*, unsigned long, unsigned long, unsigned long, unsigned long*) | 20 | 100.0% | auto_structural |
| `0025691c` | IOSsTownModeSet(int) | 20 | 80.0% | needs_review |
| `0025f3d8` | iOS_wld_pad_trg(unsigned long) | 20 | 80.0% | needs_review |
| `0025f3fc` | iOSSnapshotSet(int) | 20 | 80.0% | needs_review |
| `0025f410` | iOSSDNovelHelpTrgSet(long) | 20 | 80.0% | needs_review |
| `0025f424` | iOSSDNovelHelpTrgGet() | 20 | 80.0% | needs_review |
| `0027b480` | setDrawPrimNum(int) | 20 | 80.0% | needs_review |
| `0027b514` | getCmdKindNum() | 20 | 80.0% | needs_review |
| `0027b528` | getCmdKind(unsigned int) | 20 | 80.0% | needs_review |
| `0027fc14` | chk_ucResumeDataSetAddr(unsigned char*) | 20 | 80.0% | needs_review |
| `0028051c` | iOS_fftDelete() | 20 | 80.0% | needs_review |
| `00281664` | iOS_v2menuGetAddr() | 20 | 80.0% | needs_review |
| `00281694` | iOS_v2menuSetDecide(int) | 20 | 80.0% | needs_review |
| `002816a8` | iOS_v2menuGetDecide() | 20 | 80.0% | needs_review |
| `002819b8` | iOS_v2menuGetType() | 20 | 80.0% | needs_review |
| `00282274` | iOS_v2menuGetYline() | 20 | 80.0% | needs_review |
| `002826b4` | iOS_PalleteHosei(unsigned char, int) | 20 | 100.0% | auto_structural |
| `002843a0` | new_VectorDataBase(unsigned int) | 20 | 80.0% | needs_review |
| `002855b8` | pspItemIsEmpty | 20 | 100.0% | auto_structural |
| `00285f38` | pspMsgLzwBaseGet(FFTPSP_MSG_LZW) | 20 | 80.0% | needs_review |
| `0028612c` | ps_rand() | 20 | 100.0% | auto_structural |
| `002862e8` | IsMapTexAsideLoad(unsigned int) | 20 | 80.0% | needs_review |
| `00286794` | setEventStatus(int) | 20 | 80.0% | needs_review |
| `00286880` | getEventStatus() | 20 | 80.0% | needs_review |
| `00286894` | get_gEventMovieNo() | 20 | 80.0% | needs_review |
| `002868a8` | set_gEventMovieNo(int) | 20 | 80.0% | needs_review |
| `00286aa0` | get_netdatamode() | 20 | 80.0% | needs_review |
| `00286ab4` | set_netdatamode(int) | 20 | 80.0% | needs_review |
| `00286b0c` | set_limit_turn_flg(int) | 20 | 80.0% | needs_review |
| `00286b20` | get_limit_turn_flg() | 20 | 80.0% | needs_review |
| `00286dec` | GetNetmissionNo() | 20 | 80.0% | needs_review |
| `00287030` | get_timing_flag() | 20 | 80.0% | needs_review |
| `00287070` | get_rival() | 20 | 80.0% | needs_review |
| `00287a18` | set_g_Soldier_Draw_flg(int) | 20 | 80.0% | needs_review |
| `00287a2c` | get_g_Soldier_Draw_flg() | 20 | 80.0% | needs_review |
| `002884a0` | Set_NonDrawTaikiIconFlg(int) | 20 | 80.0% | needs_review |
| `002884b4` | Get_NonDrawTaikiIconFlg() | 20 | 80.0% | needs_review |
| `002884d4` | setBattlePoint(int) | 20 | 80.0% | needs_review |
| `002884e8` | getBattlePoint() | 20 | 80.0% | needs_review |
| `0028851c` | setMissionNo_CalcMissionPayPoint(int) | 20 | 80.0% | needs_review |
| `00288530` | getMissionNo_CalcMissionPayPoint() | 20 | 80.0% | needs_review |
| `00288544` | setTurnCount_CalcMissionPayPoint(int) | 20 | 80.0% | needs_review |
| `00288558` | getTurnCount_CalcMissionPayPoint() | 20 | 80.0% | needs_review |
| `00288578` | pspOpenDataBackBufGet(int) | 20 | 80.0% | needs_review |
| `0028858c` | pspOpenDataIconBufGet() | 20 | 80.0% | needs_review |
| `00289818` | pspPrimGetWorkBuf_current() | 20 | 80.0% | needs_review |
| `0028a08c` | Savedata_GetAddr() | 20 | 80.0% | needs_review |
| `0028a12c` | FFT_GetSavedata() | 20 | 80.0% | needs_review |
| `0028b3dc` | pspWorldDataRectGet() | 20 | 80.0% | needs_review |
| `0028ba2c` | getVSyncBlockCountTaskEmu() | 20 | 80.0% | needs_review |
| `0028ba40` | TE_setTaskType(int) | 20 | 80.0% | needs_review |
| `0028c204` | CFFT_STATE::GetRenderSize(int*, int*) | 20 | 100.0% | auto_structural |
| `0028c59c` | CFFT_STATE::AddParam(int, int) | 20 | 100.0% | auto_structural |
| `0028d1b0` | tlGetHeap() | 20 | 80.0% | needs_review |
| `0028dcf0` | StartRCnt | 20 | 80.0% | needs_review |
| `0028dea8` | InitCARD | 20 | 80.0% | needs_review |
| `0028df7c` | _card_info | 20 | 80.0% | needs_review |
| `00290b40` | SetDispMask | 20 | 100.0% | auto_structural |
| `0029b6e8` | GsGetWorkBase | 20 | 80.0% | needs_review |
| `0029fd7c` | GteGetCtrlReg(int) | 20 | 80.0% | needs_review |
| `0029fda8` | GteSetCtrlReg(long, long) | 20 | 80.0% | needs_review |
| `0029ff98` | SquareRoot0 | 20 | 100.0% | auto_structural |
| `002a133c` | SetGeomScreen | 20 | 80.0% | needs_review |
| `002a1370` | ReadGeomScreen | 20 | 80.0% | needs_review |
| `002a13b4` | InitClip | 20 | 80.0% | needs_review |
| `002a2da4` | PCclose | 20 | 80.0% | needs_review |
| `002a2fd0` | xpInitSPAD | 20 | 80.0% | needs_review |
| `002a3120` | xpGetHeapSize | 20 | 80.0% | needs_review |
| `002a3138` | xpSetResume | 20 | 80.0% | needs_review |
| `002ab6fc` | GPUCmd_GetGPUCmd_IP() | 20 | 80.0% | needs_review |
| `002ab8ec` | sceGuColor | 20 | 80.0% | needs_review |
| `002ab9cc` | sceGuFinishId | 20 | 80.0% | needs_review |
| `002abd20` | sceGuClutMode | 20 | 80.0% | needs_review |
| `002ac000` | sceGuTexMode | 20 | 80.0% | needs_review |
| `002b14d0` | Project_Archive_GetFile(int) | 20 | 80.0% | needs_review |
| `002b8708` | iOS_PressTime() | 20 | 80.0% | needs_review |
| `002b87e8` | iOS_isInGameArea() | 20 | 80.0% | needs_review |
| `002c53c0` | Main_GetPauseFlag() | 20 | 80.0% | needs_review |
| `002c53d4` | Main_SetPauseFlag(int) | 20 | 80.0% | needs_review |
| `002c9a25` | operator new[](unsigned int) | 20 | 100.0% | auto_structural |
| `002cb174` | __aeabi_cdcmple | 20 | 100.0% | auto_structural |
| `002cb188` | __aeabi_dcmpeq | 20 | 100.0% | auto_structural |
| `002cb19c` | __aeabi_dcmplt | 20 | 100.0% | auto_structural |
| `002cb1b0` | __aeabi_dcmple | 20 | 100.0% | auto_structural |
| `002cb1c4` | __aeabi_dcmpge | 20 | 100.0% | auto_structural |
| `002cb1d8` | __aeabi_dcmpgt | 20 | 100.0% | auto_structural |
| `002cb8b4` | __aeabi_cfcmple | 20 | 100.0% | auto_structural |
| `002cb8c8` | __aeabi_fcmpeq | 20 | 100.0% | auto_structural |
| `002cb8dc` | __aeabi_fcmplt | 20 | 100.0% | auto_structural |
| `002cb8f0` | __aeabi_fcmple | 20 | 100.0% | auto_structural |
| `002cb904` | __aeabi_fcmpge | 20 | 100.0% | auto_structural |
| `002cb918` | __aeabi_fcmpgt | 20 | 100.0% | auto_structural |
| `002cd8ec` | __restore_core_regs | 20 | 100.0% | auto_structural |
| `00073c64` | get_crc_table | 16 | 75.0% | needs_review |
| `0007b180` | inflateInit_ | 16 | 100.0% | auto_structural |
| `000823d4` | zlibVersion | 16 | 75.0% | needs_review |
| `00082ff4` | oggpack_bits | 16 | 100.0% | auto_structural |
| `000b1b0c` | CEGL_PACKET::SetTypeCurrent(unsigned char) | 16 | 100.0% | auto_structural |
| `000b1b34` | CEGL_PACKET::SetBlendModeCurrent(unsigned char) | 16 | 100.0% | auto_structural |
| `000b1b5c` | CEGL_PACKET::SetTextureCurrent(unsigned int) | 16 | 100.0% | auto_structural |
| `000b1b7c` | CEGL_PACKET::SetExtra(int, int, int) | 16 | 100.0% | auto_structural |
| `000b3528` | CINPUT_DATA::Init(_INPUT_DATA*) | 16 | 100.0% | auto_structural |
| `000b4f78` | CRECT::Clear() | 16 | 100.0% | auto_structural |
| `000bd464` | COggMemMapFile::IsOpen() const | 16 | 100.0% | auto_structural |
| `000bdb38` | CFRAMERATE::FrameStep(int) | 16 | 100.0% | auto_structural |
| `000bdb70` | CSTEP::Register(_DATA_STEP*) | 16 | 100.0% | auto_structural |
| `000c442c` | Adisp_abilitywindow() | 16 | 100.0% | auto_structural |
| `000d0ddc` | Ddisp_abilitywindow() | 16 | 100.0% | auto_structural |
| `000d6d98` | getStatusPad() | 16 | 75.0% | needs_review |
| `00101fc0` | WgetStatusPad() | 16 | 75.0% | needs_review |
| `0012b11c` | disp_abilitywindow() | 16 | 100.0% | auto_structural |
| `0014ba0c` | Cdisp_abilitywindow() | 16 | 100.0% | auto_structural |
| `0018377c` | fileopen(unsigned char*, unsigned int) | 16 | 75.0% | needs_review |
| `001a6368` | iOSLearnTypeGet() | 16 | 75.0% | needs_review |
| `001d4f00` | set_throwitem(int, unsigned char, unsigned char*) | 16 | 100.0% | auto_structural |
| `001eee24` | getEffShapeAddress() | 16 | 75.0% | needs_review |
| `0020d050` | getMapScrollXYZ() | 16 | 75.0% | needs_review |
| `0020d2a8` | getMapScroll() | 16 | 75.0% | needs_review |
| `0020d5c8` | getMapScale() | 16 | 75.0% | needs_review |
| `0020d83c` | getMapAngle() | 16 | 75.0% | needs_review |
| `0020dac8` | getBackColor() | 16 | 75.0% | needs_review |
| `0021036c` | setShortVector(SVECTOR*, int, int, int) | 16 | 100.0% | auto_structural |
| `0022a470` | getVariationData(int, int, int) | 16 | 100.0% | auto_structural |
| `00245b68` | o_CardInit() | 16 | 100.0% | auto_structural |
| `0025690c` | IOSsTownModeGet() | 16 | 75.0% | needs_review |
| `0025f3ec` | iOSSnapshotGet() | 16 | 75.0% | needs_review |
| `00263aac` | iOSNovelBrightStop() | 16 | 75.0% | needs_review |
| `0027b494` | getDrawPrimNum() | 16 | 75.0% | needs_review |
| `00285e40` | pspJobGetIndex2Job(int) | 16 | 100.0% | auto_structural |
| `0028bf3c` | TE_dummy() | 16 | 100.0% | auto_structural |
| `0028c5b0` | CFFT_STATE::GetStr(int) | 16 | 100.0% | auto_structural |
| `0028c7d8` | CAUTOSAVE::CAUTOSAVE() | 16 | 100.0% | auto_structural |
| `0028decc` | StartCARD | 16 | 75.0% | needs_review |
| `0028deec` | StopCARD | 16 | 75.0% | needs_review |
| `0028e694` | xpSetVblankFunc(void (*)(int, void*), void*) | 16 | 100.0% | auto_structural |
| `002a1028` | CompMatrix | 16 | 100.0% | auto_structural |
| `002a2be8` | PCinit | 16 | 75.0% | needs_review |
| `002a2fe4` | xpGetSPADAddress | 16 | 75.0% | needs_review |
| `002a3100` | xpMallocIO | 16 | 100.0% | auto_structural |
| `002a39a8` | pspSaveList::Update() | 16 | 100.0% | auto_structural |
| `002a39b8` | sceGeEdramGetAddr | 16 | 75.0% | needs_review |
| `002b1fe8` | Offscreen_Get() | 16 | 75.0% | needs_review |
| `002b375c` | Error_GetErrorCode() | 16 | 75.0% | needs_review |
| `002bef64` | ResumeData_GetHeapOffset() | 16 | 75.0% | needs_review |
| `002cb9dc` | __aeabi_ldiv0 | 16 | 100.0% | auto_structural |
| `002cdedc` | _Unwind_GetRegionStart | 16 | 100.0% | auto_structural |
| `00077ab8` | gzopen | 12 | 100.0% | auto_structural |
| `00077ac4` | gzopen64 | 12 | 100.0% | auto_structural |
| `000823c8` | unzSetOffset | 12 | 100.0% | auto_structural |
| `000a863c` | CEGL2_IF::GetCount(int) | 12 | 100.0% | auto_structural |
| `000b1b00` | CEGL_PACKET::SetType(int, unsigned char) | 12 | 100.0% | auto_structural |
| `000b1b1c` | CEGL_PACKET::GetBlendMode(int) | 12 | 100.0% | auto_structural |
| `000b1b28` | CEGL_PACKET::SetBlendMode(int, unsigned char) | 12 | 100.0% | auto_structural |
| `000b1b44` | CEGL_PACKET::GetTexture(int) | 12 | 100.0% | auto_structural |
| `000b1b50` | CEGL_PACKET::SetTexture(int, unsigned int) | 12 | 100.0% | auto_structural |
| `000b1bbc` | CEGL_PACKET::GetVBOInfo(int) | 12 | 100.0% | auto_structural |
| `000b3518` | CINPUT_DATA::CINPUT_DATA() | 12 | 100.0% | auto_structural |
| `000b3d44` | CINPUT_IF_TOUCH::SetKeyWait(int, int, unsigned int, unsigned int) | 12 | 100.0% | auto_structural |
| `000b3d5c` | CINPUT_IF_TOUCH::SetKeyDelay(int, int, unsigned int) | 12 | 100.0% | auto_structural |
| `000b4044` | CINPUT_IF_TOUCH::GetPress(int, int) | 12 | 100.0% | auto_structural |
| `000b40b0` | CINPUT_IF_TOUCH::GetDown(int, int) | 12 | 100.0% | auto_structural |
| `000b40c8` | CINPUT_IF_TOUCH::GetUp(int, int) | 12 | 100.0% | auto_structural |
| `000b40e0` | CINPUT_IF_TOUCH::GetRepeat(int, int) | 12 | 100.0% | auto_structural |
| `000b4f88` | CRECT::Register(_RECT_UI*, int) | 12 | 100.0% | auto_structural |
| `000b61d8` | CCOMP_Z_DEC::SetBlockSize(int, int) | 12 | 100.0% | auto_structural |
| `000b63a4` | CCOMP_Z_ENC::SetBlockSize(int, int) | 12 | 100.0% | auto_structural |
| `000b9f7c` | CTHREAD::RequestExit() | 12 | 100.0% | auto_structural |
| `000b9fac` | CTHREAD::RequestSuspend() | 12 | 100.0% | auto_structural |
| `000b9fb8` | CTHREAD::RequestResume() | 12 | 100.0% | auto_structural |
| `000b9fd4` | TRACE_Empty(char const*, ...) | 12 | 100.0% | auto_structural |
| `000ba084` | Sleep(unsigned int) | 12 | 100.0% | auto_structural |
| `000bdb60` | CSTEP::CSTEP() | 12 | 100.0% | auto_structural |
| `000bdb80` | CSTEP::SetUnit(int) | 12 | 100.0% | auto_structural |
| `000be1dc` | CSTEP_BATCH::Uninit() | 12 | 100.0% | auto_structural |
| `000d8734` | getanimpanel(int, SVECTOR*) | 12 | 100.0% | auto_structural |
| `00100408` | Wgetanimpanel(int, SVECTOR*) | 12 | 100.0% | auto_structural |
| `001d8d1c` | get_itemcommon(unsigned short) | 12 | 100.0% | auto_structural |
| `001dc908` | set_startingstatus(BWORK*) | 12 | 100.0% | auto_structural |
| `001e692c` | setskilldata_to_ACT(ACT*) | 12 | 100.0% | auto_structural |
| `0020ebb8` | eventTerminateAnimation(int, int, short, short, short) | 12 | 100.0% | auto_structural |
| `0021680c` | callZingle(int) | 12 | 100.0% | auto_structural |
| `0021b50c` | loadData(char*, char**) | 12 | 100.0% | auto_structural |
| `00223f24` | GetBowFirstSpeed() | 12 | 100.0% | auto_structural |
| `00243a60` | CreateList(tagLIST_STAFFROLL*, tagSTAFFROLL*) | 12 | 100.0% | auto_structural |
| `00263f9c` | ctlnobel_deactive(CTLINFO*) | 12 | 100.0% | auto_structural |
| `00282268` | iOS_clearOkNg() | 12 | 100.0% | auto_structural |
| `00284410` | Clear_VectorDataBaseObject(VECTOR_DATABASE*) | 12 | 100.0% | auto_structural |
| `0028a080` | pspGetFftPspSaveDataSize() | 12 | 100.0% | auto_structural |
| `0028aec4` | __bpGetFileNum | 12 | 100.0% | auto_structural |
| `0028afc4` | __bpGetBinarySize | 12 | 100.0% | auto_structural |
| `0028afd0` | __bpGetBinaryData | 12 | 100.0% | auto_structural |
| `0028c22c` | CFFT_STATE::SetVertexScaling(float, float) | 12 | 100.0% | auto_structural |
| `0028c2e8` | CFFT_STATE::SetMusicBuffer(int, int) | 12 | 100.0% | auto_structural |
| `0028c320` | CFFT_STATE::GetParam(int) | 12 | 100.0% | auto_structural |
| `0028c590` | CFFT_STATE::SetParam(int, int) | 12 | 100.0% | auto_structural |
| `0028ce48` | asmClearBuffer(void*, unsigned int) | 12 | 100.0% | auto_structural |
| `002a142c` | SetFogNear | 12 | 100.0% | auto_structural |
| `002b2cf8` | SysSE_PlayDef(int) | 12 | 100.0% | auto_structural |
| `002b2d04` | SysSE_PlayUI(int) | 12 | 100.0% | auto_structural |
| `002c9115` | operator delete(void*) | 12 | 100.0% | auto_structural |
| `000823e4` | zlibCompileFlags | 8 | 100.0% | auto_structural |
| `00082404` | zcalloc | 8 | 100.0% | auto_structural |
| `0008240c` | zcfree | 8 | 100.0% | auto_structural |
| `0008300c` | oggpack_get_buffer | 8 | 100.0% | auto_structural |
| `000ab4a8` | CEGL2_FBO::GetTexture() | 8 | 100.0% | auto_structural |
| `000acebc` | CEGL2_SPRITE::GetTextureHandle() | 8 | 100.0% | auto_structural |
| `000ae088` | CEGL2_SPRITE::GetMultiTextureHandle() | 8 | 100.0% | auto_structural |
| `000aee5c` | CEGL2_TEX_HYBRID::Register(int) | 8 | 100.0% | auto_structural |
| `000af9e8` | CCAMERA::SetMode(CCAMERA::CAM_MODE) | 8 | 100.0% | auto_structural |
| `000afa18` | CCAMERA::GetDir() const | 8 | 100.0% | auto_structural |
| `000b1acc` | CEGL_PACKET::GetDefaultBlendMode() | 8 | 100.0% | auto_structural |
| `000b1ad4` | CEGL_PACKET::SetDefaultBlendMode(unsigned char) | 8 | 100.0% | auto_structural |
| `000b1adc` | CEGL_PACKET::GetCount() | 8 | 100.0% | auto_structural |
| `000b1bb4` | CEGL_PACKET::GetVBOBuffer() | 8 | 100.0% | auto_structural |
| `000b3540` | CINPUT_DATA::Begin(int) | 8 | 100.0% | auto_structural |
| `000b6c68` | CFILE_DAT::GetOffset(int) | 8 | 100.0% | auto_structural |
| `000b6cd0` | CFILE_DAT::GetSize(int) | 8 | 100.0% | auto_structural |
| `000b8a18` | CLIST::GetCount() | 8 | 100.0% | auto_structural |
| `000b9dd4` | CWORK_MEM::Get() | 8 | 100.0% | auto_structural |
| `000b9df0` | CWORK_MEM::GetAllocSize() | 8 | 100.0% | auto_structural |
| `000b9fc4` | CTHREAD::SetPriority(int) | 8 | 100.0% | auto_structural |
| `000b9fcc` | CTHREAD::Wait() | 8 | 100.0% | auto_structural |
| `000ba39c` | CSOUND_IF::SetEnable(int) | 8 | 100.0% | auto_structural |
| `000bd134` | COggMemMapFile::CallbackClose(void*) | 8 | 100.0% | auto_structural |
| `000bd13c` | COggMemMapFile::CallbackTell(void*) | 8 | 100.0% | auto_structural |
| `000bd144` | CSOUND_LOADER_OGG::IsTerminated() const | 8 | 100.0% | auto_structural |
| `000bd14c` | CSOUND_LOADER_OGG::GetSoundFormat() | 8 | 100.0% | auto_structural |
| `000bd168` | CSOUND_LOADER_OGG::GetSoundEncode() const | 8 | 100.0% | auto_structural |
| `000bd18c` | CSOUND_LOADER_OGG::GetTotal() const | 8 | 100.0% | auto_structural |
| `000bd1b8` | CSOUND_LOADER_OGG::DecodeAll(unsigned char*) | 8 | 100.0% | auto_structural |
| `000bd1c0` | CSOUND_LOADER_OGG::GetLoopIn() const | 8 | 100.0% | auto_structural |
| `000bd520` | CSOUND_LOADER_OGG::IsOpen() const | 8 | 100.0% | auto_structural |
| `000bd528` | COggMemMapFile::GetBuffer() | 8 | 100.0% | auto_structural |
| `000bd530` | COggMemMapFile::GetSize() | 8 | 100.0% | auto_structural |
| `000bd738` | CSOUND_LOADER_OGG::GetPlaySample() | 8 | 100.0% | auto_structural |
| `000bd95c` | CSOUND_LOADER_OGG::GetStreamBuffer() | 8 | 100.0% | auto_structural |
| `000bdb20` | CFRAMERATE::GetSpeed() | 8 | 100.0% | auto_structural |
| `000bdb30` | CFRAMERATE::SetFixedMode(int) | 8 | 100.0% | auto_structural |
| `000c8150` | return_jobdata() | 8 | 100.0% | auto_structural |
| `000cbd6c` | CheckTrapCancelCommandWindow() | 8 | 100.0% | auto_structural |
| `000d9f2c` | attackteam_prewait() | 8 | 100.0% | auto_structural |
| `000da834` | copymat(MATRIX*, MATRIX*) | 8 | 100.0% | auto_structural |
| `000e1110` | check_eventtoolmain(int, int) | 8 | 100.0% | auto_structural |
| `000e8094` | iOS_EventNumberGet() | 8 | 100.0% | auto_structural |
| `00101be8` | Wattackteam_prewait() | 8 | 100.0% | auto_structural |
| `001024fc` | Wcopymat(MATRIX*, MATRIX*) | 8 | 100.0% | auto_structural |
| `00102734` | MESSAGE_getMessageTaskKind() | 8 | 100.0% | auto_structural |
| `001027b4` | Whook_wipe() | 8 | 100.0% | auto_structural |
| `0010fb6c` | Wcheck_eventtoolmain(int, int) | 8 | 100.0% | auto_structural |
| `0015324c` | return_jobdatafromsmall() | 8 | 100.0% | auto_structural |
| `001599a0` | asmGetGP() | 8 | 100.0% | auto_structural |
| `0016f874` | cfileopen(unsigned char*, unsigned int) | 8 | 100.0% | auto_structural |
| `0016f87c` | cfileclose(unsigned int) | 8 | 100.0% | auto_structural |
| `0016f884` | cfilelseek(int, int, int) | 8 | 100.0% | auto_structural |
| `001837a8` | filelseek(int, int, int) | 8 | 100.0% | auto_structural |
| `00183844` | CardLoad(unsigned char*, unsigned char*, unsigned long) | 8 | 100.0% | auto_structural |
| `001d3598` | set_playerwork(PENTRY*, unsigned char*) | 8 | 100.0% | auto_structural |
| `001d63fc` | after_equipchange(BWORK*) | 8 | 100.0% | auto_structural |
| `001e2b70` | check_coord(int, int, int) | 8 | 100.0% | auto_structural |
| `00202fe8` | get_netTrapLocateModeFlg() | 8 | 100.0% | auto_structural |
| `0020594c` | iOS_IsBattleSpeedUp() | 8 | 100.0% | auto_structural |
| `0020dc5c` | checkAnimation(unsigned int) | 8 | 100.0% | auto_structural |
| `0021037c` | setLongVector(VECTOR*, int, int, int) | 8 | 100.0% | auto_structural |
| `00215d60` | StopCallback | 8 | 100.0% | auto_structural |
| `00216274` | checkLoadMusic() | 8 | 100.0% | auto_structural |
| `0021bd18` | s4_killOwnTask(_EffectTCB*) | 8 | 100.0% | auto_structural |
| `00228dc8` | GetShapePrimPtTopOld() | 8 | 100.0% | auto_structural |
| `00241930` | pluge000(short, int, int, int) | 8 | 100.0% | auto_structural |
| `002419c4` | fftCdReset() | 8 | 100.0% | auto_structural |
| `00241a44` | vOpn_arzmes_exit() | 8 | 100.0% | auto_structural |
| `00244410` | rolladr_calc(unsigned long, unsigned long) | 8 | 100.0% | auto_structural |
| `00245524` | movie_loop() | 8 | 100.0% | auto_structural |
| `00245814` | strNextVlc(DECENV*) | 8 | 100.0% | auto_structural |
| `00245a58` | getMoviePlayFlg__Fv() | 8 | 100.0% | auto_structural |
| `00245c04` | o_WaitCardInfo(int, int) | 8 | 100.0% | auto_structural |
| `0026adb0` | snpl_je() | 8 | 100.0% | auto_structural |
| `0026adb8` | snpl_jne() | 8 | 100.0% | auto_structural |
| `0026ae1c` | snpl_jpageflg() | 8 | 100.0% | auto_structural |
| `0026ae24` | snpl_jnpageflg() | 8 | 100.0% | auto_structural |
| `0026ae7c` | snpl_jstatflg() | 8 | 100.0% | auto_structural |
| `0026ae84` | snpl_jnstatflg() | 8 | 100.0% | auto_structural |
| `0026aedc` | snpl_jlocalflg() | 8 | 100.0% | auto_structural |
| `0026aee4` | snpl_jnlocalflg() | 8 | 100.0% | auto_structural |
| `002712a8` | Ssd_AddWaveData(void*) | 8 | 100.0% | auto_structural |
| `002712b8` | Ssd_GetBankWaveSetPtr(short) | 8 | 100.0% | auto_structural |
| `002712d0` | Ssd_GetStereo() | 8 | 100.0% | auto_structural |
| `002712fc` | Ssd_AddMusic(void*) | 8 | 100.0% | auto_structural |
| `0027131c` | Ssd_PlayEffect(long) | 8 | 100.0% | auto_structural |
| `00271424` | Ssd_GetSeqPlayStatus(SsdSeqRec*) | 8 | 100.0% | auto_structural |
| `00279f84` | pspRoutineCheckArithmeticPermission() | 8 | 100.0% | auto_structural |
| `0027b390` | saveVram(char const*) | 8 | 100.0% | auto_structural |
| `00280530` | cSaveFFT::GetMode() | 8 | 100.0% | auto_structural |
| `00280538` | cSaveFFT::SetMode(SAVEFFT) | 8 | 100.0% | auto_structural |
| `002815dc` | test_test_addcolor() | 8 | 100.0% | auto_structural |
| `00284694` | SearchVector(VECTOR_DATABASE*, SVECTOR const*) | 8 | 100.0% | auto_structural |
| `00285f84` | pspFileManager::hockRead(void*, int) | 8 | 100.0% | auto_structural |
| `002868e4` | multwindow_keyright_checkexit() | 8 | 100.0% | auto_structural |
| `00286ac8` | get_netmode() | 8 | 100.0% | auto_structural |
| `00286ad0` | get_netmodeadhoc() | 8 | 100.0% | auto_structural |
| `00286ad8` | get_parent_child() | 8 | 100.0% | auto_structural |
| `00286ae0` | get_main_player() | 8 | 100.0% | auto_structural |
| `00286afc` | get_vsBattle_bule_trap() | 8 | 100.0% | auto_structural |
| `00286b04` | get_vsBattle_bule_arithmetic_select() | 8 | 100.0% | auto_structural |
| `00286b34` | net_send | 8 | 100.0% | auto_structural |
| `00287268` | GetgTrapCancelCount() | 8 | 100.0% | auto_structural |
| `00287270` | GetgTrapCancelResult() | 8 | 100.0% | auto_structural |
| `002884cc` | getNetBattleJudge() | 8 | 100.0% | auto_structural |
| `00288500` | getRewardLv() | 8 | 100.0% | auto_structural |
| `00288514` | getGetItemCount() | 8 | 100.0% | auto_structural |
| `00288570` | Get_AnimList(int) | 8 | 100.0% | auto_structural |
| `0028b418` | ScriptCut__Fiii(int, int, int) | 8 | 100.0% | auto_structural |
| `0028b420` | sceKernelGetGPI() | 8 | 100.0% | auto_structural |
| `0028b428` | sceIoDclose | 8 | 100.0% | auto_structural |
| `0028b430` | sceIoDread | 8 | 100.0% | auto_structural |
| `0028b438` | sceIoDopen | 8 | 100.0% | auto_structural |
| `0028b470` | ResetCallback | 8 | 100.0% | auto_structural |
| `0028b480` | EncSPU | 8 | 100.0% | auto_structural |
| `0028b488` | EncSPU2 | 8 | 100.0% | auto_structural |
| `0028b4a4` | StFreeRing | 8 | 100.0% | auto_structural |
| `0028b4ac` | StGetNext | 8 | 100.0% | auto_structural |
| `0028b4b4` | StGetNextS | 8 | 100.0% | auto_structural |
| `0028b4bc` | StNextStatus | 8 | 100.0% | auto_structural |
| `0028b4d0` | StGetBackloc | 8 | 100.0% | auto_structural |
| `0028b4d8` | StSetChannel | 8 | 100.0% | auto_structural |
| `0028b4e4` | DecDCTvlc | 8 | 100.0% | auto_structural |
| `0028b4f0` | DecDCToutCallback | 8 | 100.0% | auto_structural |
| `0028b4f8` | get_SoundOnly_Flg__Fv() | 8 | 100.0% | auto_structural |
| `0028b500` | set_SoundOnly_Flg__Fi(int) | 8 | 100.0% | auto_structural |
| `0028b520` | getToolBgmFlg__Fv() | 8 | 100.0% | auto_structural |
| `0028b528` | getBgmData__FPUsPUs(unsigned short*, unsigned short*) | 8 | 100.0% | auto_structural |
| `0028b534` | getMovieSkipFlg__Fv() | 8 | 100.0% | auto_structural |
| `0028b544` | CdSearchFile | 8 | 100.0% | auto_structural |
| `0028b54c` | CdComstr | 8 | 100.0% | auto_structural |
| `0028b554` | CdIntstr | 8 | 100.0% | auto_structural |
| `0028b55c` | CdGetSector | 8 | 100.0% | auto_structural |
| `0028b564` | CdGetSector2 | 8 | 100.0% | auto_structural |
| `0028b56c` | CdDataSync | 8 | 100.0% | auto_structural |
| `0028b574` | CdGetToc | 8 | 100.0% | auto_structural |
| `0028b57c` | CdPlay | 8 | 100.0% | auto_structural |
| `0028b584` | CdMix | 8 | 100.0% | auto_structural |
| `0028b58c` | CdRead2 | 8 | 100.0% | auto_structural |
| `0028b594` | CdReadFile | 8 | 100.0% | auto_structural |
| `0028b59c` | CdReadSync | 8 | 100.0% | auto_structural |
| `0028b5a4` | CdReady | 8 | 100.0% | auto_structural |
| `0028b5ac` | CdSetDebug | 8 | 100.0% | auto_structural |
| `0028b5b4` | CdReadCallback | 8 | 100.0% | auto_structural |
| `0028b5bc` | CdReadyCallback | 8 | 100.0% | auto_structural |
| `0028b5c4` | CdSyncCallback | 8 | 100.0% | auto_structural |
| `0028b5cc` | CdReset | 8 | 100.0% | auto_structural |
| `0028b5d4` | CdStatus | 8 | 100.0% | auto_structural |
| `0028b5dc` | CdLastCom | 8 | 100.0% | auto_structural |
| `0028b5e4` | CdLastPos | 8 | 100.0% | auto_structural |
| `0028b5ec` | CdMode | 8 | 100.0% | auto_structural |
| `0028b5f4` | CdDiskReady | 8 | 100.0% | auto_structural |
| `0028b5fc` | CdGetDiskType | 8 | 100.0% | auto_structural |
| `0028b604` | CdReadExec | 8 | 100.0% | auto_structural |
| `0028b630` | exitXpHeap() | 8 | 100.0% | auto_structural |
| `0028b6f4` | _FFT_Main() | 8 | 100.0% | auto_structural |
| `0028c238` | CFFT_STATE::GetCaptureRequest() | 8 | 100.0% | auto_structural |
| `0028c248` | CFFT_STATE::GetCaptureDraw() | 8 | 100.0% | auto_structural |
| `0028c258` | CFFT_STATE::GetEncountRequest() | 8 | 100.0% | auto_structural |
| `0028c270` | CFFT_STATE::SetMode(int) | 8 | 100.0% | auto_structural |
| `0028c280` | CFFT_STATE::SetDebugMode(int) | 8 | 100.0% | auto_structural |
| `0028c2e0` | CFFT_STATE::SetMoviePlaying(int) | 8 | 100.0% | auto_structural |
| `0028c308` | CFFT_STATE::SetSettingsEnable(int) | 8 | 100.0% | auto_structural |
| `0028c318` | CFFT_STATE::SetLinkEnable(int) | 8 | 100.0% | auto_structural |
| `0028ce40` | CAUTOSAVE::GetHeapOffset() | 8 | 100.0% | auto_structural |
| `0028ce78` | ReadTMD | 8 | 100.0% | auto_structural |
| `0028ce80` | CheckPrim | 8 | 100.0% | auto_structural |
| `0028ce88` | GetGraphDebug | 8 | 100.0% | auto_structural |
| `0028ce90` | GetTimSize | 8 | 100.0% | auto_structural |
| `0028ce98` | IsEndPrim | 8 | 100.0% | auto_structural |
| `0028cea0` | KanjiFntOpen | 8 | 100.0% | auto_structural |
| `0028ceac` | Krom2Tim | 8 | 100.0% | auto_structural |
| `0028ceb4` | MargePrim | 8 | 100.0% | auto_structural |
| `0028cebc` | OpenTMD | 8 | 100.0% | auto_structural |
| `0028cec4` | SetGraphDebug | 8 | 100.0% | auto_structural |
| `0028cecc` | KanjiFntFlush | 8 | 100.0% | auto_structural |
| `0028ced4` | NextPrim | 8 | 100.0% | auto_structural |
| `0028cf04` | BreakDraw | 8 | 100.0% | auto_structural |
| `0028cf10` | IsIdleGPU | 8 | 100.0% | auto_structural |
| `0028cf18` | GetODE | 8 | 100.0% | auto_structural |
| `0028cf20` | DrawOTag2 | 8 | 100.0% | auto_structural |
| `0028d434` | tlMalloc(unsigned int) | 8 | 100.0% | auto_structural |
| `0028de74` | _card_load | 8 | 100.0% | auto_structural |
| `0028de7c` | _card_read | 8 | 100.0% | auto_structural |
| `0028de84` | _card_status | 8 | 100.0% | auto_structural |
| `0028de8c` | firstfile(char const*, DIRENTRY*) | 8 | 100.0% | auto_structural |
| `0028de94` | nextfile(DIRENTRY*) | 8 | 100.0% | auto_structural |
| `0028e2dc` | CdInit | 8 | 100.0% | auto_structural |
| `0028e468` | CdControlF | 8 | 100.0% | auto_structural |
| `0028e4b8` | CdSync | 8 | 100.0% | auto_structural |
| `00290e88` | FntOpen | 8 | 100.0% | auto_structural |
| `00290e94` | FntPrint | 8 | 100.0% | auto_structural |
| `00290e9c` | FntFlush | 8 | 100.0% | auto_structural |
| `0029ac18` | GetGraphType | 8 | 100.0% | auto_structural |
| `0029b6fc` | GsDrawOt | 8 | 100.0% | auto_structural |
| `002a0808` | MulMatrix | 8 | 100.0% | auto_structural |
| `002a0810` | MulMatrix2 | 8 | 100.0% | auto_structural |
| `002a26c0` | PadGetState | 8 | 100.0% | auto_structural |
| `002a3114` | xpMallocErrorFuncSet | 8 | 100.0% | auto_structural |
| `002a314c` | pspSaveBase::Exit() | 8 | 100.0% | auto_structural |
| `002ab9e0` | sceGuSync | 8 | 100.0% | auto_structural |
| `002b0508` | CAPP_INFO::GetStoragePath() | 8 | 100.0% | auto_structural |
| `002b3444` | iCloud_Send() | 8 | 100.0% | auto_structural |
| `002b344c` | iCloud_Receive() | 8 | 100.0% | auto_structural |
| `002b3454` | iCloud_GetSlotCount() | 8 | 100.0% | auto_structural |
| `002b36d4` | Error_FrameMove() | 8 | 100.0% | auto_structural |
| `002b7a2c` | GetPanelCursorMode() | 8 | 100.0% | auto_structural |
| `002c9121` | operator delete[](void*) | 8 | 0.0% | needs_review |
| `002cce38` | _Unwind_GetCFA | 8 | 100.0% | auto_structural |
| `002cd57c` | __aeabi_unwind_cpp_pr0 | 8 | 100.0% | auto_structural |
| `002cd584` | __aeabi_unwind_cpp_pr1 | 8 | 100.0% | auto_structural |
| `002cd58c` | __aeabi_unwind_cpp_pr2 | 8 | 100.0% | auto_structural |
| `002cdf08` | _Unwind_GetDataRelBase | 8 | 100.0% | auto_structural |
| `002cdf10` | _Unwind_GetTextRelBase | 8 | 100.0% | auto_structural |
| `00077494` | gztell | 4 | 100.0% | auto_structural |
| `000774fc` | gzoffset | 4 | 100.0% | auto_structural |
| `00077dc8` | gzseek | 4 | 100.0% | auto_structural |
| `000785e4` | gzgetc_ | 4 | 100.0% | auto_structural |
| `0007f384` | _tr_flush_bits | 4 | 100.0% | auto_structural |
| `0008244c` | oggpackB_writeinit | 4 | 100.0% | auto_structural |
| `00082478` | oggpackB_writecheck | 4 | 100.0% | auto_structural |
| `00082548` | oggpackB_reset | 4 | 100.0% | auto_structural |
| `00082a14` | oggpackB_writeclear | 4 | 100.0% | auto_structural |
| `00082a44` | oggpackB_readinit | 4 | 100.0% | auto_structural |
| `00082ca8` | oggpackB_adv | 4 | 100.0% | auto_structural |
| `00082cdc` | oggpackB_adv1 | 4 | 100.0% | auto_structural |
| `00083004` | oggpackB_bytes | 4 | 100.0% | auto_structural |
| `00083008` | oggpackB_bits | 4 | 100.0% | auto_structural |
| `00083014` | oggpackB_get_buffer | 4 | 100.0% | auto_structural |
| `000af9bc` | CCAMERA::Uninit() | 4 | 100.0% | auto_structural |
| `000b5ac8` | CUI_SCROLLBAR::Delete() | 4 | 100.0% | auto_structural |
| `000b61d4` | CCOMP_Z_DEC::~CCOMP_Z_DEC() | 4 | 100.0% | auto_structural |
| `000b6200` | CCOMP_Z_DEC::Error(char const*) | 4 | 100.0% | auto_structural |
| `000b63a0` | CCOMP_Z_ENC::~CCOMP_Z_ENC() | 4 | 100.0% | auto_structural |
| `000b63cc` | CCOMP_Z_ENC::Error(char const*) | 4 | 100.0% | auto_structural |
| `000b6580` | CCRYPT::CCRYPT() | 4 | 100.0% | auto_structural |
| `000b6584` | CCRYPT::~CCRYPT() | 4 | 100.0% | auto_structural |
| `000b661c` | CCRYPT::Decrypt(unsigned char*, int, unsigned int) | 4 | 100.0% | auto_structural |
| `000b8bdc` | CSTR_UTIL::CSTR_UTIL() | 4 | 100.0% | auto_structural |
| `000ba090` | SleepM(unsigned int) | 4 | 100.0% | auto_structural |
| `000bb834` | CSOUND_IF_SL::FrameMove(int, float) | 4 | 100.0% | auto_structural |
| `000bcbf0` | CSOUND_LOADER::FrameMove(int, float) | 4 | 100.0% | auto_structural |
| `000be41c` | CSTEP_BATCH::GetData() | 4 | 100.0% | auto_structural |
| `000c4418` | Adisp_floateventwindow() | 4 | 100.0% | auto_structural |
| `000c4498` | attackdebugfunc() | 4 | 100.0% | auto_structural |
| `000cbd50` | SetTrapNameWindowParam(int, short, int) | 4 | 100.0% | auto_structural |
| `000cbd54` | TrapNameWindowManager() | 4 | 100.0% | auto_structural |
| `000cbd58` | CreateTrapNameWindowManagerTask() | 4 | 100.0% | auto_structural |
| `000cbd5c` | deleteEndModeWindow() | 4 | 100.0% | auto_structural |
| `000cbd60` | SetTrapNameWindowColor(int) | 4 | 100.0% | auto_structural |
| `000cbd64` | CreateTrapCancelCommandWindow() | 4 | 100.0% | auto_structural |
| `000cbd68` | DeleteTrapCancelCommandWindow() | 4 | 100.0% | auto_structural |
| `000cbd74` | CreateNetStayWindow() | 4 | 100.0% | auto_structural |
| `000d0dc8` | Ddisp_floateventwindow() | 4 | 100.0% | auto_structural |
| `000d8970` | dispemptywindow() | 4 | 100.0% | auto_structural |
| `000d8974` | send_statuschrno(int) | 4 | 100.0% | auto_structural |
| `000d8bfc` | initstatuscphase() | 4 | 100.0% | auto_structural |
| `000d9a08` | hook_disp_requirement() | 4 | 100.0% | auto_structural |
| `000d9a0c` | hook_trophics() | 4 | 100.0% | auto_structural |
| `000d9a10` | seekpcfile(char*, char*, int, int) | 4 | 100.0% | auto_structural |
| `000d9ac0` | loadonefile(char*, char*) | 4 | 100.0% | auto_structural |
| `000e62c4` | DEBUGTRACE_hook_connect_camera() | 4 | 100.0% | auto_structural |
| `000e62c8` | DEBUG_CHK_ROLL(SCROLLRECORD*) | 4 | 100.0% | auto_structural |
| `000e7f0c` | dmp_tuto(unsigned char*, int) | 4 | 100.0% | auto_structural |
| `000feaa4` | WiOS_chkallocatewindowinit() | 4 | 100.0% | auto_structural |
| `00100640` | Wdispemptywindow() | 4 | 100.0% | auto_structural |
| `00100644` | Wsend_statuschrno(int) | 4 | 100.0% | auto_structural |
| `00100840` | Winitstatuscphase() | 4 | 100.0% | auto_structural |
| `00101908` | Whook_disp_requirement() | 4 | 100.0% | auto_structural |
| `0010190c` | Whook_trophics() | 4 | 100.0% | auto_structural |
| `00101910` | Wseekpcfile(char*, char*, int, int) | 4 | 100.0% | auto_structural |
| `001019bc` | Wloadonefile(char*, char*) | 4 | 100.0% | auto_structural |
| `001019c0` | LOAD_seekeventfile(int) | 4 | 100.0% | auto_structural |
| `00102128` | Wevent_init_light() | 4 | 100.0% | auto_structural |
| `00121718` | Edisp_floateventwindow() | 4 | 100.0% | auto_structural |
| `0012b108` | disp_floateventwindow() | 4 | 100.0% | auto_structural |
| `00137b0c` | value_input() | 4 | 100.0% | auto_structural |
| `0014b9f8` | Cdisp_floateventwindow() | 4 | 100.0% | auto_structural |
| `0014e0e4` | iOSSetjoinus() | 4 | 100.0% | auto_structural |
| `0014e0e8` | statushookfunc() | 4 | 100.0% | auto_structural |
| `0014e9a0` | sol_draw(int, int, int) | 4 | 100.0% | auto_structural |
| `00155708` | story_faceload() | 4 | 100.0% | auto_structural |
| `0015991c` | asmBoxCopy(char*, char*, COPYFIELD*, COPYFIELD*) | 4 | 100.0% | auto_structural |
| `00159920` | asmKanjiCopy(char*, char*, COPYFIELD*, int) | 4 | 100.0% | auto_structural |
| `00159a70` | asmMUL64(long, long, long) | 4 | 100.0% | auto_structural |
| `00159a74` | asmMUL3232(long, long, long, long) | 4 | 100.0% | auto_structural |
| `0015a480` | iOSSoundSESet(int) | 4 | 100.0% | auto_structural |
| `0015d2a8` | iOSexecuteTurn() | 4 | 100.0% | auto_structural |
| `00161d98` | tDebugBreakCheck(int) | 4 | 100.0% | auto_structural |
| `00161d9c` | tDebugBreakTime(int) | 4 | 100.0% | auto_structural |
| `00161da0` | tDebugPointerErr() | 4 | 100.0% | auto_structural |
| `00161ef0` | wasmBoxCopy(char*, char*, COPYFIELD*, COPYFIELD*) | 4 | 100.0% | auto_structural |
| `00161ef4` | wasmKanjiCopy(char*, char*, COPYFIELD*, int) | 4 | 100.0% | auto_structural |
| `00162044` | wasmMUL64(long, long, long) | 4 | 100.0% | auto_structural |
| `00162048` | wasmMUL3232(long, long, long, long) | 4 | 100.0% | auto_structural |
| `00176b7c` | iOSBwork2ChrStts(BWORK*, CHR_STTS*, int) | 4 | 100.0% | auto_structural |
| `001836cc` | iOS_addPrim_window(tagPOLY_FT4*) | 4 | 100.0% | auto_structural |
| `0019e7b4` | shop_dummyfunc() | 4 | 100.0% | auto_structural |
| `001a6378` | iOS_resetCancelDisableAreaForStatusWindow() | 4 | 100.0% | auto_structural |
| `001a652c` | GetMessagePtr(int) | 4 | 100.0% | auto_structural |
| `001add64` | unit_dummyfunc() | 4 | 100.0% | auto_structural |
| `001b7ef0` | CallresetFFT() | 4 | 100.0% | auto_structural |
| `001d114c` | set_monomane_direction(BWORK*, unsigned char) | 4 | 100.0% | auto_structural |
| `001dca54` | callSW(int) | 4 | 100.0% | auto_structural |
| `001f01a8` | resetActionAnimation(tag_animation*) | 4 | 100.0% | auto_structural |
| `0020c258` | fftDrawSyncCallback() | 4 | 100.0% | auto_structural |
| `0020c25c` | fftCdReadyCallback() | 4 | 100.0% | auto_structural |
| `0020c260` | fftCdReadCallback() | 4 | 100.0% | auto_structural |
| `0020c5cc` | myPollhost() | 4 | 100.0% | auto_structural |
| `0020c5d0` | system_error(int, int) | 4 | 100.0% | auto_structural |
| `0020c5d4` | system_warning(int, int) | 4 | 100.0% | auto_structural |
| `0020ce14` | fileAllocateCD(unsigned long, unsigned long) | 4 | 100.0% | auto_structural |
| `0020ce18` | fileDispose(char*) | 4 | 100.0% | auto_structural |
| `0020f424` | eventEffectStart() | 4 | 100.0% | auto_structural |
| `0020f4f8` | getCharPrimList(short, Point*, unsigned long*) | 4 | 100.0% | auto_structural |
| `00215d20` | fadeGradation(int, CVECTOR*) | 4 | 100.0% | auto_structural |
| `00215d24` | fadeAnbient(int, CVECTOR*) | 4 | 100.0% | auto_structural |
| `00215d28` | fadeFlatColor(int, CVECTOR*) | 4 | 100.0% | auto_structural |
| `00215d5c` | PadStop | 4 | 100.0% | auto_structural |
| `00215db4` | resetFFT() | 4 | 100.0% | auto_structural |
| `0021610c` | iOS_rand() | 4 | 100.0% | auto_structural |
| `00216818` | stopZingle(int) | 4 | 100.0% | auto_structural |
| `0021681c` | controlZingle() | 4 | 100.0% | auto_structural |
| `002168e0` | callSystemSound(int) | 4 | 100.0% | auto_structural |
| `002168e4` | callSoundEffect(int) | 4 | 100.0% | auto_structural |
| `002168fc` | recallEnvEffect() | 4 | 100.0% | auto_structural |
| `002169cc` | pauseEnvEffect() | 4 | 100.0% | auto_structural |
| `0021ebb0` | error(char, long) | 4 | 100.0% | auto_structural |
| `00225310` | iOS_CheckPEffect(char const*, int) | 4 | 100.0% | auto_structural |
| `00225a60` | objectLG2(_EffectTCB*, _Object*) | 4 | 100.0% | auto_structural |
| `00225a64` | dmyFnc2(_EffectTCB*, _Object*) | 4 | 100.0% | auto_structural |
| `0022a614` | DumpMemory(int, void*) | 4 | 100.0% | auto_structural |
| `002419cc` | fftCdLoop(CDREC*) | 4 | 100.0% | auto_structural |
| `002419d0` | fftCdCancel(CDREC*) | 4 | 100.0% | auto_structural |
| `00248ccc` | ctlcard_init() | 4 | 100.0% | auto_structural |
| `00258ac4` | evt_skip0() | 4 | 100.0% | auto_structural |
| `0025f354` | wld_btlsect_seek() | 4 | 100.0% | auto_structural |
| `00267f38` | wldrute_init() | 4 | 100.0% | auto_structural |
| `0026b374` | sound_request(int) | 4 | 100.0% | auto_structural |
| `0026c058` | iOS_debugDispTownCircle(int, int) | 4 | 100.0% | auto_structural |
| `0026ff2c` | effectdmy() | 4 | 100.0% | auto_structural |
| `0027129c` | Ssd_Quit() | 4 | 100.0% | auto_structural |
| `002712a0` | Ssd_Enable() | 4 | 100.0% | auto_structural |
| `002712a4` | Ssd_Disable() | 4 | 100.0% | auto_structural |
| `002712b0` | Ssd_DisposeNormalWave() | 4 | 100.0% | auto_structural |
| `002712b4` | Ssd_DisposeWaveData(SsdWaveSetRec*) | 4 | 100.0% | auto_structural |
| `002712c0` | Ssd_AddEffectData(void*) | 4 | 100.0% | auto_structural |
| `002712c4` | Ssd_DisposeEffectData(void*) | 4 | 100.0% | auto_structural |
| `002712c8` | Ssd_AllStop() | 4 | 100.0% | auto_structural |
| `002712ec` | Ssd_CheckWideMode() | 4 | 100.0% | auto_structural |
| `002712f4` | Ssd_ErrorProc(int) | 4 | 100.0% | auto_structural |
| `002712f8` | Ssd_AddVagPackData(void*) | 4 | 100.0% | auto_structural |
| `00271304` | Ssd_DisposeMusic(SsdSeqRec*) | 4 | 100.0% | auto_structural |
| `00271308` | Ssd_LinkMusicData(SsdSeqRec*, void*) | 4 | 100.0% | auto_structural |
| `0027130c` | Ssd_StartMusic(SsdSeqRec*, short, short) | 4 | 100.0% | auto_structural |
| `00271310` | Ssd_StopMusic(SsdSeqRec*) | 4 | 100.0% | auto_structural |
| `00271314` | Ssd_PlaySysEffect(long) | 4 | 100.0% | auto_structural |
| `00271318` | Ssd_PlayEnvEffect(long) | 4 | 100.0% | auto_structural |
| `00271340` | Ssd_PlayEffects03(long, long, long, long) | 4 | 100.0% | auto_structural |
| `00271344` | Ssd_StopAllEffect() | 4 | 100.0% | auto_structural |
| `00271348` | Ssd_StopEffectSet(void*) | 4 | 100.0% | auto_structural |
| `00271410` | Ssd_InitEffectTrackRecWithStart(short, long, short, short) | 4 | 100.0% | auto_structural |
| `0027b398` | numa_fileAllocateCD(unsigned long, unsigned long) | 4 | 100.0% | auto_structural |
| `0027b39c` | numa_fileReadCD(unsigned long, unsigned long, void*) | 4 | 100.0% | auto_structural |
| `0027b3a0` | numa_fileReadRequest(unsigned int, unsigned int, char*) | 4 | 100.0% | auto_structural |
| `0027b510` | dispCmdKind() | 4 | 100.0% | auto_structural |
| `0027b5c8` | rprintfr(RECT16*, int, int, int) | 4 | 100.0% | auto_structural |
| `0027b670` | iOS_DEBUG_multiwindow_break_hook(unsigned long*) | 4 | 100.0% | auto_structural |
| `0027b674` | iOS_DEBUG_multiwindow_break_hook2(unsigned long*, int) | 4 | 100.0% | auto_structural |
| `0027b678` | iOS_DEBUG_multiwindow_keyright_hook() | 4 | 100.0% | auto_structural |
| `0027fc28` | chk_ucResumeData2(int) | 4 | 100.0% | auto_structural |
| `0027fc2c` | chk_ucResumeData(unsigned char*, int) | 4 | 100.0% | auto_structural |
| `0027fc78` | initSaveFFT(char*, char*, bool) | 4 | 100.0% | auto_structural |
| `0027fc7c` | cSaveFFT::~cSaveFFT() | 4 | 100.0% | auto_structural |
| `00280610` | iOS_soundDirect(int) | 4 | 100.0% | auto_structural |
| `00280670` | hook_write_eventflag(int, int) | 4 | 100.0% | auto_structural |
| `00280678` | hook_Debug(char const*) | 4 | 100.0% | auto_structural |
| `0028067c` | hook_Debug2(char const*) | 4 | 100.0% | auto_structural |
| `00280680` | hook_NextEventSet() | 4 | 100.0% | auto_structural |
| `00280684` | hook_musiclod() | 4 | 100.0% | auto_structural |
| `002806bc` | hook_read_eventflag(int*) | 4 | 100.0% | auto_structural |
| `002806c0` | hook_allocate_texture() | 4 | 100.0% | auto_structural |
| `002806c4` | hook_opt() | 4 | 100.0% | auto_structural |
| `002806c8` | hook_chk_speedup(int) | 4 | 100.0% | auto_structural |
| `00280708` | hook_pad() | 4 | 100.0% | auto_structural |
| `0028070c` | hook_pad2() | 4 | 100.0% | auto_structural |
| `00280710` | hook_drive_connect_chrmove() | 4 | 100.0% | auto_structural |
| `00280714` | hook_drive_connect_chrmove2(int) | 4 | 100.0% | auto_structural |
| `002807f4` | hook_cliptest() | 4 | 100.0% | auto_structural |
| `002807f8` | chk_RefLine(int) | 4 | 100.0% | auto_structural |
| `002807fc` | hook_drive_chr(int) | 4 | 100.0% | auto_structural |
| `00280800` | hook_fix_bugno_931(int) | 4 | 100.0% | auto_structural |
| `00280804` | hook_win_tail() | 4 | 100.0% | auto_structural |
| `00280808` | hook_allSkipTest() | 4 | 100.0% | auto_structural |
| `002815d8` | hook_num(int, int, int) | 4 | 100.0% | auto_structural |
| `002815e4` | chk_test_addcolor(unsigned int*) | 4 | 100.0% | auto_structural |
| `00281640` | hook_disp_plateorspell(int*) | 4 | 100.0% | auto_structural |
| `00281644` | hook_code_soundeffect(int) | 4 | 100.0% | auto_structural |
| `00281648` | hook_1284(char*, int) | 4 | 100.0% | auto_structural |
| `00286124` | SetSpadStack(unsigned long) | 4 | 100.0% | auto_structural |
| `00286128` | ResetSpadStack() | 4 | 100.0% | auto_structural |
| `00286744` | rsetmovie_title_flg__Fv() | 4 | 100.0% | auto_structural |
| `00286748` | setmovie_title_flg__Fv() | 4 | 100.0% | auto_structural |
| `002869f0` | _pspNetRand(char const*, int) | 4 | 100.0% | auto_structural |
| `00286a94` | timer_print_screen() | 4 | 100.0% | auto_structural |
| `00286a98` | val_letter(int, int, int) | 4 | 100.0% | auto_structural |
| `00286a9c` | set_nettimer_flag(int, int) | 4 | 100.0% | auto_structural |
| `00286ae8` | net_control_ex(void*, void*, int) | 4 | 100.0% | auto_structural |
| `00286e90` | rivalCameraWorkProcs() | 4 | 100.0% | auto_structural |
| `00286ec4` | check_rival_value(int) | 4 | 100.0% | auto_structural |
| `00287584` | load_iconpackdata() | 4 | 100.0% | auto_structural |
| `002875a0` | draw_maru(unsigned long*) | 4 | 100.0% | auto_structural |
| `002875a4` | draw_batu(unsigned long*) | 4 | 100.0% | auto_structural |
| `00287a14` | Red_Blue_Draw(int) | 4 | 100.0% | auto_structural |
| `00288498` | Draw_TuusinIcon(int, int, unsigned long*) | 4 | 100.0% | auto_structural |
| `0028849c` | Draw_Trap_CancelCommandList(int*, int, int, unsigned long*) | 4 | 100.0% | auto_structural |
| `002884c8` | NetBattleJudge() | 4 | 100.0% | auto_structural |
| `002884fc` | setRewardLv(int) | 4 | 100.0% | auto_structural |
| `00288508` | CalcRewardLv() | 4 | 100.0% | auto_structural |
| `0028850c` | CalcMissionPayPoint(int) | 4 | 100.0% | auto_structural |
| `00288510` | Final_CalcMissionPayPoint() | 4 | 100.0% | auto_structural |
| `0028856c` | init_AnimList() | 4 | 100.0% | auto_structural |
| `0028b460` | SpuInit | 4 | 100.0% | auto_structural |
| `0028b464` | SpuInitHot | 4 | 100.0% | auto_structural |
| `0028b468` | SpuQuit | 4 | 100.0% | auto_structural |
| `0028b46c` | SetMem | 4 | 100.0% | auto_structural |
| `0028b490` | StSetRing | 4 | 100.0% | auto_structural |
| `0028b494` | StClearRing | 4 | 100.0% | auto_structural |
| `0028b498` | StUnSetRing | 4 | 100.0% | auto_structural |
| `0028b49c` | StSetStream | 4 | 100.0% | auto_structural |
| `0028b4a0` | StSetEmulate | 4 | 100.0% | auto_structural |
| `0028b4c4` | StRingStatus | 4 | 100.0% | auto_structural |
| `0028b4c8` | StSetMask | 4 | 100.0% | auto_structural |
| `0028b4cc` | StCdInterrupt | 4 | 100.0% | auto_structural |
| `0028b4e0` | DecDCTReset | 4 | 100.0% | auto_structural |
| `0028b4ec` | DecDCTout | 4 | 100.0% | auto_structural |
| `0028b508` | pspMovieEnd__Fv() | 4 | 100.0% | auto_structural |
| `0028b50c` | pspMovieInit__FiPCciiii(int, char*, int, int, int, int) | 4 | 100.0% | auto_structural |
| `0028b510` | pspMoviePlay__Fv() | 4 | 100.0% | auto_structural |
| `0028b514` | pspMovieStart__Fv() | 4 | 100.0% | auto_structural |
| `0028b518` | setMoviePlayFlg__Fi(int) | 4 | 100.0% | auto_structural |
| `0028b51c` | setMovieSkipFlg__Fi(int) | 4 | 100.0% | auto_structural |
| `0028b530` | setToolBgmFlg__Fi(int) | 4 | 100.0% | auto_structural |
| `0028b53c` | setBgmData__Fii(int, int) | 4 | 100.0% | auto_structural |
| `0028b540` | CdFlush | 4 | 100.0% | auto_structural |
| `0028b60c` | CdReadBreak | 4 | 100.0% | auto_structural |
| `0028c7e8` | CAUTOSAVE::~CAUTOSAVE() | 4 | 100.0% | auto_structural |
| `0028ce54` | asmmemcpy(void*, void const*, unsigned int) | 4 | 100.0% | auto_structural |
| `0028cea8` | KanjiFntClose | 4 | 100.0% | auto_structural |
| `0028cedc` | CatPrim | 4 | 100.0% | auto_structural |
| `0028cee0` | DrawOTagIO | 4 | 100.0% | auto_structural |
| `0028cee4` | DrawOTagEnv | 4 | 100.0% | auto_structural |
| `0028cee8` | DumpClut | 4 | 100.0% | auto_structural |
| `0028ceec` | DumpDispEnv | 4 | 100.0% | auto_structural |
| `0028cef0` | DumpDrawEnv | 4 | 100.0% | auto_structural |
| `0028cef4` | DumpOTag | 4 | 100.0% | auto_structural |
| `0028cef8` | DumpTPage | 4 | 100.0% | auto_structural |
| `0028cefc` | SetDumpFnt | 4 | 100.0% | auto_structural |
| `0028cf00` | TermPrim | 4 | 100.0% | auto_structural |
| `0028cf0c` | ContinueDraw | 4 | 100.0% | auto_structural |
| `0028cf28` | GetDrawMode | 4 | 100.0% | auto_structural |
| `0028cf2c` | GetTexWindow | 4 | 100.0% | auto_structural |
| `0028cf30` | GetDrawArea | 4 | 100.0% | auto_structural |
| `0028cf34` | GetDrawOffset | 4 | 100.0% | auto_structural |
| `0028cf38` | GetDrawEnv2 | 4 | 100.0% | auto_structural |
| `0028de70` | _bu_init | 4 | 100.0% | auto_structural |
| `0028e464` | CdControlB | 4 | 100.0% | auto_structural |
| `0028e5c0` | VSync | 4 | 100.0% | auto_structural |
| `00290e90` | FntLoad | 4 | 100.0% | auto_structural |
| `0029b3ec` | GsInit3D | 4 | 100.0% | auto_structural |
| `0029b428` | GsGetActiveBuff | 4 | 100.0% | auto_structural |
| `0029ff94` | SquareRoot12 | 4 | 100.0% | auto_structural |
| `002a0818` | SetRotMatrix | 4 | 100.0% | auto_structural |
| `002a0d10` | SetTransMatrix | 4 | 100.0% | auto_structural |
| `002a1024` | OuterProduct12 | 4 | 100.0% | auto_structural |
| `002a1038` | CompMatrixLV | 4 | 100.0% | auto_structural |
| `002a1268` | TransRotPers | 4 | 100.0% | auto_structural |
| `002a1438` | SetFarColor | 4 | 100.0% | auto_structural |
| `002a143c` | SetBackColor | 4 | 100.0% | auto_structural |
| `002a2ff4` | InitHeap(unsigned long*, unsigned long) | 4 | 100.0% | auto_structural |
| `002a3110` | xpMallocSizeGet | 4 | 100.0% | auto_structural |
| `002a311c` | xpGetHeap | 4 | 100.0% | auto_structural |
| `002a3134` | xpMoveHeap | 4 | 100.0% | auto_structural |
| `002ab710` | sceGuClearColor | 4 | 100.0% | auto_structural |
| `002ab714` | sceGuClear | 4 | 100.0% | auto_structural |
| `002ab888` | sceGuAlphaFunc | 4 | 100.0% | auto_structural |
| `002ab900` | sceGuColorFunc | 4 | 100.0% | auto_structural |
| `002ab904` | sceGuDisplay | 4 | 100.0% | auto_structural |
| `002abc88` | sceGuShadeModel | 4 | 100.0% | auto_structural |
| `002abd1c` | sceGuTexFunc | 4 | 100.0% | auto_structural |
| `002acb28` | sceGuViewport | 4 | 100.0% | auto_structural |
| `002b06b0` | CAPP_INFO::Get() | 4 | 100.0% | auto_structural |
| `002b1f38` | NowLoading_FrameRender() | 4 | 100.0% | auto_structural |
| `002b3440` | Achievement_Unlock(int) | 4 | 100.0% | auto_structural |
| `002b36b8` | Boot_Uninit() | 4 | 100.0% | auto_structural |
| `002b3758` | Error_Uninit() | 4 | 100.0% | auto_structural |
| `002b5590` | Link_Suspend() | 4 | 100.0% | auto_structural |
| `002b5594` | Link_Resume() | 4 | 100.0% | auto_structural |
| `002b5eac` | Logo_Suspend() | 4 | 100.0% | auto_structural |
| `002b5eb0` | Logo_Resume() | 4 | 100.0% | auto_structural |
| `002b6bcc` | Main_Resume() | 4 | 100.0% | auto_structural |
| `002c54ac` | Movie_Uninit() | 4 | 100.0% | auto_structural |
| `002ccf94` | _Unwind_Complete | 4 | 100.0% | auto_structural |
