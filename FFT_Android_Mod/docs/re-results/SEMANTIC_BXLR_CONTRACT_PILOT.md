# Validação dos contratos locais BX LR — todas as candidatas

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

- Entradas de 4 bytes ARM verificadas: **473**
- Folhas BX LR disponíveis: **303**
- Contratos locais verificados neste lote: **303**
- Testes diferenciais ARM/Thumb deste lote: **9696**

**Status:** pronto para revisão; **0 novas certificações integrais**. As pós-condições cobrem o corpo de uma instrução no contexto ARM normal. A equivalência global, os casos de exceção e a aprovação de revisor permanecem pendentes.

| Endereço | Símbolo | Corpo completo | ARM / Thumb |
|---|---|---|---|
| `000a6d5c` | CGX_SCREEN_CORRECT::~CGX_SCREEN_CORRECT() | `BX LR` | 16 + 16 testes |
| `000a7e78` | CEGL2_IF::Setup3D() | `BX LR` | 16 + 16 testes |
| `000a8560` | CEGL2_IF::DrawGrid() | `BX LR` | 16 + 16 testes |
| `000a8564` | CEGL2_IF::DrawAxis() | `BX LR` | 16 + 16 testes |
| `000a8568` | CEGL2_IF::DrawCross(math::VECTOR3<float>, float) | `BX LR` | 16 + 16 testes |
| `000af9bc` | CCAMERA::Uninit() | `BX LR` | 16 + 16 testes |
| `000b3524` | CINPUT_DATA::~CINPUT_DATA() | `BX LR` | 16 + 16 testes |
| `000b4f70` | CRECT::CRECT() | `BX LR` | 16 + 16 testes |
| `000b4f74` | CRECT::~CRECT() | `BX LR` | 16 + 16 testes |
| `000b5524` | CRECT::MoveCursor(int) | `BX LR` | 16 + 16 testes |
| `000b5528` | CRECT::MoveCursorPos(int, int) | `BX LR` | 16 + 16 testes |
| `000b61d4` | CCOMP_Z_DEC::~CCOMP_Z_DEC() | `BX LR` | 16 + 16 testes |
| `000b6200` | CCOMP_Z_DEC::Error(char const*) | `BX LR` | 16 + 16 testes |
| `000b63a0` | CCOMP_Z_ENC::~CCOMP_Z_ENC() | `BX LR` | 16 + 16 testes |
| `000b63cc` | CCOMP_Z_ENC::Error(char const*) | `BX LR` | 16 + 16 testes |
| `000b6580` | CCRYPT::CCRYPT() | `BX LR` | 16 + 16 testes |
| `000b6584` | CCRYPT::~CCRYPT() | `BX LR` | 16 + 16 testes |
| `000b789c` | CFILE_UTIL::CFILE_UTIL() | `BX LR` | 16 + 16 testes |
| `000b78a0` | CFILE_UTIL::~CFILE_UTIL() | `BX LR` | 16 + 16 testes |
| `000b7988` | CFILE_UTIL::DirGetWindows(char*) | `BX LR` | 16 + 16 testes |
| `000b798c` | CFILE_UTIL::DirGetSystem(char*) | `BX LR` | 16 + 16 testes |
| `000b7998` | CFILE_UTIL::DirGetExecute(char*, char*) | `BX LR` | 16 + 16 testes |
| `000b8bdc` | CSTR_UTIL::CSTR_UTIL() | `BX LR` | 16 + 16 testes |
| `000b8be0` | CSTR_UTIL::~CSTR_UTIL() | `BX LR` | 16 + 16 testes |
| `000bb834` | CSOUND_IF_SL::FrameMove(int, float) | `BX LR` | 16 + 16 testes |
| `000bbb10` | CSOUND_IF_SL::SetTrans(int, float, float, float) | `BX LR` | 16 + 16 testes |
| `000bcbf0` | CSOUND_LOADER::FrameMove(int, float) | `BX LR` | 16 + 16 testes |
| `000bd964` | CFRAMERATE::~CFRAMERATE() | `BX LR` | 16 + 16 testes |
| `000bdb6c` | CSTEP::~CSTEP() | `BX LR` | 16 + 16 testes |
| `000c4418` | Adisp_floateventwindow() | `BX LR` | 16 + 16 testes |
| `000c4494` | Aitemmenu_call(unsigned long*, unsigned long, int) | `BX LR` | 16 + 16 testes |
| `000c4498` | attackdebugfunc() | `BX LR` | 16 + 16 testes |
| `000cbd50` | SetTrapNameWindowParam(int, short, int) | `BX LR` | 16 + 16 testes |
| `000cbd54` | TrapNameWindowManager() | `BX LR` | 16 + 16 testes |
| `000cbd58` | CreateTrapNameWindowManagerTask() | `BX LR` | 16 + 16 testes |
| `000cbd5c` | deleteEndModeWindow() | `BX LR` | 16 + 16 testes |
| `000cbd60` | SetTrapNameWindowColor(int) | `BX LR` | 16 + 16 testes |
| `000cbd64` | CreateTrapCancelCommandWindow() | `BX LR` | 16 + 16 testes |
| `000cbd68` | DeleteTrapCancelCommandWindow() | `BX LR` | 16 + 16 testes |
| `000cbd74` | CreateNetStayWindow() | `BX LR` | 16 + 16 testes |
| `000d0dc8` | Ddisp_floateventwindow() | `BX LR` | 16 + 16 testes |
| `000d1408` | Ditemmenu_call(unsigned long*, unsigned long, int) | `BX LR` | 16 + 16 testes |
| `000d6f80` | iOS_chkallocatewindowinit() | `BX LR` | 16 + 16 testes |
| `000d7384` | disposewindowbytask(int) | `BX LR` | 16 + 16 testes |
| `000d8970` | dispemptywindow() | `BX LR` | 16 + 16 testes |
| `000d8974` | send_statuschrno(int) | `BX LR` | 16 + 16 testes |
| `000d8bfc` | initstatuscphase() | `BX LR` | 16 + 16 testes |
| `000d9a08` | hook_disp_requirement() | `BX LR` | 16 + 16 testes |
| `000d9a0c` | hook_trophics() | `BX LR` | 16 + 16 testes |
| `000d9a10` | seekpcfile(char*, char*, int, int) | `BX LR` | 16 + 16 testes |
| `000d9ac0` | loadonefile(char*, char*) | `BX LR` | 16 + 16 testes |
| `000d9b0c` | request_tooltest() | `BX LR` | 16 + 16 testes |
| `000da334` | request_effectmes(int, int, int, int) | `BX LR` | 16 + 16 testes |
| `000da338` | request_warnmes(int, int, int, int) | `BX LR` | 16 + 16 testes |
| `000e62c4` | DEBUGTRACE_hook_connect_camera() | `BX LR` | 16 + 16 testes |
| `000e62c8` | DEBUG_CHK_ROLL(SCROLLRECORD*) | `BX LR` | 16 + 16 testes |
| `000e7f0c` | dmp_tuto(unsigned char*, int) | `BX LR` | 16 + 16 testes |
| `000feaa4` | WiOS_chkallocatewindowinit() | `BX LR` | 16 + 16 testes |
| `00100640` | Wdispemptywindow() | `BX LR` | 16 + 16 testes |
| `00100644` | Wsend_statuschrno(int) | `BX LR` | 16 + 16 testes |
| `00100840` | Winitstatuscphase() | `BX LR` | 16 + 16 testes |
| `00101908` | Whook_disp_requirement() | `BX LR` | 16 + 16 testes |
| `0010190c` | Whook_trophics() | `BX LR` | 16 + 16 testes |
| `00101910` | Wseekpcfile(char*, char*, int, int) | `BX LR` | 16 + 16 testes |
| `001019bc` | Wloadonefile(char*, char*) | `BX LR` | 16 + 16 testes |
| `00101a0c` | Wrequest_tooltest() | `BX LR` | 16 + 16 testes |
| `00101f9c` | Wrequest_effectmes(int, int, int, int) | `BX LR` | 16 + 16 testes |
| `00101fa0` | Wrequest_warnmes(int, int, int, int) | `BX LR` | 16 + 16 testes |
| `00102128` | Wevent_init_light() | `BX LR` | 16 + 16 testes |
| `00121718` | Edisp_floateventwindow() | `BX LR` | 16 + 16 testes |
| `00123c40` | Eitemmenu_call(unsigned long*, unsigned long, int) | `BX LR` | 16 + 16 testes |
| `0012b108` | disp_floateventwindow() | `BX LR` | 16 + 16 testes |
| `0014b9f8` | Cdisp_floateventwindow() | `BX LR` | 16 + 16 testes |
| `0014bec4` | Citemmenu_call(unsigned long*, unsigned long, int) | `BX LR` | 16 + 16 testes |
| `0014e0e8` | statushookfunc() | `BX LR` | 16 + 16 testes |
| `0014e9a0` | sol_draw(int, int, int) | `BX LR` | 16 + 16 testes |
| `00155708` | story_faceload() | `BX LR` | 16 + 16 testes |
| `0015f044` | iOSUnitListLRCurSet(unsigned char*, unsigned short*, int, int, int, int) | `BX LR` | 16 + 16 testes |
| `00161d98` | tDebugBreakCheck(int) | `BX LR` | 16 + 16 testes |
| `00161d9c` | tDebugBreakTime(int) | `BX LR` | 16 + 16 testes |
| `00161da0` | tDebugPointerErr() | `BX LR` | 16 + 16 testes |
| `0016f840` | cCardInit() | `BX LR` | 16 + 16 testes |
| `001836cc` | iOS_addPrim_window(tagPOLY_FT4*) | `BX LR` | 16 + 16 testes |
| `0018372c` | CardInit() | `BX LR` | 16 + 16 testes |
| `0019e7b4` | shop_dummyfunc() | `BX LR` | 16 + 16 testes |
| `001add64` | unit_dummyfunc() | `BX LR` | 16 + 16 testes |
| `001d114c` | set_monomane_direction(BWORK*, unsigned char) | `BX LR` | 16 + 16 testes |
| `001dca54` | callSW(int) | `BX LR` | 16 + 16 testes |
| `001e7368` | pspNetTrapSpread(BWORK*, int) | `BX LR` | 16 + 16 testes |
| `00202f1c` | pspNetOutPutAnimationData() | `BX LR` | 16 + 16 testes |
| `0020c258` | fftDrawSyncCallback() | `BX LR` | 16 + 16 testes |
| `0020c25c` | fftCdReadyCallback() | `BX LR` | 16 + 16 testes |
| `0020c260` | fftCdReadCallback() | `BX LR` | 16 + 16 testes |
| `0020c5cc` | myPollhost() | `BX LR` | 16 + 16 testes |
| `0020c5d0` | system_error(int, int) | `BX LR` | 16 + 16 testes |
| `0020c5d4` | system_warning(int, int) | `BX LR` | 16 + 16 testes |
| `0020f4f8` | getCharPrimList(short, Point*, unsigned long*) | `BX LR` | 16 + 16 testes |
| `0020f904` | iOS_dispAnimetion() | `BX LR` | 16 + 16 testes |
| `0020fb14` | initializeDebugFont() | `BX LR` | 16 + 16 testes |
| `00215d5c` | PadStop | `BX LR` | 16 + 16 testes |
| `002168fc` | recallEnvEffect() | `BX LR` | 16 + 16 testes |
| `002169cc` | pauseEnvEffect() | `BX LR` | 16 + 16 testes |
| `0021ebb0` | error(char, long) | `BX LR` | 16 + 16 testes |
| `00225310` | iOS_CheckPEffect(char const*, int) | `BX LR` | 16 + 16 testes |
| `00225a60` | objectLG2(_EffectTCB*, _Object*) | `BX LR` | 16 + 16 testes |
| `00225a64` | dmyFnc2(_EffectTCB*, _Object*) | `BX LR` | 16 + 16 testes |
| `0022a614` | DumpMemory(int, void*) | `BX LR` | 16 + 16 testes |
| `002419cc` | fftCdLoop(CDREC*) | `BX LR` | 16 + 16 testes |
| `002419d0` | fftCdCancel(CDREC*) | `BX LR` | 16 + 16 testes |
| `002524cc` | ctlworkingst_deactive(CTLINFO*) | `BX LR` | 16 + 16 testes |
| `00252b68` | ctlworkend_active(CTLINFO*) | `BX LR` | 16 + 16 testes |
| `00252b6c` | ctlworkend_deactive(CTLINFO*) | `BX LR` | 16 + 16 testes |
| `00258ac4` | evt_skip0() | `BX LR` | 16 + 16 testes |
| `0025f354` | wld_btlsect_seek() | `BX LR` | 16 + 16 testes |
| `00267f38` | wldrute_init() | `BX LR` | 16 + 16 testes |
| `0026c058` | iOS_debugDispTownCircle(int, int) | `BX LR` | 16 + 16 testes |
| `0026ff2c` | effectdmy() | `BX LR` | 16 + 16 testes |
| `0027129c` | Ssd_Quit() | `BX LR` | 16 + 16 testes |
| `002712a0` | Ssd_Enable() | `BX LR` | 16 + 16 testes |
| `002712a4` | Ssd_Disable() | `BX LR` | 16 + 16 testes |
| `002712b0` | Ssd_DisposeNormalWave() | `BX LR` | 16 + 16 testes |
| `002712b4` | Ssd_DisposeWaveData(SsdWaveSetRec*) | `BX LR` | 16 + 16 testes |
| `002712c0` | Ssd_AddEffectData(void*) | `BX LR` | 16 + 16 testes |
| `002712c4` | Ssd_DisposeEffectData(void*) | `BX LR` | 16 + 16 testes |
| `002712c8` | Ssd_AllStop() | `BX LR` | 16 + 16 testes |
| `002712cc` | Ssd_SetStereo(int) | `BX LR` | 16 + 16 testes |
| `002712d8` | Ssd_SetAttenuator(short) | `BX LR` | 16 + 16 testes |
| `002712dc` | Ssd_SetReverbParam(long, short, long, long) | `BX LR` | 16 + 16 testes |
| `002712e0` | Ssd_SetSpuVolume(short, short) | `BX LR` | 16 + 16 testes |
| `002712e4` | Ssd_SetCDVolume(short, short) | `BX LR` | 16 + 16 testes |
| `002712e8` | Ssd_SetCDMixingReverb(int, int) | `BX LR` | 16 + 16 testes |
| `002712ec` | Ssd_CheckWideMode() | `BX LR` | 16 + 16 testes |
| `002712f0` | Ssd_SetVolumeRec(short, SpuVolume*, char) | `BX LR` | 16 + 16 testes |
| `002712f4` | Ssd_ErrorProc(int) | `BX LR` | 16 + 16 testes |
| `002712f8` | Ssd_AddVagPackData(void*) | `BX LR` | 16 + 16 testes |
| `00271304` | Ssd_DisposeMusic(SsdSeqRec*) | `BX LR` | 16 + 16 testes |
| `00271308` | Ssd_LinkMusicData(SsdSeqRec*, void*) | `BX LR` | 16 + 16 testes |
| `0027130c` | Ssd_StartMusic(SsdSeqRec*, short, short) | `BX LR` | 16 + 16 testes |
| `00271310` | Ssd_StopMusic(SsdSeqRec*) | `BX LR` | 16 + 16 testes |
| `00271340` | Ssd_PlayEffects03(long, long, long, long) | `BX LR` | 16 + 16 testes |
| `00271348` | Ssd_StopEffectSet(void*) | `BX LR` | 16 + 16 testes |
| `00271410` | Ssd_InitEffectTrackRecWithStart(short, long, short, short) | `BX LR` | 16 + 16 testes |
| `00271414` | Ssd_SetSeqMasterVolume(SsdSeqRec*, short, short) | `BX LR` | 16 + 16 testes |
| `00271418` | Ssd_SetSeqMasterTempo(SsdSeqRec*, short, short) | `BX LR` | 16 + 16 testes |
| `0027141c` | Ssd_SetSeqMasterPitch(SsdSeqRec*, short, short) | `BX LR` | 16 + 16 testes |
| `00271420` | Ssd_SetSeqMasterPanpot(SsdSeqRec*, short, short) | `BX LR` | 16 + 16 testes |
| `0027b510` | dispCmdKind() | `BX LR` | 16 + 16 testes |
| `0027b5c8` | rprintfr(RECT16*, int, int, int) | `BX LR` | 16 + 16 testes |
| `0027b670` | iOS_DEBUG_multiwindow_break_hook(unsigned long*) | `BX LR` | 16 + 16 testes |
| `0027b674` | iOS_DEBUG_multiwindow_break_hook2(unsigned long*, int) | `BX LR` | 16 + 16 testes |
| `0027b678` | iOS_DEBUG_multiwindow_keyright_hook() | `BX LR` | 16 + 16 testes |
| `0027fc28` | chk_ucResumeData2(int) | `BX LR` | 16 + 16 testes |
| `0027fc2c` | chk_ucResumeData(unsigned char*, int) | `BX LR` | 16 + 16 testes |
| `0027fc7c` | cSaveFFT::~cSaveFFT() | `BX LR` | 16 + 16 testes |
| `002805e4` | iOS_hookHelp(int*) | `BX LR` | 16 + 16 testes |
| `00280614` | iOS_hook_disp_option() | `BX LR` | 16 + 16 testes |
| `00280618` | iOS_hook_disp_optionmain() | `BX LR` | 16 + 16 testes |
| `0028061c` | iOS_hook_common(char const*, int) | `BX LR` | 16 + 16 testes |
| `00280670` | hook_write_eventflag(int, int) | `BX LR` | 16 + 16 testes |
| `00280674` | hook_calcformula(int, int) | `BX LR` | 16 + 16 testes |
| `00280678` | hook_Debug(char const*) | `BX LR` | 16 + 16 testes |
| `0028067c` | hook_Debug2(char const*) | `BX LR` | 16 + 16 testes |
| `00280680` | hook_NextEventSet() | `BX LR` | 16 + 16 testes |
| `00280684` | hook_musiclod() | `BX LR` | 16 + 16 testes |
| `002806b0` | iOS_hook_worldhelpmenu() | `BX LR` | 16 + 16 testes |
| `002806b4` | iOS_hook_gill() | `BX LR` | 16 + 16 testes |
| `002806b8` | iOS_hook_movetopanel() | `BX LR` | 16 + 16 testes |
| `002806bc` | hook_read_eventflag(int*) | `BX LR` | 16 + 16 testes |
| `002806c0` | hook_allocate_texture() | `BX LR` | 16 + 16 testes |
| `002806c4` | hook_opt() | `BX LR` | 16 + 16 testes |
| `002806c8` | hook_chk_speedup(int) | `BX LR` | 16 + 16 testes |
| `00280708` | hook_pad() | `BX LR` | 16 + 16 testes |
| `0028070c` | hook_pad2() | `BX LR` | 16 + 16 testes |
| `00280710` | hook_drive_connect_chrmove() | `BX LR` | 16 + 16 testes |
| `00280714` | hook_drive_connect_chrmove2(int) | `BX LR` | 16 + 16 testes |
| `002807f4` | hook_cliptest() | `BX LR` | 16 + 16 testes |
| `002807f8` | chk_RefLine(int) | `BX LR` | 16 + 16 testes |
| `002807fc` | hook_drive_chr(int) | `BX LR` | 16 + 16 testes |
| `00280800` | hook_fix_bugno_931(int) | `BX LR` | 16 + 16 testes |
| `00280804` | hook_win_tail() | `BX LR` | 16 + 16 testes |
| `00280808` | hook_allSkipTest() | `BX LR` | 16 + 16 testes |
| `00280854` | iOS_hook_line() | `BX LR` | 16 + 16 testes |
| `002809c8` | iOS_hook_num() | `BX LR` | 16 + 16 testes |
| `002815d8` | hook_num(int, int, int) | `BX LR` | 16 + 16 testes |
| `002815e4` | chk_test_addcolor(unsigned int*) | `BX LR` | 16 + 16 testes |
| `00281640` | hook_disp_plateorspell(int*) | `BX LR` | 16 + 16 testes |
| `00281644` | hook_code_soundeffect(int) | `BX LR` | 16 + 16 testes |
| `00281648` | hook_1284(char*, int) | `BX LR` | 16 + 16 testes |
| `00286124` | SetSpadStack(unsigned long) | `BX LR` | 16 + 16 testes |
| `00286128` | ResetSpadStack() | `BX LR` | 16 + 16 testes |
| `00286744` | rsetmovie_title_flg__Fv() | `BX LR` | 16 + 16 testes |
| `00286748` | setmovie_title_flg__Fv() | `BX LR` | 16 + 16 testes |
| `00286a30` | pspNetSetPadPushTiming(unsigned long) | `BX LR` | 16 + 16 testes |
| `00286a94` | timer_print_screen() | `BX LR` | 16 + 16 testes |
| `00286a98` | val_letter(int, int, int) | `BX LR` | 16 + 16 testes |
| `00286a9c` | set_nettimer_flag(int, int) | `BX LR` | 16 + 16 testes |
| `00286ae8` | net_control_ex(void*, void*, int) | `BX LR` | 16 + 16 testes |
| `00286e88` | pspNetAgreementInterruptInit() | `BX LR` | 16 + 16 testes |
| `00286e8c` | pspNetCheckRivalAction() | `BX LR` | 16 + 16 testes |
| `00286e90` | rivalCameraWorkProcs() | `BX LR` | 16 + 16 testes |
| `00286ec4` | check_rival_value(int) | `BX LR` | 16 + 16 testes |
| `00287084` | pspNetCheckTrapOnlyStatus(int) | `BX LR` | 16 + 16 testes |
| `00287090` | pspNetTrapDeliveryInit(char) | `BX LR` | 16 + 16 testes |
| `00287584` | load_iconpackdata() | `BX LR` | 16 + 16 testes |
| `002875a0` | draw_maru(unsigned long*) | `BX LR` | 16 + 16 testes |
| `002875a4` | draw_batu(unsigned long*) | `BX LR` | 16 + 16 testes |
| `00287a14` | Red_Blue_Draw(int) | `BX LR` | 16 + 16 testes |
| `00288498` | Draw_TuusinIcon(int, int, unsigned long*) | `BX LR` | 16 + 16 testes |
| `0028849c` | Draw_Trap_CancelCommandList(int*, int, int, unsigned long*) | `BX LR` | 16 + 16 testes |
| `002884c8` | NetBattleJudge() | `BX LR` | 16 + 16 testes |
| `002884fc` | setRewardLv(int) | `BX LR` | 16 + 16 testes |
| `00288508` | CalcRewardLv() | `BX LR` | 16 + 16 testes |
| `0028850c` | CalcMissionPayPoint(int) | `BX LR` | 16 + 16 testes |
| `00288510` | Final_CalcMissionPayPoint() | `BX LR` | 16 + 16 testes |
| `0028856c` | init_AnimList() | `BX LR` | 16 + 16 testes |
| `0028b460` | SpuInit | `BX LR` | 16 + 16 testes |
| `0028b464` | SpuInitHot | `BX LR` | 16 + 16 testes |
| `0028b468` | SpuQuit | `BX LR` | 16 + 16 testes |
| `0028b46c` | SetMem | `BX LR` | 16 + 16 testes |
| `0028b490` | StSetRing | `BX LR` | 16 + 16 testes |
| `0028b494` | StClearRing | `BX LR` | 16 + 16 testes |
| `0028b498` | StUnSetRing | `BX LR` | 16 + 16 testes |
| `0028b49c` | StSetStream | `BX LR` | 16 + 16 testes |
| `0028b4a0` | StSetEmulate | `BX LR` | 16 + 16 testes |
| `0028b4c4` | StRingStatus | `BX LR` | 16 + 16 testes |
| `0028b4c8` | StSetMask | `BX LR` | 16 + 16 testes |
| `0028b4cc` | StCdInterrupt | `BX LR` | 16 + 16 testes |
| `0028b4e0` | DecDCTReset | `BX LR` | 16 + 16 testes |
| `0028b4ec` | DecDCTout | `BX LR` | 16 + 16 testes |
| `0028b508` | pspMovieEnd__Fv() | `BX LR` | 16 + 16 testes |
| `0028b50c` | pspMovieInit__FiPCciiii(int, char*, int, int, int, int) | `BX LR` | 16 + 16 testes |
| `0028b510` | pspMoviePlay__Fv() | `BX LR` | 16 + 16 testes |
| `0028b514` | pspMovieStart__Fv() | `BX LR` | 16 + 16 testes |
| `0028b518` | setMoviePlayFlg__Fi(int) | `BX LR` | 16 + 16 testes |
| `0028b51c` | setMovieSkipFlg__Fi(int) | `BX LR` | 16 + 16 testes |
| `0028b530` | setToolBgmFlg__Fi(int) | `BX LR` | 16 + 16 testes |
| `0028b53c` | setBgmData__Fii(int, int) | `BX LR` | 16 + 16 testes |
| `0028b540` | CdFlush | `BX LR` | 16 + 16 testes |
| `0028b60c` | CdReadBreak | `BX LR` | 16 + 16 testes |
| `0028c200` | CFFT_STATE::~CFFT_STATE() | `BX LR` | 16 + 16 testes |
| `0028c7e8` | CAUTOSAVE::~CAUTOSAVE() | `BX LR` | 16 + 16 testes |
| `0028cea8` | KanjiFntClose | `BX LR` | 16 + 16 testes |
| `0028cedc` | CatPrim | `BX LR` | 16 + 16 testes |
| `0028cee0` | DrawOTagIO | `BX LR` | 16 + 16 testes |
| `0028cee4` | DrawOTagEnv | `BX LR` | 16 + 16 testes |
| `0028cee8` | DumpClut | `BX LR` | 16 + 16 testes |
| `0028ceec` | DumpDispEnv | `BX LR` | 16 + 16 testes |
| `0028cef0` | DumpDrawEnv | `BX LR` | 16 + 16 testes |
| `0028cef4` | DumpOTag | `BX LR` | 16 + 16 testes |
| `0028cef8` | DumpTPage | `BX LR` | 16 + 16 testes |
| `0028cefc` | SetDumpFnt | `BX LR` | 16 + 16 testes |
| `0028cf00` | TermPrim | `BX LR` | 16 + 16 testes |
| `0028cf0c` | ContinueDraw | `BX LR` | 16 + 16 testes |
| `0028cf28` | GetDrawMode | `BX LR` | 16 + 16 testes |
| `0028cf2c` | GetTexWindow | `BX LR` | 16 + 16 testes |
| `0028cf30` | GetDrawArea | `BX LR` | 16 + 16 testes |
| `0028cf34` | GetDrawOffset | `BX LR` | 16 + 16 testes |
| `0028cf38` | GetDrawEnv2 | `BX LR` | 16 + 16 testes |
| `0028de70` | _bu_init | `BX LR` | 16 + 16 testes |
| `00290e90` | FntLoad | `BX LR` | 16 + 16 testes |
| `00292708` | xpLibgpuDrawCallBackSet | `BX LR` | 16 + 16 testes |
| `0029551c` | xpLibgpuBuffersSet | `BX LR` | 16 + 16 testes |
| `00295568` | xpLibgpuMoveImage | `BX LR` | 16 + 16 testes |
| `0029b3e8` | iOS_chkclutaddr() | `BX LR` | 16 + 16 testes |
| `0029b3ec` | GsInit3D | `BX LR` | 16 + 16 testes |
| `0029da84` | _gte_nop() | `BX LR` | 16 + 16 testes |
| `0029fcfc` | _gte_op12() | `BX LR` | 16 + 16 testes |
| `0029fd04` | _gte_op0() | `BX LR` | 16 + 16 testes |
| `0029fd0c` | _gte_gpf12() | `BX LR` | 16 + 16 testes |
| `0029fd14` | _gte_gpf0() | `BX LR` | 16 + 16 testes |
| `0029fd1c` | _gte_gpl12() | `BX LR` | 16 + 16 testes |
| `0029fd24` | _gte_gpl0() | `BX LR` | 16 + 16 testes |
| `0029fd2c` | _gte_mvmva_core(long) | `BX LR` | 16 + 16 testes |
| `002a1024` | OuterProduct12 | `BX LR` | 16 + 16 testes |
| `002a2ff4` | InitHeap(unsigned long*, unsigned long) | `BX LR` | 16 + 16 testes |
| `002ab710` | sceGuClearColor | `BX LR` | 16 + 16 testes |
| `002ab714` | sceGuClear | `BX LR` | 16 + 16 testes |
| `002ab888` | sceGuAlphaFunc | `BX LR` | 16 + 16 testes |
| `002ab900` | sceGuColorFunc | `BX LR` | 16 + 16 testes |
| `002ab904` | sceGuDisplay | `BX LR` | 16 + 16 testes |
| `002abc88` | sceGuShadeModel | `BX LR` | 16 + 16 testes |
| `002abd1c` | sceGuTexFunc | `BX LR` | 16 + 16 testes |
| `002acb28` | sceGuViewport | `BX LR` | 16 + 16 testes |
| `002b0420` | CAPP_INFO::~CAPP_INFO() | `BX LR` | 16 + 16 testes |
| `002b06b0` | CAPP_INFO::Get() | `BX LR` | 16 + 16 testes |
| `002b142c` | SettingsBundle_Uninit() | `BX LR` | 16 + 16 testes |
| `002b1454` | SettingsBundle_OnDefaultsChanged() | `BX LR` | 16 + 16 testes |
| `002b1f38` | NowLoading_FrameRender() | `BX LR` | 16 + 16 testes |
| `002b3440` | Achievement_Unlock(int) | `BX LR` | 16 + 16 testes |
| `002b36b8` | Boot_Uninit() | `BX LR` | 16 + 16 testes |
| `002b3758` | Error_Uninit() | `BX LR` | 16 + 16 testes |
| `002b5590` | Link_Suspend() | `BX LR` | 16 + 16 testes |
| `002b5594` | Link_Resume() | `BX LR` | 16 + 16 testes |
| `002b5eac` | Logo_Suspend() | `BX LR` | 16 + 16 testes |
| `002b5eb0` | Logo_Resume() | `BX LR` | 16 + 16 testes |
| `002b6bcc` | Main_Resume() | `BX LR` | 16 + 16 testes |
| `002bf1f8` | iOS_hook_request_status(int, int) | `BX LR` | 16 + 16 testes |
| `002c54ac` | Movie_Uninit() | `BX LR` | 16 + 16 testes |
| `002c6ef0` | Settings_Suspend() | `BX LR` | 16 + 16 testes |
| `002c6ef4` | Settings_Resume() | `BX LR` | 16 + 16 testes |
| `002c8abc` | SettingsWnd_Suspend() | `BX LR` | 16 + 16 testes |
| `002c8ac0` | SettingsWnd_Resume() | `BX LR` | 16 + 16 testes |
| `002ccf94` | _Unwind_Complete | `BX LR` | 16 + 16 testes |

Arquivos individuais JSON no artifact do workflow. Eles não são inseridos automaticamente em `semantic-certificates.json`.
