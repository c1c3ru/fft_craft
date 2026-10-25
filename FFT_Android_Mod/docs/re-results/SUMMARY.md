# Parallel reverse-engineering loop

Binary SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Analyzed in current binary: 836
Automatically triaged: 122,284 bytes / 1,837,392 inventory bytes (6.66%); **this is newly triaged coverage, not total project coverage**.

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
| `0025f44c` | frmbuf_get() | 496 | 91.13% | needs_review |
| `0027070c` | pagewinmes_put(PAGEWININFO*, int) | 496 | 95.16% | auto_structural |
| `0028d498` | tlFree(void*) | 496 | 95.97% | auto_structural |
| `0015ad38` | iOSexecuteCurSlide() | 492 | 93.5% | needs_review |
| `00280108` | cSaveFFT::Execute() | 488 | 98.36% | auto_structural |
| `0028d24c` | tlMallocAlign(unsigned int, unsigned int) | 488 | 96.72% | auto_structural |
| `000bbc4c` | CSOUND_IF_SL::Static_CreatePlayer(int, int, int) | 484 | 95.04% | auto_structural |
| `001569ac` | editdirect() | 484 | 91.74% | needs_review |
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
| `001022ec` | Wtutorial_hookfunc() | 464 | 88.79% | needs_review |
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
| `001b8c38` | sort_init() | 452 | 87.61% | needs_review |
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
| `00267ad0` | ctlret_main(CTLINFO*) | 420 | 92.38% | needs_review |
| `00274018` | ForChantedAction() | 420 | 98.1% | auto_structural |
| `0015a988` | sBattleTouchRotationMain() | 416 | 94.23% | needs_review |
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
| `00285f8c` | hockRead(void*, int, unsigned int) | 408 | 83.33% | needs_review |
| `002cb538` | __mulsf3 | 408 | 100.0% | auto_structural |
| `000e1118` | bgput(tagPOLY_FT4*, RECT16*, RECT16*, BGRECORD*) | 404 | 100.0% | auto_structural |
| `0010fb74` | Wbgput(tagPOLY_FT4*, RECT16*, RECT16*, BGRECORD*) | 404 | 100.0% | auto_structural |
| `00159aac` | asm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 404 | 80.2% | needs_review |
| `0015e5d4` | iOSShiftUnitGet() | 404 | 92.08% | needs_review |
| `00162080` | wasm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 404 | 80.2% | needs_review |
| `00266a00` | infonumber_put_zero(int, int, GsSPRITE*, GsOT*, int) | 404 | 98.02% | auto_structural |
| `00280304` | Savedata_LoadGameCleared(unsigned char*, int*) | 404 | 95.05% | auto_structural |
| `00284144` | mapclip_load(int) | 404 | 100.0% | auto_structural |
| `002cb2f0` | __subsf3 | 404 | 100.0% | auto_structural |
| `00078d9c` | gzwrite | 400 | 99.0% | auto_structural |
| `000bad78` | CSOUND_IF::Play(int, int, int, int, unsigned char) | 400 | 99.0% | auto_structural |
| `002595c0` | ctlhistory_init() | 400 | 90.0% | needs_review |
| `002b1600` | GX_Init(int) | 400 | 91.0% | needs_review |
| `002cb2f4` | __addsf3 | 400 | 100.0% | auto_structural |
| `0010d8ec` | Wevent_init() | 396 | 96.97% | auto_structural |
| `001d7538` | get_command_ability(int, int) | 396 | 96.97% | auto_structural |
| `00259780` | ctlhismes_init(int) | 396 | 91.92% | needs_review |
| `002875a8` | Draw_Win(int) | 396 | 93.94% | needs_review |
| `000af818` | CEGL2_TEX_HYBRID::GL_Load(int, unsigned int*, unsigned int, int, int, int, int, unsigned char*) | 392 | 100.0% | auto_structural |
| `000da83c` | calceffectangle(int, int) | 392 | 96.94% | auto_structural |
| `001cd308` | check_learning(int, unsigned short*) | 392 | 94.9% | needs_review |
| `001d5640` | get_actwindow_data(int, unsigned char*, unsigned char*, unsigned char*) | 392 | 96.94% | auto_structural |
| `002031a4` | iOSsetCursorByTouch(int, int, int, int, int) | 392 | 57.14% | needs_review |
| `00256174` | ctlfsetnum_main(CTLINFO*) | 392 | 90.82% | needs_review |
| `0015daf4` | iOSQSort(short*, short*, short*, short*, int, int, int) | 388 | 100.0% | auto_structural |
| `00176b80` | bChrSort(int) | 388 | 92.78% | needs_review |
| `001b6c00` | MakeTextureMessage2(unsigned char*, short*, RECT16*, int) | 388 | 100.0% | auto_structural |
| `00201798` | setActionDirection(tag_animation*, tag_animation*) | 388 | 100.0% | auto_structural |
| `0025c928` | ctlshogou_main(CTLINFO*) | 388 | 95.88% | auto_structural |
| `002c9b11` | __gxx_personality_v0 | 388 | 7.22% | needs_review |
| `00094cd4` | _vp_noisemask | 384 | 100.0% | auto_structural |
| `00102504` | Wcalceffectangle(int, int) | 384 | 96.88% | auto_structural |
| `001cced8` | get_ma_result(BWORK*) | 384 | 95.83% | auto_structural |
| `001f4440` | InitAnimationInit() | 384 | 88.54% | needs_review |
| `00242498` | ctlendroll_init() | 384 | 87.5% | needs_review |
| `002453a4` | fft_ending() | 384 | 91.67% | needs_review |
| `0024581c` | movie_init(int, int, int, int, int, char*) | 384 | 88.54% | needs_review |
| `0027fe84` | Savedata_Load(unsigned char*, int*) | 384 | 94.79% | needs_review |
| `00287734` | Draw_Lose(int) | 384 | 93.75% | needs_review |
| `0028e2e4` | CdControl | 384 | 68.75% | needs_review |
| `002b78ac` | RayPick_FT4(tagPOLY_FT4*, int, int) | 384 | 97.92% | auto_structural |
| `00082704` | oggpackB_write | 380 | 98.95% | auto_structural |
| `000b68ac` | CFILE_DAT::Open(char*, int, int) | 380 | 100.0% | auto_structural |
| `0019f798` | MainShop() | 380 | 89.47% | needs_review |
| `001b8e64` | TutrialInit(int) | 380 | 92.63% | needs_review |
| `001d205c` | check_trap(unsigned char, unsigned char, unsigned char) | 380 | 93.68% | needs_review |
| `001d972c` | get_shape2(BWORK*, unsigned char*) | 380 | 54.74% | needs_review |
| `0022a6a4` | _ReadTMD(TMD_PRIM*) | 380 | 84.21% | needs_review |
| `00283fc8` | mapclip_save(int) | 380 | 100.0% | auto_structural |
| `002b2b7c` | SysSE_Play(int, int) | 380 | 95.79% | auto_structural |
| `0020fd1c` | InitializeAll() | 376 | 88.3% | needs_review |
| `00082578` | oggpack_write | 372 | 98.92% | auto_structural |
| `000d123c` | Ddisp_staticwindow2() | 372 | 97.85% | auto_structural |
| `00123a74` | Edisp_staticwindow2() | 372 | 97.85% | auto_structural |
| `001443b0` | Cdisp_staticwindow2() | 372 | 97.85% | auto_structural |
| `0024f8c0` | ctltipsmes_main(CTLINFO*) | 372 | 93.55% | needs_review |
| `0026baec` | wldtown_init() | 372 | 91.4% | needs_review |
| `002b052c` | CAPP_INFO::Init(int) | 372 | 97.85% | auto_structural |
| `000ff2cc` | Wdisposetexture(RECT16*) | 368 | 93.48% | needs_review |
| `0019d634` | MonsterNameInput() | 368 | 88.04% | needs_review |
| `001d1204` | get_reflection_coord(BWORK*, int, int, int, int*, int*, int*) | 368 | 96.74% | auto_structural |
| `001d9d70` | get_item_number(unsigned short, int) | 368 | 96.74% | auto_structural |
| `00210eac` | initMap(int, int) | 368 | 81.52% | needs_review |
| `00211a28` | SetChangePaletteData(unsigned short, unsigned short, unsigned short, unsigned short, unsigned short) | 368 | 91.3% | needs_review |
| `0007cf58` | inflateCopy | 364 | 100.0% | auto_structural |
| `000ff4b0` | Wallocatememorywait(int) | 364 | 92.31% | needs_review |
| `00104a70` | Wdirec4(char*) | 360 | 96.67% | auto_structural |
| `0029c780` | GsSortBoxFill | 360 | 98.89% | auto_structural |
| `000785e8` | gzungetc | 356 | 98.88% | auto_structural |
| `0007874c` | gzgets | 356 | 100.0% | auto_structural |
| `000dc6ec` | direc4(char*) | 356 | 96.63% | auto_structural |
| `000e7da8` | seekcodeplus(int, int, int, int) | 356 | 97.75% | auto_structural |
| `00102f04` | Wseekcodeplus(int, int, int, int) | 356 | 97.75% | auto_structural |
| `001ab67c` | JobEquip(short, short, int) | 356 | 98.88% | auto_structural |
| `0024b824` | ctlbar_exit(CTLINFO*) | 356 | 92.13% | needs_review |
| `00268220` | wldrute_tblget(WALKINFO*, int, int) | 356 | 98.88% | auto_structural |
| `000b6cd8` | CFILE_DAT::Load(int, int, int) | 352 | 100.0% | auto_structural |
| `0015af24` | iOSexecuteScroll() | 352 | 92.05% | needs_review |
| `001d1de8` | set_unitcoord(int, unsigned char, unsigned char, unsigned char, unsigned char) | 352 | 96.59% | auto_structural |
| `002878b4` | Draw_Draw(int) | 352 | 94.32% | needs_review |
| `0029ffac` | RotMatrix | 352 | 100.0% | auto_structural |
| `002cb6d0` | __divsf3 | 352 | 100.0% | auto_structural |
| `001597c0` | disp_worlddhelpmenu() | 348 | 91.95% | needs_review |
| `001d4468` | check_game_cont() | 348 | 98.85% | auto_structural |
| `001da038` | initBdata() | 348 | 96.55% | auto_structural |
| `001e6368` | forecast_skill(BWORK*, BWORK*, ACT*) | 348 | 91.95% | needs_review |
| `00244f18` | roll_autochange() | 348 | 97.7% | auto_structural |
| `0024ac38` | vOpn_defscrwin_set(int, int, _POINT*, _POINT*) | 348 | 90.8% | needs_review |
| `0029aabc` | ReadTIM | 348 | 96.55% | auto_structural |
| `002b582c` | Logo_Init() | 348 | 85.06% | needs_review |
| `000d78f0` | allocatememorywait(int) | 344 | 91.86% | needs_review |
| `0012cc1c` | disp_staticwindow2() | 344 | 97.67% | auto_structural |
| `001d5188` | set_sanjutsuability3(int, unsigned char, short*) | 344 | 100.0% | auto_structural |
| `0020fe94` | InitializeHot() | 344 | 88.37% | needs_review |
| `002578d4` | ctlevtinfo_main(CTLINFO*) | 344 | 90.7% | needs_review |
| `0025ecd8` | iOSWorldPlayer_Hp_Mp(unsigned int, unsigned int) | 344 | 100.0% | auto_structural |
| `002b32e8` | musicPlayer_FrameMove() | 344 | 96.51% | auto_structural |
| `00248cd0` | ctlcard_main(CTLINFO*) | 340 | 89.41% | needs_review |
| `00224650` | CheckBowReachable(unsigned char, unsigned char) | 336 | 98.81% | auto_structural |
| `00255a38` | ctlflagset_init() | 336 | 90.48% | needs_review |
| `0026c27c` | ctltresure_init() | 336 | 91.67% | needs_review |
| `00273b78` | MakeMoveAreaNearByDestination(int) | 336 | 98.81% | auto_structural |
| `00081494` | unzLocateFile | 332 | 100.0% | auto_structural |
| `000a6db4` | CGX_SCREEN_CORRECT::Init(int, int, int, int) | 332 | 100.0% | auto_structural |
| `000bac2c` | CSOUND_IF::FrameMove(int, float) | 332 | 98.8% | auto_structural |
| `000bb6e8` | CSOUND_IF_SL::EngineInit(int) | 332 | 97.59% | auto_structural |
| `001d21d8` | get_stop_event(BWORK*) | 332 | 93.98% | needs_review |
| `00225644` | objectAnim(_EffectTCB*, _Object*) | 332 | 97.59% | auto_structural |
| `0015570c` | worldmap_faceload() | 328 | 95.12% | auto_structural |
| `00269fd8` | snpl_picput() | 328 | 96.34% | auto_structural |
| `0026b724` | worldmap_new() | 328 | 87.8% | needs_review |
| `0007f240` | _tr_stored_block | 324 | 100.0% | auto_structural |
| `001612d0` | iOSsTchBtlInit() | 324 | 80.25% | needs_review |
| `002169d0` | InitSound() | 324 | 91.36% | needs_review |
| `00253d84` | ctltownset_main(CTLINFO*) | 324 | 92.59% | needs_review |
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
| `00162d5c` | iOS_IsInYellowMesh(int, int) | 312 | 92.31% | needs_review |
| `001d2c10` | get_battlebonus(B_BONUS*) | 312 | 93.59% | needs_review |
| `001dc778` | levelup_one(BWORK*, int) | 312 | 100.0% | auto_structural |
| `0020c418` | db_swap(unsigned long*, unsigned long*) | 312 | 89.74% | needs_review |
| `002231d8` | GetBowReachableTangent(BowCheckWork*, int*, int*) | 312 | 100.0% | auto_structural |
| `0025a0f0` | ctlhoukmes_init(int) | 312 | 89.74% | needs_review |
| `0027add8` | MakeMapChantedAction() | 312 | 98.72% | auto_structural |
| `002a0eec` | OuterProduct0 | 312 | 100.0% | auto_structural |
| `002b2d10` | Jingle_Play(int) | 312 | 93.59% | needs_review |
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
| `00225514` | MemoryMapper() | 304 | 88.16% | needs_review |
| `00244de8` | roll_bkfade() | 304 | 96.05% | auto_structural |
| `00255908` | ctlflag_winset(CTLINFO*) | 304 | 96.05% | auto_structural |
| `002bf1fc` | Main_Settings_DrawYesNo(int, int, int) | 304 | 96.05% | auto_structural |
| `0024717c` | ctlsound_init() | 300 | 90.67% | needs_review |
| `002530b8` | ctlbrst_zodiac() | 300 | 93.33% | needs_review |
| `00255054` | ctlmap_eventchk() | 300 | 93.33% | needs_review |
| `00256ec8` | ctltownmenu_exit(CTLINFO*, int) | 300 | 92.0% | needs_review |
| `00257af4` | ctlparty_main(CTLINFO*) | 300 | 90.67% | needs_review |
| `002b3464` | Boot_Init() | 300 | 92.0% | needs_review |
| `001ac3c4` | DrawF4(short*, COLOR*, int, int) | 296 | 97.3% | auto_structural |
| `001b2ac8` | SetJobName() | 296 | 90.54% | needs_review |
| `001d40a8` | set_monsterability2(int, unsigned char, short*, int, unsigned char*) | 296 | 95.95% | auto_structural |
| `0027ec94` | iOS_CMenuTouchSaveLoad::exec(int*, int*) | 296 | 100.0% | auto_structural |
| `00200bb8` | eventZoomChange(int) | 292 | 93.15% | needs_review |
| `0025e310` | sun_to_ivarisday(int*, int*) | 292 | 95.89% | auto_structural |
| `002702f0` | scrwin_para_set(int, int, _POINT*, _POINT*) | 292 | 90.41% | needs_review |
| `002a3648` | pspSaveBase::Update() | 292 | 100.0% | auto_structural |
| `000758c8` | deflateBound | 288 | 100.0% | auto_structural |
| `00079058` | gzvprintf | 288 | 100.0% | auto_structural |
| `0007f388` | _tr_align | 288 | 100.0% | auto_structural |
| `000c18cc` | disp_maptitle() | 288 | 94.44% | needs_review |
| `000da35c` | event_init_memory() | 288 | 76.39% | needs_review |
| `00221d64` | RequestHitMarkEffect(long, EffectOrder*, long) | 288 | 93.06% | needs_review |
| `00249da4` | vOpn_dataload() | 288 | 95.83% | auto_structural |
| `0026af98` | snpl_effcheck(int, int, int) | 288 | 97.22% | auto_structural |
| `002899a0` | pspFftSave(int, FFT_SAVE_DATA*, int*) | 288 | 63.89% | needs_review |
| `0019f914` | ExitShop() | 284 | 91.55% | needs_review |
| `001a6410` | MessageDataSet(int) | 284 | 83.1% | needs_review |
| `001ccafc` | get_floor_damage(BWORK*) | 284 | 90.14% | needs_review |
| `0027f904` | iOS_Resume() | 284 | 98.59% | auto_structural |
| `00076cf0` | deflateParams | 280 | 97.14% | auto_structural |
| `000bb38c` | CSOUND_IF::Pause(int, unsigned char) | 280 | 100.0% | auto_structural |
| `00163bb4` | iOS_initTouchDisable(int) | 280 | 91.43% | needs_review |
| `001ac774` | DrawLineG3(RECT16*, COLOR*, int, int) | 280 | 97.14% | auto_structural |
| `00200e2c` | eventFukanChange(int) | 280 | 92.86% | needs_review |
| `0024935c` | vOpn_swapbuff() | 280 | 95.71% | auto_structural |
| `0024971c` | vOpn_key_rep(unsigned long) | 280 | 94.29% | needs_review |
| `000b5e38` | CUI_SCROLLBAR::FrameMove(float) | 276 | 100.0% | auto_structural |
| `000cbc3c` | TrapWindowTaskManager(int, int, short, int) | 276 | 94.2% | needs_review |
| `00101fe4` | Wevent_init_memory() | 276 | 76.81% | needs_review |
| `001aec8c` | DrawEquipCategory(int, int, int) | 276 | 94.2% | needs_review |
| `00244418` | vEnd_rollline_put(unsigned long*, int) | 276 | 97.1% | auto_structural |
| `0026b904` | wldsymbol_init() | 276 | 91.3% | needs_review |
| `00291178` | MoveImage2 | 276 | 94.2% | needs_review |
| `0029a2d8` | DrawOTag | 276 | 89.86% | needs_review |
| `002b7378` | RENDER_TO_SCREEN(int, int, int*, int*) | 276 | 91.3% | needs_review |
| `000d9638` | fade_eventlocal(ITEMPRIM*, int) | 272 | 95.59% | auto_structural |
| `000f38c4` | disp_plateorspell(ACT*, int, int) | 272 | 97.06% | auto_structural |
| `00155b4c` | worldmap_menuinit() | 272 | 89.71% | needs_review |
| `00159c40` | iosAsmMUL64(long, long, long) | 272 | 98.53% | auto_structural |
| `0015d748` | iOSCurSameOK() | 272 | 89.71% | needs_review |
| `001dc944` | set_casting_status(BWORK*, unsigned char) | 272 | 85.29% | needs_review |
| `001e21f8` | getskillresult_first(int) | 272 | 91.18% | needs_review |
| `001eb360` | defrost(char*, char*) | 272 | 98.53% | auto_structural |
| `0022588c` | NewObject(short, short) | 272 | 92.65% | needs_review |
| `002b7268` | SCREEN_TO_RENDER(int, int, int*, int*) | 272 | 91.18% | needs_review |
| `002c8ac4` | IS_SETTINGS_WND_SLIDER_AREA(int, int) | 272 | 97.06% | auto_structural |
| `000793e0` | inflateBackInit_ | 268 | 97.01% | auto_structural |
| `00082de4` | oggpackB_read | 268 | 100.0% | auto_structural |
| `000a7d1c` | CEGL2_IF::CEGL2_IF() | 268 | 98.51% | auto_structural |
| `00101450` | Wfade_eventlocal(ITEMPRIM*, int) | 268 | 95.52% | auto_structural |
| `0010d738` | Wdisp_plateorspell(ACT*, int, int) | 268 | 97.01% | auto_structural |
| `00159d50` | iosAsmMUL3232(long, long, long, long) | 268 | 98.51% | auto_structural |
| `001d93a4` | add_jobpoint(int, int) | 268 | 100.0% | auto_structural |
| `00200cdc` | startZoomChange(int) | 268 | 94.03% | needs_review |
| `0022a820` | GetAnimationPosition(int, int, EffectOrder*, SVECTOR*) | 268 | 100.0% | auto_structural |
| `00249ac0` | vOpn_padread() | 268 | 91.04% | needs_review |
| `002557ac` | ctlhelp_main(CTLINFO*) | 268 | 85.07% | needs_review |
| `0026c12c` | townbtl_check(int, int*) | 268 | 95.52% | auto_structural |
| `0028b738` | initTaskEmu() | 268 | 92.54% | needs_review |
| `002b7050` | Main_Novel_GetBtnRect(int*, int*, int*, int*, int*, int*) | 268 | 98.51% | auto_structural |
| `002ca215` | __cxa_call_unexpected | 268 | 0.0% | needs_review |
| `0007f138` | _tr_init | 264 | 98.48% | auto_structural |
| `0007fc50` | _tr_tally | 264 | 95.45% | auto_structural |
| `00088bf4` | _ve_envelope_mark | 264 | 100.0% | auto_structural |
| `000ba3a4` | CSOUND_IF::Init(unsigned int, int, char*, int) | 264 | 100.0% | auto_structural |
| `0015a064` | iosAsmKanjiCopy(char*, char*, tCOPYFIELD*, int) | 264 | 96.97% | auto_structural |
| `001c067c` | addlocalprim3(tagPOLY_FT4*, int) | 264 | 96.97% | auto_structural |
| `0025b8ec` | houkoku_mesput(CTLINFO*, int) | 264 | 92.42% | needs_review |
| `00082ce0` | oggpack_read | 260 | 98.46% | auto_structural |
| `000bca88` | CSOUND_IF_SL::EngineUninit() | 260 | 100.0% | auto_structural |
| `001537dc` | eventflaginit() | 260 | 81.54% | needs_review |
| `0019d530` | FighterName() | 260 | 86.15% | needs_review |
| `001bad9c` | SeExec() | 260 | 92.31% | needs_review |
| `001d9250` | get_job_change_flag(unsigned char*, unsigned char) | 260 | 100.0% | auto_structural |
| `00249174` | vOpn_parainit() | 260 | 78.46% | needs_review |
| `00255654` | ctlhelp_init(int, int) | 260 | 87.69% | needs_review |
| `00259ad4` | ctlhismes_main(CTLINFO*) | 260 | 90.77% | needs_review |
| `0026a2cc` | snpl_scrdisp() | 260 | 93.85% | needs_review |
| `00280004` | cSaveFFT::Load() | 260 | 96.92% | auto_structural |
| `00282374` | DispClipedPolygonNo(int, int, int) | 260 | 96.92% | auto_structural |
| `0007b080` | inflateInit2_ | 256 | 96.88% | auto_structural |
| `000b1980` | CEGL_PACKET::Alloc(int) | 256 | 100.0% | auto_structural |
| `00137424` | statusfigprint0(int, int, char*, COPYFIELD*) | 256 | 95.31% | auto_structural |
| `001cc9fc` | status_countdown(int) | 256 | 92.19% | needs_review |
| `001f5320` | displayCursor() | 256 | 96.88% | auto_structural |
| `00210c9c` | setMapVector(SVECTOR*, SVECTOR*) | 256 | 89.06% | needs_review |
| `00225210` | DoPermanentEffect() | 256 | 89.06% | needs_review |
| `0024988c` | vOpn_sun2ivaday(int*, int*) | 256 | 95.31% | auto_structural |
| `0024cf68` | ctlbrst_deactive(CTLINFO*) | 256 | 95.31% | auto_structural |
| `00255180` | ctlmap_active(CTLINFO*) | 256 | 90.62% | needs_review |
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
| `00079308` | gzclose_w | 216 | 100.0% | auto_structural |
| `000cb9e0` | readmaptitle() | 216 | 96.3% | auto_structural |
| `000fef24` | Wdisposewindow(MESSAGEPACKET*) | 216 | 94.44% | needs_review |
| `00201b84` | resetActionDirection(tag_animation*) | 216 | 100.0% | auto_structural |
| `00218cf4` | SetDefaultCamera() | 216 | 98.15% | auto_structural |
| `002867a8` | getMovieEventNum(int) | 216 | 68.52% | needs_review |
| `001c02d4` | JobToAbiChg() | 212 | 92.45% | needs_review |
| `001fea38` | rideOnChokobo(tag_animation*, tag_animation*) | 212 | 100.0% | auto_structural |
| `00249f94` | vOpn_pacinit() | 212 | 86.79% | needs_review |
| `0024b6bc` | ctlbar_active(CTLINFO*) | 212 | 94.34% | needs_review |
| `002531e4` | ctltuto_zodiac() | 212 | 90.57% | needs_review |
| `0025e434` | mouke_app_chk(int, int) | 212 | 100.0% | auto_structural |
| `0025f280` | snpl_load(int) | 212 | 86.79% | needs_review |
| `0029c518` | GsSortLine | 212 | 98.11% | auto_structural |
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
| `000dbba4` | eventsetstatus(int, int, int, int) | 204 | 96.08% | auto_structural |
| `00103ff4` | Weventsetstatus(int, int, int, int) | 204 | 96.08% | auto_structural |
| `0014bedc` | joinfaceuvclut(tagPOLY_FT4*, int, int*) | 204 | 96.08% | auto_structural |
| `00200a1c` | startKnockBack(tag_animation*, tag_animation*) | 204 | 100.0% | auto_structural |
| `00228c74` | InitShape() | 204 | 82.35% | needs_review |
| `00255e14` | ctlfsetnum_init(int, int) | 204 | 86.27% | needs_review |
| `0028a6a0` | pspTitleSaveCheck() | 204 | 98.04% | auto_structural |
| `002a103c` | TransRot_32 | 204 | 98.04% | auto_structural |
| `000d8fe0` | get_cursoroffset(int) | 200 | 92.0% | needs_review |
| `00100df8` | Wget_cursoroffset(int) | 200 | 92.0% | needs_review |
| `0015a7d8` | iOSScrollButtonMove() | 200 | 90.0% | needs_review |
| `0024232c` | vOpn_arzpic_main() | 200 | 98.0% | auto_structural |
| `0024a5c0` | vOpn_winopen_frmcalc(int, RECT16*, RECT16*) | 200 | 96.0% | auto_structural |
| `00257a2c` | ctlparty_init() | 200 | 86.0% | needs_review |
| `0029c6b8` | GsGetTimInfo | 200 | 100.0% | auto_structural |
| `002a16d0` | ColorMatCol | 200 | 100.0% | auto_structural |
| `002b1e70` | NowLoading_FrameMove() | 200 | 90.0% | needs_review |
| `000da720` | tutorial_hookfunc() | 196 | 85.71% | needs_review |
| `001383a4` | maptest() | 196 | 85.71% | needs_review |
| `001a8508` | GetCommandList(short, short*) | 196 | 97.96% | auto_structural |
| `00200f44` | startFukanChange() | 196 | 91.84% | needs_review |
| `0021025c` | InitializePartyItem() | 196 | 93.88% | needs_review |
| `00211e50` | setPresentClutDataAsDefault(unsigned int, unsigned int, int) | 196 | 93.88% | needs_review |
| `00242268` | vOpn_arzpic_init(int) | 196 | 89.8% | needs_review |
| `0025e508` | person_year_up() | 196 | 93.88% | needs_review |
| `0028dae4` | tlMoveHeap(long long, int) | 196 | 97.96% | auto_structural |
| `002a0bc4` | ScaleMatrixL | 196 | 100.0% | auto_structural |
| `002b77e8` | RayPick_GT3_input(tagPOLY_GT3*, int, int, int, int) | 196 | 100.0% | auto_structural |
| `0007fd58` | uncompress | 192 | 97.92% | auto_structural |
| `001d9f58` | get_setstatus_max(A_RESULT*) | 192 | 95.83% | auto_structural |
| `0020c774` | mallocForFile(unsigned int) | 192 | 95.83% | auto_structural |
| `0020f350` | callEventEffect(int, int, void*) | 192 | 100.0% | auto_structural |
| `0024a924` | vOpnwin_set(int, RECT16, int, unsigned long*) | 192 | 97.92% | auto_structural |
| `00269870` | snpl_syscur() | 192 | 89.58% | needs_review |
| `000d8978` | itemuvclut(tagSPRT*, int) | 188 | 95.74% | auto_structural |
| `000dfa94` | makemessagestructure() | 188 | 91.49% | needs_review |
| `000ff61c` | Wdisposememory(char*) | 188 | 97.87% | auto_structural |
| `00100648` | Witemuvclut(tagSPRT*, int) | 188 | 95.74% | auto_structural |
| `0020c19c` | fftVSyncCallback() | 188 | 87.23% | needs_review |
| `0020c628` | mallocForSound(unsigned int) | 188 | 95.74% | auto_structural |
| `0020f43c` | debugEffectWait() | 188 | 80.85% | needs_review |
| `00261b0c` | mouke_eventday_chg() | 188 | 93.62% | needs_review |
| `0028b638` | FFT_Main(void*) | 188 | 97.87% | auto_structural |
| `00291098` | StoreImage2 | 188 | 93.62% | needs_review |
| `00291744` | SetDrawEnv | 188 | 100.0% | auto_structural |
| `002a0998` | ApplyMatrixLV | 188 | 97.87% | auto_structural |
| `002ab718` | sceGuEnable | 188 | 97.87% | auto_structural |
| `001cd490` | set_learning(BWORK*) | 184 | 97.83% | auto_structural |
| `0020e314` | moveToPanel(int, SVECTOR*, int, int, int) | 184 | 100.0% | auto_structural |
| `00254f9c` | ctltownset_init(int, int) | 184 | 86.96% | needs_review |
| `0028d0f8` | tlInitHeap(void*, unsigned int) | 184 | 95.65% | auto_structural |
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
| `0029c954` | sceVfpuVector4OuterProductXYZ(ScePspFVector4*, ScePspFVector4 const*, ScePspFVector4 const*) | 180 | 100.0% | auto_structural |
| `002ab7d4` | sceGuDisable | 180 | 97.78% | auto_structural |
| `001568fc` | worldmap_restart() | 176 | 81.82% | needs_review |
| `001abb9c` | GetJobShape(short, short, short*) | 176 | 95.45% | auto_structural |
| `001b6f14` | CountWidthMessage(unsigned char*) | 176 | 97.73% | auto_structural |
| `001d91a0` | init_entry_status(BWORK*) | 176 | 100.0% | auto_structural |
| `001e3988` | get_movetype(BWORK*) | 176 | 100.0% | auto_structural |
| `00201008` | iOSVectorNormal(VECTOR*) | 176 | 97.73% | auto_structural |
| `00249cf4` | vOpn_timload(unsigned long*) | 176 | 100.0% | auto_structural |
| `002741bc` | SetMove() | 176 | 95.45% | auto_structural |
| `00285d6c` | pspJobGetTamanegiLevel(unsigned char (*) [3]) | 176 | 100.0% | auto_structural |
| `0029a92c` | LoadTPage | 176 | 100.0% | auto_structural |
| `000da4ac` | event_init_light() | 172 | 88.37% | needs_review |
| `001049c4` | Weventsetchrcol(char*) | 172 | 100.0% | auto_structural |
| `001bd320` | UnitTableInitFirst(short) | 172 | 83.72% | needs_review |
| `001cc950` | status_handle_main(BWORK*) | 172 | 93.02% | needs_review |
| `001cce2c` | get_trap_result(BWORK*) | 172 | 88.37% | needs_review |
| `001d7340` | net_change_bwork() | 172 | 100.0% | auto_structural |
| `0021f0e4` | NewPEffectTCB() | 172 | 97.67% | auto_structural |
| `00225370` | Malloc(unsigned long, long) | 172 | 95.35% | auto_structural |
| `0024998c` | vOpn_iwaprog() | 172 | 83.72% | needs_review |
| `002699bc` | snpl_putpara() | 172 | 83.72% | needs_review |
| `002919c0` | SetDrawMode | 172 | 100.0% | auto_structural |
| `002aca7c` | GuEmu_FrameMove() | 172 | 93.02% | needs_review |
| `002b1f3c` | Offscreen_ReadPixels(int, int, int, int) | 172 | 93.02% | needs_review |
| `00073a2c` | compress2 | 168 | 97.62% | auto_structural |
| `00097e9c` | _book_maptype1_quantvals | 168 | 100.0% | auto_structural |
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
| `001bb460` | SetSttsAbi(int) | 164 | 92.68% | needs_review |
| `001f4a88` | initEntryPlayerAnimations() | 164 | 87.8% | needs_review |
| `0024556c` | movie_exit(int) | 164 | 97.56% | auto_structural |
| `0025dd14` | iOSwldkey_repSet(unsigned long) | 164 | 95.12% | auto_structural |
| `00289ac0` | pspFftLoad(int, FFT_SAVE_DATA*, int*, int) | 164 | 92.68% | needs_review |
| `0029a3ec` | DrawPrim | 164 | 90.24% | needs_review |
| `00081bb8` | unzCloseCurrentFile | 160 | 100.0% | auto_structural |
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
| `00078900` | gzclose_r | 156 | 100.0% | auto_structural |
| `000da280` | recieve_statusinfo() | 156 | 92.31% | needs_review |
| `000db3a4` | envvolcontrol() | 156 | 100.0% | auto_structural |
| `001bb224` | SetSttsEqu2(int) | 156 | 87.18% | needs_review |
| `001cd9b0` | inc_party_item(BWORK*, unsigned short, BWORK*) | 156 | 94.87% | needs_review |
| `001d2d48` | clear_status_animation(BWORK*) | 156 | 100.0% | auto_structural |
| `001d9104` | set_status_counter(BWORK*, int, int) | 156 | 97.44% | auto_structural |
| `001ed8b0` | getBattleWorkAnimationHight(tag_animation*) | 156 | 100.0% | auto_structural |
| `00221028` | RequestBowEffect(long, EffectOrder*) | 156 | 94.87% | needs_review |
| `0027faa0` | iOS_SuspendWorldMap() | 156 | 97.44% | auto_structural |
| `00077b80` | gzrewind | 152 | 100.0% | auto_structural |
| `0007854c` | gzgetc | 152 | 100.0% | auto_structural |
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
| `00263254` | ctlmouketeam_deactive(CTLINFO*) | 152 | 94.74% | needs_review |
| `002cb0c0` | __gedf2 | 152 | 92.11% | needs_review |
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
| `001f5b50` | terminateAnimationSub(int, int, short, short, short) | 148 | 100.0% | auto_structural |
| `00266544` | iOS_drawMenuAssist_wld(iOS_CMenuTouch*, GsOT*) | 148 | 100.0% | auto_structural |
| `00268ec4` | wldcenter_move() | 148 | 94.59% | needs_review |
| `00290b54` | ClearOTag | 148 | 100.0% | auto_structural |
| `002b6b38` | Main_Uninit() | 148 | 94.59% | needs_review |
| `002b715c` | setPspDispNum(short, short, short) | 148 | 89.19% | needs_review |
| `002bb678` | iOSMenuOkCancelHelpGet(int, int) | 148 | 94.59% | needs_review |
| `00097b70` | _float32_pack | 144 | 88.89% | needs_review |
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
| `0026dc2c` | ctltuto_active(CTLINFO*) | 144 | 94.44% | needs_review |
| `00291824` | SetDrawLoad | 144 | 100.0% | auto_structural |
| `00292678` | __xpLibgpuDrawCallBack(int) | 144 | 83.33% | needs_review |
| `002abc8c` | sceGuTexFilter | 144 | 94.44% | needs_review |
| `002cb0c8` | __ledf2 | 144 | 97.22% | auto_structural |
| `000da9c4` | checkpara1(int) | 140 | 100.0% | auto_structural |
| `000dfb50` | recover_chrname() | 140 | 97.14% | auto_structural |
| `000ff718` | Wsttsback_normal(STTSWINDOWBACK*) | 140 | 94.29% | needs_review |
| `00102e14` | Wenvvolcontrol() | 140 | 100.0% | auto_structural |
| `0010c7fc` | Wrecover_chrname() | 140 | 97.14% | auto_structural |
| `001bb504` | SetSttsBoth(int) | 140 | 91.43% | needs_review |
| `001dc37c` | inc_dead_number(BWORK*) | 140 | 97.14% | auto_structural |
| `0021627c` | readMusicBuffer(int, int) | 140 | 94.29% | needs_review |
| `0022a618` | _OpenTMD(unsigned long*, int) | 140 | 97.14% | auto_structural |
| `00245e38` | ctlstartmov_init(int, int, int, int) | 140 | 85.71% | needs_review |
| `002562fc` | sthelp_curpos_set(CTLINFO*) | 140 | 94.29% | needs_review |
| `00284314` | Init_VectorDataBaseObject(VECTOR_DATABASE_CONTAINER*, unsigned int) | 140 | 100.0% | auto_structural |
| `00284594` | new_Vector(VECTOR_DATABASE*, SVECTOR const*) | 140 | 100.0% | auto_structural |
| `002889cc` | pspOffScreenInit(RECT16*, RECT16*) | 140 | 97.14% | auto_structural |
| `002cb4ac` | __floatundisf | 140 | 82.86% | needs_review |
| `00080844` | unzStringFileNameCompare | 136 | 100.0% | auto_structural |
| `000e5680` | disp_status2() | 136 | 85.29% | needs_review |
| `000e5708` | disp_status2right() | 136 | 85.29% | needs_review |
| `00161da4` | iOSGetStatuswindowTap() | 136 | 100.0% | auto_structural |
| `001d2de4` | init_status_animation(int) | 136 | 97.06% | auto_structural |
| `0020db18` | setBackColorOffset(short, short, short) | 136 | 97.06% | auto_structural |
| `00224cc4` | GetPermanentEffectAnimationAngle() | 136 | 97.06% | auto_structural |
| `00228d40` | InitPermanentShape() | 136 | 82.35% | needs_review |
| `002433dc` | fRoll_cdxastop(short*) | 136 | 97.06% | auto_structural |
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
| `0026dcbc` | ctltuto_deactive(CTLINFO*) | 132 | 93.94% | needs_review |
| `0028d7d0` | tlHeapStat(tl_mem_stat_t*) | 132 | 96.97% | auto_structural |
| `00290be8` | ClearOTagR | 132 | 100.0% | auto_structural |
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
| `002b3590` | Boot_FrameMove() | 128 | 90.62% | needs_review |
| `000791a8` | gzflush | 124 | 100.0% | auto_structural |
| `000daff0` | move_ambient() | 124 | 96.77% | auto_structural |
| `00102aa4` | Wmove_ambient() | 124 | 96.77% | auto_structural |
| `00105510` | Wwait_direc(int) | 124 | 93.55% | needs_review |
| `00161ef8` | wasmTaskEntry() | 124 | 93.55% | needs_review |
| `0016a14c` | ASURA_soundStop() | 124 | 90.32% | needs_review |
| `001baae8` | SttsAMovingChk() | 124 | 90.32% | needs_review |
| `001dbc48` | init_entry_status0(BWORK*) | 124 | 100.0% | auto_structural |
| `0020c550` | db_swap_generate(unsigned long*, unsigned long*) | 124 | 90.32% | needs_review |
| `00210d9c` | NewEntry(int, int, int, short, short, short, short, BWORK*, int) | 124 | 96.77% | auto_structural |
| `0024a544` | vOpn_add_winpac(unsigned long*, int*) | 124 | 93.55% | needs_review |
| `0024a9e4` | vOpnwin_trans(int, unsigned long*) | 124 | 96.77% | auto_structural |
| `002665d8` | add_anmpac(unsigned long*, int*) | 124 | 93.55% | needs_review |
| `00279eec` | SetTrapPanel(int, int, int) | 124 | 96.77% | auto_structural |
| `0028bec0` | TE_VSync(int) | 124 | 90.32% | needs_review |
| `0029a89c` | SetDefDrawEnv | 124 | 100.0% | auto_structural |
| `002b2798` | SE_CorrectFID(int) | 124 | 93.55% | needs_review |
| `002b2a18` | SE_StopVFX(int) | 124 | 90.32% | needs_review |
| `002b36dc` | Error_FrameRender() | 124 | 90.32% | needs_review |
| `002cb4bc` | __aeabi_l2f | 124 | 100.0% | auto_structural |
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
| `0028441c` | Clear_VectorDataBaseContainer(VECTOR_DATABASE_CONTAINER*) | 120 | 100.0% | auto_structural |
| `002918ec` | SetTexWindow | 120 | 100.0% | auto_structural |
| `002b1458` | Project_Core_Bootup() | 120 | 96.67% | auto_structural |
| `002c5434` | Movie_FrameRender() | 120 | 90.0% | needs_review |
| `00077524` | gzerror | 116 | 93.1% | needs_review |
| `00081660` | unzGoToFilePos64 | 116 | 100.0% | auto_structural |
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
| `0024fd00` | pspCtltutonet_active(CTLINFO*) | 116 | 93.1% | needs_review |
| `0025b878` | houkokumes_select(int, int) | 116 | 100.0% | auto_structural |
| `0025d590` | directedit_chk() | 116 | 96.55% | auto_structural |
| `002816bc` | iOS_v2menuSetEnable(V2_MENU_ITEM, int) | 116 | 93.1% | needs_review |
| `002cabdc` | __aeabi_ul2d | 116 | 75.86% | needs_review |
| `002cb830` | __gtsf2 | 116 | 89.66% | needs_review |
| `00080a4c` | unzGoToFirstFile | 112 | 100.0% | auto_structural |
| `00097a48` | res1_forward | 112 | 100.0% | auto_structural |
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
| `0028d088` | tlSetHeap(void*) | 112 | 85.71% | needs_review |
| `0028e25c` | OpenEvent(unsigned long, long, long, long (*)()) | 112 | 92.86% | needs_review |
| `002a1798` | gteMIMefunc | 112 | 100.0% | auto_structural |
| `002a23bc` | RotColorDpq3_nom | 112 | 96.43% | auto_structural |
| `00096f20` | res1_inverse | 108 | 96.3% | auto_structural |
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
| `0026a504` | snpl_jparasmall() | 108 | 96.3% | auto_structural |
| `00281730` | iOS_v2menuGetEnable(V2_MENU_ITEM) | 108 | 92.59% | needs_review |
| `00282648` | wgte_color_set_vec(MATRIX const*, int, SVECTOR const*) | 108 | 100.0% | auto_structural |
| `002ab960` | sceGuGetMemory_for_iOS | 108 | 96.3% | auto_structural |
