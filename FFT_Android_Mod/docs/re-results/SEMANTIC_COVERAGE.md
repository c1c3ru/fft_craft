# Cobertura semântica verificável — FFT Craft

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

> **Regra:** aprovação estrutural, análise estática e microexecuções parciais não significam equivalência semântica integral.

| Métrica | Quantidade |
|---|---:|
| Entradas/símbolos no inventário | 6,455 |
| Endereços de execução únicos | 6,329 |
| Semântica integral certificada por registro | 5 |
| Evidência parcial registrada | 0 |
| Sem certificação registrada | 6,324 |
| Progresso certificado por endereço | 0.08% |
| Progresso certificado por bytes | 0.00% |

Contagens medem **certificados registrados no ledger**, não a ausência de conhecimento em relatórios anteriores.
Um certificado revisado e testes diferenciais são necessários antes de afirmar equivalência. O esquema não prova completude por si.

## Fila por bytes ainda sem certificação

| Endereço | Função | Bytes | Estado |
|---|---|---:|---|
| `00207e10` | battle() | 17156 | unknown |
| `0011173c` | Wmesputmain() | 16312 | unknown |
| `002c141c` | Main_FrameRender() | 16164 | unknown |
| `0017c27c` | BattleUnitList(unsigned char*, unsigned long*) | 15920 | unknown |
| `000e88c4` | mesputmain() | 15744 | unknown |
| `0016a6a4` | ASHURA_addPrim(MATRIX*) | 15412 | unknown |
| `001aeda0` | ItemMenu() | 13764 | unknown |
| `002bbb74` | Main_FrameMove() | 13272 | unknown |
| `0018aeec` | eItemMenu() | 12580 | unknown |
| `000c5148` | op_attackteam() | 12272 | unknown |
| `00184670` | CardAccess(int) | 11004 | unknown |
| `001506ec` | requireprinf() | 10976 | unknown |
| `00225ac8` | CreateObjectWithTable(short, int, int, _Object*) | 10724 | unknown |
| `0016fc90` | BattleCardAccess(int) | 10448 | unknown |
| `00128ed4` | disp_personalwindow() | 8756 | unknown |
| `0012f2f0` | Wdisp_personalwindow() | 8632 | unknown |
| `0023e29c` | Mdl0024(short, int, int, int) | 8616 | unknown |
| `0022f48c` | Mdl0004(short, int, int, int) | 8420 | unknown |
| `000ce834` | Ddisp_personalwindow() | 7912 | unknown |
| `0011f848` | Edisp_personalwindow() | 7888 | unknown |
| `000c96a0` | Adisp_personalwindow() | 7728 | unknown |
| `00236320` | Mdl0010(short, int, int, int) | 7684 | unknown |
| `0022d69c` | Mdl0003(short, int, int, int) | 7664 | unknown |
| `00234580` | Mdl0009(short, int, int, int) | 7584 | unknown |
| `0014c010` | Cdisp_personalwindow() | 7484 | unknown |
| `000ec908` | disp_scrollwindow() | 7444 | unknown |
| `0023237c` | Mdl0007(short, int, int, int) | 6996 | unknown |
| `001bde2c` | UnitTable(short, short, short, short, short, int (*)(int), int (*)(int), int) | 6976 | unknown |
| `001c0930` | UnitList(int, int) | 6956 | unknown |
| `001a486c` | AbilityMenu() | 6908 | unknown |
| `00238bac` | Mdl0013(short, int, int, int) | 6792 | unknown |
| `0007b200` | inflate | 6652 | unknown |
| `00117374` | Wdisp_scrollwindow() | 6504 | unknown |
| `002ae900` | GuEmu_libgu_to_gl() | 6368 | unknown |
| `001314a8` | Wdisp_floateventwindow() | 6228 | unknown |
| `001b2ea8` | JobChange() | 6216 | unknown |
| `000b1cdc` | gl3stubInit | 6204 | unknown |
| `0014ec70` | resultproc() | 6156 | unknown |
| `00274764` | BattleRoutine(int, ActionRequest*) | 5848 | unknown |
| `002bf3e8` | Main_Init() | 5832 | unknown |
| `000afb30` | CCAMERA::Update() | 5576 | unknown |
| `0022c138` | Mdl0002(short, int, int, int) | 5476 | unknown |
| `000f431c` | event_call(unsigned long*, unsigned long) | 5456 | unknown |
| `0015834c` | world_scrollwindow() | 5236 | unknown |
| `00163ccc` | ASHURA_set_Mesh(int, int) | 5160 | unknown |
| `002b8900` | iOS_SetIconPosition() | 5036 | unknown |
| `0023b310` | Mdl0015(short, int, int, int) | 5024 | unknown |
| `00213e78` | executeChangeClut() | 4976 | unknown |
| `000759e8` | deflate | 4872 | unknown |
| `0022ae34` | Mdl0001(short, int, int, int) | 4868 | unknown |
| `00127360` | Wdisp_helpmenu() | 4808 | unknown |
| `0023c79c` | Mdl0017(short, int, int, int) | 4792 | unknown |
| `0014935c` | Cdisp_bothwindow() | 4780 | unknown |
| `0013f1dc` | battle_scrollwindow() | 4728 | unknown |
| `002406d4` | Mdl0028(short, int, int, int) | 4700 | unknown |
| `000794ec` | inflateBack | 4660 | unknown |
| `001255e0` | disp_helpmenu() | 4628 | unknown |
| `001da9e4` | set_monsterwork_j(BWORK*, EDATA*, int, int) | 4540 | unknown |
| `000e62cc` | iOS_RESUME_SET_EVENT(IOS_RESUME_DATA_EVENT*, IOS_RESUME_DATACOPY_MODE) | 4448 | unknown |
| `000c1e20` | Adisp_bothwindow() | 4260 | unknown |
| `000d1ab0` | debug_chrmenu() | 4244 | unknown |
| `0012b12c` | disp_bothwindow() | 4196 | unknown |
| `000cd5e8` | Ddisp_bothwindow() | 4128 | unknown |
| `00216e5c` | iOS_RESUME_SET_WORK_MU(IOS_RESUME_DATA_WORK_MU*, IOS_RESUME_DATACOPY_MODE) | 4004 | unknown |
| `0013d248` | disp_option(int) | 3996 | unknown |
| `0019e7b8` | Shop(int) | 3936 | unknown |
| `001f1680` | executeShape(tag_animation*) | 3924 | unknown |
| `001156f4` | Wdisp_statusc() | 3880 | unknown |
| `001cda4c` | setskillresult(int) | 3844 | unknown |
| `000ef83c` | disp_statusc() | 3828 | unknown |
| `001431c4` | Wdisp_option(int) | 3828 | unknown |
| `00221f64` | dispPolygonObject(SVECTOR*, VECTOR*, SVECTOR*, VECTOR*, int) | 3816 | unknown |
| `00228ee8` | drawShape2(Shape2*, Point*, short, VECTOR*, unsigned long*) | 3808 | unknown |
| `001a17e8` | GlobalName(unsigned char*, unsigned char*) | 3764 | unknown |
| `00219728` | DoEffectCameraWork() | 3740 | unknown |
| `002b4680` | Link_FrameRender() | 3636 | unknown |
| `00168ba8` | ASHURA_MapProjectMem2Mem(unsigned char, char*) | 3632 | unknown |
| `002adab4` | sceGuSendList | 3544 | unknown |
| `00156bec` | worldmap_call(unsigned long*, unsigned long) | 3520 | unknown |
| `0016e7c8` | ASHURA_GNS_Garage(long, unsigned long) | 3504 | unknown |
| `00178e98` | bWorldJobStts() | 3300 | unknown |
| `00246450` | ctlopentitle_main(CTLINFO*) | 3296 | unknown |
| `0023a634` | Mdl0014(short, int, int, int) | 3292 | unknown |
| `0015c15c` | sBattleTouchToCur(int) | 3284 | unknown |
| `002ace34` | sceGuDrawArray | 3200 | unknown |
| `002210fc` | p04_magicChantFunc() | 3176 | unknown |
| `002542a4` | ctlmap_main(CTLINFO*) | 3124 | unknown |
| `001f3828` | NewAnimation(int, int, int, short, short, short, short, BWORK*, int, void*) | 3096 | unknown |
| `00175a98` | bDB_init(DB*, unsigned long*, tagPOLY_F3*, tagPOLY_FT3*, tagPOLY_F4*, tagPOLY_FT4*, tagPOLY_G3*, tagPOLY_GT3*, tagPOLY_G4*, tagPOLY_GT4*, tagLINE_F2*, tagLINE_F3*, tagLINE_F4*, tagLINE_G2*, tagLINE_G3*, tagLINEG4*, tagTILE*, tagTILE_1*, tagTILE_8*, tagTILE_16*, tagSPRT*, tagSPRT_8*, tagSPRT_16*, DR_MOVE*, DR_AREA*, DR_MODE*) | 3016 | unknown |
| `00165b68` | ASURA_LMDL_TIME_TBL() | 2996 | unknown |
| `001cba40` | calc_result(ACT*, unsigned char) | 2996 | unknown |
| `00166ee0` | ASHURA_Animation() | 2976 | unknown |
| `00278f84` | FundamentalRoutine() | 2880 | unknown |
| `001267f4` | disp_helpmenu2() | 2840 | unknown |
| `000940f0` | _vp_psy_init | 2828 | unknown |
| `0011cbb4` | iOS_RESUME_SET_EVENT_W(IOS_RESUME_DATA_EVENT_W*, IOS_RESUME_DATACOPY_MODE) | 2812 | unknown |
| `001e03c8` | getskillrange(ACT*) | 2812 | unknown |
| `0008aa00` | floor1_fit | 2800 | unknown |
| `00264cf8` | ctlnobel_main(CTLINFO*) | 2784 | unknown |
| `001b5104` | LearnAbiStts() | 2716 | unknown |
| `001e4f3c` | getskilleffect(ACT*) | 2712 | unknown |
| `001adf8c` | Equip() | 2684 | unknown |
| `0009f3f8` | ov_pcm_seek_page | 2576 | unknown |
| `001b937c` | Tutrial() | 2568 | unknown |
| `001225e8` | Edisp_bothwindow() | 2552 | unknown |
| `00287a78` | hight_font_draw(int) | 2548 | unknown |
| `000956d4` | _vp_couple_quantize_normalize | 2544 | unknown |
| `00133be4` | Wdisp_bothwindow() | 2544 | unknown |
| `0025a908` | ctlhoukmes_main(CTLINFO*) | 2504 | unknown |
| `0019b620` | DressEquip() | 2492 | unknown |
| `0024265c` | ctlendroll_main(CTLINFO*) | 2488 | unknown |
| `00211f14` | requestChangeClut(int, int, unsigned int, unsigned int, int, short, short, short) | 2440 | unknown |
| `000c8238` | attack_assumechr() | 2416 | unknown |
| `002c6550` | Settings_FrameRender() | 2412 | unknown |
| `000c8ba8` | attack_assumeface() | 2396 | unknown |
| `002235f4` | p20_gunFunc() | 2352 | unknown |
| `0016828c` | ASHURA_LMDL_Read(unsigned short*, L_MATRIX*, int) | 2332 | unknown |
| `0011c2bc` | Wdisp_status3() | 2296 | unknown |
| `000e5998` | disp_status3() | 2292 | unknown |
| `002c8194` | SettingsWnd_FrameRender() | 2292 | unknown |
| `000d5d6c` | make_abilitylistmain(int) | 2288 | unknown |
| `000fd318` | Wmake_abilitylistmain(int) | 2288 | unknown |
| `001d59fc` | time_flies(int) | 2288 | unknown |
| `00124078` | Wselect_value() | 2284 | unknown |
| `0024d068` | ctlbrst_main(CTLINFO*) | 2272 | unknown |
| `00124964` | Wselect_valuewithmessage() | 2260 | unknown |
| `000a98c8` | CEGL2_IF::DrawTile4(float, float, float, float, unsigned int*, float) | 2248 | unknown |
| `000e062c` | drawmessagepolygons() | 2240 | unknown |
| `001ebffc` | getShadowRect(tag_animation*) | 2240 | unknown |
| `002c78d4` | SettingsWnd_FrameMove() | 2240 | unknown |
| `0021d620` | s28_doSchedule(_EffectTCB*) | 2236 | unknown |
| `0014e0ec` | wipe_const() | 2228 | unknown |
| `0015b688` | sBattleTouchRotation() | 2224 | unknown |
| `001d82a8` | get_ability(int, int) | 2224 | unknown |
| `00135218` | Witemmenu_call(unsigned long*, unsigned long, int) | 2188 | unknown |
| `000d361c` | disp_chapter() | 2184 | unknown |
| `001b5ba0` | WorldJobStts() | 2180 | unknown |
| `002826c8` | GLIVON_FT4_old(unsigned long*, tagPOLY_GT4*, short, int, unsigned short*) | 2176 | unknown |
| `0012cdcc` | itemmenu_call(unsigned long*, unsigned long, int) | 2168 | unknown |
| `0012171c` | Edisp_equipwindow() | 2156 | unknown |
| `001e2308` | check_coord2(int, int, int, unsigned char) | 2152 | unknown |
| `00132cfc` | Wdisp_equipwindow() | 2148 | unknown |
| `0023837c` | Mdl0012(short, int, int, int) | 2096 | unknown |
| `000a42d8` | CG2D_LOADER_BMP::Copy(void*) | 2084 | unknown |
| `002ac014` | sceGuTexImage | 2084 | unknown |
| `000a4ef8` | CG2D_LOADER_TGA::Copy(void*) | 2076 | unknown |
| `00085fe0` | vorbis_synthesis_blockin | 2068 | unknown |
| `0015f3b0` | iOSJobChangeRot(short*, short*) | 2044 | unknown |
| `00272aac` | ForAutoCommand() | 2044 | unknown |
| `00277720` | EvaluationFunction() | 2044 | unknown |
| `0010e918` | Wevent_call(unsigned long*, unsigned long) | 2040 | unknown |
| `0026e428` | ctltuto_main(CTLINFO*) | 1992 | unknown |
| `0010e154` | Wdrawmessagepolygons() | 1988 | unknown |
| `0016671c` | ASHURA_Control(unsigned long, unsigned long, long, long) | 1988 | unknown |
| `000f5898` | menu_call(unsigned long*, unsigned long) | 1984 | unknown |
| `002632ec` | ctlmouketeam_main(CTLINFO*) | 1984 | unknown |
| `001e5bac` | getskillresult_main(int, SKILL_RESULT*) | 1980 | unknown |
| `002b07ac` | CDebugPrint::FrameStep(int, int, int, int, unsigned int) | 1980 | unknown |
| `002c562c` | Settings_Init() | 1968 | unknown |
| `0007f4a8` | _tr_flush_block | 1960 | unknown |
| `0010f124` | Wmenu_call(unsigned long*, unsigned long) | 1960 | unknown |
| `000a872c` | CEGL2_IF::Add3D(int, _EGL_PACKET_SPR*, unsigned char) | 1944 | unknown |
| `002284ac` | createPermanentObject(_JochuParameter*, Physics*) | 1944 | unknown |
| `00091898` | mdct_forward | 1932 | unknown |
| `002657f8` | ctlbackpage_main(CTLINFO*) | 1932 | unknown |
| `00278480` | GetDestinationsAndMakeMaskTG() | 1932 | unknown |
| `002c5ddc` | Settings_FrameMove() | 1908 | unknown |
| `00091128` | mdct_backward | 1904 | unknown |
| `000a75ac` | math::MATRIX4::operator*=(math::MATRIX4 const&) | 1904 | unknown |
| `000c478c` | load_loaddata() | 1896 | unknown |
| `0019aec0` | DressMain() | 1888 | unknown |
| `001c37dc` | MakeWindowFunc(unsigned char*) | 1884 | unknown |
| `00281a94` | iOS_v2menuExecute(V2_TOUCH*) | 1880 | unknown |
| `0028a76c` | ConvTutoData(FFT_SAVE_DATA*) | 1880 | unknown |
| `0029bbec` | GsSortFlipSprite | 1876 | unknown |
| `002c718c` | SettingsWnd_Init() | 1864 | unknown |
| `0008b594` | floor1_encode | 1860 | unknown |
| `000aa190` | CEGL2_IF::DrawPacket(int, int) | 1860 | unknown |
| `00231570` | Mdl0005(short, int, int, int) | 1852 | unknown |
| `001f5420` | displayDirection() | 1840 | unknown |
| `001b7270` | RoundHelpMessage(short) | 1836 | unknown |
| `00276e4c` | CheckUnitActionEffective(int, int) | 1828 | unknown |
| `00174aa0` | cMakeWindowFunc(unsigned char*) | 1800 | unknown |
| `001f25d4` | displayShape(tag_animation*) | 1796 | unknown |
| `00187920` | eDB_init(DB*, unsigned long*, tagPOLY_F3*, tagPOLY_FT3*, tagPOLY_F4*, tagPOLY_FT4*, tagPOLY_G3*, tagPOLY_GT3*, tagPOLY_G4*, tagPOLY_GT4*, tagLINE_F2*, tagLINE_F3*, tagLINE_F4*, tagLINE_G2*, tagLINE_G3*, tagLINEG4*, tagTILE*, tagTILE_1*, tagTILE_8*, tagTILE_16*, tagSPRT*, tagSPRT_8*, tagSPRT_16*, DR_MOVE*, DR_AREA*, DR_MODE*) | 1784 | unknown |
| `000a2c4c` | CG2D_LOADER_BMP::Save(void*, int, int, _G2D_SAVE*) | 1780 | unknown |
| `00282f48` | GLIVON_FT3_old(unsigned long*, tagPOLY_GT3*, short, int, unsigned short*) | 1776 | unknown |
| `001b7f68` | GetPad() | 1768 | unknown |
| `001eda18` | executeAnimationStatus(tag_animation*) | 1768 | unknown |
| `001aaa24` | GetTryBestEquip(short, short, short*) | 1760 | unknown |
| `000f07c0` | disp_selectwindow() | 1752 | unknown |
| `00231cac` | Mdl0006(short, int, int, int) | 1744 | unknown |
| `00257e5c` | ctleeff_draw(GsOT*) | 1740 | unknown |
| `0011661c` | Wdisp_selectwindow() | 1736 | unknown |
| `0017a42c` | bRoundHelpMessage(short, unsigned char) | 1732 | unknown |
| `0019a3f8` | BuyUnit() | 1716 | unknown |
| `00233ed0` | Mdl0008(short, int, int, int) | 1712 | unknown |
| `000d071c` | Ddisp_parawindow() | 1708 | unknown |
| `000d140c` | chokobo_chrmenu(int) | 1700 | unknown |
| `0018e3f0` | BattleEquip(int, long*) | 1700 | unknown |
| `001aa014` | GetBestEquip(short, short*) | 1692 | unknown |
| `00262b18` | hakenunit_status_main(CTLINFO*) | 1692 | unknown |
| `000ae584` | CEGL2_SPRITE::DrawScrollBG(float, float, _RECT_F32*, _RECT_F32*) | 1676 | unknown |
| `00137b10` | select_valuewithmessage() | 1676 | unknown |
| `0017aaf0` | bGetPad() | 1672 | unknown |
| `000c3d94` | Adisp_parawindow() | 1668 | unknown |
| `00133560` | Wdisp_abilitywindow() | 1668 | unknown |
| `0014a834` | Cdisp_parawindow() | 1668 | unknown |
| `00180b64` | bMakeWindowFunc(unsigned char*) | 1652 | unknown |
| `00190b98` | eMakeWindowFunc(unsigned char*) | 1652 | unknown |
| `0008cbf4` | vorbis_analysis_headerout | 1648 | unknown |
| `00163348` | ASHURA_SetMatrix(long, MATRIX*, MATRIX*, unsigned short) | 1636 | unknown |
| `00195270` | AbiStts() | 1636 | unknown |
| `00121f88` | Edisp_abilitywindow() | 1632 | unknown |
| `0012c190` | disp_parawindow() | 1632 | unknown |
| `001f2f84` | DisplayAnimations() | 1624 | unknown |
| `0008c4fc` | vorbis_synthesis_headerin | 1612 | unknown |
| `00097f44` | _book_unquantize | 1608 | unknown |
| `00193104` | jDB_init(DB*, unsigned long*, tagPOLY_F3*, tagPOLY_FT3*, tagPOLY_F4*, tagPOLY_FT4*, tagPOLY_G3*, tagPOLY_GT3*, tagPOLY_G4*, tagPOLY_GT4*, tagLINE_F2*, tagLINE_F3*, tagLINE_F4*, tagLINE_G2*, tagLINE_G3*, tagLINEG4*, tagTILE*, tagTILE_1*, tagTILE_8*, tagTILE_16*, tagSPRT*, tagSPRT_8*, tagSPRT_16*, DR_MOVE*, DR_AREA*) | 1608 | unknown |
| `00122fe0` | Edisp_parawindow() | 1604 | unknown |
| `001a33a0` | PoachBuy() | 1596 | unknown |
| `00261dac` | ctlmouketeam_init() | 1592 | unknown |
| `001345d4` | Wdisp_parawindow() | 1588 | unknown |
| `00173df8` | cGetPad() | 1588 | unknown |
| `0019e188` | NameChgSelect() | 1580 | unknown |
| `00169aa4` | ASHURA_LMDL_DB_COPY(unsigned short*) | 1572 | unknown |
| `0018f374` | eGetPad() | 1568 | unknown |
| `00084790` | vorbis_bitrate_addblock | 1564 | unknown |
| `001965a4` | jGetPad() | 1560 | unknown |
| `00108568` | Wevent_status_set(unsigned short, unsigned short) | 1540 | unknown |
| `00280dfc` | iOS_setStatusHPMPCT(IOS_STTSNUM*, int, int, int, int, int, int, int, int, int, void*, int) | 1540 | unknown |
| `001e6d74` | getreaction_post(unsigned short*) | 1524 | unknown |
| `0024b988` | ctlbar_main(CTLINFO*) | 1524 | unknown |
| `002570f4` | ctltownmenu_main(CTLINFO*) | 1516 | unknown |
| `00137524` | select_value() | 1512 | unknown |
| `0007a760` | inflate_fast | 1504 | unknown |
| `00197a10` | jMakeWindowFunc(unsigned char*) | 1504 | unknown |
| `00165520` | ASURA_FALL_INIT(unsigned char) | 1500 | unknown |
| `001a6d00` | Dismiss() | 1496 | unknown |
| `00094e54` | _vp_tonemask | 1480 | unknown |
| `0019cd3c` | DressSellEquip() | 1480 | unknown |
| `00218060` | ExecuteEffectAnimation(effectAnimation*, char, char, char) | 1480 | unknown |
| `00199a1c` | Buy() | 1468 | unknown |
| `0027a3bc` | SetUnitParameter(int) | 1464 | unknown |
| `001dbcec` | set_unitdata(int) | 1456 | unknown |
| `0021f5e4` | p02_hitMarkFunc() | 1456 | unknown |
| `000de724` | move_camera() | 1448 | unknown |
| `001f0550` | setShapeDataSub(tag_animation*, subAnimation*, unsigned short, unsigned short) | 1448 | unknown |
| `0007d158` | inflate_table | 1436 | unknown |
| `00258528` | ctleeff_main(CTLINFO*) | 1436 | unknown |
| `00202950` | generateAttackTeam() | 1424 | unknown |
| `001077f4` | Wmove_camera() | 1420 | unknown |
| `001ec8bc` | getPositionHight(SVECTOR*, unsigned char) | 1416 | unknown |
| `00087700` | vorbis_book_decodev_add | 1412 | unknown |
| `0027c7a8` | iOS_CMenuTouch::execPress(int*, int*, int*, IOS_MENU_TOUCH_RESULT*) | 1408 | unknown |
| `001e1a80` | search_reverse_mp(int, int, int, int, int, int*, int) | 1404 | unknown |
| `00191498` | eValueFunc(unsigned char*) | 1400 | unknown |
| `00264458` | ctlnobelstop_main(CTLINFO*) | 1400 | unknown |
| `00250984` | ctlworking_init() | 1396 | unknown |
| `00181e10` | bValueFuncShort(short*) | 1392 | unknown |
| `001ee70c` | drawDamage(tag_animation*, Point*) | 1388 | unknown |
| `001c5208` | ValueFuncShort(short*) | 1384 | unknown |
| `0024ecd0` | ctlpersmes_main(CTLINFO*) | 1384 | unknown |
| `00243c9c` | drawListStaffroll(int) | 1380 | unknown |
| `001c4958` | ValueFunc(unsigned char*) | 1368 | unknown |
| `002152f4` | loadClutDataCalcPlus(int, unsigned short*, unsigned int, unsigned int, int, short, short, short, int) | 1368 | unknown |
| `00183c20` | MakeSaveData(int) | 1364 | unknown |
| `0019bfdc` | DressRemove() | 1360 | unknown |
| `00181578` | bValueFunc(unsigned char*) | 1356 | unknown |
| `00256930` | ctltownmenu_init(int) | 1344 | unknown |
| `0026cdd8` | ctltremes_main(CTLINFO*) | 1344 | unknown |
| `00195910` | BattleJobStts(int, int) | 1340 | unknown |
| `001a6764` | DB_init(DB*, unsigned long*, tagPOLY_F3*, tagPOLY_FT3*, tagPOLY_F4*, tagPOLY_FT4*, tagPOLY_G3*, tagPOLY_GT3*, tagPOLY_G4*, tagPOLY_GT4*, tagLINE_F2*, tagLINE_F3*, tagLINE_F4*, tagLINE_G2*, tagLINE_G3*, tagLINEG4*, tagTILE*, tagTILE_1*, tagTILE_8*, tagTILE_16*, tagSPRT*, tagSPRT_8*, tagSPRT_16*, DR_MOVE*, DR_AREA*, DR_MODE*) | 1328 | unknown |
| `0027c27c` | iOS_CMenuTouch::execTap(IOS_MENU_TOUCH_RESULT*, int*, int*, int*) | 1324 | unknown |
| `002247a0` | CheckBowResult(int, SVECTOR*, int) | 1316 | unknown |
| `00081c9c` | unzOpenCurrentFile3 | 1300 | unknown |
| `000cb4d0` | assumehelpmessage() | 1296 | unknown |
| `001579d4` | addzodiacback() | 1296 | unknown |
| `00213228` | requestChangeAnbient(int, int, int, int, int) | 1292 | unknown |
| `00213898` | requestChangeFlat(int, int, int, int, int) | 1292 | unknown |
| `0011e160` | Wextend_windowframemain(int, int, RECT16*, int, int, int) | 1288 | unknown |
| `0024c89c` | ctlbrst_init() | 1284 | unknown |
| `0011d864` | extend_windowframemain(int, int, RECT16*, int, int, int) | 1280 | unknown |
| `00156054` | disp_floatwindow() | 1276 | unknown |
| `00184174` | SetLoadData(int) | 1276 | unknown |
| `001a96c8` | ItemSort(int, short*) | 1272 | unknown |
| `0027426c` | MainBattleRoutine() | 1272 | unknown |
| `0016e2d8` | ASURA_WorkInit() | 1264 | unknown |
| `001f4b2c` | entryAnimations() | 1260 | unknown |
| `0025cd24` | wldpara_init() | 1256 | unknown |
| `0029b704` | GsSortPoly | 1256 | unknown |
| `0021abec` | SetCameraWorkWithMetaschedule(short) | 1252 | unknown |
| `00220ab0` | p22_shoukanFunc() | 1252 | unknown |
| `0022416c` | p01_bowFunc() | 1252 | unknown |
| `0025a424` | ctlhoukmes2_init(int) | 1252 | unknown |
| `001d2394` | get_succession_data(BWORK*) | 1248 | unknown |
| `000ad324` | CEGL2_SPRITE::AddPacketPartial(float, float, float, float, float, float, CEGL_PACKET*) | 1244 | unknown |
| `0016a1c8` | ASHURA_FALL(unsigned char) | 1244 | unknown |
| `002524d0` | ctlworkingst_main(CTLINFO*) | 1244 | unknown |
| `001a39dc` | PoachBuyValue() | 1240 | unknown |
| `001b4c34` | LearnJobStts() | 1232 | unknown |
| `0008d318` | vorbis_lpc_from_data | 1224 | unknown |
| `001e3f20` | search_root(int, int, int, int) | 1224 | unknown |
| `00212c00` | requestChangeGradation(int, int, int, int, int) | 1220 | unknown |
| `00273378` | SetTmp_UA(UnitAction*) | 1220 | unknown |
| `000986d0` | vorbis_book_init_decode | 1212 | unknown |
| `002010cc` | iOSBATTLE_scrollLandscape() | 1212 | unknown |
| `0025b2d0` | ctlhoukmes2_main(CTLINFO*) | 1212 | unknown |
| `0021871c` | testBowLineDisp(int) | 1208 | unknown |
| `000e1db8` | statusfigprint(int, int, char*, COPYFIELD*) | 1204 | unknown |
| `0027cf50` | iOS_CMenuTouch::exec(int*, int*, int*) | 1204 | unknown |
| `00188fe4` | eItemSort(int, short*) | 1200 | unknown |
| `0024e0f8` | ctlkiromes_main(CTLINFO*) | 1200 | unknown |
| `0009ebfc` | ov_raw_seek | 1192 | unknown |
| `001bb714` | DetailStatus() | 1188 | unknown |
| `001f45c0` | InitAnimation() | 1188 | unknown |
| `00250ef8` | ctlwork_main(CTLINFO*) | 1184 | unknown |
| `000a574c` | CG2D_LOADER_TGA::TGA_AnalyzeHeader(void*) | 1176 | unknown |
| `001e3500` | search_force_mp(int, SVECTOR*) | 1160 | unknown |
| `00283a50` | GLIVON_F4_old(unsigned long*, tagPOLY_F4*, short, VECTOR_DATABASE*) | 1160 | unknown |
| `001108a4` | Wstatusfigprint(int, int, char*, COPYFIELD*) | 1156 | unknown |
| `001acf38` | DrawTexFlip(short*, COLOR*, char, int, int, int) | 1156 | unknown |
| `001d35a0` | set_monsterwork(unsigned char*, unsigned char*) | 1156 | unknown |
| `00241a60` | pmkprim_put(int) | 1152 | unknown |
| `002b4200` | Link_FrameMove() | 1152 | unknown |
| `000a0df0` | ov_read_filter | 1140 | unknown |
| `00244974` | create_rollline(unsigned char*) | 1140 | unknown |
| `00194e04` | JobStatus() | 1132 | unknown |
| `000cc270` | Caddzodiacback() | 1128 | unknown |
| `001e64c4` | setskilldata_common(ACT*, ACT*, int) | 1128 | unknown |
| `00160008` | iOSCurHojyo(SVECTOR*) | 1120 | unknown |
| `000ee61c` | disp_waitwindow() | 1112 | unknown |
| `002691cc` | wldwalk_rute() | 1108 | unknown |
| `00261184` | ctlhakenokng_init() | 1096 | unknown |
| `000ae090` | CEGL2_SPRITE::DrawPartial(float, float, float, float, float, float) | 1088 | unknown |
| `000aceec` | CEGL2_SPRITE::Draw8(float, float, unsigned int, void*) | 1080 | unknown |
| `000b1448` | CEGL_COLLISION::IsVertexInTriangle3D(math::VECTOR3<float>, math::VECTOR3<float>, math::VECTOR3<float>, math::VECTOR3<float>) | 1080 | unknown |
| `001a2f68` | PoachSellValue() | 1080 | unknown |
| `00285084` | pspBattleEntryAreaMake(int, int) | 1080 | unknown |
| `001b2560` | JobCicle(int, int, int, int) | 1076 | unknown |
| `001a4338` | SellValue() | 1072 | unknown |
| `0019c918` | DressAuto() | 1060 | unknown |
| `001a2b44` | PoachSell() | 1060 | unknown |
| `002435f0` | vEnd_rollinit() | 1060 | unknown |
| `00199fd8` | BuyValue() | 1056 | unknown |
| `001a3f1c` | Sell() | 1052 | unknown |
| `001bbe90` | ShopStatus() | 1052 | unknown |
| `00177ed0` | bDrawTexFlip(short*, COLOR*, char, int, int, int) | 1048 | unknown |
| `00283638` | GLIVON_F3_old(unsigned long*, tagPOLY_F3*, short, VECTOR_DATABASE*) | 1048 | unknown |
| `001196ac` | Wdisp_waitwindow() | 1040 | unknown |
| `002191f8` | SetEffectTransCameraWork(int, int, int, VECTOR*) | 1040 | unknown |
| `00266f30` | wldinfo_put(GsOT*) | 1040 | unknown |
| `000a5e98` | CG2D_LOADER_TIM::Save(void*, int, int, _G2D_SAVE*) | 1036 | unknown |
| `000feaa8` | Wallocatewindow() | 1036 | unknown |
| `0026d318` | ctlnvcontinue_main(CTLINFO*) | 1036 | unknown |
| `00218df4` | SetEffectAngleCameraWork(int, int, int, SVECTOR*) | 1028 | unknown |
| `000d6f84` | allocatewindow() | 1024 | unknown |
| `0025e8d4` | iOSwldscr_snapshot(int) | 1024 | unknown |
| `00147e9c` | active_disp_waitwindow() | 1020 | unknown |
| `0021101c` | initBattleMap(int, int, int) | 1016 | unknown |
| `00256500` | ctlsthelp_main(CTLINFO*) | 1016 | unknown |
| `00289420` | pspPrimDirectPartsDraw(int, int, unsigned long*, unsigned char*) | 1016 | unknown |
| `0019c52c` | Account() | 1004 | unknown |
| `0024fdf4` | pspCtltutonet_main(CTLINFO*) | 1004 | unknown |
| `0025fbc4` | world_map() | 1004 | unknown |
| `00263b08` | ctlnobel_init(int) | 1004 | unknown |
| `001a749c` | Bwork2ChrStts(BWORK*, CHR_STTS*, UM_WORK*) | 1000 | unknown |
| `000b8414` | CFILE_UTIL::FileReplaceStr(char*, char*, char*, int*) | 988 | unknown |
| `00245f24` | ctlopentitle_init(int) | 988 | unknown |
| `002885f0` | pspOpenIconDraw(unsigned long*, int, int, PSP_OPEN_ICON_TYPE, int) | 988 | unknown |
| `000d8270` | count_words2(short*, short*, char*) | 984 | unknown |
| `0021e388` | s29_doMetaschedule(_EffectTCB*) | 984 | unknown |
| `0023dc94` | Mdl0022(short, int, int, int) | 984 | unknown |
| `000ffe58` | Wcount_words2(short*, short*, char*) | 980 | unknown |
| `0019d83c` | MainEmploy() | 980 | unknown |
| `002520c8` | ctlworkinginf_main(CTLINFO*) | 980 | unknown |
| `000abcd0` | std::priv::_Rb_global<bool>::_Rebalance_for_erase(std::priv::_Rb_tree_node_base*, std::priv::_Rb_tree_node_base*&, std::priv::_Rb_tree_node_base*&, std::priv::_Rb_tree_node_base*&) | 976 | unknown |
| `001604fc` | iOSSlideYajiMain() | 976 | unknown |
| `001bff08` | PostModeChg(int) | 972 | unknown |
| `000b74d8` | CFILE_TXT::Load(char*, int, unsigned int) | 964 | unknown |
| `0026ca14` | ctlnvcontinue_init(int) | 964 | unknown |
| `0009fe08` | ov_pcm_seek | 960 | unknown |
| `00247eb4` | ctlbirthday_main(CTLINFO*) | 960 | unknown |
| `00084060` | ogg_stream_pagein | 952 | unknown |
| `0021e7d8` | doEffect_sub() | 948 | unknown |
| `00261728` | ctlhakenokng_main(CTLINFO*) | 948 | unknown |
| `001a7a84` | ChrSort(int) | 944 | unknown |
| `001c2ce0` | MakeSmallWindowFunc(unsigned char*) | 944 | unknown |
| `001cd600` | set_status_all(int, int) | 944 | unknown |
| `00073c74` | crc32 | 936 | unknown |
| `000e2698` | iOS_statusfigprint_FT4(tagPOLY_FT4*, int, unsigned short, int, int, void*, int, int, COPYFIELD*, int) | 936 | unknown |
| `0021a648` | SearchNextMetascheduleDividePos(short, short, long*, long*) | 932 | unknown |
| `00288a78` | pspPrimAddDirect(unsigned long*, int, int, int, int) | 928 | unknown |
| `001bfb6c` | PreModeChg(int) | 924 | unknown |
| `002517cc` | ctlworking_main(CTLINFO*) | 924 | unknown |
| `00085b94` | vorbis_analysis_blockout | 920 | unknown |
| `00134c08` | Wdisp_selectrefleshwindow() | 920 | unknown |
| `001a1450` | Name(unsigned char*, short*) | 920 | unknown |
| `0027b788` | iOS_CMenuTouch::initPacket() | 920 | unknown |
| `00086e9c` | vorbis_staticbook_unpack | 916 | unknown |
| `001ca5a4` | change_status_adjust(int) | 916 | unknown |
| `0027dffc` | iOS_CMenuTouchSaveLoad::initPacket() | 916 | unknown |
| `0027e900` | iOS_CMenuTouchSaveLoad::execPress(int*, int*, IOS_MENU_TOUCH_SAVELOAD_RESULT*) | 916 | unknown |
| `000e2308` | disp_statuscpara() | 912 | unknown |
| `00250440` | ctlwork_init() | 912 | unknown |
| `00260ce8` | mouke_okng(CTLINFO*) | 912 | unknown |
| `00110dc4` | Wdisp_statuscpara() | 908 | unknown |
| `00241ee0` | vOpn_arzmes_main() | 904 | unknown |
| `001e2b78` | CheckPoleResult(int, int, int, int, int) | 900 | unknown |
| `001ee278` | initializeDamageNumber(tag_animation*) | 900 | unknown |
| `0024b09c` | barmenu_reset(CTLINFO*) | 900 | unknown |
| `0020023c` | iOSexecuteMoveProcs(tag_animation*) | 896 | unknown |
| `00174724` | cMakeSmallWindowFunc(unsigned char*) | 892 | unknown |
| `002cdb20` | __gnu_unwind_execute | 892 | unknown |
| `001aa6b0` | GetShopItemList(short, short, short, short*, int) | 884 | unknown |
| `000d0dec` | Ddisp_selectrefleshwindow() | 880 | unknown |
| `00123624` | Edisp_selectrefleshwindow() | 880 | unknown |
| `0014ba1c` | Cdisp_selectrefleshwindow() | 880 | unknown |
| `001eef44` | loadCharacterClut(tag_animation*, int, int) | 876 | unknown |
| `002445cc` | roll_xaplay() | 876 | unknown |
| `0027bd18` | iOS_CMenuTouch::setMenuAssistPosition(int) | 876 | unknown |
| `0024a0ac` | vOpn_anim(ANMPAC*, unsigned long*) | 872 | unknown |
| `000aae00` | CEGL2_FBO::RenderToFBO(float, float, float, float, float, float, unsigned char, unsigned char, int, int) | 868 | unknown |
| `00222e4c` | p18_reflecFunc() | 868 | unknown |
| `002532b8` | ctlzodiac_init(int, int, int) | 868 | unknown |
| `000d7f10` | count_words(short*, short*, char*) | 864 | unknown |
| `00111150` | WiOS_statusfigprint_FT4(tagPOLY_FT4*, int, unsigned short, int, int, void*, int, int, COPYFIELD*, int) | 864 | unknown |
| `0028a340` | pspStartSaveCheck() | 864 | unknown |
| `00086b40` | vorbis_staticbook_pack | 860 | unknown |
| `000ffafc` | Wcount_words(short*, short*, char*) | 860 | unknown |
| `00210384` | placeNameStart() | 860 | unknown |
| `000736ac` | adler32 | 856 | unknown |
| `002cd594` | _Unwind_VRS_Pop | 856 | unknown |
| `002660b8` | wld_anim(ANMPAC*, GsOT*) | 852 | unknown |
| `0025361c` | ctlzodiac_main(CTLINFO*) | 848 | unknown |
| `000a4b38` | CG2D_LOADER_TGA::Save(void*, int, int, _G2D_SAVE*) | 844 | unknown |
| `0012c7f0` | disp_selectrefleshwindow() | 844 | unknown |
| `00229dc8` | DrawPermanentShape(PermanentObject*) | 844 | unknown |
| `0024c554` | ctlbrst_menu_set() | 840 | unknown |
| `00270f3c` | iOSpagewin_main(PAGEWININFO*) | 840 | unknown |
| `0026f4ec` | ctlunregmes_main(CTLINFO*) | 836 | unknown |
| `00272254` | ForAbnormalStatus() | 836 | unknown |
| `001a2710` | MainPoach() | 832 | unknown |
| `001d4600` | set_event_table(TURN_TABLE*, int) | 832 | unknown |
| `000a36e8` | CG2D_LOADER_BMP::BMP_AnalyzeCore() | 828 | unknown |
| `00215db8` | mainLoop() | 828 | unknown |
| `000db06c` | move_light() | 824 | unknown |
| `0018a3ac` | eDrawTexFlip(short*, COLOR*, char, int, int, int) | 824 | unknown |
| `00172f8c` | cDrawTexFlip(short*, COLOR*, char, int, int, int) | 816 | unknown |
| `0024d964` | ctlkiroku_init() | 808 | unknown |
| `0008174c` | unzReadCurrentFile | 804 | unknown |
| `00153940` | Zaddzod(ZODRECORD*, tagPOLY_FT4*) | 804 | unknown |
| `00216b14` | Resume_Init_WORK_MU() | 804 | unknown |
| `00248274` | ctlbirthokng_main(CTLINFO*) | 804 | unknown |
| `00248720` | ctlmusic_main(CTLINFO*) | 800 | unknown |
| `00194238` | jDrawTexFlip(RECT16*, short*, COLOR*, char, int, int, int) | 796 | unknown |
| `00106448` | Wmake_abilitycommandmain() | 792 | unknown |
| `00262708` | hakenunit_change(CTLINFO*) | 792 | unknown |
| `001d2ff4` | set_playerwork_common_child(PENTRY*, int) | 788 | unknown |
| `000ac540` | std::priv::_Rb_tree<int, std::less<int>, std::pair<int const, CEGL2_SHADER::DATA_SHADER>, std::priv::_Select1st<std::pair<int const, CEGL2_SHADER::DATA_SHADER> >, std::priv::_MapTraitsT<std::pair<int const, CEGL2_SHADER::DATA_SHADER> >, std::allocator<std::pair<int const, CEGL2_SHADER::DATA_SHADER> > >::insert_unique(std::priv::_Rb_tree_iterator<std::pair<int const, CEGL2_SHADER::DATA_SHADER>, std::priv::_MapTraitsT<std::pair<int const, CEGL2_SHADER::DATA_SHADER> > >, std::pair<int const, CEGL2_SHADER::DATA_SHADER> const&) | 784 | unknown |
| `0025bc78` | mksuccess_calc() | 784 | unknown |
| `0008e038` | vorbis_lsp_to_curve | 776 | unknown |
| `000bc67c` | CSOUND_IF_SL::LoadOGG(int, char*, unsigned char*, unsigned int, unsigned int, int) | 776 | unknown |
| `0015f048` | iOS_DrawTexFlip(short*, COLOR*, char, int, int, unsigned char*, unsigned short*) | 776 | unknown |
| `001f5018` | doCursor(VECTOR*, SVECTOR*, SVECTOR*) | 776 | unknown |
| `00248e6c` | vOpn_scrinit(int) | 776 | unknown |
| `002514c4` | ctlworkinginf_init(int) | 776 | unknown |
| `002649f0` | ctlbackpage_init() | 776 | unknown |
| `001abf20` | EggChk(int) | 772 | unknown |
| `00260574` | ctlmouke_main(CTLINFO*) | 772 | unknown |
| `002862fc` | FFTPSP_ASURA_polygon_combine(unsigned int, ADB*, SVECTOR*, SVECTOR*, SVECTOR*, SVECTOR*) | 772 | unknown |
| `0028b0c0` | pspWorldBlackSpotDraw(GsOT*, int) | 772 | unknown |
| `0009c9a0` | drft_init | 764 | unknown |
| `001fe718` | changeAnimationStatus(int, int, int) | 764 | unknown |
| `0025f694` | wldnormal_lop() | 764 | unknown |
| `0026a874` | snpl_init(int) | 764 | unknown |
| `0008e340` | vorbis_lpc_to_lsp | 756 | unknown |
| `00102b20` | Wmove_light() | 756 | unknown |
| `001a8620` | GetAbilityList(short, short, int, short*, int) | 756 | unknown |
| `000b55e4` | CRECT::MoveCursorFocus(int, int, int, int) | 752 | unknown |
| `000c449c` | loadname() | 752 | unknown |
| `00167d08` | ASHURA_GNS_Read(unsigned short) | 752 | unknown |
| `00177088` | bGetAbilityList(short, short, int, short*, int) | 752 | unknown |
| `0026854c` | rutegrow_draw(GsOT*) | 752 | unknown |
| `000e1588` | statusfigprint16(int, int, char*, COPYFIELD*) | 748 | unknown |
| `0011006c` | Wstatusfigprint16(int, int, char*, COPYFIELD*) | 748 | unknown |
| `001d4940` | set_normability2(int, unsigned char, short*, unsigned char*, unsigned char*, int, unsigned char*, unsigned char*) | 748 | unknown |
| `001dc474` | adjust_equip_change_common(BWORK*, int, int) | 748 | unknown |
| `002acb48` | GuEmu_EngineInit() | 748 | unknown |
| `001609f8` | iOSYajiEffect(unsigned char*, unsigned short*) | 740 | unknown |
| `00267f3c` | wldrute_draw(GsOT*) | 740 | unknown |
| `000cbf7c` | card_call(unsigned long*, unsigned long, int) | 736 | unknown |
| `0021df6c` | doMetaschedulePtclCommandOnce(unsigned short, _EffectTCB*) | 736 | unknown |
| `002450c4` | fft_opening(int) | 736 | unknown |
| `00090e08` | mdct_init | 732 | unknown |
| `000ab164` | CEGL2_FBO::RenderFromFBO(unsigned int, float, float, float, float, float, float, unsigned char, unsigned char, int) | 732 | unknown |
| `001908bc` | eMakeSmallWindowFunc(unsigned char*) | 732 | unknown |
| `001bc5a0` | Bottun(short, short, short, short, short, short) | 732 | unknown |
| `001e6a98` | getreaction_pre(int, unsigned short*) | 732 | unknown |
| `000db4a4` | calcformula(int, int, int, int) | 728 | unknown |
| `00103068` | Wcalcformula(int, int, int, int) | 728 | unknown |
| `001bbbb8` | CurChrChg2() | 728 | unknown |
| `0026ec48` | ctlsentuto_main(CTLINFO*) | 728 | unknown |
| `00076ef8` | deflateInit2_ | 724 | unknown |
| `0008742c` | vorbis_book_decodevs_add | 724 | unknown |
| `0010fd08` | Wmultiwindow_packetinit(RECT16*, COMRECORD*, PRIMPACKET*) | 720 | unknown |
| `000a6314` | CG2D_LOADER_TIM::Copy(void*) | 716 | unknown |
| `00180898` | bMakeSmallWindowFunc(unsigned char*) | 716 | unknown |
| `00197744` | jMakeSmallWindowFunc(unsigned char*) | 716 | unknown |
| `00251b68` | ctlworkingst_dataset(int) | 716 | unknown |
| `002abd34` | sceGuClutLoad_for_iOS | 716 | unknown |
| `002b3f34` | Link_Init() | 716 | unknown |
| `001757d0` | bSwapDB(int, int) | 712 | unknown |
| `001bd464` | UnitFlagInit() | 712 | unknown |
| `0025fff8` | ctlmouke_init() | 712 | unknown |
| `000a67d8` | CG2D_LOADER_TIM::TIM_LoadFile(char*, unsigned int) | 708 | unknown |
| `000ec644` | multiwindow_keyright(COMRECORD*, int) | 708 | unknown |
| `0010558c` | Wmultiwindow_keyright(COMRECORD*, int) | 708 | unknown |
| `001981b0` | jValueFunc(unsigned char*) | 708 | unknown |
| `00267c74` | ctlretokng_main(CTLINFO*) | 708 | unknown |
| `00201ca4` | callEffect(int, tag_animation*) | 704 | unknown |
| `0021ba18` | DynamicsAllObject(_Object*) | 704 | unknown |
| `002207f0` | p17_crystalFunc() | 704 | unknown |
| `000db8c4` | cnvglobaltolocalid(int) | 700 | unknown |
| `00103c94` | Wcnvglobaltolocalid(int) | 700 | unknown |
| `001e2efc` | getweaponeffect(ACT*) | 700 | unknown |
| `0027f238` | iOS_RectHitExecute() | 700 | unknown |
| `000b1190` | CEGL_COLLISION::IsVertexInTriangle2D(math::VECTOR2<float>, math::VECTOR2<float>, math::VECTOR2<float>, math::VECTOR2<float>) | 696 | unknown |
| `001f024c` | requestDamageAnimation(tag_animation*, tag_animation*) | 696 | unknown |
| `00205694` | iOS_RESUME_SET_BATTLE(IOS_RESUME_DATA_BATTLE*, IOS_RESUME_DATACOPY_MODE) | 696 | unknown |
| `0011dd88` | extend_systemframe(int, int, RECT16*, int) | 692 | unknown |
| `00162e94` | ASHURA_LightSwitch(long) | 692 | unknown |
| `0029b134` | xpLib_DebugImport() | 692 | unknown |
| `00187264` | MakeHeader(int, int, CARD_HEADER*) | 688 | unknown |
| `0026883c` | rute_find(int, int) | 688 | unknown |
| `002ca8a0` | __aeabi_dsub | 688 | unknown |
| `000af120` | CEGL2_TEX_HYBRID::GL_IsUpdate(unsigned int, int*, _RECT_S32*) | 684 | unknown |
| `001f2cd8` | getDisplayPosition() | 684 | unknown |
| `00270c90` | pagewin_main(PAGEWININFO*) | 684 | unknown |
| `002ca8a4` | __aeabi_dadd | 684 | unknown |
| `001c245c` | UnitSort() | 680 | unknown |
| `00220548` | p15_deathFunc() | 680 | unknown |
| `00263fcc` | ctlnobelstop_init() | 680 | unknown |
| `000a1a5c` | CG2D_COLOR::HSBToRGB(unsigned short, unsigned short, unsigned short, unsigned int*) | 676 | unknown |
| `0021b5bc` | LoadEffect() | 676 | unknown |
| `0029ae90` | xpLib_DebugExport() | 676 | unknown |
| `0015e144` | iOSGetChrList() | 672 | unknown |
| `001d15d8` | iOS_RESUME_SET_BCALC(IOS_RESUME_DATA_BCALC*, IOS_RESUME_DATACOPY_MODE) | 672 | unknown |
| `0026df48` | ctlhentuto_main(CTLINFO*) | 672 | unknown |
| `002ab9e8` | sceGuScissor | 672 | unknown |
| `000dd9fc` | make_abilitycommandmain() | 668 | unknown |
| `00160fb4` | iOSYajiEffectSetLRTGA(int) | 668 | unknown |
| `001baec8` | MasaDataInit() | 668 | unknown |
| `002475e8` | ctlchrmake_main(CTLINFO*) | 668 | unknown |
| `0024a688` | vOpn_window(WINPAC*, unsigned long*) | 668 | unknown |
| `0024b420` | ctlbar_init() | 668 | unknown |
| `000b4a98` | CINPUT_IF_TOUCH::GetGesturePinch(float, float*, unsigned int*, int*, int*, float*, int*) | 664 | unknown |
| `0024fa34` | pspCtltutonet_init() | 664 | unknown |
| `00259bd8` | ctlhouk_init() | 664 | unknown |
| `001650f4` | ASHURA_init() | 660 | unknown |
| `001efe60` | requestStatusChangeAnimation(tag_animation*) | 660 | unknown |
| `00251e34` | ctlworkingst_init(int, int) | 660 | unknown |
| `00255ee0` | ctlflagset_main(CTLINFO*) | 660 | unknown |
| `000ff03c` | Wallocatetexture(RECT16*, tagPOLY_FT4*, long*) | 656 | unknown |
| `00211460` | padRead() | 656 | unknown |
| `00267840` | ctlretokng_init(int) | 656 | unknown |
| `0024de6c` | ctlkiroku_main(CTLINFO*) | 652 | unknown |
| `00255b88` | ctlopt_main(CTLINFO*) | 652 | unknown |
| `0025da88` | wldkey_rep(unsigned long) | 652 | unknown |
| `000d7498` | allocatetexture(RECT16*, tagPOLY_FT4*, long*) | 648 | unknown |
| `001c6ca4` | CursolDownFunc(DVECTOR*, unsigned short*, int) | 648 | unknown |
| `0025c124` | mkbonus_check() | 648 | unknown |
| `00289198` | pspPrimBackDrawRGB(int, int, unsigned short, unsigned short, unsigned long*, unsigned char*, unsigned char, unsigned char, unsigned char, int) | 648 | unknown |
| `0026d9a8` | ctltuto_init(int, int) | 644 | unknown |
| `00276930` | GetTargetBaseArea(int, int) | 644 | unknown |
| `000851d0` | vorbis_dsp_clear | 640 | unknown |
| `0009673c` | res1_class | 640 | unknown |
| `001da6f8` | set_playerwork_j(BWORK*, int, int) | 640 | unknown |
| `002106e0` | placeNameEnd() | 640 | unknown |
| `002b8378` | IS_GAME_AREA(int, int) | 640 | unknown |
| `00088978` | _ve_envelope_search | 636 | unknown |
| `0024f238` | ctltips_init(int) | 632 | unknown |
| `0028ca3c` | CAUTOSAVE::Load() | 632 | unknown |
| `00291c48` | xpLibgpuInit | 632 | unknown |
| `000d9b10` | request_command(int) | 628 | unknown |
| `001831e0` | bCursolDownFunc(DVECTOR*, unsigned short*, int) | 628 | unknown |
| `001d3308` | set_playerwork_common(PENTRY*, int) | 628 | unknown |
| `001e180c` | search_mp(int, int, int, int) | 628 | unknown |
| `0027d98c` | iOS_CMenuTouchNum::execPress(int*, IOS_MENU_TOUCH_NUM_RESULT*) | 628 | unknown |
| `000a17ec` | CG2D_COLOR::RGBToHSB(unsigned int, unsigned short*, unsigned short*, unsigned short*) | 624 | unknown |
| `001876b0` | eSwapDB(int, int) | 624 | unknown |
| `002a27c4` | xpLibpad::Update(int) | 624 | unknown |
| `002b2fe8` | musicPlayer_Play(int, int, int, int) | 624 | unknown |
| `000868a4` | vorbis_synthesis_lapout | 620 | unknown |
| `0026b378` | wldssd_control() | 620 | unknown |
| `002b5bec` | Logo_FrameRender() | 620 | unknown |
| `002cac50` | __aeabi_dmul | 620 | unknown |
| `00083900` | ogg_stream_iovecin | 616 | unknown |
| `00087ecc` | vorbis_book_decodevv_add | 616 | unknown |
| `0026c418` | ctltremes_init(int) | 616 | unknown |
| `00288f30` | pspPrimBackDraw(int, int, unsigned short, unsigned short, unsigned long*, unsigned char*) | 616 | unknown |
| `000ba9c8` | CSOUND_IF::Load(int, char*, unsigned char*, unsigned int, unsigned int, int, int, int, int, int, int) | 612 | unknown |
| `0011e68c` | Wextend_systemframe(int, int, RECT16*, int) | 612 | unknown |
| `0013cfe4` | iOS_limitOptrecSub() | 612 | unknown |
| `00142f60` | WiOS_limitOptrecSub() | 612 | unknown |
| `0028c32c` | CFFT_STATE::SetRenderSize(int, int) | 612 | unknown |
| `002b5988` | Logo_FrameMove() | 612 | unknown |
| `002bb910` | iOSTatchPanelCtrl(int, int) | 612 | unknown |
| `000a4078` | CG2D_LOADER_BMP::BMP_DecodeRLE4(unsigned char*, unsigned char*, int, int) | 608 | unknown |
| `000b81b4` | CFILE_UTIL::FileConvertLF(char*) | 608 | unknown |
| `000bced4` | CSOUND_LOADER_PCM::Open(char*, unsigned char*, unsigned int, unsigned int) | 608 | unknown |
| `000bddd8` | CSTEP::GetDataF() | 608 | unknown |
| `001a829c` | GetJobList(unsigned char, short*, int) | 604 | unknown |
| `001aea08` | AutoEquip() | 604 | unknown |
| `00252e5c` | ctlworkendmes_main(CTLINFO*) | 604 | unknown |
| `0025b9f4` | yokoyari_mesput(CTLINFO*, int, int) | 604 | unknown |
| `00260a8c` | ctlmoumes_main(CTLINFO*) | 604 | unknown |
| `002624ac` | mouketeam_unitface(CTLINFO*, int, int) | 604 | unknown |
| `0026f830` | ctluwa_init() | 604 | unknown |
| `002b1790` | AppEngine_FrameStep() | 604 | unknown |
| `00073370` | Android_Font_Render(char const*, int) | 600 | unknown |
| `00097c44` | _make_words | 600 | unknown |
| `00157ee4` | cnvattackclutno(int) | 600 | unknown |
| `00238124` | Mdl0011(short, int, int, int) | 600 | unknown |
| `00267368` | ctlret_init() | 600 | unknown |
| `000ac850` | CEGL2_SHADER::Load(int, void*, unsigned int, void*, unsigned int) | 596 | unknown |
| `000c4ef4` | attackteam_end() | 596 | unknown |
| `000acb00` | CEGL2_SPRITE::Save(char*, int, _G2D_SAVE*) | 592 | unknown |
| `001acafc` | DrawFT4RGB(RECT16*, int, int, COLOR*, int, unsigned short, unsigned short, int) | 592 | unknown |
| `00268c74` | walkrute_set(int, int) | 592 | unknown |
| `00289d5c` | pspFftSizeCheck(int*, int*, int*) | 592 | unknown |
| `0028c7ec` | CAUTOSAVE::Save(unsigned int) | 592 | unknown |
| `0009541c` | _vp_offset_and_mix | 588 | unknown |
| `00172660` | cDB_init(DB*, unsigned long*, tagPOLY_F3*, tagPOLY_FT3*, tagPOLY_F4*, tagPOLY_FT4*, tagPOLY_G3*, tagPOLY_GT3*, tagPOLY_G4*, tagPOLY_GT4*, tagLINE_F2*, tagLINE_F3*, tagLINE_F4*, tagLINE_G2*, tagLINE_G3*, tagLINEG4*, tagTILE*, tagTILE_1*, tagTILE_8*, tagTILE_16*, tagSPRT*, tagSPRT_8*, tagSPRT_16*, DR_MOVE*, DR_AREA*) | 588 | unknown |
| `001751a8` | cValueFunc(unsigned char*) | 588 | unknown |
| `001d9968` | resist_savedata(BWORK*, int) | 588 | unknown |
| `0026f0bc` | ctlunregmes_init(int) | 588 | unknown |
| `00294af8` | PutDispEnv | 588 | unknown |
| `002a0124` | MulMatrix0 | 588 | unknown |
| `00087c84` | vorbis_book_decodev_set | 584 | unknown |
| `000e12ac` | multiwindow_packetinit(RECT16*, COMRECORD*, PRIMPACKET*) | 584 | unknown |
| `0028bfb8` | CFFT_STATE::CFFT_STATE() | 584 | unknown |
| `00177664` | bDrawPluralFT4RGB(unsigned char*, COLOR*, int, unsigned short, unsigned short, int, int) | 580 | unknown |
| `00189d6c` | eDrawPluralFT4RGB(unsigned char*, COLOR*, int, unsigned short, unsigned short, int, int) | 580 | unknown |
| `00193e04` | jDrawPluralFT4RGB(unsigned char*, COLOR*, int, unsigned short, unsigned short, int, int) | 580 | unknown |
| `002ac838` | sceGuTexWrap | 580 | unknown |
| `000adcd4` | CEGL2_SPRITE::LoadEnd(int, int) | 576 | unknown |
| `0024adec` | calender_add(int) | 576 | unknown |
| `0026e1e8` | ctlsentuto_init() | 576 | unknown |
| `0027286c` | DattoNoGotokuNigeyoRoutine() | 576 | unknown |
| `001d1374` | set_monomane_act(BWORK*) | 572 | unknown |
| `00257c20` | ctleeff_init(int) | 572 | unknown |
| `000962d0` | res0_unpack | 568 | unknown |
| `0009734c` | res2_inverse | 568 | unknown |
| `00167a80` | ASURA_PKT_Analyze(unsigned long*) | 568 | unknown |
| `001729d4` | cDrawPluralFT4RGB(unsigned char*, COLOR*, int, unsigned short, unsigned short, int, int) | 568 | unknown |
| `0024f688` | ctltips_main(CTLINFO*) | 568 | unknown |
| `00096508` | res0_look | 564 | unknown |
| `00189fb0` | eDrawFT4RGB(RECT16*, int, int, COLOR*, int, unsigned short, unsigned short, int) | 564 | unknown |
| `001ac8c8` | DrawPluralFT4RGB(unsigned char*, COLOR*, int, unsigned short, unsigned short, int, int) | 564 | unknown |
| `001bd8e8` | DrawEggWithShadow(short, DVECTOR*, int, COLOR*, int, int) | 564 | unknown |
| `00247a30` | ctlbirthday_init() | 564 | unknown |
| `00259ebc` | ctlhouk_main(CTLINFO*) | 564 | unknown |
| `0025f990` | wldfast_lop() | 564 | unknown |
| `0026760c` | moukeevtinf_window(CTLINFO*, int, int) | 564 | unknown |
| `0009c55c` | drft_forward | 560 | unknown |
| `000bc2bc` | CSOUND_IF_SL::Stream_CreatePlayer(int, int, int) | 560 | unknown |
| `000dc3d4` | direc1(char*) | 560 | unknown |
| `00224e44` | CheckGunResult(int, SVECTOR*, int) | 560 | unknown |
| `0023e06c` | Mdl0023(short, int, int, int) | 560 | unknown |
| `00104798` | Wdirec1(char*) | 556 | unknown |
| `001052e4` | Wdirec2(char*, int) | 556 | unknown |
| `00118cdc` | Wmake_statusscroll() | 556 | unknown |
| `001778a8` | bDrawFT4RGB(RECT16*, int, int, COLOR*, int, unsigned short, unsigned short, int) | 556 | unknown |
| `001997f0` | DrawItemCategory(int, iOS_CMenuTouch*, int, IOS_MENU_TOUCH_RESULT) | 556 | unknown |
| `002b1be8` | AppEngine_Init(int) | 556 | unknown |
| `000a8218` | CEGL2_IF::LoadShaderAll(char*) | 552 | unknown |
| `000b5fac` | CUI_SCROLLBAR::DragEnd(int, int) | 552 | unknown |
| `000e00c4` | request_makeattack() | 552 | unknown |
| `001d8d50` | set_equipbonus(BWORK*, int) | 552 | unknown |
| `001d41d0` | check_tobe_crystal(int, BWORK*) | 548 | unknown |
| `00253b60` | ctlrutegrow_main(CTLINFO*) | 548 | unknown |
| `0027abb4` | MakeMapCostToDest(unsigned char*) | 548 | unknown |
| `002847d8` | Vector_ColorTransform(VECTOR_DATABASE*) | 548 | unknown |
| `000753c0` | deflateSetDictionary | 544 | unknown |
| `00153cb8` | iOS_RESUME_SET_WORK_IW(IOS_RESUME_DATA_WORK_IW*, IOS_RESUME_DATACOPY_MODE) | 544 | unknown |
| `001bdc0c` | DrawUnitWithShadow(short, DVECTOR*, COLOR*, int, int) | 544 | unknown |
| `000bd740` | CSOUND_LOADER_OGG::Decode(signed char*, int, long long, long long, int*) | 540 | unknown |
| `00193a10` | jGetAbilityList(short, short, int, short*, int) | 540 | unknown |
| `0028179c` | iOS_v2menuSetType(V2MENU_TYPE) | 540 | unknown |
| `0029a618` | ClearImage2 | 540 | unknown |
| `000dca14` | direc2(char*, int) | 536 | unknown |
| `002b1124` | SettingsBundle_Init() | 536 | unknown |
| `002b75d0` | RayPick_GT4_input(tagPOLY_GT4*, int, int, int, int) | 536 | unknown |
| `0009c78c` | drft_backward | 532 | unknown |
| `00279cc0` | GetDirectionOfAutoUnit() | 532 | unknown |
| `000aab58` | CEGL2_FBO::Save(_RECT_S32*, char*, int, _G2D_SAVE*) | 528 | unknown |
| `0015b388` | iOSMapCursorCheck() | 528 | unknown |
| `001a9e04` | GetItemList(short, short, signed char, short*, unsigned short, unsigned char) | 528 | unknown |
| `001b8a28` | iOS_RESUME_SET_RESERVE(IOS_RESUME_DATA_RESERVE*, IOS_RESUME_DATACOPY_MODE) | 528 | unknown |
| `00244200` | vEnd_rollproc() | 528 | unknown |
| `0027e470` | iOS_CMenuTouchSaveLoad::setMenuAssistPosition(int) | 528 | unknown |
| `000df864` | event_status_set(unsigned short, unsigned short) | 524 | unknown |
| `000ef5e0` | make_statusscroll() | 524 | unknown |
| `0024c070` | wldbg_init() | 524 | unknown |
| `00088718` | _ve_envelope_init | 520 | unknown |
| `000dfebc` | event_init() | 520 | unknown |
| `00159e5c` | iosAsmBoxCopy(char*, char*, tCOPYFIELD*, tCOPYFIELD*) | 520 | unknown |
| `001639ac` | ASHURA_CVECTOR(long, CVECTOR*) | 520 | unknown |
| `00191d84` | eCursolFunc(DVECTOR*, unsigned short*, int) | 520 | unknown |
| `00198614` | jCursolFunc(DVECTOR*, unsigned short*, int) | 520 | unknown |
| `001c5770` | CursolFunc(DVECTOR*, unsigned short*, int) | 520 | unknown |
| `002494c8` | vOpn_fadeproc(unsigned long*) | 520 | unknown |
| `002708fc` | pagewin_init(PAGEWININFO*) | 520 | unknown |
| `00168088` | ASHURA_EVENT_CLUT_LOAD(int) | 516 | unknown |
| `001753f4` | cCursolFunc(DVECTOR*, unsigned short*, int) | 516 | unknown |
| `0028d854` | tlGarbageCollection() | 516 | unknown |
| `002caebc` | __aeabi_ddiv | 516 | unknown |
| `000b7cd8` | CFILE_UTIL::FileInsert(char*, char*) | 512 | unknown |
| `00177cd0` | bDrawGT4RGB(short*, COLOR*, int, int) | 512 | unknown |
| `001ad634` | DrawGT4RGB(short*, COLOR*, int, int) | 512 | unknown |
| `0021a9ec` | SetCameraWorkWithSchedule(short) | 512 | unknown |
| `0025d33c` | wldstart_check() | 512 | unknown |
| `00273910` | SetSafePanel(int, int) | 512 | unknown |
| `00177ad4` | bDrawFT4RGB2(int, int, int, int, int, int, int, int, COLOR*, int, unsigned short, unsigned short, int) | 508 | unknown |
| `00182380` | bCursolFunc(DVECTOR*, unsigned short*, int) | 508 | unknown |
| `00192f08` | jSwapDB(int, int) | 508 | unknown |
| `001a8914` | GetTotalAbilityList(short, int, short*) | 508 | unknown |
| `0025a228` | houkoku_okng(CTLINFO*) | 508 | unknown |
| `00271ba4` | SetBaseTargetGroup(int, int) | 508 | unknown |
| `002b2448` | EnvSE_Play(int) | 508 | unknown |
| `00072cec` | Android_Dialog_Open(int, int, int, int, char const*, char const*, int) | 504 | unknown |
| `00191a10` | eValueFunc2(unsigned char*) | 504 | unknown |
| `00196bbc` | jGetMaskedPad() | 504 | unknown |
| `0026037c` | ctlmoumes_init(int) | 504 | unknown |
| `0028bb88` | TE_asmTaskEntry(int) | 504 | unknown |
| `000a6a9c` | CG2D_LOADER_TIM::TIM_LoadMemory(unsigned char*) | 500 | unknown |
| `0017376c` | cFontToImageAll(unsigned char*, RECT16*, int, int, unsigned char*, short*, int, short, int) | 500 | unknown |
| `00179ec4` | bFontToImageAll(unsigned char*, RECT16*, int, int, unsigned char*, short*, int, short, int) | 500 | unknown |
| `0018ede8` | eFontToImageAll(unsigned char*, RECT16*, int, int, unsigned char*, short*, int, short, int) | 500 | unknown |
| `00196154` | jFontToImageAll(unsigned char*, RECT16*, int, int, unsigned char*, short*, int, short, int) | 500 | unknown |
| `001a7e34` | GetChrList(short, CHR_STTS**, int) | 500 | unknown |
| `001b6778` | FontToImageAll(unsigned char*, RECT16*, int, int, unsigned char*, short*, int, short, int) | 500 | unknown |
| `001efc6c` | requestDefaultAnimation(tag_animation*) | 500 | unknown |
| `0020c9c4` | fileReadRequestOffset(unsigned int, unsigned int, unsigned int, void*) | 500 | unknown |
| `0021cc84` | StartEffect(long, long, EffectOrder*) | 500 | unknown |
| `0024eadc` | ctlperson_main(CTLINFO*) | 500 | unknown |
| `002576e0` | ctlevtinfo_init(int) | 500 | unknown |
| `000969bc` | res2_class | 496 | unknown |
| `0015813c` | unittoface(int) | 496 | unknown |
| `001896e4` | eGetItemList(short, short, signed char, short*, unsigned short, unsigned char) | 496 | unknown |
| `00194048` | jDrawFT4RGB(RECT16*, int, int, COLOR*, int, unsigned short, unsigned short, int) | 496 | unknown |
| `001bc87c` | UnitTableInit(short) | 496 | unknown |
| `001ccc3c` | getTrapResultDamage(BWORK*, int) | 496 | unknown |
| `0025f44c` | frmbuf_get() | 496 | unknown |
| `0027070c` | pagewinmes_put(PAGEWININFO*, int) | 496 | unknown |
| `0028d498` | tlFree(void*) | 496 | unknown |
| `0015ad38` | iOSexecuteCurSlide() | 492 | unknown |
| `001acd4c` | DrawFT4RGB2(int, int, int, int, int, int, int, int, COLOR*, int, unsigned short, unsigned short, int) | 492 | unknown |
| `0015ec1c` | iOSUnitListOutWin(unsigned char*) | 488 | unknown |
| `00280108` | cSaveFFT::Execute() | 488 | unknown |
| `0028d24c` | tlMallocAlign(unsigned int, unsigned int) | 488 | unknown |
| `0008c274` | vorbis_info_clear | 484 | unknown |
| `000bbc4c` | CSOUND_IF_SL::Static_CreatePlayer(int, int, int) | 484 | unknown |
| `001569ac` | editdirect() | 484 | unknown |
| `001c4eb0` | ValueFunc2(unsigned char*) | 484 | unknown |
| `001d6514` | set_md(unsigned char*) | 484 | unknown |
| `002472a8` | ctlsound_main(CTLINFO*) | 484 | unknown |
| `0026f308` | ctlunreg_main(CTLINFO*) | 484 | unknown |
| `0029f730` | _gte_ncs() | 484 | unknown |
| `00072b0c` | Android_FileEnum(int, char*, CLIST*) | 480 | unknown |
| `0015596c` | worldmap_startinit() | 480 | unknown |
| `0015667c` | world_extend_systemframe(int, int, char*) | 480 | unknown |
| `00253f20` | ctlmap_init() | 480 | unknown |
| `0026c680` | ctltresure_main(CTLINFO*) | 480 | unknown |
| `001a6588` | SwapDB(int, int) | 476 | unknown |
| `001e3324` | setexperience(int, REWARD*) | 476 | unknown |
| `00252c80` | ctlworkend_main(CTLINFO*) | 476 | unknown |
| `002553a8` | ctlhelp2_init(int, int) | 476 | unknown |
| `0025c4fc` | tokuseijob_check() | 476 | unknown |
| `000a1374` | ov_crosslap | 472 | unknown |
| `000aa980` | CEGL2_FBO::Create(int, int, int, int, int) | 472 | unknown |
| `00181ac4` | bValueFunc2(unsigned char*) | 472 | unknown |
| `00193c2c` | jDrawTex(RECT16*, short*, COLOR*, int, int) | 472 | unknown |
| `0019dc10` | SttsEmploy() | 472 | unknown |
| `001d68d8` | change_md(int, int, int, int, int) | 472 | unknown |
| `0025df88` | wldfade_proc() | 472 | unknown |
| `0027207c` | GetNearestUnit(int) | 472 | unknown |
| `0027a974` | BattleRoutineInit() | 472 | unknown |
| `00281400` | iOS_setStatusPTHIT_STATUS(IOS_STTSNUM*, int, int, int, int, void*, int) | 472 | unknown |
| `0029c340` | GsSortFastSprite | 472 | unknown |
| `00077200` | deflateCopy | 468 | unknown |
| `000af644` | CEGL2_TEX_HYBRID::DecodeTexture(unsigned int*, unsigned char*, int, int, unsigned int*, int, int, int, int) | 468 | unknown |
| `0028a16c` | pspSaveDelete() | 468 | unknown |
| `000a3518` | CG2D_LOADER_BMP::BMP_AnalyzeInfoHeader(void*) | 464 | unknown |
| `001022ec` | Wtutorial_hookfunc() | 464 | unknown |
| `001d1a7c` | set_netplayerwork_common(int, int) | 464 | unknown |
| `0021c474` | s25_playObject(_EffectTCB*) | 464 | unknown |
| `0024c27c` | wldbg_draw(GsOT*) | 464 | unknown |
| `0026dd40` | ctlhentuto_init() | 464 | unknown |
| `00290ea4` | LoadImage2 | 464 | unknown |
| `00083e34` | ogg_sync_pageseek | 460 | unknown |
| `000bd56c` | CSOUND_LOADER_OGG::Open(char*, unsigned char*, unsigned int, unsigned int) | 460 | unknown |
| `002608c0` | ctlokng_init(_POINT) | 460 | unknown |
| `0027fcb8` | cSaveFFT::Save(int) | 460 | unknown |
| `000b7120` | CFILE_TXT::Save(char*, unsigned int) | 456 | unknown |
| `000d8a34` | faceuvclut(tagPOLY_FT4*, int, int*) | 456 | unknown |
| `0018a1e4` | eDrawFT4RGB2(int, int, int, int, int, int, int, int, COLOR*, int, unsigned short, unsigned short, int) | 456 | unknown |
| `0024cda0` | ctlbrst_active(CTLINFO*) | 456 | unknown |
| `0025990c` | ctlhistory_main(CTLINFO*) | 456 | unknown |
| `00268384` | rutegrow_init(int, int) | 456 | unknown |
| `0026b0f4` | wld_snpl() | 456 | unknown |
| `000a3c18` | CG2D_LOADER_BMP::BMP_LoadFile(char*, unsigned int) | 452 | unknown |
| `000bc0a4` | CSOUND_IF_SL::Play(int, int, int, int, int) | 452 | unknown |
| `001a7884` | SetChrListOne(int) | 452 | unknown |
| `001b8c38` | sort_init() | 452 | unknown |
| `001d8b58` | get_ability_address(int, ABILITY_COMMON_DATA**, void**) | 452 | unknown |
| `0029dd18` | _gte_rtps() | 452 | unknown |
| `000a6618` | CG2D_LOADER_TIM::TIM_AnalyzeFileHeader(void*) | 448 | unknown |
| `000bbe7c` | CSOUND_IF_SL::LoadPCM(int, char*, unsigned char*, unsigned int, unsigned int, int) | 448 | unknown |
| `00172c0c` | cDrawFT4RGB(RECT16*, int, int, COLOR*, int, unsigned short, unsigned short, int) | 448 | unknown |
| `00172dcc` | cDrawFT4RGB2(int, int, int, int, int, int, int, int, COLOR*, int, unsigned short, unsigned short, int) | 448 | unknown |
| `001abc4c` | GetShapeData(short, short*) | 448 | unknown |
| `001e10c8` | get_unit_height(int) | 448 | unknown |
| `0020ebc4` | loadEventAnimation(int, unsigned char*) | 448 | unknown |
| `0024e91c` | ctlpersmes_init(int) | 448 | unknown |
| `00078390` | gzread | 444 | unknown |
| `0009cd08` | vorbis_synthesis | 444 | unknown |
| `0017c0c0` | UnitBakOne(int) | 444 | unknown |
| `0019d304` | DressSellStock() | 444 | unknown |
| `001bd72c` | UnitBakTwo(int, int) | 444 | unknown |
| `002529ac` | ctlworkend_init() | 444 | unknown |
| `0026d7ec` | wld_tutomenu_reset(CTLINFO*) | 444 | unknown |
| `000d7bb4` | initstatusback(RECT16*, STTSWINDOWBACK*) | 440 | unknown |
| `000ff7a4` | Winitstatusback(RECT16*, STTSWINDOWBACK*) | 440 | unknown |
| `00188c6c` | eSetChrList() | 440 | unknown |
| `0027edbc` | iOS_CMenuTouchSaveLoad::drawMenuAssist(int, long*) | 440 | unknown |
| `00280c44` | iOS_setStatusLVEXP_STATUS(IOS_STTSNUM*, int, int, int, int, int, void*, int) | 440 | unknown |
| `0015047c` | setjoinus_net() | 436 | unknown |
| `001eb124` | loadAbilityAnimation(tag_animation*, void*) | 436 | unknown |
| `0020c264` | db_init(int, int, int, unsigned char, unsigned char, unsigned char) | 436 | unknown |
| `0026c860` | picsand_draw(GsIMAGE*, int) | 436 | unknown |
| `00077c18` | gzseek64 | 432 | unknown |
| `000b63d0` | CCOMP_Z_ENC::Encode(unsigned char*, unsigned char*, int, int) | 432 | unknown |
| `0019df84` | AccountEmploy() | 432 | unknown |
| `00212a04` | requestDestinationGradation(int, CVECTOR*) | 432 | unknown |
| `0026abac` | timeevt_chk() | 432 | unknown |
| `0027f680` | iOS_Suspend(IOS_RESUME_MODE) | 432 | unknown |
| `00087280` | vorbis_book_decode | 428 | unknown |
| `000e1c0c` | iOS_statusfigprint16_FT4(tagPOLY_FT4*, int, unsigned short, int, int, void*, int, int, COPYFIELD*, int) | 428 | unknown |
| `001106f8` | WiOS_statusfigprint16_FT4(tagPOLY_FT4*, int, unsigned short, int, int, void*, int, int, COPYFIELD*, int) | 428 | unknown |
| `001eb8d8` | setPanelPrioritySub(SVECTOR*, SVECTOR*, int) | 428 | unknown |
| `0020fb18` | db_init_all(int, int, int, unsigned char, unsigned char, unsigned char) | 428 | unknown |
| `00247884` | birthday_change(CTLINFO*) | 428 | unknown |
| `000b79d8` | CFILE_UTIL::FileCopy(char*, char*) | 424 | unknown |
| `0010da78` | Wrequest_makeattack() | 424 | unknown |
| `00270520` | valnumwin_set(int, unsigned long, int, _POINT*) | 424 | unknown |
| `00276788` | CheckUnitActionOK(unsigned char*) | 424 | unknown |
| `00286140` | pspMapArrayOperate(unsigned int, unsigned char, unsigned char, unsigned int, short*, short*, short*, short*, short*, short*, short*, short*, short*, short*, short*, short*) | 424 | unknown |
| `000ab4b0` | CEGL2_FBO::ErrorGL(char const*, char const*, unsigned int) | 420 | unknown |
| `000aecb8` | CEGL2_SPRITE::ErrorGL(char const*, char const*, unsigned int) | 420 | unknown |
| `0025d64c` | wldiwasaki_put(GsOT*) | 420 | unknown |
| `00267ad0` | ctlret_main(CTLINFO*) | 420 | unknown |
| `00274018` | ForChantedAction() | 420 | unknown |
| `000a0374` | ov_bitrate | 416 | unknown |
| `00100b2c` | Wmultiwindow_break(unsigned long*) | 416 | unknown |
| `0015a988` | sBattleTouchRotationMain() | 416 | unknown |
| `001d3e18` | get_comwindow_data(int) | 416 | unknown |
| `0024f4e8` | ctltipsmes_init(int) | 416 | unknown |
| `0026fca8` | ctluwa_main(CTLINFO*) | 416 | unknown |
| `002b2814` | SE_Play(int) | 416 | unknown |
| `000859f8` | vorbis_analysis_wrote | 412 | unknown |
| `000b6204` | CCOMP_Z_DEC::Decode(unsigned char*, unsigned char*, int) | 412 | unknown |
| `000d91c4` | multiwindow_packetanm(COMRECORD*, PRIMPACKET*, int, int) | 412 | unknown |
| `00100fdc` | Wmultiwindow_packetanm(COMRECORD*, PRIMPACKET*, int, int) | 412 | unknown |
| `00173584` | cFontToImage(int, unsigned char*, RECT16*, int) | 412 | unknown |
| `00173abc` | cMakeTextureMessage(unsigned char*, short*, RECT16*, int) | 412 | unknown |
| `00179cdc` | bFontToImage(int, unsigned char*, RECT16*, int) | 412 | unknown |
| `0017a154` | bMakeTextureMessage(unsigned char*, short*, RECT16*, int) | 412 | unknown |
| `0018ec00` | eFontToImage(int, unsigned char*, RECT16*, int) | 412 | unknown |
| `0018f0c8` | eMakeTextureMessage(unsigned char*, short*, RECT16*, int) | 412 | unknown |
| `00195f6c` | jFontToImage(int, unsigned char*, RECT16*, int) | 412 | unknown |
| `00196348` | jMakeTextureMessage(unsigned char*, short*, RECT16*, int) | 412 | unknown |
| `0019dde8` | BuyEmploy() | 412 | unknown |
| `001b6590` | FontToImage(int, unsigned char*, RECT16*, int) | 412 | unknown |
| `0021d04c` | DisposeTCB(short) | 412 | unknown |
| `00225074` | CheckEventGunResult(int, SVECTOR*, int) | 412 | unknown |
| `0024e734` | ctlperson_init() | 412 | unknown |
| `0025bf88` | mkbasept_calc() | 412 | unknown |
| `002cb2e8` | __aeabi_frsub | 412 | unknown |
| `000a0514` | ov_time_seek | 408 | unknown |
| `000a06ac` | ov_time_seek_page | 408 | unknown |
| `00123de0` | Wdisp_noframe() | 408 | unknown |
| `0013728c` | disp_noframe() | 408 | unknown |
| `00165388` | ASHURA_matrix(MATRIX*, SVECTOR*, VECTOR*, VECTOR*) | 408 | unknown |
| `001782e8` | bDrawTexFree(short*, COLOR*, int, int) | 408 | unknown |
| `0018a6e4` | eDrawTexFree(short*, COLOR*, int, int) | 408 | unknown |
| `00194554` | jDrawTexFree(short*, COLOR*, int, int) | 408 | unknown |
| `001ab918` | AbilityLearning(short, short, short) | 408 | unknown |
| `0021ef4c` | InitPermanentEffect() | 408 | unknown |
| `00269034` | wldencount_chk(int, int) | 408 | unknown |
| `00285f8c` | hockRead(void*, int, unsigned int) | 408 | unknown |
| `002cb538` | __aeabi_fmul | 408 | unknown |
| `000e1118` | bgput(tagPOLY_FT4*, RECT16*, RECT16*, BGRECORD*) | 404 | unknown |
| `0010fb74` | Wbgput(tagPOLY_FT4*, RECT16*, RECT16*, BGRECORD*) | 404 | unknown |
| `00159aac` | asm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 404 | unknown |
| `0015e5d4` | iOSShiftUnitGet() | 404 | unknown |
| `00162080` | wasm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 404 | unknown |
| `0024dcd8` | ctlkiromes_init(int) | 404 | unknown |
| `00266a00` | infonumber_put_zero(int, int, GsSPRITE*, GsOT*, int) | 404 | unknown |
| `00280304` | Savedata_LoadGameCleared(unsigned char*, int*) | 404 | unknown |
| `00284144` | mapclip_load(int) | 404 | unknown |
| `002cb2f0` | __aeabi_fsub | 404 | unknown |
| `00078d9c` | gzwrite | 400 | unknown |
| `000a3a24` | CG2D_LOADER_BMP::BMP_AnalyzeBitMask(unsigned int*) | 400 | unknown |
| `000b91d8` | CSTR_UTIL::ToAbsolutePath(char*, char*, char*) | 400 | unknown |
| `000bad78` | CSOUND_IF::Play(int, int, int, int, unsigned char) | 400 | unknown |
| `00188880` | eSttsCSub(C_STTS*, C_STTS*, C_STTS*, int) | 400 | unknown |
| `001a8d6c` | SttsCSub(C_STTS*, C_STTS*, C_STTS*, int) | 400 | unknown |
| `001ad3bc` | DrawTexFree(short*, COLOR*, int, int) | 400 | unknown |
| `002005bc` | executeForceMoveProcs(tag_animation*) | 400 | unknown |
| `002595c0` | ctlhistory_init() | 400 | unknown |
| `0027b0b0` | MakeMapDanger() | 400 | unknown |
| `002849fc` | Vector_AffineTransform(int) | 400 | unknown |
| `0028b89c` | executeTaskEmu() | 400 | unknown |
| `002b1600` | GX_Init(int) | 400 | unknown |
| `002cb2f4` | __aeabi_fadd | 400 | unknown |
| `000a2240` | CG2D_LOADER::Load(char*, unsigned char*, unsigned int, unsigned int) | 396 | unknown |
| `000a2400` | CG2D_LOADER::CopyAsTexture(void*, int, int, int) | 396 | unknown |
| `0010d8ec` | Wevent_init() | 396 | unknown |
| `001d7538` | get_command_ability(int, int) | 396 | unknown |
| `0024e5a8` | iOS_chkBraveEventFlag(unsigned int) | 396 | unknown |
| `00259780` | ctlhismes_init(int) | 396 | unknown |
| `002875a8` | Draw_Win(int) | 396 | unknown |
| `0028ccb4` | CAUTOSAVE::IsExist() | 396 | unknown |
| `000af818` | CEGL2_TEX_HYBRID::GL_Load(int, unsigned int*, unsigned int, int, int, int, int, unsigned char*) | 392 | unknown |
| `000cbdf4` | iOS_RESUME_SET_ATTACK(IOS_RESUME_DATA_ATTACK*, IOS_RESUME_DATACOPY_MODE) | 392 | unknown |
| `000da83c` | calceffectangle(int, int) | 392 | unknown |
| `00175634` | cSelectWindowClut(int) | 392 | unknown |
| `001774dc` | bDrawG4(RECT16*, COLOR*, int, int) | 392 | unknown |
| `001834c8` | bSelectWindowClut(int) | 392 | unknown |
| `00192cc8` | eSelectWindowClut(int) | 392 | unknown |
| `00199484` | jSelectWindowClut(int) | 392 | unknown |
| `001ac4ec` | DrawG4(RECT16*, COLOR*, int, int) | 392 | unknown |
| `001c6fb4` | SelectWindowClut(int) | 392 | unknown |
| `001cd308` | check_learning(int, unsigned short*) | 392 | unknown |
| `001d5640` | get_actwindow_data(int, unsigned char*, unsigned char*, unsigned char*) | 392 | unknown |
| `001ef76c` | requestAttackAnimation(tag_animation*, tag_animation*) | 392 | unknown |
| `002031a4` | iOSsetCursorByTouch(int, int, int, int, int) | 392 | unknown |
| `00256174` | ctlfsetnum_main(CTLINFO*) | 392 | unknown |
| `000b9bc4` | CSTR_UTIL::DecodeEscSequence(char*, char*) | 388 | unknown |
| `0015daf4` | iOSQSort(short*, short*, short*, short*, int, int, int) | 388 | unknown |
| `00176b80` | bChrSort(int) | 388 | unknown |
| `001b6c00` | MakeTextureMessage2(unsigned char*, short*, RECT16*, int) | 388 | unknown |
| `00201798` | setActionDirection(tag_animation*, tag_animation*) | 388 | unknown |
| `0025c928` | ctlshogou_main(CTLINFO*) | 388 | unknown |
| `002c9b11` | __gxx_personality_v0 | 388 | unknown |
| `00094cd4` | _vp_noisemask | 384 | unknown |
| `000ab674` | CEGL2_SHADER::Load(int, char const*, char const*) | 384 | unknown |
| `00102504` | Wcalceffectangle(int, int) | 384 | unknown |
| `0015dc78` | iOSUnitPosGet(int*, int*, unsigned long*, int*) | 384 | unknown |
| `00193750` | jGetChrSingle(int) | 384 | unknown |
| `001cced8` | get_ma_result(BWORK*) | 384 | unknown |
| `001f4440` | InitAnimationInit() | 384 | unknown |
| `00242498` | ctlendroll_init() | 384 | unknown |
| `002453a4` | fft_ending() | 384 | unknown |
| `0024581c` | movie_init(int, int, int, int, int, char*) | 384 | unknown |
| `0027fe84` | Savedata_Load(unsigned char*, int*) | 384 | unknown |
| `00287734` | Draw_Lose(int) | 384 | unknown |
| `0028e2e4` | CdControl | 384 | unknown |
| `002b78ac` | RayPick_FT4(tagPOLY_FT4*, int, int) | 384 | unknown |
| `00082704` | oggpackB_write | 380 | unknown |
| `000b68ac` | CFILE_DAT::Open(char*, int, int) | 380 | unknown |
| `0019f798` | MainShop() | 380 | unknown |
| `001b8e64` | TutrialInit(int) | 380 | unknown |
| `001d205c` | check_trap(unsigned char, unsigned char, unsigned char) | 380 | unknown |
| `001d972c` | get_shape2(BWORK*, unsigned char*) | 380 | unknown |
| `00205518` | iOSBtlUnit_Hp_Mp(int, int, int) | 380 | unknown |
| `0022a6a4` | _ReadTMD(TMD_PRIM*) | 380 | unknown |
| `00283fc8` | mapclip_save(int) | 380 | unknown |
| `002b2b7c` | SysSE_Play(int, int) | 380 | unknown |
| `0018fc84` | eGetMaskedPad() | 376 | unknown |
| `001f0af8` | requestDefaultGraphic(tag_animation*, int) | 376 | unknown |
| `0020fd1c` | InitializeAll() | 376 | unknown |
| `0027d53c` | iOS_CMenuTouchNum::initPacket() | 376 | unknown |
| `00294980` | xpLibgpuVramChangeDispMode | 376 | unknown |
| `00082578` | oggpack_write | 372 | unknown |
| `000d123c` | Ddisp_staticwindow2() | 372 | unknown |
| `00123a74` | Edisp_staticwindow2() | 372 | unknown |
| `001443b0` | Cdisp_staticwindow2() | 372 | unknown |
| `0015e7a4` | iOSStatusSlideSet() | 372 | unknown |
| `0024f8c0` | ctltipsmes_main(CTLINFO*) | 372 | unknown |
| `00266c84` | wldday_put(GsOT*) | 372 | unknown |
| `0026baec` | wldtown_init() | 372 | unknown |
| `002b052c` | CAPP_INFO::Init(int) | 372 | unknown |
| `000a8ec4` | CEGL2_IF::AddTile(int, int, int, int, int, unsigned char, unsigned char, unsigned char, unsigned char, unsigned char) | 368 | unknown |
| `000ff2cc` | Wdisposetexture(RECT16*) | 368 | unknown |
| `0019d634` | MonsterNameInput() | 368 | unknown |
| `001d1204` | get_reflection_coord(BWORK*, int, int, int, int*, int*, int*) | 368 | unknown |
| `001d9d70` | get_item_number(unsigned short, int) | 368 | unknown |
| `00210eac` | initMap(int, int) | 368 | unknown |
| `00211a28` | SetChangePaletteData(unsigned short, unsigned short, unsigned short, unsigned short, unsigned short) | 368 | unknown |
| `002485b0` | ctlmusic_init() | 368 | unknown |
| `0029270c` | xpLibgpuStoreImage | 368 | unknown |
| `0007cf58` | inflateCopy | 364 | unknown |
| `000a5be4` | CG2D_LOADER_TGA::TGA_LoadFile(char*, unsigned int) | 364 | unknown |
| `000ff4b0` | Wallocatememorywait(int) | 364 | unknown |
| `000adf14` | CEGL2_SPRITE::OnResume() | 360 | unknown |
| `000d8c74` | multiwindow_keydown(COMRECORD*) | 360 | unknown |
| `001009c4` | Wmultiwindow_keydown(COMRECORD*) | 360 | unknown |
| `00104a70` | Wdirec4(char*) | 360 | unknown |
| `0015e918` | iOSBtlStsOutWin() | 360 | unknown |
| `0018990c` | eIsItemEquip(short, short, short) | 360 | unknown |
| `0029c780` | GsSortBoxFill | 360 | unknown |
| `000785e8` | gzungetc | 356 | unknown |
| `0007874c` | gzgets | 356 | unknown |
| `0008d7e0` | vorbis_lpc_predict | 356 | unknown |
| `000b42b0` | CINPUT_IF_TOUCH::OnTouchesBegan(int, int, int, int, int) | 356 | unknown |
| `000dc6ec` | direc4(char*) | 356 | unknown |
| `000e7da8` | seekcodeplus(int, int, int, int) | 356 | unknown |
| `00102f04` | Wseekcodeplus(int, int, int, int) | 356 | unknown |
| `001ab67c` | JobEquip(short, short, int) | 356 | unknown |
| `0024b824` | ctlbar_exit(CTLINFO*) | 356 | unknown |
| `0025caac` | wldframe_clr(int) | 356 | unknown |
| `0026679c` | wld_window(WINPAC*, GsOT*) | 356 | unknown |
| `00268220` | wldrute_tblget(WALKINFO*, int, int) | 356 | unknown |
| `000b6cd8` | CFILE_DAT::Load(int, int, int) | 352 | unknown |
| `000d7720` | disposetexture(RECT16*) | 352 | unknown |
| `0015af24` | iOSexecuteScroll() | 352 | unknown |
| `001d1de8` | set_unitcoord(int, unsigned char, unsigned char, unsigned char, unsigned char) | 352 | unknown |
| `0020f004` | getAnimationLoadAreaStatus(char*) | 352 | unknown |
| `0026fb48` | ctluwames_init(int) | 352 | unknown |
| `002878b4` | Draw_Draw(int) | 352 | unknown |
| `0029ffac` | RotMatrix | 352 | unknown |
| `002cb6d0` | __aeabi_fdiv | 352 | unknown |
| `000a1dc0` | CG2D_LOADER::Save(void*, int, int, _G2D_SAVE*) | 348 | unknown |
| `001597c0` | disp_worlddhelpmenu() | 348 | unknown |
| `001cb678` | change_moruboru(BWORK*) | 348 | unknown |
| `001d4468` | check_game_cont() | 348 | unknown |
| `001da038` | initBdata() | 348 | unknown |
| `001e6368` | forecast_skill(BWORK*, BWORK*, ACT*) | 348 | unknown |
| `0020ce1c` | fileOpenPC(char*, void*, int, int) | 348 | unknown |
| `0021f190` | DisposePEffectTCB(unsigned char) | 348 | unknown |
| `0021ff74` | p09_chakusuiFunc() | 348 | unknown |
| `00244f18` | roll_autochange() | 348 | unknown |
| `0024748c` | ctlchrmake_init() | 348 | unknown |
| `0024ac38` | vOpn_defscrwin_set(int, int, _POINT*, _POINT*) | 348 | unknown |
| `002615cc` | ctlhaken_main(CTLINFO*) | 348 | unknown |
| `0027e7a4` | iOS_CMenuTouchSaveLoad::execTap(IOS_MENU_TOUCH_SAVELOAD_RESULT*, int*, int*) | 348 | unknown |
| `0029aabc` | ReadTIM | 348 | unknown |
| `002b582c` | Logo_Init() | 348 | unknown |
| `000b4d30` | CINPUT_IF_TOUCH::GetTouchState(_INPUT_DEVICE_TOUCH*, _INPUT_DATA*) | 344 | unknown |
| `000d78f0` | allocatememorywait(int) | 344 | unknown |
| `0012cc1c` | disp_staticwindow2() | 344 | unknown |
| `0015d400` | iOSUnitPrmWorkSet(tagPOLY_FT4*, int, unsigned long) | 344 | unknown |
| `0016f5e0` | iOS_RESUME_SET_ASURA(IOS_RESUME_DATA_ASURA*, IOS_RESUME_DATACOPY_MODE) | 344 | unknown |
| `001d5188` | set_sanjutsuability3(int, unsigned char, short*) | 344 | unknown |
| `0020fe94` | InitializeHot() | 344 | unknown |
| `002578d4` | ctlevtinfo_main(CTLINFO*) | 344 | unknown |
| `0025ecd8` | iOSWorldPlayer_Hp_Mp(unsigned int, unsigned int) | 344 | unknown |
| `002a2e08` | xpLibSN::PCopen(char*, int, int, int) | 344 | unknown |
| `002b32e8` | musicPlayer_FrameMove() | 344 | unknown |
| `0017b178` | bMenuSel2D(int, int, int, int, int) | 340 | unknown |
| `00189494` | eRefleshItemUserSort(int) | 340 | unknown |
| `001a9bc0` | RefleshItemUserSort(int) | 340 | unknown |
| `001b7d64` | MenuSel2D(int, int, int, int, int) | 340 | unknown |
| `001b9104` | iOSTutoBattleKeyWaitCheck(unsigned long, short) | 340 | unknown |
| `001ef618` | requestAttackSound(tag_animation*, int) | 340 | unknown |
| `00248cd0` | ctlcard_main(CTLINFO*) | 340 | unknown |
| `0027dc00` | iOS_CMenuTouchNum::execTap(int*, IOS_MENU_TOUCH_NUM_RESULT*) | 340 | unknown |
| `000a1614` | _vorbis_apply_window | 336 | unknown |
| `000b7b88` | CFILE_UTIL::FileConnect(char*, char*, int) | 336 | unknown |
| `000d9d84` | request_help() | 336 | unknown |
| `00101a40` | Wrequest_help() | 336 | unknown |
| `00224650` | CheckBowReachable(unsigned char, unsigned char) | 336 | unknown |
| `00255a38` | ctlflagset_init() | 336 | unknown |
| `0026c27c` | ctltresure_init() | 336 | unknown |
| `00273b78` | MakeMoveAreaNearByDestination(int) | 336 | unknown |
| `00081494` | unzLocateFile | 332 | unknown |
| `000a0884` | ov_time_tell | 332 | unknown |
| `000a6db4` | CGX_SCREEN_CORRECT::Init(int, int, int, int) | 332 | unknown |
| `000a977c` | CEGL2_IF::DrawTile(float, float, float, float, unsigned int) | 332 | unknown |
| `000ac134` | std::priv::_Rb_global<bool>::_Rebalance(std::priv::_Rb_tree_node_base*, std::priv::_Rb_tree_node_base*&) | 332 | unknown |
| `000ac280` | std::priv::_Rb_tree<int, std::less<int>, std::pair<int const, CEGL2_SHADER::DATA_SHADER>, std::priv::_Select1st<std::pair<int const, CEGL2_SHADER::DATA_SHADER> >, std::priv::_MapTraitsT<std::pair<int const, CEGL2_SHADER::DATA_SHADER> >, std::allocator<std::pair<int const, CEGL2_SHADER::DATA_SHADER> > >::_M_insert(std::priv::_Rb_tree_node_base*, std::pair<int const, CEGL2_SHADER::DATA_SHADER> const&, std::priv::_Rb_tree_node_base*, std::priv::_Rb_tree_node_base*) | 332 | unknown |
| `000b50e8` | CRECT::DropTest(_RECT_S32*) | 332 | unknown |
| `000bac2c` | CSOUND_IF::FrameMove(int, float) | 332 | unknown |
| `000bb6e8` | CSOUND_IF_SL::EngineInit(int) | 332 | unknown |
| `001b8650` | GetMaskedPad() | 332 | unknown |
| `001d21d8` | get_stop_event(BWORK*) | 332 | unknown |
| `00225644` | objectAnim(_EffectTCB*, _Object*) | 332 | unknown |
| `002809cc` | iOS_setNumPrim(tagPOLY_FT4*, int, int, int, int) | 332 | unknown |
| `0029ac20` | xpLibgpuLoadImageTrans | 332 | unknown |
| `0015570c` | worldmap_faceload() | 328 | unknown |
| `001a8c24` | GetItemParameter(short, A_STTS*, C_STTS*, int) | 328 | unknown |
| `00269fd8` | snpl_picput() | 328 | unknown |
| `0026b724` | worldmap_new() | 328 | unknown |
| `0007f240` | _tr_stored_block | 324 | unknown |
| `000a258c` | CG2D_LOADER::CopyAsTexture(unsigned int*, int, int, unsigned int*, _G2D_FORMAT*, int) | 324 | unknown |
| `000b7eec` | CFILE_UTIL::DirCopy(char*, char*) | 324 | unknown |
| `001612d0` | iOSsTchBtlInit() | 324 | unknown |
| `001ab17c` | IsItemEquip(short, short, short) | 324 | unknown |
| `002169d0` | InitSound() | 324 | unknown |
| `00253d84` | ctltownset_main(CTLINFO*) | 324 | unknown |
| `00261c68` | mouketeam_scrollset(CTLINFO*) | 324 | unknown |
| `00286600` | pspMapTexUVCorrect(unsigned int, unsigned char, unsigned int, unsigned char*, unsigned char*, unsigned char*, unsigned char*, unsigned char*, unsigned char*, unsigned char*, unsigned char*) | 324 | unknown |
| `002b20f4` | onGotoNextMode(int) | 324 | unknown |
| `0007cdd8` | inflateSync | 320 | unknown |
| `00096190` | res0_pack | 320 | unknown |
| `00135080` | Wdisp_staticwindow2() | 320 | unknown |
| `001938d0` | jGetJobList(unsigned char, short*, int) | 320 | unknown |
| `0026bc60` | wldtown_bright() | 320 | unknown |
| `00289c1c` | pspFftDelete(int*) | 320 | unknown |
| `00084628` | vorbis_bitrate_init | 316 | unknown |
| `000b495c` | CINPUT_IF_TOUCH::GetGestureSwipe_Old(int, int, int, unsigned int) | 316 | unknown |
| `000c9504` | attackfaceuvclut(tagPOLY_FT4*, int) | 316 | unknown |
| `00100704` | Wfaceuvclut(tagPOLY_FT4*, int, int*) | 316 | unknown |
| `00201588` | initializeTurn() | 316 | unknown |
| `0021d408` | doSchedulePtclCommandOnce(unsigned short, unsigned char, _EffectTCB*) | 316 | unknown |
| `002201ec` | p13_levelupFunc() | 316 | unknown |
| `00243048` | fRoll_mesput(short*) | 316 | unknown |
| `0025eea8` | fftCdLoopTim(CDREC*) | 316 | unknown |
| `00162d5c` | iOS_IsInYellowMesh(int, int) | 312 | unknown |
| `00188748` | eGetItemParameter(short, A_STTS*, C_STTS*, int) | 312 | unknown |
| `001d2c10` | get_battlebonus(B_BONUS*) | 312 | unknown |
| `001dc778` | levelup_one(BWORK*, int) | 312 | unknown |
| `0020c418` | db_swap(unsigned long*, unsigned long*) | 312 | unknown |
| `002231d8` | GetBowReachableTangent(BowCheckWork*, int*, int*) | 312 | unknown |
| `0025a0f0` | ctlhoukmes_init(int) | 312 | unknown |
| `0027add8` | MakeMapChantedAction() | 312 | unknown |
| `002a0eec` | OuterProduct0 | 312 | unknown |
| `002b2d10` | Jingle_Play(int) | 312 | unknown |
| `000a7ec4` | CEGL2_IF::SetBlendMode(int) | 308 | unknown |
| `000a94c4` | CEGL2_IF::Draw(CEGL2_SPRITE*, float, float, float, float, float, float, unsigned int, int, int, int, int) | 308 | unknown |
| `001615dc` | iOSSdNovelSelectSet(int, int) | 308 | unknown |
| `001d8fd0` | levelup_eggmonster(UM_WORK*, int) | 308 | unknown |
| `001e31f0` | add_jobpointB(int, int, unsigned char, int) | 308 | unknown |
| `00203070` | setCursorByTouch(int, int, int) | 308 | unknown |
| `002130c4` | requestDestinationAnbient(int, CVECTOR*) | 308 | unknown |
| `00213734` | requestDestinationFlat(int, CVECTOR*) | 308 | unknown |
| `0026ef3c` | ctlunreg_init() | 308 | unknown |
| `00270b5c` | pageupdown_cursor(PAGEWININFO*) | 308 | unknown |
| `0028e0c8` | xpLibapiSaveCheck | 308 | unknown |
| `0029a490` | xpSetDrawMove | 308 | unknown |
| `000a3e34` | CG2D_LOADER_BMP::Load(char*, unsigned char*, unsigned int, unsigned int) | 304 | unknown |
| `000d9360` | multiwindow_packetclip(CLIP*, RECT16*, int, int) | 304 | unknown |
| `000d9f34` | request_option() | 304 | unknown |
| `00101178` | Wmultiwindow_packetclip(CLIP*, RECT16*, int, int) | 304 | unknown |
| `00101bf0` | Wrequest_option() | 304 | unknown |
| `001a9424` | GetItemType(short, short) | 304 | unknown |
| `001d29d0` | search_character_f(int) | 304 | unknown |
| `001d67a8` | get_mapid(int, int, int, int) | 304 | unknown |
| `0020ee48` | activateCompressedAnimation(int, int) | 304 | unknown |
| `00225514` | MemoryMapper() | 304 | unknown |
| `00244de8` | roll_bkfade() | 304 | unknown |
| `00255908` | ctlflag_winset(CTLINFO*) | 304 | unknown |
| `002b6d80` | iOSUnitListCurAreaTapCheck() | 304 | unknown |
| `002b6eb0` | iOSUnitListCurAreaTapNowCheck() | 304 | unknown |
| `002bb7e0` | iOSTutoSkipKeyCheck() | 304 | unknown |
| `002bf1fc` | Main_Settings_DrawYesNo(int, int, int) | 304 | unknown |
| `0024717c` | ctlsound_init() | 300 | unknown |
| `002530b8` | ctlbrst_zodiac() | 300 | unknown |
| `00255054` | ctlmap_eventchk() | 300 | unknown |
| `00256ec8` | ctltownmenu_exit(CTLINFO*, int) | 300 | unknown |
| `00257af4` | ctlparty_main(CTLINFO*) | 300 | unknown |
| `00280b18` | iOS_setStatusNo_STATUS(IOS_STTSNUM*, int, int, int, int, void*, int) | 300 | unknown |
| `002b3464` | Boot_Init() | 300 | unknown |
| `000729e4` | Android_GetSystemPath(int, char*) | 296 | unknown |
| `000d94e0` | multiwindow_packetadd(PRIMPACKET*, int, int) | 296 | unknown |
| `001012f8` | Wmultiwindow_packetadd(PRIMPACKET*, int, int) | 296 | unknown |
| `001ac3c4` | DrawF4(short*, COLOR*, int, int) | 296 | unknown |
| `001b2ac8` | SetJobName() | 296 | unknown |
| `001d40a8` | set_monsterability2(int, unsigned char, short*, int, unsigned char*) | 296 | unknown |
| `001fd3ec` | requestParmanentEffect(tag_animation*) | 296 | unknown |
| `00255280` | ctlopt_init() | 296 | unknown |
| `0025ddb8` | wlddisp_mask(int) | 296 | unknown |
| `0027ec94` | iOS_CMenuTouchSaveLoad::exec(int*, int*) | 296 | unknown |
| `000adbb0` | CEGL2_SPRITE::LoadBegin(int, int, int) | 292 | unknown |
| `0015d558` | iOSUnitCheck(tagPOLY_GT4*) | 292 | unknown |
| `00200bb8` | eventZoomChange(int) | 292 | unknown |
| `0025e310` | sun_to_ivarisday(int*, int*) | 292 | unknown |
| `002702f0` | scrwin_para_set(int, int, _POINT*, _POINT*) | 292 | unknown |
| `0027d808` | iOS_CMenuTouchNum::drawDebug() | 292 | unknown |
| `002a3648` | pspSaveBase::Update() | 292 | unknown |
| `000758c8` | deflateBound | 288 | unknown |
| `00079058` | gzvprintf | 288 | unknown |
| `0007f388` | _tr_align | 288 | unknown |
| `000c18cc` | disp_maptitle() | 288 | unknown |
| `000da35c` | event_init_memory() | 288 | unknown |
| `00219608` | SetEffectScaleCameraWork(int, int, int, VECTOR*) | 288 | unknown |
| `00221d64` | RequestHitMarkEffect(long, EffectOrder*, long) | 288 | unknown |
| `00249da4` | vOpn_dataload() | 288 | unknown |
| `0026af98` | snpl_effcheck(int, int, int) | 288 | unknown |
| `002899a0` | pspFftSave(int, FFT_SAVE_DATA*, int*) | 288 | unknown |
| `0019f914` | ExitShop() | 284 | unknown |
| `001a6410` | MessageDataSet(int) | 284 | unknown |
| `001ccafc` | get_floor_damage(BWORK*) | 284 | unknown |
| `001eac28` | searchAnimationByPositionBattle(int, int, int) | 284 | unknown |
| `0021fd48` | p06_chargeFunc() | 284 | unknown |
| `002200d0` | p12_poisonFunc() | 284 | unknown |
| `00269620` | iOS_RESUME_SET_WLDSAVE(IOS_RESUME_DATA_WLDSAVE*, IOS_RESUME_DATACOPY_MODE) | 284 | unknown |
| `0027f904` | iOS_Resume() | 284 | unknown |
| `00076cf0` | deflateParams | 280 | unknown |
| `000a2128` | CG2D_LOADER::GetSavePixelFormatOverwrite(_G2D_FORMAT*, int) | 280 | unknown |
| `000bb38c` | CSOUND_IF::Pause(int, unsigned char) | 280 | unknown |
| `000dfbdc` | request_status(int, int, int) | 280 | unknown |
| `0010c888` | Wrequest_status(int, int, int) | 280 | unknown |
| `00156564` | request_worldcommand(int, int, int) | 280 | unknown |
| `00163148` | ASHURA_LightMatrix(MATRIX*, MATRIX*) | 280 | unknown |
| `00163bb4` | iOS_initTouchDisable(int) | 280 | unknown |
| `00188630` | eGetItemUserSort(int, short*) | 280 | unknown |
| `001a810c` | GetItemUserSort(int, short*) | 280 | unknown |
| `001ac774` | DrawLineG3(RECT16*, COLOR*, int, int) | 280 | unknown |
| `001c0564` | LRCurChrChg(short) | 280 | unknown |
| `00200e2c` | eventFukanChange(int) | 280 | unknown |
| `0021b108` | LoadEffectTIM(short) | 280 | unknown |
| `0024935c` | vOpn_swapbuff() | 280 | unknown |
| `0024971c` | vOpn_key_rep(unsigned long) | 280 | unknown |
| `000a2014` | CG2D_LOADER::GetSavePixelFormatData(unsigned int, int, int*) | 276 | unknown |
| `000a2864` | CG2D_LOADER::GetImageFormatType(unsigned int, int, char*) | 276 | unknown |
| `000a2a90` | CG2D_LOADER::GetImageExtExt(int, char*) | 276 | unknown |
| `000a3f64` | CG2D_LOADER_BMP::BMP_DecodeRLE8(unsigned char*, unsigned char*, int, int) | 276 | unknown |
| `000b5e38` | CUI_SCROLLBAR::FrameMove(float) | 276 | unknown |
| `000cbc3c` | TrapWindowTaskManager(int, int, short, int) | 276 | unknown |
| `00101fe4` | Wevent_init_memory() | 276 | unknown |
| `00176f64` | bGetJobList(unsigned char, short*, int) | 276 | unknown |
| `001aec8c` | DrawEquipCategory(int, int, int) | 276 | unknown |
| `00244418` | vEnd_rollline_put(unsigned long*, int) | 276 | unknown |
| `0025cc10` | wldscr_init() | 276 | unknown |
| `0025d81c` | wldpad_read() | 276 | unknown |
| `0026b904` | wldsymbol_init() | 276 | unknown |
| `00291178` | MoveImage2 | 276 | unknown |
| `0029a2d8` | DrawOTag | 276 | unknown |
| `002b7378` | RENDER_TO_SCREEN(int, int, int*, int*) | 276 | unknown |
| `000a2978` | CG2D_LOADER::GetImageFormatExt(unsigned int, char*) | 272 | unknown |
| `000b5c34` | CUI_SCROLLBAR::DragBegin(int, int) | 272 | unknown |
| `000d9638` | fade_eventlocal(ITEMPRIM*, int) | 272 | unknown |
| `000f38c4` | disp_plateorspell(ACT*, int, int) | 272 | unknown |
| `00155b4c` | worldmap_menuinit() | 272 | unknown |
| `00159c40` | iosAsmMUL64(long, long, long) | 272 | unknown |
| `0015c04c` | iOSMapCurModeSet(int) | 272 | unknown |
| `0015d748` | iOSCurSameOK() | 272 | unknown |
| `001d2b00` | search_controlID(int, int*) | 272 | unknown |
| `001dc944` | set_casting_status(BWORK*, unsigned char) | 272 | unknown |
| `001e21f8` | getskillresult_first(int) | 272 | unknown |
| `001eb360` | defrost(char*, char*) | 272 | unknown |
| `0021fc38` | p03_golemFunc() | 272 | unknown |
| `0021fe64` | p08_landingFunc() | 272 | unknown |
| `00220328` | p19_telepoFunc() | 272 | unknown |
| `00220438` | p21_breakFunc() | 272 | unknown |
| `0022588c` | NewObject(short, short) | 272 | unknown |
| `00252b70` | ctlworkendmes_init(int) | 272 | unknown |
| `002b7268` | SCREEN_TO_RENDER(int, int, int*, int*) | 272 | unknown |
| `002c8ac4` | IS_SETTINGS_WND_SLIDER_AREA(int, int) | 272 | unknown |
| `000793e0` | inflateBackInit_ | 268 | unknown |
| `00082de4` | oggpackB_read | 268 | unknown |
| `000a7d1c` | CEGL2_IF::CEGL2_IF() | 268 | unknown |
| `00101450` | Wfade_eventlocal(ITEMPRIM*, int) | 268 | unknown |
| `0010d738` | Wdisp_plateorspell(ACT*, int, int) | 268 | unknown |
| `00159d50` | iosAsmMUL3232(long, long, long, long) | 268 | unknown |
| `0015cf60` | iOSRotSlideAreaOut() | 268 | unknown |
| `0015fce0` | iOSJobChanegAngleReset(short, short*) | 268 | unknown |
| `001d93a4` | add_jobpoint(int, int) | 268 | unknown |
| `00200cdc` | startZoomChange(int) | 268 | unknown |
| `0022a820` | GetAnimationPosition(int, int, EffectOrder*, SVECTOR*) | 268 | unknown |
| `00249ac0` | vOpn_padread() | 268 | unknown |
| `002557ac` | ctlhelp_main(CTLINFO*) | 268 | unknown |
| `00261078` | ctlhaken_init() | 268 | unknown |
| `0026c12c` | townbtl_check(int, int*) | 268 | unknown |
| `0027b67c` | iOS_CMenuTouch::calcTapArea() | 268 | unknown |
| `0027c160` | iOS_CMenuTouch::drawDebug() | 268 | unknown |
| `0028b738` | initTaskEmu() | 268 | unknown |
| `002b7050` | Main_Novel_GetBtnRect(int*, int*, int*, int*, int*, int*) | 268 | unknown |
| `002ca215` | __cxa_call_unexpected | 268 | unknown |
| `0007f138` | _tr_init | 264 | unknown |
| `0007fc50` | _tr_tally | 264 | unknown |
| `00088bf4` | _ve_envelope_mark | 264 | unknown |
| `000a9270` | CEGL2_IF::Setup2D() | 264 | unknown |
| `000ada14` | CEGL2_SPRITE::LoadBegin(char*, unsigned char*, unsigned int, unsigned int, int) | 264 | unknown |
| `000ba3a4` | CSOUND_IF::Init(unsigned int, int, char*, int) | 264 | unknown |
| `0015a064` | iosAsmKanjiCopy(char*, char*, tCOPYFIELD*, int) | 264 | unknown |
| `0015d06c` | iOSstartFukanChange() | 264 | unknown |
| `001ada4c` | FadeIn(int*) | 264 | unknown |
| `001c067c` | addlocalprim3(tagPOLY_FT4*, int) | 264 | unknown |
| `002404d8` | Mdl0026(short, int, int, int) | 264 | unknown |
| `00256388` | ctlsthelp_init() | 264 | unknown |
| `0025b8ec` | houkoku_mesput(CTLINFO*, int) | 264 | unknown |
| `000727f4` | Java_com_square_1enix_FFT_1Android_GL2JNILib_onTouchEvent | 260 | unknown |
| `00082ce0` | oggpack_read | 260 | unknown |
| `000bca88` | CSOUND_IF_SL::EngineUninit() | 260 | unknown |
| `001537dc` | eventflaginit() | 260 | unknown |
| `001608cc` | iOSSlideNaviCurMove() | 260 | unknown |
| `00176d04` | bGetChrList(short, CHR_STTS**, int) | 260 | unknown |
| `0018eafc` | eGetWindowPosition(int, short*, short*, short*) | 260 | unknown |
| `0019d530` | FighterName() | 260 | unknown |
| `001bad9c` | SeExec() | 260 | unknown |
| `001d9250` | get_job_change_flag(unsigned char*, unsigned char) | 260 | unknown |
| `0020e590` | setAnimationPosition(int, SVECTOR*, int) | 260 | unknown |
| `00210004` | requestReadEntryData() | 260 | unknown |
| `00249174` | vOpn_parainit() | 260 | unknown |
| `00255654` | ctlhelp_init(int, int) | 260 | unknown |
| `00259ad4` | ctlhismes_main(CTLINFO*) | 260 | unknown |
| `00266df8` | wldtname_put(GsOT*) | 260 | unknown |
| `0026a2cc` | snpl_scrdisp() | 260 | unknown |
| `00280004` | cSaveFFT::Load() | 260 | unknown |
| `00282374` | DispClipedPolygonNo(int, int, int) | 260 | unknown |
| `00286f18` | pspNetInitRivalData() | 260 | unknown |
| `0007b080` | inflateInit2_ | 256 | unknown |
| `0008bfe4` | vorbis_comment_query | 256 | unknown |
| `000b1980` | CEGL_PACKET::Alloc(int) | 256 | unknown |
| `00123f78` | Wstatusfigprint0(int, int, char*, COPYFIELD*) | 256 | unknown |
| `00137424` | statusfigprint0(int, int, char*, COPYFIELD*) | 256 | unknown |
| `00172560` | cSwapDB(int, int) | 256 | unknown |
| `0017b494` | bGetMaskedPad() | 256 | unknown |
| `00189c6c` | eDrawLineF2(RECT16*, COLOR*, char, int) | 256 | unknown |
| `001ac674` | DrawLineF2(RECT16*, COLOR*, char, int) | 256 | unknown |
| `001c0464` | GetWindowPosition(int, short*, short*, short*) | 256 | unknown |
| `001cc9fc` | status_countdown(int) | 256 | unknown |
| `001eaf0c` | searchAnotherAnimationByPosition(tag_animation*, int, int, int) | 256 | unknown |
| `001f5320` | displayCursor() | 256 | unknown |
| `001fd2ec` | requestHitMark(tag_animation*, int) | 256 | unknown |
| `0020ccbc` | fileReadCDWithErrorCheck(unsigned long, unsigned long, void*) | 256 | unknown |
| `00210c9c` | setMapVector(SVECTOR*, SVECTOR*) | 256 | unknown |
| `00225210` | DoPermanentEffect() | 256 | unknown |
| `0024988c` | vOpn_sun2ivaday(int*, int*) | 256 | unknown |
| `0024cf68` | ctlbrst_deactive(CTLINFO*) | 256 | unknown |
| `00255180` | ctlmap_active(CTLINFO*) | 256 | unknown |
| `00256ff4` | wld_shop(int) | 256 | unknown |
| `00266900` | infonumber_put(int, int, GsSPRITE*, GsOT*) | 256 | unknown |
| `0027de0c` | iOS_CMenuTouchNum::exec(int*) | 256 | unknown |
| `000a341c` | CG2D_LOADER_BMP::BMP_AnalyzeFileHeader(void*) | 252 | unknown |
| `000a8440` | CEGL2_IF::CreateTexture(int, int, void*, bool) | 252 | unknown |
| `000e0fb8` | initdrmode(DR_MODE*, int) | 252 | unknown |
| `001773e0` | bDrawTile(RECT16*, COLOR*, char, int) | 252 | unknown |
| `00181c9c` | bWindowInit(short*, int, unsigned char*) | 252 | unknown |
| `001895e8` | eIsAbleEquip(short, short) | 252 | unknown |
| `00189b70` | eDrawTile(RECT16*, COLOR*, char, int) | 252 | unknown |
| `001ac2c8` | DrawTile(RECT16*, COLOR*, char, int) | 252 | unknown |
| `001bc334` | GetSttsApos(short) | 252 | unknown |
| `001c5094` | WindowInit(short*, int, unsigned char*) | 252 | unknown |
| `001f5df8` | MydisplayCursor(int) | 252 | unknown |
| `0020c834` | mallocAddress(void*, unsigned int) | 252 | unknown |
| `00225790` | InitObjectManager() | 252 | unknown |
| `0026a6d4` | fastpage_print(int, int) | 252 | unknown |
| `002b1ff8` | Debug_DrawFPS() | 252 | unknown |
| `0009e624` | ov_clear | 248 | unknown |
| `000a1f1c` | CG2D_LOADER::GetSavePixelFormatInfo(unsigned int, _G2D_SAVE_INFO*) | 248 | unknown |
| `000b44a4` | CINPUT_IF_TOUCH::OnTouchesEnded(int, int, int, int, int) | 248 | unknown |
| `000b8060` | CFILE_UTIL::FileEnum_Add(CLIST*, char*, unsigned int) | 248 | unknown |
| `000ba138` | CompareLocalTime(_SYSTEMTIME*, _SYSTEMTIME*) | 248 | unknown |
| `0010fa1c` | Winitdrmode(DR_MODE*, int) | 248 | unknown |
| `00161a18` | iOSUnitListUDCur(unsigned char*, unsigned short*) | 248 | unknown |
| `0018716c` | CardAccess3() | 248 | unknown |
| `00188348` | allitem_count() | 248 | unknown |
| `001abe0c` | GetShapeNo(CHR_STTS*, int) | 248 | unknown |
| `001caa10` | set_ct_weapon(ACT*) | 248 | unknown |
| `001f5c08` | requestSpecialStatus(tag_animation*) | 248 | unknown |
| `001f5d00` | DrawPanel(int, int, int, int) | 248 | unknown |
| `0021b920` | Dynamics(Physics*) | 248 | unknown |
| `00224d4c` | CheckGunReachable(unsigned char, unsigned char) | 248 | unknown |
| `0022541c` | Free(void*) | 248 | unknown |
| `00253a68` | ctlcenter_main(CTLINFO*) | 248 | unknown |
| `00262a20` | hakenunit_status(int) | 248 | unknown |
| `0027ce58` | iOS_CMenuTouch::init(int, int, int, int, int, int, int, int) | 248 | unknown |
| `002b1508` | AppEngine_Bootup() | 248 | unknown |
| `00080958` | unzGetCurrentFileInfo | 244 | unknown |
| `00085904` | vorbis_analysis_buffer | 244 | unknown |
| `000ac44c` | std::priv::_Rb_tree<int, std::less<int>, std::pair<int const, CEGL2_SHADER::DATA_SHADER>, std::priv::_Select1st<std::pair<int const, CEGL2_SHADER::DATA_SHADER> >, std::priv::_MapTraitsT<std::pair<int const, CEGL2_SHADER::DATA_SHADER> >, std::allocator<std::pair<int const, CEGL2_SHADER::DATA_SHADER> > >::insert_unique(std::pair<int const, CEGL2_SHADER::DATA_SHADER> const&) | 244 | unknown |
| `000afa3c` | CCAMERA::SetProjOrtho(float, float, float, float) | 244 | unknown |
| `000bd9e4` | CFRAMERATE::FrameMove() | 244 | unknown |
| `001728e0` | cDrawTile(RECT16*, COLOR*, char, int) | 244 | unknown |
| `00178874` | bFadeOut(int*) | 244 | unknown |
| `00188b78` | eChrPower(C_STTS*, short*) | 244 | unknown |
| `001a2a50` | initMenuTouch(iOS_CMenuTouch*, int) | 244 | unknown |
| `001a9064` | ChrPower(C_STTS*, short*) | 244 | unknown |
| `001ab2c0` | ItemEquip(short, short, short) | 244 | unknown |
| `001ab824` | AbilityEquip(short, short, short, int) | 244 | unknown |
| `001adb54` | FadeOut() | 244 | unknown |
| `001b799c` | SystemWarningTime(int, int) | 244 | unknown |
| `001d2874` | set_succession_data(BWORK*, int) | 244 | unknown |
| `001eb7d4` | setPanelPriorityMoveSub(SVECTOR*, SVECTOR*, int) | 244 | unknown |
| `002405e0` | Mdl0027(short, int, int, int) | 244 | unknown |
| `00245720` | strCallback() | 244 | unknown |
| `0024bf7c` | wldpnl_calc() | 244 | unknown |
| `0025c744` | shogou_check() | 244 | unknown |
| `00286cf8` | pspNetEntranceMissionStateExec(CTLINFO*) | 244 | unknown |
| `00076e08` | deflateEnd | 240 | unknown |
| `000b3c24` | CINPUT_IF_TOUCH::Init() | 240 | unknown |
| `000dd360` | eventanmreq(char*) | 240 | unknown |
| `00100844` | Wcheckkeyok() | 240 | unknown |
| `001069ac` | Weventanmreq(char*) | 240 | unknown |
| `001a9d14` | IsAbleEquip(short, short) | 240 | unknown |
| `001b6b10` | MakeTextureMessage(unsigned char*, short*, RECT16*, int) | 240 | unknown |
| `001bc430` | UnitScroll(short*, short*) | 240 | unknown |
| `001bdb1c` | DrawShapeWithShadow(short*, COLOR*, int, int) | 240 | unknown |
| `0020d2e0` | requestMapScroll(VECTOR*, unsigned short) | 240 | unknown |
| `00211b98` | ExecuteChangePalette() | 240 | unknown |
| `00250894` | ctlwork_deactive(CTLINFO*) | 240 | unknown |
| `0025c3ac` | mkdaypt_calc() | 240 | unknown |
| `0025c838` | ctlshogou_init() | 240 | unknown |
| `00266b94` | info_war_funds(GsOT*, GsSPRITE*, GsLINE*) | 240 | unknown |
| `0026bf68` | town_touch(_POINT, int*, int*) | 240 | unknown |
| `0027df0c` | iOS_CMenuTouchSaveLoad::calcTapArea() | 240 | unknown |
| `002b133c` | SettingsBundle_Save() | 240 | unknown |
| `000b3e28` | CINPUT_IF_TOUCH::ClearAll() | 236 | unknown |
| `000b4f94` | CRECT::FrameMove(int, int) | 236 | unknown |
| `000ef4f4` | hook_jobmenu() | 236 | unknown |
| `00101650` | Whook_jobmenu() | 236 | unknown |
| `00155e40` | request_worldwindow(int, int, int, int) | 236 | unknown |
| `0015ce74` | iOSMapIconModeSet(int) | 236 | unknown |
| `00178788` | bFadeIn(int*) | 236 | unknown |
| `00191c08` | eWindowInit(short*, int, unsigned char*) | 236 | unknown |
| `001ead44` | searchAnimationByPositionOther(int, int, int) | 236 | unknown |
| `001f35dc` | EndAnimation(tag_animation*) | 236 | unknown |
| `00247dc8` | ctlbirthokng_init() | 236 | unknown |
| `002590e8` | wld_event(int, int) | 236 | unknown |
| `0025b78c` | houkoku_talkunit(int) | 236 | unknown |
| `0026be7c` | town_find3(_POINT, int) | 236 | unknown |
| `00284df4` | pspBattleForceParticipationExit() | 236 | unknown |
| `002a3154` | pspSaveAuto::paramCreate() | 236 | unknown |
| `00077598` | gz_error | 232 | unknown |
| `0009cec4` | vorbis_synthesis_trackonly | 232 | unknown |
| `000a9048` | CEGL2_IF::CLUT_Load(int, unsigned int*, int) | 232 | unknown |
| `000ba8e0` | CSOUND_IF::SetVolume(int, int) | 232 | unknown |
| `000be2b4` | CSTEP_BATCH::FrameMove(float) | 232 | unknown |
| `000dc604` | eventsetchrcol(char*) | 232 | unknown |
| `00163260` | ASHURA_BackColor(long, long, long, long) | 232 | unknown |
| `0017861c` | bDrawMove(RECT16*, int, int, long) | 232 | unknown |
| `0018a87c` | eDrawMove(RECT16*, int, int, long) | 232 | unknown |
| `001946ec` | jDrawMove(RECT16*, int, int, long) | 232 | unknown |
| `00198474` | jWindowInit(short*, int, unsigned char*) | 232 | unknown |
| `001ad54c` | DrawMove(RECT16*, int, int, long) | 232 | unknown |
| `001bb62c` | CurChrChg() | 232 | unknown |
| `001ceb14` | reset_status_forevent2(BWORK*) | 232 | unknown |
| `001f36fc` | executeTerminateAnimation(tag_animation*) | 232 | unknown |
| `00202068` | pspNetDecisionOccurmagic(BWORK*) | 232 | unknown |
| `0020d3d0` | requestMapScrollRelative(VECTOR*, unsigned short) | 232 | unknown |
| `00285aac` | pspItemIsOnion | 232 | unknown |
| `00285e50` | pspMsgGet(unsigned int) | 232 | unknown |
| `00078f2c` | gzputc | 228 | unknown |
| `00079224` | gzsetparams | 228 | unknown |
| `000d90e0` | multiwindow_packetextend(COMRECORD*, tagSPRT*, int) | 228 | unknown |
| `00100ef8` | Wmultiwindow_packetextend(COMRECORD*, tagSPRT*, int) | 228 | unknown |
| `00188a94` | eChrPowerCompare(C_STTS*, A_STTS*, short*, short*) | 228 | unknown |
| `001a8f80` | ChrPowerCompare(C_STTS*, A_STTS*, short*, short*) | 228 | unknown |
| `001c07a0` | iOS_SetStatusWindowSTTSHit() | 228 | unknown |
| `001eb67c` | myInitShape() | 228 | unknown |
| `0020f1d0` | getCharacterInfo(int, unsigned short*) | 228 | unknown |
| `00223310` | GetParabolaYPos(int, int) | 228 | unknown |
| `0026fe48` | ctluwames_main(CTLINFO*) | 228 | unknown |
| `0028d6ec` | tlCheckHeap() | 228 | unknown |
| `00072ee4` | Android_Web_Open(char const*, int) | 224 | unknown |
| `00072fc4` | Android_Movie_Play(char const*, int) | 224 | unknown |
| `000813b4` | unzGoToNextFile | 224 | unknown |
| `000834f4` | ogg_page_checksum_set | 224 | unknown |
| `000a0294` | ov_time_total | 224 | unknown |
| `000acd50` | CEGL2_SPRITE::Overwrite(unsigned char*, int, int, int, int) | 224 | unknown |
| `000b907c` | CSTR_UTIL::GetPrevPath(char*, char*) | 224 | unknown |
| `000cbb48` | delTrapWindowTaskall() | 224 | unknown |
| `000d115c` | Ddisp_eventwaitwindow() | 224 | unknown |
| `00123994` | Edisp_eventwaitwindow() | 224 | unknown |
| `001252d0` | Wdisp_eventwindow() | 224 | unknown |
| `0012cb3c` | disp_eventwaitwindow() | 224 | unknown |
| `00134fa0` | Wdisp_eventwaitwindow() | 224 | unknown |
| `00138234` | disp_eventwindow() | 224 | unknown |
| `0014bd8c` | Cdisp_eventwaitwindow() | 224 | unknown |
| `0015588c` | title_menuinit() | 224 | unknown |
| `0015a33c` | iOSsTchBtlEnd() | 224 | unknown |
| `0017349c` | cFadeOut() | 224 | unknown |
| `00189a74` | eItemEquip(short, short, short) | 224 | unknown |
| `001cea0c` | set_walker_result(BWORK*, REWARD*) | 224 | unknown |
| `001dc29c` | set_eggmonster(int, int, int) | 224 | unknown |
| `0020f970` | iOS_RESUME_SET_GLBLWORK(IOS_RESUME_DATA_GLBLWORK*, IOS_RESUME_DATACOPY_MODE) | 224 | unknown |
| `002541c4` | ctlcenter_init(int) | 224 | unknown |
| `00264378` | ctlnblwldinfo_init() | 224 | unknown |
| `00265fd8` | wldpac_init() | 224 | unknown |
| `0029dc34` | _gte_rt() | 224 | unknown |
| `000b99f4` | CSTR_UTIL::ToLineFeed(char*, char*, int) | 220 | unknown |
| `000e7f10` | iOS_Resume_BGM() | 220 | unknown |
| `001733c0` | cFadeIn() | 220 | unknown |
| `00187514` | TimeConvert(int) | 220 | unknown |
| `00188470` | eGetChrSingle(int) | 220 | unknown |
| `001b6d84` | MakeTextureChar(unsigned short, int, int, int) | 220 | unknown |
| `001b9258` | iOSTutoBtlSkipSet() | 220 | unknown |
| `001d588c` | set_event_table_skill(BWORK*, ACT*, TURN_TABLE*) | 220 | unknown |
| `001eae30` | searchAnimationByPositionChokobo(int, int, int) | 220 | unknown |
| `00218640` | AnimatePermanentObject(int) | 220 | unknown |
| `0021d544` | getNextSENo(int) | 220 | unknown |
| `0025d930` | speed_calc(SPDINFO*, int) | 220 | unknown |
| `00268f58` | wldmap_scrol(_POINT*) | 220 | unknown |
| `0026bda0` | town_find(_POINT) | 220 | unknown |
| `0027b3a4` | numaSaveDataLoad(unsigned char*) | 220 | unknown |
| `002ab620` | GuEmu_ClearTexCache() | 220 | unknown |
| `002b2ea0` | Jingle_FrameMove() | 220 | unknown |
| `002b54b4` | Link_Uninit() | 220 | unknown |
| `002ca79c` | __divsi3 | 220 | unknown |
| `00079308` | gzclose_w | 216 | unknown |
| `00094bfc` | _vp_psy_clear | 216 | unknown |
| `00097970` | res2_forward | 216 | unknown |
| `000a129c` | ov_read_float | 216 | unknown |
| `000b7400` | CFILE_TXT::CutSpace(char*, int) | 216 | unknown |
| `000bc5a4` | CSOUND_IF_SL::Stream_Load(int) | 216 | unknown |
| `000cb9e0` | readmaptitle() | 216 | unknown |
| `000d8ddc` | multiwindow_break(unsigned long*) | 216 | unknown |
| `000fef24` | Wdisposewindow(MESSAGEPACKET*) | 216 | unknown |
| `00201b84` | resetActionDirection(tag_animation*) | 216 | unknown |
| `00218cf4` | SetDefaultCamera() | 216 | unknown |
| `002867a8` | getMovieEventNum(int) | 216 | unknown |
| `0029e588` | _gte_rtv0bk() | 216 | unknown |
| `0029e664` | _gte_rtv1bk() | 216 | unknown |
| `0029e740` | _gte_rtv2bk() | 216 | unknown |
| `0029e81c` | _gte_rtirbk() | 216 | unknown |
| `00083160` | ogg_page_granulepos | 212 | unknown |
| `000aee64` | CEGL2_TEX_HYBRID::UV_Regist(_RECT_S32*) | 212 | unknown |
| `000b4888` | CINPUT_IF_TOUCH::GetGestureSwipe(int, int, int, unsigned int) | 212 | unknown |
| `000b8d34` | CSTR_UTIL::GetName(char*, char*, int) | 212 | unknown |
| `000d7388` | disposewindow(MESSAGEPACKET*) | 212 | unknown |
| `001c02d4` | JobToAbiChg() | 212 | unknown |
| `001e2124` | afterskillhandle(BWORK*) | 212 | unknown |
| `001fea38` | rideOnChokobo(tag_animation*, tag_animation*) | 212 | unknown |
| `00216530` | activateMusic(int, int, int) | 212 | unknown |
| `00248a40` | ctlopenhelp_init(int, int) | 212 | unknown |
| `00249f94` | vOpn_pacinit() | 212 | unknown |
| `0024b6bc` | ctlbar_active(CTLINFO*) | 212 | unknown |
| `002531e4` | ctltuto_zodiac() | 212 | unknown |
| `0025e434` | mouke_app_chk(int, int) | 212 | unknown |
| `0025efe4` | wlddata_load() | 212 | unknown |
| `0025f280` | snpl_load(int) | 212 | unknown |
| `0026ba18` | wldtown_draw() | 212 | unknown |
| `0027afdc` | IsNeedlessToFear(int) | 212 | unknown |
| `00286b3c` | pspNetEntranceInit(ENTRANCE_MODE) | 212 | unknown |
| `0029c518` | GsSortLine | 212 | unknown |
| `002bb70c` | iOSTutoMenuCtrl(int*) | 212 | unknown |
| `00082b14` | oggpackB_look | 208 | unknown |
| `00083d28` | ogg_sync_buffer | 208 | unknown |
| `000b6fac` | CFILE_TXT::GetDataAsStr(int, int, unsigned int) | 208 | unknown |
| `000b96a8` | CSTR_UTIL::FindDBCS(char*, char*) | 208 | unknown |
| `000bb5fc` | CSOUND_IF_SL::CB_for_Stream(SLAndroidSimpleBufferQueueItf_ const* const*, void*) | 208 | unknown |
| `000da064` | request_backtotitle() | 208 | unknown |
| `000da134` | request_resumebacktotitle() | 208 | unknown |
| `00101d20` | Wrequest_backtotitle() | 208 | unknown |
| `00101df0` | Wrequest_resumebacktotitle() | 208 | unknown |
| `0015a65c` | siOS_TCurSucCheck(unsigned int) | 208 | unknown |
| `0017854c` | bDrawArea(RECT16*, long) | 208 | unknown |
| `0018a964` | eDrawArea(RECT16*, long) | 208 | unknown |
| `001947d4` | jDrawArea(RECT16*, long) | 208 | unknown |
| `001a9158` | IsItem(int) | 208 | unknown |
| `001ad834` | DrawArea(RECT16*, long) | 208 | unknown |
| `001bab78` | GetIwaPadData() | 208 | unknown |
| `00215adc` | initChangeClut() | 208 | unknown |
| `0021d2e0` | CreateEffectTask(char*, short, short) | 208 | unknown |
| `00255584` | ctlhelp2_main(CTLINFO*) | 208 | unknown |
| `0025d26c` | wlddraw_init() | 208 | unknown |
| `0026c05c` | townmenu_check(int, int*) | 208 | unknown |
| `0027b2c0` | iOS_setDisableMapClip(int) | 208 | unknown |
| `0027bbfc` | iOS_CMenuTouch::isInAssist(int, int, int) | 208 | unknown |
| `00290cf0` | ResetGraph | 208 | unknown |
| `002a1600` | ColorMatDpq | 208 | unknown |
| `002a2060` | RotAverage4 | 208 | unknown |
| `002b2644` | EnvSE_Stop(int) | 208 | unknown |
| `000755e0` | deflateResetKeep | 204 | unknown |
| `00082a48` | oggpack_look | 204 | unknown |
| `000a01c8` | ov_halfrate | 204 | unknown |
| `000a5d90` | CG2D_LOADER_TGA::Load(char*, unsigned char*, unsigned int, unsigned int) | 204 | unknown |
| `000a6c90` | CG2D_LOADER_TIM::Load(char*, unsigned char*, unsigned int, unsigned int) | 204 | unknown |
| `000a71f0` | CGX_SCREEN_CORRECT::Area_InitLandscape(int, int, int, int, int, int) | 204 | unknown |
| `000b78b4` | CFILE_UTIL::DirCreate(char*) | 204 | unknown |
| `000bdc6c` | CSTEP::FrameMove(float, unsigned int) | 204 | unknown |
| `000dbba4` | eventsetstatus(int, int, int, int) | 204 | unknown |
| `00103ff4` | Weventsetstatus(int, int, int, int) | 204 | unknown |
| `0014bedc` | joinfaceuvclut(tagPOLY_FT4*, int, int*) | 204 | unknown |
| `00155f88` | multiwindow_addinit(COMRECORD*, tagSPRT*, int) | 204 | unknown |
| `001699d8` | ASHURA_GNS_Analyzer(unsigned long, unsigned long) | 204 | unknown |
| `00178480` | bDrawModeChg(int, int, int, RECT16*, int) | 204 | unknown |
| `0018aa34` | eDrawModeChg(int, int, int, RECT16*, int) | 204 | unknown |
| `001ad904` | DrawModeChg(int, int, int, RECT16*, int) | 204 | unknown |
| `00200a1c` | startKnockBack(tag_animation*, tag_animation*) | 204 | unknown |
| `00228c74` | InitShape() | 204 | unknown |
| `0023da54` | Mdl0018(short, int, int, int) | 204 | unknown |
| `0023db20` | Mdl0019(short, int, int, int) | 204 | unknown |
| `00255e14` | ctlfsetnum_init(int, int) | 204 | unknown |
| `00270224` | wldpicwin_set(int, RECT16, _POINT, int) | 204 | unknown |
| `00273f4c` | SetBMList() | 204 | unknown |
| `0027af10` | GetCountToNextTurn(BWORK*) | 204 | unknown |
| `0028a6a0` | pspTitleSaveCheck() | 204 | unknown |
| `0029c5ec` | GsSortClear | 204 | unknown |
| `0029df24` | _gte_rtv0() | 204 | unknown |
| `0029dff4` | _gte_rtv1() | 204 | unknown |
| `0029e0c4` | _gte_rtv2() | 204 | unknown |
| `0029e248` | _gte_rtv0tr() | 204 | unknown |
| `0029e318` | _gte_rtv1tr() | 204 | unknown |
| `0029e3e8` | _gte_rtv2tr() | 204 | unknown |
| `0029e4b8` | _gte_rtirtr() | 204 | unknown |
| `0029e8f8` | _gte_llv0() | 204 | unknown |
| `0029ea14` | _gte_llv1() | 204 | unknown |
| `0029eae4` | _gte_llv2() | 204 | unknown |
| `0029ebb4` | _gte_llir() | 204 | unknown |
| `0029eee4` | _gte_lcv0() | 204 | unknown |
| `0029efb4` | _gte_lcv1() | 204 | unknown |
| `0029f084` | _gte_lcv2() | 204 | unknown |
| `0029f154` | _gte_lcir() | 204 | unknown |
| `002a103c` | TransRot_32 | 204 | unknown |
| `00081af0` | unzGetLocalExtrafield | 200 | unknown |
| `00084560` | vorbis_analysis | 200 | unknown |
| `0008c0e4` | vorbis_comment_query_count | 200 | unknown |
| `000b1c14` | CEGL_PACKET::AddTexFilter(int) | 200 | unknown |
| `000b992c` | CSTR_UTIL::Divide(char*, char, CLIST*) | 200 | unknown |
| `000d8fe0` | get_cursoroffset(int) | 200 | unknown |
| `00100df8` | Wget_cursoroffset(int) | 200 | unknown |
| `0015a7d8` | iOSScrollButtonMove() | 200 | unknown |
| `001745a0` | cWriteBitStream(unsigned char) | 200 | unknown |
| `0017b314` | bMenuSelSide(unsigned short, unsigned char, unsigned long) | 200 | unknown |
| `0017b5b0` | bGetBitStream(unsigned int) | 200 | unknown |
| `0018e26c` | eCurChrChg() | 200 | unknown |
| `0018fb04` | eMenuSelSide(unsigned short, unsigned char, unsigned long) | 200 | unknown |
| `001b88a4` | WriteBitStream(unsigned char) | 200 | unknown |
| `001bac98` | iOSWldEffectLR(int) | 200 | unknown |
| `0020d4b8` | executeMapScroll() | 200 | unknown |
| `0024232c` | vOpn_arzpic_main() | 200 | unknown |
| `0024a5c0` | vOpn_winopen_frmcalc(int, RECT16*, RECT16*) | 200 | unknown |
| `00257a2c` | ctlparty_init() | 200 | unknown |
| `002623e4` | mouketeam_unitwin(CTLINFO*) | 200 | unknown |
| `002666d4` | winopen_frmcalc(int, RECT16*, RECT16*) | 200 | unknown |
| `0029b42c` | GsInitGraph2 | 200 | unknown |
| `0029c6b8` | GsGetTimInfo | 200 | unknown |
| `002a16d0` | ColorMatCol | 200 | unknown |
| `002b1e70` | NowLoading_FrameMove() | 200 | unknown |
| `000ad938` | CEGL2_SPRITE::Unload(int) | 196 | unknown |
| `000da720` | tutorial_hookfunc() | 196 | unknown |
| `000e2a40` | iOS_valueput_FT4(tagPOLY_FT4*, VALUERECORD*, COPYFIELD*, int, void*, int, int, int) | 196 | unknown |
| `001114b0` | WiOS_valueput_FT4(tagPOLY_FT4*, VALUERECORD*, COPYFIELD*, int, void*, int, int, int) | 196 | unknown |
| `001383a4` | maptest() | 196 | unknown |
| `0015ea80` | iOSBtlStsButtonCheck() | 196 | unknown |
| `0015fdec` | iOSJobChgRotAct() | 196 | unknown |
| `00161b10` | iOSUnitListLRCur(unsigned char*, unsigned short*) | 196 | unknown |
| `00180140` | bGetWindowPosition(int, short*, short*, short*) | 196 | unknown |
| `001a8508` | GetCommandList(short, short*) | 196 | unknown |
| `00200f44` | startFukanChange() | 196 | unknown |
| `0020d088` | requestMapScrollXYZ(VECTOR*, unsigned short) | 196 | unknown |
| `0021025c` | InitializePartyItem() | 196 | unknown |
| `00211e50` | setPresentClutDataAsDefault(unsigned int, unsigned int, int) | 196 | unknown |
| `0022599c` | DisposeObject(short, _Object*) | 196 | unknown |
| `00242268` | vOpn_arzpic_init(int) | 196 | unknown |
| `002507d0` | ctlwork_active(CTLINFO*) | 196 | unknown |
| `00254ed8` | ctlrutegrow_init(int, int, int) | 196 | unknown |
| `0025e508` | person_year_up() | 196 | unknown |
| `0026ffc8` | wldwin_set(int, RECT16, int, unsigned long*) | 196 | unknown |
| `00279b70` | CheckAbilityGet(int, int, int) | 196 | unknown |
| `0028dae4` | tlMoveHeap(long long, int) | 196 | unknown |
| `002a0bc4` | ScaleMatrixL | 196 | unknown |
| `002b19ec` | AppEngine_Uninit() | 196 | unknown |
| `002b77e8` | RayPick_GT3_input(tagPOLY_GT3*, int, int, int, int) | 196 | unknown |
| `002cd0c4` | __gnu_Unwind_Backtrace | 196 | unknown |
| `0007fd58` | uncompress | 192 | unknown |
| `001964e4` | jHelpMessage(int) | 192 | unknown |
| `00196de0` | jMenuSelSide(unsigned short, unsigned char, unsigned long) | 192 | unknown |
| `001d9f58` | get_setstatus_max(A_RESULT*) | 192 | unknown |
| `0020c774` | mallocForFile(unsigned int) | 192 | unknown |
| `0020d600` | requestMapScale(VECTOR*, unsigned short) | 192 | unknown |
| `0020d874` | requestMapAngle(SVECTOR*, unsigned short) | 192 | unknown |
| `0020f350` | callEventEffect(int, int, void*) | 192 | unknown |
| `00245d24` | ctlopenmov_main(CTLINFO*) | 192 | unknown |
| `0024a924` | vOpnwin_set(int, RECT16, int, unsigned long*) | 192 | unknown |
| `00269870` | snpl_syscur() | 192 | unknown |
| `002a0b04` | ScaleMatrix | 192 | unknown |
| `002a37b0` | pspSaveBase::pspSaveBase() | 192 | unknown |
| `000d8978` | itemuvclut(tagSPRT*, int) | 188 | unknown |
| `000dfa94` | makemessagestructure() | 188 | unknown |
| `000ff61c` | Wdisposememory(char*) | 188 | unknown |
| `00100648` | Witemuvclut(tagSPRT*, int) | 188 | unknown |
| `0015a8cc` | iOSRotStop() | 188 | unknown |
| `00174668` | cGetBitStream2(unsigned int) | 188 | unknown |
| `0018feec` | eGetBitStream2(unsigned int) | 188 | unknown |
| `00196fac` | jGetBitStream2(unsigned int) | 188 | unknown |
| `001b896c` | GetBitStream2(unsigned int) | 188 | unknown |
| `001ce950` | setskillresult_caster(int) | 188 | unknown |
| `0020c19c` | fftVSyncCallback() | 188 | unknown |
| `0020c628` | mallocForSound(unsigned int) | 188 | unknown |
| `0020f43c` | debugEffectWait() | 188 | unknown |
| `0025e6f8` | wld_dayread(unsigned long*, int, FINDDAY*) | 188 | unknown |
| `00261b0c` | mouke_eventday_chg() | 188 | unknown |
| `0027f830` | iOS_ResumeBeforeBattle() | 188 | unknown |
| `002859cc` | pspItemGetItemData | 188 | unknown |
| `0028b638` | FFT_Main(void*) | 188 | unknown |
| `00291098` | StoreImage2 | 188 | unknown |
| `00291744` | SetDrawEnv | 188 | unknown |
| `002a0998` | ApplyMatrixLV | 188 | unknown |
| `002ab718` | sceGuEnable | 188 | unknown |
| `002b0f70` | CDebugPrint::AddText(int, int, int, char*, int) | 188 | unknown |
| `002bb58c` | iOS_getFingerAddPos(int, int) | 188 | unknown |
| `0009e98c` | ov_bitrate_instant | 184 | unknown |
| `000bb05c` | CSOUND_IF::FadeVolume(int, int, int, int) | 184 | unknown |
| `000bc4ec` | CSOUND_IF_SL::Stream_DeletePlayer(int) | 184 | unknown |
| `000bcd0c` | CSOUND_LOADER_PCM::Read(void*, unsigned long, unsigned long*) | 184 | unknown |
| `0015e51c` | iOSBtlUnitSearch(int, int) | 184 | unknown |
| `00160de8` | iOSYajiEffectSet(short, short, short, short, RECT16*) | 184 | unknown |
| `001744e8` | cGetBitStream(unsigned int) | 184 | unknown |
| `0018fe34` | eGetBitStream(unsigned int) | 184 | unknown |
| `00195eb4` | jGetWindowPosition(int, short*, short*, short*) | 184 | unknown |
| `00196ef4` | jGetBitStream(unsigned int) | 184 | unknown |
| `001b69bc` | MesEventSingleAddy(int, unsigned int, int, int, int) | 184 | unknown |
| `001b7af4` | MenuSelVertical(unsigned short, unsigned char, unsigned long) | 184 | unknown |
| `001b7c2c` | MenuSelSide(unsigned short, unsigned char, unsigned long) | 184 | unknown |
| `001b87ec` | GetBitStream(unsigned int) | 184 | unknown |
| `001cd490` | set_learning(BWORK*) | 184 | unknown |
| `0020e314` | moveToPanel(int, SVECTOR*, int, int, int) | 184 | unknown |
| `00254f9c` | ctltownset_init(int, int) | 184 | unknown |
| `0027efec` | iOS_CMenuTouchSaveLoad::init(int, int, int, int, int, int, int, int) | 184 | unknown |
| `0028d0f8` | tlInitHeap(void*, unsigned int) | 184 | unknown |
| `002a2288` | RotAverageNclipColorDpq3 | 184 | unknown |
| `000756ac` | deflateReset | 180 | unknown |
| `0009eab0` | ov_raw_total | 180 | unknown |
| `000b3f90` | CINPUT_IF_TOUCH::FrameEnd() | 180 | unknown |
| `0015a4dc` | iOSSlideNaviCurSet(unsigned long) | 180 | unknown |
| `001739b0` | cMesEventSingleAddy(int, unsigned int, int, int, int) | 180 | unknown |
| `00188eb4` | eGetItemCategory(short) | 180 | unknown |
| `001a959c` | GetItemCategory(short) | 180 | unknown |
| `001b71bc` | HelpMessage(int) | 180 | unknown |
| `001cc89c` | check_hide_reset(BWORK*) | 180 | unknown |
| `001d1150` | resist_monomane_data(BWORK*) | 180 | unknown |
| `001e736c` | iOS_RESUME_SET_UNIT_SD(IOS_RESUME_DATA_UNIT_SD*, IOS_RESUME_DATACOPY_MODE) | 180 | unknown |
| `001ed964` | getTapedDirection() | 180 | unknown |
| `001ee1c4` | drawItem(tag_animation*) | 180 | unknown |
| `001f00f4` | NewWeaponEquip(int, tag_animation*) | 180 | unknown |
| `002101a8` | loadPlayerPartyData(int) | 180 | unknown |
| `0021589c` | loadBackGradation() | 180 | unknown |
| `00215a28` | transferClutData() | 180 | unknown |
| `00216308` | readMusic(int) | 180 | unknown |
| `0021cf30` | InitEffect() | 180 | unknown |
| `00247c64` | ctlbirthday_active(CTLINFO*) | 180 | unknown |
| `00248c18` | ctlpremov_main(CTLINFO*) | 180 | unknown |
| `0024ab84` | vOpnpicwin_set(int, RECT16, _POINT, int) | 180 | unknown |
| `0027d488` | iOS_CMenuTouchNum::calcTapArea() | 180 | unknown |
| `002856fc` | pspItemGetWeaponData | 180 | unknown |
| `002857b0` | pspItemGetShieldData | 180 | unknown |
| `00285864` | pspItemGetArmorData | 180 | unknown |
| `00285918` | pspItemGetAccessoryData | 180 | unknown |
| `0028dd74` | TestEvent | 180 | unknown |
| `0029c954` | sceVfpuVector4OuterProductXYZ(ScePspFVector4*, ScePspFVector4 const*, ScePspFVector4 const*) | 180 | unknown |
| `002ab7d4` | sceGuDisable | 180 | unknown |
| `000730a4` | Android_Movie_IsPlaying() | 176 | unknown |
| `000731fc` | Android_Vibrator_IsExist() | 176 | unknown |
| `000bd284` | CSOUND_LOADER_OGG::Read(void*, unsigned long, unsigned long*) | 176 | unknown |
| `001568fc` | worldmap_restart() | 176 | unknown |
| `001abb9c` | GetJobShape(short, short, short*) | 176 | unknown |
| `001b6f14` | CountWidthMessage(unsigned char*) | 176 | unknown |
| `001d91a0` | init_entry_status(BWORK*) | 176 | unknown |
| `001e3988` | get_movetype(BWORK*) | 176 | unknown |
| `00201008` | iOSVectorNormal(VECTOR*) | 176 | unknown |
| `00211da0` | requestDestinationClutAsDefault(int, unsigned int, unsigned int, int, unsigned short*) | 176 | unknown |
| `00247d18` | ctlbirthday_deactive(CTLINFO*) | 176 | unknown |
| `00249cf4` | vOpn_timload(unsigned long*) | 176 | unknown |
| `0025e5cc` | wldday_countup() | 176 | unknown |
| `00268aec` | wldcenter_chk(_POINT*) | 176 | unknown |
| `002741bc` | SetMove() | 176 | unknown |
| `00285d6c` | pspJobGetTamanegiLevel(unsigned char (*) [3]) | 176 | unknown |
| `0029a92c` | LoadTPage | 176 | unknown |
| `000732c4` | Android_Font_SetStyle(int) | 172 | unknown |
| `000757e4` | deflatePrime | 172 | unknown |
| `0007ccf0` | inflateSetDictionary | 172 | unknown |
| `00082214` | unzGetGlobalComment | 172 | unknown |
| `000850a8` | _vorbis_block_ripcord | 172 | unknown |
| `0008bf38` | vorbis_comment_add_tag | 172 | unknown |
| `0008cb48` | vorbis_commentheader_out | 172 | unknown |
| `000af02c` | CEGL2_TEX_HYBRID::CEGL2_TEX_HYBRID() | 172 | unknown |
| `000af424` | CEGL2_TEX_HYBRID::AutoRelease() | 172 | unknown |
| `000b4654` | CINPUT_IF_TOUCH::CreateDevice(int, unsigned int, int) | 172 | unknown |
| `000b475c` | CINPUT_IF_TOUCH::GetGestureTap(int, int, int, unsigned int) | 172 | unknown |
| `000bbb6c` | CSOUND_IF_SL::SetSLDataFormat(int, int, SLDataFormat_PCM_*) | 172 | unknown |
| `000da4ac` | event_init_light() | 172 | unknown |
| `001049c4` | Weventsetchrcol(char*) | 172 | unknown |
| `0015e098` | iOSUnitNumberGet(int, int) | 172 | unknown |
| `00173d4c` | cDrawMessageFast(int, COMRECORD*) | 172 | unknown |
| `001b7110` | DrawMessageFast(int, COMRECORD*) | 172 | unknown |
| `001bb3b4` | SetSttsPara2(int) | 172 | unknown |
| `001bd320` | UnitTableInitFirst(short) | 172 | unknown |
| `001c0884` | iOS_SetStatusWindowLRCurHit() | 172 | unknown |
| `001cc950` | status_handle_main(BWORK*) | 172 | unknown |
| `001cce2c` | get_trap_result(BWORK*) | 172 | unknown |
| `001d7340` | net_change_bwork() | 172 | unknown |
| `001efbc0` | requestStanderdWalkAnimation(tag_animation*) | 172 | unknown |
| `00217f5c` | DisposeEffectAnimation(effectAnimation*) | 172 | unknown |
| `0021f0e4` | NewPEffectTCB() | 172 | unknown |
| `00225370` | Malloc(unsigned long, long) | 172 | unknown |
| `0024998c` | vOpn_iwaprog() | 172 | unknown |
| `00258e70` | evt_town_cent() | 172 | unknown |
| `0025903c` | evt_chr() | 172 | unknown |
| `002699bc` | snpl_putpara() | 172 | unknown |
| `0026aeec` | snpl_mreqcore(int) | 172 | unknown |
| `00273ea0` | SetBestMoveAnywhereOK() | 172 | unknown |
| `00290dc0` | DrawSync | 172 | unknown |
| `002919c0` | SetDrawMode | 172 | unknown |
| `0029f95c` | _gte_ncds() | 172 | unknown |
| `0029fb08` | _gte_cdp() | 172 | unknown |
| `002aca7c` | GuEmu_FrameMove() | 172 | unknown |
| `002b1f3c` | Offscreen_ReadPixels(int, int, int, int) | 172 | unknown |
| `00073154` | Android_Vibrator_Vibrate() | 168 | unknown |
| `00073a2c` | compress2 | 168 | unknown |
| `00097e9c` | _book_maptype1_quantvals | 168 | unknown |
| `000ab924` | CEGL2_SHADER::Uninit() | 168 | unknown |
| `000b18a8` | CEGL_PACKET::Free() | 168 | unknown |
| `000f39d4` | ask_event(int, int, int, SVECTOR*, int) | 168 | unknown |
| `0010d844` | Wask_event(int, int, int, SVECTOR*, int) | 168 | unknown |
| `0015fc38` | iOSJobChanegAngleHosei(short, short*) | 168 | unknown |
| `001732bc` | cDrawModeChg(int, int, int, RECT16*, int) | 168 | unknown |
| `0017a384` | bHelpMessage(int) | 168 | unknown |
| `001dbba0` | employ_from_entry(unsigned char*, int, int, int) | 168 | unknown |
| `001eec88` | forceChangeAnimation(int, int, tag_animation*) | 168 | unknown |
| `0020e940` | requestNewAnimation(int, int, int, short, short, int, int) | 168 | unknown |
| `002116f0` | padReadGenerate() | 168 | unknown |
| `00217e14` | InitEffectAnimation() | 168 | unknown |
| `00248b70` | ctlpremov_init(int, int, int, int, int, char*) | 168 | unknown |
| `0025dee0` | wldfade_set(int, int) | 168 | unknown |
| `00263ef4` | ctlnobel_active(CTLINFO*) | 168 | unknown |
| `00272598` | SetMoveAreaSafePanelOnly() | 168 | unknown |
| `00284ee0` | pspBattleForceParticipationInit(int) | 168 | unknown |
| `00285cc4` | pspJobGetJobChangeFlag(unsigned char*, unsigned char, unsigned char (*) [3], int) | 168 | unknown |
| `0029e194` | _gte_rtir() | 168 | unknown |
| `002b3610` | Boot_FrameRender() | 168 | unknown |
| `002ca6d4` | __udivsi3 | 168 | unknown |
| `0008b4f0` | floor1_interpolate_fit | 164 | unknown |
| `0008c458` | vorbis_synthesis_idheader | 164 | unknown |
| `0008d264` | vorbis_granule_time | 164 | unknown |
| `0009cfac` | vorbis_packet_blocksize | 164 | unknown |
| `0009f244` | ov_open_callbacks | 164 | unknown |
| `000b5d94` | CUI_SCROLLBAR::CorrectScrollBounds(int) | 164 | unknown |
| `000b8f48` | CSTR_UTIL::GetExt(char*, char*, int) | 164 | unknown |
| `000b95a0` | CSTR_UTIL::Diff_DBCS(char*, char*) | 164 | unknown |
| `000ba094` | GetLocalTime(_SYSTEMTIME*) | 164 | unknown |
| `001ac224` | iOS_RESUME_SET_FFTDATA_UNITLIST(IOS_RESUME_DATA_FFTDATA_UNITLIST*, IOS_RESUME_DATACOPY_MODE) | 164 | unknown |
| `001bb460` | SetSttsAbi(int) | 164 | unknown |
| `001ef8f4` | requestThrowAnimation(tag_animation*, tag_animation*) | 164 | unknown |
| `001f4a88` | initEntryPlayerAnimations() | 164 | unknown |
| `0021669c` | fadeMusic(int, int) | 164 | unknown |
| `0024556c` | movie_exit(int) | 164 | unknown |
| `0025dd14` | iOSwldkey_repSet(unsigned long) | 164 | unknown |
| `0025e160` | fadeanb_calc(CVECTOR*, CVECTOR*) | 164 | unknown |
| `00276cd4` | JudgeStatus(int, BWORK*, int) | 164 | unknown |
| `00289ac0` | pspFftLoad(int, FFT_SAVE_DATA*, int*, int) | 164 | unknown |
| `0029a3ec` | DrawPrim | 164 | unknown |
| `002a1dcc` | RotAverage3 | 164 | unknown |
| `002b2a94` | SE_SetVol(int, int) | 164 | unknown |
| `002cce40` | __gnu_Unwind_RaiseException | 164 | unknown |
| `00081bb8` | unzCloseCurrentFile | 160 | unknown |
| `00084f88` | vorbis_block_init | 160 | unknown |
| `000960f0` | res0_free_look | 160 | unknown |
| `000a7ff8` | CEGL2_IF::SetTexWrapMode(int) | 160 | unknown |
| `000aec18` | CEGL2_SPRITE::CEGL2_SPRITE() | 160 | unknown |
| `000b3d88` | CINPUT_IF_TOUCH::Clear(int) | 160 | unknown |
| `000be204` | CSTEP_BATCH::Init(_DATA_STEP_BATCH*, int, int, char*) | 160 | unknown |
| `000d6da8` | initpolyft4(tagPOLY_FT4*) | 160 | unknown |
| `000fe8cc` | Winitpolyft4(tagPOLY_FT4*) | 160 | unknown |
| `0015685c` | load_worldname() | 160 | unknown |
| `0015e3e4` | iOSAnimeIDCntGet(int, int) | 160 | unknown |
| `0018fa20` | eMenuSelVertical(unsigned short, unsigned char, unsigned long) | 160 | unknown |
| `001d4008` | check_monsterup(BWORK*) | 160 | unknown |
| `001f01ac` | requestGuardedAnimation(tag_animation*, tag_animation*) | 160 | unknown |
| `0020d14c` | requestMapScrollXYZRelative(VECTOR*, unsigned short) | 160 | unknown |
| `0020d6c0` | requestMapScaleRelative(VECTOR*, unsigned short) | 160 | unknown |
| `0020d934` | requestMapAngleRelative(SVECTOR*, unsigned short) | 160 | unknown |
| `0020de58` | resetAllAnimationDirection() | 160 | unknown |
| `0020f728` | checkScrolling() | 160 | unknown |
| `00210108` | requestEntryData() | 160 | unknown |
| `00211c88` | DisplayChangePalette() | 160 | unknown |
| `00215254` | loadClutData(unsigned short*, unsigned int, unsigned int, int) | 160 | unknown |
| `00217ebc` | NewEffectAnimation(short) | 160 | unknown |
| `0024452c` | rollline_scroll() | 160 | unknown |
| `00251398` | ctlworking_active(CTLINFO*) | 160 | unknown |
| `00261bc8` | endevent_count(int) | 160 | unknown |
| `002631b4` | ctlmouketeam_active(CTLINFO*) | 160 | unknown |
| `002a0d14` | VectorNormal | 160 | unknown |
| `002a0db4` | VectorNormalS | 160 | unknown |
| `002a21e8` | RotColorDpq3 | 160 | unknown |
| `002cb248` | __aeabi_d2f | 160 | unknown |
| `00078900` | gzclose_r | 156 | unknown |
| `0007af1c` | inflateResetKeep | 156 | unknown |
| `000ba264` | CSOUND_IF::~CSOUND_IF() | 156 | unknown |
| `000baf74` | CSOUND_IF::SetMute(int, int) | 156 | unknown |
| `000bba00` | CSOUND_IF_SL::SetVolume(int, int) | 156 | unknown |
| `000d7a48` | disposememory(char*) | 156 | unknown |
| `000da280` | recieve_statusinfo() | 156 | unknown |
| `000db3a4` | envvolcontrol() | 156 | unknown |
| `000e226c` | valueput(char*, VALUERECORD*, COPYFIELD*, int) | 156 | unknown |
| `00110d28` | Wvalueput(char*, VALUERECORD*, COPYFIELD*, int) | 156 | unknown |
| `001bb224` | SetSttsEqu2(int) | 156 | unknown |
| `001bb590` | AllSttsReflesh() | 156 | unknown |
| `001cd9b0` | inc_party_item(BWORK*, unsigned short, BWORK*) | 156 | unknown |
| `001d1c4c` | pspNetSetPlayerWorkEntry() | 156 | unknown |
| `001d2d48` | clear_status_animation(BWORK*) | 156 | unknown |
| `001d9104` | set_status_counter(BWORK*, int, int) | 156 | unknown |
| `001ed8b0` | getBattleWorkAnimationHight(tag_animation*) | 156 | unknown |
| `00216458` | disposeMusic(int) | 156 | unknown |
| `0021f548` | DisposePermanentObject(char) | 156 | unknown |
| `00221028` | RequestBowEffect(long, EffectOrder*) | 156 | unknown |
| `00271504` | GetDirectionForPanel(signed char*, signed char*) | 156 | unknown |
| `00273d20` | IsNullUnit(int) | 156 | unknown |
| `0027faa0` | iOS_SuspendWorldMap() | 156 | unknown |
| `002a1eb4` | RotAverageNclipColorCol3 | 156 | unknown |
| `002b6bd0` | iOSUnitListAreaTapCheck() | 156 | unknown |
| `002b6c6c` | iOSUnitListStsAreaCheck() | 156 | unknown |
| `00077b80` | gzrewind | 152 | unknown |
| `0007854c` | gzgetc | 152 | unknown |
| `0007afe8` | inflateReset2 | 152 | unknown |
| `0009eb64` | ov_pcm_total | 152 | unknown |
| `000b10f8` | CCAMERA::CCAMERA() | 152 | unknown |
| `00125238` | Wrecover_windows(int, int) | 152 | unknown |
| `0013819c` | recover_windows(int, int) | 152 | unknown |
| `0014dd4c` | addbpitem(int) | 152 | unknown |
| `0015e484` | iOSAnimeIDCntGet2(BWORK*, int) | 152 | unknown |
| `001a7404` | SetRyoteFlag(short*, int) | 152 | unknown |
| `001bd3cc` | UnitListInit() | 152 | unknown |
| `001ed6fc` | getDestAnimationHight(tag_animation*) | 152 | unknown |
| `001ed818` | getOriginalAnimationHight(tag_animation*) | 152 | unknown |
| `001ee674` | initializeCancelSignal(tag_animation*, int) | 152 | unknown |
| `0021f328` | GetPermanentObject() | 152 | unknown |
| `0022ab4c` | AddRndVECTORToVECTORShift12(VECTOR*, VECTOR*, VECTOR*) | 152 | unknown |
| `002432e4` | fRoll_cdxareq(short*) | 152 | unknown |
| `0025f1e8` | wldmes_load(int) | 152 | unknown |
| `00263254` | ctlmouketeam_deactive(CTLINFO*) | 152 | unknown |
| `0026b86c` | wldsymbol_draw() | 152 | unknown |
| `0026ff30` | wldwintex_point(int, RECT16, _POINT*) | 152 | unknown |
| `00271378` | Ssd_SetEffectVolume(long, short) | 152 | unknown |
| `0027e3d8` | iOS_CMenuTouchSaveLoad::isInAssist(int, int, int) | 152 | unknown |
| `0028dc58` | xpApiEnv::StartRCnt(unsigned long) | 152 | unknown |
| `002a0e54` | VectorNormalSS | 152 | unknown |
| `002a1d34` | RotTransPers3N | 152 | unknown |
| `002cb0c0` | __gtdf2 | 152 | unknown |
| `0007cc5c` | inflateGetDictionary | 148 | unknown |
| `0008bea4` | vorbis_comment_add | 148 | unknown |
| `000ac0a0` | CEGL2_SHADER::Unload(int) | 148 | unknown |
| `000adb1c` | CEGL2_SPRITE::LoadBegin(unsigned char*, int, int, int, int, int, unsigned char, int) | 148 | unknown |
| `000b6588` | CCRYPT::Encrypt(unsigned char*, int, unsigned int) | 148 | unknown |
| `000d665c` | addlocalprim(tagPOLY_FT4*) | 148 | unknown |
| `000d7d6c` | sttsback_blue(STTSWINDOWBACK*) | 148 | unknown |
| `000d8f4c` | multiwindow_packetcolor(PRIMPACKET*) | 148 | unknown |
| `000da63c` | export_suc(int) | 148 | unknown |
| `000e14f4` | statusfigprint10(int, int, char*, COPYFIELD*) | 148 | unknown |
| `000fe1a4` | Waddlocalprim(tagPOLY_FT4*) | 148 | unknown |
| `00100d64` | Wmultiwindow_packetcolor(PRIMPACKET*) | 148 | unknown |
| `00102208` | Wexport_suc(int) | 148 | unknown |
| `0010ffd8` | Wstatusfigprint10(int, int, char*, COPYFIELD*) | 148 | unknown |
| `0015a1e8` | iOSLRChgSwype(int, int, int, int) | 148 | unknown |
| `0015a744` | iOSScrollButtonAreaCheck() | 148 | unknown |
| `0015b084` | iOSSlidStop() | 148 | unknown |
| `0015d6b4` | iOSTchCurUnitCheck() | 148 | unknown |
| `0015da60` | iOSSwap(short*, short*, short*, short*, int, int) | 148 | unknown |
| `00160468` | iOSSlideYajiSet(int) | 148 | unknown |
| `0017a2f0` | bDrawMessage(int, COMRECORD*) | 148 | unknown |
| `001bb320` | SetSttsEqu(int) | 148 | unknown |
| `001d5968` | set_turn_end(int) | 148 | unknown |
| `001d7438` | search_empty_savework(int, unsigned char*) | 148 | unknown |
| `001eeeb0` | requestKnockBack(tag_animation*) | 148 | unknown |
| `001f5b50` | terminateAnimationSub(int, int, short, short, short) | 148 | unknown |
| `0020e9e8` | requestEntryAnimation(int, int) | 148 | unknown |
| `00210e18` | pspNetGetRandomWeather() | 148 | unknown |
| `002161e0` | loadMusic(int) | 148 | unknown |
| `00220f94` | StartPermanentEffect(long, long, EffectOrder*) | 148 | unknown |
| `00240444` | Mdl0025(short, int, int, int) | 148 | unknown |
| `0024b790` | ctlbar_deactive(CTLINFO*) | 148 | unknown |
| `0026640c` | wldpac_draw(GsOT*, unsigned long*, int) | 148 | unknown |
| `00266544` | iOS_drawMenuAssist_wld(iOS_CMenuTouch*, GsOT*) | 148 | unknown |
| `00268be0` | wldcenter_set(_POINT*, SVECTOR*) | 148 | unknown |
| `00268ec4` | wldcenter_move() | 148 | unknown |
| `002766f4` | GetHightDistance(unsigned char*, BWORK*) | 148 | unknown |
| `0028e010` | xpLibapiSaveStart | 148 | unknown |
| `00290b54` | ClearOTag | 148 | unknown |
| `002a04fc` | RotMatrixXZY | 148 | unknown |
| `002a0590` | RotMatrixYXZ | 148 | unknown |
| `002a0638` | RotMatrixYZX | 148 | unknown |
| `002a06cc` | RotMatrixZXY | 148 | unknown |
| `002a0760` | RotMatrixZYX | 148 | unknown |
| `002b6b38` | Main_Uninit() | 148 | unknown |
| `002b715c` | setPspDispNum(short, short, short) | 148 | unknown |
| `002bb678` | iOSMenuOkCancelHelpGet(int, int) | 148 | unknown |
| `002bf0a8` | iOS_setFaceDataID(int, int) | 148 | unknown |
| `0008333c` | ogg_stream_init | 144 | unknown |
| `00097b70` | _float32_pack | 144 | unknown |
| `000a7160` | CGX_SCREEN_CORRECT::Area_InitPortrait(int, int, int, int, int) | 144 | unknown |
| `000b4414` | CINPUT_IF_TOUCH::OnTouchesMoved(int, int, int, int) | 144 | unknown |
| `000b72e8` | CFILE_TXT::GetWord(char*, int, CLIST*, char) | 144 | unknown |
| `000b8ca4` | CSTR_UTIL::GetFile(char*, char*) | 144 | unknown |
| `000b8e10` | CSTR_UTIL::ToUpperAndConv3(char, char*, char*) | 144 | unknown |
| `000b8fec` | CSTR_UTIL::CorrectToPath(char*) | 144 | unknown |
| `000d7b24` | sttsback_normal(STTSWINDOWBACK*) | 144 | unknown |
| `000f0730` | multiwindow_keyloop(COMRECORD*, int*) | 144 | unknown |
| `000ff95c` | Wsttsback_blue(STTSWINDOWBACK*) | 144 | unknown |
| `00100934` | Wmultiwindow_keyloop(COMRECORD*, int*) | 144 | unknown |
| `0011d6b0` | TEST_read_eventflag(int) | 144 | unknown |
| `001253b0` | Wextend_valuefield(int) | 144 | unknown |
| `00138314` | extend_valuefield(int) | 144 | unknown |
| `001532c0` | task_create(long, char*) | 144 | unknown |
| `00153584` | Wtask_create(long, char*) | 144 | unknown |
| `00161c4c` | iOSUnitListLRMoveCheck() | 144 | unknown |
| `00167ff8` | ASHURA_FileRead_Proto(char const*, char*, char*, unsigned long) | 144 | unknown |
| `001a8b94` | AbilityCompare(C_STTS*, short, short) | 144 | unknown |
| `001d6718` | get_mapstp(int, int, int) | 144 | unknown |
| `00207d6c` | iOS_mapVectorLimit() | 144 | unknown |
| `0020e228` | get2DPosition(SVECTOR*, SVECTOR*) | 144 | unknown |
| `0021b38c` | SetEffectSEDPtr(short) | 144 | unknown |
| `00221e84` | RequestLandingEffect(EffectOrder*, VECTOR*) | 144 | unknown |
| `00245690` | strInit(int, void (*)()) | 144 | unknown |
| `0025e204` | wldfade_mask() | 144 | unknown |
| `0026dc2c` | ctltuto_active(CTLINFO*) | 144 | unknown |
| `00273e10` | CompareMove(MOVE*, MOVE*) | 144 | unknown |
| `00291824` | SetDrawLoad | 144 | unknown |
| `00292678` | __xpLibgpuDrawCallBack(int) | 144 | unknown |
| `002abc8c` | sceGuTexFilter | 144 | unknown |
| `002cb0c8` | __ltdf2 | 144 | unknown |
| `00084dac` | vorbis_bitrate_flushpacket | 140 | unknown |
| `0008c1ac` | vorbis_comment_clear | 140 | unknown |
| `000a9430` | CEGL2_IF::Init() | 140 | unknown |
| `000b5394` | CRECT::MulAndAddRect(int, float, int, int) | 140 | unknown |
| `000b552c` | CRECT::GetFirstEnableUI(int) | 140 | unknown |
| `000b5988` | CRECT::GetNextEnableUI(int, int) | 140 | unknown |
| `000b8c18` | CSTR_UTIL::GetPath(char*, char*) | 140 | unknown |
| `000bb570` | CSOUND_IF_SL::CB_for_Static(SLAndroidSimpleBufferQueueItf_ const* const*, void*) | 140 | unknown |
| `000bc9fc` | CSOUND_IF_SL::Unload(int) | 140 | unknown |
| `000da9c4` | checkpara1(int) | 140 | unknown |
| `000dfb50` | recover_chrname() | 140 | unknown |
| `000ff718` | Wsttsback_normal(STTSWINDOWBACK*) | 140 | unknown |
| `00102e14` | Wenvvolcontrol() | 140 | unknown |
| `0010c7fc` | Wrecover_chrname() | 140 | unknown |
| `0017a0b8` | bMessageMake(unsigned char*, unsigned char*, short*, int) | 140 | unknown |
| `001837b8` | CardDelete(unsigned char*) | 140 | unknown |
| `0018f02c` | eMessageMake(unsigned char*, unsigned char*, short*, int) | 140 | unknown |
| `001b6a74` | MessageMake(unsigned char*, unsigned char*, short*, int) | 140 | unknown |
| `001bb504` | SetSttsBoth(int) | 140 | unknown |
| `001dc37c` | inc_dead_number(BWORK*) | 140 | unknown |
| `00202f5c` | pspNetRequestStatus(int) | 140 | unknown |
| `00216154` | loadMusicBuffer(int, int) | 140 | unknown |
| `0021627c` | readMusicBuffer(int, int) | 140 | unknown |
| `0022a618` | _OpenTMD(unsigned long*, int) | 140 | unknown |
| `0022aac0` | AddRndVECTORToVECTOR(VECTOR*, VECTOR*, VECTOR*) | 140 | unknown |
| `0022ac38` | AddRndSVECTORToSVECTOR(SVECTOR*, SVECTOR*, SVECTOR*) | 140 | unknown |
| `00245e38` | ctlstartmov_init(int, int, int, int) | 140 | unknown |
| `00251438` | ctlworking_deactive(CTLINFO*) | 140 | unknown |
| `002562fc` | sthelp_curpos_set(CTLINFO*) | 140 | unknown |
| `0025e7b4` | wldfrm_clr(int) | 140 | unknown |
| `0027fb3c` | iOS_ResumeWorldMap() | 140 | unknown |
| `00284314` | Init_VectorDataBaseObject(VECTOR_DATABASE_CONTAINER*, unsigned int) | 140 | unknown |
| `00284594` | new_Vector(VECTOR_DATABASE*, SVECTOR const*) | 140 | unknown |
| `002889cc` | pspOffScreenInit(RECT16*, RECT16*) | 140 | unknown |
| `0028e5e0` | pspNetPadRead | 140 | unknown |
| `0029b544` | GsClearOt | 140 | unknown |
| `002cb4ac` | __floatundisf | 140 | unknown |
| `00080844` | unzStringFileNameCompare | 136 | unknown |
| `000b39b4` | CINPUT_DATA::GetUpGroup(int) | 136 | unknown |
| `000b4ee8` | CINPUT_IF_TOUCH::BeginAll(int) | 136 | unknown |
| `000b58d4` | CRECT::GetPrevEnableUI(int, int) | 136 | unknown |
| `000b7378` | CFILE_TXT::SetData(int, int, char*) | 136 | unknown |
| `000b9778` | CSTR_UTIL::FindChar_DBCS(char*, char*, CLIST*) | 136 | unknown |
| `000db83c` | read_eventflag(int) | 136 | unknown |
| `000e5680` | disp_status2() | 136 | unknown |
| `000e5708` | disp_status2right() | 136 | unknown |
| `00103400` | Wread_eventflag(int) | 136 | unknown |
| `0015ee54` | iOSUnitListWinInit(int) | 136 | unknown |
| `00161da4` | iOSGetStatuswindowTap() | 136 | unknown |
| `0018e13c` | eSetSttsPara2(int) | 136 | unknown |
| `001bc2ac` | AllSttsDelete() | 136 | unknown |
| `001d2de4` | init_status_animation(int) | 136 | unknown |
| `001ee13c` | initializeItem(tag_animation*, int) | 136 | unknown |
| `001ef9d8` | requestCast1Animation(tag_animation*) | 136 | unknown |
| `0020db18` | setBackColorOffset(short, short, short) | 136 | unknown |
| `00224cc4` | GetPermanentEffectAnimationAngle() | 136 | unknown |
| `00228d40` | InitPermanentShape() | 136 | unknown |
| `002433dc` | fRoll_cdxastop(short*) | 136 | unknown |
| `00269798` | snpl_wait() | 136 | unknown |
| `002715a0` | CountMap(unsigned short (*) [18]) | 136 | unknown |
| `0027cd28` | iOS_CMenuTouch::drawMenuAssist(int, long*) | 136 | unknown |
| `0028dba8` | xpApiEnv::SetRCnt(unsigned long, unsigned short, long) | 136 | unknown |
| `0029f4d0` | _gte_dpcs() | 136 | unknown |
| `0029f5f0` | _gte_intpl() | 136 | unknown |
| `002b85f8` | RayPick_GT4(tagPOLY_GT4*, int, int) | 136 | unknown |
| `002b8680` | RayPick_GT3(tagPOLY_GT3*, int, int) | 136 | unknown |
| `002cb0d0` | __cmpdf2 | 136 | unknown |
| `0007d9ac` | fill_fopen_filefunc | 132 | unknown |
| `0007da30` | fill_fopen64_filefunc | 132 | unknown |
| `000822c0` | unzGetOffset64 | 132 | unknown |
| `0009864c` | vorbis_book_init_encode | 132 | unknown |
| `000a1d3c` | CG2D_LOADER::~CG2D_LOADER() | 132 | unknown |
| `000a26d0` | CG2D_LOADER::CalcAsTexture(int*, int*) | 132 | unknown |
| `000a3340` | CG2D_LOADER_BMP::GetSavePixelFormatOverwrite(_G2D_FORMAT*, int) | 132 | unknown |
| `000a7390` | CGX_SCREEN_CORRECT::Area_ToScreen(int, int, int, int*, int*) | 132 | unknown |
| `000b9368` | CSTR_UTIL::ToText(char*, char*) | 132 | unknown |
| `0011bfa8` | Wdisp_status2() | 132 | unknown |
| `0011c02c` | Wdisp_status2right() | 132 | unknown |
| `0015dfbc` | iOSActiveUnitGet() | 132 | unknown |
| `00161994` | iOSUnitListStsMoveCheck() | 132 | unknown |
| `00188a10` | ePowerCompare(C_STTS*, A_STTS*, short, short, int) | 132 | unknown |
| `001a8b10` | GetAbilityParameter(short, C_STTS*) | 132 | unknown |
| `001a8efc` | PowerCompare(C_STTS*, A_STTS*, short, short, int) | 132 | unknown |
| `001abb18` | MakeChr(short) | 132 | unknown |
| `001d57c8` | get_unit_turn(BWORK*) | 132 | unknown |
| `001ed794` | getAnimationHight(tag_animation*) | 132 | unknown |
| `0021a5c4` | SearchNextScheduleDividePos(short, short, long*, long*) | 132 | unknown |
| `0024a414` | vOpn_pacdraw(unsigned long*, unsigned long*, int) | 132 | unknown |
| `002642f4` | ctlnobelstop_deactive(CTLINFO*) | 132 | unknown |
| `0026a120` | snpl_rndjp() | 132 | unknown |
| `0026dcbc` | ctltuto_deactive(CTLINFO*) | 132 | unknown |
| `0027d730` | iOS_CMenuTouchNum::setMenuAssistPosition(int) | 132 | unknown |
| `00280498` | cSaveFFT::Delete() | 132 | unknown |
| `00285650` | pspItemGetWeaponVariationData(unsigned short) | 132 | unknown |
| `0028d7d0` | tlHeapStat(tl_mem_stat_t*) | 132 | unknown |
| `00290be8` | ClearOTagR | 132 | unknown |
| `00290c6c` | AddPrim | 132 | unknown |
| `002a0370` | RotMatrixX | 132 | unknown |
| `002a03f4` | RotMatrixY | 132 | unknown |
| `002a0478` | RotMatrixZ | 132 | unknown |
| `002a2740` | PadInitDirect | 132 | unknown |
| `002b2714` | EnvSE_SetVol(int, int) | 132 | unknown |
| `002bf364` | Debug_SetMapPolyCheck(int) | 132 | unknown |
| `00085028` | _vorbis_block_alloc | 128 | unknown |
| `000a80f4` | CEGL2_IF::SetTexFilter(int) | 128 | unknown |
| `000ac3cc` | std::priv::_Rb_global<bool>::_M_decrement(std::priv::_Rb_tree_node_base*) | 128 | unknown |
| `000b4808` | CINPUT_IF_TOUCH::GetGestureTapChance(int, int, int, unsigned int) | 128 | unknown |
| `000b8800` | CFILE_UTIL::FileGetSize(char*) | 128 | unknown |
| `000b8880` | CFILE_UTIL::FileGetTime(char*, _SYSTEMTIME*) | 128 | unknown |
| `000be038` | CSTEP::InitFromCurrent(int, int, int, unsigned int) | 128 | unknown |
| `000d9790` | wait_overlay(int) | 128 | unknown |
| `000d9988` | wait_loaddata(int) | 128 | unknown |
| `000dc994` | movetopanelsub(char*) | 128 | unknown |
| `001015a4` | Wwait_overlay(int) | 128 | unknown |
| `00101888` | Wwait_loaddata(int) | 128 | unknown |
| `00103f50` | Wmovetopanelsub(char*) | 128 | unknown |
| `0015d324` | iOSUnitWorkClear() | 128 | unknown |
| `0015df3c` | iOSTapCalcu() | 128 | unknown |
| `00161250` | iOSSdNovelClear() | 128 | unknown |
| `00173ccc` | cDrawMessage(int, COMRECORD*) | 128 | unknown |
| `0018f284` | eDrawMessage(int, COMRECORD*) | 128 | unknown |
| `001b7074` | DrawMessage(int, COMRECORD*) | 128 | unknown |
| `001bc520` | scroll_chk() | 128 | unknown |
| `001d3d98` | check_act_ok(BWORK*) | 128 | unknown |
| `001d6494` | iOS_RESUME_SET_COMWIND(IOS_RESUME_DATA_COMWIND*, IOS_RESUME_DATACOPY_MODE) | 128 | unknown |
| `001e1ffc` | CheckBladeResult(int, int, int, int, int) | 128 | unknown |
| `0020df40` | eventMapJump(int, int) | 128 | unknown |
| `0020dfc0` | eventMapJump2(int, int) | 128 | unknown |
| `0020e3cc` | jumpToPanel(int, int, int) | 128 | unknown |
| `0020f7f4` | prepareForEventGun(int, int) | 128 | unknown |
| `00245610` | strSetDefDecEnv(DECENV*, int, int, int, int) | 128 | unknown |
| `00249f14` | vOpn_dataload2() | 128 | unknown |
| `0024ab04` | vOpnwin_noropen(int, RECT16, int, int, unsigned long*) | 128 | unknown |
| `0024fd74` | pspCtltutonet_deactive(CTLINFO*) | 128 | unknown |
| `0025f0b8` | pic_load(int) | 128 | unknown |
| `0025f168` | bk_load(int) | 128 | unknown |
| `0025f358` | psp_bk_load(int, void*) | 128 | unknown |
| `00264274` | ctlnobelstop_active(CTLINFO*) | 128 | unknown |
| `00266654` | add_winpac(unsigned long*, int*) | 128 | unknown |
| `002701a4` | wldwin_noropen(int, RECT16, int, int, unsigned long*) | 128 | unknown |
| `0027b240` | GetCountToDeath(BWORK*) | 128 | unknown |
| `00286c10` | pspNetEntranceMapThumLoad() | 128 | unknown |
| `0028defc` | xpApiEnv::_card_info(long) | 128 | unknown |
| `00291b40` | xpLibgpuEndRender | 128 | unknown |
| `002b102c` | CDebugPrint::AddLine(float, float, float, float, unsigned char, unsigned char, unsigned char, unsigned char) | 128 | unknown |
| `002b3590` | Boot_FrameMove() | 128 | unknown |
| `000791a8` | gzflush | 124 | unknown |
| `00085154` | vorbis_block_clear | 124 | unknown |
| `00085f2c` | vorbis_synthesis_restart | 124 | unknown |
| `000867f4` | vorbis_synthesis_pcmout | 124 | unknown |
| `000a2754` | CG2D_LOADER::CalcAsTexture(int, int, int*, int*) | 124 | unknown |
| `000a96a0` | CEGL2_IF::DrawSprite(CEGL2_SPRITE*, float, float, float, float, float, float) | 124 | unknown |
| `000ab86c` | CEGL2_SHADER::End() | 124 | unknown |
| `000aef8c` | CEGL2_TEX_HYBRID::CLUTAddr_Regist(unsigned int) | 124 | unknown |
| `000b5318` | CRECT::MulRect(int, float) | 124 | unknown |
| `000b6bdc` | CFILE_DAT::CacheReplace(int, unsigned char*, int) | 124 | unknown |
| `000b915c` | CSTR_UTIL::CorrectToFile(char*) | 124 | unknown |
| `000b9ad0` | CSTR_UTIL::Shorten(char*, int) | 124 | unknown |
| `000ba684` | CSOUND_IF::Stop(int) | 124 | unknown |
| `000ba774` | CSOUND_IF::IsPlaying(int, int) | 124 | unknown |
| `000bb4a4` | CSOUND_IF::PauseAll(unsigned char, unsigned char) | 124 | unknown |
| `000bb8c8` | CSOUND_IF_SL::Pause(int) | 124 | unknown |
| `000da204` | request_atlist() | 124 | unknown |
| `000daff0` | move_ambient() | 124 | unknown |
| `00101ec0` | Wrequest_atlist() | 124 | unknown |
| `00102aa4` | Wmove_ambient() | 124 | unknown |
| `00105510` | Wwait_direc(int) | 124 | unknown |
| `00159924` | asmTaskEntry() | 124 | unknown |
| `00161ef8` | wasmTaskEntry() | 124 | unknown |
| `0016a14c` | ASURA_soundStop() | 124 | unknown |
| `00198598` | jDrawWindow(unsigned char*, unsigned long) | 124 | unknown |
| `001baae8` | SttsAMovingChk() | 124 | unknown |
| `001dbc48` | init_entry_status0(BWORK*) | 124 | unknown |
| `001efb44` | requestStanderdStandAnimation(tag_animation*) | 124 | unknown |
| `0020c550` | db_swap_generate(unsigned long*, unsigned long*) | 124 | unknown |
| `0020e0b0` | eventMapExit(int) | 124 | unknown |
| `00210d9c` | NewEntry(int, int, int, short, short, short, short, BWORK*, int) | 124 | unknown |
| `0024a544` | vOpn_add_winpac(unsigned long*, int*) | 124 | unknown |
| `0024a9e4` | vOpnwin_trans(int, unsigned long*) | 124 | unknown |
| `0025da0c` | wldkey_repinit() | 124 | unknown |
| `002665d8` | add_anmpac(unsigned long*, int*) | 124 | unknown |
| `00269bc0` | snpl_timeset() | 124 | unknown |
| `0027008c` | wldwin_trans(int, unsigned long*) | 124 | unknown |
| `00271da0` | EvaluateAllUnitAction() | 124 | unknown |
| `00279eec` | SetTrapPanel(int, int, int) | 124 | unknown |
| `0027d6b4` | iOS_CMenuTouchNum::init(int, int, int, int, int, int, int, int, int) | 124 | unknown |
| `0028bec0` | TE_VSync(int) | 124 | unknown |
| `0029a89c` | SetDefDrawEnv | 124 | unknown |
| `002a1bfc` | RotTransPers4 | 124 | unknown |
| `002a2340` | RotAverageNclipColorDpq3_nom | 124 | unknown |
| `002b2798` | SE_CorrectFID(int) | 124 | unknown |
| `002b2a18` | SE_StopVFX(int) | 124 | unknown |
| `002b36dc` | Error_FrameRender() | 124 | unknown |
| `002cb4bc` | __floatdisf | 124 | unknown |
| `000ab7f4` | CEGL2_SHADER::Begin(int, math::MATRIX4*) | 120 | unknown |
| `000b422c` | CINPUT_IF_TOUCH::GetGestureDoubleTap(int, int, int, int) | 120 | unknown |
| `000b5b4c` | CUI_SCROLLBAR::Add(int, int) | 120 | unknown |
| `000b6834` | CFILE_DAT::CFILE_DAT() | 120 | unknown |
| `000b9800` | CSTR_UTIL::CmpLastChar(char*, char, int) | 120 | unknown |
| `000bc984` | CSOUND_IF_SL::Stream_Unload(int) | 120 | unknown |
| `000bdbf4` | CSTEP::Init(int, int, int, int, unsigned int) | 120 | unknown |
| `000d7e00` | load_replaceitems(int, int) | 120 | unknown |
| `000dcc2c` | wait_direc(int) | 120 | unknown |
| `000ff9ec` | Wload_replaceitems(int, int) | 120 | unknown |
| `0015d2ac` | iOS_GameAreaCheck() | 120 | unknown |
| `00161bd4` | iOSUnitListStsMoveLRCheck() | 120 | unknown |
| `001789e0` | iOS_addPrim_graphic(tagPOLY_FT4*, short) | 120 | unknown |
| `001a47e0` | pspAbilityCompareSupport(short, short) | 120 | unknown |
| `001a9254` | GetTotalEquipItem(short) | 120 | unknown |
| `001a92f8` | ItemCheck() | 120 | unknown |
| `001ab104` | IsUntauchable(int) | 120 | unknown |
| `001adcec` | iOS_addPrim_window_graphics_unitlist(tagPOLY_FT4*, short) | 120 | unknown |
| `001d9ee0` | copy_entry_coord(BWORK*, EDATA*) | 120 | unknown |
| `001e4e94` | get_step_no(BWORK*) | 120 | unknown |
| `001ee5fc` | initializeExpNumber(tag_animation*) | 120 | unknown |
| `001ef4e8` | requestDefaultColor(tag_animation*, int, int) | 120 | unknown |
| `001efa60` | requestCast2Animation(tag_animation*, tag_animation*) | 120 | unknown |
| `001fd200` | setTurnOrder() | 120 | unknown |
| `00211d28` | requestDestinationClut(int, unsigned int, unsigned int, int, unsigned short*) | 120 | unknown |
| `0021e760` | doSequence(short) | 120 | unknown |
| `0023c6b0` | Mdl0016(short, int, int, int) | 120 | unknown |
| `00245aa8` | o_GetCardEvent() | 120 | unknown |
| `00245b78` | o_GetCardEvent_X() | 120 | unknown |
| `0024a4cc` | vOpn_add_anmpac(unsigned long*, int*) | 120 | unknown |
| `00258c78` | evt_deep() | 120 | unknown |
| `0025e680` | wld_daywrite(unsigned long*, int, FINDDAY*) | 120 | unknown |
| `0028441c` | Clear_VectorDataBaseContainer(VECTOR_DATABASE_CONTAINER*) | 120 | unknown |
| `002918ec` | SetTexWindow | 120 | unknown |
| `00294d44` | xpLibgpuVramInit | 120 | unknown |
| `002a1f50` | RotAverageNclipColorCol3_nom | 120 | unknown |
| `002a38d8` | pspSaveList::setUserId() | 120 | unknown |
| `002b10ac` | CDebugPrint::AddRect(float, float, float, float, unsigned char, unsigned char, unsigned char, unsigned char) | 120 | unknown |
| `002b1458` | Project_Core_Bootup() | 120 | unknown |
| `002b6d08` | iOSUnitListAllStatusTapCheck() | 120 | unknown |
| `002b71f0` | iOS_ResumeByAutoSave(int) | 120 | unknown |
| `002c5434` | Movie_FrameRender() | 120 | unknown |
| `00077524` | gzerror | 116 | unknown |
| `00081660` | unzGoToFilePos64 | 116 | unknown |
| `00082ef0` | oggpack_read1 | 116 | unknown |
| `00082f64` | oggpackB_read1 | 116 | unknown |
| `00088cfc` | _ve_envelope_shift | 116 | unknown |
| `000a6f38` | CGX_SCREEN_CORRECT::ToScreen(int, int, int*, int*) | 116 | unknown |
| `000a731c` | CGX_SCREEN_CORRECT::Area_ToRender(int, int, int, int*, int*) | 116 | unknown |
| `000aa8f8` | CEGL2_FBO::Delete() | 116 | unknown |
| `000b6654` | CFILE::Open(unsigned int) | 116 | unknown |
| `000b8b3c` | CLIST::Create(int, void*) | 116 | unknown |
| `000ba610` | CSOUND_IF::UnloadAll(unsigned char) | 116 | unknown |
| `000ba700` | CSOUND_IF::StopAll(unsigned char) | 116 | unknown |
| `000c81c4` | tool_squareinit() | 116 | unknown |
| `000d8c00` | checkkeyok() | 116 | unknown |
| `000e2b04` | statusnowprint(char*, COPYFIELD*) | 116 | unknown |
| `000fb4bc` | iOS_setEventFace(int) | 116 | unknown |
| `000ff43c` | Wallocatememoryinit() | 116 | unknown |
| `00111574` | Wstatusnowprint(char*, COPYFIELD*) | 116 | unknown |
| `0018e0c8` | eSetSttsEqu(int) | 116 | unknown |
| `001b7ef4` | TruePadRead(int) | 116 | unknown |
| `001cd058` | adjust_input_flag(BWORK*) | 116 | unknown |
| `001d43f4` | check_unit_active(BWORK*) | 116 | unknown |
| `001fd168` | setActivePanelFromAction(tag_animation*) | 116 | unknown |
| `001fd514` | requestParmanentEffectMyself(tag_animation*, int) | 116 | unknown |
| `00201708` | setActionStartDirection(tag_animation*) | 116 | unknown |
| `002042c8` | startTurnRelative(int) | 116 | unknown |
| `0020d1ec` | executeMapScrollXYZ() | 116 | unknown |
| `0020d760` | executeMapScale() | 116 | unknown |
| `0020d9d4` | executeMapAngle() | 116 | unknown |
| `0020e19c` | getAnimationPositionFromBattleWork(unsigned int, SVECTOR*) | 116 | unknown |
| `0021cc10` | s1e_ifMetascheduleEnd(_EffectTCB*) | 116 | unknown |
| `0023c728` | Mdl0017_sub(int, int, VECTOR*, SVECTOR*) | 116 | unknown |
| `002492b8` | vEnd_init() | 116 | unknown |
| `0024c44c` | bgscrol_chk_x(_POINT*, VECTOR*) | 116 | unknown |
| `0024c4c0` | bgscrol_chk_y(_POINT*, VECTOR*) | 116 | unknown |
| `0024fd00` | pspCtltutonet_active(CTLINFO*) | 116 | unknown |
| `00258bcc` | evt_exit_sel() | 116 | unknown |
| `0025b878` | houkokumes_select(int, int) | 116 | unknown |
| `0025d590` | directedit_chk() | 116 | unknown |
| `00276bb4` | GetUnitOnPanel(unsigned char*) | 116 | unknown |
| `002816bc` | iOS_v2menuSetEnable(V2_MENU_ITEM, int) | 116 | unknown |
| `00284fd0` | pspBattleEntryAreaCheck(int, int, int, int, short) | 116 | unknown |
| `0028a0a0` | iOS_RESUME_SET_PSPSAVE(IOS_RESUME_DATA_PSPSAVE*, IOS_RESUME_DATACOPY_MODE) | 116 | unknown |
| `0029f67c` | _gte_sqr12() | 116 | unknown |
| `002a3418` | pspSaveBase::SystemFileSet() | 116 | unknown |
| `002cabdc` | __floatundidf | 116 | unknown |
| `002cb830` | __gtsf2 | 116 | unknown |
| `002ccf00` | __gnu_Unwind_Resume | 116 | unknown |
| `0007b190` | inflatePrime | 112 | unknown |
| `00080a4c` | unzGoToFirstFile | 112 | unknown |
| `00082c38` | oggpack_adv | 112 | unknown |
| `00097a48` | res1_forward | 112 | unknown |
| `000b417c` | CINPUT_IF_TOUCH::GetTouchPoint(int, int*, int*, int) | 112 | unknown |
| `000b6e70` | CFILE_DAT::Decode(int, unsigned char*, int) | 112 | unknown |
| `000b8900` | CFILE_UTIL::FileSetTime(char*, _SYSTEMTIME*) | 112 | unknown |
| `000d7880` | allocatememoryinit() | 112 | unknown |
| `000daa50` | checktaskkind(int) | 112 | unknown |
| `000db77c` | write_eventflag(int, int) | 112 | unknown |
| `000e05bc` | addlocalprim2(tagPOLY_FT4*) | 112 | unknown |
| `000feeb4` | Wdisposewindowbytask(int) | 112 | unknown |
| `001026c4` | Wchecktaskkind(int) | 112 | unknown |
| `00103340` | Wwrite_eventflag(int, int) | 112 | unknown |
| `0010e0e4` | Waddlocalprim2(tagPOLY_FT4*) | 112 | unknown |
| `0015b278` | iOSSlidBUfDel() | 112 | unknown |
| `0015bfac` | iOSTchInputCheckCur() | 112 | unknown |
| `0015d900` | iOSBtlUnitMoveCheckSub() | 112 | unknown |
| `0018f304` | eHelpMessage(int) | 112 | unknown |
| `001d1f8c` | check_charge(BWORK*, int) | 112 | unknown |
| `001d2324` | get_mapitem(BWORK*) | 112 | unknown |
| `001eb0b4` | raiseAnimationPriority(int) | 112 | unknown |
| `001ed68c` | getTargetAnimationHight(tag_animation*, SVECTOR*) | 112 | unknown |
| `0020e040` | eventMapFadeIn(int) | 112 | unknown |
| `00241938` | fftCdRead2(CDREC*, int, int, int, unsigned long*) | 112 | unknown |
| `002419d4` | vOpn_arzmes_init(int, int, unsigned long*) | 112 | unknown |
| `00254100` | wldctl_init() | 112 | unknown |
| `0026030c` | ctlmouke_exit(CTLINFO*) | 112 | unknown |
| `0026fad8` | ctluwa_exit(CTLINFO*) | 112 | unknown |
| `00270490` | curhis_put(int, int, int) | 112 | unknown |
| `002727fc` | StayAtSafePanel() | 112 | unknown |
| `00276c28` | CheckCrystalAndTresureBox() | 112 | unknown |
| `0027ef74` | iOS_CMenuTouchSaveLoad::isTaped() | 112 | unknown |
| `002821f8` | iOS_dispOkNg(int, int) | 112 | unknown |
| `0028d088` | tlSetHeap(void*) | 112 | unknown |
| `0028e25c` | OpenEvent(unsigned long, long, long, long (*)()) | 112 | unknown |
| `0029fa50` | _gte_nccs() | 112 | unknown |
| `002a1798` | gteMIMefunc | 112 | unknown |
| `002a23bc` | RotColorDpq3_nom | 112 | unknown |
| `002a3240` | pspSaveAuto::pspSaveAuto() | 112 | unknown |
| `002b1ab0` | AppEngine_Suspend() | 112 | unknown |
| `002b22e8` | AppEngineFFT_Init() | 112 | unknown |
| `002ca125` | __cxa_type_match | 112 | unknown |
| `000726fc` | Java_com_square_1enix_FFT_1Android_GL2JNILib_init | 108 | unknown |
| `00095668` | _vp_ampmax_decay | 108 | unknown |
| `00096eb4` | res0_inverse | 108 | unknown |
| `00096f20` | res1_inverse | 108 | unknown |
| `000985e0` | vorbis_book_clear | 108 | unknown |
| `0009cc9c` | drft_clear | 108 | unknown |
| `0009ea44` | ov_serialnumber | 108 | unknown |
| `000ad858` | CEGL2_SPRITE::AddPacketLayout(float, float, _EGL_SPRITE_LAYOUT*, CEGL_PACKET*) | 108 | unknown |
| `000b6a58` | CFILE_DAT::Close() | 108 | unknown |
| `000b6f00` | CFILE_TXT::Unload() | 108 | unknown |
| `000b98c0` | CSTR_UTIL::Insert(char*, int, char*) | 108 | unknown |
| `000baf08` | CSOUND_IF::SetMasterVolume(int, int, int) | 108 | unknown |
| `000bb230` | CSOUND_IF::SetTrans(int, float, float, float) | 108 | unknown |
| `000d6eac` | iOS_initsprt_num(tagSPRT*, int) | 108 | unknown |
| `000d8778` | import_localstatus(char*, char*, char*, char*) | 108 | unknown |
| `000d9a14` | seekfacefile(int) | 108 | unknown |
| `000fe9d0` | WiOS_initsprt_num(tagSPRT*, int) | 108 | unknown |
| `00101914` | Wseekfacefile(int) | 108 | unknown |
| `0015ac3c` | iOSRotSpeedGet(int) | 108 | unknown |
| `0015b20c` | iOSSlideSpeedGet(int) | 108 | unknown |
| `0015d858` | iOSCurSameOKMove() | 108 | unknown |
| `00165afc` | ASHURA_Flat_OTZ(unsigned long) | 108 | unknown |
| `001a9370` | GetTotalItemBackup(short) | 108 | unknown |
| `001b6e60` | GetCharAdr(unsigned char*, int) | 108 | unknown |
| `001b9070` | iOSTutoTaskCheck() | 108 | unknown |
| `001d1d20` | appare_unit_f(int) | 108 | unknown |
| `001efad8` | requestLevelupAnimation(tag_animation*) | 108 | unknown |
| `0020c930` | freeForFile(void*) | 108 | unknown |
| `0020f164` | setEventClut(int, int, int) | 108 | unknown |
| `0020f2e4` | eventEffectCall(int, int, SVECTOR*) | 108 | unknown |
| `002151e8` | resetClutData(unsigned int, unsigned int, int) | 108 | unknown |
| `00215950` | loadAnbient() | 108 | unknown |
| `002159bc` | loadFlatColor() | 108 | unknown |
| `00215c08` | changeCharacterClut(int, int, int, short, short, short) | 108 | unknown |
| `0021bf70` | s19_ifChildTaskEQU(_EffectTCB*) | 108 | unknown |
| `00245c0c` | o_GetCardState() | 108 | unknown |
| `00249c58` | vOpn_bk_load(int, unsigned long*) | 108 | unknown |
| `00259324` | evt_get_date(int*, int*, int*, int*) | 108 | unknown |
| `0025c6d8` | shogou_mesput(CTLINFO*) | 108 | unknown |
| `00269ec8` | snpl_mesput() | 108 | unknown |
| `0026a504` | snpl_jparasmall() | 108 | unknown |
| `00281730` | iOS_v2menuGetEnable(V2_MENU_ITEM) | 108 | unknown |
| `00282648` | wgte_color_set_vec(MATRIX const*, int, SVECTOR const*) | 108 | unknown |
| `00287198` | pspNetTrapSetAnimation() | 108 | unknown |
| `0029fe04` | xpLibgteSetData | 108 | unknown |
| `002a2460` | RotColorMatDpq(SVECTOR*, SVECTOR*, CVECTOR*, long*, CVECTOR*, long, long*) | 108 | unknown |
| `002a3550` | pspSaveBase::TitleStrSet(char const*, char const*, char const*) | 108 | unknown |
| `002a35dc` | pspSaveBase::ErrorMsgTypeGet(unsigned int) | 108 | unknown |
| `002ab960` | sceGuGetMemory_for_iOS | 108 | unknown |
| `002b2f7c` | musicPlayer_Stop() | 108 | unknown |
| `002cb838` | __ltsf2 | 108 | unknown |
| `00077ad0` | gzdopen | 104 | unknown |
| `00082360` | unzSetOffset64 | 104 | unknown |
| `00083c1c` | ogg_stream_pageout_fill | 104 | unknown |
| `0008589c` | vorbis_analysis_init | 104 | unknown |
| `0009f390` | ov_test_open | 104 | unknown |
| `000ab440` | CEGL2_FBO::ReadPixels(unsigned int*, int, int, int, int) | 104 | unknown |
| `000af50c` | CEGL2_TEX_HYBRID::~CEGL2_TEX_HYBRID() | 104 | unknown |
| `000b35e4` | CINPUT_DATA::SetKeyWaitGroup(int, unsigned int, unsigned int) | 104 | unknown |
| `000b38e4` | CINPUT_DATA::GetPressGroup(int) | 104 | unknown |
| `000b394c` | CINPUT_DATA::GetDownGroup(int) | 104 | unknown |
| `000b3a3c` | CINPUT_DATA::GetUpDirectGroup(int) | 104 | unknown |
| `000b3aa4` | CINPUT_DATA::GetRepeatGroup(int) | 104 | unknown |
| `000b3b0c` | CINPUT_DATA::GetDelayDownGroup(int) | 104 | unknown |
| `000b6708` | CFILE::Read(void*, unsigned int, unsigned int, unsigned int*) | 104 | unknown |
| `000b8ad4` | CLIST::Delete(int) | 104 | unknown |
| `000b9484` | CSTR_UTIL::ChangeExt(char*, char*) | 104 | unknown |
| `000b94ec` | CSTR_UTIL::ExtCmp(char*, char*) | 104 | unknown |
| `000ba51c` | CSOUND_IF::ClearSavedata(int) | 104 | unknown |
| `000bc03c` | CSOUND_IF_SL::Static_Load(int) | 104 | unknown |
| `000bdb8c` | CSTEP::InitF(float, float, int, int, unsigned int) | 104 | unknown |
| `0010044c` | Wimport_localstatus(char*, char*, char*, char*) | 104 | unknown |
| `0015a180` | iOSLRChgTap(int, int, int, int) | 104 | unknown |
| `0016f578` | ASHURA_Exit() | 104 | unknown |
| `00176e84` | bSearchUnit(short) | 104 | unknown |
| `00177378` | iOS_RESUME_SET_FFTDATA(IOS_RESUME_DATA_FFTDATA*, IOS_RESUME_DATACOPY_MODE) | 104 | unknown |
| `001abab0` | SearchUnit(short) | 104 | unknown |
| `001d18e4` | Resume_MK_BSTR_IsLoaded(int) | 104 | unknown |
| `001e0ec4` | check_invincible(int, int*) | 104 | unknown |
| `001e6938` | setskilldata(ACT*) | 104 | unknown |
| `0020c6e4` | freeForSound(void*) | 104 | unknown |
| `00213da4` | startColorRotation(int, int, int, int) | 104 | unknown |
| `0021cfe4` | GetEffectTCB() | 104 | unknown |
| `00259390` | evt_date_high() | 104 | unknown |
| `002593f8` | evt_date_low() | 104 | unknown |
| `00269aa0` | snpl_chgpara() | 104 | unknown |
| `00269e04` | snpl_mfadein() | 104 | unknown |
| `0026a1cc` | snpl_musicstop() | 104 | unknown |
| `0026b5e4` | ssd_request(int, int) | 104 | unknown |
| `002738a8` | SetThresholdDoNothing() | 104 | unknown |
| `0027ab4c` | iOS_RESUME_SET_INITIAL(IOS_RESUME_DATA_INITIAL*, IOS_RESUME_DATACOPY_MODE) | 104 | unknown |
| `00281a2c` | iOS_v2menuIsInMenu(int, int) | 104 | unknown |
| `00294ed8` | xpLibgpuBuffersOffsetGet | 104 | unknown |
| `0029cf68` | _gte_SetRotMatrix(MATRIX*) | 104 | unknown |
| `0029db80` | _gte_FlipRotMatrixX() | 104 | unknown |
| `0029fbb8` | _gte_cc() | 104 | unknown |
| `002a1c78` | RotNclip4 | 104 | unknown |
| `002cba30` | __aeabi_d2ulz | 104 | unknown |
| `00077498` | gzoffset64 | 100 | unknown |
| `0007d0f4` | inflateMark | 100 | unknown |
| `0007d8b0` | call_zseek64 | 100 | unknown |
| `00083bb8` | ogg_stream_pageout | 100 | unknown |
| `000a3bb4` | CG2D_LOADER_BMP::BMP_SetAddress(unsigned char*) | 100 | unknown |
| `000a8188` | CEGL2_IF::SetScissor(int, int, int, int) | 100 | unknown |
| `000a86c8` | CEGL2_IF::AddSprite(int, CEGL2_SPRITE*, float, float, float, float, float, float, unsigned char) | 100 | unknown |
| `000a9378` | CEGL2_IF::SetupSprite(math::MATRIX4*) | 100 | unknown |
| `000ae520` | CEGL2_SPRITE::DrawLayout(float, float, _EGL_SPRITE_LAYOUT*) | 100 | unknown |
| `000b36c4` | CINPUT_DATA::End(int, int) | 100 | unknown |
| `000b9644` | CSTR_UTIL::Find(char*, char*) | 100 | unknown |
| `000ba020` | timeGetTimeM() | 100 | unknown |
| `000ba5ac` | CSOUND_IF::Unload(int) | 100 | unknown |
| `000bd220` | COggMemMapFile::CallbackSeek(void*, long long, int) | 100 | unknown |
| `000cbab8` | createEndModeWindow() | 100 | unknown |
| `000cbd90` | iOS_ResumeMusic() | 100 | unknown |
| `000d6e48` | initsprt(tagSPRT*) | 100 | unknown |
| `000d8648` | getanimpos(int) | 100 | unknown |
| `000db440` | eventenvse() | 100 | unknown |
| `000f15a0` | disp_backtotitle_yesno() | 100 | unknown |
| `000fe96c` | Winitsprt(tagSPRT*) | 100 | unknown |
| `00102ea0` | Weventenvse() | 100 | unknown |
| `0010638c` | Wdisp_backtotitle_yesno() | 100 | unknown |
| `001d1a18` | set_playerwork_sp(PENTRY*, unsigned char*, int) | 100 | unknown |
| `001d3a24` | iOS_RESUME_SET_BW_INIT(IOS_RESUME_DATA_BW_INIT*, IOS_RESUME_DATACOPY_MODE) | 100 | unknown |
| `001e20c0` | dec_party_item(BWORK*, unsigned short, int) | 100 | unknown |
| `001eb2fc` | disposeAbilityAnimation(tag_animation*) | 100 | unknown |
| `001fecc0` | rideOffChokobo(tag_animation*) | 100 | unknown |
| `0020e498` | offsetAnimationPosition(int, SVECTOR*) | 100 | unknown |
| `0020e4fc` | setOffsetAnimationPosition(int, SVECTOR*) | 100 | unknown |
| `00215cbc` | fadeCharacterClut(int, int, unsigned short*) | 100 | unknown |
| `0022a268` | getAbsoluteMaximumOf3(short, short, short) | 100 | unknown |
| `0024358c` | fRoll_autochg(short*) | 100 | unknown |
| `00246388` | ctlopentitle_active(CTLINFO*) | 100 | unknown |
| `002463ec` | ctlopentitle_deactive(CTLINFO*) | 100 | unknown |
| `0025e2ac` | mouke_tbl_get(MOUINFO*, int) | 100 | unknown |
| `002775dc` | JudgeMovable(int) | 100 | unknown |
| `0027cdb0` | iOS_CMenuTouch::setLRCurEffect(int) | 100 | unknown |
| `0027dda8` | iOS_CMenuTouchNum::setNumCurEffect(int) | 100 | unknown |
| `0028d1c4` | tlPushHeap(void*) | 100 | unknown |
| `002a1204` | SquareSS12 | 100 | unknown |
| `002a2184` | RotColorDpq | 100 | unknown |
| `002b0200` | GlTexEnv_GetTextureSize(int, float*, float*, float*, float*) | 100 | unknown |
| `002b0264` | GlTexEnv_GetTextureSize_2X(int, float*, float*, float*, float*) | 100 | unknown |
| `002b0718` | CDebugPrint::EngineInit(char*, float) | 100 | unknown |
| `002b29b4` | SE_StopAll() | 100 | unknown |
| `002bf020` | iOS_isInCursorRotate() | 100 | unknown |
| `002bf174` | iOS_setFaceDataCLUT(int, int) | 100 | unknown |
| `002cb840` | __cmpsf2 | 100 | unknown |
| `0007cbfc` | inflateEnd | 96 | unknown |
| `00084000` | ogg_sync_pageout | 96 | unknown |
| `00084444` | ogg_stream_reset | 96 | unknown |
| `000a971c` | CEGL2_IF::DrawScrollBG(CEGL2_SPRITE*, float, float, _RECT_F32*, _RECT_F32*) | 96 | unknown |
| `000abb28` | CEGL2_SHADER::CompileShader(unsigned int&, void*, unsigned int) | 96 | unknown |
| `000af5d4` | CEGL2_TEX_HYBRID::GL_GetTextureSize(int, float*, float*, float*, float*) | 96 | unknown |
| `000b37c0` | CINPUT_DATA::GetUp(int, int) | 96 | unknown |
| `000b4050` | CINPUT_IF_TOUCH::GetPressCount(int) | 96 | unknown |
| `000b4e88` | CINPUT_IF_TOUCH::Begin(int, int) | 96 | unknown |
| `000b5f4c` | CUI_SCROLLBAR::DragUpdate(int, int) | 96 | unknown |
| `000b6c70` | CFILE_DAT::GetBuffer(int) | 96 | unknown |
| `000bb160` | CSOUND_IF::GetPlaySample(int) | 96 | unknown |
| `000bb1c0` | CSOUND_IF::GetTotalSample(int) | 96 | unknown |
| `000bd3b4` | COggMemMapFile::Open(char const*, unsigned int, unsigned int) | 96 | unknown |
| `000d7e78` | serchmessagepointer(int) | 96 | unknown |
| `000ffa64` | Wserchmessagepointer(int) | 96 | unknown |
| `00100320` | Wgetanimpos(int) | 96 | unknown |
| `0010c79c` | Wmakemessagestructure() | 96 | unknown |
| `00150630` | NetEndSyncProc() | 96 | unknown |
| `0015ab7c` | iOSRotBufSetX(int) | 96 | unknown |
| `0015abdc` | iOSRotBufSetY(int) | 96 | unknown |
| `0015b14c` | iOSSlideBufSetX(int) | 96 | unknown |
| `0015b1ac` | iOSSlideBufSetY(int) | 96 | unknown |
| `0015b604` | iOSTchStatusModeGet() | 96 | unknown |
| `0015de8c` | iOSGT4_MapOTZGet(unsigned long, short) | 96 | unknown |
| `00160f54` | iOSYajiEffectSetTGA(short, short, int) | 96 | unknown |
| `0016a0ec` | ASHURA_snowMatrix(long, long) | 96 | unknown |
| `001885d0` | eSetItemUserSort(int, short*) | 96 | unknown |
| `001a637c` | iOS_setCancelDisableAreaForStatusWindow() | 96 | unknown |
| `001a72d8` | ChgMoney(int) | 96 | unknown |
| `001a73a4` | ChrNameSet(short, unsigned char*) | 96 | unknown |
| `001a80ac` | SetItemUserSort(int, short*) | 96 | unknown |
| `001ade40` | GetItemCategoryPos(int) | 96 | unknown |
| `001b8fe0` | iOSTutorialMessageKill() | 96 | unknown |
| `001baa18` | unit_isdark() | 96 | unknown |
| `001bb164` | SetSttsA(int) | 96 | unknown |
| `001bb1c4` | SetSttsA2(int) | 96 | unknown |
| `001bb2c0` | SetSttsPara(int) | 96 | unknown |
| `001cd0cc` | set_calcmode_think() | 96 | unknown |
| `001d1ffc` | check_item_left(int, int, int) | 96 | unknown |
| `001d639c` | check_turn_end(int) | 96 | unknown |
| `0020f620` | getMapIDFromAnimationPosition(int) | 96 | unknown |
| `00225a68` | GetParentObject(short, short) | 96 | unknown |
| `00228de4` | NewShape2(unsigned char) | 96 | unknown |
| `0024322c` | fRoll_wait(short*) | 96 | unknown |
| `00245ec4` | ctlopenmov_init(int, int, int) | 96 | unknown |
| `00246300` | vOpn_ctlinit(int) | 96 | unknown |
| `00258da8` | evt_rute_erase() | 96 | unknown |
| `0025c49c` | houkokuinf_init(int) | 96 | unknown |
| `0025d20c` | world_exit() | 96 | unknown |
| `0026a674` | op_search(int, int) | 96 | unknown |
| `002854bc` | iOS_RESUME_SET_PSP_BATTLE(IOS_RESUME_DATA_PSP_BATTLE*, IOS_RESUME_DATACOPY_MODE) | 96 | unknown |
| `0029aa24` | AddPrims | 96 | unknown |
| `002a251c` | RotNclip3 | 96 | unknown |
| `002a2d44` | xpLibSN::PCclose(int) | 96 | unknown |
| `002ab88c` | sceGuBlendFunc | 96 | unknown |
| `002cabf0` | __aeabi_l2d | 96 | unknown |
| `0007d950` | fill_zlib_filefunc64_32_def_from_filefunc32 | 92 | unknown |
| `00081340` | unzOpen2_64 | 92 | unknown |
| `000a8098` | CEGL2_IF::InitRenderState2D() | 92 | unknown |
| `000b5a6c` | CUI_SCROLLBAR::Create(_RECT_S32*, _RECT_S32*, int) | 92 | unknown |
| `000da59c` | initatchrrsvcursor(int) | 92 | unknown |
| `000e10b4` | initdrmode2(DR_MODE*, RECT16*) | 92 | unknown |
| `0010216c` | Winitatchrrsvcursor(int) | 92 | unknown |
| `00155d14` | reactive_worldwindow() | 92 | unknown |
| `00155f2c` | multiwindow_windowbackinit(RECT16*, COMRECORD*, tagSPRT*) | 92 | unknown |
| `00156b90` | hook_tuto(int) | 92 | unknown |
| `0015d3a4` | iOSUnitWorkSet(tag_animation*) | 92 | unknown |
| `0015fbdc` | iOSJobChanegAngleInit(short, short) | 92 | unknown |
| `00161548` | iOSSdNovelBrightCtrlClear() | 92 | unknown |
| `0018e010` | eSetSttsA(int) | 92 | unknown |
| `0018e06c` | eSetSttsPara(int) | 92 | unknown |
| `0018e1c4` | eAllSttsReflesh() | 92 | unknown |
| `0018e358` | esys_warning(int, int) | 92 | unknown |
| `001d52e0` | set_chargeability2(int, unsigned char, short*, unsigned char*, unsigned char*) | 92 | unknown |
| `0020dcb4` | setAnimationDirection(unsigned int, unsigned int) | 92 | unknown |
| `0020ddc8` | setAnimationDirection16(unsigned int, unsigned int) | 92 | unknown |
| `0020e2b8` | getAnimationPanelInfo(unsigned short, SVECTOR*) | 92 | unknown |
| `00216884` | callMusic(int) | 92 | unknown |
| `00216900` | fadeSoundEffect(int, int) | 92 | unknown |
| `002423f4` | ctlendmov_init(int, int, int) | 92 | unknown |
| `00248b14` | ctlopenhelp_main(CTLINFO*) | 92 | unknown |
| `00258b70` | evt_exit_jump() | 92 | unknown |
| `00258cf0` | evt_fset_exit() | 92 | unknown |
| `00258d4c` | evt_rute_grow() | 92 | unknown |
| `0026adc0` | snpl_jpageflg_sub(int) | 92 | unknown |
| `00277f1c` | SetBestMove() | 92 | unknown |
| `0027e738` | iOS_CMenuTouchSaveLoad::drawDebug() | 92 | unknown |
| `0027f568` | iOS_GetRectHitNoTouchDirect(int, int) | 92 | unknown |
| `00288ebc` | pspGetpspPrimWorkBuf(int) | 92 | unknown |
| `0028d43c` | tlGetAllocSize(void const*) | 92 | unknown |
| `00291964` | SetDrawTPage | 92 | unknown |
| `00291ae4` | xpLibgpuStartRender | 92 | unknown |
| `00294924` | xpLibgpuOffScreenRectSet | 92 | unknown |
| `002a1174` | SquareSL12 | 92 | unknown |
| `002b03a4` | TexHybrid_FindNextTexture(int, int) | 92 | unknown |
| `002b1e14` | NowLoading_Init() | 92 | unknown |
| `002b74d4` | IS_GAME_ROT_AREA(int, int) | 92 | unknown |
| `002b7530` | IS_GAME_MOV_AREA(int, int) | 92 | unknown |
| `002cb1ec` | __aeabi_d2iz | 92 | unknown |
| `002cb92c` | __aeabi_f2iz | 92 | unknown |
| `002ccfb8` | _Unwind_VRS_Get | 92 | unknown |
| `002cd03c` | _Unwind_VRS_Set | 92 | unknown |
| `00088920` | _ve_envelope_clear | 88 | unknown |
| `0009f338` | ov_fopen | 88 | unknown |
| `000a3ddc` | CG2D_LOADER_BMP::BMP_LoadMemory(unsigned char*) | 88 | unknown |
| `000a9648` | CEGL2_IF::DrawSprite(CEGL2_SPRITE*, float, float, _EGL_SPRITE_LAYOUT*) | 88 | unknown |
| `000abbc4` | CEGL2_SHADER::~CEGL2_SHADER() | 88 | unknown |
| `000ad800` | CEGL2_SPRITE::AddPacket(float, float, CEGL_PACKET*) | 88 | unknown |
| `000af3cc` | CEGL2_TEX_HYBRID::GL_Unload(int, int) | 88 | unknown |
| `000b3f38` | CINPUT_IF_TOUCH::EndAll(int) | 88 | unknown |
| `000b942c` | CSTR_UTIL::Conv(char, char, char*) | 88 | unknown |
| `000bb838` | CSOUND_IF_SL::Stop(int) | 88 | unknown |
| `000c443c` | Aitemmenu_uvclut(short*, int) | 88 | unknown |
| `000d13b0` | Ditemmenu_uvclut(short*, int) | 88 | unknown |
| `0010fb14` | Winitdrmode2(DR_MODE*, RECT16*) | 88 | unknown |
| `00123be8` | Eitemmenu_uvclut(short*, int) | 88 | unknown |
| `0012cd74` | itemmenu_uvclut(short*, int) | 88 | unknown |
| `001351c0` | Witemmenu_uvclut(short*, int) | 88 | unknown |
| `0014be6c` | Citemmenu_uvclut(short*, int) | 88 | unknown |
| `0015ef7c` | iOSUnitListWinOnOff(int) | 88 | unknown |
| `00161710` | iOSTgaIconClear() | 88 | unknown |
| `00187658` | pspWindowCommonIsType(WINOBJ_TYPE, unsigned char, unsigned char, unsigned char, unsigned char) | 88 | unknown |
| `001a6530` | ScriptRead(int, TUTRIAL*) | 88 | unknown |
| `001ab3b4` | UnitDismiss(short) | 88 | unknown |
| `001ca9b8` | reset_toumei_afterskill(BWORK*) | 88 | unknown |
| `001d62ec` | set_move_end(int) | 88 | unknown |
| `001d6344` | set_act_end(int) | 88 | unknown |
| `001d8f78` | get_pmaxlevel() | 88 | unknown |
| `001dc8b0` | levelup_check(BWORK*) | 88 | unknown |
| `001eab34` | searchActiveAnimation() | 88 | unknown |
| `001eab8c` | searchCurrentAnimation() | 88 | unknown |
| `0020cdbc` | fileOpenForSndCDWithErrorCheck(unsigned long, unsigned long) | 88 | unknown |
| `0020eadc` | inactivateAnimation(int) | 88 | unknown |
| `0020ed84` | activateEventAnimation(int) | 88 | unknown |
| `0020fcc4` | initializeStaticTexture() | 88 | unknown |
| `002163bc` | checkReadMusic() | 88 | unknown |
| `00218008` | ChangeEffectAnimation(effectAnimation*, unsigned char, short) | 88 | unknown |
| `0021b518` | LoadOverlayBin(long) | 88 | unknown |
| `0021d3b0` | s2_startTask(_EffectTCB*) | 88 | unknown |
| `0022a210` | getRandom(short, short) | 88 | unknown |
| `0024328c` | fRoll_waitdot(short*) | 88 | unknown |
| `00243508` | fRoll_bkfadeout(short*) | 88 | unknown |
| `00245c78` | o_Wait_GetCardState(int) | 88 | unknown |
| `00249834` | wldbin_loadchk(int) | 88 | unknown |
| `0024aaac` | vOpnmess_frm(int, _POINT*) | 88 | unknown |
| `00253a10` | wldctl_active() | 88 | unknown |
| `00253ec8` | wldctl_deactive() | 88 | unknown |
| `00256490` | ctlsthelp_active(CTLINFO*) | 88 | unknown |
| `0025f63c` | wldlop_chk() | 88 | unknown |
| `0026b31c` | snplread_parcalc() | 88 | unknown |
| `00270b04` | pagenext_cursor(PAGEWININFO*) | 88 | unknown |
| `00273cc8` | IsAlmostNullUnit(int) | 88 | unknown |
| `0027f1ac` | iOS_SetRectHit(int, int, int, int, int, int) | 88 | unknown |
| `002815e8` | iOS_RESUME_SET_SUBR(IOS_RESUME_DATA_SUBR*, IOS_RESUME_DATACOPY_MODE) | 88 | unknown |
| `0028b844` | uninitTaskEmu() | 88 | unknown |
| `0028c768` | CFFT_STATE::AttackTeamFaceIDToUnitATFID(int) | 88 | unknown |
| `002916b8` | SetDrawArea | 88 | unknown |
| `00294dbc` | xpLibgpuOffScreenRectGet | 88 | unknown |
| `0029b678` | GsSetDrawBuffClip | 88 | unknown |
| `0029cdb8` | _gte_ldopv1(VECTOR*) | 88 | unknown |
| `0029d080` | _gte_SetTransMatrix(MATRIX*) | 88 | unknown |
| `0029d120` | _gte_SetTransVector(VECTOR*) | 88 | unknown |
| `0029d298` | _gte_ldopv1SV(SVECTOR*) | 88 | unknown |
| `002a126c` | TransRotPers3 | 88 | unknown |
| `002a3950` | pspSaveList::paramCreate() | 88 | unknown |
| `002ab908` | sceGuStart | 88 | unknown |
| `002b2290` | GX_ApplyVertexScaling(int) | 88 | unknown |
| `002b2e48` | Jingle_Stop(int) | 88 | unknown |
| `000824cc` | oggpackB_writetrunc | 84 | unknown |
| `000832e8` | ogg_stream_clear | 84 | unknown |
| `0009858c` | vorbis_staticbook_destroy | 84 | unknown |
| `000b89b0` | CLIST::DeleteAll() | 84 | unknown |
| `000b8ea0` | CSTR_UTIL::ToUpper(char*) | 84 | unknown |
| `000b8ef4` | CSTR_UTIL::ToLower(char*) | 84 | unknown |
| `000b9eb0` | CTHREAD::Register(unsigned int (*)(void*), void*) | 84 | unknown |
| `000ba838` | CSOUND_IF::GetMute(int) | 84 | unknown |
| `000ba88c` | CSOUND_IF::GetVolume(int) | 84 | unknown |
| `000bb2cc` | CSOUND_IF::SetAutoUnload(int, int) | 84 | unknown |
| `000bc268` | CSOUND_IF_SL::Static_Unload(int) | 84 | unknown |
| `000bce58` | CSOUND_LOADER_PCM::Seek(unsigned long) | 84 | unknown |
| `000e0568` | export_localpad(long*) | 84 | unknown |
| `000e0f14` | iOS_assist_addlocalprim2(iOS_CMenuTouch*, int) | 84 | unknown |
| `000e2fbc` | statuskanjiprintadv(int, char*, COPYFIELD*) | 84 | unknown |
| `0010dea4` | Wexport_localpad(long*) | 84 | unknown |
| `0010f8f4` | WiOS_assist_addlocalprim2(iOS_CMenuTouch*, int) | 84 | unknown |
| `0010f948` | iOS_assist_addlocalprim3(iOS_CMenuTouch*, int, int) | 84 | unknown |
| `0011a440` | Wstatuskanjiprintadv(int, char*, COPYFIELD*) | 84 | unknown |
| `001531f8` | edit_smallpacket() | 84 | unknown |
| `0015ab28` | iOSRotSpeed(int*, int*, double, double) | 84 | unknown |
| `0015bf58` | iOSSlideDirecChgMode() | 84 | unknown |
| `0015eff0` | iOSUnitListLRCurWrite(unsigned char*, unsigned short*) | 84 | unknown |
| `0015fec4` | iOSJobNumberGet(short, short) | 84 | unknown |
| `0015ffa0` | iOSJobChgRotStop() | 84 | unknown |
| `00173c78` | cDrawMessageKillFast(int) | 84 | unknown |
| `00181dbc` | bDrawWindow(unsigned char*, unsigned long) | 84 | unknown |
| `00191d30` | eDrawWindow(unsigned char*, unsigned long) | 84 | unknown |
| `0019d7e8` | DrawUnits() | 84 | unknown |
| `0019e134` | SuccessEmploy() | 84 | unknown |
| `001b7020` | DrawMessageKillFast(int) | 84 | unknown |
| `001c51b4` | DrawWindow(unsigned char*, unsigned long) | 84 | unknown |
| `001eed30` | getShapeAddress(unsigned short) | 84 | unknown |
| `0021c274` | s7_setEditorProc(_EffectTCB*) | 84 | unknown |
| `0021c2c8` | s8_mapScrollXYZ(_EffectTCB*) | 84 | unknown |
| `0021d1e8` | s3_killChildTask(_EffectTCB*) | 84 | unknown |
| `0022531c` | NewHeap(void*, long) | 84 | unknown |
| `0022a480` | getVariationAppearPosition(_ParticleParameter*, int, VECTOR*) | 84 | unknown |
| `0022a4d4` | getVariationAppearRange(_ParticleParameter*, int, VECTOR*) | 84 | unknown |
| `0022a528` | getVariationAppearVec(_ParticleParameter*, int, VECTOR*) | 84 | unknown |
| `0022a57c` | getVariationAppearVecRange(_ParticleParameter*, int, VECTOR*) | 84 | unknown |
| `0022abe4` | AddVECTORToVECTORShift12(VECTOR*, VECTOR*, VECTOR*) | 84 | unknown |
| `0023dbec` | Mdl0020(short, int, int, int) | 84 | unknown |
| `0023dc40` | Mdl0021(short, int, int, int) | 84 | unknown |
| `002434b4` | fRoll_bkfadein(short*) | 84 | unknown |
| `00243bf4` | drawMessage(int) | 84 | unknown |
| `00243c48` | DeleteData(tagLIST_STAFFROLL*, tagSTAFFROLL*, tagSTAFFROLL*) | 84 | unknown |
| `002459ec` | strSync(DECENV*, int) | 84 | unknown |
| `00245cd0` | o_CardCheck() | 84 | unknown |
| `00245de4` | vOpn_ctlprog() | 84 | unknown |
| `0024b02c` | wldmapEntry(int) | 84 | unknown |
| `002539bc` | wldctl_cur() | 84 | unknown |
| `00255758` | iOSHelpCheck() | 84 | unknown |
| `0025d53c` | world_init() | 84 | unknown |
| `00265f84` | iOSSDNovelBackLogCheck() | 84 | unknown |
| `00269b2c` | snpl_jparae() | 84 | unknown |
| `00269db0` | snpl_mfadeout() | 84 | unknown |
| `00269f84` | snpl_backput() | 84 | unknown |
| `0026a45c` | snpl_jparane() | 84 | unknown |
| `0026a4b0` | snpl_jparabig() | 84 | unknown |
| `0026a7d0` | snSound_play(int) | 84 | unknown |
| `0026ad5c` | snpl_je_sub(int) | 84 | unknown |
| `00273dbc` | CompareScore(SCORE*, SCORE*) | 84 | unknown |
| `0027bba8` | iOS_CMenuTouch::isCanDown(int*, int*) | 84 | unknown |
| `0027dd54` | iOS_CMenuTouchNum::setNumCur() | 84 | unknown |
| `0027fa4c` | iOS_Resume_DataCopyAddr(IOS_RESUME_DATACOPY_MODE, unsigned char*, unsigned char*, int) | 84 | unknown |
| `00285c30` | pspItemIsDataType | 84 | unknown |
| `00288e18` | pspPushScreenRect(RECT16*, RECT16*) | 84 | unknown |
| `00289fac` | pspLoadSystemFile() | 84 | unknown |
| `0028a000` | pspSaveSystemFile() | 84 | unknown |
| `0029a5c4` | xpLibgpuClearImage | 84 | unknown |
| `0029f55c` | _gte_dpcl() | 84 | unknown |
| `002a0c88` | TransposeMatrix | 84 | unknown |
| `002a1ce0` | RotTransPersN | 84 | unknown |
| `002a2130` | RotAverageNclip4 | 84 | unknown |
| `002b0350` | TexHybrid_FindPrevTexture(int, int) | 84 | unknown |
| `002b5e58` | Logo_Uninit() | 84 | unknown |
| `002cb988` | __aeabi_f2uiz | 84 | unknown |
| `002cdf18` | __aeabi_d2uiz | 84 | unknown |
| `00072960` | Java_com_square_1enix_FFT_1Android_GL2JNILib_setAccelerometerValue | 80 | unknown |
| `00075794` | deflatePending | 80 | unknown |
| `000788b0` | gzdirect | 80 | unknown |
| `000815e0` | unzGetFilePos64 | 80 | unknown |
| `0008247c` | oggpack_writetrunc | 80 | unknown |
| `00087230` | vorbis_book_encode | 80 | unknown |
| `0009e92c` | ov_test | 80 | unknown |
| `0009f2e8` | ov_open | 80 | unknown |
| `000a09d0` | ov_info | 80 | unknown |
| `000a0da0` | ov_comment | 80 | unknown |
| `000a95f8` | CEGL2_IF::DrawSprite(CEGL2_SPRITE*, float, float) | 80 | unknown |
| `000aad68` | CEGL2_FBO::Begin(int, int) | 80 | unknown |
| `000ae4d0` | CEGL2_SPRITE::Draw(float, float) | 80 | unknown |
| `000b5d44` | CUI_SCROLLBAR::GetCellDraw(int) | 80 | unknown |
| `000d8830` | makemessagepacket(char*) | 80 | unknown |
| `000d9490` | multiwindow_packetclipinit(CLIP*) | 80 | unknown |
| `000db7ec` | tutorial_syscall(int) | 80 | unknown |
| `000e2b78` | statuskanjiprint(int, char*, COPYFIELD*) | 80 | unknown |
| `00100500` | Wmakemessagepacket(char*) | 80 | unknown |
| `001012a8` | Wmultiwindow_packetclipinit(CLIP*) | 80 | unknown |
| `001033b0` | Wtutorial_syscall(int) | 80 | unknown |
| `001115e8` | Wstatuskanjiprint(int, char*, COPYFIELD*) | 80 | unknown |
| `0015a60c` | siOS_TCurPosGet(unsigned int, int) | 80 | unknown |
| `00167cb8` | ASHURA_MapProjectFlag(char, short, short) | 80 | unknown |
| `00173960` | cMesEventSingle(int, unsigned int, int, int) | 80 | unknown |
| `0018efdc` | eMesEventSingle(int, unsigned int, int, int) | 80 | unknown |
| `001b696c` | MesEventSingle(int, unsigned int, int, int) | 80 | unknown |
| `001bac48` | iOSWldUnitListWinSet(int) | 80 | unknown |
| `001d6430` | eacape_battlefield(int) | 80 | unknown |
| `001d74cc` | get_unitno(int) | 80 | unknown |
| `001ebfac` | setAnimationRealVector(SVECTOR*, tag_animation*) | 80 | unknown |
| `001eee60` | getPositionFromPanel(tag_animation*) | 80 | unknown |
| `001f5ef4` | iOS_setAnimationIrowakeSub(tag_animation*, short, int, int, int) | 80 | unknown |
| `001f639c` | setLongPositionToPosition(tag_animation*) | 80 | unknown |
| `001fce04` | setActivePanelFromAnimation(tag_animation*) | 80 | unknown |
| `0020c14c` | iOS_isIrobakeEffect() | 80 | unknown |
| `0020dc64` | getAnimationDirection(unsigned int) | 80 | unknown |
| `0020dd78` | getAnimationDirection16(unsigned int) | 80 | unknown |
| `0020eb34` | checkJumpReset() | 80 | unknown |
| `0021584c` | loadClutDataCalc(unsigned short*, unsigned int, unsigned int, int, short, short, short, int) | 80 | unknown |
| `0021c35c` | sb_mapAngle(_EffectTCB*) | 80 | unknown |
| `00221f14` | RequestReboundEffect() | 80 | unknown |
| `00228e98` | GetShapePrim(int) | 80 | unknown |
| `00243464` | fRoll_bkput(short*) | 80 | unknown |
| `0024599c` | strNext(DECENV*) | 80 | unknown |
| `00249ec4` | vEnd_dataload() | 80 | unknown |
| `0025396c` | ctlmap_deactive(CTLINFO*) | 80 | unknown |
| `002591d4` | evt_get_flgdt(int*, int*) | 80 | unknown |
| `00269820` | snpl_picclr() | 80 | unknown |
| `00269c80` | snpl_selparacalc() | 80 | unknown |
| `00269f34` | snpl_mesput2() | 80 | unknown |
| `0026a27c` | snpl_fadein() | 80 | unknown |
| `0026a40c` | snpl_volchg() | 80 | unknown |
| `0026a5fc` | snplinf_clr(SNPLINFO*) | 80 | unknown |
| `0026ae2c` | snpl_jstatflg_sub(int) | 80 | unknown |
| `0026ae8c` | snpl_jlocalflg_sub(int) | 80 | unknown |
| `0026d724` | iOS_chkBraveTresureFlag(unsigned int) | 80 | unknown |
| `00270154` | wldmess_frm(int, _POINT*) | 80 | unknown |
| `00282478` | iOS_ClippedInit() | 80 | unknown |
| `002824c8` | iOS_disableClipInit() | 80 | unknown |
| `00288e6c` | pspPopScreenRect(RECT16*, RECT16*) | 80 | unknown |
| `0028c690` | CFFT_STATE::UnitIDToFID_SP2(int, int) | 80 | unknown |
| `002912f8` | LoadClut | 80 | unknown |
| `0029b4f4` | GsDefDispBuff | 80 | unknown |
| `0029cf18` | _gte_ldsvrtrow0(SVECTOR*) | 80 | unknown |
| `0029d8dc` | _gte_ReadRotMatrix(MATRIX*) | 80 | unknown |
| `0029d954` | _gte_ReadLightMatrix(MATRIX*) | 80 | unknown |
| `0029d9a4` | _gte_ReadColorMatrix(MATRIX*) | 80 | unknown |
| `0029da34` | _gte_mvlvtr() | 80 | unknown |
| `0029fc24` | _gte_nclip() | 80 | unknown |
| `002a1fc8` | RotAverageNclip3_nom | 80 | unknown |
| `002a24cc` | RotTransPers3 | 80 | unknown |
| `002a2b98` | xpLibSN::PCinit() | 80 | unknown |
| `002a2db8` | xpLibSN::OpenCheck(char*) | 80 | unknown |
| `002a30b0` | xpMallocAlign | 80 | unknown |
| `002bb53c` | Main_Suspend() | 80 | unknown |
| `00077400` | gzbuffer | 76 | unknown |
| `000a7514` | CGX_SCREEN_CORRECT::Area_X_ScalingDiff(int, int, float) | 76 | unknown |
| `000a7560` | CGX_SCREEN_CORRECT::Area_Y_ScalingDiff(int, int, float) | 76 | unknown |
| `000a9224` | CEGL2_IF::SetupFont() | 76 | unknown |
| `000abc38` | std::priv::_Rb_global<bool>::_Rotate_left(std::priv::_Rb_tree_node_base*, std::priv::_Rb_tree_node_base*&) | 76 | unknown |
| `000abc84` | std::priv::_Rb_global<bool>::_Rotate_right(std::priv::_Rb_tree_node_base*, std::priv::_Rb_tree_node_base*&) | 76 | unknown |
| `000af574` | CEGL2_TEX_HYBRID::RAW_IsUpdate(int) | 76 | unknown |
| `000b1a80` | CEGL_PACKET::Add(int) | 76 | unknown |
| `000b3bd8` | CINPUT_IF_TOUCH::CINPUT_IF_TOUCH() | 76 | unknown |
| `000b5bc4` | CUI_SCROLLBAR::IsEnableScrollDown() | 76 | unknown |
| `000b70d4` | CFILE_TXT::IsDataComment(int, int, unsigned int) | 76 | unknown |
| `000b8158` | CFILE_UTIL::FileFind(char*) | 76 | unknown |
| `000b9554` | CSTR_UTIL::CmpN(char*, char*, int) | 76 | unknown |
| `000bbe30` | CSOUND_IF_SL::Static_DeletePlayer(int) | 76 | unknown |
| `000bd998` | CFRAMERATE::CFRAMERATE(float, float) | 76 | unknown |
| `000d87e4` | export_localstatus(char*, char*, char*) | 76 | unknown |
| `000d8eb4` | multiwindow_loadcolor(tagSPRT*) | 76 | unknown |
| `000d8f00` | multiwindow_loadcolor2(tagSPRT*) | 76 | unknown |
| `000e3010` | statuskanjiprintwithptr(char*, COPYFIELD*, char*) | 76 | unknown |
| `001004b4` | Wexport_localstatus(char*, char*, char*) | 76 | unknown |
| `00100ccc` | Wmultiwindow_loadcolor(tagSPRT*) | 76 | unknown |
| `00100d18` | Wmultiwindow_loadcolor2(tagSPRT*) | 76 | unknown |
| `0011a494` | Wstatuskanjiprintwithptr(char*, COPYFIELD*, char*) | 76 | unknown |
| `00155d88` | active_worldwindow() | 76 | unknown |
| `0015a27c` | iOSPressArea() | 76 | unknown |
| `0015a2c8` | iOSTapArea() | 76 | unknown |
| `0015d178` | iOSstartLeftTurnSub(int) | 76 | unknown |
| `0015d1ec` | iOSstartRightTurnSub(int) | 76 | unknown |
| `0015ddf8` | iOSGT4_MapXYZ(unsigned long, long, long, long) | 76 | unknown |
| `00161d04` | iOSWldUnitTypeHelpSet(int) | 76 | unknown |
| `00173720` | cGetMesAdr(unsigned char*, short, int) | 76 | unknown |
| `0017442c` | cGetMaskedPad() | 76 | unknown |
| `00179e78` | bGetMesAdr(unsigned char*, short, int) | 76 | unknown |
| `0018854c` | eGetSortCondition(int, short*) | 76 | unknown |
| `0018e220` | eAllSttsDelete() | 76 | unknown |
| `0018ed9c` | eGetMesAdr(unsigned char*, short, int) | 76 | unknown |
| `00196108` | jGetMesAdr(unsigned char*, short, int) | 76 | unknown |
| `001a8028` | GetSortCondition(int, short*) | 76 | unknown |
| `001b672c` | GetMesAdr(unsigned char*, short, int) | 76 | unknown |
| `001baa78` | sys_warning(int, int) | 76 | unknown |
| `001cb064` | init_target_result(A_RESULT*) | 76 | unknown |
| `001d4cf4` | set_itemitem(int, unsigned char, unsigned char*) | 76 | unknown |
| `001d4fc8` | set_katanaitem(int, unsigned char, unsigned char*) | 76 | unknown |
| `001d50f0` | set_sanjutsuability2(int, unsigned char, short*) | 76 | unknown |
| `001d513c` | set_sanjutsuability1(int, unsigned char, short*) | 76 | unknown |
| `001e4dfc` | search_root_think(int, int, int, int, int, int, int, int, int, int*) | 76 | unknown |
| `001e4e48` | search_root_ev(int, int, int, int, int, int, int, int) | 76 | unknown |
| `001ef560` | requestDefaultFukidashi(tag_animation*) | 76 | unknown |
| `001ef5cc` | requestDefaultPosition(tag_animation*) | 76 | unknown |
| `001f0504` | resetTargetAnimation(tag_animation*) | 76 | unknown |
| `001feb0c` | rideOffChokoboS(tag_animation*) | 76 | unknown |
| `00200ae8` | startLeftTurnSub(int) | 76 | unknown |
| `00200b34` | startRightTurnSub(int) | 76 | unknown |
| `0020da7c` | popBackColor() | 76 | unknown |
| `0020e44c` | rideOnChokoboForced(int, int) | 76 | unknown |
| `0020ea90` | activateAnimation(int) | 76 | unknown |
| `0020efb8` | initializeAnimationLoadArea() | 76 | unknown |
| `00210320` | InitializeGame(int) | 76 | unknown |
| `00211414` | pspNetCheckAutoCommandPlayer() | 76 | unknown |
| `00212bb4` | requestDestinationGradationAsDefault(int, CVECTOR*) | 76 | unknown |
| `0021b570` | SeekEffect() | 76 | unknown |
| `002233f4` | GetLinearPos(VECTOR*, int, int, VECTOR*) | 76 | unknown |
| `00243a14` | deleteMessage() | 76 | unknown |
| `00247130` | ctlopentitle_main3() | 76 | unknown |
| `002496d0` | vOpn_key_repinit() | 76 | unknown |
| `0024aa60` | vOpnmess_put(int, int, _POINT, unsigned long*) | 76 | unknown |
| `00258f1c` | evt_gil_high() | 76 | unknown |
| `00258f68` | evt_gil_low() | 76 | unknown |
| `0025e888` | day_to_month(int, int*, int*) | 76 | unknown |
| `00263abc` | iOSNovelBrightOn() | 76 | unknown |
| `0026a5b0` | snpl_meswait() | 76 | unknown |
| `0026b694` | wldssd_wait() | 76 | unknown |
| `00270108` | wldmess_put(int, int, _POINT, unsigned long*) | 76 | unknown |
| `00270414` | defscrwin_set(int, int, _POINT*, _POINT*) | 76 | unknown |
| `0027bccc` | iOS_CMenuTouch::isInMenu(int, int) | 76 | unknown |
| `0028469c` | ForEachVector(VECTOR_DATABASE*, short) | 76 | unknown |
| `00285bac` | pspItemIsExist | 76 | unknown |
| `0028bb3c` | TE_task_killmyself() | 76 | unknown |
| `0028c6e0` | CFFT_STATE::WorldFaceIDToFaceID(int) | 76 | unknown |
| `0028d6a0` | tlSetMallocUserPointer(void**) | 76 | unknown |
| `0029ad6c` | xpSetDrawOffset | 76 | unknown |
| `0029ae00` | xpLibGetOffset(int*, int*) | 76 | unknown |
| `0029dbe8` | _gte_FlipTRX() | 76 | unknown |
| `002a257c` | RotNclip3_nom | 76 | unknown |
| `002b1b64` | AppEngine_IsExit() | 76 | unknown |
| `002c99b5` | operator new(unsigned int) | 76 | unknown |
| `00072918` | Java_com_square_1enix_FFT_1Android_GL2JNILib_setBatteryLevel | 72 | unknown |
| `0007744c` | gztell64 | 72 | unknown |
| `00077b38` | gzclearerr | 72 | unknown |
| `00079010` | gzputs | 72 | unknown |
| `000a6fec` | CGX_SCREEN_CORRECT::ScalingDiff(int, float, float) | 72 | unknown |
| `000a856c` | CEGL2_IF::AllocPacket(int, int) | 72 | unknown |
| `000a85b4` | CEGL2_IF::FreePacket(int) | 72 | unknown |
| `000a91dc` | CEGL2_IF::SetupSpriteCLUT() | 72 | unknown |
| `000aadb8` | CEGL2_FBO::End(int, int) | 72 | unknown |
| `000acab8` | CEGL2_SPRITE::Create(int, int) | 72 | unknown |
| `000b9878` | CSTR_UTIL::StrNLen(char*, int) | 72 | unknown |
| `000ba354` | CSOUND_IF::Resume() | 72 | unknown |
| `000ba7f0` | CSOUND_IF::GetMasterVolume(int*, int*, int*) | 72 | unknown |
| `000bb010` | CSOUND_IF::GetLoop(int) | 72 | unknown |
| `000bd474` | CSOUND_LOADER_OGG::Close() | 72 | unknown |
| `000bd4bc` | CSOUND_LOADER_OGG::~CSOUND_LOADER_OGG() | 72 | unknown |
| `000d9ac4` | request_maptest() | 72 | unknown |
| `001019c4` | Wrequest_maptest() | 72 | unknown |
| `00101f3c` | Wrecieve_statusinfo() | 72 | unknown |
| `00153278` | task_wait_fast(long) | 72 | unknown |
| `001533d8` | task_init() | 72 | unknown |
| `0015353c` | Wtask_wait_fast(long) | 72 | unknown |
| `0015369c` | Wtask_init() | 72 | unknown |
| `0015a438` | iOSBtlUnitMoveCheck() | 72 | unknown |
| `0015de44` | iOSGT4_MapXYZClear(unsigned long) | 72 | unknown |
| `0015ff40` | iOSJobRotStop() | 72 | unknown |
| `00160ea0` | iOSYajiEffectSetLR(short, short, short, short, int) | 72 | unknown |
| `00173a74` | cCountMessage(unsigned char*) | 72 | unknown |
| `00176e08` | bGetSortCondition(int, short*) | 72 | unknown |
| `00178740` | bFadeOutInit() | 72 | unknown |
| `001800f8` | bSetWindowPosition(int, int, int, short*) | 72 | unknown |
| `00199760` | CallGetAll2(int) | 72 | unknown |
| `001997a8` | CallGetEqp2(int) | 72 | unknown |
| `0019f750` | DrawFunds() | 72 | unknown |
| `001a93dc` | ChgShopStockItem(short, int) | 72 | unknown |
| `001b6ecc` | CountMessage(unsigned char*) | 72 | unknown |
| `001cb7fc` | check_reaction_deny2(BWORK*) | 72 | unknown |
| `001d189c` | Resume_MK_BSTR_Init() | 72 | unknown |
| `001d533c` | set_chargeability(int, unsigned char, short*) | 72 | unknown |
| `001d6ab0` | iOS_RESUME_SET_MAPADJ(IOS_RESUME_DATA_MAPADJ*, IOS_RESUME_DATACOPY_MODE) | 72 | unknown |
| `001d98c8` | check_status_data2(BWORK*, int) | 72 | unknown |
| `001ed644` | getAnimationHeightAddValue(tag_animation*, BLOCK*) | 72 | unknown |
| `001eed84` | getSequenceAddress(unsigned short) | 72 | unknown |
| `00201c5c` | resetTargetDirection(tag_animation*) | 72 | unknown |
| `00216984` | stopEffect(int) | 72 | unknown |
| `0021c154` | s22_addValue(_EffectTCB*) | 72 | unknown |
| `0021c19c` | s23_subValue(_EffectTCB*) | 72 | unknown |
| `0021c22c` | s6_setPersonalProc(_EffectTCB*) | 72 | unknown |
| `0021c3ec` | se_mapScale(_EffectTCB*) | 72 | unknown |
| `0021ebbc` | p05_reboundFunc() | 72 | unknown |
| `0022acc4` | AddSVECTORToSVECTORAnd0xfff(SVECTOR*, SVECTOR*, SVECTOR*) | 72 | unknown |
| `00242450` | vEnd_ctlinit() | 72 | unknown |
| `00248e24` | vEnd_exit() | 72 | unknown |
| `00249a38` | vOpn_month2day(int, int) | 72 | unknown |
| `00259224` | evt_flag() | 72 | unknown |
| `0025926c` | evt_flag_high() | 72 | unknown |
| `002592b4` | evt_flag_low() | 72 | unknown |
| `002594a0` | evt_brave_high() | 72 | unknown |
| `002594e8` | evt_brave_low() | 72 | unknown |
| `00259530` | evt_faith_high() | 72 | unknown |
| `00259578` | evt_faith_low() | 72 | unknown |
| `0025e840` | month_to_day(int, int) | 72 | unknown |
| `0026a234` | snpl_fadeout() | 72 | unknown |
| `0026b64c` | wldmusic_change(int) | 72 | unknown |
| `0027bb20` | iOS_CMenuTouch::isInRect(RECT16*, int, int) | 72 | unknown |
| `0027d420` | setCancelDisableArea(int, int, int, int, int) | 72 | unknown |
| `0027d7c0` | iOS_CMenuTouchNum::isInRect(RECT16*, int, int) | 72 | unknown |
| `0027e390` | iOS_CMenuTouchSaveLoad::isInRect(RECT16*, int, int) | 72 | unknown |
| `00282288` | iOS_disableClipFT4_getCliped() | 72 | unknown |
| `0028464c` | delete_Vector(VECTOR_DATABASE*, short) | 72 | unknown |
| `00284f88` | pspBattleEntryAreaInit() | 72 | unknown |
| `0028674c` | get_movie_filename(int) | 72 | unknown |
| `00287148` | pspNetSetKeepAnimationData() | 72 | unknown |
| `00287204` | pspNetTrapReturnStatus() | 72 | unknown |
| `00289898` | pspSaveInit() | 72 | unknown |
| `0028baf4` | TE_task_get_no() | 72 | unknown |
| `0028dd2c` | CloseEvent | 72 | unknown |
| `00291a9c` | xpLibgpuFilterSet | 72 | unknown |
| `0029a9dc` | LoadClut2 | 72 | unknown |
| `0029b5d0` | GsSwapDispBuff | 72 | unknown |
| `0029d0d8` | _gte_ldtr(long, long, long) | 72 | unknown |
| `0029e9c8` | _gte_ll() | 72 | unknown |
| `0029ec84` | _gte_llv0tr() | 72 | unknown |
| `0029ecd0` | _gte_llv1tr() | 72 | unknown |
| `0029ed1c` | _gte_llv2tr() | 72 | unknown |
| `0029ed68` | _gte_llirtr() | 72 | unknown |
| `0029edb4` | _gte_llv0bk() | 72 | unknown |
| `0029ee00` | _gte_llv1bk() | 72 | unknown |
| `0029ee4c` | _gte_llv2bk() | 72 | unknown |
| `0029ee98` | _gte_llirbk() | 72 | unknown |
| `0029f224` | _gte_lcv0tr() | 72 | unknown |
| `0029f270` | _gte_lcv1tr() | 72 | unknown |
| `0029f2bc` | _gte_lcv2tr() | 72 | unknown |
| `0029f308` | _gte_lcirtr() | 72 | unknown |
| `0029f354` | _gte_lcv0bk() | 72 | unknown |
| `0029f3a0` | _gte_lc() | 72 | unknown |
| `0029f3ec` | _gte_lcv1bk() | 72 | unknown |
| `0029f438` | _gte_lcv2bk() | 72 | unknown |
| `0029f484` | _gte_lcirbk() | 72 | unknown |
| `002a2018` | RotAverage3_nom | 72 | unknown |
| `002a2678` | set_trans_matrix(long, long, long) | 72 | unknown |
| `002a3068` | xpMalloc | 72 | unknown |
| `002b3258` | musicPlayer_Pause() | 72 | unknown |
| `002b32a0` | musicPlayer_Replay() | 72 | unknown |
| `002b748c` | isInRectUi(_RECT_UI*, int, int) | 72 | unknown |
| `002b8750` | iOS_isMovedDist() | 72 | unknown |
| `000812fc` | unzOpen2 | 68 | unknown |
| `000816d4` | unzGoToFilePos | 68 | unknown |
| `00081c58` | unzClose | 68 | unknown |
| `000910e4` | mdct_clear | 68 | unknown |
| `00097c00` | _float32_unpack | 68 | unknown |
| `000a8684` | CEGL2_IF::AddSprite(int, CEGL2_SPRITE*, float, float, _EGL_SPRITE_LAYOUT*, unsigned char) | 68 | unknown |
| `000b9b4c` | CSTR_UTIL::GetHashValue(char*) | 68 | unknown |
| `000ba310` | CSOUND_IF::Suspend() | 68 | unknown |
| `000ba4d8` | CSOUND_IF::RegisterSavedata(int, _SOUND_SAVEDATA*, unsigned char) | 68 | unknown |
| `000bb9b4` | CSOUND_IF_SL::IsPlaying(int) | 68 | unknown |
| `000bbb28` | CSOUND_IF_SL::GetPosition(int, unsigned int*) | 68 | unknown |
| `000bd1dc` | COggMemMapFile::CallbackRead(void*, unsigned int, unsigned int, void*) | 68 | unknown |
| `000bd334` | CSOUND_LOADER_OGG::Seek(unsigned long) | 68 | unknown |
| `000be0b8` | CSTEP::InitFromCurrentF(float, int, int, unsigned int) | 68 | unknown |
| `000d8880` | pushmessagepacket() | 68 | unknown |
| `000da558` | event_start() | 68 | unknown |
| `00100550` | Wpushmessagepacket() | 68 | unknown |
| `0010f9c0` | Wloadcsrc(int, int, int, int) | 68 | unknown |
| `0015ce30` | iOSMapCurModeSet_SLIDE() | 68 | unknown |
| `0017b3dc` | bMenuSelSideWithSnd(unsigned short, unsigned char, unsigned long, int) | 68 | unknown |
| `0018fac0` | eMenuSelVerticalWithSnd(unsigned short, unsigned char, unsigned long, int) | 68 | unknown |
| `0018fbcc` | eMenuSelSideWithSnd(unsigned short, unsigned char, unsigned long, int) | 68 | unknown |
| `0019d7a4` | DrawPrice() | 68 | unknown |
| `001ab7e0` | IsUntauchableAbility(int) | 68 | unknown |
| `001b7bac` | MenuSelVerticalWithSnd(unsigned short, unsigned char, unsigned long, int) | 68 | unknown |
| `001b7ce4` | MenuSelSideWithSnd(unsigned short, unsigned char, unsigned long, int) | 68 | unknown |
| `001cab08` | clear_addeffect() | 68 | unknown |
| `001cd16c` | get_weatherdata() | 68 | unknown |
| `001cec5c` | setCasterDirection(int, unsigned char) | 68 | unknown |
| `001dc408` | set_temp_status(BWORK*, int, unsigned char, int) | 68 | unknown |
| `001e0384` | check_chokobo(BWORK*) | 68 | unknown |
| `001e207c` | getskilldata(int) | 68 | unknown |
| `001eabe4` | searchAnimationByPosition(int, int, int) | 68 | unknown |
| `001f37e4` | ExecuteAnimations() | 68 | unknown |
| `001f6d4c` | resetCharacterPanelPosition(tag_animation*) | 68 | unknown |
| `001fd850` | requestPhysicalDamageFromBattleID(int, int) | 68 | unknown |
| `001fd894` | requestPhysicalDamage(int, int) | 68 | unknown |
| `002016c4` | reserveCharacterPosition(tag_animation*) | 68 | unknown |
| `00204210` | iOS_isCursorOnUnit() | 68 | unknown |
| `0020cf78` | fileReadPC(char*, void*) | 68 | unknown |
| `0020e7fc` | getBattleWorkIDFromAnimation(unsigned int) | 68 | unknown |
| `00210960` | MenuTest() | 68 | unknown |
| `00216414` | readMusicBlock(int) | 68 | unknown |
| `00216618` | effectFadeoutMusic(int, int) | 68 | unknown |
| `00216740` | tempoMusic(int, int) | 68 | unknown |
| `00216784` | pitchMusic(int, int) | 68 | unknown |
| `002167c8` | panpotMusic(int, int) | 68 | unknown |
| `0021c0cc` | s20_countUp(_EffectTCB*) | 68 | unknown |
| `0021c110` | s21_countDown(_EffectTCB*) | 68 | unknown |
| `0022a5d0` | efrand(int, int) | 68 | unknown |
| `00242618` | ctlendmov_main(CTLINFO*) | 68 | unknown |
| `0024a068` | vOpn_pacloop() | 68 | unknown |
| `00258fb4` | evt_dead_high() | 68 | unknown |
| `00258ff8` | evt_dead_low() | 68 | unknown |
| `00268b9c` | wldcenter_calc(SVECTOR*, VECTOR*) | 68 | unknown |
| `00269c3c` | snpl_mesput3() | 68 | unknown |
| `0026b6e0` | iOSwldssd_wait() | 68 | unknown |
| `002706c8` | pageanmpac_reset(int, int, int) | 68 | unknown |
| `00273864` | GetDestinationRange() | 68 | unknown |
| `00277640` | SetThisDestination(unsigned char*) | 68 | unknown |
| `00285574` | pspItemGetEquipBonus | 68 | unknown |
| `00291348` | GetTPage | 68 | unknown |
| `0029a858` | SetDefDispEnv | 68 | unknown |
| `0029fef0` | ratan2 | 68 | unknown |
| `002a0878` | PushMatrix | 68 | unknown |
| `002a08bc` | PopMatrix | 68 | unknown |
| `002a1e70` | RotAverageNclip3 | 68 | unknown |
| `002a2d00` | xpLibSN::Fd2Idx(int) | 68 | unknown |
| `002b1b20` | AppEngine_Resume() | 68 | unknown |
| `002b2b38` | SysSE_Stop(int) | 68 | unknown |
| `002b758c` | IS_ICON_AREA(int) | 68 | unknown |
| `002cb9ec` | __aeabi_d2lz | 68 | unknown |
| `0007a720` | inflateBackEnd | 64 | unknown |
| `0007cf18` | inflateSyncPoint | 64 | unknown |
| `00080918` | unzGetCurrentFileInfo64 | 64 | unknown |
| `00083284` | ogg_page_packets | 64 | unknown |
| `000a5d50` | CG2D_LOADER_TGA::TGA_LoadMemory(unsigned char*) | 64 | unknown |
| `000b3780` | CINPUT_DATA::SetDown(int, int, int) | 64 | unknown |
| `000b38a4` | CINPUT_DATA::SetDelayDown(int, int, int) | 64 | unknown |
| `000b41ec` | CINPUT_IF_TOUCH::GetTouchCount() | 64 | unknown |
| `000b6770` | CFILE::Write(void*, unsigned int, unsigned int) | 64 | unknown |
| `000b93ec` | CSTR_UTIL::ToStr(char*, char*) | 64 | unknown |
| `000b9f04` | CTHREAD::CreateAndRegister(int, unsigned int (*)(void*), void*) | 64 | unknown |
| `000b9fe0` | timeGetTime() | 64 | unknown |
| `000bb520` | CSOUND_IF::GetSoundType(int) | 64 | unknown |
| `000d7ae4` | addstatusback(STTSWINDOWBACK*) | 64 | unknown |
| `000d9a80` | send_sttslinecol(char*) | 64 | unknown |
| `000d9eec` | extend_endornot() | 64 | unknown |
| `000f1560` | disp_resume_yesno() | 64 | unknown |
| `000fb554` | chkMessagepacket() | 64 | unknown |
| `000feffc` | Wallocatetextureinit() | 64 | unknown |
| `000ff6d8` | Waddstatusback(STTSWINDOWBACK*) | 64 | unknown |
| `00101ba8` | Wextend_endornot() | 64 | unknown |
| `0010212c` | Wevent_start() | 64 | unknown |
| `00102684` | Wcheckpara1(int) | 64 | unknown |
| `0010634c` | Wdisp_resume_yesno() | 64 | unknown |
| `00153398` | task_killmyself() | 64 | unknown |
| `0015365c` | Wtask_killmyself() | 64 | unknown |
| `00155cac` | world_stopnoend(int) | 64 | unknown |
| `0015b2e8` | iOSSlidOkCheck() | 64 | unknown |
| `0015d9e0` | iOSTchCurLimit(int) | 64 | unknown |
| `0016f7b8` | ASHURA_clearOT() | 64 | unknown |
| `00176eec` | bGetJobNumber(int) | 64 | unknown |
| `00187618` | GetLocalJobNumber(short) | 64 | unknown |
| `001a3edc` | CallGetSellItemPrice(int) | 64 | unknown |
| `001a8224` | GetJobNumber(int) | 64 | unknown |
| `001adea0` | GetItemPos(int) | 64 | unknown |
| `001cd12c` | reset_calcmode_think() | 64 | unknown |
| `001d584c` | get_turn_unit(int) | 64 | unknown |
| `001d94b0` | adjust_joblevel(unsigned short*, unsigned char*) | 64 | unknown |
| `001e7420` | iOS_AddClearItem() | 64 | unknown |
| `001eb074` | countCrystalAnimation() | 64 | unknown |
| `001eb794` | iOSmyGetShapePrim() | 64 | unknown |
| `001ef998` | requestCast0Animation(tag_animation*) | 64 | unknown |
| `0020cbe8` | fileOpenForSndCD(unsigned long, unsigned long) | 64 | unknown |
| `0020cc28` | fileOpenBBCD(unsigned long, unsigned long) | 64 | unknown |
| `0020dad8` | setBackColor(unsigned char, unsigned char, unsigned char) | 64 | unknown |
| `0020dc1c` | requestAnimationForAll(unsigned int) | 64 | unknown |
| `0020e840` | getAnimationIDFormBattleWork(int) | 64 | unknown |
| `0020e880` | getFontIDFormBattleWork(int) | 64 | unknown |
| `0020ef78` | inactivateCompressedAnimation(int) | 64 | unknown |
| `0021665c` | effectFadeinMusic(int) | 64 | unknown |
| `0021b34c` | SetEffectMSQLPtr(short) | 64 | unknown |
| `0021bd20` | s5_setSequenceID(_EffectTCB*) | 64 | unknown |
| `0021bd60` | s10_setValue(_EffectTCB*) | 64 | unknown |
| `0021bda0` | s11_ifEQU(_EffectTCB*) | 64 | unknown |
| `0021bde0` | s12_ifGE(_EffectTCB*) | 64 | unknown |
| `0021be20` | s13_ifGT(_EffectTCB*) | 64 | unknown |
| `0021be60` | s14_ifLE(_EffectTCB*) | 64 | unknown |
| `0021bea0` | s15_ifLT(_EffectTCB*) | 64 | unknown |
| `0021c04c` | s1c_ifNotEQU(_EffectTCB*) | 64 | unknown |
| `0021c08c` | s1f_ifNumTargetEQU(_EffectTCB*) | 64 | unknown |
| `0021c644` | s26_createObjectWithTable(_EffectTCB*) | 64 | unknown |
| `0021c684` | s27_setEnvironmentWithTable(_EffectTCB*) | 64 | unknown |
| `0021cbd0` | s1d_ifScheduleEnd(_EffectTCB*) | 64 | unknown |
| `0024552c` | cdxa_stop() | 64 | unknown |
| `00249278` | vOpn_init(int) | 64 | unknown |
| `00249a80` | vOpn_SetCDVolume(int, int) | 64 | unknown |
| `00259460` | get_ramza_savework() | 64 | unknown |
| `0025ee30` | wldload_wait() | 64 | unknown |
| `00269b80` | snpl_keywait() | 64 | unknown |
| `0026a570` | snpl_fadewait() | 64 | unknown |
| `0026ebf0` | ctlsentuto_active(CTLINFO*) | 64 | unknown |
| `00273b38` | SetSafePanelAhead(int) | 64 | unknown |
| `00278440` | GetPanelUnderUnit(int, unsigned char*) | 64 | unknown |
| `0027bb68` | iOS_CMenuTouch::isCanUp(int*, int*) | 64 | unknown |
| `002844b8` | VectorIsEqual(SVECTOR const*, SVECTOR const*) | 64 | unknown |
| `00285044` | pspBattleEntryAreaCellDataGet(int, int, short) | 64 | unknown |
| `00285c84` | pspItemGetWeaponClut | 64 | unknown |
| `0028b080` | pspWorldCallBackExec() | 64 | unknown |
| `0028be80` | _ps_test() | 64 | unknown |
| `0029ca68` | _gte_ldv3(SVECTOR*, SVECTOR*, SVECTOR*) | 64 | unknown |
| `0029caa8` | _gte_ldv3c(SVECTOR*) | 64 | unknown |
| `0029cae8` | _gte_ldv3c_vertc(VERTC*) | 64 | unknown |
| `0029da88` | _gte_subdvl(DVECTOR*, DVECTOR*, VECTOR*) | 64 | unknown |
| `0029db04` | _gte_adddvl(DVECTOR*, DVECTOR*, VECTOR*) | 64 | unknown |
| `0029dee0` | _gte_rtpt() | 64 | unknown |
| `0029f918` | _gte_nct() | 64 | unknown |
| `0029fa0c` | _gte_ncdt() | 64 | unknown |
| `0029fac4` | _gte_ncct() | 64 | unknown |
| `0029fcb8` | _gte_avsz4() | 64 | unknown |
| `002a0aa0` | ApplyRotMatrixLV | 64 | unknown |
| `002a1bbc` | RotTransPers | 64 | unknown |
| `002a3028` | xpFree | 64 | unknown |
| `002b8888` | iOS_InitMovie(int) | 64 | unknown |
| `002c5340` | GX_GetScreenW_1X() | 64 | unknown |
| `002c5380` | GX_GetScreenH_1X() | 64 | unknown |
| `002cab9c` | __aeabi_f2d | 64 | unknown |
| `002cde9c` | __gnu_unwind_frame | 64 | unknown |
| `0007cd9c` | inflateGetHeader | 60 | unknown |
| `0007d914` | call_ztell64 | 60 | unknown |
| `00083df8` | ogg_sync_wrote | 60 | unknown |
| `0009403c` | _vp_global_look | 60 | unknown |
| `000a1d00` | CG2D_LOADER::CG2D_LOADER(int) | 60 | unknown |
| `000a2828` | CG2D_LOADER::GetImageFormatFormat(int) | 60 | unknown |
| `000a6d60` | CGX_SCREEN_CORRECT::SetEnable(int) | 60 | unknown |
| `000a72bc` | CGX_SCREEN_CORRECT::Area_GetCorrect(int, float*, float*, float*, float*) | 60 | unknown |
| `000a7414` | CGX_SCREEN_CORRECT::Area_ToScreenX(int, int) | 60 | unknown |
| `000a74d8` | CGX_SCREEN_CORRECT::Area_X_AlignC(int, int) | 60 | unknown |
| `000a8648` | CEGL2_IF::AddSprite(int, CEGL2_SPRITE*, float, float, unsigned char) | 60 | unknown |
| `000ab8e8` | CEGL2_SHADER::SetTexture(int) | 60 | unknown |
| `000ab9cc` | CEGL2_SHADER::CEGL2_SHADER() | 60 | unknown |
| `000abb88` | std::priv::_Rb_tree<int, std::less<int>, std::pair<int const, CEGL2_SHADER::DATA_SHADER>, std::priv::_Select1st<std::pair<int const, CEGL2_SHADER::DATA_SHADER> >, std::priv::_MapTraitsT<std::pair<int const, CEGL2_SHADER::DATA_SHADER> >, std::allocator<std::pair<int const, CEGL2_SHADER::DATA_SHADER> > >::_M_erase(std::priv::_Rb_tree_node_base*) | 60 | unknown |
| `000af4d0` | CEGL2_TEX_HYBRID::GL_UnloadAll() | 60 | unknown |
| `000b52a0` | CRECT::SetRect(int, _RECT_S32*) | 60 | unknown |
| `000b52dc` | CRECT::SetRect16(int, _RECT_S16*) | 60 | unknown |
| `000b8a98` | CLIST::GetNode(int) | 60 | unknown |
| `000bb124` | CSOUND_IF::GetPlaySec(int) | 60 | unknown |
| `000bb350` | CSOUND_IF::GetBufferType(int) | 60 | unknown |
| `000bcdc4` | CSOUND_LOADER_PCM::Close() | 60 | unknown |
| `000bce00` | CSOUND_LOADER_PCM::~CSOUND_LOADER_PCM() | 60 | unknown |
| `000bd414` | COggMemMapFile::Close() | 60 | unknown |
| `000bdd9c` | CSTEP::GetEnd() | 60 | unknown |
| `000be0fc` | CSTEP::GetData() | 60 | unknown |
| `000d6f18` | initsprtfield(tagSPRT*, int, int) | 60 | unknown |
| `000d745c` | allocatetextureinit() | 60 | unknown |
| `000fea3c` | Winitsprtfield(tagSPRT*, int, int) | 60 | unknown |
| `00101980` | Wsend_sttslinecol(char*) | 60 | unknown |
| `001534a4` | send_taskparamater4(long, long, long, long, long) | 60 | unknown |
| `00153768` | Wsend_taskparamater4(long, long, long, long, long) | 60 | unknown |
| `001538e0` | iOS_setDefaultOption() | 60 | unknown |
| `00155e04` | changewindowamb(int, int, int) | 60 | unknown |
| `0015a5b0` | iOSSlideNaviCurDyGet() | 60 | unknown |
| `0015b5c8` | iOSMapCursorModeGet() | 60 | unknown |
| `0015e768` | iOSShiftUnitSet(int) | 60 | unknown |
| `00160f18` | iOSYajiEffectSetTGABase(int, short, short) | 60 | unknown |
| `0016f738` | iOS_cacheFilesNameClear() | 60 | unknown |
| `0017b420` | bMenuSelSideWithSndDirect(unsigned short, unsigned char, int, int) | 60 | unknown |
| `0018e3b4` | eWindowPositionInit() | 60 | unknown |
| `0018eac0` | eSetWindowPosition(int, int, int, short*) | 60 | unknown |
| `0018fc10` | eMenuSelSideWithSndDirect(unsigned short, unsigned char, int, int) | 60 | unknown |
| `001958d4` | jWindowPositionInit() | 60 | unknown |
| `00195e78` | jSetWindowPosition(int, int, int, short*) | 60 | unknown |
| `001a7368` | IsDismiss(short) | 60 | unknown |
| `001a7a48` | SetChrList() | 60 | unknown |
| `001b6fc4` | GetFontCode(unsigned char*, short, int) | 60 | unknown |
| `001b7bf0` | MenuSelVerticalWithSndDirect(unsigned short, unsigned char, int, int) | 60 | unknown |
| `001b7d28` | MenuSelSideWithSndDirect(unsigned short, unsigned char, int, int) | 60 | unknown |
| `001bad60` | iOSUnitModeItem_Abi() | 60 | unknown |
| `001c713c` | DrawWindow2(unsigned char*, unsigned long, int) | 60 | unknown |
| `001c7178` | SelectWindowClutEx(int, int) | 60 | unknown |
| `001ca97c` | overlayMonomaneStack() | 60 | unknown |
| `001d2994` | iOS_get_bwork_no(BWORK*) | 60 | unknown |
| `001d3d5c` | get_active_unit() | 60 | unknown |
| `001d45c4` | check_turn_frozen(BWORK*) | 60 | unknown |
| `001ee100` | initializeImage(tag_animation*) | 60 | unknown |
| `00202f20` | set_direction_sub(tag_animation*, int) | 60 | unknown |
| `00213e0c` | stopColorRotation(unsigned int) | 60 | unknown |
| `002164f4` | inactivateMusic() | 60 | unknown |
| `0022a2ec` | getSmooth(int, int, int, int) | 60 | unknown |
| `0022aa0c` | AddVECTORToVECTOR(VECTOR*, VECTOR*, VECTOR*) | 60 | unknown |
| `0022aa48` | AddSVECTORToSVECTOR(SVECTOR*, SVECTOR*, SVECTOR*) | 60 | unknown |
| `0022aa84` | AddSVECTORToVECTOR(SVECTOR*, VECTOR*, VECTOR*) | 60 | unknown |
| `0022ad4c` | Add1Shougen(VECTOR*, VECTOR*, SVECTOR*) | 60 | unknown |
| `0022adbc` | Add3Shougen(VECTOR*, VECTOR*, SVECTOR*) | 60 | unknown |
| `0022adf8` | Add4Shougen(VECTOR*, VECTOR*, SVECTOR*) | 60 | unknown |
| `002431b4` | fRoll_fadein(short*) | 60 | unknown |
| `002431f0` | fRoll_fadeout(short*) | 60 | unknown |
| `00244938` | numword_chk(int) | 60 | unknown |
| `00249bcc` | vOpn_loadwait() | 60 | unknown |
| `00249c08` | vOpn_CdRead(CDREC*, int, int, unsigned long*) | 60 | unknown |
| `0026a3d0` | snpl_wordcol() | 60 | unknown |
| `0026ab70` | snpl_envsndreq() | 60 | unknown |
| `0027ce14` | iOS_CMenuTouch::isTaped() | 60 | unknown |
| `0027d950` | iOS_CMenuTouchNum::addNum(int*, int) | 60 | unknown |
| `002819cc` | iOS_v2menuInit() | 60 | unknown |
| `002822d0` | iOS_disableClipFT3_getCliped() | 60 | unknown |
| `00283ed8` | GLIVON_FT4(unsigned long*, tagPOLY_GT4*, short, unsigned long*, unsigned short*) | 60 | unknown |
| `00283f14` | GLIVON_FT3(unsigned long*, tagPOLY_GT3*, short, unsigned long*, unsigned short*) | 60 | unknown |
| `002842d8` | VectorDataBase(unsigned int) | 60 | unknown |
| `00284748` | VectorDataBase_SetFlag(VECTOR_DATABASE*, short) | 60 | unknown |
| `00284784` | ColorVectorDataBase(unsigned int) | 60 | unknown |
| `00284ccc` | pspBattleDataPadGet() | 60 | unknown |
| `0028551c` | pspItemGetCommonData | 60 | unknown |
| `002870f0` | pspNetTrapInitTable() | 60 | unknown |
| `00289844` | pspClearSaveData() | 60 | unknown |
| `0028af88` | __bpResetBinpackData | 60 | unknown |
| `0028afdc` | __bpGetAllBinarySize | 60 | unknown |
| `0028b6fc` | STEP_DISP(char const*) | 60 | unknown |
| `0028bf7c` | _ps_cond() | 60 | unknown |
| `0028c72c` | CFFT_STATE::AttackTeamFaceIDToFaceID(int, int*) | 60 | unknown |
| `0029b618` | iOSGsSwapDispBuff() | 60 | unknown |
| `0029dac8` | _gte_subdvd(DVECTOR*, DVECTOR*, DVECTOR*) | 60 | unknown |
| `0029db44` | _gte_adddvd(DVECTOR*, DVECTOR*, DVECTOR*) | 60 | unknown |
| `0029fc78` | _gte_avsz3() | 60 | unknown |
| `002a1838` | RotTransPers4_nom | 60 | unknown |
| `002a338c` | pspSaveBase::TitleIdSet(char const*) | 60 | unknown |
| `002ab5cc` | GuEmu_Clear() | 60 | unknown |
| `002b6fe0` | iOSReleaseButtonAreaCheck() | 60 | unknown |
| `002ca195` | __cxa_begin_cleanup | 60 | unknown |
| `000724b0` | _JNIEnv::NewObject(_jclass*, _jmethodID*, ...) | 56 | unknown |
| `00072638` | _JNIEnv::CallStaticObjectMethod(_jclass*, _jmethodID*, ...) | 56 | unknown |
| `00072670` | _JNIEnv::CallStaticIntMethod(_jclass*, _jmethodID*, ...) | 56 | unknown |
| `000726a8` | _JNIEnv::CallStaticVoidMethod(_jclass*, _jmethodID*, ...) | 56 | unknown |
| `00075890` | deflateTune | 56 | unknown |
| `00082414` | oggpack_writeinit | 56 | unknown |
| `00083b68` | ogg_stream_packetin | 56 | unknown |
| `00085fa8` | vorbis_synthesis_init | 56 | unknown |
| `000a1264` | ov_read | 56 | unknown |
| `000a4ec0` | CG2D_LOADER_TGA::GetSavePixelFormatOverwrite(_G2D_FORMAT*, int) | 56 | unknown |
| `000a7450` | CGX_SCREEN_CORRECT::Area_ToScreenY(int, int) | 56 | unknown |
| `000a9154` | CEGL2_IF::CLUT_FindFree(int) | 56 | unknown |
| `000ace30` | CEGL2_SPRITE::OnSuspend() | 56 | unknown |
| `000b35ac` | CINPUT_DATA::SetKeyWait(int, int, unsigned int, unsigned int) | 56 | unknown |
| `000b461c` | CINPUT_IF_TOUCH::DeleteDevice(int) | 56 | unknown |
| `000b6e38` | CFILE_DAT::Decrypt(int, unsigned int) | 56 | unknown |
| `000b9f44` | CTHREAD::Sync() | 56 | unknown |
| `000bb890` | CSOUND_IF_SL::StopAll() | 56 | unknown |
| `000bb944` | CSOUND_IF_SL::EngineSuspend() | 56 | unknown |
| `000bb97c` | CSOUND_IF_SL::EngineResume() | 56 | unknown |
| `000bcba0` | CSOUND_IF_SL::UnloadAll() | 56 | unknown |
| `000bdae0` | CFRAMERATE::GetRate() | 56 | unknown |
| `000be3ac` | CSTEP_BATCH::SetStage(int) | 56 | unknown |
| `000be3e4` | CSTEP_BATCH::FinishStage(int) | 56 | unknown |
| `000d7ed8` | getvaluelength(int) | 56 | unknown |
| `000d86d8` | getanimpos3d(int, short*) | 56 | unknown |
| `000d8740` | checkstatusscroll(int) | 56 | unknown |
| `000d88c4` | popmessagepacket() | 56 | unknown |
| `000d90a8` | multiwindow_packetdefload(COMRECORD*, tagSPRT*, int) | 56 | unknown |
| `000e0f68` | loadcsrc(int, int, int, int) | 56 | unknown |
| `000e8010` | iOS_clearFLAGeventdirect() | 56 | unknown |
| `000e8048` | iOS_clearFLAGmonsentry() | 56 | unknown |
| `000ffac4` | Wgetvaluelength(int) | 56 | unknown |
| `001003ac` | Wgetanimpos3d(int, short*) | 56 | unknown |
| `00100414` | Wcheckstatusscroll(int) | 56 | unknown |
| `00100594` | Wpopmessagepacket() | 56 | unknown |
| `00100ec0` | Wmultiwindow_packetdefload(COMRECORD*, tagSPRT*, int) | 56 | unknown |
| `001534e0` | taskActiveCheck() | 56 | unknown |
| `001537a4` | WtaskActiveCheck() | 56 | unknown |
| `0015aca8` | iOSRotSetupAfterX() | 56 | unknown |
| `0015ace0` | iOSRotSetupAfterY() | 56 | unknown |
| `0015d67c` | iOSUnitGetPos(unsigned char*, unsigned char*) | 56 | unknown |
| `001615a4` | iOSSdNovelSelectClear() | 56 | unknown |
| `00174478` | cClearPadData() | 56 | unknown |
| `00176f2c` | bGetSpecialJob(short) | 56 | unknown |
| `0017b45c` | bClearPadData() | 56 | unknown |
| `00188598` | eSetSortCondition(int, short*) | 56 | unknown |
| `0018fc4c` | eClearPadData() | 56 | unknown |
| `0019f718` | iOSShopHelpStatusCheck() | 56 | unknown |
| `001a8074` | SetSortCondition(int, short*) | 56 | unknown |
| `001a8264` | GetSpecialJob(short) | 56 | unknown |
| `001b7eb8` | ClearPadData() | 56 | unknown |
| `001c03a8` | DrawSingleUnit(short) | 56 | unknown |
| `001c042c` | SetWindowPosition(int, int, int, short*) | 56 | unknown |
| `001cec24` | copy_target_table2(unsigned char*) | 56 | unknown |
| `001ceca0` | _rand_() | 56 | unknown |
| `001d1ce8` | erase_unit_f(int) | 56 | unknown |
| `001d3d24` | gc_bwp(int) | 56 | unknown |
| `001e31b8` | get_unit_jl(BWORK*, int, int*) | 56 | unknown |
| `001eb03c` | searchAnimationByBattleID(unsigned short) | 56 | unknown |
| `001f5f44` | iOS_resetAnimationIrowake() | 56 | unknown |
| `001f5f7c` | iOS_getClutOffs(int) | 56 | unknown |
| `00200b80` | endTrunAction() | 56 | unknown |
| `0020c114` | iOS_GaryutenseiCheck() | 56 | unknown |
| `0020e12c` | getAnimationSum() | 56 | unknown |
| `0020e8dc` | checkCharacterMove(int) | 56 | unknown |
| `0020ee10` | disposeEventAnimation(int) | 56 | unknown |
| `0021b0d0` | InitEffectLoadAddress() | 56 | unknown |
| `0021b4a8` | GetSQLFrameRate(_EffectTCB*) | 56 | unknown |
| `0021bfdc` | s1a_ifChildTaskExist(_EffectTCB*) | 56 | unknown |
| `0021c014` | s1b_ifChildTaskNonExist(_EffectTCB*) | 56 | unknown |
| `0021ce78` | IsPermanentEffect(long) | 56 | unknown |
| `002210c4` | ConvertEffectAttribute(int) | 56 | unknown |
| `0022a328` | getSmoothSVECCosPai(SVECTOR*, SVECTOR*, int, int, SVECTOR*) | 56 | unknown |
| `0022a360` | getSmoothSVECCos2Pai(SVECTOR*, SVECTOR*, int, int, SVECTOR*) | 56 | unknown |
| `0022a3cc` | getSmoothVECCosPai(VECTOR*, VECTOR*, int, int, VECTOR*) | 56 | unknown |
| `0022a404` | getSmoothVECCos2Pai(VECTOR*, VECTOR*, int, int, VECTOR*) | 56 | unknown |
| `00254170` | iOSMapNaviCurSet(unsigned long) | 56 | unknown |
| `002558b8` | iOSWld_HelpTerget() | 56 | unknown |
| `00258c40` | evt_wldinfo() | 56 | unknown |
| `0025ee70` | wldCdRead(CDREC*, int, int, int, unsigned long*) | 56 | unknown |
| `00269a68` | snpl_hidepara() | 56 | unknown |
| `00269cd0` | snpl_setstat() | 56 | unknown |
| `00269d08` | snpl_clrstat() | 56 | unknown |
| `00269d40` | snpl_setlocal() | 56 | unknown |
| `00269d78` | snpl_clrlocal() | 56 | unknown |
| `0026a824` | snpl_snsndreq() | 56 | unknown |
| `00279c88` | MemClearDW(int*, int) | 56 | unknown |
| `0027b4a4` | initCmdKind() | 56 | unknown |
| `0027fc80` | cSaveFFT::Destroy() | 56 | unknown |
| `00280558` | iOS_fftLoad(int) | 56 | unknown |
| `002843b4` | VectorDataBaseContainer_ClearFlags(VECTOR_DATABASE_CONTAINER*) | 56 | unknown |
| `00285bf8` | pspItemIsType | 56 | unknown |
| `00285f4c` | pspFileManager::hockSeek(int) | 56 | unknown |
| `00286cc0` | pspNetEntranceMissionStateInit() | 56 | unknown |
| `00287a40` | load_hight_font() | 56 | unknown |
| `0028c288` | CFFT_STATE::GetBackdropColor(float*, float*, float*) | 56 | unknown |
| `0028c5d4` | CFFT_STATE::Suspend(_FFT_STATE_RESUME*) | 56 | unknown |
| `0028c60c` | CFFT_STATE::Resume(_FFT_STATE_RESUME*) | 56 | unknown |
| `0028da58` | tlDumpHeap() | 56 | unknown |
| `0028daac` | tlGetHeapSize() | 56 | unknown |
| `002918b4` | SetDrawStp | 56 | unknown |
| `0029aa84` | OpenTIM | 56 | unknown |
| `0029cff0` | _gte_SetLightMatrix(MATRIX*) | 56 | unknown |
| `0029d048` | _gte_SetColorMatrix(MATRIX*) | 56 | unknown |
| `0029d5ac` | _gte_stsz4(long*, long*, long*, long*) | 56 | unknown |
| `0029f5b4` | _gte_dpct() | 56 | unknown |
| `0029f6f4` | _gte_sqr0() | 56 | unknown |
| `0029ff5c` | PSX_csqrt | 56 | unknown |
| `002a1594` | DpqColor3 | 56 | unknown |
| `002a193c` | NormalColorDpq3 | 56 | unknown |
| `002a1a14` | read_sz_fifo4(long*, long*, long*, long*) | 56 | unknown |
| `002a2f60` | PCopen | 56 | unknown |
| `002a3308` | pspSaveAuto::getUtilSize() | 56 | unknown |
| `002a3870` | pspSaveList::FocusSet() | 56 | unknown |
| `002b88c8` | iOS_StartMovie() | 56 | unknown |
| `002bf13c` | iOS_getFaceDataID(int) | 56 | unknown |
| `002bf32c` | Debug_SetDebugDirectBtn(int) | 56 | unknown |
| `002c0ae8` | GX_GetScreenOffsetX_1X() | 56 | unknown |
| `00075760` | deflateSetHeader | 52 | unknown |
| `000771cc` | deflateInit_ | 52 | unknown |
| `00081718` | unzGetCurrentFileZStreamPos64 | 52 | unknown |
| `00081abc` | unzeof | 52 | unknown |
| `00083cc8` | ogg_sync_clear | 52 | unknown |
| `000844a4` | ogg_stream_reset_serialno | 52 | unknown |
| `000844d8` | ogg_stream_packetout | 52 | unknown |
| `00086870` | vorbis_synthesis_read | 52 | unknown |
| `0009d050` | vorbis_synthesis_halfrate | 52 | unknown |
| `000a23cc` | CG2D_LOADER::Copy(void*) | 52 | unknown |
| `000a91a0` | CEGL2_IF::SetWVP(math::MATRIX4 const&) | 52 | unknown |
| `000b4728` | CINPUT_IF_TOUCH::GetTouchTime(int) | 52 | unknown |
| `000b6620` | CFILE::CFILE(char*) | 52 | unknown |
| `000b67dc` | CFILE::GetTime(_SYSTEMTIME*) | 52 | unknown |
| `000b6b04` | CFILE_DAT::CacheLoad(int, unsigned int, int) | 52 | unknown |
| `000b8a20` | CLIST::GetData(int) | 52 | unknown |
| `000b9b90` | CSTR_UTIL::GetHashValueEx(char*, int) | 52 | unknown |
| `000ba230` | CSOUND_IF::CSOUND_IF(int) | 52 | unknown |
| `000bd538` | CSOUND_LOADER_OGG::CSOUND_LOADER_OGG() | 52 | unknown |
| `000d893c` | allocatetextureconst(RECT16*, int, int, tagPOLY_FT4*, int) | 52 | unknown |
| `000e7488` | getCodeLength(unsigned char*) | 52 | unknown |
| `0010060c` | Wallocatetextureconst(RECT16*, int, int, tagPOLY_FT4*, int) | 52 | unknown |
| `0012f2a8` | iOSPersonalWinPos(int) | 52 | unknown |
| `00153470` | send_taskparamater(long, long, long, long) | 52 | unknown |
| `00153734` | Wsend_taskparamater(long, long, long, long) | 52 | unknown |
| `00159a78` | asmSerchMessagePointer(char*, int) | 52 | unknown |
| `0015b118` | iOSSlideSpeed(int*, int*, double, double) | 52 | unknown |
| `0015b354` | iOSSlideNaviCurIconGet() | 52 | unknown |
| `0015ebc0` | iOSStatusChangeCheck() | 52 | unknown |
| `00161e2c` | iOSIsCurMode() | 52 | unknown |
| `0016204c` | wasmSerchMessagePointer(char*, int) | 52 | unknown |
| `00176e50` | bSetSortCondition(int, short*) | 52 | unknown |
| `001a63dc` | bak_read(int, void*) | 52 | unknown |
| `001addd8` | CallGetAll(int) | 52 | unknown |
| `001ade0c` | CallGetEqp(int) | 52 | unknown |
| `001adf58` | CallGetAllDress(int) | 52 | unknown |
| `001cb030` | clear_setstatus(A_RESULT*) | 52 | unknown |
| `001cb844` | check_reaction_deny_all(BWORK*) | 52 | unknown |
| `001d9370` | get_joblevel(unsigned short) | 52 | unknown |
| `001eb760` | myStartShape() | 52 | unknown |
| `001f36c8` | EndAllAnimation() | 52 | unknown |
| `001fd278` | startInterventionMode() | 52 | unknown |
| `001fd7e4` | requestDamageNumber(int) | 52 | unknown |
| `0020d7d4` | pushMapAngle() | 52 | unknown |
| `0020d808` | popMapAngle() | 52 | unknown |
| `0020da48` | pushBackColor() | 52 | unknown |
| `0020dd10` | getAnimationRelativeDirection(unsigned int) | 52 | unknown |
| `0020dd44` | getUnitRelativeDirection(unsigned int) | 52 | unknown |
| `0020de24` | getAnimationRelativeDirection16(unsigned int) | 52 | unknown |
| `0020eb84` | disposeAnimation(int) | 52 | unknown |
| `0020eddc` | inactivateEventAnimation(int) | 52 | unknown |
| `0020f574` | getMapXYZ(SVECTOR*) | 52 | unknown |
| `002119c0` | PushChangePalette() | 52 | unknown |
| `002119f4` | PopChangePalette() | 52 | unknown |
| `00215bd4` | changeMapClut(int, int, short, short, short) | 52 | unknown |
| `0021b474` | GetMSQFrameRate(_EffectTCB*) | 52 | unknown |
| `00228e64` | startShape() | 52 | unknown |
| `0022a398` | getSmoothSVECLinear(SVECTOR*, SVECTOR*, int, int, SVECTOR*) | 52 | unknown |
| `0022a43c` | getSmoothVECLinear(VECTOR*, VECTOR*, int, int, VECTOR*) | 52 | unknown |
| `0022ad88` | Add2Shougen(VECTOR*, VECTOR*, SVECTOR*) | 52 | unknown |
| `00243014` | fRoll_exit(short*) | 52 | unknown |
| `00245a74` | o_ClearCardEvent() | 52 | unknown |
| `00245b34` | o_ClearCardEvent_X() | 52 | unknown |
| `0024a498` | iOS_vOpn_touchNum_addprim(iOS_CMenuTouchNum*, unsigned long*, int) | 52 | unknown |
| `0024dc8c` | ctlkiroku_active(CTLINFO*) | 52 | unknown |
| `0024e8d0` | ctlperson_active(CTLINFO*) | 52 | unknown |
| `0024fccc` | iOSTutoTipFadeCheck() | 52 | unknown |
| `00258e08` | evt_town_set() | 52 | unknown |
| `00258e3c` | evt_town_clr() | 52 | unknown |
| `00259e70` | ctlhouk_active(CTLINFO*) | 52 | unknown |
| `0025d618` | wldiwasaki_init() | 52 | unknown |
| `002602c0` | ctlmouke_active(CTLINFO*) | 52 | unknown |
| `00266efc` | pspGetWarFundsOfs(short*, short*) | 52 | unknown |
| `002675c0` | ctlret_active(CTLINFO*) | 52 | unknown |
| `0026b2bc` | snplflg_write(unsigned long*, int, int) | 52 | unknown |
| `0026c3cc` | ctltresure_active(CTLINFO*) | 52 | unknown |
| `0026f070` | ctlunreg_active(CTLINFO*) | 52 | unknown |
| `0026fa8c` | ctluwa_active(CTLINFO*) | 52 | unknown |
| `0027b4dc` | setCmdKind(unsigned int) | 52 | unknown |
| `0027f14c` | iOS_ClearRectHitAll() | 52 | unknown |
| `0027f204` | iOS_SetRectHit(int, RECT16*, int) | 52 | unknown |
| `0028230c` | iOS_disableClipFT4_getMaxPage() | 52 | unknown |
| `00282340` | iOS_disableClipFT3_getMaxPage() | 52 | unknown |
| `00282548` | iOS_disableClipFT3_Set(int) | 52 | unknown |
| `0028257c` | iOS_disableClipFT3_Reset(int) | 52 | unknown |
| `002825e0` | iOS_disableClipFT4_Set(int) | 52 | unknown |
| `00282614` | iOS_disableClipFT4_Reset(int) | 52 | unknown |
| `00284714` | CalcVectorFromID(VECTOR_DATABASE*, short) | 52 | unknown |
| `002869bc` | pspNetRandSub() | 52 | unknown |
| `0028af54` | __bpInitBinpackData | 52 | unknown |
| `0028e4e0` | xpLibcdSet(char const*) | 52 | unknown |
| `00291710` | SetDrawOffset | 52 | unknown |
| `00291bf8` | xpLibgpuExit | 52 | unknown |
| `002a0844` | ReadRotMatrix | 52 | unknown |
| `002a0cdc` | ApplyTransposeMatrixLV | 52 | unknown |
| `002a11d0` | SquareSS0 | 52 | unknown |
| `002a14d8` | ColorDpq | 52 | unknown |
| `002a15cc` | DpqColorLight | 52 | unknown |
| `002a242c` | RotColorDpq_nom | 52 | unknown |
| `002a2bf8` | xpLibSN::IdxGet() | 52 | unknown |
| `002a2c2c` | xpLibSN::IsFD(int) | 52 | unknown |
| `002ae88c` | GuEmu_GetCLUTAddress(unsigned short, int*, int*) | 52 | unknown |
| `002c5400` | Movie_FrameMove() | 52 | unknown |
| `002c6ebc` | Settings_Uninit() | 52 | unknown |
| `002c8a88` | SettingsWnd_Uninit() | 52 | unknown |
| `00079178` | gzprintf | 48 | unknown |
| `0007afb8` | inflateReset | 48 | unknown |
| `0007d0c4` | inflateUndermine | 48 | unknown |
| `00081630` | unzGetFilePos | 48 | unknown |
| `00082cac` | oggpack_adv1 | 48 | unknown |
| `0008450c` | ogg_stream_packetpeek | 48 | unknown |
| `00086b10` | vorbis_window | 48 | unknown |
| `000a2ba4` | CG2D_LOADER::GetImageExtFormat(int) | 48 | unknown |
| `000a33ec` | CG2D_LOADER_BMP::GetImageFormatExt(int) | 48 | unknown |
| `000a62e4` | CG2D_LOADER_TIM::GetSavePixelFormatOverwrite(_G2D_FORMAT*, int) | 48 | unknown |
| `000a7e7c` | CEGL2_IF::ClearBackdrop(float, float, float) | 48 | unknown |
| `000b3694` | CINPUT_DATA::Clear(int) | 48 | unknown |
| `000b6a28` | CFILE_DAT::Unload() | 48 | unknown |
| `000b6ad4` | CFILE_DAT::CacheUnload(int) | 48 | unknown |
| `000b6b7c` | CFILE_DAT::CacheFind(int) | 48 | unknown |
| `000b6bac` | CFILE_DAT::CacheFindFree() | 48 | unknown |
| `000b8030` | CFILE_UTIL::DirMove(char*, char*) | 48 | unknown |
| `000b9d5c` | CWORK_MEM::Delete(int) | 48 | unknown |
| `000b9da4` | CWORK_MEM::New(int) | 48 | unknown |
| `000bb29c` | CSOUND_IF::GetPlayMode(int) | 48 | unknown |
| `000bb320` | CSOUND_IF::GetFormatType(int) | 48 | unknown |
| `000bd968` | CFRAMERATE::Clear() | 48 | unknown |
| `000da47c` | event_init_system() | 48 | unknown |
| `000da6d0` | geteventcategory() | 48 | unknown |
| `000e0538` | import_localpad(int) | 48 | unknown |
| `00101a10` | Wrequest_command(int) | 48 | unknown |
| `001020f8` | Wevent_init_system() | 48 | unknown |
| `0010229c` | Wgeteventcategory() | 48 | unknown |
| `00153420` | wait_taskend(long) | 48 | unknown |
| `001536e4` | Wwait_taskend(long) | 48 | unknown |
| `0015b598` | iOSMapCurModeGet() | 48 | unknown |
| `0015d9b0` | iOSUnitTapCheck(int) | 48 | unknown |
| `0015e068` | iOSNumberGet(int) | 48 | unknown |
| `0015f350` | iOSUnitListUDDispCheck() | 48 | unknown |
| `0015f380` | iOSUnitListLRDispCheck() | 48 | unknown |
| `0015fbac` | iOSJobChanegAngle() | 48 | unknown |
| `00160cdc` | iOSYajiEffectGetFlagOk(int) | 48 | unknown |
| `00160d60` | iOSYajiEffectGetAlpha(int, int) | 48 | unknown |
| `00160d90` | iOSYajiEffectGetSizeTGA(int, int) | 48 | unknown |
| `00160ee8` | iOSYajiEffectEnd(int) | 48 | unknown |
| `001728ac` | cSetFrameRate(int) | 48 | unknown |
| `00176660` | bSetFrameRate(int) | 48 | unknown |
| `001800c8` | bWindowPositionInitSingle(int) | 48 | unknown |
| `00183484` | bWindowColorSet(COLOR*) | 48 | unknown |
| `00188440` | eItemChg(short, int) | 48 | unknown |
| `00188e24` | eGetTotalEquipItem(short) | 48 | unknown |
| `00188e84` | eItemCategoryPos(int, short*) | 48 | unknown |
| `001a6c94` | SetFrameRate(int) | 48 | unknown |
| `001a7338` | ItemChg(short, int) | 48 | unknown |
| `001a956c` | ItemCategoryPos(int, short*) | 48 | unknown |
| `001b9040` | iOSTutorialPadWaitCheck() | 48 | unknown |
| `001c03fc` | WindowPositionInitSingle(int) | 48 | unknown |
| `001c6f70` | WindowColorSet(COLOR*) | 48 | unknown |
| `001d1db8` | leave_unit_f(int) | 48 | unknown |
| `001d1f48` | check_move_ability(BWORK*) | 48 | unknown |
| `001d2e6c` | get_coord_address(BWORK*) | 48 | unknown |
| `001d9548` | check_prob(int, int) | 48 | unknown |
| `001dc914` | set_cco_SD(BWORK*) | 48 | unknown |
| `001e4f0c` | get_fusui_ability(BWORK*) | 48 | unknown |
| `001eb00c` | searchAnimationByID(unsigned short) | 48 | unknown |
| `001eedf4` | getWpnSequenceAddress(unsigned short) | 48 | unknown |
| `001f1650` | setMovingAnimationShape() | 48 | unknown |
| `00202150` | standerdExecution() | 48 | unknown |
| `00204268` | startLeftTurn(int) | 48 | unknown |
| `00204298` | startRightTurn(int) | 48 | unknown |
| `0020dbec` | requestAnimation(unsigned int, unsigned int) | 48 | unknown |
| `0020e560` | getOffsetAnimationPosition(int) | 48 | unknown |
| `002131f8` | requestDestinationAnbientAsDefault(int, CVECTOR*) | 48 | unknown |
| `00213868` | requestDestinationFlatAsDefault(int, CVECTOR*) | 48 | unknown |
| `00213e48` | stopAllColorRotation() | 48 | unknown |
| `00215d2c` | battleFileRead() | 48 | unknown |
| `0021b268` | SetEffectANMPtr(short) | 48 | unknown |
| `0021b298` | SetEffectTSQPtr(short) | 48 | unknown |
| `0021b860` | SetGravity(Vector*) | 48 | unknown |
| `0021bee0` | s16_ifObjNumEQU(_EffectTCB*) | 48 | unknown |
| `0021bf10` | s17_ifObjNumGT(_EffectTCB*) | 48 | unknown |
| `0021bf40` | s18_ifObjNumLT(_EffectTCB*) | 48 | unknown |
| `0021d23c` | initScheduleControl(_EffectTCB*, short) | 48 | unknown |
| `0021d290` | initMetascheduleControl(_EffectTCB*) | 48 | unknown |
| `0022a92c` | GetAnimationPositionFromBattleID(int, int, EffectOrder*, SVECTOR*) | 48 | unknown |
| `00243184` | fRoll_scroll(short*) | 48 | unknown |
| `0024337c` | fRoll_cdxafin(short*) | 48 | unknown |
| `002433ac` | fRoll_cdxafout(short*) | 48 | unknown |
| `0024932c` | vOpn_loopinit() | 48 | unknown |
| `00249cc4` | vEnd_CdReady_Chk() | 48 | unknown |
| `0024ad94` | openEntry(int) | 48 | unknown |
| `0025249c` | ctlworkingst_active(CTLINFO*) | 48 | unknown |
| `0025f138` | townpic_load(int) | 48 | unknown |
| `0025ffb0` | iOSSDNovelGetOT(int) | 48 | unknown |
| `0026995c` | snpl_addpara() | 48 | unknown |
| `0026998c` | snpl_subpara() | 48 | unknown |
| `00269e98` | snpl_exit() | 48 | unknown |
| `00270460` | curhis_get(int) | 48 | unknown |
| `00271e1c` | GetDistance(BWORK*, BWORK*) | 48 | unknown |
| `00279c34` | MemCpyW(unsigned short*, unsigned short const*, int) | 48 | unknown |
| `0027fc48` | cSaveFFT::Create(char*) | 48 | unknown |
| `00282518` | iOS_disableClipFT3_Get(int) | 48 | unknown |
| `002825b0` | iOS_disableClipFT4_Get(int) | 48 | unknown |
| `00283f50` | GLIVON_F3(unsigned long*, tagPOLY_F3*, short, unsigned long*) | 48 | unknown |
| `00283f80` | GLIVON_F4(unsigned long*, tagPOLY_F4*, short, unsigned long*) | 48 | unknown |
| `00286c90` | pspNetEntranceMapThumUnLoad() | 48 | unknown |
| `00286e94` | pspNetKeepTime(int) | 48 | unknown |
| `00289970` | pspIsNoneSaveData(int) | 48 | unknown |
| `0028ba54` | TE_task_create(int, void (*)(), int) | 48 | unknown |
| `0028bf4c` | _ps_wait() | 48 | unknown |
| `0028e538` | CdRead | 48 | unknown |
| `0028e6a4` | xpInitVblankFunc() | 48 | unknown |
| `0029138c` | GetClut | 48 | unknown |
| `0029c8e8` | xpLibgsAddOt | 48 | unknown |
| `0029cb28` | _gte_ldv01(SVECTOR*, SVECTOR*) | 48 | unknown |
| `0029cb58` | _gte_ldv01c(SVECTOR*) | 48 | unknown |
| `0029cba0` | _gte_ldrgb3(CVECTOR*, CVECTOR*, CVECTOR*) | 48 | unknown |
| `0029cbd0` | _gte_ldrgb3c(CVECTOR*) | 48 | unknown |
| `0029d60c` | _gte_stsz4c(long*) | 48 | unknown |
| `0029fdd4` | xpLibgteGetData | 48 | unknown |
| `002a12c4` | AverageZ3 | 48 | unknown |
| `002a12f4` | AverageZ4 | 48 | unknown |
| `002a1384` | NormalClip | 48 | unknown |
| `002a145c` | ReadLightMatrix | 48 | unknown |
| `002a14a8` | ReadColorMatrix | 48 | unknown |
| `002a2ff8` | xpInitHeap | 48 | unknown |
| `002a33e0` | pspSaveBase::ParamBaseSet(int, int, int, int, int, int) | 48 | unknown |
| `002a38a8` | pspSaveList::pspSaveList() | 48 | unknown |
| `002b045c` | CAPP_INFO::GetResourceScale() | 48 | unknown |
| `002b077c` | CDebugPrint::ApplyVertexScaling(float, float, float) | 48 | unknown |
| `002b2260` | RETINA_SCALE(int) | 48 | unknown |
| `002b2378` | Music_Stop() | 48 | unknown |
| `002b23a8` | Music_Pause() | 48 | unknown |
| `002b8348` | Main_IsTitle() | 48 | unknown |
| `002c0ab0` | GX_GetScreenOffsetX() | 48 | unknown |
| `002cb158` | __aeabi_cdrcmple | 48 | unknown |
| `00072788` | Java_com_square_1enix_FFT_1Android_GL2JNILib_onPause | 44 | unknown |
| `000773d4` | gzclose | 44 | unknown |
| `000808cc` | unzGetGlobalInfo64 | 44 | unknown |
| `0008254c` | oggpack_writeclear | 44 | unknown |
| `00082a18` | oggpack_readinit | 44 | unknown |
| `00082c0c` | oggpackB_look1 | 44 | unknown |
| `00084418` | ogg_sync_reset | 44 | unknown |
| `000960c4` | res0_free_info | 44 | unknown |
| `0009e900` | ov_test_callbacks | 44 | unknown |
| `000a70e0` | CGX_SCREEN_CORRECT::X_AlignR(int) | 44 | unknown |
| `000a7134` | CGX_SCREEN_CORRECT::Y_AlignB(int) | 44 | unknown |
| `000aba20` | CEGL2_SHADER::SetMatrix4(int, math::MATRIX4 const&) | 44 | unknown |
| `000af0d8` | CEGL2_TEX_HYBRID::CLUTAddr_AutoRelease() | 44 | unknown |
| `000b3728` | CINPUT_DATA::GetPress(int, int) | 44 | unknown |
| `000b3754` | CINPUT_DATA::GetDown(int, int) | 44 | unknown |
| `000b3820` | CINPUT_DATA::GetUpDirect(int, int) | 44 | unknown |
| `000b384c` | CINPUT_DATA::GetRepeat(int, int) | 44 | unknown |
| `000b3878` | CINPUT_DATA::GetDelayDown(int, int) | 44 | unknown |
| `000b5480` | CRECT::SetEnableAll(int) | 44 | unknown |
| `000b55b8` | CRECT::MoveCursorFirst(int, int) | 44 | unknown |
| `000b595c` | CRECT::MoveCursorPrev(int, int) | 44 | unknown |
| `000b5a14` | CRECT::MoveCursorNext(int, int) | 44 | unknown |
| `000b5a40` | CUI_SCROLLBAR::CUI_SCROLLBAR() | 44 | unknown |
| `000ba4ac` | CSOUND_IF::RegisterRootPath(char*) | 44 | unknown |
| `000bba9c` | CSOUND_IF_SL::GetPlaySample(int) | 44 | unknown |
| `000bbae4` | CSOUND_IF_SL::GetTotalSample(int) | 44 | unknown |
| `000bcc20` | CSOUND_LOADER_PCM::IsTerminated() const | 44 | unknown |
| `000d6f54` | allocatewindowinit() | 44 | unknown |
| `000d86ac` | getanimpos2d(int, SVECTOR*) | 44 | unknown |
| `000d9810` | hook_disp_option() | 44 | unknown |
| `000da610` | set_autobattletarget(int, int) | 44 | unknown |
| `000f1484` | disp_okng() | 44 | unknown |
| `000f14b0` | disp_yesno() | 44 | unknown |
| `000f14dc` | disp_attackng() | 44 | unknown |
| `000f1508` | disp_coverng() | 44 | unknown |
| `000f1534` | disp_executeng() | 44 | unknown |
| `000f1604` | disp_dismiss_yesno() | 44 | unknown |
| `000f1630` | disp_yameru_yesno() | 44 | unknown |
| `000f586c` | attackteam_call(unsigned long*, unsigned long) | 44 | unknown |
| `000fea78` | Wallocatewindowinit() | 44 | unknown |
| `00100380` | Wgetanimpos2d(int, SVECTOR*) | 44 | unknown |
| `00101624` | Whook_disp_option() | 44 | unknown |
| `001021dc` | Wset_autobattletarget(int, int) | 44 | unknown |
| `00106270` | Wdisp_okng() | 44 | unknown |
| `0010629c` | Wdisp_yesno() | 44 | unknown |
| `001062c8` | Wdisp_attackng() | 44 | unknown |
| `001062f4` | Wdisp_coverng() | 44 | unknown |
| `00106320` | Wdisp_executeng() | 44 | unknown |
| `001063f0` | Wdisp_dismiss_yesno() | 44 | unknown |
| `0010641c` | Wdisp_yameru_yesno() | 44 | unknown |
| `0012f250` | iOSdisp_personalWinDisp() | 44 | unknown |
| `0012f27c` | iOSdisp_personalWinStay() | 44 | unknown |
| `001599d0` | asmGetInput2() | 44 | unknown |
| `001599fc` | asmGetInput3() | 44 | unknown |
| `00159a28` | asmGetActiveF() | 44 | unknown |
| `0015a498` | iOSUnitAutoModeCheck() | 44 | unknown |
| `0015d238` | iOSstartRightTurn(int) | 44 | unknown |
| `0015d970` | iOSStatusConfGet() | 44 | unknown |
| `0015da34` | iOSCurSameProcs(ActionRequest*) | 44 | unknown |
| `0015df10` | iOSGT4_MapT9Get(unsigned long) | 44 | unknown |
| `0015eb80` | iOSBtlStsOutWinSet() | 44 | unknown |
| `0015ef50` | iOSUnitListMovOtherCheck() | 44 | unknown |
| `00161fa4` | wasmGetInput2() | 44 | unknown |
| `00161fd0` | wasmGetInput3() | 44 | unknown |
| `00161ffc` | wasmGetActiveF() | 44 | unknown |
| `0017b2cc` | bMenuSelInit() | 44 | unknown |
| `00183650` | bDrawWindow2(unsigned char*, unsigned long, int) | 44 | unknown |
| `0018ea94` | eWindowPositionInitSingle(int) | 44 | unknown |
| `00192e50` | eDrawWindow2(unsigned char*, unsigned long, int) | 44 | unknown |
| `00195e4c` | jWindowPositionInitSingle(int) | 44 | unknown |
| `00196db4` | jMenuSelInit() | 44 | unknown |
| `00199694` | CallGetItemPrice(int) | 44 | unknown |
| `001a92cc` | GetTotalItem(short) | 44 | unknown |
| `001ad9f8` | FadeInInit() | 44 | unknown |
| `001b7a90` | MenuSelInit() | 44 | unknown |
| `001cb878` | bcp_roll(BWORK*) | 44 | unknown |
| `001d1d8c` | disappare_unit_f(int) | 44 | unknown |
| `001d2968` | get_bwp(int) | 44 | unknown |
| `001d6404` | set_guard_status(int) | 44 | unknown |
| `001d94f0` | get_rangedata(unsigned short) | 44 | unknown |
| `001d951c` | get_effectdata(unsigned short) | 44 | unknown |
| `001f7598` | executeAnimationProgram(tag_animation*) | 44 | unknown |
| `0020e6b0` | requestAnimationFlipOFF(int) | 44 | unknown |
| `0020e788` | setAnimationBrightColor(int) | 44 | unknown |
| `0020e914` | eventWeaponEquip(int, int) | 44 | unknown |
| `0020f7c8` | setCurrentPanel(int) | 44 | unknown |
| `0020f874` | eventWarpEffect(int) | 44 | unknown |
| `0021b2c8` | SetEffectSEQPtr(short) | 44 | unknown |
| `0021b2f4` | SetEffectTBLPtr(short) | 44 | unknown |
| `0021b320` | SetEffectPMTPtr(short) | 44 | unknown |
| `0021b41c` | SetEffectSetUpDataPtr(short) | 44 | unknown |
| `0021b448` | SetEffectFrameRatePtr(short) | 44 | unknown |
| `0021b8c4` | PopGravity() | 44 | unknown |
| `0021ceb0` | WhoUnlockEffect(long) | 44 | unknown |
| `00243560` | fRoll_xawait(short*) | 44 | unknown |
| `00249474` | vOpn_fadein(int) | 44 | unknown |
| `00256e70` | ctltownmenu_active(CTLINFO*) | 44 | unknown |
| `00256e9c` | ctltownmenu_deactive(CTLINFO*) | 44 | unknown |
| `0025d7f0` | wldfrm_rect(int, RECT16*) | 44 | unknown |
| `00269930` | snpl_setpara() | 44 | unknown |
| `00269e6c` | snpl_sndstop() | 44 | unknown |
| `0026b2f0` | snplflg_read(unsigned long*, int) | 44 | unknown |
| `0027134c` | Ssd_StopEffect(long) | 44 | unknown |
| `0027334c` | SetDestUnit(int) | 44 | unknown |
| `0027b53c` | LoadImage_menuData() | 44 | unknown |
| `0027c0e8` | iOS_CMenuTouch::setYLine(int) | 44 | unknown |
| `0027f180` | iOS_ClearRectHit(int) | 44 | unknown |
| `0027f654` | iOS_SetLastBGMFromResumeData(unsigned short*, unsigned short*) | 44 | unknown |
| `0027fa20` | iOS_Resume_DataCopy(IOS_RESUME_DATACOPY_MODE, unsigned char*, unsigned char*, int) | 44 | unknown |
| `00280590` | GetAbilityName(int) | 44 | unknown |
| `00284620` | new_VectorXYZ(VECTOR_DATABASE*, short, short, short) | 44 | unknown |
| `002846e8` | VectorFromID(VECTOR_DATABASE*, short) | 44 | unknown |
| `00287044` | get_timing_true() | 44 | unknown |
| `0028846c` | free_hight_font() | 44 | unknown |
| `0028a054` | pspClearCurrentSystemFile() | 44 | unknown |
| `0028a140` | pspSaveDataEnableSystemFlg_Direct(FFTPSP_SYSTEM_FLG) | 44 | unknown |
| `0028baa4` | TE_task_stop(long) | 44 | unknown |
| `002a0900` | MulRotMatrix0 | 44 | unknown |
| `002a096c` | ApplyMatrix | 44 | unknown |
| `002a0a54` | ApplyMatrixSV | 44 | unknown |
| `002a1148` | SquareSL0 | 44 | unknown |
| `002a2620` | RotTrans | 44 | unknown |
| `002a264c` | RotTransSV | 44 | unknown |
| `002a32b0` | pspSaveAuto::getFreeSize() | 44 | unknown |
| `002a32dc` | pspSaveAuto::getMsSize() | 44 | unknown |
| `002a3524` | pspSaveBase::NewDataItemSet(void*, unsigned int, unsigned int) | 44 | unknown |
| `002b23d8` | Music_Replay() | 44 | unknown |
| `002bef74` | PIE_OFFSET(unsigned int) | 44 | unknown |
| `00081a94` | unztell64 | 40 | unknown |
| `00082450` | oggpack_writecheck | 40 | unknown |
| `00082520` | oggpack_reset | 40 | unknown |
| `000829c4` | oggpack_writecopy | 40 | unknown |
| `000829ec` | oggpackB_writecopy | 40 | unknown |
| `00082be4` | oggpack_look1 | 40 | unknown |
| `00083234` | ogg_page_serialno | 40 | unknown |
| `0008325c` | ogg_page_pageno | 40 | unknown |
| `00083ca0` | ogg_sync_init | 40 | unknown |
| `0008c24c` | vorbis_info_init | 40 | unknown |
| `00094078` | _vp_global_free | 40 | unknown |
| `000940a0` | _vi_gpsy_free | 40 | unknown |
| `000940c8` | _vi_psy_free | 40 | unknown |
| `000a2be8` | CG2D_LOADER_BMP::~CG2D_LOADER_BMP() | 40 | unknown |
| `000a2c24` | CG2D_LOADER_BMP::GetSavePixelFormatData(int, int*) | 40 | unknown |
| `000a33c4` | CG2D_LOADER_BMP::GetImageFormatType(int) | 40 | unknown |
| `000a4b10` | CG2D_LOADER_TGA::~CG2D_LOADER_TGA() | 40 | unknown |
| `000a4e98` | CG2D_LOADER_TGA::GetSavePixelFormatData(int, int*) | 40 | unknown |
| `000a5714` | CG2D_LOADER_TGA::GetImageFormatType(int) | 40 | unknown |
| `000a5e70` | CG2D_LOADER_TIM::~CG2D_LOADER_TIM() | 40 | unknown |
| `000a62bc` | CG2D_LOADER_TIM::GetSavePixelFormatData(int, int*) | 40 | unknown |
| `000a65e0` | CG2D_LOADER_TIM::GetImageFormatType(int) | 40 | unknown |
| `000a6f00` | CGX_SCREEN_CORRECT::GetCorrect(float*, float*, float*) | 40 | unknown |
| `000a70b8` | CGX_SCREEN_CORRECT::X_AlignL(int) | 40 | unknown |
| `000a710c` | CGX_SCREEN_CORRECT::Y_AlignT(int) | 40 | unknown |
| `000a7488` | CGX_SCREEN_CORRECT::Area_W_Scaled(int, int) | 40 | unknown |
| `000a74b0` | CGX_SCREEN_CORRECT::Area_H_Scaled(int, int) | 40 | unknown |
| `000a7e30` | CEGL2_IF::GetExtension(char*) | 40 | unknown |
| `000a85fc` | CEGL2_IF::Term() | 40 | unknown |
| `000abb00` | CEGL2_SHADER::SetFVector4Array(int, int, math::VECTOR4<float>*) | 40 | unknown |
| `000ace68` | CEGL2_SPRITE::GetPixelByte() | 40 | unknown |
| `000aef54` | CEGL2_TEX_HYBRID::UV_AutoRelease() | 40 | unknown |
| `000af9c0` | CCAMERA::~CCAMERA() | 40 | unknown |
| `000b1880` | CEGL_PACKET::CEGL_PACKET() | 40 | unknown |
| `000b356c` | CINPUT_DATA::SetKeyCode(int, int, unsigned int, int) | 40 | unknown |
| `000b364c` | CINPUT_DATA::SetKeyDelay(int, int, unsigned int) | 40 | unknown |
| `000b45f4` | CINPUT_IF_TOUCH::GetData(int) | 40 | unknown |
| `000b50c0` | CRECT::Init() | 40 | unknown |
| `000b5254` | CRECT::GetChangeRID(int, int, int) | 40 | unknown |
| `000b6b38` | CFILE_DAT::CacheUnloadAll() | 40 | unknown |
| `000b70ac` | CFILE_TXT::GetDataAsFloat(int, int, unsigned int) | 40 | unknown |
| `000ba584` | CSOUND_IF::SetAttr(int, unsigned char) | 40 | unknown |
| `000bcce4` | CSOUND_LOADER::~CSOUND_LOADER() | 40 | unknown |
| `000bceac` | CSOUND_LOADER_PCM::CSOUND_LOADER_PCM() | 40 | unknown |
| `000bd378` | CSOUND_LOADER_OGG::Tell() const | 40 | unknown |
| `000be18c` | CSTEP::SetProgress(float) | 40 | unknown |
| `000be1b4` | CSTEP_BATCH::CSTEP_BATCH() | 40 | unknown |
| `000daac0` | settaskkind(int) | 40 | unknown |
| `000e0eec` | jobstts_call(unsigned long*, unsigned long) | 40 | unknown |
| `000e744c` | iOS_GetKeyMask() | 40 | unknown |
| `001024bc` | Wreaded_mapchange() | 40 | unknown |
| `0010278c` | Wsettaskkind(int) | 40 | unknown |
| `0010de7c` | Wimport_localpad(int) | 40 | unknown |
| `0010f8cc` | Wjobstts_call(unsigned long*, unsigned long) | 40 | unknown |
| `0012f19c` | get_pitno() | 40 | unknown |
| `0012f1ec` | iOSdisp_personalWinAppear() | 40 | unknown |
| `0012f228` | iOSdisp_personalWinPosGet() | 40 | unknown |
| `00155cec` | tutorialstatusget(int) | 40 | unknown |
| `001599a8` | asmGetInput1() | 40 | unknown |
| `0015d1c4` | iOSstartLeftTurn(int) | 40 | unknown |
| `0015e040` | iOSActUnitCurSet() | 40 | unknown |
| `0015eb58` | iOSBtlStsOutWinReset() | 40 | unknown |
| `0015ebf4` | iOSMapTouchCancel() | 40 | unknown |
| `0015ee2c` | iOSUnitListWinReset() | 40 | unknown |
| `001609d0` | iOSYajiEffectClear() | 40 | unknown |
| `001614c4` | iOSSdNovelEnd() | 40 | unknown |
| `0016196c` | iOSWldHelpCheck() | 40 | unknown |
| `00161f7c` | wasmGetInput1() | 40 | unknown |
| `001755f8` | cWindowColorSet(COLOR*) | 40 | unknown |
| `001875f0` | GetSaveDataInit() | 40 | unknown |
| `0018f9a8` | eMenuSelInit() | 40 | unknown |
| `00192c8c` | eWindowColorSet(COLOR*) | 40 | unknown |
| `001a3eb4` | PoachUnit() | 40 | unknown |
| `001ac88c` | addFT4num() | 40 | unknown |
| `001ad9d0` | GetFadeStatus() | 40 | unknown |
| `001ada24` | FadeOutInit() | 40 | unknown |
| `001baea0` | unitans_init() | 40 | unknown |
| `001ca954` | net_getknockback(unsigned char*, unsigned char*, unsigned char*) | 40 | unknown |
| `001cb7d4` | check_reaction_deny(BWORK*) | 40 | unknown |
| `001ceaec` | set_status_all_sp(int, int) | 40 | unknown |
| `001cebfc` | set_target_table2(unsigned char*) | 40 | unknown |
| `001d73ec` | clear_unitwork() | 40 | unknown |
| `001d8d28` | get_jobdata(int) | 40 | unknown |
| `001dbcc4` | unitwork_init2all(BWORK*, int) | 40 | unknown |
| `001dc44c` | adjust_entry_status(BWORK*) | 40 | unknown |
| `001eedcc` | getWpnShapeAddress(unsigned short) | 40 | unknown |
| `001f6374` | setPositionToLongPosition(tag_animation*) | 40 | unknown |
| `001fd2c4` | endInterventionMode() | 40 | unknown |
| `001fd794` | requestTargetAnimation(int) | 40 | unknown |
| `001fd7bc` | requestTargetAnimationFromBattleID(int) | 40 | unknown |
| `00202040` | pspNetDecisionIyasi() | 40 | unknown |
| `0020c5d8` | errorHandler(int) | 40 | unknown |
| `0020c600` | warningHandler(int) | 40 | unknown |
| `0020c74c` | initSoundHeap() | 40 | unknown |
| `0020c99c` | initFileBuffer() | 40 | unknown |
| `0020cc90` | fileReadCD(unsigned long, unsigned long, void*) | 40 | unknown |
| `0020d060` | setMapScrollXYZ(VECTOR*) | 40 | unknown |
| `0020d2b8` | setMapScroll(VECTOR*) | 40 | unknown |
| `0020d5d8` | setMapScale(VECTOR*) | 40 | unknown |
| `0020d84c` | setMapAngle(SVECTOR*) | 40 | unknown |
| `0020f5a8` | getMapSize(SVECTOR*) | 40 | unknown |
| `0020f5d0` | getMapIDFromAnimationID(int) | 40 | unknown |
| `0020f5f8` | getMapIDFromBattleID(int) | 40 | unknown |
| `0020f680` | eventMapRewrite() | 40 | unknown |
| `00216820` | initializeMusicBuffer() | 40 | unknown |
| `0021695c` | stopAllEffect() | 40 | unknown |
| `00218dcc` | InitCamera() | 40 | unknown |
| `002231b0` | GetReachableHeight(int) | 40 | unknown |
| `0022a994` | EqualRShift12VECTORToVECTOR(VECTOR*, VECTOR*) | 40 | unknown |
| `0022a9bc` | EqualLShift12VECTORToVECTOR(VECTOR*, VECTOR*) | 40 | unknown |
| `0022a9e4` | EqualAnd0xfffSVECTORToSVECTOR(SVECTOR*, SVECTOR*) | 40 | unknown |
| `00246360` | ctlstartmov_main(CTLINFO*) | 40 | unknown |
| `002494a0` | vOpn_fadeout(int) | 40 | unknown |
| `0024adc4` | endEntry() | 40 | unknown |
| `002592fc` | evt_flagset() | 40 | unknown |
| `0025bc50` | jobnumber_conv(int) | 40 | unknown |
| `00267340` | iOS_add_anmpac_max(int) | 40 | unknown |
| `0026a1a4` | snpl_sndreq() | 40 | unknown |
| `0026a64c` | snplinf_init(int) | 40 | unknown |
| `0026b0b8` | snpl_musicreq() | 40 | unknown |
| `0027383c` | ClearMove(MOVE*) | 40 | unknown |
| `00273b10` | SetSafePanelInRange(int) | 40 | unknown |
| `0027c130` | iOS_CMenuTouch::setXIconRect(unsigned char, int, int, int, int) | 40 | unknown |
| `0027e710` | iOS_CMenuTouchSaveLoad::setXIconRect(unsigned char, int, int, int, int) | 40 | unknown |
| `0027fbc8` | iOS_WorldMapResumeGetData(unsigned char**, unsigned int*) | 40 | unknown |
| `002808b8` | iOS_initTransFace() | 40 | unknown |
| `00286e58` | pspNetEntranceOptionInit() | 40 | unknown |
| `0028b3f0` | pspWorldDataRectSet(RECT16*) | 40 | unknown |
| `0028c668` | CFFT_STATE::UnitIDToFID_SPR(int) | 40 | unknown |
| `0028dc30` | SetRCnt | 40 | unknown |
| `0028dd04` | xpApiEnv::alarmHandler(void*) | 40 | unknown |
| `0028e66c` | PadInit | 40 | unknown |
| `00291428` | SetPolyFT4 | 40 | unknown |
| `00291498` | SetPolyGT4 | 40 | unknown |
| `00294e88` | xpLibgpuDrawEnvSet | 40 | unknown |
| `00295520` | xpLibgpuDispListSetFromEdram | 40 | unknown |
| `0029cc00` | _gte_ldlv0(VECTOR*) | 40 | unknown |
| `0029cc28` | _gte_ldlvl(VECTOR*) | 40 | unknown |
| `0029cc50` | _gte_ldsv(SVECTOR*) | 40 | unknown |
| `0029cc98` | _gte_ldcv(CVECTOR*) | 40 | unknown |
| `0029ccc0` | _gte_ldclmv(MATRIX*) | 40 | unknown |
| `0029cd54` | _gte_ldsxy3c(long*) | 40 | unknown |
| `0029ce10` | _gte_ldopv2(VECTOR*) | 40 | unknown |
| `0029ce80` | _gte_SetBackColor(long, long, long) | 40 | unknown |
| `0029cec4` | _gte_SetFarColor(long, long, long) | 40 | unknown |
| `0029d1f8` | _gte_ld_intpol_sv0(SVECTOR*) | 40 | unknown |
| `0029d220` | _gte_ld_intpol_sv1(SVECTOR*) | 40 | unknown |
| `0029d248` | _gte_ldfc(long*) | 40 | unknown |
| `0029d270` | _gte_ldopv2SV(SVECTOR*) | 40 | unknown |
| `0029d308` | _gte_stsxy3(long*, long*, long*) | 40 | unknown |
| `0029d330` | _gte_stsxy3c(long*) | 40 | unknown |
| `0029d3e0` | _gte_stsxy3_f3(tagPOLY_F3*) | 40 | unknown |
| `0029d408` | _gte_stsxy3_g3(tagPOLY_G3*) | 40 | unknown |
| `0029d430` | _gte_stsxy3_ft3(tagPOLY_FT3*) | 40 | unknown |
| `0029d458` | _gte_stsxy3_gt3(tagPOLY_GT3*) | 40 | unknown |
| `0029d480` | _gte_stsxy3_f4(tagPOLY_F4*) | 40 | unknown |
| `0029d4a8` | _gte_stsxy3_g4(tagPOLY_G4*) | 40 | unknown |
| `0029d4d0` | _gte_stsxy3_ft4(tagPOLY_FT4*) | 40 | unknown |
| `0029d4f8` | _gte_stsxy3_gt4(tagPOLY_GT4*) | 40 | unknown |
| `0029d584` | _gte_stsz3(long*, long*, long*) | 40 | unknown |
| `0029d5e4` | _gte_stsz3c(long*) | 40 | unknown |
| `0029d63c` | _gte_stszotz(long*) | 40 | unknown |
| `0029d694` | _gte_stlvl(VECTOR*) | 40 | unknown |
| `0029d6bc` | _gte_stlvnl(VECTOR*) | 40 | unknown |
| `0029d72c` | _gte_stsv(SVECTOR*) | 40 | unknown |
| `0029d754` | _gte_stclmv(MATRIX*) | 40 | unknown |
| `0029d79c` | _gte_stcv(CVECTOR*) | 40 | unknown |
| `0029d7dc` | _gte_strgb3(CVECTOR*, CVECTOR*, CVECTOR*) | 40 | unknown |
| `0029d804` | _gte_strgb3_g3(tagPOLY_G3*) | 40 | unknown |
| `0029d82c` | _gte_strgb3_gt3(tagPOLY_GT3*) | 40 | unknown |
| `0029d854` | _gte_strgb3_g4(tagPOLY_G4*) | 40 | unknown |
| `0029d87c` | _gte_strgb3_gt4(tagPOLY_GT4*) | 40 | unknown |
| `0029d92c` | _gte_sttr(VECTOR*) | 40 | unknown |
| `0029da0c` | _gte_stfc(long*) | 40 | unknown |
| `0029ff34` | cln | 40 | unknown |
| `002a081c` | SetMulMatrix | 40 | unknown |
| `002a092c` | SetMulRotMatrix | 40 | unknown |
| `002a13c8` | Intpl | 40 | unknown |
| `002a150c` | ColorCol | 40 | unknown |
| `002a156c` | DpqColor | 40 | unknown |
| `002a18ac` | NormalColor3 | 40 | unknown |
| `002a18d4` | NormalColorDpq_nom | 40 | unknown |
| `002a1914` | NormalColorDpq3_nom | 40 | unknown |
| `002a19c4` | NormalColorCol3 | 40 | unknown |
| `002a19ec` | read_sz_fifo3(long*, long*, long*) | 40 | unknown |
| `002a1aac` | read_sxsy_fifo3(long*, long*, long*) | 40 | unknown |
| `002a1b1c` | read_rgb_fifo(long*, long*, long*) | 40 | unknown |
| `002a25f8` | read_mt(long*, long*, long*) | 40 | unknown |
| `002a2b5c` | xpLibSN::Init() | 40 | unknown |
| `002b2238` | IS_TEX_2X() | 40 | unknown |
| `002b2404` | Music_SetVol(int, int) | 40 | unknown |
| `002b7a34` | SetDisableMapTouchRect(RECT16*) | 40 | unknown |
| `002cab74` | __aeabi_i2d | 40 | unknown |
| `002cb484` | __aeabi_ui2f | 40 | unknown |
| `000727d0` | Java_com_square_1enix_FFT_1Android_GL2JNILib_isExit | 36 | unknown |
| `000735c8` | Android_Font_GetBuffer(int*, int*) | 36 | unknown |
| `00077500` | gzeof | 36 | unknown |
| `00081a70` | unztell | 36 | unknown |
| `000821b0` | unzOpenCurrentFile | 36 | unknown |
| `000821d4` | unzOpenCurrentFilePassword | 36 | unknown |
| `000832c4` | ogg_stream_check | 36 | unknown |
| `0008453c` | ogg_packet_clear | 36 | unknown |
| `00097b4c` | ov_ilog | 36 | unknown |
| `000a154c` | ov_raw_seek_lap | 36 | unknown |
| `000a1570` | ov_pcm_seek_lap | 36 | unknown |
| `000a1594` | ov_pcm_seek_page_lap | 36 | unknown |
| `000a15b8` | ov_time_seek_lap | 36 | unknown |
| `000a15dc` | ov_time_seek_page_lap | 36 | unknown |
| `000a72f8` | CGX_SCREEN_CORRECT::Area_GetScale(int, float*, float*) | 36 | unknown |
| `000a81ec` | CEGL2_IF::SetScissor(_RECT_S32*) | 36 | unknown |
| `000a853c` | CEGL2_IF::DeleteTexture(unsigned int) | 36 | unknown |
| `000a9130` | CEGL2_IF::CLUT_Unload(int) | 36 | unknown |
| `000aa8d4` | CEGL2_FBO::CEGL2_FBO() | 36 | unknown |
| `000aba4c` | CEGL2_SHADER::SetFVector4(int, math::VECTOR4<float> const&) | 36 | unknown |
| `000aba70` | CEGL2_SHADER::SetFVector3(int, math::VECTOR3<float> const&) | 36 | unknown |
| `000aba94` | CEGL2_SHADER::SetFVector2(int, math::VECTOR2<float> const&) | 36 | unknown |
| `000abab8` | CEGL2_SHADER::SetFloat(int, float) | 36 | unknown |
| `000abadc` | CEGL2_SHADER::SetBool(int, bool) | 36 | unknown |
| `000ad900` | CEGL2_SPRITE::SetColor(int, unsigned char, unsigned char, unsigned char) | 36 | unknown |
| `000af008` | CEGL2_TEX_HYBRID::CLUTAddr_UnregistAll() | 36 | unknown |
| `000b3548` | CINPUT_DATA::GetData(int) | 36 | unknown |
| `000b3d14` | CINPUT_IF_TOUCH::SetKeyCode(int, int, unsigned int) | 36 | unknown |
| `000b3f14` | CINPUT_IF_TOUCH::End(int, int) | 36 | unknown |
| `000b459c` | CINPUT_IF_TOUCH::OnTouchesCanceled(int, int, int, int) | 36 | unknown |
| `000b45d0` | CINPUT_IF_TOUCH::GetDevice(int) | 36 | unknown |
| `000b527c` | CRECT::GetRect(int, _RECT_S32*) | 36 | unknown |
| `000b5acc` | CUI_SCROLLBAR::~CUI_SCROLLBAR() | 36 | unknown |
| `000b5af0` | CUI_SCROLLBAR::GetDragOffset(int*, int*) | 36 | unknown |
| `000b67b8` | CFILE::GetSize() | 36 | unknown |
| `000b6f88` | CFILE_TXT::GetColumnNum(int) | 36 | unknown |
| `000b79b4` | CFILE_UTIL::FileDelete(char*, int) | 36 | unknown |
| `000b8a74` | CLIST::ResetID(int) | 36 | unknown |
| `000b8be4` | CSTR_UTIL::IsLeadByte(unsigned char) | 36 | unknown |
| `000b9f88` | CTHREAD::~CTHREAD() | 36 | unknown |
| `000bd194` | CSOUND_LOADER_OGG::GetTotalDecoded() const | 36 | unknown |
| `000be138` | CSTEP::SetData(int) | 36 | unknown |
| `000be15c` | CSTEP::SetDataF(float) | 36 | unknown |
| `000d8710` | getanimpos3dl(int, long*) | 36 | unknown |
| `000da7e4` | readed_mapchange() | 36 | unknown |
| `000dfa70` | wait_anmend(int) | 36 | unknown |
| `000e7fec` | iOS_Resume_ENVEFFECT_Rain() | 36 | unknown |
| `000fb530` | iOS_setLastBgmForResume(int, int) | 36 | unknown |
| `001003e4` | Wgetanimpos3dl(int, long*) | 36 | unknown |
| `00108e28` | Wwait_anmend(int) | 36 | unknown |
| `0010f99c` | WiOS_touchNum_addlocalprim2(iOS_CMenuTouchNum*) | 36 | unknown |
| `0011dd64` | extend_windowframe(int, int, RECT16*, int, int) | 36 | unknown |
| `0011e668` | Wextend_windowframe(int, int, RECT16*, int, int) | 36 | unknown |
| `00153254` | task_wait(long) | 36 | unknown |
| `00153350` | task_start(long) | 36 | unknown |
| `00153374` | task_stop(long) | 36 | unknown |
| `00153518` | Wtask_wait(long) | 36 | unknown |
| `00153614` | Wtask_start(long) | 36 | unknown |
| `00153638` | Wtask_stop(long) | 36 | unknown |
| `0015391c` | check_eventtool(int, int) | 36 | unknown |
| `0015b664` | iOSTchInputCheck() | 36 | unknown |
| `0015deec` | iOSGT4_MapT9(unsigned long, long) | 36 | unknown |
| `00161430` | iOSSdNovelGetFlagOk(int) | 36 | unknown |
| `00161784` | iOSTgaIconFlagCls() | 36 | unknown |
| `001617a8` | iOSTgaIconGetFlagOk(int) | 36 | unknown |
| `00161d50` | iOSPosW(int) | 36 | unknown |
| `00161d74` | iOSPosH(int) | 36 | unknown |
| `0016a0c8` | ASHURA_on_disp() | 36 | unknown |
| `0016f794` | ASHURA_getOTptrZ(int) | 36 | unknown |
| `001789bc` | iOS_getMasaCdbOt_graphics(long) | 36 | unknown |
| `00181d98` | bWindowInit2(short*, int, int, unsigned char*) | 36 | unknown |
| `00183730` | GetCardState() | 36 | unknown |
| `0018e334` | equans_init() | 36 | unknown |
| `00191cf4` | eWindowInit2(short*, int, int, unsigned char*) | 36 | unknown |
| `001948dc` | iOS_getMasaCdbOt(int) | 36 | unknown |
| `0019855c` | jWindowInit2(short*, int, int, unsigned char*) | 36 | unknown |
| `0019960c` | jDrawWindow2(unsigned char*, unsigned long, int) | 36 | unknown |
| `001baac4` | event_warning(short, int) | 36 | unknown |
| `001c5190` | WindowInit2(short*, int, int, unsigned char*) | 36 | unknown |
| `001ca580` | get_net_rival_weapon_range() | 36 | unknown |
| `001ccc18` | get_trap_no(BWORK*) | 36 | unknown |
| `001d1878` | iOS_RESUME_SET_BSTR(IOS_RESUME_DATA_BSTR*, IOS_RESUME_DATACOPY_MODE) | 36 | unknown |
| `001d7414` | get_unitwork_add(int) | 36 | unknown |
| `001eb2d8` | vramDeleteUsed() | 36 | unknown |
| `001f4a64` | initEntryEnemyAnimations(int) | 36 | unknown |
| `001f5be4` | terminateAnimation(int) | 36 | unknown |
| `001fd1dc` | nextTurnOrder() | 36 | unknown |
| `001fea14` | changeWeaponEquipment(int, int) | 36 | unknown |
| `0020d008` | pushMapScrollXYZ() | 36 | unknown |
| `0020d02c` | popMapScrollXYZ() | 36 | unknown |
| `0020d260` | pushMapScroll() | 36 | unknown |
| `0020d284` | popMapScroll() | 36 | unknown |
| `0020d580` | pushMapScale() | 36 | unknown |
| `0020d5a4` | popMapScale() | 36 | unknown |
| `0020def8` | setAnimationShadowOn(int) | 36 | unknown |
| `0020df1c` | setAnimationShadowOff(int) | 36 | unknown |
| `0020e6dc` | requestAnimationFlipON(int) | 36 | unknown |
| `0020e740` | setAnimationColorChangeOff(int) | 36 | unknown |
| `0020e764` | setAnimationColorChangeOn(int) | 36 | unknown |
| `0020e7b4` | setAnimationSoundOff(int) | 36 | unknown |
| `0020e7d8` | setAnimationSoundOn(int) | 36 | unknown |
| `0020f514` | stopAnimation() | 36 | unknown |
| `0020f550` | changeFlameRate(int) | 36 | unknown |
| `0020f928` | getAnimationCurrentFlame(unsigned int) | 36 | unknown |
| `00215c98` | fadeMapClut(int, unsigned short*) | 36 | unknown |
| `00216860` | stopMusic() | 36 | unknown |
| `00216e38` | iOS_RESUME_SET_WORK_MU_before_Battle(IOS_RESUME_DATA_WORK_MU*, IOS_RESUME_DATACOPY_MODE) | 36 | unknown |
| `0021b220` | SetEditANMPtr() | 36 | unknown |
| `0021b244` | SetEditTSQPtr() | 36 | unknown |
| `0021d26c` | s2a_initScheduleControl(_EffectTCB*) | 36 | unknown |
| `0021eb8c` | DoEffect() | 36 | unknown |
| `00260878` | ctlmoumes_active(CTLINFO*) | 36 | unknown |
| `0026089c` | ctlmoumes_deactive(CTLINFO*) | 36 | unknown |
| `00263fa8` | iOSSDNovelSysCurCheck() | 36 | unknown |
| `00269774` | snpl_jp() | 36 | unknown |
| `00269b08` | snpl_effmode() | 36 | unknown |
| `0026c238` | iOSNovelModeBackup() | 36 | unknown |
| `0026d774` | iOSTutoReset() | 36 | unknown |
| `00279c64` | MemCpyB(unsigned char*, unsigned char const*, int) | 36 | unknown |
| `0027c084` | iOS_CMenuTouch::getCursorPosLeft(int*, int*) | 36 | unknown |
| `0027c0a8` | iOS_CMenuTouch::getCursorPosRight(int*, int*) | 36 | unknown |
| `0027d92c` | iOS_CMenuTouchNum::setSprite() | 36 | unknown |
| `0027e680` | iOS_CMenuTouchSaveLoad::getCursorPosLeft(int*, int*) | 36 | unknown |
| `0027e6a4` | iOS_CMenuTouchSaveLoad::getCursorPosRight(int*, int*) | 36 | unknown |
| `0027fbf0` | iOS_WorldMapResumeGetData2(unsigned char**, unsigned int*) | 36 | unknown |
| `002806cc` | iOS_HookAddPrim() | 36 | unknown |
| `00281a08` | iOS_v2menuCheckSEError() | 36 | unknown |
| `002843ec` | VectorDataBase_ClearFlags() | 36 | unknown |
| `00284494` | Clear_VectorDataBase() | 36 | unknown |
| `00284d18` | pspBattleDataWorkInit() | 36 | unknown |
| `00285e1c` | pspJobIsSpecialJob(int) | 36 | unknown |
| `0028bad0` | TE_is_task_end(long) | 36 | unknown |
| `0028c644` | CFFT_STATE::FaceIDToFID(int) | 36 | unknown |
| `0028d228` | tlPopHeap() | 36 | unknown |
| `0028de28` | EnableEvent | 36 | unknown |
| `0028de4c` | DisableEvent | 36 | unknown |
| `0028e470` | CdIntToPos | 36 | unknown |
| `0028e494` | CdPosToInt | 36 | unknown |
| `0028e514` | xpLibcdIsExist() | 36 | unknown |
| `00291074` | PSX_LoadImage | 36 | unknown |
| `00291154` | StoreImage | 36 | unknown |
| `0029128c` | MoveImage | 36 | unknown |
| `002913bc` | SetPolyF3 | 36 | unknown |
| `002913e0` | SetPolyF4 | 36 | unknown |
| `00291404` | SetPolyFT3 | 36 | unknown |
| `00291450` | SetPolyG4 | 36 | unknown |
| `00291474` | SetPolyGT3 | 36 | unknown |
| `002914c0` | SetPolyG3 | 36 | unknown |
| `002914e4` | SetSprt | 36 | unknown |
| `00291508` | SetSprt16 | 36 | unknown |
| `0029152c` | SetSprt8 | 36 | unknown |
| `00291550` | SetLineF2 | 36 | unknown |
| `00291574` | SetLineG2 | 36 | unknown |
| `00291598` | SetLineF3 | 36 | unknown |
| `002915bc` | SetLineG3 | 36 | unknown |
| `002915e0` | SetLineF4 | 36 | unknown |
| `00291604` | SetLineG4 | 36 | unknown |
| `00291628` | SetTile | 36 | unknown |
| `0029164c` | SetTile1 | 36 | unknown |
| `00291670` | SetTile16 | 36 | unknown |
| `00291694` | SetTile8 | 36 | unknown |
| `00291800` | SetDrawMove | 36 | unknown |
| `00294e64` | GetDrawEnv | 36 | unknown |
| `00294eb0` | xpLibgpuDispEnvSet | 36 | unknown |
| `0029a834` | ClearImage | 36 | unknown |
| `0029ae4c` | xpLibGetScreen(RECT16*) | 36 | unknown |
| `0029b654` | GsSetClip2D | 36 | unknown |
| `0029fd34` | _gte_mvmva_b(long, long, long, long, long) | 36 | unknown |
| `0029fd58` | _gte_mvmva(long, long, long, long, long) | 36 | unknown |
| `002a0ae0` | TransMatrix | 36 | unknown |
| `002a1408` | SetFogFar | 36 | unknown |
| `002a334c` | pspSaveBase::SaveStart() | 36 | unknown |
| `002b02c8` | TexHybrid_Register(int) | 36 | unknown |
| `002b0324` | TexHybrid_GetTextureSize(int, int, float*, float*, float*, float*) | 36 | unknown |
| `002bf084` | iOS_setFaceDataMode(int) | 36 | unknown |
| `002cab50` | __floatunsidf | 36 | unknown |
| `002cb8a4` | __aeabi_cfrcmple | 36 | unknown |
| `002cd9e0` | _Unwind_RaiseException | 36 | unknown |
| `002cda04` | _Unwind_Resume | 36 | unknown |
| `002cda28` | ___Unwind_Resume_or_Rethrow | 36 | unknown |
| `002cda4c` | ___Unwind_ForcedUnwind | 36 | unknown |
| `002cda70` | ___Unwind_Backtrace | 36 | unknown |
| `000729c4` | Android_GetDeviceSize(int*, int*) | 32 | unknown |
| `000808f8` | unzGetGlobalInfo | 32 | unknown |
| `000834d4` | ogg_stream_destroy | 32 | unknown |
| `00083cfc` | ogg_sync_destroy | 32 | unknown |
| `00084770` | vorbis_bitrate_managed | 32 | unknown |
| `000a0844` | ov_raw_tell | 32 | unknown |
| `000a0864` | ov_pcm_tell | 32 | unknown |
| `000a27e4` | CG2D_LOADER::GetPixelByte() | 32 | unknown |
| `000a6fac` | CGX_SCREEN_CORRECT::Scaled(int) | 32 | unknown |
| `000a6fcc` | CGX_SCREEN_CORRECT::NonScaled(int) | 32 | unknown |
| `000a7078` | CGX_SCREEN_CORRECT::CorrectX(float) | 32 | unknown |
| `000a7098` | CGX_SCREEN_CORRECT::CorrectY(float) | 32 | unknown |
| `000a93dc` | CEGL2_IF::SetViewDir(math::VECTOR3<float> const&) | 32 | unknown |
| `000ab654` | CEGL2_SHADER::Init() | 32 | unknown |
| `000ad8e0` | CEGL2_SPRITE::SetColor(unsigned char, unsigned char, unsigned char) | 32 | unknown |
| `000b1bc8` | CEGL_PACKET::GetVBOBufferCurrent() | 32 | unknown |
| `000b3674` | CINPUT_DATA::SetKeyGroup(int, int, int) | 32 | unknown |
| `000b4708` | CINPUT_IF_TOUCH::~CINPUT_IF_TOUCH() | 32 | unknown |
| `000b66c8` | CFILE::Close() | 32 | unknown |
| `000b66e8` | CFILE::~CFILE() | 32 | unknown |
| `000b8bbc` | CLIST::SetData(int, void*) | 32 | unknown |
| `000bbc2c` | CSOUND_IF_SL::GetSLState(int) | 32 | unknown |
| `000c8158` | tool_writesquare(int, int, int) | 32 | unknown |
| `000c8178` | tool_readsquare(int, int, int) | 32 | unknown |
| `000d88fc` | stopmenutransfer() | 32 | unknown |
| `000d891c` | startmenutransfer() | 32 | unknown |
| `000da33c` | changeflame(int) | 32 | unknown |
| `000da700` | chk_nexteventtype(int) | 32 | unknown |
| `000e742c` | iOS_GetMenuMask() | 32 | unknown |
| `000e809c` | iOS_setsoundf(int*, int) | 32 | unknown |
| `001005cc` | Wstopmenutransfer() | 32 | unknown |
| `001005ec` | Wstartmenutransfer() | 32 | unknown |
| `001022cc` | Wchk_nexteventtype(int) | 32 | unknown |
| `00153450` | task_status(long) | 32 | unknown |
| `00153714` | Wtask_status(long) | 32 | unknown |
| `00153c64` | iOS_getOptionDispCameraIcon() | 32 | unknown |
| `00153c84` | iOS_updateDispCameraIconSetting() | 32 | unknown |
| `00155c8c` | stop_adventuremessage(int) | 32 | unknown |
| `0015832c` | rewrite_worldscroll(int) | 32 | unknown |
| `0015a590` | iOSSlideNaviCurGet() | 32 | unknown |
| `0015a5ec` | siOS_TCurGet(unsigned int) | 32 | unknown |
| `0015ad18` | iOSCurIsInGame(int, int) | 32 | unknown |
| `0015bf38` | iOSTchMovingModeCheck() | 32 | unknown |
| `0015c01c` | iOSTchHoseiControl() | 32 | unknown |
| `0015ef1c` | iOSUnitListMoveFlagResetSTA(unsigned char*) | 32 | unknown |
| `0016f774` | ASHURA_getOTptr() | 32 | unknown |
| `0016f820` | cCardEventClose() | 32 | unknown |
| `00173380` | cFadeInInit() | 32 | unknown |
| `001733a0` | cFadeOutInit() | 32 | unknown |
| `00173c58` | cDrawMessageKill(int) | 32 | unknown |
| `00178720` | bFadeInInit() | 32 | unknown |
| `0018370c` | CardEventClose() | 32 | unknown |
| `0018f264` | eDrawMessageKill(int) | 32 | unknown |
| `001adc48` | FadeCondition() | 32 | unknown |
| `001b7000` | DrawMessageKill(int) | 32 | unknown |
| `001b9334` | iOSTutoBtlSkipClear() | 32 | unknown |
| `001b9d84` | iOS_clearTutorialbreak() | 32 | unknown |
| `001d66f8` | set_td(unsigned char*) | 32 | unknown |
| `001d98a8` | get_shape2_plus(BWORK*, unsigned char*) | 32 | unknown |
| `001d9910` | get_ability_flag(BWORK*, int) | 32 | unknown |
| `001d9948` | copy_struct_data(void const*, void*, int) | 32 | unknown |
| `001da018` | clear_cmemory(void*, int) | 32 | unknown |
| `001ef5ac` | requestDefaultTransparency(tag_animation*) | 32 | unknown |
| `001ffb30` | callAnimationSound(tag_animation*, int) | 32 | unknown |
| `00202efc` | iOS_BattleEventCheck() | 32 | unknown |
| `002044e0` | iOSpreCommandInit() | 32 | unknown |
| `002064a8` | iOS_IsEnableMenuItemTouch() | 32 | unknown |
| `0020696c` | iOS_IsEnableFlicker() | 32 | unknown |
| `0020e700` | setAnimationHFlip(int) | 32 | unknown |
| `0020e720` | resetAnimationHFlip(int) | 32 | unknown |
| `0020f6c0` | startModelAnimation(int, int) | 32 | unknown |
| `0020f6f4` | startVRAMAnimation(int, int) | 32 | unknown |
| `0020f8cc` | setFrameRate(int) | 32 | unknown |
| `0020f908` | getAnimationSequence(unsigned int) | 32 | unknown |
| `002119a0` | ResetChangePalette() | 32 | unknown |
| `0021b8a4` | PushGravity() | 32 | unknown |
| `0021bcd8` | s0_end(_EffectTCB*) | 32 | unknown |
| `0021bcf8` | s1_goto(_EffectTCB*) | 32 | unknown |
| `0021c31c` | s9_pushMapScrollXYZ(_EffectTCB*) | 32 | unknown |
| `0021c33c` | sa_popMapScrollXYZ(_EffectTCB*) | 32 | unknown |
| `0021c3ac` | sc_pushMapAngle(_EffectTCB*) | 32 | unknown |
| `0021c3cc` | sd_popMapAngle(_EffectTCB*) | 32 | unknown |
| `0021c434` | sf_pushMapScale(_EffectTCB*) | 32 | unknown |
| `0021c454` | s24_popMapScale(_EffectTCB*) | 32 | unknown |
| `0021cedc` | UnlockEffect() | 32 | unknown |
| `0021cefc` | LockEffectCompelBreak() | 32 | unknown |
| `0021d2c0` | s2b_initMetascheduleControl(_EffectTCB*) | 32 | unknown |
| `0021f308` | PermanentEffectEndRequest(unsigned char) | 32 | unknown |
| `00228e44` | DisposeShape2(Shape2*) | 32 | unknown |
| `0022a2cc` | getAbsoluteMaximumOf2(short, short) | 32 | unknown |
| `0024c534` | bgscrol_chk(_POINT*, VECTOR*) | 32 | unknown |
| `0024f4b0` | ctltips_active(CTLINFO*) | 32 | unknown |
| `002649d0` | iOS_setNobelMesRect(int, int, int, int) | 32 | unknown |
| `002657d8` | backpage_put(CTLINFO*, int) | 32 | unknown |
| `0026df10` | ctlhentuto_active(CTLINFO*) | 32 | unknown |
| `00270500` | curhis_clr(int) | 32 | unknown |
| `0027b5cc` | iOS_setHalftoneSize(RECT16*) | 32 | unknown |
| `0027b608` | iOS_setPanelCursorRect(int, int, int, int) | 32 | unknown |
| `0027b628` | iOS_getPanelCursorRect(RECT16*) | 32 | unknown |
| `0027f620` | iOS_ResumeGetData(unsigned char**, unsigned int*) | 32 | unknown |
| `00280770` | iOS_chkclipoffNoFT4(int) | 32 | unknown |
| `00280790` | iOS_chkclipoffNoFT3(int) | 32 | unknown |
| `0028080c` | IOS_PSP2IOS_X(int) | 32 | unknown |
| `0028082c` | IOS_PSP2IOS_Y(int) | 32 | unknown |
| `00280870` | iOS_getTransFace(int) | 32 | unknown |
| `00280890` | iOS_getTransFace2(int) | 32 | unknown |
| `002808f8` | iOS_getTransFaceAT(int) | 32 | unknown |
| `00280938` | iOS_getTransFaceEVT(int) | 32 | unknown |
| `00280958` | iOS_getTransFaceEVT2(int) | 32 | unknown |
| `002809a8` | iOS_getTpageForNum() | 32 | unknown |
| `00286974` | pspNetInitializeBattleData() | 32 | unknown |
| `00288a58` | pspPrimDirectParamSet(int, RECT16*) | 32 | unknown |
| `00289ba8` | pspSaveDataMissionRateSave(FFT_SAVE_DATA*) | 32 | unknown |
| `00289bc8` | pspSaveDataEnableSystemFlg(FFTPSP_SYSTEM_FLG) | 32 | unknown |
| `0028b610` | initXpHeap() | 32 | unknown |
| `0028ba84` | TE_task_start(long) | 32 | unknown |
| `0028ce58` | sceCtrlPeekBufferPositive | 32 | unknown |
| `0028df90` | xpLibapiGameDataSet | 32 | unknown |
| `0028dfb0` | xpLibapiTitleStrSet | 32 | unknown |
| `0028dfd0` | xpLibapiIcon0DataSet | 32 | unknown |
| `0028dff0` | xpLibapiBackGoundPic1DataSet | 32 | unknown |
| `0028e4c0` | xpLibcdInit() | 32 | unknown |
| `00294e44` | GetDispEnv | 32 | unknown |
| `00295548` | xpLibgpuOffScreenPartBlockSet | 32 | unknown |
| `0029ae70` | xpLib_GetTPage(int*) | 32 | unknown |
| `0029c934` | sceVfpuVector4Set(ScePspFVector4*, float, float, float, float) | 32 | unknown |
| `0029ca08` | _gte_ldv0(SVECTOR*) | 32 | unknown |
| `0029ca28` | _gte_ldv1(SVECTOR*) | 32 | unknown |
| `0029ca48` | _gte_ldv2(SVECTOR*) | 32 | unknown |
| `0029cc78` | _gte_ldbv(char*) | 32 | unknown |
| `0029cd98` | _gte_ldsz4(long, long, long, long) | 32 | unknown |
| `0029cfd0` | _gte_ldsvllrow0(SVECTOR*) | 32 | unknown |
| `0029d028` | _gte_ldsvlcrow0(SVECTOR*) | 32 | unknown |
| `0029d178` | _gte_ld_intpol_uv0(char*) | 32 | unknown |
| `0029d198` | _gte_ld_intpol_uv1(char*) | 32 | unknown |
| `0029d1b8` | _gte_ld_intpol_bv0(char*) | 32 | unknown |
| `0029d1d8` | _gte_ld_intpol_bv1(char*) | 32 | unknown |
| `0029d3a0` | _gte_stsxy01(long*, long*) | 32 | unknown |
| `0029d3c0` | _gte_stsxy01c(long*) | 32 | unknown |
| `0029d77c` | _gte_stbv(char*) | 32 | unknown |
| `0029d8a4` | _gte_ReadGeomOffset(long*, long*) | 32 | unknown |
| `002a0a80` | ApplyRotMatrix | 32 | unknown |
| `002a1108` | Square0 | 32 | unknown |
| `002a1128` | Square12 | 32 | unknown |
| `002a1350` | ReadGeomOffset | 32 | unknown |
| `002a2c70` | PCread | 32 | unknown |
| `002a2ca8` | PClseek | 32 | unknown |
| `002a2ce0` | PCwrite | 32 | unknown |
| `002a2f98` | xpLibSN::PCcreat(char*, int) | 32 | unknown |
| `002ae8c0` | GlTexEnv_GetSprite(int) | 32 | unknown |
| `002ae8e0` | GlTexEnv_GetTextureHandle(int) | 32 | unknown |
| `002b01e0` | GlTexEnv_GetTextureHandle_2X(int) | 32 | unknown |
| `002b0400` | CAPP_INFO::CAPP_INFO() | 32 | unknown |
| `002b06b4` | CDebugPrint::CDebugPrint() | 32 | unknown |
| `002b06d4` | CDebugPrint::EngineUninit() | 32 | unknown |
| `002b2358` | Music_Play(int, int, int, int) | 32 | unknown |
| `002b871c` | iOS_isTouchBegan() | 32 | unknown |
| `002b9cac` | iOS_setV2Icon(V2ICON_DATA, int) | 32 | unknown |
| `002ca77c` | __aeabi_uidivmod | 32 | unknown |
| `002ca878` | __aeabi_idivmod | 32 | unknown |
| `002cb48c` | __aeabi_i2f | 32 | unknown |
| `002ccf74` | __gnu_Unwind_Resume_or_Rethrow | 32 | unknown |
| `002ccf98` | _Unwind_DeleteException | 32 | unknown |
| `000726e0` | JNI_OnLoad | 28 | unknown |
| `0007276c` | Java_com_square_1enix_FFT_1Android_GL2JNILib_onResume | 28 | unknown |
| `000727b4` | Java_com_square_1enix_FFT_1Android_GL2JNILib_onDestroy | 28 | unknown |
| `00073ad4` | compress | 28 | unknown |
| `0007d894` | call_zopen64 | 28 | unknown |
| `000821f8` | unzOpenCurrentFile2 | 28 | unknown |
| `00082344` | unzGetOffset | 28 | unknown |
| `00082fd8` | oggpack_bytes | 28 | unknown |
| `00083c84` | ogg_stream_eos | 28 | unknown |
| `000a2804` | CG2D_LOADER::GetPixelCount() | 28 | unknown |
| `000a7034` | CGX_SCREEN_CORRECT::GetOffset_1X(float*, float*) | 28 | unknown |
| `000a9414` | CEGL2_IF::~CEGL2_IF() | 28 | unknown |
| `000abc1c` | CEGL2_SHADER::~CEGL2_SHADER() | 28 | unknown |
| `000aef38` | CEGL2_TEX_HYBRID::UV_UnregistAll() | 28 | unknown |
| `000af9a0` | CCAMERA::Init(float, float) | 28 | unknown |
| `000afa20` | CCAMERA::~CCAMERA() | 28 | unknown |
| `000b1964` | CEGL_PACKET::~CEGL_PACKET() | 28 | unknown |
| `000b5420` | CRECT::GetDrawRect(int, _RECT_S32*) | 28 | unknown |
| `000b543c` | CRECT::SetDrawRect(int, _RECT_S32*) | 28 | unknown |
| `000b61e4` | CCOMP_Z_DEC::CCOMP_Z_DEC() | 28 | unknown |
| `000b63b0` | CCOMP_Z_ENC::CCOMP_Z_ENC() | 28 | unknown |
| `000b6810` | CFILE::SetTime(_SYSTEMTIME*) | 28 | unknown |
| `000b6b60` | CFILE_DAT::~CFILE_DAT() | 28 | unknown |
| `000b7090` | CFILE_TXT::GetDataAsInt(int, int, unsigned int) | 28 | unknown |
| `000b8a58` | CLIST::GetDataAsInt(int) | 28 | unknown |
| `000b9e78` | CTHREAD::CTHREAD() | 28 | unknown |
| `000b9e94` | CTHREAD::Create(int) | 28 | unknown |
| `000bb6cc` | CSOUND_IF_SL::CSOUND_IF_SL() | 28 | unknown |
| `000bbac8` | CSOUND_IF_SL::GetPlaySec(int) | 28 | unknown |
| `000bcc04` | CSOUND_LOADER_PCM::Tell() const | 28 | unknown |
| `000bcc70` | CSOUND_LOADER_PCM::GetFormatDecoded() const | 28 | unknown |
| `000bcca4` | CSOUND_LOADER_PCM::GetTotalDecoded() const | 28 | unknown |
| `000bce3c` | CSOUND_LOADER_PCM::~CSOUND_LOADER_PCM() | 28 | unknown |
| `000bd170` | CSOUND_LOADER_OGG::GetFormatDecoded() const | 28 | unknown |
| `000bd504` | CSOUND_LOADER_OGG::~CSOUND_LOADER_OGG() | 28 | unknown |
| `000bdd38` | CSTEP::Pause(int) | 28 | unknown |
| `000bdd54` | CSTEP::Uninit() | 28 | unknown |
| `000be1e8` | CSTEP_BATCH::~CSTEP_BATCH() | 28 | unknown |
| `000d961c` | setplatetime(int) | 28 | unknown |
| `000d9748` | iOS_battle_scrollwindow_tap() | 28 | unknown |
| `000daae8` | hook_wipe() | 28 | unknown |
| `000e628c` | Get_bravebreak() | 28 | unknown |
| `000e62a8` | Set_bravebreak(unsigned short) | 28 | unknown |
| `00101434` | Wsetplatetime(int) | 28 | unknown |
| `0010155c` | WiOS_battle_scrollwindow_tap() | 28 | unknown |
| `00101fa4` | Wchangeflame(int) | 28 | unknown |
| `00155854` | set_worldday(int, int) | 28 | unknown |
| `00155870` | set_worldmoney(int) | 28 | unknown |
| `00155c5c` | ret_optionstatus() | 28 | unknown |
| `00159a54` | asmGetActiveTask(int) | 28 | unknown |
| `0015a41c` | iOSBtlFreeCurCheck() | 28 | unknown |
| `0015efd4` | iOSUnitListCurSave_W(int, int) | 28 | unknown |
| `00160d0c` | iOSYajiEffectGetX(int) | 28 | unknown |
| `00160d28` | iOSYajiEffectGetY(int) | 28 | unknown |
| `00160d44` | iOSYajiEffectGetCount(int) | 28 | unknown |
| `00161414` | iOSSdNovelSetFlag(int, int) | 28 | unknown |
| `00161454` | iOSSdNovelGetX(int) | 28 | unknown |
| `00161470` | iOSSdNovelGetY(int) | 28 | unknown |
| `0016148c` | iOSSdNovelGetCount(int) | 28 | unknown |
| `001614a8` | iOSSdNovelGetAlpha(int) | 28 | unknown |
| `001614ec` | iOSSdNovelGetSizeW(int) | 28 | unknown |
| `00161508` | iOSSdNovelGetSizeH(int) | 28 | unknown |
| `00161768` | iOSTgaIconSetFlag(int, int) | 28 | unknown |
| `001617cc` | iOSTgaIconGetX(int) | 28 | unknown |
| `001617e8` | iOSTgaIconGetY(int) | 28 | unknown |
| `00161804` | iOSTgaIconGetCount(int) | 28 | unknown |
| `00161820` | iOSTgaIconGetAlpha(int) | 28 | unknown |
| `0016183c` | iOSTgaIconGetSizeW(int) | 28 | unknown |
| `00161858` | iOSTgaIconGetSizeH(int) | 28 | unknown |
| `00161874` | iOSTgaIconSetX(int, int) | 28 | unknown |
| `00161890` | iOSTgaIconSetY(int, int) | 28 | unknown |
| `001618ac` | iOSTgaIconSetCount(int, int) | 28 | unknown |
| `001618c8` | iOSTgaIconSetAlpha(int, int) | 28 | unknown |
| `001618e4` | iOSTgaIconSetSizeW(int, int) | 28 | unknown |
| `00161900` | iOSTgaIconSetSizeH(int, int) | 28 | unknown |
| `00162028` | wasmGetActiveTask(int) | 28 | unknown |
| `00173364` | cGetFadeStatus() | 28 | unknown |
| `001744b0` | cSetBitStream(unsigned char*) | 28 | unknown |
| `001744cc` | cSetBitStream2(unsigned char*) | 28 | unknown |
| `00178704` | bGetFadeStatus() | 28 | unknown |
| `00178968` | bWaitLoadImage(RECT16*, unsigned char*) | 28 | unknown |
| `00178984` | bWaitStoreImage(RECT16*, unsigned char*) | 28 | unknown |
| `001789a0` | bWaitMoveImage(RECT16*, short, short) | 28 | unknown |
| `0017b2f8` | bSetMenuSelSide(unsigned char, short) | 28 | unknown |
| `0017b594` | bSetBitStream(unsigned char*) | 28 | unknown |
| `001800ac` | bWindowPositionInit() | 28 | unknown |
| `0018378c` | fileclose(unsigned int) | 28 | unknown |
| `001898d4` | eCopyChrStts(short, short) | 28 | unknown |
| `001898f0` | eNitoryu(short) | 28 | unknown |
| `00189b54` | eRyoute(short) | 28 | unknown |
| `0018ab00` | eWaitLoadImage(RECT16*, unsigned char*) | 28 | unknown |
| `0018ab1c` | eWaitStoreImage(RECT16*, unsigned char*) | 28 | unknown |
| `0018ab38` | eWaitMoveImage(RECT16*, short, short) | 28 | unknown |
| `0018ab54` | iOS_getOt_equip(int) | 28 | unknown |
| `0018f9d0` | eSetMenuSelVertical(unsigned char, short) | 28 | unknown |
| `0018fa04` | eSetMenuSelSide(unsigned char, short) | 28 | unknown |
| `0018fdfc` | eSetBitStream(unsigned char*) | 28 | unknown |
| `0018fe18` | eSetBitStream2(unsigned char*) | 28 | unknown |
| `001948a4` | jWaitLoadImage(RECT16*, unsigned char*) | 28 | unknown |
| `001948c0` | jWaitStoreImage(RECT16*, unsigned char*) | 28 | unknown |
| `00196ea0` | MenuSelSideDirect(unsigned char, unsigned char) | 28 | unknown |
| `00196ebc` | jSetBitStream(unsigned char*) | 28 | unknown |
| `00196ed8` | jSetBitStream2(unsigned char*) | 28 | unknown |
| `001a85cc` | Nitoryu(short) | 28 | unknown |
| `001a85e8` | Ryoute(short) | 28 | unknown |
| `001a8604` | Mituryo(short) | 28 | unknown |
| `001abf04` | CopyChrStts(short, short) | 28 | unknown |
| `001adc7c` | WaitLoadImage(RECT16*, unsigned char*) | 28 | unknown |
| `001adc98` | WaitStoreImage(RECT16*, unsigned char*) | 28 | unknown |
| `001adcb4` | WaitMoveImage(RECT16*, short, short) | 28 | unknown |
| `001adcd0` | iOS_getMasaCdbOt_graphics_unitlist(int) | 28 | unknown |
| `001b70f4` | DrawMessageWithPosition(int, COMRECORD*, int) | 28 | unknown |
| `001b7abc` | SetMenuSelVertical(unsigned char, short) | 28 | unknown |
| `001b7ad8` | SetMenuSelSide(unsigned char, short) | 28 | unknown |
| `001b87b4` | SetBitStream(unsigned char*) | 28 | unknown |
| `001b87d0` | SetBitStream2(unsigned char*) | 28 | unknown |
| `001c03e0` | WindowPositionInit() | 28 | unknown |
| `001c0784` | iOS_GetTouchStartUnitNo() | 28 | unknown |
| `001c7218` | TEST_TEST() | 28 | unknown |
| `001ca938` | net_setknockback(unsigned char, unsigned char, unsigned char) | 28 | unknown |
| `001cd548` | _changeAnimationStatus_(int, int, int) | 28 | unknown |
| `001d357c` | set_playerwork2(PENTRY*, unsigned char*) | 28 | unknown |
| `001d751c` | erase_unit(int) | 28 | unknown |
| `001d9354` | set_jcflag(unsigned char*, int) | 28 | unknown |
| `001fd8d8` | requestDamageResult(int) | 28 | unknown |
| `001fe6fc` | requestDamageResultFromBattleID(int) | 28 | unknown |
| `0020177c` | reserveActionDirection(tag_animation*) | 28 | unknown |
| `00202ee0` | isInputEnable() | 28 | unknown |
| `0020cbb8` | fileReadRequest(unsigned long, unsigned long, void*) | 28 | unknown |
| `0020e164` | getAnimationPosition(unsigned int) | 28 | unknown |
| `0020e180` | getAnimationPositionFromBattleID(unsigned int) | 28 | unknown |
| `0020e694` | checkAnimationExist(int) | 28 | unknown |
| `0020e8c0` | getAnimationAction(int) | 28 | unknown |
| `0021f2ec` | GetPEffectStatus(unsigned char) | 28 | unknown |
| `0022a95c` | EqualSVectorToVECTOR(SVector*, VECTOR*) | 28 | unknown |
| `0022a978` | EqualSVectorToSVECTOR(SVector*, SVECTOR*) | 28 | unknown |
| `002419a8` | doublespeed_chk(CDREC*) | 28 | unknown |
| `0024b080` | wldbinEntry() | 28 | unknown |
| `0024d948` | iOS_BRST_CHECK() | 28 | unknown |
| `002541a8` | iOSWldMapZoomGet() | 28 | unknown |
| `00258ac8` | evt_skip1() | 28 | unknown |
| `00258ae4` | evt_skip2() | 28 | unknown |
| `00258b00` | evt_skip3() | 28 | unknown |
| `00258b1c` | evt_skip4() | 28 | unknown |
| `00258b38` | evt_item() | 28 | unknown |
| `00258b54` | evt_eqp() | 28 | unknown |
| `0026973c` | snpl_endpage() | 28 | unknown |
| `00269758` | snpl_startpage() | 28 | unknown |
| `0026c25c` | iOSNovelModeRestore() | 28 | unknown |
| `0026d7d0` | iOSTutoFlagAdd(int) | 28 | unknown |
| `0026ef20` | iOSTutoHenseiBattleFadeCheck() | 28 | unknown |
| `00271324` | Ssd_PlayEffects01(long, long) | 28 | unknown |
| `00279f68` | JudgeTimeOut() | 28 | unknown |
| `0027b5ec` | iOS_getHalftoneSize(RECT16*) | 28 | unknown |
| `0027d404` | iOS_CMenuTouch::setDispAssist(int) | 28 | unknown |
| `00281678` | iOS_v2menuGetItem() | 28 | unknown |
| `00284bc8` | pspBattleGetEvent() | 28 | unknown |
| `00284be4` | pspBattleDisableFlg(unsigned int) | 28 | unknown |
| `00284c00` | pspBattleEnableFlg(unsigned int) | 28 | unknown |
| `00284cb0` | pspBattleDataPadSet(unsigned short) | 28 | unknown |
| `00284d3c` | pspBattleDataForceParticipationEventNoSet(int) | 28 | unknown |
| `00285558` | pspItemGetOptionData | 28 | unknown |
| `0028712c` | pspNetTrapSetTable(char, char, int) | 28 | unknown |
| `002885b8` | pspOpenDisableFlg(PSP_OPEN_FLG) | 28 | unknown |
| `002885d4` | pspOpenEnableFlg(PSP_OPEN_FLG) | 28 | unknown |
| `00289b8c` | pspSaveDataMissionRateLoad(FFT_SAVE_DATA*) | 28 | unknown |
| `00289be8` | pspSaveDataDisableSystemFlg(FFTPSP_SYSTEM_FLG) | 28 | unknown |
| `0028b018` | pspWorldEnableFlg(PSP_WORLD_FLG) | 28 | unknown |
| `0028b034` | pspWorldDisableFlg(PSP_WORLD_FLG) | 28 | unknown |
| `0028da90` | tlMallocErrorFunc(void (*)(TL_MALLOC_ERROR)) | 28 | unknown |
| `0028e5c4` | VSyncCallback | 28 | unknown |
| `0028e6d4` | xpSetWaitVSyncFunc(int (*)()) | 28 | unknown |
| `00290e6c` | DrawSyncCallback | 28 | unknown |
| `00291bc0` | PutDrawEnv | 28 | unknown |
| `00291bdc` | xpLibgpuIsRender | 28 | unknown |
| `00291c2c` | xpLibgpuEnableFlg | 28 | unknown |
| `00291ec0` | xpLibgpuDisableFlg | 28 | unknown |
| `00294e14` | xpLibgpuClutNumGet | 28 | unknown |
| `0029b3f0` | GsClearDispArea | 28 | unknown |
| `0029c918` | xpLibgsDrawEnvGet | 28 | unknown |
| `0029cd38` | _gte_ldsxy3(long, long, long) | 28 | unknown |
| `0029cd7c` | _gte_ldsz3(long, long, long) | 28 | unknown |
| `0029ce64` | _gte_ldbkdir(long, long, long) | 28 | unknown |
| `0029cea8` | _gte_ldfcdir(long, long, long) | 28 | unknown |
| `0029d550` | _gte_stflg_4(long*) | 28 | unknown |
| `0029fea0` | rcos | 28 | unknown |
| `0029fed4` | PSX_ccos | 28 | unknown |
| `002a1440` | SetLightMatrix | 28 | unknown |
| `002a148c` | SetColorMatrix | 28 | unknown |
| `002a1534` | LightColor | 28 | unknown |
| `002a1550` | LocalLight | 28 | unknown |
| `002a1974` | NormalColorCol_nom | 28 | unknown |
| `002a19a8` | NormalColorCol3_nom | 28 | unknown |
| `002a2a4c` | xpPadKeyBufGet | 28 | unknown |
| `002a2b10` | xpPadDebugSet | 28 | unknown |
| `002a348c` | pspSaveBase::UserIdSet(int) | 28 | unknown |
| `002a3780` | pspSaveBase::ErrorMsgStrGet(unsigned int) | 28 | unknown |
| `002acb2c` | GuEmu_GetRAW(int) | 28 | unknown |
| `002b02ec` | TexHybrid_RegistCLUTAddr(int, unsigned int) | 28 | unknown |
| `002b0308` | TexHybrid_GetTextureHandle(int, int) | 28 | unknown |
| `002b06f4` | CDebugPrint::~CDebugPrint() | 28 | unknown |
| `002b1bb0` | AppEngine_Dialog_OnClose(int) | 28 | unknown |
| `002b1bcc` | NowLoading_Bootup() | 28 | unknown |
| `002b242c` | Music_IsPlaying() | 28 | unknown |
| `002b7034` | iOSCancelButtonCheck() | 28 | unknown |
| `002befa0` | iOS_OrMenuTouchKeyInput(unsigned int) | 28 | unknown |
| `002bf1dc` | iOS_hook_faceload(int) | 28 | unknown |
| `002ccee4` | __gnu_Unwind_ForcedUnwind | 28 | unknown |
| `002cdeec` | _Unwind_GetLanguageSpecificData | 28 | unknown |
| `000728f8` | Java_com_square_1enix_FFT_1Android_GL2JNILib_onKeyEvent | 24 | unknown |
| `000732ac` | Android_Accelerometer_Get(int) | 24 | unknown |
| `000823ec` | zError | 24 | unknown |
| `000826ec` | oggpack_writealign | 24 | unknown |
| `00082880` | oggpackB_writealign | 24 | unknown |
| `00098b8c` | vorbis_book_codeword | 24 | unknown |
| `00098ba4` | vorbis_book_codelen | 24 | unknown |
| `0009e8e8` | ov_halfrate_p | 24 | unknown |
| `000a62a4` | CG2D_LOADER_TIM::GetSavePixelFormatInfo(_G2D_SAVE_INFO*) | 24 | unknown |
| `000a6d9c` | CGX_SCREEN_CORRECT::CGX_SCREEN_CORRECT() | 24 | unknown |
| `000a7eac` | CEGL2_IF::ClearZ(float) | 24 | unknown |
| `000aba08` | CEGL2_SHADER::GetUniformIndex(int) | 24 | unknown |
| `000ad9fc` | CEGL2_SPRITE::~CEGL2_SPRITE() | 24 | unknown |
| `000b1bfc` | CEGL_PACKET::SetVBOInfoCurrent(int, int) | 24 | unknown |
| `000b3594` | CINPUT_DATA::SetKeyNum(int, int) | 24 | unknown |
| `000b9d8c` | CWORK_MEM::~CWORK_MEM() | 24 | unknown |
| `000bcbd8` | CSOUND_LOADER::~CSOUND_LOADER() | 24 | unknown |
| `000bcc8c` | CSOUND_LOADER_PCM::GetTotal() const | 24 | unknown |
| `000bdd84` | CSTEP::GetEndF() | 24 | unknown |
| `000be428` | CSTEP_BATCH::GetProgressInverse() | 24 | unknown |
| `000c8138` | return_pentry() | 24 | unknown |
| `000c8198` | tool_squarecursor(int, int) | 24 | unknown |
| `000cbb30` | resetYLine() | 24 | unknown |
| `000cbd78` | pspEntrySquareDataGet() | 24 | unknown |
| `000d9764` | iOS_set_status_pad(unsigned long*) | 24 | unknown |
| `000d9ed4` | request_startextend() | 24 | unknown |
| `000da31c` | request_turnwindowrestart() | 24 | unknown |
| `000da5f8` | return_actionstructure() | 24 | unknown |
| `000da808` | whatweather() | 24 | unknown |
| `000ddd48` | tutorial_padcontrol(int*) | 24 | unknown |
| `000e0fa0` | loadcdst(int, int) | 24 | unknown |
| `00101578` | WiOS_set_status_pad(unsigned long*) | 24 | unknown |
| `00101b90` | Wrequest_startextend() | 24 | unknown |
| `00101f84` | Wrequest_turnwindowrestart() | 24 | unknown |
| `001024e4` | Wwhatweather() | 24 | unknown |
| `0010729c` | Wtutorial_padcontrol(int*) | 24 | unknown |
| `0010fa04` | Wloadcdst(int, int) | 24 | unknown |
| `00150690` | setNetErrorCutFlg() | 24 | unknown |
| `001506bc` | rsetNetErrorCutFlg() | 24 | unknown |
| `001506d4` | SetgMission_Successflg() | 24 | unknown |
| `001531cc` | ResetgMission_Successflg() | 24 | unknown |
| `001556f0` | worldcursorposset(int) | 24 | unknown |
| `00155d70` | reactive_worldstatus() | 24 | unknown |
| `00155dd4` | active_worldstatus() | 24 | unknown |
| `00155dec` | teach_onocursor(int, int) | 24 | unknown |
| `0015a4c4` | iOSSlideNaviCurClear() | 24 | unknown |
| `0015a72c` | iOSScrollButtonDTap() | 24 | unknown |
| `0015a8b4` | iOSRotateButtonDTap() | 24 | unknown |
| `0015b328` | iOSSlideIconReset() | 24 | unknown |
| `0015d264` | iOSRotAutoSet() | 24 | unknown |
| `0015d27c` | iOSRotAutoReset() | 24 | unknown |
| `0015eedc` | iOSUnitListMoveFlagSet() | 24 | unknown |
| `0015eef4` | iOSUnitListMoveFlagClear() | 24 | unknown |
| `0015ff88` | iOSCircleCtrl(unsigned short) | 24 | unknown |
| `00161e60` | iOSSetRotMode() | 24 | unknown |
| `00183454` | bScrollWindowInit(short*, int, unsigned char*, unsigned char*) | 24 | unknown |
| `0018346c` | bScrollWindowInit2(short*, int, int, unsigned char*, unsigned char*) | 24 | unknown |
| `00188e54` | eGetTotalItem(short) | 24 | unknown |
| `00188e6c` | eGetItemSmallCategory(short) | 24 | unknown |
| `0018f9ec` | eGetMenuSelVertical(unsigned char) | 24 | unknown |
| `00191d18` | eScrollWindowInit2(short*, int, int, unsigned char*, unsigned char*) | 24 | unknown |
| `00192c74` | eScrollWindowInit(short*, int, unsigned char*, unsigned char*) | 24 | unknown |
| `00198580` | jScrollWindowInit2(short*, int, int, unsigned char*, unsigned char*) | 24 | unknown |
| `0019946c` | jScrollWindowInit(short*, int, unsigned char*, unsigned char*) | 24 | unknown |
| `001a9228` | GetItemPrice(short) | 24 | unknown |
| `001a9554` | GetItemSmallCategory(short) | 24 | unknown |
| `001b879c` | GetMenuSelVertical(unsigned char) | 24 | unknown |
| `001c6f2c` | ScrollWindowInit(short*, int, unsigned char*, unsigned char*) | 24 | unknown |
| `001c6f44` | ScrollWindowInit2(short*, int, int, unsigned char*, unsigned char*) | 24 | unknown |
| `001d9930` | copyACTst(ACT*, ACT*) | 24 | unknown |
| `001ed94c` | getDirectionVector(int) | 24 | unknown |
| `001eee48` | getShapeWaitType(unsigned short) | 24 | unknown |
| `001fd2ac` | resetTurnOrder() | 24 | unknown |
| `0020dba4` | requestStandingAnimation(unsigned int) | 24 | unknown |
| `0020dbbc` | requestWalkingAnimation(unsigned int) | 24 | unknown |
| `0020dbd4` | requestStanderdAnimation(unsigned int) | 24 | unknown |
| `0020e210` | getAnimationPriority(unsigned short, SVECTOR*) | 24 | unknown |
| `0020f2b4` | getAnimationHeight(int) | 24 | unknown |
| `0020f2cc` | getAnimationHeightFromBattleID(int) | 24 | unknown |
| `0020f4fc` | clearOverSpecCtr() | 24 | unknown |
| `0020f538` | restartAnimation() | 24 | unknown |
| `0020f6a8` | eventMapRewriteWait() | 24 | unknown |
| `0020f8a0` | finishAttackTeamSelect() | 24 | unknown |
| `0020f8ec` | resetFrameRate() | 24 | unknown |
| `0020ffec` | iOS_InitializeHot2() | 24 | unknown |
| `002160f4` | ps_main() | 24 | unknown |
| `00216110` | iOS_setTexCacheLine(int) | 24 | unknown |
| `00216128` | iOS_resetTexCacheLine() | 24 | unknown |
| `00216848` | getMusicPointer(int) | 24 | unknown |
| `00218628` | SetAnimationMode(effectAnimation*, short) | 24 | unknown |
| `0021b4f4` | largeFileRead(long, char*, unsigned long) | 24 | unknown |
| `0021b8f0` | PushAirDensity() | 24 | unknown |
| `0021b908` | PopAirDensity() | 24 | unknown |
| `0021c1e4` | s2c_samplingMSQFrame(_EffectTCB*) | 24 | unknown |
| `0021c1fc` | s2d_samplingSQLFrame(_EffectTCB*) | 24 | unknown |
| `0021c214` | dmyFnc(_EffectTCB*) | 24 | unknown |
| `00228c44` | CreateObjectWithTableWithParentData(short, int, int, int, _Object*) | 24 | unknown |
| `00228c5c` | OgataInit() | 24 | unknown |
| `00245a40` | strKickCD(CdlLOC*) | 24 | unknown |
| `00248598` | iOS_TestDraw(unsigned long*) | 24 | unknown |
| `0024dcc0` | ctlkiroku_deactive(CTLINFO*) | 24 | unknown |
| `0024e904` | ctlperson_deactive(CTLINFO*) | 24 | unknown |
| `0024f4d0` | ctltips_deactive(CTLINFO*) | 24 | unknown |
| `002558f0` | iOSWld_Help_Town() | 24 | unknown |
| `002564e8` | ctlsthelp_deactive(CTLINFO*) | 24 | unknown |
| `00259750` | ctlhistory_active(CTLINFO*) | 24 | unknown |
| `00259768` | ctlhistory_deactive(CTLINFO*) | 24 | unknown |
| `00259ea4` | ctlhouk_deactive(CTLINFO*) | 24 | unknown |
| `0025e294` | mkadrtbl_calc(int) | 24 | unknown |
| `0025ffe0` | iOS_IsTutoStart() | 24 | unknown |
| `002602f4` | ctlmouke_deactive(CTLINFO*) | 24 | unknown |
| `002675f4` | ctlret_deactive(CTLINFO*) | 24 | unknown |
| `0026a85c` | envSound_play(int) | 24 | unknown |
| `0026c400` | ctltresure_deactive(CTLINFO*) | 24 | unknown |
| `0026df30` | ctlhentuto_deactive(CTLINFO*) | 24 | unknown |
| `0026ec30` | ctlsentuto_deactive(CTLINFO*) | 24 | unknown |
| `0026f0a4` | ctlunreg_deactive(CTLINFO*) | 24 | unknown |
| `0026fac0` | ctluwa_deactive(CTLINFO*) | 24 | unknown |
| `00271284` | Ssd_Init(unsigned short) | 24 | unknown |
| `00279ed4` | ClearForBattleRoutine() | 24 | unknown |
| `0027d468` | disableCancelDisableArea() | 24 | unknown |
| `0027e6e4` | iOS_CMenuTouchSaveLoad::setYLine(int) | 24 | unknown |
| `0027f134` | iOS_SetRectHitOffset(int, int) | 24 | unknown |
| `0027f5d8` | Resume_Get_WORK_MU_FontID() | 24 | unknown |
| `0027f5f0` | Resume_Get_WORK_MU_BWorkFontID() | 24 | unknown |
| `0027f608` | Resume_Get_WORK_MU_BWorkAnimationID() | 24 | unknown |
| `0027f8ec` | iOS_ResumeAfterAttackTeam() | 24 | unknown |
| `0027fc30` | cSaveFFT::cSaveFFT(char*) | 24 | unknown |
| `00280540` | iOS_fftSave() | 24 | unknown |
| `002806f0` | iOS_clearDebugPrimNum() | 24 | unknown |
| `00280740` | iOS_setClipoffNoFT4(int) | 24 | unknown |
| `00280758` | iOS_setClipoffNoFT3(int) | 24 | unknown |
| `002807c4` | iOS_getFt3Clipoff(int) | 24 | unknown |
| `002807dc` | iOS_get_testClip(int) | 24 | unknown |
| `00280858` | iOS_setTransFace(int, int) | 24 | unknown |
| `002808e0` | iOS_setTransFaceAT(int, int) | 24 | unknown |
| `00280920` | iOS_setTransFaceEVT(int, int) | 24 | unknown |
| `0028164c` | iOS_v2menuSetScreenSize(int, int) | 24 | unknown |
| `00283fb0` | mapclip_setpath(char*) | 24 | unknown |
| `002847c0` | new_ColorVectorDataBase(unsigned int) | 24 | unknown |
| `00284b9c` | pspBattleCheckFlg(unsigned int) | 24 | unknown |
| `00284c98` | pspBattleDataCharTexBufGet(int) | 24 | unknown |
| `00285b94` | pspItemIsMineruba | 24 | unknown |
| `00287588` | reset_g_NetIcon_DrawFlg() | 24 | unknown |
| `002885a0` | pspOpenCheckFlg(PSP_OPEN_FLG) | 24 | unknown |
| `00288f18` | pspgFreamBufCountCountReset() | 24 | unknown |
| `0028982c` | pspPrimReetWorkBuf_current() | 24 | unknown |
| `00289880` | pspClearSaveEnv() | 24 | unknown |
| `00289c04` | pspSaveDataCheckSystemFlg(FFTPSP_SYSTEM_FLG) | 24 | unknown |
| `0028a114` | FFT_GetCurrentSystemFile() | 24 | unknown |
| `0028b050` | pspWorldCheckFlg(PSP_WORLD_FLG) | 24 | unknown |
| `0028b068` | pspWorldCallBackSet(PSP_WORLD_CALLBACK_ID, void (*)()) | 24 | unknown |
| `0028b3c4` | pspWorldDataBackBufGet(int) | 24 | unknown |
| `0028c2c0` | CFFT_STATE::GetMenuBarVisible() | 24 | unknown |
| `0028c7c0` | CFFT_STATE::EVTCHRToFID(int) | 24 | unknown |
| `0028d688` | tlFreeAll() | 24 | unknown |
| `00291a6c` | SetSemiTrans | 24 | unknown |
| `00291a84` | SetShadeTex | 24 | unknown |
| `00291ef0` | xpLibgpuCheckFlg | 24 | unknown |
| `0029adb8` | xpLibgpuTPageGet | 24 | unknown |
| `0029add0` | xpLibgpuExVramSet | 24 | unknown |
| `0029ade8` | xpLibgpuTPageGet2() | 24 | unknown |
| `0029b6d0` | GsSetWorkBase | 24 | unknown |
| `0029cb88` | _gte_ldrgb(CVECTOR*) | 24 | unknown |
| `0029ce4c` | _gte_SetRGBcd(long*) | 24 | unknown |
| `0029ceec` | _gte_SetGeomOffset(long, long) | 24 | unknown |
| `0029d2f0` | _gte_stsxy(long*) | 24 | unknown |
| `0029d358` | _gte_stsxy2(long*) | 24 | unknown |
| `0029d370` | _gte_stsxy1(long*) | 24 | unknown |
| `0029d388` | _gte_stsxy0(long*) | 24 | unknown |
| `0029d520` | _gte_stdp(long*) | 24 | unknown |
| `0029d538` | _gte_stflg(long*) | 24 | unknown |
| `0029d56c` | _gte_stsz(long*) | 24 | unknown |
| `0029d664` | _gte_stotz(long*) | 24 | unknown |
| `0029d67c` | _gte_stopz(long*) | 24 | unknown |
| `0029d6e4` | _gte_stlvnl0(long*) | 24 | unknown |
| `0029d6fc` | _gte_stlvnl1(long*) | 24 | unknown |
| `0029d714` | _gte_stlvnl2(long*) | 24 | unknown |
| `0029d7c4` | _gte_strgb(CVECTOR*) | 24 | unknown |
| `0029d8c4` | _gte_ReadGeomScreen(long*) | 24 | unknown |
| `0029d9f4` | _gte_stlzc(long*) | 24 | unknown |
| `0029fd90` | GteGetDataReg(int) | 24 | unknown |
| `0029fdbc` | GteSetDataReg(long, long) | 24 | unknown |
| `0029fe70` | InitGeom | 24 | unknown |
| `0029fe88` | rsin | 24 | unknown |
| `0029febc` | PSX_csin | 24 | unknown |
| `002a0954` | MulRotMatrix | 24 | unknown |
| `002a1324` | SetGeomOffset | 24 | unknown |
| `002a13f0` | SetFogNearFar | 24 | unknown |
| `002a1884` | NormalColor | 24 | unknown |
| `002a18fc` | NormalColorDpq | 24 | unknown |
| `002a1990` | NormalColorCol | 24 | unknown |
| `002a1a4c` | read_szx(long*) | 24 | unknown |
| `002a1a64` | read_sz0(long*) | 24 | unknown |
| `002a1a7c` | read_sz1(long*) | 24 | unknown |
| `002a1a94` | read_sz2(long*) | 24 | unknown |
| `002a1ad4` | read_sxsy0(long*) | 24 | unknown |
| `002a1aec` | read_sxsy1(long*) | 24 | unknown |
| `002a1b04` | read_sxsy2(long*) | 24 | unknown |
| `002a1b44` | read_rgb0(long*) | 24 | unknown |
| `002a1b5c` | read_rgb1(long*) | 24 | unknown |
| `002a1b74` | read_rgb2(long*) | 24 | unknown |
| `002a1b8c` | read_flag(long*) | 24 | unknown |
| `002a1ba4` | read_p(long*) | 24 | unknown |
| `002a25c8` | read_otz(long*) | 24 | unknown |
| `002a25e0` | read_opz(long*) | 24 | unknown |
| `002a2728` | xpPadAnalogAssign | 24 | unknown |
| `002a2a34` | xpPadUpdateData | 24 | unknown |
| `002a2a68` | xpPadWorkBufGet | 24 | unknown |
| `002a2a80` | xpPadTriggerGet | 24 | unknown |
| `002a2a98` | xpPadGet | 24 | unknown |
| `002a2ab0` | xpPadAnalogXGet | 24 | unknown |
| `002a2ac8` | xpPadAnalogYGet | 24 | unknown |
| `002a2ae0` | xpPadPspPadDataGet | 24 | unknown |
| `002a2af8` | xpPadRepeatGet | 24 | unknown |
| `002a2b2c` | xpPadKeyTblSet | 24 | unknown |
| `002a2b44` | xpPadKeyTblGet | 24 | unknown |
| `002a2c90` | xpLibSN::PClseek(int, int, int) | 24 | unknown |
| `002a2cc8` | xpLibSN::PCwrite(int, char*, int) | 24 | unknown |
| `002a2fb8` | PCcreat | 24 | unknown |
| `002ab608` | GuEmu_SetLineInterval(int) | 24 | unknown |
| `002b36bc` | Error_Init() | 24 | unknown |
| `002b376c` | Error_SetError(int, char*) | 24 | unknown |
| `002b701c` | iOSHelpButtonCheck() | 24 | unknown |
| `002b7a5c` | SetDisableMapTouch() | 24 | unknown |
| `002b7a74` | ClearDisableMapTouch() | 24 | unknown |
| `002b7c6c` | iOS_getTutoBegin(int) | 24 | unknown |
| `002b7c84` | iOS_setTutoBegin(int, int) | 24 | unknown |
| `002b7c9c` | iOS_getTutoNow(int) | 24 | unknown |
| `002b7cb4` | iOS_setTutoNow(int, int) | 24 | unknown |
| `002b7ccc` | iOS_getV2Icon(V2ICON_DATA) | 24 | unknown |
| `002bef4c` | iOS_isExistResumeData() | 24 | unknown |
| `002befbc` | iOS_ClearMenuTouchKeyInput() | 24 | unknown |
| `002bf008` | chkSeDouble() | 24 | unknown |
| `002c53e8` | Movie_Init() | 24 | unknown |
| `000729b0` | Java_com_square_1enix_FFT_1Android_GL2JNILib_getCommand | 20 | unknown |
| `00073a04` | adler32_combine | 20 | unknown |
| `00073a18` | adler32_combine64 | 20 | unknown |
| `00073af0` | compressBound | 20 | unknown |
| `0008c238` | vorbis_info_blocksize | 20 | unknown |
| `000a1600` | _vorbis_window_get | 20 | unknown |
| `000a1774` | CG2D_COLOR::GetTone4To8() | 20 | unknown |
| `000a1788` | CG2D_COLOR::GetTone5To8() | 20 | unknown |
| `000a179c` | CG2D_COLOR::GetTone6To8() | 20 | unknown |
| `000a17b0` | CG2D_COLOR::GetTone64To255() | 20 | unknown |
| `000a17c4` | CG2D_COLOR::GetTone64To255Inv() | 20 | unknown |
| `000a17d8` | CG2D_COLOR::GetTone64To255_Sll24() | 20 | unknown |
| `000a27d0` | CG2D_LOADER::GetFormat() | 20 | unknown |
| `000a2bd4` | CG2D_LOADER_BMP::CG2D_LOADER_BMP(_G2D_FORMAT*, int) | 20 | unknown |
| `000a2c10` | CG2D_LOADER_BMP::GetSavePixelFormatInfo(_G2D_SAVE_INFO*) | 20 | unknown |
| `000a4afc` | CG2D_LOADER_TGA::CG2D_LOADER_TGA(_G2D_FORMAT*, int) | 20 | unknown |
| `000a4e84` | CG2D_LOADER_TGA::GetSavePixelFormatInfo(_G2D_SAVE_INFO*) | 20 | unknown |
| `000a5e5c` | CG2D_LOADER_TIM::CG2D_LOADER_TIM(_G2D_FORMAT*, int) | 20 | unknown |
| `000a7050` | CGX_SCREEN_CORRECT::GetAppScreenSize(float*, float*) | 20 | unknown |
| `000a7064` | CGX_SCREEN_CORRECT::GetAppScaledScreenSize(float*, float*) | 20 | unknown |
| `000a7e58` | CEGL2_IF::GetScreenSize(float*, float*) | 20 | unknown |
| `000a8174` | CEGL2_IF::GetScissor(_RECT_S32*) | 20 | unknown |
| `000a9034` | CEGL2_IF::CLUT_IsLoad(int) | 20 | unknown |
| `000a918c` | CEGL2_IF::ResetStatus() | 20 | unknown |
| `000aa96c` | CEGL2_FBO::~CEGL2_FBO() | 20 | unknown |
| `000acea0` | CEGL2_SPRITE::GetImageSize(int*, int*) | 20 | unknown |
| `000acec4` | CEGL2_SPRITE::GetTextureSize(float*, float*) | 20 | unknown |
| `000aced8` | CEGL2_SPRITE::GetTextureBuffer() | 20 | unknown |
| `000ad924` | CEGL2_SPRITE::SetAlpha(unsigned char) | 20 | unknown |
| `000af5c0` | CEGL2_TEX_HYBRID::GL_GetTextureHandle(int) | 20 | unknown |
| `000b1950` | CEGL_PACKET::Clear() | 20 | unknown |
| `000b1b8c` | CEGL_PACKET::GetExtraCurrent(int) | 20 | unknown |
| `000b1ba0` | CEGL_PACKET::SetExtraCurrent(int, int) | 20 | unknown |
| `000b1be8` | CEGL_PACKET::SetVBOInfo(int, int, int) | 20 | unknown |
| `000b3b74` | CINPUT_DATA::GetPressMask(int) | 20 | unknown |
| `000b3b88` | CINPUT_DATA::GetDownMask(int) | 20 | unknown |
| `000b3b9c` | CINPUT_DATA::GetUpMask(int) | 20 | unknown |
| `000b3bb0` | CINPUT_DATA::GetRepeatMask(int) | 20 | unknown |
| `000b3bc4` | CINPUT_DATA::GetDelayDownMask(int) | 20 | unknown |
| `000b5080` | CRECT::GetMouseCursorPos(int*, int*) | 20 | unknown |
| `000b50a0` | CRECT::GetScreenOffset(int*, int*) | 20 | unknown |
| `000b5458` | CRECT::GetEnable(int) | 20 | unknown |
| `000b546c` | CRECT::SetEnable(int, int) | 20 | unknown |
| `000b54ac` | CRECT::GetVisible(int) | 20 | unknown |
| `000b54c0` | CRECT::SetVisible(int, int) | 20 | unknown |
| `000b54d4` | CRECT::GetNoFocus(int) | 20 | unknown |
| `000b54e8` | CRECT::SetNoFocus(int, int) | 20 | unknown |
| `000b54fc` | CRECT::GetGroup(int) | 20 | unknown |
| `000b5510` | CRECT::SetGroup(int, int) | 20 | unknown |
| `000b5b1c` | CUI_SCROLLBAR::GetScrollOffset(int*, int*) | 20 | unknown |
| `000b5c20` | CUI_SCROLLBAR::SetCellPress(int, int) | 20 | unknown |
| `000b6f6c` | CFILE_TXT::~CFILE_TXT() | 20 | unknown |
| `000b707c` | CFILE_TXT::GetDataAsChar(int, int, unsigned int) | 20 | unknown |
| `000b7ed8` | CFILE_UTIL::FileEnum(char*, char*, CLIST*, CLIST*, unsigned int) | 20 | unknown |
| `000b8980` | CLIST::Init() | 20 | unknown |
| `000b8994` | CLIST::CLIST() | 20 | unknown |
| `000b8a04` | CLIST::~CLIST() | 20 | unknown |
| `000b9d48` | CWORK_MEM::CWORK_MEM() | 20 | unknown |
| `000b9ddc` | CWORK_MEM::GetTail(unsigned int) | 20 | unknown |
| `000bbb14` | CSOUND_IF_SL::GetBufferType(int) | 20 | unknown |
| `000bbc18` | CSOUND_IF_SL::GetSLFormat(int) | 20 | unknown |
| `000bcb8c` | CSOUND_IF_SL::~CSOUND_IF_SL() | 20 | unknown |
| `000bcc5c` | CSOUND_LOADER_PCM::GetFormat() const | 20 | unknown |
| `000bccd0` | CSOUND_LOADER_PCM::GetLoopOut() const | 20 | unknown |
| `000bd154` | CSOUND_LOADER_OGG::GetFormat() const | 20 | unknown |
| `000bd1c8` | CSOUND_LOADER_OGG::GetLoopOut() const | 20 | unknown |
| `000bd3a0` | COggMemMapFile::COggMemMapFile() | 20 | unknown |
| `000bd450` | COggMemMapFile::~COggMemMapFile() | 20 | unknown |
| `000bdd70` | CSTEP::IsFinish() | 20 | unknown |
| `000c81b0` | tool_setarrowmode(int) | 20 | unknown |
| `000cbb1c` | getYLine() | 20 | unknown |
| `000cbc28` | TrapWindow_Taskchk(int) | 20 | unknown |
| `000cc25c` | Cregist_zodiacot(unsigned int*) | 20 | unknown |
| `000d6d84` | iOS_GetFontBuffer() | 20 | unknown |
| `000d9608` | get_padframe() | 20 | unknown |
| `000d977c` | iOS_getStatusAllgrayf() | 20 | unknown |
| `000da820` | iOS_getLastEventNo() | 20 | unknown |
| `000e7474` | iOS_GetTutorialStartF() | 20 | unknown |
| `000e8080` | iOS_getPadTutorial() | 20 | unknown |
| `000fb4a8` | iOS_getLastBlkNo() | 20 | unknown |
| `00101420` | Wget_padframe() | 20 | unknown |
| `00101590` | WiOS_getStatusAllgrayf() | 20 | unknown |
| `00101fd0` | iOStorideflagGet() | 20 | unknown |
| `001021c8` | Wreturn_actionstructure() | 20 | unknown |
| `0010f110` | Wattackteam_call(unsigned long*, unsigned long) | 20 | unknown |
| `0012f1c4` | iOSdisp_personalWinPhase() | 20 | unknown |
| `0012f1d8` | iOSdisp_personalWinPhaseSet(int) | 20 | unknown |
| `0012f214` | iOSpersonalWinPosClear(int) | 20 | unknown |
| `0012f2dc` | iOSPersonalWinPosSet(int) | 20 | unknown |
| `0013c724` | iOS_getOptionAddOfsX() | 20 | unknown |
| `0013cfd0` | iOS_getOptionAddOfsMode() | 20 | unknown |
| `00142840` | WiOS_getOptionAddOfsX() | 20 | unknown |
| `00142f4c` | WiOS_getOptionAddOfsMode() | 20 | unknown |
| `0014bec8` | disp_requirement() | 20 | unknown |
| `001506a8` | getNetErrorCutFlg() | 20 | unknown |
| `001531e4` | GetgMission_Successflg() | 20 | unknown |
| `00153ca4` | iOS_set_globalgamestartflag(unsigned char) | 20 | unknown |
| `00155c78` | ret_adventurestatus() | 20 | unknown |
| `00156550` | send_worldkeymask(unsigned long) | 20 | unknown |
| `001579ac` | worldcursormove(int) | 20 | unknown |
| `001579c0` | regist_zodiacot(unsigned int*) | 20 | unknown |
| `0015a16c` | iOSTapTimeAreaGet() | 20 | unknown |
| `0015a314` | iOSsTchBtlFlagGet() | 20 | unknown |
| `0015a328` | iOSsTchBtlFlagSet(int) | 20 | unknown |
| `0015a484` | iOSUnitStatusLRGet() | 20 | unknown |
| `0015a8a0` | iOSScrollgStatusModeGet() | 20 | unknown |
| `0015b340` | iOSSlideIconGet() | 20 | unknown |
| `0015d294` | iOSRotAutoGet() | 20 | unknown |
| `0015d8c4` | iOSStatusLRPosiFlagGet() | 20 | unknown |
| `0015d8d8` | iOSStatusLRPosiFlagSet(int) | 20 | unknown |
| `0015d8ec` | iOSStatusDownGet() | 20 | unknown |
| `0015d99c` | iOSUnitTapSet(int) | 20 | unknown |
| `0015da20` | iOSGetTchCurLimit() | 20 | unknown |
| `0015eb44` | iOSBtlStsDYGet() | 20 | unknown |
| `0015ebac` | iOSStatusChangeSet(int) | 20 | unknown |
| `0015ee04` | iOSUnitListFlagGet() | 20 | unknown |
| `0015ee18` | iOSUnitListAddGet() | 20 | unknown |
| `0015ef3c` | iOSUnitListMoveFlagGet() | 20 | unknown |
| `0015feb0` | iOSJobChgRotChk() | 20 | unknown |
| `0015ff18` | iOSJobAngleSet(short) | 20 | unknown |
| `0015ff2c` | iOSJobAngleGet() | 20 | unknown |
| `0015fff4` | iOSGetTchRotDY() | 20 | unknown |
| `00160dc0` | iOSYajiEffectGetMultiRezCorrectEnable() | 20 | unknown |
| `00160dd4` | iOSYajiEffectSetMultiRezCorrectEnable(int) | 20 | unknown |
| `0016191c` | iOSWldHelpGet() | 20 | unknown |
| `00161930` | iOSWldHelpSet(int) | 20 | unknown |
| `00161944` | iOSHelpInputWaitGet() | 20 | unknown |
| `00161958` | iOSHelpInputWaitSet(int) | 20 | unknown |
| `00161cdc` | iOSWldUnitTypeGet() | 20 | unknown |
| `00161cf0` | iOSWldUnitTypeSet(int) | 20 | unknown |
| `00161e78` | iOS_getChkRotate() | 20 | unknown |
| `00161e8c` | iOS_getSlideCur() | 20 | unknown |
| `00161ea0` | iOS_setChkRotate(int) | 20 | unknown |
| `00161eb4` | iOS_getTchAreaX_Start() | 20 | unknown |
| `00161ec8` | iOS_getTchAreaY_Start() | 20 | unknown |
| `00161edc` | iOS_getsUnitSsUpDwn() | 20 | unknown |
| `0016f7f8` | cSelectCard(int) | 20 | unknown |
| `0016f80c` | cGetCardNo() | 20 | unknown |
| `00175620` | cWindowPrioritySet(int) | 20 | unknown |
| `001757bc` | cGetWindowColor() | 20 | unknown |
| `001834b4` | bWindowPrioritySet(int) | 20 | unknown |
| `0018367c` | bSetWindowCount(int) | 20 | unknown |
| `00183690` | bGetWindowCount() | 20 | unknown |
| `001836a4` | bGetWindowColor() | 20 | unknown |
| `001836b8` | iOS_setDispCursor_window(unsigned char) | 20 | unknown |
| `001836d0` | iOS_getScrollType_window() | 20 | unknown |
| `001836e4` | SelectCard(int) | 20 | unknown |
| `001836f8` | GetCardNo() | 20 | unknown |
| `0018f994` | eStopGetPad(int) | 20 | unknown |
| `00192cb4` | eWindowPrioritySet(int) | 20 | unknown |
| `00192e7c` | eSetWindowCount(int) | 20 | unknown |
| `00192e90` | eGetWindowCount() | 20 | unknown |
| `00192ea4` | eGetWindowColor() | 20 | unknown |
| `00192eb8` | iOS_getOtNum_equip() | 20 | unknown |
| `00192ecc` | iOS_setDispCursor_window_equip(unsigned char) | 20 | unknown |
| `00192ee0` | iOS_getMaxLineWindowEquip() | 20 | unknown |
| `00192ef4` | iOS_getScrollType_equip() | 20 | unknown |
| `00199630` | jSetWindowCount(int) | 20 | unknown |
| `00199644` | jGetWindowCount() | 20 | unknown |
| `00199658` | iOS_getOtNum() | 20 | unknown |
| `0019966c` | iOS_setCursorDisp(char) | 20 | unknown |
| `00199680` | iOS_getScrollType_jobstts() | 20 | unknown |
| `001a4858` | iOSLearnTypeSet(int) | 20 | unknown |
| `001a9240` | GetItemSellPrice(short) | 20 | unknown |
| `001ac8b4` | dispFT4num() | 20 | unknown |
| `001adc68` | FadeMask(int) | 20 | unknown |
| `001aec64` | iOSItemTypeSet(int) | 20 | unknown |
| `001aec78` | iOSItemTypeGet() | 20 | unknown |
| `001b4c20` | IsDark(int) | 20 | unknown |
| `001b8e50` | get_tutrial_pad() | 20 | unknown |
| `001b90dc` | iOSTutoBtlInputGet() | 20 | unknown |
| `001b90f0` | iOSTutoBtlInputSet(int) | 20 | unknown |
| `001b9354` | iOS_getTutorialbreak() | 20 | unknown |
| `001b9368` | iOS_setTutorialbreak(unsigned short) | 20 | unknown |
| `001ba9c8` | iOSUnitListTapCheck() | 20 | unknown |
| `001ba9dc` | iOSUnitListTapCheck(int) | 20 | unknown |
| `001ba9f0` | iOSUnitListCurChrGet() | 20 | unknown |
| `001baa04` | iOSUnitListCurChrSet(int) | 20 | unknown |
| `001bab64` | GetSttsAMovingTime() | 20 | unknown |
| `001c6f5c` | iOS_SetScrollNameFunc(unsigned char) | 20 | unknown |
| `001c6fa0` | WindowPrioritySet(int) | 20 | unknown |
| `001c71b4` | SetWindowCount(int) | 20 | unknown |
| `001c71c8` | GetWindowCount() | 20 | unknown |
| `001c71dc` | GetWindowColor() | 20 | unknown |
| `001c71f0` | iOS_getOtNum_unitlist() | 20 | unknown |
| `001c7204` | iOS_setDispCursor_window_unitlist(unsigned char) | 20 | unknown |
| `001c7234` | iOS_getScrollType_unitlist() | 20 | unknown |
| `001c7248` | iOS_getMaxLineWindowUnitlist() | 20 | unknown |
| `001d15b0` | get_originalability() | 20 | unknown |
| `001d15c4` | pspNetCheckAttackLoop() | 20 | unknown |
| `001d1f78` | charge_break(BWORK*) | 20 | unknown |
| `001d6480` | clear_actendflag(BWORK*) | 20 | unknown |
| `001eee34` | getEffSequenceAddress() | 20 | unknown |
| `001fcdf0` | iOSgetCursorVisible() | 20 | unknown |
| `002010b8` | iOSmapVectorScrollCheck() | 20 | unknown |
| `002041e8` | setStartBattleFlg(int) | 20 | unknown |
| `002041fc` | getStartBattleFlg() | 20 | unknown |
| `00204254` | setTurning(int) | 20 | unknown |
| `00207dfc` | iOS_setSelectWindowRecord(short) | 20 | unknown |
| `0020cbd4` | fileReadCheck() | 20 | unknown |
| `0020cc68` | fileOpenCD(unsigned long, unsigned long, void*) | 20 | unknown |
| `0020cc7c` | fileOpenCDOffset(unsigned long, unsigned long, unsigned long, void*) | 20 | unknown |
| `0020ea7c` | loadNewAnimation() | 20 | unknown |
| `0020f410` | eventEffectWait() | 20 | unknown |
| `0020f428` | eventEffectExecute() | 20 | unknown |
| `0020f6e0` | checkModelAnimation(int) | 20 | unknown |
| `0020f714` | checkVRAMAnimation(int) | 20 | unknown |
| `0020f8b8` | getFrameTicks() | 20 | unknown |
| `0020f95c` | iOS_SetFrameRate(int) | 20 | unknown |
| `00215bac` | stopMapPaletteAnimation() | 20 | unknown |
| `00215bc0` | restertMapPaletteAnimation() | 20 | unknown |
| `00216140` | iOS_getTexCacheLine() | 20 | unknown |
| `00216604` | checkActiveMusic() | 20 | unknown |
| `002168e8` | callEnvEffect(int) | 20 | unknown |
| `00217e00` | iOS_setInterventionEnable(int) | 20 | unknown |
| `0021b4e0` | GetPlugInFuncAdr(short) | 20 | unknown |
| `0021b890` | SetAirDensity(long) | 20 | unknown |
| `0021cf1c` | GetEffectStatus() | 20 | unknown |
| `0021ef24` | iOS_setSkipAddPrim(int) | 20 | unknown |
| `0021ef38` | iOS_getSkipAddPrim() | 20 | unknown |
| `00228dd0` | GetShapePrimPtNow() | 20 | unknown |
| `00241a4c` | iOS_SetMojiBlend(int) | 20 | unknown |
| `00245074` | iOS_setDispMenuTouch(char) | 20 | unknown |
| `00245088` | iOS_getDispMenuTouch() | 20 | unknown |
| `0024509c` | TEST_setClearOt(int) | 20 | unknown |
| `002450b0` | TEST_getClearOt() | 20 | unknown |
| `00245a60` | o_SelectCard(int) | 20 | unknown |
| `00245b20` | o_WaitCardEvent() | 20 | unknown |
| `00245bf0` | o_WaitCardEvent_X() | 20 | unknown |
| `00249c44` | numa_vOpn_CdRead(CDREC*, unsigned long, unsigned long, unsigned long, unsigned long*) | 20 | unknown |
| `002568f8` | iOS_getIwaPadMask() | 20 | unknown |
| `0025691c` | IOSsTownModeSet(int) | 20 | unknown |
| `0025f3d8` | iOS_wld_pad_trg(unsigned long) | 20 | unknown |
| `0025f3fc` | iOSSnapshotSet(int) | 20 | unknown |
| `0025f410` | iOSSDNovelHelpTrgSet(long) | 20 | unknown |
| `0025f424` | iOSSDNovelHelpTrgGet() | 20 | unknown |
| `0025f438` | iOSWldCntGet() | 20 | unknown |
| `0026b0e0` | iOS_getNblFuncName(int) | 20 | unknown |
| `0026d7a8` | iOSTutoFlagCheck(int) | 20 | unknown |
| `0026d7bc` | iOSTutoFlagSet(int, int) | 20 | unknown |
| `0027b480` | setDrawPrimNum(int) | 20 | unknown |
| `0027b514` | getCmdKindNum() | 20 | unknown |
| `0027b528` | getCmdKind(unsigned int) | 20 | unknown |
| `0027b648` | iOS_setHalftoneTap(int) | 20 | unknown |
| `0027b65c` | iOS_getHalftoneTap() | 20 | unknown |
| `0027c11c` | iOS_CMenuTouch::setDisableHeightAdjust(unsigned char, short) | 20 | unknown |
| `0027e6fc` | iOS_CMenuTouchSaveLoad::setDisableHeightAdjust(unsigned char, short) | 20 | unknown |
| `0027f504` | iOS_GetRectHitNoRelease() | 20 | unknown |
| `0027f518` | iOS_GetRectHitNoTouch() | 20 | unknown |
| `0027f52c` | iOS_GetRectHitNoSlide() | 20 | unknown |
| `0027f540` | iOS_GetRectHitNoTouchTrg() | 20 | unknown |
| `0027f554` | iOS_GetRectHitNoTouchOld() | 20 | unknown |
| `0027f5c4` | iOS_GetRectHitNoBegin() | 20 | unknown |
| `0027f640` | iOS_ResumeGetMode() | 20 | unknown |
| `0027fc14` | chk_ucResumeDataSetAddr(unsigned char*) | 20 | unknown |
| `002802f0` | executeSaveFFT() | 20 | unknown |
| `0028051c` | iOS_fftDelete() | 20 | unknown |
| `002805bc` | iOS_setDisableInterrupt(unsigned char) | 20 | unknown |
| `002805d0` | iOS_getDisableInterrupt() | 20 | unknown |
| `002805e8` | iOS_setUnitStatusCur(unsigned char) | 20 | unknown |
| `002805fc` | iOS_getUnitStatusCur() | 20 | unknown |
| `00280620` | iOS_setLockInput(unsigned char) | 20 | unknown |
| `00280634` | iOS_getLockInput() | 20 | unknown |
| `00280648` | iOS_setReset(int) | 20 | unknown |
| `0028065c` | iOS_getReset() | 20 | unknown |
| `00280688` | iOS_getEventbreak() | 20 | unknown |
| `0028069c` | iOS_setEventbreak(int) | 20 | unknown |
| `00280718` | iOS_getClipoffNoFT4() | 20 | unknown |
| `0028072c` | iOS_getClipoffNoFT3() | 20 | unknown |
| `002807b0` | iOS_getFt4Clipoff(int) | 20 | unknown |
| `00280980` | iOS_setTransFaceForChrRemove(int) | 20 | unknown |
| `00280994` | iOS_getTransFaceForChrRemove() | 20 | unknown |
| `00281664` | iOS_v2menuGetAddr() | 20 | unknown |
| `00281694` | iOS_v2menuSetDecide(int) | 20 | unknown |
| `002816a8` | iOS_v2menuGetDecide() | 20 | unknown |
| `002819b8` | iOS_v2menuGetType() | 20 | unknown |
| `00282274` | iOS_v2menuGetYline() | 20 | unknown |
| `002826b4` | iOS_PalleteHosei(unsigned char, int) | 20 | unknown |
| `002843a0` | new_VectorDataBase(unsigned int) | 20 | unknown |
| `00284bb4` | pspBattleGetFlg() | 20 | unknown |
| `002855b8` | pspItemIsEmpty | 20 | unknown |
| `002856d4` | pspItemGetWeaponVariationClut | 20 | unknown |
| `002856e8` | pspItemGetWeaponVariationBlock | 20 | unknown |
| `00285a98` | pspItemIsMagicalGun | 20 | unknown |
| `00285f38` | pspMsgLzwBaseGet(FFTPSP_MSG_LZW) | 20 | unknown |
| `0028612c` | ps_rand() | 20 | unknown |
| `002862e8` | IsMapTexAsideLoad(unsigned int) | 20 | unknown |
| `00286794` | setEventStatus(int) | 20 | unknown |
| `00286880` | getEventStatus() | 20 | unknown |
| `00286894` | get_gEventMovieNo() | 20 | unknown |
| `002868a8` | set_gEventMovieNo(int) | 20 | unknown |
| `002868bc` | pspNetGetTimeOutTimer() | 20 | unknown |
| `002868d0` | pspNetSetTimeOutTimer(int) | 20 | unknown |
| `002868ec` | pspNetGetGenearteAttackErrorFlag() | 20 | unknown |
| `00286900` | pspNetSetGenearteAttackErrorFlag(char) | 20 | unknown |
| `00286914` | pspNetSetControlChar(char) | 20 | unknown |
| `00286928` | pspNetGetControlChar() | 20 | unknown |
| `0028693c` | pspNetGetMoruboruFlag() | 20 | unknown |
| `00286950` | pspNetSetMoruboruFlag(char) | 20 | unknown |
| `00286994` | pspNetGetBattleModeFlag() | 20 | unknown |
| `002869a8` | pspNetSetBattleModeFlag(char) | 20 | unknown |
| `002869f4` | pspNetSetPad(int) | 20 | unknown |
| `00286a08` | pspNetGetPad() | 20 | unknown |
| `00286a1c` | pspNetGetPadPushTiming() | 20 | unknown |
| `00286a3c` | pspNetSetCharacterWaitFlag(char) | 20 | unknown |
| `00286a50` | pspNetGetCharacterWaitFlag() | 20 | unknown |
| `00286aa0` | get_netdatamode() | 20 | unknown |
| `00286ab4` | set_netdatamode(int) | 20 | unknown |
| `00286b0c` | set_limit_turn_flg(int) | 20 | unknown |
| `00286b20` | get_limit_turn_flg() | 20 | unknown |
| `00286dec` | GetNetmissionNo() | 20 | unknown |
| `00286e00` | pspNetEntranceDataMissionSceneNoGet(int) | 20 | unknown |
| `00286e24` | pspNetEntranceOptionArrayGet(NET_OPTION_TYPE) | 20 | unknown |
| `00286ec8` | pspNetSetAttackTimingFrame(int) | 20 | unknown |
| `00286edc` | pspNetGetTimingThroughFlag() | 20 | unknown |
| `00286ef0` | pspNetSetTimingThroughFlag(int) | 20 | unknown |
| `00286f04` | pspNetSetAttackTimingEffectFlag(int) | 20 | unknown |
| `0028701c` | pspNetGetAttackTimingEffectFlag() | 20 | unknown |
| `00287030` | get_timing_flag() | 20 | unknown |
| `00287070` | get_rival() | 20 | unknown |
| `00287094` | pspNetGetTrapFlag() | 20 | unknown |
| `002870dc` | pspNetSetTrapFlag(char) | 20 | unknown |
| `00287254` | AddrgTrapCommandTable_forDraw() | 20 | unknown |
| `00287a18` | set_g_Soldier_Draw_flg(int) | 20 | unknown |
| `00287a2c` | get_g_Soldier_Draw_flg() | 20 | unknown |
| `002884a0` | Set_NonDrawTaikiIconFlg(int) | 20 | unknown |
| `002884b4` | Get_NonDrawTaikiIconFlg() | 20 | unknown |
| `002884d4` | setBattlePoint(int) | 20 | unknown |
| `002884e8` | getBattlePoint() | 20 | unknown |
| `0028851c` | setMissionNo_CalcMissionPayPoint(int) | 20 | unknown |
| `00288530` | getMissionNo_CalcMissionPayPoint() | 20 | unknown |
| `00288544` | setTurnCount_CalcMissionPayPoint(int) | 20 | unknown |
| `00288558` | getTurnCount_CalcMissionPayPoint() | 20 | unknown |
| `00288578` | pspOpenDataBackBufGet(int) | 20 | unknown |
| `0028858c` | pspOpenDataIconBufGet() | 20 | unknown |
| `00289818` | pspPrimGetWorkBuf_current() | 20 | unknown |
| `00289b64` | pspSaveDataGetOne(int, FFT_SAVE_DATA*) | 20 | unknown |
| `00289b78` | pspSaveDataGet() | 20 | unknown |
| `0028a08c` | Savedata_GetAddr() | 20 | unknown |
| `0028a12c` | FFT_GetSavedata() | 20 | unknown |
| `0028b3dc` | pspWorldDataRectGet() | 20 | unknown |
| `0028ba2c` | getVSyncBlockCountTaskEmu() | 20 | unknown |
| `0028ba40` | TE_setTaskType(int) | 20 | unknown |
| `0028c204` | CFFT_STATE::GetRenderSize(int*, int*) | 20 | unknown |
| `0028c218` | CFFT_STATE::GetVertexScaling(float*, float*) | 20 | unknown |
| `0028c59c` | CFFT_STATE::AddParam(int, int) | 20 | unknown |
| `0028c5c0` | CFFT_STATE::SetStr(int, char*) | 20 | unknown |
| `0028d1b0` | tlGetHeap() | 20 | unknown |
| `0028dcf0` | StartRCnt | 20 | unknown |
| `0028dea8` | InitCARD | 20 | unknown |
| `0028df7c` | _card_info | 20 | unknown |
| `0028e0b4` | xpLibapiUserIdSet | 20 | unknown |
| `0028e1fc` | xpLibapiTitleIdSet | 20 | unknown |
| `0028e210` | xpLibapiDataVersionSet | 20 | unknown |
| `0028e5ac` | iOS_setPadState(unsigned long) | 20 | unknown |
| `00290b40` | SetDispMask | 20 | unknown |
| `00291edc` | xpLibgpuGetFlg | 20 | unknown |
| `00294e30` | xpLibgpuDispModeGet | 20 | unknown |
| `0029a918` | xpLibgpuActiveBufIdxGet | 20 | unknown |
| `0029b6e8` | GsGetWorkBase | 20 | unknown |
| `0029cce8` | _gte_lddp(long) | 20 | unknown |
| `0029ccfc` | _gte_ldsxy0(long) | 20 | unknown |
| `0029cd10` | _gte_ldsxy1(long) | 20 | unknown |
| `0029cd24` | _gte_ldsxy2(long) | 20 | unknown |
| `0029ce38` | _gte_ldlzc(long) | 20 | unknown |
| `0029cf04` | _gte_SetGeomScreen(long) | 20 | unknown |
| `0029fd7c` | GteGetCtrlReg(int) | 20 | unknown |
| `0029fda8` | GteSetCtrlReg(long, long) | 20 | unknown |
| `0029ff98` | SquareRoot0 | 20 | unknown |
| `002a0110` | RotMatrix_gte | 20 | unknown |
| `002a0624` | RotMatrixYXZ_gte | 20 | unknown |
| `002a07f4` | RotMatrixZYX_gte | 20 | unknown |
| `002a133c` | SetGeomScreen | 20 | unknown |
| `002a1370` | ReadGeomScreen | 20 | unknown |
| `002a13b4` | InitClip | 20 | unknown |
| `002a2b84` | xpLibSN::xpLibSN() | 20 | unknown |
| `002a2da4` | PCclose | 20 | unknown |
| `002a2fd0` | xpInitSPAD | 20 | unknown |
| `002a3120` | xpGetHeapSize | 20 | unknown |
| `002a3138` | xpSetResume | 20 | unknown |
| `002a3370` | pspSaveBase::SaveEnd() | 20 | unknown |
| `002a34a8` | pspSaveBase::setUserId() | 20 | unknown |
| `002a34d0` | pspSaveBase::GameDataSet(void*, unsigned int, unsigned int) | 20 | unknown |
| `002a376c` | pspSaveBase::errorMsgStrGet(pspSaveBase::PspSaveErrorMsgType) | 20 | unknown |
| `002ab6fc` | GPUCmd_GetGPUCmd_IP() | 20 | unknown |
| `002ab8ec` | sceGuColor | 20 | unknown |
| `002ab9cc` | sceGuFinishId | 20 | unknown |
| `002abd20` | sceGuClutMode | 20 | unknown |
| `002ac000` | sceGuTexMode | 20 | unknown |
| `002b1430` | SettingsBundle_Get() | 20 | unknown |
| `002b14d0` | Project_Archive_GetFile(int) | 20 | unknown |
| `002b6b24` | iOS_getv2menuSprIdTbl() | 20 | unknown |
| `002b7a8c` | iOS_getTouchTap() | 20 | unknown |
| `002b7aa0` | iOS_setTouchTap(int) | 20 | unknown |
| `002b7ab4` | iOS_getTouchFreeTap() | 20 | unknown |
| `002b7ac8` | iOS_getTouchRelease() | 20 | unknown |
| `002b7adc` | iOS_setTouchRelease(int) | 20 | unknown |
| `002b7af0` | iOS_getTouchPress() | 20 | unknown |
| `002b7b04` | iOS_setTouchPress(int) | 20 | unknown |
| `002b7b18` | iOS_getTouchBeginX() | 20 | unknown |
| `002b7b2c` | iOS_getTouchBeginY() | 20 | unknown |
| `002b7b40` | iOS_getTouchNowX() | 20 | unknown |
| `002b7b54` | iOS_getTouchNowY() | 20 | unknown |
| `002b7b68` | iOS_getDirectionTapDir() | 20 | unknown |
| `002b7b7c` | iOS_setDirectionTapDir(int) | 20 | unknown |
| `002b7b90` | iOS_getTouchSwype() | 20 | unknown |
| `002b7ba4` | iOS_getTouchSwypeUD() | 20 | unknown |
| `002b7bb8` | iOS_getTouchSlideflag() | 20 | unknown |
| `002b7bcc` | iOS_setEnterBattleFlag(int) | 20 | unknown |
| `002b7be0` | iOS_getEnterBattleFlag() | 20 | unknown |
| `002b7bf4` | iOS_getgDisableMapTouch() | 20 | unknown |
| `002b7c08` | iOS_getTutorialType() | 20 | unknown |
| `002b7c1c` | iOS_getTutorialPress() | 20 | unknown |
| `002b7c30` | iOS_setTutorialType(int) | 20 | unknown |
| `002b7c44` | iOS_getTutorialPad() | 20 | unknown |
| `002b7c58` | iOS_setTutorialPad(long) | 20 | unknown |
| `002b8708` | iOS_PressTime() | 20 | unknown |
| `002b873c` | iOS_getTouchCount() | 20 | unknown |
| `002b8798` | iOS_getTouchBeginXOrg() | 20 | unknown |
| `002b87ac` | iOS_getTouchBeginYOrg() | 20 | unknown |
| `002b87c0` | iOS_getTouchNowXOrg() | 20 | unknown |
| `002b87d4` | iOS_getTouchNowYOrg() | 20 | unknown |
| `002b87e8` | iOS_isInGameArea() | 20 | unknown |
| `002b87fc` | iOS_setInterFlag(int) | 20 | unknown |
| `002b8810` | iOS_getInterFlag() | 20 | unknown |
| `002b8824` | iOS_setStatusTimer(int) | 20 | unknown |
| `002b8838` | iOS_getStatusTimer() | 20 | unknown |
| `002b884c` | iOS_getCarrierType() | 20 | unknown |
| `002b8860` | iOS_getDoubleTap() | 20 | unknown |
| `002b8874` | iOS_getPressFirst() | 20 | unknown |
| `002bb664` | iOS_getTutoFreeTap() | 20 | unknown |
| `002befd4` | iOS_GetMenuTouchKeyInput() | 20 | unknown |
| `002beff4` | iOS_getGlobalCounter() | 20 | unknown |
| `002c53c0` | Main_GetPauseFlag() | 20 | unknown |
| `002c53d4` | Main_SetPauseFlag(int) | 20 | unknown |
| `002c9a25` | operator new[](unsigned int) | 20 | unknown |
| `002cb174` | __aeabi_cdcmpeq | 20 | unknown |
| `002cb188` | __aeabi_dcmpeq | 20 | unknown |
| `002cb19c` | __aeabi_dcmplt | 20 | unknown |
| `002cb1b0` | __aeabi_dcmple | 20 | unknown |
| `002cb1c4` | __aeabi_dcmpge | 20 | unknown |
| `002cb1d8` | __aeabi_dcmpgt | 20 | unknown |
| `002cb8b4` | __aeabi_cfcmpeq | 20 | unknown |
| `002cb8c8` | __aeabi_fcmpeq | 20 | unknown |
| `002cb8dc` | __aeabi_fcmplt | 20 | unknown |
| `002cb8f0` | __aeabi_fcmple | 20 | unknown |
| `002cb904` | __aeabi_fcmpge | 20 | unknown |
| `002cb918` | __aeabi_fcmpgt | 20 | unknown |
| `002cd8ec` | restore_core_regs | 20 | unknown |
| `00073c64` | get_crc_table | 16 | unknown |
| `0007b180` | inflateInit_ | 16 | unknown |
| `000823d4` | zlibVersion | 16 | unknown |
| `00082ff4` | oggpack_bits | 16 | unknown |
| `00083130` | ogg_page_continued | 16 | unknown |
| `00083140` | ogg_page_bos | 16 | unknown |
| `00083150` | ogg_page_eos | 16 | unknown |
| `0008d308` | vorbis_version_string | 16 | unknown |
| `000a1764` | CG2D_COLOR::GetTone2To8() | 16 | unknown |
| `000a573c` | CG2D_LOADER_TGA::GetImageFormatExt(int) | 16 | unknown |
| `000a6608` | CG2D_LOADER_TIM::GetImageFormatExt(int) | 16 | unknown |
| `000a6f28` | CGX_SCREEN_CORRECT::GetScale(float*) | 16 | unknown |
| `000ace90` | CEGL2_SPRITE::IsLoad() | 16 | unknown |
| `000aef7c` | CEGL2_TEX_HYBRID::UV_Get(int) | 16 | unknown |
| `000af634` | CEGL2_TEX_HYBRID::GL_SetUsed(int, int) | 16 | unknown |
| `000b1ae4` | CEGL_PACKET::GetIndices() | 16 | unknown |
| `000b1b0c` | CEGL_PACKET::SetTypeCurrent(unsigned char) | 16 | unknown |
| `000b1b34` | CEGL_PACKET::SetBlendModeCurrent(unsigned char) | 16 | unknown |
| `000b1b5c` | CEGL_PACKET::SetTextureCurrent(unsigned int) | 16 | unknown |
| `000b1b6c` | CEGL_PACKET::GetExtra(int, int) | 16 | unknown |
| `000b1b7c` | CEGL_PACKET::SetExtra(int, int, int) | 16 | unknown |
| `000b3528` | CINPUT_DATA::Init(_INPUT_DATA*) | 16 | unknown |
| `000b45c0` | CINPUT_IF_TOUCH::OnEventDispatched(int) | 16 | unknown |
| `000b4f78` | CRECT::Clear() | 16 | unknown |
| `000b5b3c` | CUI_SCROLLBAR::GetCellRect(int) | 16 | unknown |
| `000b5c10` | CUI_SCROLLBAR::GetCellPress(int) | 16 | unknown |
| `000b6c58` | CFILE_DAT::GetTable(int, int) | 16 | unknown |
| `000b6ef0` | CFILE_TXT::CFILE_TXT(char) | 16 | unknown |
| `000b8c08` | CSTR_UTIL::DBCSToWORD(char*) | 16 | unknown |
| `000bb114` | CSOUND_IF::GetPosition(int) | 16 | unknown |
| `000bb220` | CSOUND_IF::GetLength(int) | 16 | unknown |
| `000bb560` | CSOUND_IF::GetFormat(int) | 16 | unknown |
| `000bd464` | COggMemMapFile::IsOpen() const | 16 | unknown |
| `000bdb38` | CFRAMERATE::FrameStep(int) | 16 | unknown |
| `000bdb50` | CFRAMERATE::SetPause(int) | 16 | unknown |
| `000bdb70` | CSTEP::Register(_DATA_STEP*) | 16 | unknown |
| `000be2a4` | CSTEP_BATCH::GetEnable() | 16 | unknown |
| `000c441c` | Adisp_equipwindow() | 16 | unknown |
| `000c442c` | Adisp_abilitywindow() | 16 | unknown |
| `000d0dcc` | Ddisp_equipwindow() | 16 | unknown |
| `000d0ddc` | Ddisp_abilitywindow() | 16 | unknown |
| `000d6d98` | getStatusPad() | 16 | unknown |
| `00101fc0` | WgetStatusPad() | 16 | unknown |
| `0012b10c` | disp_equipwindow() | 16 | unknown |
| `0012b11c` | disp_abilitywindow() | 16 | unknown |
| `0014b9fc` | Cdisp_equipwindow() | 16 | unknown |
| `0014ba0c` | Cdisp_abilitywindow() | 16 | unknown |
| `0015c03c` | iOSRotSlidCls() | 16 | unknown |
| `0015ef0c` | iOSUnitListMoveFlagReset() | 16 | unknown |
| `00173a64` | cWindowDel(int) | 16 | unknown |
| `00177078` | bGetCommandNumber(int) | 16 | unknown |
| `0017a144` | bWindowDel(int) | 16 | unknown |
| `0018377c` | fileopen(unsigned char*, unsigned int) | 16 | unknown |
| `0018f0b8` | eWindowDel(int) | 16 | unknown |
| `001a6368` | iOSLearnTypeGet() | 16 | unknown |
| `001a84f8` | GetCommandNumber(int) | 16 | unknown |
| `001b6b00` | WindowDel(int) | 16 | unknown |
| `001d4f00` | set_throwitem(int, unsigned char, unsigned char*) | 16 | unknown |
| `001eec78` | changeAnimation(int, int, tag_animation*) | 16 | unknown |
| `001eee24` | getEffShapeAddress() | 16 | unknown |
| `0020d050` | getMapScrollXYZ() | 16 | unknown |
| `0020d2a8` | getMapScroll() | 16 | unknown |
| `0020d5c8` | getMapScale() | 16 | unknown |
| `0020d83c` | getMapAngle() | 16 | unknown |
| `0020dac8` | getBackColor() | 16 | unknown |
| `0021036c` | setShortVector(SVECTOR*, int, int, int) | 16 | unknown |
| `0022a470` | getVariationData(int, int, int) | 16 | unknown |
| `0022ad0c` | Add2ToShort(short*) | 16 | unknown |
| `0022ad1c` | Add4ToShort(short*) | 16 | unknown |
| `0022ad2c` | Add6ToShort(short*) | 16 | unknown |
| `0022ad3c` | Add8ToShort(short*) | 16 | unknown |
| `00243a6c` | Add(tagLIST_STAFFROLL*, tagSTAFFROLL*) | 16 | unknown |
| `00245b68` | o_CardInit() | 16 | unknown |
| `0025690c` | IOSsTownModeGet() | 16 | unknown |
| `0025f3ec` | iOSSnapshotGet() | 16 | unknown |
| `00263aac` | iOSNovelBrightStop() | 16 | unknown |
| `0026d798` | iOSTutoCheck() | 16 | unknown |
| `0027b494` | getDrawPrimNum() | 16 | unknown |
| `0027c26c` | iOS_CMenuTouch::drawDebug2() | 16 | unknown |
| `0027e794` | iOS_CMenuTouchSaveLoad::drawDebug2() | 16 | unknown |
| `0027f4f4` | iOS_GetRectHitNoTap() | 16 | unknown |
| `00284b8c` | pspBattleDataBackBufGet() | 16 | unknown |
| `00284d08` | pspBattleDataGet() | 16 | unknown |
| `002855d8` | pspItemIsRandom | 16 | unknown |
| `00285a88` | pspItemGetItemDataByAbility | 16 | unknown |
| `00285e40` | pspJobGetIndex2Job(int) | 16 | unknown |
| `00286a64` | pspNetCheckDuty() | 16 | unknown |
| `00286a7c` | pspNetCheckPlayerTeamCurrent() | 16 | unknown |
| `00286e14` | pspNetEntranceDataMissionBufferGet() | 16 | unknown |
| `00286e38` | pspNetEntranceOptionRecordGet() | 16 | unknown |
| `00286e48` | pspNetEntranceOptionScrRecordGet() | 16 | unknown |
| `0028bf3c` | TE_dummy() | 16 | unknown |
| `0028c5b0` | CFFT_STATE::GetStr(int) | 16 | unknown |
| `0028c7d8` | CAUTOSAVE::CAUTOSAVE() | 16 | unknown |
| `0028debc` | xpApiEnv::startCARD() | 16 | unknown |
| `0028decc` | StartCARD | 16 | unknown |
| `0028dedc` | xpApiEnv::stopCARD() | 16 | unknown |
| `0028deec` | StopCARD | 16 | unknown |
| `0028e0a4` | xpLibapiSaveEnd | 16 | unknown |
| `0028e224` | xpLibapiGetFreeSize | 16 | unknown |
| `0028e234` | xpLibapiGetMsSize | 16 | unknown |
| `0028e244` | xpLibapiGetUtilSize | 16 | unknown |
| `0028e2cc` | xpLibapiSaveUpdate | 16 | unknown |
| `0028e694` | xpSetVblankFunc(void (*)(int, void*), void*) | 16 | unknown |
| `002a1028` | CompMatrix | 16 | unknown |
| `002a1808` | RotTrans_nom | 16 | unknown |
| `002a1818` | RotTransPers_nom | 16 | unknown |
| `002a1828` | RotTransPers3_nom | 16 | unknown |
| `002a1874` | NormalColor_nom | 16 | unknown |
| `002a189c` | NormalColor3_nom | 16 | unknown |
| `002a26d4` | xpLibpad::AssignLR(int) | 16 | unknown |
| `002a2be8` | PCinit | 16 | unknown |
| `002a2c60` | xpLibSN::PCread(int, char*, int) | 16 | unknown |
| `002a2fe4` | xpGetSPADAddress | 16 | unknown |
| `002a3100` | xpMallocIO | 16 | unknown |
| `002a33d0` | pspSaveBase::SecureFileIdSet(unsigned char const*) | 16 | unknown |
| `002a34e4` | pspSaveBase::Icon0DataSet(void*, unsigned int, unsigned int) | 16 | unknown |
| `002a34f4` | pspSaveBase::PmfIcon1DataSet(void*, unsigned int, unsigned int) | 16 | unknown |
| `002a3504` | pspSaveBase::BackGoundPic1DataSet(void*, unsigned int, unsigned int) | 16 | unknown |
| `002a3514` | pspSaveBase::Snd0Set(void*, unsigned int, unsigned int) | 16 | unknown |
| `002a39a8` | pspSaveList::Update() | 16 | unknown |
| `002a39b8` | sceGeEdramGetAddr | 16 | unknown |
| `002b1444` | SettingsBundle_IsLeftHand() | 16 | unknown |
| `002b1fe8` | Offscreen_Get() | 16 | unknown |
| `002b375c` | Error_GetErrorCode() | 16 | unknown |
| `002bef64` | ResumeData_GetHeapOffset() | 16 | unknown |
| `002cb9dc` | __aeabi_idiv0 | 16 | unknown |
| `002cdedc` | _Unwind_GetRegionStart | 16 | unknown |
| `00077ab8` | gzopen | 12 | unknown |
| `00077ac4` | gzopen64 | 12 | unknown |
| `0008139c` | unzOpen | 12 | unknown |
| `000813a8` | unzOpen64 | 12 | unknown |
| `000823c8` | unzSetOffset | 12 | unknown |
| `00083124` | ogg_page_version | 12 | unknown |
| `00083ba0` | ogg_stream_flush | 12 | unknown |
| `00083bac` | ogg_stream_flush_fill | 12 | unknown |
| `00083d1c` | ogg_sync_check | 12 | unknown |
| `00084764` | vorbis_bitrate_clear | 12 | unknown |
| `0008be98` | vorbis_comment_init | 12 | unknown |
| `0009d084` | vorbis_synthesis_halfrate_p | 12 | unknown |
| `000a7e6c` | CEGL2_IF::SetScreenSize(float, float) | 12 | unknown |
| `000a8624` | CEGL2_IF::ClearPacket(int) | 12 | unknown |
| `000a8630` | CEGL2_IF::GetPacket(int) | 12 | unknown |
| `000a863c` | CEGL2_IF::GetCount(int) | 12 | unknown |
| `000acaa4` | CEGL2_SPRITE::SetVertexOffset(float, float) | 12 | unknown |
| `000ad8c4` | CEGL2_SPRITE::SetScale(float, float) | 12 | unknown |
| `000ae07c` | CEGL2_SPRITE::SetAlpha(int, unsigned char) | 12 | unknown |
| `000af104` | CEGL2_TEX_HYBRID::CLUTAddr_GetAddr(int) | 12 | unknown |
| `000b1af4` | CEGL_PACKET::GetType(int) | 12 | unknown |
| `000b1b00` | CEGL_PACKET::SetType(int, unsigned char) | 12 | unknown |
| `000b1b1c` | CEGL_PACKET::GetBlendMode(int) | 12 | unknown |
| `000b1b28` | CEGL_PACKET::SetBlendMode(int, unsigned char) | 12 | unknown |
| `000b1b44` | CEGL_PACKET::GetTexture(int) | 12 | unknown |
| `000b1b50` | CEGL_PACKET::SetTexture(int, unsigned int) | 12 | unknown |
| `000b1bbc` | CEGL_PACKET::GetVBOInfo(int) | 12 | unknown |
| `000b3518` | CINPUT_DATA::CINPUT_DATA() | 12 | unknown |
| `000b3d38` | CINPUT_IF_TOUCH::SetKeyNum(int, int) | 12 | unknown |
| `000b3d44` | CINPUT_IF_TOUCH::SetKeyWait(int, int, unsigned int, unsigned int) | 12 | unknown |
| `000b3d50` | CINPUT_IF_TOUCH::SetKeyWaitGroup(int, unsigned int, unsigned int) | 12 | unknown |
| `000b3d5c` | CINPUT_IF_TOUCH::SetKeyDelay(int, int, unsigned int) | 12 | unknown |
| `000b3d68` | CINPUT_IF_TOUCH::SetKeyGroup(int, int, int) | 12 | unknown |
| `000b3d74` | CINPUT_IF_TOUCH::SetRelaxUpMode(int) | 12 | unknown |
| `000b4044` | CINPUT_IF_TOUCH::GetPress(int, int) | 12 | unknown |
| `000b40b0` | CINPUT_IF_TOUCH::GetDown(int, int) | 12 | unknown |
| `000b40bc` | CINPUT_IF_TOUCH::SetDown(int, int, int) | 12 | unknown |
| `000b40c8` | CINPUT_IF_TOUCH::GetUp(int, int) | 12 | unknown |
| `000b40d4` | CINPUT_IF_TOUCH::GetUpDirect(int, int) | 12 | unknown |
| `000b40e0` | CINPUT_IF_TOUCH::GetRepeat(int, int) | 12 | unknown |
| `000b40ec` | CINPUT_IF_TOUCH::GetDelayDown(int, int) | 12 | unknown |
| `000b40f8` | CINPUT_IF_TOUCH::SetDelayDown(int, int, int) | 12 | unknown |
| `000b4104` | CINPUT_IF_TOUCH::GetPressGroup(int) | 12 | unknown |
| `000b4110` | CINPUT_IF_TOUCH::GetDownGroup(int) | 12 | unknown |
| `000b411c` | CINPUT_IF_TOUCH::GetUpGroup(int) | 12 | unknown |
| `000b4128` | CINPUT_IF_TOUCH::GetRepeatGroup(int) | 12 | unknown |
| `000b4134` | CINPUT_IF_TOUCH::GetDelayDownGroup(int) | 12 | unknown |
| `000b4140` | CINPUT_IF_TOUCH::GetPressMask(int) | 12 | unknown |
| `000b414c` | CINPUT_IF_TOUCH::GetDownMask(int) | 12 | unknown |
| `000b4158` | CINPUT_IF_TOUCH::GetUpMask(int) | 12 | unknown |
| `000b4164` | CINPUT_IF_TOUCH::GetRepeatMask(int) | 12 | unknown |
| `000b4170` | CINPUT_IF_TOUCH::GetDelayDownMask(int) | 12 | unknown |
| `000b42a4` | CINPUT_IF_TOUCH::GetEvent(int) | 12 | unknown |
| `000b4f88` | CRECT::Register(_RECT_UI*, int) | 12 | unknown |
| `000b5094` | CRECT::SetScreenOffset(int, int) | 12 | unknown |
| `000b50b4` | CRECT::SetScreenScale(float, float) | 12 | unknown |
| `000b5b30` | CUI_SCROLLBAR::IsEnableScrollUp() | 12 | unknown |
| `000b61d8` | CCOMP_Z_DEC::SetBlockSize(int, int) | 12 | unknown |
| `000b63a4` | CCOMP_Z_ENC::SetBlockSize(int, int) | 12 | unknown |
| `000b8bb0` | CLIST::Add(void*) | 12 | unknown |
| `000b9f7c` | CTHREAD::RequestExit() | 12 | unknown |
| `000b9fac` | CTHREAD::RequestSuspend() | 12 | unknown |
| `000b9fb8` | CTHREAD::RequestResume() | 12 | unknown |
| `000b9fd4` | TRACE_Empty(char const*, ...) | 12 | unknown |
| `000ba084` | Sleep(unsigned int) | 12 | unknown |
| `000bdb60` | CSTEP::CSTEP() | 12 | unknown |
| `000bdb80` | CSTEP::SetUnit(int) | 12 | unknown |
| `000be180` | CSTEP::GetProgress() | 12 | unknown |
| `000be1dc` | CSTEP_BATCH::Uninit() | 12 | unknown |
| `000d8734` | getanimpanel(int, SVECTOR*) | 12 | unknown |
| `00100408` | Wgetanimpanel(int, SVECTOR*) | 12 | unknown |
| `00161524` | iOSSdNovelLogIcon() | 12 | unknown |
| `00161530` | iOSSdNovelLogIconOn() | 12 | unknown |
| `0016153c` | iOSSdNovelLogIconOff() | 12 | unknown |
| `001d8d1c` | get_itemcommon(unsigned short) | 12 | unknown |
| `001dc760` | adjudt_equip_change_sp(BWORK*) | 12 | unknown |
| `001dc76c` | adjust_equip_change(BWORK*) | 12 | unknown |
| `001dc908` | set_startingstatus(BWORK*) | 12 | unknown |
| `001e692c` | setskilldata_to_ACT(ACT*) | 12 | unknown |
| `0020ebb8` | eventTerminateAnimation(int, int, short, short, short) | 12 | unknown |
| `00215c74` | changeGradation(int, int, short, short, short) | 12 | unknown |
| `00215c80` | changeAnbient(int, int, short, short, short) | 12 | unknown |
| `00215c8c` | changeFlatColor(int, int, short, short, short) | 12 | unknown |
| `0021680c` | callZingle(int) | 12 | unknown |
| `0021b50c` | loadData(char*, char**) | 12 | unknown |
| `00223f24` | GetBowFirstSpeed() | 12 | unknown |
| `00243a60` | CreateList(tagLIST_STAFFROLL*, tagSTAFFROLL*) | 12 | unknown |
| `0025d60c` | iOS_directedit_clear() | 12 | unknown |
| `00263f9c` | ctlnobel_deactive(CTLINFO*) | 12 | unknown |
| `0027c0dc` | iOS_CMenuTouch::setDispOffset(int, int) | 12 | unknown |
| `0027d7b4` | iOS_CMenuTouchNum::setDispOffset(int, int) | 12 | unknown |
| `0027e6d8` | iOS_CMenuTouchSaveLoad::setDispOffset(int, int) | 12 | unknown |
| `002821ec` | iOS_setMask(int) | 12 | unknown |
| `00282268` | iOS_clearOkNg() | 12 | unknown |
| `00284410` | Clear_VectorDataBaseObject(VECTOR_DATABASE*) | 12 | unknown |
| `002855cc` | pspItemIsBarehand | 12 | unknown |
| `0028a080` | pspGetFftPspSaveDataSize() | 12 | unknown |
| `0028aec4` | __bpGetFileNum | 12 | unknown |
| `0028afc4` | __bpGetBinarySize | 12 | unknown |
| `0028afd0` | __bpGetBinaryData | 12 | unknown |
| `0028c22c` | CFFT_STATE::SetVertexScaling(float, float) | 12 | unknown |
| `0028c2e8` | CFFT_STATE::SetMusicBuffer(int, int) | 12 | unknown |
| `0028c2f4` | CFFT_STATE::GetMusicBuffer(int) | 12 | unknown |
| `0028c320` | CFFT_STATE::GetParam(int) | 12 | unknown |
| `0028c590` | CFFT_STATE::SetParam(int, int) | 12 | unknown |
| `0028ce48` | asmClearBuffer(void*, unsigned int) | 12 | unknown |
| `0028de9c` | xpApiEnv::initCARD(long) | 12 | unknown |
| `002a142c` | SetFogNear | 12 | unknown |
| `002a26c8` | xpLibpad::RepParamSet(short, short) | 12 | unknown |
| `002a2714` | xpLibpad::PadTblSet(unsigned int*) | 12 | unknown |
| `002a3340` | pspSaveBase::FocusSet() | 12 | unknown |
| `002a34bc` | pspSaveBase::setExecType() | 12 | unknown |
| `002b0510` | CAPP_INFO::GetTempPath() | 12 | unknown |
| `002b2cf8` | SysSE_PlayDef(int) | 12 | unknown |
| `002b2d04` | SysSE_PlayUI(int) | 12 | unknown |
| `002befe8` | iOS_SetErrorCode(int) | 12 | unknown |
| `002c9115` | operator delete(void*) | 12 | unknown |
| `00072910` | Java_com_square_1enix_FFT_1Android_GL2JNILib_dialogOnClose | 8 | unknown |
| `000823e4` | zlibCompileFlags | 8 | unknown |
| `00082404` | zcalloc | 8 | unknown |
| `0008240c` | zcfree | 8 | unknown |
| `0008300c` | oggpack_get_buffer | 8 | unknown |
| `0009e97c` | ov_streams | 8 | unknown |
| `0009e984` | ov_seekable | 8 | unknown |
| `000a2820` | CG2D_LOADER::GetImageFormatCount() | 8 | unknown |
| `000a2a88` | CG2D_LOADER::GetImageExtCount() | 8 | unknown |
| `000a7e28` | CEGL2_IF::GetMaxTextureSize() | 8 | unknown |
| `000a8210` | CEGL2_IF::GetShader() | 8 | unknown |
| `000a91d4` | CEGL2_IF::GetWVP() const | 8 | unknown |
| `000a93fc` | CEGL2_IF::GetViewDir() const | 8 | unknown |
| `000a9404` | CEGL2_IF::EnableLighting(bool) | 8 | unknown |
| `000a940c` | CEGL2_IF::GetLight(int) | 8 | unknown |
| `000a94bc` | CEGL2_IF::LoadShader(int, char const*, char const*) | 8 | unknown |
| `000ab4a8` | CEGL2_FBO::GetTexture() | 8 | unknown |
| `000acab0` | CEGL2_SPRITE::SetVertexScale(float) | 8 | unknown |
| `000aceb4` | CEGL2_SPRITE::GetImageBPP() | 8 | unknown |
| `000acebc` | CEGL2_SPRITE::GetTextureHandle() | 8 | unknown |
| `000ad8d0` | CEGL2_SPRITE::GetScaleAlignCenter() | 8 | unknown |
| `000ad8d8` | CEGL2_SPRITE::SetScaleAlignCenter(int) | 8 | unknown |
| `000ae088` | CEGL2_SPRITE::GetMultiTextureHandle() | 8 | unknown |
| `000aec10` | CEGL2_SPRITE::SetMultiTextureHandle(unsigned int) | 8 | unknown |
| `000aee5c` | CEGL2_TEX_HYBRID::Register(int) | 8 | unknown |
| `000af110` | CEGL2_TEX_HYBRID::RAW_GetFID() | 8 | unknown |
| `000af118` | CEGL2_TEX_HYBRID::RAW_GetBuf() | 8 | unknown |
| `000af9e8` | CCAMERA::SetMode(CCAMERA::CAM_MODE) | 8 | unknown |
| `000af9f0` | CCAMERA::SetNearClip(float) | 8 | unknown |
| `000af9f8` | CCAMERA::SetFarClip(float) | 8 | unknown |
| `000afa00` | CCAMERA::SetFov(float) | 8 | unknown |
| `000afa08` | CCAMERA::GetView() const | 8 | unknown |
| `000afa10` | CCAMERA::GetProj() const | 8 | unknown |
| `000afa18` | CCAMERA::GetDir() const | 8 | unknown |
| `000b1acc` | CEGL_PACKET::GetDefaultBlendMode() | 8 | unknown |
| `000b1ad4` | CEGL_PACKET::SetDefaultBlendMode(unsigned char) | 8 | unknown |
| `000b1adc` | CEGL_PACKET::GetCount() | 8 | unknown |
| `000b1bb4` | CEGL_PACKET::GetVBOBuffer() | 8 | unknown |
| `000b3538` | CINPUT_DATA::SetRelaxUpMode(int) | 8 | unknown |
| `000b3540` | CINPUT_DATA::Begin(int) | 8 | unknown |
| `000b3d80` | CINPUT_IF_TOUCH::SetMultiTouchMax(int) | 8 | unknown |
| `000b4700` | CINPUT_IF_TOUCH::DeleteDeviceAll() | 8 | unknown |
| `000b5234` | CRECT::GetRectNum() | 8 | unknown |
| `000b523c` | CRECT::GetLastRID() | 8 | unknown |
| `000b5244` | CRECT::GetRID() | 8 | unknown |
| `000b524c` | CRECT::SetRID(int) | 8 | unknown |
| `000b5b14` | CUI_SCROLLBAR::GetScissor() | 8 | unknown |
| `000b67b0` | CFILE::GetLastError() | 8 | unknown |
| `000b682c` | CFILE::GetHandle() | 8 | unknown |
| `000b6ac4` | CFILE_DAT::GetFileNum() | 8 | unknown |
| `000b6acc` | CFILE_DAT::GetFileName() | 8 | unknown |
| `000b6c68` | CFILE_DAT::GetOffset(int) | 8 | unknown |
| `000b6cd0` | CFILE_DAT::GetSize(int) | 8 | unknown |
| `000b6ee0` | CFILE_DAT::GetCompress(int) | 8 | unknown |
| `000b6ee8` | CFILE_DAT::GetFormat(int) | 8 | unknown |
| `000b6f80` | CFILE_TXT::GetLineNum() | 8 | unknown |
| `000b78a4` | CFILE_UTIL::DrvGetDiscPath(char*, char*) | 8 | unknown |
| `000b78ac` | CFILE_UTIL::DrvGetFree(char*, unsigned int*, unsigned int*) | 8 | unknown |
| `000b7980` | CFILE_UTIL::DirDelete(char*, int) | 8 | unknown |
| `000b7990` | CFILE_UTIL::DirGetSpecial(unsigned int, int, char*) | 8 | unknown |
| `000b799c` | CFILE_UTIL::DirEnum(char*, CLIST*, unsigned int) | 8 | unknown |
| `000b79a4` | CFILE_UTIL::DirFind(char*) | 8 | unknown |
| `000b79ac` | CFILE_UTIL::FileCreate(char*) | 8 | unknown |
| `000b7b80` | CFILE_UTIL::FileMove(char*, char*) | 8 | unknown |
| `000b81a4` | CFILE_UTIL::FileSetReadOnly(char*, int) | 8 | unknown |
| `000b81ac` | CFILE_UTIL::FileSetExcludedFromBackup(char*, int) | 8 | unknown |
| `000b87f0` | CFILE_UTIL::FileOpenProp(char*) | 8 | unknown |
| `000b87f8` | CFILE_UTIL::FileCreateTemp(char*, char*) | 8 | unknown |
| `000b8970` | CFILE_UTIL::DlgGetPath(unsigned int, char*, char*, char*) | 8 | unknown |
| `000b8978` | CFILE_UTIL::DlgGetFile(unsigned int, unsigned int, char*, char*, char*, int, char*, char*) | 8 | unknown |
| `000b89a8` | CLIST::Insert(int, void*) | 8 | unknown |
| `000b8a18` | CLIST::GetCount() | 8 | unknown |
| `000b8e08` | CSTR_UTIL::IsRootPath(char*) | 8 | unknown |
| `000b9dd4` | CWORK_MEM::Get() | 8 | unknown |
| `000b9df0` | CWORK_MEM::GetAllocSize() | 8 | unknown |
| `000b9fc4` | CTHREAD::SetPriority(int) | 8 | unknown |
| `000b9fcc` | CTHREAD::Wait() | 8 | unknown |
| `000ba300` | CSOUND_IF::GetIF() | 8 | unknown |
| `000ba308` | CSOUND_IF::GetEnable() | 8 | unknown |
| `000ba39c` | CSOUND_IF::SetEnable(int) | 8 | unknown |
| `000bb9f8` | CSOUND_IF_SL::GetVolume(int) | 8 | unknown |
| `000bcbf4` | CSOUND_LOADER::GetSoundFormat() | 8 | unknown |
| `000bcbfc` | CSOUND_LOADER_PCM::IsOpen() const | 8 | unknown |
| `000bcc4c` | CSOUND_LOADER_PCM::GetSoundFormat() | 8 | unknown |
| `000bcc54` | CSOUND_LOADER_PCM::GetSoundEncode() const | 8 | unknown |
| `000bccc0` | CSOUND_LOADER_PCM::DecodeAll(unsigned char*) | 8 | unknown |
| `000bccc8` | CSOUND_LOADER_PCM::GetLoopIn() const | 8 | unknown |
| `000bd134` | COggMemMapFile::CallbackClose(void*) | 8 | unknown |
| `000bd13c` | COggMemMapFile::CallbackTell(void*) | 8 | unknown |
| `000bd144` | CSOUND_LOADER_OGG::IsTerminated() const | 8 | unknown |
| `000bd14c` | CSOUND_LOADER_OGG::GetSoundFormat() | 8 | unknown |
| `000bd168` | CSOUND_LOADER_OGG::GetSoundEncode() const | 8 | unknown |
| `000bd18c` | CSOUND_LOADER_OGG::GetTotal() const | 8 | unknown |
| `000bd1b8` | CSOUND_LOADER_OGG::DecodeAll(unsigned char*) | 8 | unknown |
| `000bd1c0` | CSOUND_LOADER_OGG::GetLoopIn() const | 8 | unknown |
| `000bd520` | CSOUND_LOADER_OGG::IsOpen() const | 8 | unknown |
| `000bd528` | COggMemMapFile::GetBuffer() | 8 | unknown |
| `000bd530` | COggMemMapFile::GetSize() | 8 | unknown |
| `000bd738` | CSOUND_LOADER_OGG::GetPlaySample() | 8 | unknown |
| `000bd95c` | CSOUND_LOADER_OGG::GetStreamBuffer() | 8 | unknown |
| `000bdad8` | CFRAMERATE::GetRootCnt() | 8 | unknown |
| `000bdb18` | CFRAMERATE::GetShowFPS() | 8 | unknown |
| `000bdb20` | CFRAMERATE::GetSpeed() | 8 | unknown |
| `000bdb28` | CFRAMERATE::SetSpeed(float) | 8 | unknown |
| `000bdb30` | CFRAMERATE::SetFixedMode(int) | 8 | unknown |
| `000bdb48` | CFRAMERATE::GetPause() | 8 | unknown |
| `000be39c` | CSTEP_BATCH::GetPrevStage() | 8 | unknown |
| `000be3a4` | CSTEP_BATCH::GetStage() | 8 | unknown |
| `000c8150` | return_jobdata() | 8 | unknown |
| `000cbd6c` | CheckTrapCancelCommandWindow() | 8 | unknown |
| `000d9f2c` | attackteam_prewait() | 8 | unknown |
| `000da834` | copymat(MATRIX*, MATRIX*) | 8 | unknown |
| `000e1110` | check_eventtoolmain(int, int) | 8 | unknown |
| `000e8094` | iOS_EventNumberGet() | 8 | unknown |
| `00101be8` | Wattackteam_prewait() | 8 | unknown |
| `001024fc` | Wcopymat(MATRIX*, MATRIX*) | 8 | unknown |
| `00102734` | MESSAGE_getMessageTaskKind() | 8 | unknown |
| `001027b4` | Whook_wipe() | 8 | unknown |
| `0010fb6c` | Wcheck_eventtoolmain(int, int) | 8 | unknown |
| `0015324c` | return_jobdatafromsmall() | 8 | unknown |
| `001599a0` | asmGetGP() | 8 | unknown |
| `00161f74` | wasmGetGP() | 8 | unknown |
| `0016f844` | cGetCardState() | 8 | unknown |
| `0016f84c` | cWait_GetCardState(int) | 8 | unknown |
| `0016f854` | cCardFileList(DIRENTRY*, int) | 8 | unknown |
| `0016f85c` | cCardFreeTotal(DIRENTRY*, int) | 8 | unknown |
| `0016f864` | cCardSetUp() | 8 | unknown |
| `0016f86c` | cCardFormat() | 8 | unknown |
| `0016f874` | cfileopen(unsigned char*, unsigned int) | 8 | unknown |
| `0016f87c` | cfileclose(unsigned int) | 8 | unknown |
| `0016f884` | cfilelseek(int, int, int) | 8 | unknown |
| `0016f88c` | cCardSave(unsigned char*, unsigned char*, unsigned long, int) | 8 | unknown |
| `0016f894` | cCardDelete(unsigned char*) | 8 | unknown |
| `0016f89c` | cCardLoad2(int, unsigned char*, unsigned long) | 8 | unknown |
| `0016f8a4` | cCardSave2(int, unsigned char*, unsigned long) | 8 | unknown |
| `00183754` | Wait_GetCardState(int) | 8 | unknown |
| `0018375c` | CardFileList(DIRENTRY*, int) | 8 | unknown |
| `00183764` | CardFreeTotal(DIRENTRY*, int) | 8 | unknown |
| `0018376c` | CardSetUp() | 8 | unknown |
| `00183774` | CardFormat() | 8 | unknown |
| `001837a8` | filelseek(int, int, int) | 8 | unknown |
| `001837b0` | CardSave(unsigned char*, unsigned char*, unsigned long, int) | 8 | unknown |
| `00183844` | CardLoad(unsigned char*, unsigned char*, unsigned long) | 8 | unknown |
| `0018384c` | CardLoad2(int, unsigned char*, unsigned long) | 8 | unknown |
| `00183854` | CardSave2(int, unsigned char*, unsigned long) | 8 | unknown |
| `001d3598` | set_playerwork(PENTRY*, unsigned char*) | 8 | unknown |
| `001d63fc` | after_equipchange(BWORK*) | 8 | unknown |
| `001e2b70` | check_coord(int, int, int) | 8 | unknown |
| `001eb8c8` | setPanelPriorityMove(SVECTOR*, SVECTOR*) | 8 | unknown |
| `001eb8d0` | setPanelPrioritySppMove(SVECTOR*, SVECTOR*) | 8 | unknown |
| `001eba84` | setPanelPriority(SVECTOR*, SVECTOR*) | 8 | unknown |
| `001ebfa4` | setPanelPrioritySpp(SVECTOR*, SVECTOR*) | 8 | unknown |
| `001fd588` | requestCristalEffect(tag_animation*) | 8 | unknown |
| `001fd590` | requestDeathEffect(tag_animation*) | 8 | unknown |
| `001fd598` | requestLevelupEffect(tag_animation*) | 8 | unknown |
| `001fd668` | requestPoisonEffect(tag_animation*) | 8 | unknown |
| `001fd670` | requestWaterinEffect(tag_animation*) | 8 | unknown |
| `001fd678` | requestLandingEffect(tag_animation*) | 8 | unknown |
| `001fd78c` | requestTelepoEffect(tag_animation*) | 8 | unknown |
| `00202fe8` | get_netTrapLocateModeFlg() | 8 | unknown |
| `0020594c` | iOS_IsBattleSpeedUp() | 8 | unknown |
| `0020dc5c` | checkAnimation(unsigned int) | 8 | unknown |
| `0020f94c` | iOS_GetFrameRate() | 8 | unknown |
| `0020f954` | iOS_GetFrameRateNative() | 8 | unknown |
| `0021037c` | setLongVector(VECTOR*, int, int, int) | 8 | unknown |
| `00215d60` | StopCallback | 8 | unknown |
| `00216274` | checkLoadMusic() | 8 | unknown |
| `0021bd18` | s4_killOwnTask(_EffectTCB*) | 8 | unknown |
| `0021ebb4` | p00_nullFunc() | 8 | unknown |
| `0021ec04` | p07_knockBackFunc() | 8 | unknown |
| `0021ec0c` | p10_jumpFunc() | 8 | unknown |
| `0021ec14` | p11_waterjumpFunc() | 8 | unknown |
| `0021ec1c` | p14_sweatFunc() | 8 | unknown |
| `0021ec24` | p16_reviveFunc() | 8 | unknown |
| `00225314` | iOS_GetPEffectCount() | 8 | unknown |
| `00228dc8` | GetShapePrimPtTopOld() | 8 | unknown |
| `00241930` | pluge000(short, int, int, int) | 8 | unknown |
| `002419c4` | fftCdReset() | 8 | unknown |
| `00241a44` | vOpn_arzmes_exit() | 8 | unknown |
| `00244410` | rolladr_calc(unsigned long, unsigned long) | 8 | unknown |
| `00245524` | movie_loop() | 8 | unknown |
| `00245814` | strNextVlc(DECENV*) | 8 | unknown |
| `00245a58` | getMoviePlayFlg__Fv() | 8 | unknown |
| `00245c04` | o_WaitCardInfo(int, int) | 8 | unknown |
| `0025d604` | iOS_directedit_chk() | 8 | unknown |
| `0026adb0` | snpl_je() | 8 | unknown |
| `0026adb8` | snpl_jne() | 8 | unknown |
| `0026ae1c` | snpl_jpageflg() | 8 | unknown |
| `0026ae24` | snpl_jnpageflg() | 8 | unknown |
| `0026ae7c` | snpl_jstatflg() | 8 | unknown |
| `0026ae84` | snpl_jnstatflg() | 8 | unknown |
| `0026aedc` | snpl_jlocalflg() | 8 | unknown |
| `0026aee4` | snpl_jnlocalflg() | 8 | unknown |
| `002712a8` | Ssd_AddWaveData(void*) | 8 | unknown |
| `002712b8` | Ssd_GetBankWaveSetPtr(short) | 8 | unknown |
| `002712d0` | Ssd_GetStereo() | 8 | unknown |
| `002712fc` | Ssd_AddMusic(void*) | 8 | unknown |
| `0027131c` | Ssd_PlayEffect(long) | 8 | unknown |
| `00271424` | Ssd_GetSeqPlayStatus(SsdSeqRec*) | 8 | unknown |
| `00279f84` | pspRoutineCheckArithmeticPermission() | 8 | unknown |
| `0027b390` | saveVram(char const*) | 8 | unknown |
| `0027b568` | getClutActiveMenuL() | 8 | unknown |
| `0027b570` | getClutActiveMenuR() | 8 | unknown |
| `0027b578` | getClutActiveMenuC() | 8 | unknown |
| `0027b580` | getClutActiveMenuName() | 8 | unknown |
| `0027b588` | getClutActiveMenuCursor() | 8 | unknown |
| `0027b590` | getClutActiveMenuCursorShadow() | 8 | unknown |
| `0027b598` | getClutMenuCursor() | 8 | unknown |
| `0027b5a0` | getClutBuyIcon() | 8 | unknown |
| `0027b5a8` | getClutPanelCursor() | 8 | unknown |
| `0027b5b0` | getClutScrollBar() | 8 | unknown |
| `0027b5b8` | getClutNamePopup() | 8 | unknown |
| `0027b5c0` | getClutNum() | 8 | unknown |
| `0027c0cc` | iOS_CMenuTouch::setMaxNumY(int) | 8 | unknown |
| `0027c0d4` | iOS_CMenuTouch::setDispNumY(int) | 8 | unknown |
| `0027c114` | iOS_CMenuTouch::setMaxnumX(int) | 8 | unknown |
| `0027c158` | iOS_CMenuTouch::setEnableUpDownRect(unsigned char) | 8 | unknown |
| `0027ce50` | iOS_CMenuTouch::setMode(IOS_MENU_TOUCH_MODE) | 8 | unknown |
| `0027d480` | iOS_CMenuTouchNum::setAddNum(int) | 8 | unknown |
| `0027e6c8` | iOS_CMenuTouchSaveLoad::setMaxNumY(int) | 8 | unknown |
| `0027e6d0` | iOS_CMenuTouchSaveLoad::setDispNumY(int) | 8 | unknown |
| `0027efe4` | iOS_CMenuTouchSaveLoad::setMode(IOS_MENU_TOUCH_SAVELOAD_MODE) | 8 | unknown |
| `00280530` | cSaveFFT::GetMode() | 8 | unknown |
| `00280538` | cSaveFFT::SetMode(SAVEFFT) | 8 | unknown |
| `0028084c` | iOS_hook_mesputmain() | 8 | unknown |
| `002808b0` | iOS_getTransFaceMax() | 8 | unknown |
| `00280918` | iOS_getTransFaceATMax() | 8 | unknown |
| `00280978` | iOS_getTransFaceEVTMax() | 8 | unknown |
| `002815dc` | test_test_addcolor() | 8 | unknown |
| `00284694` | SearchVector(VECTOR_DATABASE*, SVECTOR const*) | 8 | unknown |
| `00285f84` | pspFileManager::hockRead(void*, int) | 8 | unknown |
| `002868e4` | multwindow_keyright_checkexit() | 8 | unknown |
| `00286964` | pspNetWorkNoRand(BWORK*) | 8 | unknown |
| `0028696c` | pspNetKeepRand() | 8 | unknown |
| `00286a34` | pspNetJudgeBattlePoint() | 8 | unknown |
| `00286a74` | pspNetCheckPlayerTeam(tag_animation*) | 8 | unknown |
| `00286a8c` | pspNetGetLimitAction() | 8 | unknown |
| `00286ac8` | get_netmode() | 8 | unknown |
| `00286ad0` | get_netmodeadhoc() | 8 | unknown |
| `00286ad8` | get_parent_child() | 8 | unknown |
| `00286ae0` | get_main_player() | 8 | unknown |
| `00286aec` | pspNetGetErrorCode() | 8 | unknown |
| `00286af4` | pspNetDisconnectOrder() | 8 | unknown |
| `00286afc` | get_vsBattle_bule_trap() | 8 | unknown |
| `00286b04` | get_vsBattle_bule_arithmetic_select() | 8 | unknown |
| `00286b34` | net_send | 8 | unknown |
| `00286e80` | pspNetGetInterruptEndFlag() | 8 | unknown |
| `00287088` | pspNetGetStructTrapData(char) | 8 | unknown |
| `00287190` | pspNetCheckTrapAskEvent() | 8 | unknown |
| `0028724c` | pspNetTrapGetCommandNum() | 8 | unknown |
| `00287268` | GetgTrapCancelCount() | 8 | unknown |
| `00287270` | GetgTrapCancelResult() | 8 | unknown |
| `002884cc` | getNetBattleJudge() | 8 | unknown |
| `00288500` | getRewardLv() | 8 | unknown |
| `00288514` | getGetItemCount() | 8 | unknown |
| `00288570` | Get_AnimList(int) | 8 | unknown |
| `0028b418` | ScriptCut__Fiii(int, int, int) | 8 | unknown |
| `0028b420` | sceKernelGetGPI() | 8 | unknown |
| `0028b428` | sceIoDclose | 8 | unknown |
| `0028b430` | sceIoDread | 8 | unknown |
| `0028b438` | sceIoDopen | 8 | unknown |
| `0028b440` | sceDisplayGetVcount() | 8 | unknown |
| `0028b448` | sceDisplayGetAccumulatedHcount() | 8 | unknown |
| `0028b450` | sceDisplayWaitVblankStartCB() | 8 | unknown |
| `0028b458` | sceDisplaySetVblankCallback(int, void (*)(int, void*), void*) | 8 | unknown |
| `0028b470` | ResetCallback | 8 | unknown |
| `0028b478` | TestEvent(long) | 8 | unknown |
| `0028b480` | EncSPU | 8 | unknown |
| `0028b488` | EncSPU2 | 8 | unknown |
| `0028b4a4` | StFreeRing | 8 | unknown |
| `0028b4ac` | StGetNext | 8 | unknown |
| `0028b4b4` | StGetNextS | 8 | unknown |
| `0028b4bc` | StNextStatus | 8 | unknown |
| `0028b4d0` | StGetBackloc | 8 | unknown |
| `0028b4d8` | StSetChannel | 8 | unknown |
| `0028b4e4` | DecDCTvlc | 8 | unknown |
| `0028b4f0` | DecDCToutCallback | 8 | unknown |
| `0028b4f8` | get_SoundOnly_Flg__Fv() | 8 | unknown |
| `0028b500` | set_SoundOnly_Flg__Fi(int) | 8 | unknown |
| `0028b520` | getToolBgmFlg__Fv() | 8 | unknown |
| `0028b528` | getBgmData__FPUsPUs(unsigned short*, unsigned short*) | 8 | unknown |
| `0028b534` | getMovieSkipFlg__Fv() | 8 | unknown |
| `0028b544` | CdSearchFile | 8 | unknown |
| `0028b54c` | CdComstr | 8 | unknown |
| `0028b554` | CdIntstr | 8 | unknown |
| `0028b55c` | CdGetSector | 8 | unknown |
| `0028b564` | CdGetSector2 | 8 | unknown |
| `0028b56c` | CdDataSync | 8 | unknown |
| `0028b574` | CdGetToc | 8 | unknown |
| `0028b57c` | CdPlay | 8 | unknown |
| `0028b584` | CdMix | 8 | unknown |
| `0028b58c` | CdRead2 | 8 | unknown |
| `0028b594` | CdReadFile | 8 | unknown |
| `0028b59c` | CdReadSync | 8 | unknown |
| `0028b5a4` | CdReady | 8 | unknown |
| `0028b5ac` | CdSetDebug | 8 | unknown |
| `0028b5b4` | CdReadCallback | 8 | unknown |
| `0028b5bc` | CdReadyCallback | 8 | unknown |
| `0028b5c4` | CdSyncCallback | 8 | unknown |
| `0028b5cc` | CdReset | 8 | unknown |
| `0028b5d4` | CdStatus | 8 | unknown |
| `0028b5dc` | CdLastCom | 8 | unknown |
| `0028b5e4` | CdLastPos | 8 | unknown |
| `0028b5ec` | CdMode | 8 | unknown |
| `0028b5f4` | CdDiskReady | 8 | unknown |
| `0028b5fc` | CdGetDiskType | 8 | unknown |
| `0028b604` | CdReadExec | 8 | unknown |
| `0028b630` | exitXpHeap() | 8 | unknown |
| `0028b6f4` | _FFT_Main() | 8 | unknown |
| `0028c238` | CFFT_STATE::GetCaptureRequest() | 8 | unknown |
| `0028c240` | CFFT_STATE::SetCaptureRequest(int) | 8 | unknown |
| `0028c248` | CFFT_STATE::GetCaptureDraw() | 8 | unknown |
| `0028c250` | CFFT_STATE::SetCaptureDraw(int) | 8 | unknown |
| `0028c258` | CFFT_STATE::GetEncountRequest() | 8 | unknown |
| `0028c260` | CFFT_STATE::SetEncountRequest(int) | 8 | unknown |
| `0028c268` | CFFT_STATE::GetMode() | 8 | unknown |
| `0028c270` | CFFT_STATE::SetMode(int) | 8 | unknown |
| `0028c278` | CFFT_STATE::GetDebugMode() | 8 | unknown |
| `0028c280` | CFFT_STATE::SetDebugMode(int) | 8 | unknown |
| `0028c2d8` | CFFT_STATE::GetMoviePlaying() | 8 | unknown |
| `0028c2e0` | CFFT_STATE::SetMoviePlaying(int) | 8 | unknown |
| `0028c300` | CFFT_STATE::GetSettingsEnable() | 8 | unknown |
| `0028c308` | CFFT_STATE::SetSettingsEnable(int) | 8 | unknown |
| `0028c310` | CFFT_STATE::GetLinkEnable() | 8 | unknown |
| `0028c318` | CFFT_STATE::SetLinkEnable(int) | 8 | unknown |
| `0028ce40` | CAUTOSAVE::GetHeapOffset() | 8 | unknown |
| `0028ce78` | ReadTMD | 8 | unknown |
| `0028ce80` | CheckPrim | 8 | unknown |
| `0028ce88` | GetGraphDebug | 8 | unknown |
| `0028ce90` | GetTimSize | 8 | unknown |
| `0028ce98` | IsEndPrim | 8 | unknown |
| `0028cea0` | KanjiFntOpen | 8 | unknown |
| `0028ceac` | Krom2Tim | 8 | unknown |
| `0028ceb4` | MargePrim | 8 | unknown |
| `0028cebc` | OpenTMD | 8 | unknown |
| `0028cec4` | SetGraphDebug | 8 | unknown |
| `0028cecc` | KanjiFntFlush | 8 | unknown |
| `0028ced4` | NextPrim | 8 | unknown |
| `0028cf04` | BreakDraw | 8 | unknown |
| `0028cf10` | IsIdleGPU | 8 | unknown |
| `0028cf18` | GetODE | 8 | unknown |
| `0028cf20` | DrawOTag2 | 8 | unknown |
| `0028d434` | tlMalloc(unsigned int) | 8 | unknown |
| `0028de74` | _card_load | 8 | unknown |
| `0028de7c` | _card_read | 8 | unknown |
| `0028de84` | _card_status | 8 | unknown |
| `0028de8c` | firstfile(char const*, DIRENTRY*) | 8 | unknown |
| `0028de94` | nextfile(DIRENTRY*) | 8 | unknown |
| `0028e254` | xpLibapiIsMemoryStick | 8 | unknown |
| `0028e2dc` | CdInit | 8 | unknown |
| `0028e468` | CdControlF | 8 | unknown |
| `0028e4b8` | CdSync | 8 | unknown |
| `0028e568` | sceDisplayWaitVblankStartCB | 8 | unknown |
| `0028e594` | sceDisplayGetVcount | 8 | unknown |
| `0028e59c` | sceDisplayGetAccumulatedHcount | 8 | unknown |
| `0028e5a4` | sceDisplaySetVblankCallback | 8 | unknown |
| `00290e88` | FntOpen | 8 | unknown |
| `00290e94` | FntPrint | 8 | unknown |
| `00290e9c` | FntFlush | 8 | unknown |
| `00292670` | xpLibgpuDrawOffScreen | 8 | unknown |
| `0029ac18` | GetGraphType | 8 | unknown |
| `0029b6fc` | GsDrawOt | 8 | unknown |
| `002a0808` | MulMatrix | 8 | unknown |
| `002a0810` | MulMatrix2 | 8 | unknown |
| `002a26c0` | PadGetState | 8 | unknown |
| `002a26e4` | xpLibpad::TriggerGet() | 8 | unknown |
| `002a26ec` | xpLibpad::PadGet() const | 8 | unknown |
| `002a26f4` | xpLibpad::AnalogXGet() const | 8 | unknown |
| `002a26fc` | xpLibpad::AnalogYGet() const | 8 | unknown |
| `002a2704` | xpLibpad::PspPadDataGet() const | 8 | unknown |
| `002a270c` | xpLibpad::RepGet() const | 8 | unknown |
| `002a2720` | xpLibpad::PadTblGet() const | 8 | unknown |
| `002a3114` | xpMallocErrorFuncSet | 8 | unknown |
| `002a314c` | pspSaveBase::Exit() | 8 | unknown |
| `002a3384` | pspSaveBase::IsExec() | 8 | unknown |
| `002a33c8` | pspSaveBase::FileNameSet(char const*) | 8 | unknown |
| `002a3410` | pspSaveBase::AnimFrameSet(int) | 8 | unknown |
| `002a34c8` | pspSaveBase::ExecTypeSet(int) | 8 | unknown |
| `002a35bc` | pspSaveBase::ExecResultGet() | 8 | unknown |
| `002a35c4` | pspSaveBase::AbortedStatusGet() | 8 | unknown |
| `002a35cc` | pspSaveBase::ExecStateGet() | 8 | unknown |
| `002a35d4` | pspSaveBase::ErrorTypeGet() | 8 | unknown |
| `002a37a0` | pspSaveBase::IsMemoryStick() | 8 | unknown |
| `002a37a8` | pspSaveBase::DataVersionSet(SceUtilitySavedataVersion) | 8 | unknown |
| `002ab9e0` | sceGuSync | 8 | unknown |
| `002b0348` | TexHybrid_GetTextureMax(int) | 8 | unknown |
| `002b0424` | CAPP_INFO::GetDeviceType() | 8 | unknown |
| `002b042c` | CAPP_INFO::GetDeviceW() | 8 | unknown |
| `002b0434` | CAPP_INFO::GetDeviceH() | 8 | unknown |
| `002b043c` | CAPP_INFO::IsDeviceiPhoneRetina4inch() | 8 | unknown |
| `002b0444` | CAPP_INFO::GetDeviceScaleNative() | 8 | unknown |
| `002b044c` | CAPP_INFO::GetDeviceScale() | 8 | unknown |
| `002b0454` | CAPP_INFO::SetDeviceScale(float) | 8 | unknown |
| `002b048c` | CAPP_INFO::GetDeviceOrientation() | 8 | unknown |
| `002b0494` | CAPP_INFO::SetDeviceOrientation(int) | 8 | unknown |
| `002b049c` | CAPP_INFO::GetDeviceBatteryLevel() | 8 | unknown |
| `002b04a4` | CAPP_INFO::SetDeviceBatteryLevel(float) | 8 | unknown |
| `002b04ac` | CAPP_INFO::GetDiskSpaceTotal() | 8 | unknown |
| `002b04b4` | CAPP_INFO::GetDiskSpaceFree() | 8 | unknown |
| `002b04c0` | CAPP_INFO::CheckOSVersionRequirement(char*) | 8 | unknown |
| `002b04c8` | CAPP_INFO::GetLang() | 8 | unknown |
| `002b04d0` | CAPP_INFO::SetLang(int) | 8 | unknown |
| `002b04d8` | CAPP_INFO::IsEnableMultiTask() | 8 | unknown |
| `002b04e0` | CAPP_INFO::GetEnableiCloud() | 8 | unknown |
| `002b04e8` | CAPP_INFO::SetEnableiCloud(int) | 8 | unknown |
| `002b04f0` | CAPP_INFO::GetRootPath() | 8 | unknown |
| `002b04f8` | CAPP_INFO::GetDataPath() | 8 | unknown |
| `002b0500` | CAPP_INFO::GetDataPath_Native() | 8 | unknown |
| `002b0508` | CAPP_INFO::GetStoragePath() | 8 | unknown |
| `002b051c` | CAPP_INFO::GetActive() | 8 | unknown |
| `002b0524` | CAPP_INFO::SetActive(int) | 8 | unknown |
| `002b06a0` | CAPP_INFO::GetRenderScale() | 8 | unknown |
| `002b06a8` | CAPP_INFO::SetRenderScale(float) | 8 | unknown |
| `002b0710` | CDebugPrint::SetFontSize(float) | 8 | unknown |
| `002b0f68` | CDebugPrint::IsActive() | 8 | unknown |
| `002b3444` | iCloud_Send() | 8 | unknown |
| `002b344c` | iCloud_Receive() | 8 | unknown |
| `002b3454` | iCloud_GetSlotCount() | 8 | unknown |
| `002b36d4` | Error_FrameMove() | 8 | unknown |
| `002b7a2c` | GetPanelCursorMode() | 8 | unknown |
| `002c0ae0` | GX_GetScreenOffsetY() | 8 | unknown |
| `002c0b20` | GX_GetScreenOffsetY_1X() | 8 | unknown |
| `002c9121` | operator delete[](void*) | 8 | unknown |
| `002cce38` | _Unwind_GetCFA | 8 | unknown |
| `002cd57c` | __aeabi_unwind_cpp_pr0 | 8 | unknown |
| `002cd584` | __aeabi_unwind_cpp_pr1 | 8 | unknown |
| `002cd58c` | __aeabi_unwind_cpp_pr2 | 8 | unknown |
| `002cdf08` | _Unwind_GetDataRelBase | 8 | unknown |
| `002cdf10` | _Unwind_GetTextRelBase | 8 | unknown |
| `00072768` | Java_com_square_1enix_FFT_1Android_GL2JNILib_step | 4 | unknown |
| `0007401c` | crc32_combine | 4 | unknown |
| `00074020` | crc32_combine64 | 4 | unknown |
| `00077494` | gztell | 4 | unknown |
| `000774fc` | gzoffset | 4 | unknown |
| `00077dc8` | gzseek | 4 | unknown |
| `000785e4` | gzgetc_ | 4 | unknown |
| `0007f384` | _tr_flush_bits | 4 | unknown |
| `0008244c` | oggpackB_writeinit | 4 | unknown |
| `00082478` | oggpackB_writecheck | 4 | unknown |
| `00082548` | oggpackB_reset | 4 | unknown |
| `00082a14` | oggpackB_writeclear | 4 | unknown |
| `00082a44` | oggpackB_readinit | 4 | unknown |
| `00082ca8` | oggpackB_adv | 4 | unknown |
| `00082cdc` | oggpackB_adv1 | 4 | unknown |
| `00083004` | oggpackB_bytes | 4 | unknown |
| `00083008` | oggpackB_bits | 4 | unknown |
| `00083014` | oggpackB_get_buffer | 4 | unknown |
| `000af9bc` | CCAMERA::Uninit() | 4 | unknown |
| `000b3524` | CINPUT_DATA::~CINPUT_DATA() | 4 | unknown |
| `000b4f70` | CRECT::CRECT() | 4 | unknown |
| `000b4f74` | CRECT::~CRECT() | 4 | unknown |
| `000b5524` | CRECT::MoveCursor(int) | 4 | unknown |
| `000b5528` | CRECT::MoveCursorPos(int, int) | 4 | unknown |
| `000b5ac8` | CUI_SCROLLBAR::Delete() | 4 | unknown |
| `000b61d4` | CCOMP_Z_DEC::~CCOMP_Z_DEC() | 4 | unknown |
| `000b6200` | CCOMP_Z_DEC::Error(char const*) | 4 | unknown |
| `000b63a0` | CCOMP_Z_ENC::~CCOMP_Z_ENC() | 4 | unknown |
| `000b63cc` | CCOMP_Z_ENC::Error(char const*) | 4 | unknown |
| `000b6580` | CCRYPT::CCRYPT() | 4 | unknown |
| `000b6584` | CCRYPT::~CCRYPT() | 4 | unknown |
| `000b661c` | CCRYPT::Decrypt(unsigned char*, int, unsigned int) | 4 | unknown |
| `000b789c` | CFILE_UTIL::CFILE_UTIL() | 4 | unknown |
| `000b78a0` | CFILE_UTIL::~CFILE_UTIL() | 4 | unknown |
| `000b7988` | CFILE_UTIL::DirGetWindows(char*) | 4 | unknown |
| `000b798c` | CFILE_UTIL::DirGetSystem(char*) | 4 | unknown |
| `000b7998` | CFILE_UTIL::DirGetExecute(char*, char*) | 4 | unknown |
| `000b8a54` | CLIST::GetDataAsStr(int) | 4 | unknown |
| `000b8bdc` | CSTR_UTIL::CSTR_UTIL() | 4 | unknown |
| `000b8be0` | CSTR_UTIL::~CSTR_UTIL() | 4 | unknown |
| `000ba090` | SleepM(unsigned int) | 4 | unknown |
| `000bb058` | CSOUND_IF::ResetLoopPoint(int) | 4 | unknown |
| `000bb834` | CSOUND_IF_SL::FrameMove(int, float) | 4 | unknown |
| `000bbb10` | CSOUND_IF_SL::SetTrans(int, float, float, float) | 4 | unknown |
| `000bcbf0` | CSOUND_LOADER::FrameMove(int, float) | 4 | unknown |
| `000bd964` | CFRAMERATE::~CFRAMERATE() | 4 | unknown |
| `000bdb6c` | CSTEP::~CSTEP() | 4 | unknown |
| `000be41c` | CSTEP_BATCH::GetData() | 4 | unknown |
| `000be420` | CSTEP_BATCH::GetDataF() | 4 | unknown |
| `000be424` | CSTEP_BATCH::GetProgress() | 4 | unknown |
| `000be440` | CSTEP_BATCH::SetProgress(float) | 4 | unknown |
| `000c4418` | Adisp_floateventwindow() | 4 | unknown |
| `000c4494` | Aitemmenu_call(unsigned long*, unsigned long, int) | 4 | unknown |
| `000c4498` | attackdebugfunc() | 4 | unknown |
| `000cbd50` | SetTrapNameWindowParam(int, short, int) | 4 | unknown |
| `000cbd54` | TrapNameWindowManager() | 4 | unknown |
| `000cbd58` | CreateTrapNameWindowManagerTask() | 4 | unknown |
| `000cbd5c` | deleteEndModeWindow() | 4 | unknown |
| `000cbd60` | SetTrapNameWindowColor(int) | 4 | unknown |
| `000cbd64` | CreateTrapCancelCommandWindow() | 4 | unknown |
| `000cbd68` | DeleteTrapCancelCommandWindow() | 4 | unknown |
| `000cbd74` | CreateNetStayWindow() | 4 | unknown |
| `000d0dc8` | Ddisp_floateventwindow() | 4 | unknown |
| `000d1408` | Ditemmenu_call(unsigned long*, unsigned long, int) | 4 | unknown |
| `000d6f80` | iOS_chkallocatewindowinit() | 4 | unknown |
| `000d7384` | disposewindowbytask(int) | 4 | unknown |
| `000d8970` | dispemptywindow() | 4 | unknown |
| `000d8974` | send_statuschrno(int) | 4 | unknown |
| `000d8bfc` | initstatuscphase() | 4 | unknown |
| `000d9a08` | hook_disp_requirement() | 4 | unknown |
| `000d9a0c` | hook_trophics() | 4 | unknown |
| `000d9a10` | seekpcfile(char*, char*, int, int) | 4 | unknown |
| `000d9ac0` | loadonefile(char*, char*) | 4 | unknown |
| `000d9b0c` | request_tooltest() | 4 | unknown |
| `000da334` | request_effectmes(int, int, int, int) | 4 | unknown |
| `000da338` | request_warnmes(int, int, int, int) | 4 | unknown |
| `000e62c4` | DEBUGTRACE_hook_connect_camera() | 4 | unknown |
| `000e62c8` | DEBUG_CHK_ROLL(SCROLLRECORD*) | 4 | unknown |
| `000e7f0c` | dmp_tuto(unsigned char*, int) | 4 | unknown |
| `000feaa4` | WiOS_chkallocatewindowinit() | 4 | unknown |
| `00100640` | Wdispemptywindow() | 4 | unknown |
| `00100644` | Wsend_statuschrno(int) | 4 | unknown |
| `00100840` | Winitstatuscphase() | 4 | unknown |
| `00101908` | Whook_disp_requirement() | 4 | unknown |
| `0010190c` | Whook_trophics() | 4 | unknown |
| `00101910` | Wseekpcfile(char*, char*, int, int) | 4 | unknown |
| `001019bc` | Wloadonefile(char*, char*) | 4 | unknown |
| `001019c0` | LOAD_seekeventfile(int) | 4 | unknown |
| `00101a0c` | Wrequest_tooltest() | 4 | unknown |
| `00101f9c` | Wrequest_effectmes(int, int, int, int) | 4 | unknown |
| `00101fa0` | Wrequest_warnmes(int, int, int, int) | 4 | unknown |
| `00102128` | Wevent_init_light() | 4 | unknown |
| `00121718` | Edisp_floateventwindow() | 4 | unknown |
| `00123c40` | Eitemmenu_call(unsigned long*, unsigned long, int) | 4 | unknown |
| `0012b108` | disp_floateventwindow() | 4 | unknown |
| `00137b0c` | value_input() | 4 | unknown |
| `0014b9f8` | Cdisp_floateventwindow() | 4 | unknown |
| `0014bec4` | Citemmenu_call(unsigned long*, unsigned long, int) | 4 | unknown |
| `0014e0e4` | iOSSetjoinus() | 4 | unknown |
| `0014e0e8` | statushookfunc() | 4 | unknown |
| `0014e9a0` | sol_draw(int, int, int) | 4 | unknown |
| `00155708` | story_faceload() | 4 | unknown |
| `0015991c` | asmBoxCopy(char*, char*, COPYFIELD*, COPYFIELD*) | 4 | unknown |
| `00159920` | asmKanjiCopy(char*, char*, COPYFIELD*, int) | 4 | unknown |
| `00159a70` | asmMUL64(long, long, long) | 4 | unknown |
| `00159a74` | asmMUL3232(long, long, long, long) | 4 | unknown |
| `0015a480` | iOSSoundSESet(int) | 4 | unknown |
| `0015d174` | iOSstartTurn() | 4 | unknown |
| `0015d2a8` | iOSexecuteTurn() | 4 | unknown |
| `0015f044` | iOSUnitListLRCurSet(unsigned char*, unsigned short*, int, int, int, int) | 4 | unknown |
| `00161d98` | tDebugBreakCheck(int) | 4 | unknown |
| `00161d9c` | tDebugBreakTime(int) | 4 | unknown |
| `00161da0` | tDebugPointerErr() | 4 | unknown |
| `00161ef0` | wasmBoxCopy(char*, char*, COPYFIELD*, COPYFIELD*) | 4 | unknown |
| `00161ef4` | wasmKanjiCopy(char*, char*, COPYFIELD*, int) | 4 | unknown |
| `00162044` | wasmMUL64(long, long, long) | 4 | unknown |
| `00162048` | wasmMUL3232(long, long, long, long) | 4 | unknown |
| `0016f840` | cCardInit() | 4 | unknown |
| `001728dc` | cGetFrameRate() | 4 | unknown |
| `0017357c` | cWaitLoadImage(RECT16*, unsigned char*) | 4 | unknown |
| `00173580` | cWaitStoreImage(RECT16*, unsigned char*) | 4 | unknown |
| `00176690` | bGetFrameRate() | 4 | unknown |
| `00176b7c` | iOSBwork2ChrStts(BWORK*, CHR_STTS*, int) | 4 | unknown |
| `001836cc` | iOS_addPrim_window(tagPOLY_FT4*) | 4 | unknown |
| `0018372c` | CardInit() | 4 | unknown |
| `00188018` | eGetFrameRate() | 4 | unknown |
| `0019374c` | jGetFrameRate() | 4 | unknown |
| `0019e7b4` | shop_dummyfunc() | 4 | unknown |
| `001a6378` | iOS_resetCancelDisableAreaForStatusWindow() | 4 | unknown |
| `001a652c` | GetMessagePtr(int) | 4 | unknown |
| `001a6cc4` | GetFrameRate() | 4 | unknown |
| `001add64` | unit_dummyfunc() | 4 | unknown |
| `001b7ef0` | CallresetFFT() | 4 | unknown |
| `001d114c` | set_monomane_direction(BWORK*, unsigned char) | 4 | unknown |
| `001dca54` | callSW(int) | 4 | unknown |
| `001e7368` | pspNetTrapSpread(BWORK*, int) | 4 | unknown |
| `001f01a8` | resetActionAnimation(tag_animation*) | 4 | unknown |
| `00202f1c` | pspNetOutPutAnimationData() | 4 | unknown |
| `0020c258` | fftDrawSyncCallback() | 4 | unknown |
| `0020c25c` | fftCdReadyCallback() | 4 | unknown |
| `0020c260` | fftCdReadCallback() | 4 | unknown |
| `0020c5cc` | myPollhost() | 4 | unknown |
| `0020c5d0` | system_error(int, int) | 4 | unknown |
| `0020c5d4` | system_warning(int, int) | 4 | unknown |
| `0020ccb8` | fileReadCDOffset(unsigned long, unsigned long, unsigned long, void*) | 4 | unknown |
| `0020ce14` | fileAllocateCD(unsigned long, unsigned long) | 4 | unknown |
| `0020ce18` | fileDispose(char*) | 4 | unknown |
| `0020dba0` | requestStatusResult(unsigned int) | 4 | unknown |
| `0020f424` | eventEffectStart() | 4 | unknown |
| `0020f4f8` | getCharPrimList(short, Point*, unsigned long*) | 4 | unknown |
| `0020f904` | iOS_dispAnimetion() | 4 | unknown |
| `0020fb14` | initializeDebugFont() | 4 | unknown |
| `00215d20` | fadeGradation(int, CVECTOR*) | 4 | unknown |
| `00215d24` | fadeAnbient(int, CVECTOR*) | 4 | unknown |
| `00215d28` | fadeFlatColor(int, CVECTOR*) | 4 | unknown |
| `00215d5c` | PadStop | 4 | unknown |
| `00215db4` | resetFFT() | 4 | unknown |
| `0021610c` | iOS_rand() | 4 | unknown |
| `00216818` | stopZingle(int) | 4 | unknown |
| `0021681c` | controlZingle() | 4 | unknown |
| `002168e0` | callSystemSound(int) | 4 | unknown |
| `002168e4` | callSoundEffect(int) | 4 | unknown |
| `002168fc` | recallEnvEffect() | 4 | unknown |
| `002169cc` | pauseEnvEffect() | 4 | unknown |
| `0021ebb0` | error(char, long) | 4 | unknown |
| `00225310` | iOS_CheckPEffect(char const*, int) | 4 | unknown |
| `00225a60` | objectLG2(_EffectTCB*, _Object*) | 4 | unknown |
| `00225a64` | dmyFnc2(_EffectTCB*, _Object*) | 4 | unknown |
| `0022a614` | DumpMemory(int, void*) | 4 | unknown |
| `002419cc` | fftCdLoop(CDREC*) | 4 | unknown |
| `002419d0` | fftCdCancel(CDREC*) | 4 | unknown |
| `00248ccc` | ctlcard_init() | 4 | unknown |
| `002524cc` | ctlworkingst_deactive(CTLINFO*) | 4 | unknown |
| `00252b68` | ctlworkend_active(CTLINFO*) | 4 | unknown |
| `00252b6c` | ctlworkend_deactive(CTLINFO*) | 4 | unknown |
| `00258ac4` | evt_skip0() | 4 | unknown |
| `0025e67c` | get_unitwork_add_wld(int) | 4 | unknown |
| `0025ecd4` | wldscr_snapshot(int) | 4 | unknown |
| `0025f354` | wld_btlsect_seek() | 4 | unknown |
| `00267f38` | wldrute_init() | 4 | unknown |
| `0026b374` | sound_request(int) | 4 | unknown |
| `0026c058` | iOS_debugDispTownCircle(int, int) | 4 | unknown |
| `0026c278` | iOS_getMasaCdbOt_graphics_sdnovel(int) | 4 | unknown |
| `0026ff2c` | effectdmy() | 4 | unknown |
| `0027129c` | Ssd_Quit() | 4 | unknown |
| `002712a0` | Ssd_Enable() | 4 | unknown |
| `002712a4` | Ssd_Disable() | 4 | unknown |
| `002712b0` | Ssd_DisposeNormalWave() | 4 | unknown |
| `002712b4` | Ssd_DisposeWaveData(SsdWaveSetRec*) | 4 | unknown |
| `002712c0` | Ssd_AddEffectData(void*) | 4 | unknown |
| `002712c4` | Ssd_DisposeEffectData(void*) | 4 | unknown |
| `002712c8` | Ssd_AllStop() | 4 | unknown |
| `002712cc` | Ssd_SetStereo(int) | 4 | unknown |
| `002712d8` | Ssd_SetAttenuator(short) | 4 | unknown |
| `002712dc` | Ssd_SetReverbParam(long, short, long, long) | 4 | unknown |
| `002712e0` | Ssd_SetSpuVolume(short, short) | 4 | unknown |
| `002712e4` | Ssd_SetCDVolume(short, short) | 4 | unknown |
| `002712e8` | Ssd_SetCDMixingReverb(int, int) | 4 | unknown |
| `002712ec` | Ssd_CheckWideMode() | 4 | unknown |
| `002712f0` | Ssd_SetVolumeRec(short, SpuVolume*, char) | 4 | unknown |
| `002712f4` | Ssd_ErrorProc(int) | 4 | unknown |
| `002712f8` | Ssd_AddVagPackData(void*) | 4 | unknown |
| `00271304` | Ssd_DisposeMusic(SsdSeqRec*) | 4 | unknown |
| `00271308` | Ssd_LinkMusicData(SsdSeqRec*, void*) | 4 | unknown |
| `0027130c` | Ssd_StartMusic(SsdSeqRec*, short, short) | 4 | unknown |
| `00271310` | Ssd_StopMusic(SsdSeqRec*) | 4 | unknown |
| `00271314` | Ssd_PlaySysEffect(long) | 4 | unknown |
| `00271318` | Ssd_PlayEnvEffect(long) | 4 | unknown |
| `00271340` | Ssd_PlayEffects03(long, long, long, long) | 4 | unknown |
| `00271344` | Ssd_StopAllEffect() | 4 | unknown |
| `00271348` | Ssd_StopEffectSet(void*) | 4 | unknown |
| `00271410` | Ssd_InitEffectTrackRecWithStart(short, long, short, short) | 4 | unknown |
| `00271414` | Ssd_SetSeqMasterVolume(SsdSeqRec*, short, short) | 4 | unknown |
| `00271418` | Ssd_SetSeqMasterTempo(SsdSeqRec*, short, short) | 4 | unknown |
| `0027141c` | Ssd_SetSeqMasterPitch(SsdSeqRec*, short, short) | 4 | unknown |
| `00271420` | Ssd_SetSeqMasterPanpot(SsdSeqRec*, short, short) | 4 | unknown |
| `0027b398` | numa_fileAllocateCD(unsigned long, unsigned long) | 4 | unknown |
| `0027b39c` | numa_fileReadCD(unsigned long, unsigned long, void*) | 4 | unknown |
| `0027b3a0` | numa_fileReadRequest(unsigned int, unsigned int, char*) | 4 | unknown |
| `0027b510` | dispCmdKind() | 4 | unknown |
| `0027b5c8` | rprintfr(RECT16*, int, int, int) | 4 | unknown |
| `0027b670` | iOS_DEBUG_multiwindow_break_hook(unsigned long*) | 4 | unknown |
| `0027b674` | iOS_DEBUG_multiwindow_break_hook2(unsigned long*, int) | 4 | unknown |
| `0027b678` | iOS_DEBUG_multiwindow_keyright_hook() | 4 | unknown |
| `0027fc28` | chk_ucResumeData2(int) | 4 | unknown |
| `0027fc2c` | chk_ucResumeData(unsigned char*, int) | 4 | unknown |
| `0027fc78` | initSaveFFT(char*, char*, bool) | 4 | unknown |
| `0027fc7c` | cSaveFFT::~cSaveFFT() | 4 | unknown |
| `002805e4` | iOS_hookHelp(int*) | 4 | unknown |
| `00280610` | iOS_soundDirect(int) | 4 | unknown |
| `00280614` | iOS_hook_disp_option() | 4 | unknown |
| `00280618` | iOS_hook_disp_optionmain() | 4 | unknown |
| `0028061c` | iOS_hook_common(char const*, int) | 4 | unknown |
| `00280670` | hook_write_eventflag(int, int) | 4 | unknown |
| `00280674` | hook_calcformula(int, int) | 4 | unknown |
| `00280678` | hook_Debug(char const*) | 4 | unknown |
| `0028067c` | hook_Debug2(char const*) | 4 | unknown |
| `00280680` | hook_NextEventSet() | 4 | unknown |
| `00280684` | hook_musiclod() | 4 | unknown |
| `002806b0` | iOS_hook_worldhelpmenu() | 4 | unknown |
| `002806b4` | iOS_hook_gill() | 4 | unknown |
| `002806b8` | iOS_hook_movetopanel() | 4 | unknown |
| `002806bc` | hook_read_eventflag(int*) | 4 | unknown |
| `002806c0` | hook_allocate_texture() | 4 | unknown |
| `002806c4` | hook_opt() | 4 | unknown |
| `002806c8` | hook_chk_speedup(int) | 4 | unknown |
| `00280708` | hook_pad() | 4 | unknown |
| `0028070c` | hook_pad2() | 4 | unknown |
| `00280710` | hook_drive_connect_chrmove() | 4 | unknown |
| `00280714` | hook_drive_connect_chrmove2(int) | 4 | unknown |
| `002807f4` | hook_cliptest() | 4 | unknown |
| `002807f8` | chk_RefLine(int) | 4 | unknown |
| `002807fc` | hook_drive_chr(int) | 4 | unknown |
| `00280800` | hook_fix_bugno_931(int) | 4 | unknown |
| `00280804` | hook_win_tail() | 4 | unknown |
| `00280808` | hook_allSkipTest() | 4 | unknown |
| `00280854` | iOS_hook_line() | 4 | unknown |
| `002809c8` | iOS_hook_num() | 4 | unknown |
| `002815d8` | hook_num(int, int, int) | 4 | unknown |
| `002815e4` | chk_test_addcolor(unsigned int*) | 4 | unknown |
| `00281640` | hook_disp_plateorspell(int*) | 4 | unknown |
| `00281644` | hook_code_soundeffect(int) | 4 | unknown |
| `00281648` | hook_1284(char*, int) | 4 | unknown |
| `00286124` | SetSpadStack(unsigned long) | 4 | unknown |
| `00286128` | ResetSpadStack() | 4 | unknown |
| `00286744` | rsetmovie_title_flg__Fv() | 4 | unknown |
| `00286748` | setmovie_title_flg__Fv() | 4 | unknown |
| `002869f0` | _pspNetRand(char const*, int) | 4 | unknown |
| `00286a30` | pspNetSetPadPushTiming(unsigned long) | 4 | unknown |
| `00286a94` | timer_print_screen() | 4 | unknown |
| `00286a98` | val_letter(int, int, int) | 4 | unknown |
| `00286a9c` | set_nettimer_flag(int, int) | 4 | unknown |
| `00286ae8` | net_control_ex(void*, void*, int) | 4 | unknown |
| `00286e88` | pspNetAgreementInterruptInit() | 4 | unknown |
| `00286e8c` | pspNetCheckRivalAction() | 4 | unknown |
| `00286e90` | rivalCameraWorkProcs() | 4 | unknown |
| `00286ec4` | check_rival_value(int) | 4 | unknown |
| `00287084` | pspNetCheckTrapOnlyStatus(int) | 4 | unknown |
| `00287090` | pspNetTrapDeliveryInit(char) | 4 | unknown |
| `00287584` | load_iconpackdata() | 4 | unknown |
| `002875a0` | draw_maru(unsigned long*) | 4 | unknown |
| `002875a4` | draw_batu(unsigned long*) | 4 | unknown |
| `00287a14` | Red_Blue_Draw(int) | 4 | unknown |
| `00288498` | Draw_TuusinIcon(int, int, unsigned long*) | 4 | unknown |
| `0028849c` | Draw_Trap_CancelCommandList(int*, int, int, unsigned long*) | 4 | unknown |
| `002884c8` | NetBattleJudge() | 4 | unknown |
| `002884fc` | setRewardLv(int) | 4 | unknown |
| `00288508` | CalcRewardLv() | 4 | unknown |
| `0028850c` | CalcMissionPayPoint(int) | 4 | unknown |
| `00288510` | Final_CalcMissionPayPoint() | 4 | unknown |
| `0028856c` | init_AnimList() | 4 | unknown |
| `00289968` | pspSaveUpdate() | 4 | unknown |
| `0028996c` | pspSaveExit() | 4 | unknown |
| `0028b460` | SpuInit | 4 | unknown |
| `0028b464` | SpuInitHot | 4 | unknown |
| `0028b468` | SpuQuit | 4 | unknown |
| `0028b46c` | SetMem | 4 | unknown |
| `0028b490` | StSetRing | 4 | unknown |
| `0028b494` | StClearRing | 4 | unknown |
| `0028b498` | StUnSetRing | 4 | unknown |
| `0028b49c` | StSetStream | 4 | unknown |
| `0028b4a0` | StSetEmulate | 4 | unknown |
| `0028b4c4` | StRingStatus | 4 | unknown |
| `0028b4c8` | StSetMask | 4 | unknown |
| `0028b4cc` | StCdInterrupt | 4 | unknown |
| `0028b4e0` | DecDCTReset | 4 | unknown |
| `0028b4ec` | DecDCTout | 4 | unknown |
| `0028b508` | pspMovieEnd__Fv() | 4 | unknown |
| `0028b50c` | pspMovieInit__FiPCciiii(int, char*, int, int, int, int) | 4 | unknown |
| `0028b510` | pspMoviePlay__Fv() | 4 | unknown |
| `0028b514` | pspMovieStart__Fv() | 4 | unknown |
| `0028b518` | setMoviePlayFlg__Fi(int) | 4 | unknown |
| `0028b51c` | setMovieSkipFlg__Fi(int) | 4 | unknown |
| `0028b530` | setToolBgmFlg__Fi(int) | 4 | unknown |
| `0028b53c` | setBgmData__Fii(int, int) | 4 | unknown |
| `0028b540` | CdFlush | 4 | unknown |
| `0028b60c` | CdReadBreak | 4 | unknown |
| `0028c200` | CFFT_STATE::~CFFT_STATE() | 4 | unknown |
| `0028c7e8` | CAUTOSAVE::~CAUTOSAVE() | 4 | unknown |
| `0028ce54` | asmmemcpy(void*, void const*, unsigned int) | 4 | unknown |
| `0028cea8` | KanjiFntClose | 4 | unknown |
| `0028cedc` | CatPrim | 4 | unknown |
| `0028cee0` | DrawOTagIO | 4 | unknown |
| `0028cee4` | DrawOTagEnv | 4 | unknown |
| `0028cee8` | DumpClut | 4 | unknown |
| `0028ceec` | DumpDispEnv | 4 | unknown |
| `0028cef0` | DumpDrawEnv | 4 | unknown |
| `0028cef4` | DumpOTag | 4 | unknown |
| `0028cef8` | DumpTPage | 4 | unknown |
| `0028cefc` | SetDumpFnt | 4 | unknown |
| `0028cf00` | TermPrim | 4 | unknown |
| `0028cf0c` | ContinueDraw | 4 | unknown |
| `0028cf28` | GetDrawMode | 4 | unknown |
| `0028cf2c` | GetTexWindow | 4 | unknown |
| `0028cf30` | GetDrawArea | 4 | unknown |
| `0028cf34` | GetDrawOffset | 4 | unknown |
| `0028cf38` | GetDrawEnv2 | 4 | unknown |
| `0028de70` | _bu_init | 4 | unknown |
| `0028e464` | CdControlB | 4 | unknown |
| `0028e5c0` | VSync | 4 | unknown |
| `00290e90` | FntLoad | 4 | unknown |
| `0029266c` | xpLibgpuDrawUserOffScreen | 4 | unknown |
| `00292708` | xpLibgpuDrawCallBackSet | 4 | unknown |
| `00294ed4` | xpLibgpuVramAddrGet | 4 | unknown |
| `0029551c` | xpLibgpuBuffersSet | 4 | unknown |
| `00295568` | xpLibgpuMoveImage | 4 | unknown |
| `0029b3e8` | iOS_chkclutaddr() | 4 | unknown |
| `0029b3ec` | GsInit3D | 4 | unknown |
| `0029b428` | GsGetActiveBuff | 4 | unknown |
| `0029da84` | _gte_nop() | 4 | unknown |
| `0029dd14` | _gte_rt_b() | 4 | unknown |
| `0029dedc` | _gte_rtps_b() | 4 | unknown |
| `0029df20` | _gte_rtpt_b() | 4 | unknown |
| `0029dff0` | _gte_rtv0_b() | 4 | unknown |
| `0029e0c0` | _gte_rtv1_b() | 4 | unknown |
| `0029e190` | _gte_rtv2_b() | 4 | unknown |
| `0029e23c` | _gte_rtir_b() | 4 | unknown |
| `0029e240` | _gte_rtir_sf0() | 4 | unknown |
| `0029e244` | _gte_rtir_sf0_b() | 4 | unknown |
| `0029e314` | _gte_rtv0tr_b() | 4 | unknown |
| `0029e3e4` | _gte_rtv1tr_b() | 4 | unknown |
| `0029e4b4` | _gte_rtv2tr_b() | 4 | unknown |
| `0029e584` | _gte_rtirtr_b() | 4 | unknown |
| `0029e660` | _gte_rtv0bk_b() | 4 | unknown |
| `0029e73c` | _gte_rtv1bk_b() | 4 | unknown |
| `0029e818` | _gte_rtv2bk_b() | 4 | unknown |
| `0029e8f4` | _gte_rtirbk_b() | 4 | unknown |
| `0029e9c4` | _gte_llv0_b() | 4 | unknown |
| `0029ea10` | _gte_ll_b() | 4 | unknown |
| `0029eae0` | _gte_llv1_b() | 4 | unknown |
| `0029ebb0` | _gte_llv2_b() | 4 | unknown |
| `0029ec80` | _gte_llir_b() | 4 | unknown |
| `0029eccc` | _gte_llv0tr_b() | 4 | unknown |
| `0029ed18` | _gte_llv1tr_b() | 4 | unknown |
| `0029ed64` | _gte_llv2tr_b() | 4 | unknown |
| `0029edb0` | _gte_llirtr_b() | 4 | unknown |
| `0029edfc` | _gte_llv0bk_b() | 4 | unknown |
| `0029ee48` | _gte_llv1bk_b() | 4 | unknown |
| `0029ee94` | _gte_llv2bk_b() | 4 | unknown |
| `0029eee0` | _gte_llirbk_b() | 4 | unknown |
| `0029efb0` | _gte_lcv0_b() | 4 | unknown |
| `0029f080` | _gte_lcv1_b() | 4 | unknown |
| `0029f150` | _gte_lcv2_b() | 4 | unknown |
| `0029f220` | _gte_lcir_b() | 4 | unknown |
| `0029f26c` | _gte_lcv0tr_b() | 4 | unknown |
| `0029f2b8` | _gte_lcv1tr_b() | 4 | unknown |
| `0029f304` | _gte_lcv2tr_b() | 4 | unknown |
| `0029f350` | _gte_lcirtr_b() | 4 | unknown |
| `0029f39c` | _gte_lcv0bk_b() | 4 | unknown |
| `0029f3e8` | _gte_lc_b() | 4 | unknown |
| `0029f434` | _gte_lcv1bk_b() | 4 | unknown |
| `0029f480` | _gte_lcv2bk_b() | 4 | unknown |
| `0029f4cc` | _gte_lcirbk_b() | 4 | unknown |
| `0029f558` | _gte_dpcs_b() | 4 | unknown |
| `0029f5b0` | _gte_dpcl_b() | 4 | unknown |
| `0029f5ec` | _gte_dpct_b() | 4 | unknown |
| `0029f678` | _gte_intpl_b() | 4 | unknown |
| `0029f6f0` | _gte_sqr12_b() | 4 | unknown |
| `0029f72c` | _gte_sqr0_b() | 4 | unknown |
| `0029f914` | _gte_ncs_b() | 4 | unknown |
| `0029f958` | _gte_nct_b() | 4 | unknown |
| `0029fa08` | _gte_ncds_b() | 4 | unknown |
| `0029fa4c` | _gte_ncdt_b() | 4 | unknown |
| `0029fac0` | _gte_nccs_b() | 4 | unknown |
| `0029fb04` | _gte_ncct_b() | 4 | unknown |
| `0029fbb4` | _gte_cdp_b() | 4 | unknown |
| `0029fc20` | _gte_cc_b() | 4 | unknown |
| `0029fc74` | _gte_nclip_b() | 4 | unknown |
| `0029fcb4` | _gte_avsz3_b() | 4 | unknown |
| `0029fcf8` | _gte_avsz4_b() | 4 | unknown |
| `0029fcfc` | _gte_op12() | 4 | unknown |
| `0029fd00` | _gte_op12_b() | 4 | unknown |
| `0029fd04` | _gte_op0() | 4 | unknown |
| `0029fd08` | _gte_op0_b() | 4 | unknown |
| `0029fd0c` | _gte_gpf12() | 4 | unknown |
| `0029fd10` | _gte_gpf12_b() | 4 | unknown |
| `0029fd14` | _gte_gpf0() | 4 | unknown |
| `0029fd18` | _gte_gpf0_b() | 4 | unknown |
| `0029fd1c` | _gte_gpl12() | 4 | unknown |
| `0029fd20` | _gte_gpl12_b() | 4 | unknown |
| `0029fd24` | _gte_gpl0() | 4 | unknown |
| `0029fd28` | _gte_gpl0_b() | 4 | unknown |
| `0029fd2c` | _gte_mvmva_core(long) | 4 | unknown |
| `0029fd30` | _gte_mvmva_core_b(long) | 4 | unknown |
| `0029ff94` | SquareRoot12 | 4 | unknown |
| `002a010c` | RotMatrixC | 4 | unknown |
| `002a0818` | SetRotMatrix | 4 | unknown |
| `002a0d10` | SetTransMatrix | 4 | unknown |
| `002a1024` | OuterProduct12 | 4 | unknown |
| `002a1038` | CompMatrixLV | 4 | unknown |
| `002a1268` | TransRotPers | 4 | unknown |
| `002a1438` | SetFarColor | 4 | unknown |
| `002a143c` | SetBackColor | 4 | unknown |
| `002a2ff4` | InitHeap(unsigned long*, unsigned long) | 4 | unknown |
| `002a3110` | xpMallocSizeGet | 4 | unknown |
| `002a311c` | xpGetHeap | 4 | unknown |
| `002a3134` | xpMoveHeap | 4 | unknown |
| `002a379c` | pspSaveBase::ErrorMsgStrGet(pspSaveBase::PspSaveErrorMsgType) | 4 | unknown |
| `002ab710` | sceGuClearColor | 4 | unknown |
| `002ab714` | sceGuClear | 4 | unknown |
| `002ab888` | sceGuAlphaFunc | 4 | unknown |
| `002ab900` | sceGuColorFunc | 4 | unknown |
| `002ab904` | sceGuDisplay | 4 | unknown |
| `002abc88` | sceGuShadeModel | 4 | unknown |
| `002abd1c` | sceGuTexFunc | 4 | unknown |
| `002acb28` | sceGuViewport | 4 | unknown |
| `002b0420` | CAPP_INFO::~CAPP_INFO() | 4 | unknown |
| `002b04bc` | CAPP_INFO::IsEnableVibration() | 4 | unknown |
| `002b06b0` | CAPP_INFO::Get() | 4 | unknown |
| `002b142c` | SettingsBundle_Uninit() | 4 | unknown |
| `002b1454` | SettingsBundle_OnDefaultsChanged() | 4 | unknown |
| `002b1f38` | NowLoading_FrameRender() | 4 | unknown |
| `002b3440` | Achievement_Unlock(int) | 4 | unknown |
| `002b36b8` | Boot_Uninit() | 4 | unknown |
| `002b3758` | Error_Uninit() | 4 | unknown |
| `002b5590` | Link_Suspend() | 4 | unknown |
| `002b5594` | Link_Resume() | 4 | unknown |
| `002b5eac` | Logo_Suspend() | 4 | unknown |
| `002b5eb0` | Logo_Resume() | 4 | unknown |
| `002b6bcc` | Main_Resume() | 4 | unknown |
| `002bf1d8` | iOS_setFaceData(int, int, int, int) | 4 | unknown |
| `002bf1f8` | iOS_hook_request_status(int, int) | 4 | unknown |
| `002c54ac` | Movie_Uninit() | 4 | unknown |
| `002c6ef0` | Settings_Suspend() | 4 | unknown |
| `002c6ef4` | Settings_Resume() | 4 | unknown |
| `002c8abc` | SettingsWnd_Suspend() | 4 | unknown |
| `002c8ac0` | SettingsWnd_Resume() | 4 | unknown |
| `002ccf94` | _Unwind_Complete | 4 | unknown |
