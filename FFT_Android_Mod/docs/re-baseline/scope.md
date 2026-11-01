# T02 — Matriz de escopo

Depende de T01 (`ready_for_review`, parcial — ver `T01_BASELINE_REPORT.md`). Executado em 2026-10-31.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** A matriz abaixo fixa versão/ABI/papel para tudo que foi hasheado em T01 e documenta decisão/origem para cada eixo do escopo pedido (componentes Android, motor, assets, idiomas, integrações). Dois pontos ficam como **decisão pendente do mantenedor** (não decididos unilateralmente por esta auditoria) e um ponto fica **indeterminado por achado técnico de T01** — listados na seção 6.

## 1. Versão-alvo primária

| Campo | Valor | Fonte |
|---|---|---|
| Artefato | `original/FFT_By_MortalGx.apk` (= `FFT By MortalGx.apk` na raiz, mesmo SHA-256) | T01, `artifacts.json` |
| SHA-256 | `d4478f550c59e1cd4e1bdc35cfbcca934432bf4b9b57d055554646ab2363586d` | T01 |
| Package | `com.square_enix.android_googleplay.FFT_en2` | `src/apktool.yml`, manifest |
| versionCode / versionName | `1002` / `1.0.0` | `src/apktool.yml` |
| minSdkVersion / targetSdkVersion | `14` / `21` | `src/apktool.yml` |
| ABIs presentes | `armeabi` (`libgl2jni.so`, 4.463.112 B), `x86` (`libgl2jni.so`, 4.988.572 B) | T01 |
| apktool usado para decode | `3.0.3` | `src/apktool.yml` |

Este é o artefato do qual `src/` foi decodificado e é a base de **toda** a engenharia reversa registrada em `RE_FUNCTION_INVENTORY.csv` e `docs/re-results/`. Nenhuma outra versão deve ser usada como fonte de endereços/offsets sem revalidação do SHA-256 do `.so` correspondente.

## 2. APK "2.2.0" — coluna própria (NÃO a versão-alvo)

| Campo | MortalGx (alvo primário) | `..._2.2.0-APK_Award-Mod.apk` |
|---|---|---|
| SHA-256 | `d4478f55...63586d` | `31bb102e...dfb92be` |
| ABI nativa | `armeabi` | `armeabi-v7a` (biblioteca de tamanho diferente — **não é o mesmo binário**) |
| `classes.dex` | 247.332 B | 1.457.440 B |
| Dependências Google | só LVL (licensing) | LVL + Google Play Services / Sign-In |
| Membros do ZIP | 19 | 71 (apenas 8 em comum com o MortalGx) |

**Decisão pendente do mantenedor:** este documento NÃO declara a comparação com o APK "2.2.0" como objetivo adicional. Trata-se de uma decisão de escopo de produto (se o projeto quer também reconstruir/comparar essa variante posterior com Play Services), não uma conclusão técnica que esta auditoria possa tomar sozinha. **Padrão adotado até decisão em contrário: fora de escopo.** Se o mantenedor decidir incluí-lo, isso exige T04 (inventário), T05 (reconciliação) e T31 (equivalência ARM/x86 — aqui seria armeabi-v7a) específicos para esse artefato, tratados como uma segunda linha de base, nunca somados à cobertura do MortalGx.

## 3. Componentes Android (do `AndroidManifest.xml` decodificado, `src/AndroidManifest.xml`)

| Componente | Tipo | `exported` | Papel |
|---|---|---|---|
| `GL2JNIActivity` | activity | `true` | Activity principal do jogo (`singleTask`, fullscreen, `sensorLandscape`) |
| `LicenseCheckerActivity` | activity | `true` | Launcher real (`MAIN`/`LAUNCHER`); dispara o fluxo LVL patcheado (seção 4) |
| `FileChkActivity` | activity | `false` | Verifica presença do OBB antes de abrir `GL2JNIActivity` |
| `ObbDownloaderService` | service | `false` | Download do OBB via infraestrutura de expansion files do Google Play |
| `ObbAlarmReceiver` | receiver | `false` | Agendamento/retomada do download do OBB |

Permissões declaradas: `ACCESS_NETWORK_STATE`, `ACCESS_WIFI_STATE`, `INTERNET`, `VIBRATE`, `WAKE_LOCK`, `WRITE_EXTERNAL_STORAGE`, `com.android.vending.CHECK_LICENSE`. `uses-feature glEsVersion=0x20000` (OpenGL ES 2.0, exigido).

Java/smali inventariado nesta revisão: 123 arquivos em `src/smali` (a nota histórica de "57 classes" citada em `REVERSE_ENGINEERING_NOTES.md` §6 referia-se à decompilação JADX de alto nível, não ao total de arquivos smali — a reconciliação completa é tarefa de T27, não repetida aqui).

## 4. Motor e integrações

| Item | Descrição | Escopo |
|---|---|---|
| `libgl2jni.so` | Motor nativo C/C++ (gráfico, som, input, lógica de jogo, IA — ver `libgl2jni_analysis_report.md`) | Núcleo do escopo de RE (T04–T26) |
| 12 métodos JNI exportados (`GL2JNILib`) | `init`, `step`, `getCommand`, `dialogOnClose`, `onTouchEvent`, `onKeyEvent`, `setAccelerometerValue`, `setBatteryLevel`, `onPause`, `onResume`, `onDestroy`, `isExit` + `JNI_OnLoad` | Fronteira Java↔nativo — mapeamento completo é T27 |
| Google Play Licensing (LVL) | Patch always-true em `ServerManagedPolicy.allowAccess()` | Comportamento **modificado** (seção 5) |
| Google Play Expansion Downloader | `ObbDownloaderService`/`ObbAlarmReceiver`, infraestrutura padrão do Google, não modificada no código Java (mas ver `OBB_VERSION`, seção 5) | Comportamento **original**, dependente de infraestrutura hoje provavelmente indisponível para este jogo (nota já registrada em `REVERSE_ENGINEERING_NOTES.md` §4) |
| OpenGL ES 2.0 / `GL2JNIView` | Superfície de renderização Android padrão | Comportamento **original** |

## 5. Assets

| Asset | Origem | Observação |
|---|---|---|
| `fftpack.bin`, `g2d.dat`, `music.dat`, `sound.dat`, `music/track_%03d.ogg`, `gTex16*.bin` | Dentro do OBB (não no APK) | Strings confirmadas no `.so` (`REVERSE_ENGINEERING_NOTES.md` §1) |
| Imagem FAT32 do OBB | `obb-data/main.202000....obb` **ou** o membro OBB embutido em `com.square_enix.android_googleplay.FFT_en2.zip` | **Indeterminado — ver seção 6.** T01 encontrou que os dois têm tamanho igual mas conteúdo diferente (206/778 blocos de 1 MiB, SHA-256/CRC32 diferentes). Nenhuma fonte no repositório indica qual é a imagem correta/atual. |
| `fftpatcher-src`, `nenkai-fftpack-filelist.txt` (em `docs/translation-research/`) | Material de terceiros (comunidade FFHacktics / projeto `Nenkai/fftivc.utility.modloader`) usado como referência para o parser de `fftpack.bin` | Ferramental auxiliar, não é asset do jogo — manter proveniência registrada ao usar (T29) |

## 6. Comportamento original vs. modificado vs. melhoria desejada

| Item | Classificação | Evidência |
|---|---|---|
| Lógica de jogo, engine, IA, renderização, áudio (tudo dentro de `libgl2jni.so`, salvo o patch de 181 bytes ainda não explicado) | **Original** (presumido — sem patch identificado além do já registrado) | T01 |
| Patch binário de 181 bytes em `.data` de `libgl2jni.so` (ARM e x86) | **Modificado — motivo ainda não identificado** | T01, `native_lib_patch_diff.json` |
| `ServerManagedPolicy.allowAccess()` sempre `true` | **Modificado** (patch de licenciamento "LVL always-true") | `REVERSE_ENGINEERING_NOTES.md` §3 |
| `BuildSettings.OBB_VERSION` = `202000` (em vez do `versionCode` original `1002`) | **Modificado** (correção de nome/versão do arquivo de expansão) | `src/smali/.../BuildSettings.smali`, confirmado em T01 |
| Reassinatura do APK com chave de teste AOSP | **Modificado** (consequência necessária de repack, não altera comportamento do app) | `REVERSE_ENGINEERING_NOTES.md` §5 |
| Tradução PT-BR (menus/nomes decodificados; diálogo de história bloqueado por bytecode de evento não documentado para WotL/mobile) | **Melhoria desejada, fora do escopo intrínseco de RE** desta versão | `docs/TRANSLATION_PTBR_PROGRESS.md` |
| Seletor de dificuldade de IA / IA "mais inteligente" | **Melhoria desejada, fora do escopo intrínseco de RE** — pesquisa inicial apenas, não implementada | `docs/AI_DIFFICULTY_RESEARCH.md` |
| Suporte a ABI 64-bit | **Fora de escopo** — nenhuma lib 64-bit existe nos artefatos atuais; exigiria projeto próprio (consistente com `RE_COMPLETUDE_TASKS.md` §2) | T01 |

## 7. Recursos explicitamente excluídos / indeterminados (bloqueiam alegação de cobertura irrestrita)

1. **Qual arquivo OBB é a linha de base** (seção 5) — decisão técnica pendente, não resolvida nesta tarefa; nenhuma tarefa de T08 em diante que dependa do conteúdo do OBB pode alegar cobertura completa enquanto isso não for resolvido.
2. **Se o APK "2.2.0" entra no escopo do projeto** (seção 2) — decisão de produto do mantenedor, não técnica; padrão atual é "fora de escopo".
3. **Tradução completa e suporte 64-bit** — explicitamente fora do escopo intrínseco de RE por definição do próprio `RE_COMPLETUDE_TASKS.md` §2; tratar como metas de produto separadas, com seus próprios critérios de aceite, se e quando forem priorizadas.
4. **Dispositivo real / infraestrutura de licenciamento e download do Google Play** — não testados nesta ou em nenhuma auditoria registrada até a data desta tarefa; qualquer afirmação de funcionamento end-to-end do fluxo de licença/OBB depende de T28/T38, ainda `pending`.

## 8. Como isso evita misturar hash/ABI/versão

Toda referência a endereço, offset ou achado neste projeto deve citar: (a) qual artefato (MortalGx vs. "2.2.0"), (b) qual ABI (`armeabi` vs. `x86` vs. `armeabi-v7a`, que é de um artefato diferente), e (c) o SHA-256 do `.so` correspondente — os três já tabulados em `artifacts.json` (T01). Um achado sem essas três referências é considerado não rastreável e não deve ser promovido a `read_full`/certificado.
