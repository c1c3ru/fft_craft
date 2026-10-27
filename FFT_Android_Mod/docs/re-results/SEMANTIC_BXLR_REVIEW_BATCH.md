# Primeira fila de revisão formal: contratos BX LR

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Execução de origem do CI: `40550839542`

- Contratos locais preparados para revisão: **100**
- Microexecuções **novas neste passo**: **0** (reutiliza as 32 observações ARM/Thumb por candidato).
- Certificados integrais emitidos automaticamente: **0**.

**Nenhuma função está certificada por este pacote.** A revisão independente deve avaliar o escopo de execução normal, interworking, preservação dos registradores, efeitos de memória, alinhamento do LR e casos de exceção excluídos.

| Endereço | Função | Opcode original | Testes anteriores | Estado |
|---|---|---|---:|---|
| `000bbb10` | CSOUND_IF_SL::SetTrans(int, float, float, float) | `1eff2fe1` | 32 | revisão pendente |
| `000bcbf0` | CSOUND_LOADER::FrameMove(int, float) | `1eff2fe1` | 32 | revisão pendente |
| `000bd964` | CFRAMERATE::~CFRAMERATE() | `1eff2fe1` | 32 | revisão pendente |
| `000bdb6c` | CSTEP::~CSTEP() | `1eff2fe1` | 32 | revisão pendente |
| `000c4418` | Adisp_floateventwindow() | `1eff2fe1` | 32 | revisão pendente |
| `000c4494` | Aitemmenu_call(unsigned long*, unsigned long, int) | `1eff2fe1` | 32 | revisão pendente |
| `000c4498` | attackdebugfunc() | `1eff2fe1` | 32 | revisão pendente |
| `000cbd50` | SetTrapNameWindowParam(int, short, int) | `1eff2fe1` | 32 | revisão pendente |
| `000cbd54` | TrapNameWindowManager() | `1eff2fe1` | 32 | revisão pendente |
| `000cbd58` | CreateTrapNameWindowManagerTask() | `1eff2fe1` | 32 | revisão pendente |
| `000cbd5c` | deleteEndModeWindow() | `1eff2fe1` | 32 | revisão pendente |
| `000cbd60` | SetTrapNameWindowColor(int) | `1eff2fe1` | 32 | revisão pendente |
| `000cbd64` | CreateTrapCancelCommandWindow() | `1eff2fe1` | 32 | revisão pendente |
| `000cbd68` | DeleteTrapCancelCommandWindow() | `1eff2fe1` | 32 | revisão pendente |
| `000cbd74` | CreateNetStayWindow() | `1eff2fe1` | 32 | revisão pendente |
| `000d0dc8` | Ddisp_floateventwindow() | `1eff2fe1` | 32 | revisão pendente |
| `000d1408` | Ditemmenu_call(unsigned long*, unsigned long, int) | `1eff2fe1` | 32 | revisão pendente |
| `000d6f80` | iOS_chkallocatewindowinit() | `1eff2fe1` | 32 | revisão pendente |
| `000d7384` | disposewindowbytask(int) | `1eff2fe1` | 32 | revisão pendente |
| `000d8970` | dispemptywindow() | `1eff2fe1` | 32 | revisão pendente |
| `000d8974` | send_statuschrno(int) | `1eff2fe1` | 32 | revisão pendente |
| `000d8bfc` | initstatuscphase() | `1eff2fe1` | 32 | revisão pendente |
| `000d9a08` | hook_disp_requirement() | `1eff2fe1` | 32 | revisão pendente |
| `000d9a0c` | hook_trophics() | `1eff2fe1` | 32 | revisão pendente |
| `000d9a10` | seekpcfile(char*, char*, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `000d9ac0` | loadonefile(char*, char*) | `1eff2fe1` | 32 | revisão pendente |
| `000d9b0c` | request_tooltest() | `1eff2fe1` | 32 | revisão pendente |
| `000da334` | request_effectmes(int, int, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `000da338` | request_warnmes(int, int, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `000e62c4` | DEBUGTRACE_hook_connect_camera() | `1eff2fe1` | 32 | revisão pendente |
| `000e62c8` | DEBUG_CHK_ROLL(SCROLLRECORD*) | `1eff2fe1` | 32 | revisão pendente |
| `000e7f0c` | dmp_tuto(unsigned char*, int) | `1eff2fe1` | 32 | revisão pendente |
| `000feaa4` | WiOS_chkallocatewindowinit() | `1eff2fe1` | 32 | revisão pendente |
| `00100640` | Wdispemptywindow() | `1eff2fe1` | 32 | revisão pendente |
| `00100644` | Wsend_statuschrno(int) | `1eff2fe1` | 32 | revisão pendente |
| `00100840` | Winitstatuscphase() | `1eff2fe1` | 32 | revisão pendente |
| `00101908` | Whook_disp_requirement() | `1eff2fe1` | 32 | revisão pendente |
| `0010190c` | Whook_trophics() | `1eff2fe1` | 32 | revisão pendente |
| `00101910` | Wseekpcfile(char*, char*, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `001019bc` | Wloadonefile(char*, char*) | `1eff2fe1` | 32 | revisão pendente |
| `00101a0c` | Wrequest_tooltest() | `1eff2fe1` | 32 | revisão pendente |
| `00101f9c` | Wrequest_effectmes(int, int, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `00101fa0` | Wrequest_warnmes(int, int, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `00102128` | Wevent_init_light() | `1eff2fe1` | 32 | revisão pendente |
| `00121718` | Edisp_floateventwindow() | `1eff2fe1` | 32 | revisão pendente |
| `00123c40` | Eitemmenu_call(unsigned long*, unsigned long, int) | `1eff2fe1` | 32 | revisão pendente |
| `0012b108` | disp_floateventwindow() | `1eff2fe1` | 32 | revisão pendente |
| `0014b9f8` | Cdisp_floateventwindow() | `1eff2fe1` | 32 | revisão pendente |
| `0014bec4` | Citemmenu_call(unsigned long*, unsigned long, int) | `1eff2fe1` | 32 | revisão pendente |
| `0014e0e8` | statushookfunc() | `1eff2fe1` | 32 | revisão pendente |
| `0014e9a0` | sol_draw(int, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `00155708` | story_faceload() | `1eff2fe1` | 32 | revisão pendente |
| `0015f044` | iOSUnitListLRCurSet(unsigned char*, unsigned short*, int, int, int, int) | `1eff2fe1` | 32 | revisão pendente |
| `00161d98` | tDebugBreakCheck(int) | `1eff2fe1` | 32 | revisão pendente |
| `00161d9c` | tDebugBreakTime(int) | `1eff2fe1` | 32 | revisão pendente |
| `00161da0` | tDebugPointerErr() | `1eff2fe1` | 32 | revisão pendente |
| `0016f840` | cCardInit() | `1eff2fe1` | 32 | revisão pendente |
| `001836cc` | iOS_addPrim_window(tagPOLY_FT4*) | `1eff2fe1` | 32 | revisão pendente |
| `0018372c` | CardInit() | `1eff2fe1` | 32 | revisão pendente |
| `0019e7b4` | shop_dummyfunc() | `1eff2fe1` | 32 | revisão pendente |
| `001add64` | unit_dummyfunc() | `1eff2fe1` | 32 | revisão pendente |
| `001d114c` | set_monomane_direction(BWORK*, unsigned char) | `1eff2fe1` | 32 | revisão pendente |
| `001dca54` | callSW(int) | `1eff2fe1` | 32 | revisão pendente |
| `001e7368` | pspNetTrapSpread(BWORK*, int) | `1eff2fe1` | 32 | revisão pendente |
| `00202f1c` | pspNetOutPutAnimationData() | `1eff2fe1` | 32 | revisão pendente |
| `0020c258` | fftDrawSyncCallback() | `1eff2fe1` | 32 | revisão pendente |
| `0020c25c` | fftCdReadyCallback() | `1eff2fe1` | 32 | revisão pendente |
| `0020c260` | fftCdReadCallback() | `1eff2fe1` | 32 | revisão pendente |
| `0020c5cc` | myPollhost() | `1eff2fe1` | 32 | revisão pendente |
| `0020c5d0` | system_error(int, int) | `1eff2fe1` | 32 | revisão pendente |
| `0020c5d4` | system_warning(int, int) | `1eff2fe1` | 32 | revisão pendente |
| `0020f4f8` | getCharPrimList(short, Point*, unsigned long*) | `1eff2fe1` | 32 | revisão pendente |
| `0020f904` | iOS_dispAnimetion() | `1eff2fe1` | 32 | revisão pendente |
| `0020fb14` | initializeDebugFont() | `1eff2fe1` | 32 | revisão pendente |
| `00215d5c` | PadStop | `1eff2fe1` | 32 | revisão pendente |
| `002168fc` | recallEnvEffect() | `1eff2fe1` | 32 | revisão pendente |
| `002169cc` | pauseEnvEffect() | `1eff2fe1` | 32 | revisão pendente |
| `0021ebb0` | error(char, long) | `1eff2fe1` | 32 | revisão pendente |
| `00225310` | iOS_CheckPEffect(char const*, int) | `1eff2fe1` | 32 | revisão pendente |
| `00225a60` | objectLG2(_EffectTCB*, _Object*) | `1eff2fe1` | 32 | revisão pendente |
| `00225a64` | dmyFnc2(_EffectTCB*, _Object*) | `1eff2fe1` | 32 | revisão pendente |
| `0022a614` | DumpMemory(int, void*) | `1eff2fe1` | 32 | revisão pendente |
| `002419cc` | fftCdLoop(CDREC*) | `1eff2fe1` | 32 | revisão pendente |
| `002419d0` | fftCdCancel(CDREC*) | `1eff2fe1` | 32 | revisão pendente |
| `002524cc` | ctlworkingst_deactive(CTLINFO*) | `1eff2fe1` | 32 | revisão pendente |
| `00252b68` | ctlworkend_active(CTLINFO*) | `1eff2fe1` | 32 | revisão pendente |
| `00252b6c` | ctlworkend_deactive(CTLINFO*) | `1eff2fe1` | 32 | revisão pendente |
| `00258ac4` | evt_skip0() | `1eff2fe1` | 32 | revisão pendente |
| `0025f354` | wld_btlsect_seek() | `1eff2fe1` | 32 | revisão pendente |
| `00267f38` | wldrute_init() | `1eff2fe1` | 32 | revisão pendente |
| `0026c058` | iOS_debugDispTownCircle(int, int) | `1eff2fe1` | 32 | revisão pendente |
| `0026ff2c` | effectdmy() | `1eff2fe1` | 32 | revisão pendente |
| `0027129c` | Ssd_Quit() | `1eff2fe1` | 32 | revisão pendente |
| `002712a0` | Ssd_Enable() | `1eff2fe1` | 32 | revisão pendente |
| `002712a4` | Ssd_Disable() | `1eff2fe1` | 32 | revisão pendente |
| `002712b0` | Ssd_DisposeNormalWave() | `1eff2fe1` | 32 | revisão pendente |
| `002712b4` | Ssd_DisposeWaveData(SsdWaveSetRec*) | `1eff2fe1` | 32 | revisão pendente |
| `002712c0` | Ssd_AddEffectData(void*) | `1eff2fe1` | 32 | revisão pendente |
| `002712c4` | Ssd_DisposeEffectData(void*) | `1eff2fe1` | 32 | revisão pendente |
| `002712c8` | Ssd_AllStop() | `1eff2fe1` | 32 | revisão pendente |

## Como concluir a revisão

1. Conferir os registros individuais em `SEMANTIC_BXLR_REVIEW_BATCH.json` com o ELF original.
2. Verificar as pré/pós-condições e documentar ressalvas; o escopo **não** cobre o programa completo.
3. Submeter proposta explícita de certificados ao ledger em PR separado; jamais copiar aprovação fictícia de uma fixture.
4. Obter revisão independente registrada no GitHub. O gate verifica PR, identidade, commit, endereço e bytes do ELF antes de contar qualquer certificado.

Este arquivo é uma fila de revisão e não uma declaração de equivalência semântica integral.
