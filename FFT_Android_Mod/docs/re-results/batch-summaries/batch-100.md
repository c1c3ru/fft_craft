# Parallel reverse-engineering loop

Binary SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Analyzed in current binary: 99
Automatically triaged: 31,556 bytes / 1,837,392 inventory bytes (1.72%); **this is newly triaged coverage, not total project coverage**.

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
