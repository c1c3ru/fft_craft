# Parallel reverse-engineering loop

Binary SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Analyzed in current binary: 344
Automatically triaged: 77,164 bytes / 1,837,392 inventory bytes (4.20%); **this is newly triaged coverage, not total project coverage**.

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
