# Candidatas de contrato semântico: folhas ARM BX LR

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

- Entradas ARM de 4 bytes inspecionadas: **473**
- Candidatas com opcode exato `E12FFF1E`: **303**
- Microexecuções Unicorn válidas: **1212**

> Cada teste executa o opcode **original** do ELF e verifica PC, registradores, CPSR e ausência de acessos a dados. **Não constitui certificação semântica integral:** a cobertura formal dos estados e a revisão da equivalência continuam pendentes.

| Endereço | Função | Testes |
|---|---|---:|
| `000a6d5c` | CGX_SCREEN_CORRECT::~CGX_SCREEN_CORRECT() | 4 |
| `000a7e78` | CEGL2_IF::Setup3D() | 4 |
| `000a8560` | CEGL2_IF::DrawGrid() | 4 |
| `000a8564` | CEGL2_IF::DrawAxis() | 4 |
| `000a8568` | CEGL2_IF::DrawCross(math::VECTOR3<float>, float) | 4 |
| `000af9bc` | CCAMERA::Uninit() | 4 |
| `000b3524` | CINPUT_DATA::~CINPUT_DATA() | 4 |
| `000b4f70` | CRECT::CRECT() | 4 |
| `000b4f74` | CRECT::~CRECT() | 4 |
| `000b5524` | CRECT::MoveCursor(int) | 4 |
| `000b5528` | CRECT::MoveCursorPos(int, int) | 4 |
| `000b61d4` | CCOMP_Z_DEC::~CCOMP_Z_DEC() | 4 |
| `000b6200` | CCOMP_Z_DEC::Error(char const*) | 4 |
| `000b63a0` | CCOMP_Z_ENC::~CCOMP_Z_ENC() | 4 |
| `000b63cc` | CCOMP_Z_ENC::Error(char const*) | 4 |
| `000b6580` | CCRYPT::CCRYPT() | 4 |
| `000b6584` | CCRYPT::~CCRYPT() | 4 |
| `000b789c` | CFILE_UTIL::CFILE_UTIL() | 4 |
| `000b78a0` | CFILE_UTIL::~CFILE_UTIL() | 4 |
| `000b7988` | CFILE_UTIL::DirGetWindows(char*) | 4 |
| `000b798c` | CFILE_UTIL::DirGetSystem(char*) | 4 |
| `000b7998` | CFILE_UTIL::DirGetExecute(char*, char*) | 4 |
| `000b8bdc` | CSTR_UTIL::CSTR_UTIL() | 4 |
| `000b8be0` | CSTR_UTIL::~CSTR_UTIL() | 4 |
| `000bb834` | CSOUND_IF_SL::FrameMove(int, float) | 4 |
| `000bbb10` | CSOUND_IF_SL::SetTrans(int, float, float, float) | 4 |
| `000bcbf0` | CSOUND_LOADER::FrameMove(int, float) | 4 |
| `000bd964` | CFRAMERATE::~CFRAMERATE() | 4 |
| `000bdb6c` | CSTEP::~CSTEP() | 4 |
| `000c4418` | Adisp_floateventwindow() | 4 |
| `000c4494` | Aitemmenu_call(unsigned long*, unsigned long, int) | 4 |
| `000c4498` | attackdebugfunc() | 4 |
| `000cbd50` | SetTrapNameWindowParam(int, short, int) | 4 |
| `000cbd54` | TrapNameWindowManager() | 4 |
| `000cbd58` | CreateTrapNameWindowManagerTask() | 4 |
| `000cbd5c` | deleteEndModeWindow() | 4 |
| `000cbd60` | SetTrapNameWindowColor(int) | 4 |
| `000cbd64` | CreateTrapCancelCommandWindow() | 4 |
| `000cbd68` | DeleteTrapCancelCommandWindow() | 4 |
| `000cbd74` | CreateNetStayWindow() | 4 |
| `000d0dc8` | Ddisp_floateventwindow() | 4 |
| `000d1408` | Ditemmenu_call(unsigned long*, unsigned long, int) | 4 |
| `000d6f80` | iOS_chkallocatewindowinit() | 4 |
| `000d7384` | disposewindowbytask(int) | 4 |
| `000d8970` | dispemptywindow() | 4 |
| `000d8974` | send_statuschrno(int) | 4 |
| `000d8bfc` | initstatuscphase() | 4 |
| `000d9a08` | hook_disp_requirement() | 4 |
| `000d9a0c` | hook_trophics() | 4 |
| `000d9a10` | seekpcfile(char*, char*, int, int) | 4 |
| `000d9ac0` | loadonefile(char*, char*) | 4 |
| `000d9b0c` | request_tooltest() | 4 |
| `000da334` | request_effectmes(int, int, int, int) | 4 |
| `000da338` | request_warnmes(int, int, int, int) | 4 |
| `000e62c4` | DEBUGTRACE_hook_connect_camera() | 4 |
| `000e62c8` | DEBUG_CHK_ROLL(SCROLLRECORD*) | 4 |
| `000e7f0c` | dmp_tuto(unsigned char*, int) | 4 |
| `000feaa4` | WiOS_chkallocatewindowinit() | 4 |
| `00100640` | Wdispemptywindow() | 4 |
| `00100644` | Wsend_statuschrno(int) | 4 |
| `00100840` | Winitstatuscphase() | 4 |
| `00101908` | Whook_disp_requirement() | 4 |
| `0010190c` | Whook_trophics() | 4 |
| `00101910` | Wseekpcfile(char*, char*, int, int) | 4 |
| `001019bc` | Wloadonefile(char*, char*) | 4 |
| `00101a0c` | Wrequest_tooltest() | 4 |
| `00101f9c` | Wrequest_effectmes(int, int, int, int) | 4 |
| `00101fa0` | Wrequest_warnmes(int, int, int, int) | 4 |
| `00102128` | Wevent_init_light() | 4 |
| `00121718` | Edisp_floateventwindow() | 4 |
| `00123c40` | Eitemmenu_call(unsigned long*, unsigned long, int) | 4 |
| `0012b108` | disp_floateventwindow() | 4 |
| `0014b9f8` | Cdisp_floateventwindow() | 4 |
| `0014bec4` | Citemmenu_call(unsigned long*, unsigned long, int) | 4 |
| `0014e0e8` | statushookfunc() | 4 |
| `0014e9a0` | sol_draw(int, int, int) | 4 |
| `00155708` | story_faceload() | 4 |
| `0015f044` | iOSUnitListLRCurSet(unsigned char*, unsigned short*, int, int, int, int) | 4 |
| `00161d98` | tDebugBreakCheck(int) | 4 |
| `00161d9c` | tDebugBreakTime(int) | 4 |
| `00161da0` | tDebugPointerErr() | 4 |
| `0016f840` | cCardInit() | 4 |
| `001836cc` | iOS_addPrim_window(tagPOLY_FT4*) | 4 |
| `0018372c` | CardInit() | 4 |
| `0019e7b4` | shop_dummyfunc() | 4 |
| `001add64` | unit_dummyfunc() | 4 |
| `001d114c` | set_monomane_direction(BWORK*, unsigned char) | 4 |
| `001dca54` | callSW(int) | 4 |
| `001e7368` | pspNetTrapSpread(BWORK*, int) | 4 |
| `00202f1c` | pspNetOutPutAnimationData() | 4 |
| `0020c258` | fftDrawSyncCallback() | 4 |
| `0020c25c` | fftCdReadyCallback() | 4 |
| `0020c260` | fftCdReadCallback() | 4 |
| `0020c5cc` | myPollhost() | 4 |
| `0020c5d0` | system_error(int, int) | 4 |
| `0020c5d4` | system_warning(int, int) | 4 |
| `0020f4f8` | getCharPrimList(short, Point*, unsigned long*) | 4 |
| `0020f904` | iOS_dispAnimetion() | 4 |
| `0020fb14` | initializeDebugFont() | 4 |
| `00215d5c` | PadStop | 4 |

Demais 203 registros: arquivos JSON por endereço.

A fila de certificação deve revisar os contratos e seus domínios antes de promover qualquer candidato.
