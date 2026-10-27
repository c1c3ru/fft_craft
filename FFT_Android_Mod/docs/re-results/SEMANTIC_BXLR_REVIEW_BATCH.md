# Primeira fila de revisão formal: contratos BX LR

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Execução de origem do CI: `40554628588`

- Contratos locais preparados para revisão: **100**
- Microexecuções **novas neste passo**: **0** (reutiliza as 32 observações ARM/Thumb por candidato).
- Certificados integrais emitidos automaticamente: **0**.

**Nenhuma função está certificada por este pacote.** A revisão independente deve avaliar o escopo de execução normal, interworking, preservação dos registradores, efeitos de memória, alinhamento do LR e casos de exceção excluídos.

| Endereço | Função | Opcode original | Testes anteriores | Estado |
|---|---|---|---:|---|
| `002712cc` | Ssd_SetStereo(int) | `1eff2fe1` | 32 | revisão pendente |
| `002712d8` | Ssd_SetAttenuator(short) | `1eff2fe1` | 32 | revisão pendente |
| `002712dc` | Ssd_SetReverbParam(long, short, long, long) | `1eff2fe1` | 32 | revisão pendente |
| `002712e0` | Ssd_SetSpuVolume(short, short) | `1eff2fe1` | 32 | revisão pendente |
| `002712e4` | Ssd_SetCDVolume(short, short) | `1eff2fe1` | 32 | revisão pendente |
| `002712e8` | Ssd_SetCDMixingReverb(int, int) | `1eff2fe1` | 32 | revisão pendente |
| `002712ec` | Ssd_CheckWideMode() | `1eff2fe1` | 32 | revisão pendente |
| `002712f0` | Ssd_SetVolumeRec(short, SpuVolume*, char) | `1eff2fe1` | 32 | revisão pendente |
| `002712f4` | Ssd_ErrorProc(int) | `1eff2fe1` | 32 | revisão pendente |
| `002712f8` | Ssd_AddVagPackData(void*) | `1eff2fe1` | 32 | revisão pendente |
| `00271304` | Ssd_DisposeMusic(SsdSeqRec*) | `1eff2fe1` | 32 | revisão pendente |
| `00271308` | Ssd_LinkMusicData(SsdSeqRec*, void*) | `1eff2fe1` | 32 | revisão pendente |
| `0027130c` | Ssd_StartMusic(SsdSeqRec*, short, short) | `1eff2fe1` | 32 | revisão pendente |
| `00271310` | Ssd_StopMusic(SsdSeqRec*) | `1eff2fe1` | 32 | revisão pendente |
| `00271340` | Ssd_PlayEffects03(long, long, long, long) | `1eff2fe1` | 32 | revisão pendente |
| `00271348` | Ssd_StopEffectSet(void*) | `1eff2fe1` | 32 | revisão pendente |
| `00271410` | Ssd_InitEffectTrackRecWithStart(short, long, short, short) | `1eff2fe1` | 32 | revisão pendente |
| `00271414` | Ssd_SetSeqMasterVolume(SsdSeqRec*, short, short) | `1eff2fe1` | 32 | revisão pendente |
| `00271418` | Ssd_SetSeqMasterTempo(SsdSeqRec*, short, short) | `1eff2fe1` | 32 | revisão pendente |
| `0027141c` | Ssd_SetSeqMasterPitch(SsdSeqRec*, short, short) | `1eff2fe1` | 32 | revisão pendente |
| `00271420` | Ssd_SetSeqMasterPanpot(SsdSeqRec*, short, short) | `1eff2fe1` | 32 | revisão pendente |
| `0027b510` | dispCmdKind() | `1eff2fe1` | 32 | revisão pendente |
| `0027b5c8` | rprintfr(RECT16*, int, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `0027b670` | iOS_DEBUG_multiwindow_break_hook(unsigned long*) | `1eff2fe1` | 32 | revisão pendente |
| `0027b674` | iOS_DEBUG_multiwindow_break_hook2(unsigned long*, int) | `1eff2fe1` | 32 | revisão pendente |
| `0027b678` | iOS_DEBUG_multiwindow_keyright_hook() | `1eff2fe1` | 32 | revisão pendente |
| `0027fc28` | chk_ucResumeData2(int) | `1eff2fe1` | 32 | revisão pendente |
| `0027fc2c` | chk_ucResumeData(unsigned char*, int) | `1eff2fe1` | 32 | revisão pendente |
| `0027fc7c` | cSaveFFT::~cSaveFFT() | `1eff2fe1` | 32 | revisão pendente |
| `002805e4` | iOS_hookHelp(int*) | `1eff2fe1` | 32 | revisão pendente |
| `00280614` | iOS_hook_disp_option() | `1eff2fe1` | 32 | revisão pendente |
| `00280618` | iOS_hook_disp_optionmain() | `1eff2fe1` | 32 | revisão pendente |
| `0028061c` | iOS_hook_common(char const*, int) | `1eff2fe1` | 32 | revisão pendente |
| `00280670` | hook_write_eventflag(int, int) | `1eff2fe1` | 32 | revisão pendente |
| `00280674` | hook_calcformula(int, int) | `1eff2fe1` | 32 | revisão pendente |
| `00280678` | hook_Debug(char const*) | `1eff2fe1` | 32 | revisão pendente |
| `0028067c` | hook_Debug2(char const*) | `1eff2fe1` | 32 | revisão pendente |
| `00280680` | hook_NextEventSet() | `1eff2fe1` | 32 | revisão pendente |
| `00280684` | hook_musiclod() | `1eff2fe1` | 32 | revisão pendente |
| `002806b0` | iOS_hook_worldhelpmenu() | `1eff2fe1` | 32 | revisão pendente |
| `002806b4` | iOS_hook_gill() | `1eff2fe1` | 32 | revisão pendente |
| `002806b8` | iOS_hook_movetopanel() | `1eff2fe1` | 32 | revisão pendente |
| `002806bc` | hook_read_eventflag(int*) | `1eff2fe1` | 32 | revisão pendente |
| `002806c0` | hook_allocate_texture() | `1eff2fe1` | 32 | revisão pendente |
| `002806c4` | hook_opt() | `1eff2fe1` | 32 | revisão pendente |
| `002806c8` | hook_chk_speedup(int) | `1eff2fe1` | 32 | revisão pendente |
| `00280708` | hook_pad() | `1eff2fe1` | 32 | revisão pendente |
| `0028070c` | hook_pad2() | `1eff2fe1` | 32 | revisão pendente |
| `00280710` | hook_drive_connect_chrmove() | `1eff2fe1` | 32 | revisão pendente |
| `00280714` | hook_drive_connect_chrmove2(int) | `1eff2fe1` | 32 | revisão pendente |
| `002807f4` | hook_cliptest() | `1eff2fe1` | 32 | revisão pendente |
| `002807f8` | chk_RefLine(int) | `1eff2fe1` | 32 | revisão pendente |
| `002807fc` | hook_drive_chr(int) | `1eff2fe1` | 32 | revisão pendente |
| `00280800` | hook_fix_bugno_931(int) | `1eff2fe1` | 32 | revisão pendente |
| `00280804` | hook_win_tail() | `1eff2fe1` | 32 | revisão pendente |
| `00280808` | hook_allSkipTest() | `1eff2fe1` | 32 | revisão pendente |
| `00280854` | iOS_hook_line() | `1eff2fe1` | 32 | revisão pendente |
| `002809c8` | iOS_hook_num() | `1eff2fe1` | 32 | revisão pendente |
| `002815d8` | hook_num(int, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `002815e4` | chk_test_addcolor(unsigned int*) | `1eff2fe1` | 32 | revisão pendente |
| `00281640` | hook_disp_plateorspell(int*) | `1eff2fe1` | 32 | revisão pendente |
| `00281644` | hook_code_soundeffect(int) | `1eff2fe1` | 32 | revisão pendente |
| `00281648` | hook_1284(char*, int) | `1eff2fe1` | 32 | revisão pendente |
| `00286124` | SetSpadStack(unsigned long) | `1eff2fe1` | 32 | revisão pendente |
| `00286128` | ResetSpadStack() | `1eff2fe1` | 32 | revisão pendente |
| `00286744` | rsetmovie_title_flg__Fv() | `1eff2fe1` | 32 | revisão pendente |
| `00286748` | setmovie_title_flg__Fv() | `1eff2fe1` | 32 | revisão pendente |
| `00286a30` | pspNetSetPadPushTiming(unsigned long) | `1eff2fe1` | 32 | revisão pendente |
| `00286a94` | timer_print_screen() | `1eff2fe1` | 32 | revisão pendente |
| `00286a98` | val_letter(int, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `00286a9c` | set_nettimer_flag(int, int) | `1eff2fe1` | 32 | revisão pendente |
| `00286ae8` | net_control_ex(void*, void*, int) | `1eff2fe1` | 32 | revisão pendente |
| `00286e88` | pspNetAgreementInterruptInit() | `1eff2fe1` | 32 | revisão pendente |
| `00286e8c` | pspNetCheckRivalAction() | `1eff2fe1` | 32 | revisão pendente |
| `00286e90` | rivalCameraWorkProcs() | `1eff2fe1` | 32 | revisão pendente |
| `00286ec4` | check_rival_value(int) | `1eff2fe1` | 32 | revisão pendente |
| `00287084` | pspNetCheckTrapOnlyStatus(int) | `1eff2fe1` | 32 | revisão pendente |
| `00287090` | pspNetTrapDeliveryInit(char) | `1eff2fe1` | 32 | revisão pendente |
| `00287584` | load_iconpackdata() | `1eff2fe1` | 32 | revisão pendente |
| `002875a0` | draw_maru(unsigned long*) | `1eff2fe1` | 32 | revisão pendente |
| `002875a4` | draw_batu(unsigned long*) | `1eff2fe1` | 32 | revisão pendente |
| `00287a14` | Red_Blue_Draw(int) | `1eff2fe1` | 32 | revisão pendente |
| `00288498` | Draw_TuusinIcon(int, int, unsigned long*) | `1eff2fe1` | 32 | revisão pendente |
| `0028849c` | Draw_Trap_CancelCommandList(int*, int, int, unsigned long*) | `1eff2fe1` | 32 | revisão pendente |
| `002884c8` | NetBattleJudge() | `1eff2fe1` | 32 | revisão pendente |
| `002884fc` | setRewardLv(int) | `1eff2fe1` | 32 | revisão pendente |
| `00288508` | CalcRewardLv() | `1eff2fe1` | 32 | revisão pendente |
| `0028850c` | CalcMissionPayPoint(int) | `1eff2fe1` | 32 | revisão pendente |
| `00288510` | Final_CalcMissionPayPoint() | `1eff2fe1` | 32 | revisão pendente |
| `0028856c` | init_AnimList() | `1eff2fe1` | 32 | revisão pendente |
| `0028b460` | SpuInit | `1eff2fe1` | 32 | revisão pendente |
| `0028b464` | SpuInitHot | `1eff2fe1` | 32 | revisão pendente |
| `0028b468` | SpuQuit | `1eff2fe1` | 32 | revisão pendente |
| `0028b46c` | SetMem | `1eff2fe1` | 32 | revisão pendente |
| `0028b490` | StSetRing | `1eff2fe1` | 32 | revisão pendente |
| `0028b494` | StClearRing | `1eff2fe1` | 32 | revisão pendente |
| `0028b498` | StUnSetRing | `1eff2fe1` | 32 | revisão pendente |
| `0028b49c` | StSetStream | `1eff2fe1` | 32 | revisão pendente |
| `0028b4a0` | StSetEmulate | `1eff2fe1` | 32 | revisão pendente |
| `0028b4c4` | StRingStatus | `1eff2fe1` | 32 | revisão pendente |

## Como concluir a revisão

1. Conferir os registros individuais em `SEMANTIC_BXLR_REVIEW_BATCH.json` com o ELF original.
2. Verificar as pré/pós-condições e documentar ressalvas; o escopo **não** cobre o programa completo.
3. Submeter proposta explícita de certificados ao ledger em PR separado; jamais copiar aprovação fictícia de uma fixture.
4. Obter revisão independente registrada no GitHub. O gate verifica PR, identidade, commit, endereço e bytes do ELF antes de contar qualquer certificado.

Este arquivo é uma fila de revisão e não uma declaração de equivalência semântica integral.
