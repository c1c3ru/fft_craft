# Notas de engenharia reversa

Alvo: `original/FFT_By_MortalGx.apk`
SHA-256: `d4478f550c59e1cd4e1bdc35cfbcca934432bf4b9b57d055554646ab2363586d`
Package: `com.square_enix.android_googleplay.FFT_en2` · versionCode `1002` ·
versionName `1.0.0` · minSdk 14 · targetSdk 21

Ferramentas usadas: REA (`rea-agents` CLI/MCP) com provider JADX
(`jadx-headless-mcp` 0.7.1) para inventário de artefato e decompilação
Java; leitura direta de ELF/AXML/ZIP para o restante.

## 1. Estrutura do APK

```
AndroidManifest.xml
classes.dex                 247 KB — só 57 classes, DEX pequeno
lib/armeabi/libgl2jni.so    4,46 MB — engine nativo do jogo
lib/x86/libgl2jni.so        4,99 MB
res/...                     ícones, layouts (main, licensing, notificação)
resources.arsc
META-INF/{MANIFEST.MF,CERT.SF,CERT.RSA}
```

Sem `assets/`. O jogo inteiro (texturas, música, eventos, mapas) mora fora
do APK, num arquivo de expansão OBB — ver seção 4.

## 2. A camada Java é só uma casca

`libgl2jni.so` exporta os símbolos JNI que a Activity chama
(`Java_com_square_1enix_FFT_1Android_GL2JNILib_{init,step,onTouchEvent,
onKeyEvent,setAccelerometerValue,setBatteryLevel,onPause,onResume,
onDestroy,isExit,getCommand,dialogOnClose}` + `JNI_OnLoad`). A lógica de
jogo propriamente dita está no nativo, não no Java — strings dentro da lib
confirmam `"FINAL FANTASY TACTICS: The War of the Lions"` e referências a
`fftpack.bin`, `g2d.dat`, `music.dat`, `sound.dat`, `music/track_%03d.ogg`,
`gTex16*.bin` (todos dentro do OBB).

## 3. Verificação de licença — patch identificado

Fluxo normal (Google Play Licensing / LVL):
`LicenseCheckerActivity.onCreate()` → `doCheck()` →
`LicenseChecker.checkAccess(mLicenseCheckerCallback)` → resposta do
servidor cai em `ServerManagedPolicy.processServerResponse()` → decisão
final em `ServerManagedPolicy.allowAccess()`.

`MyLicenseCheckerCallback.allow/dontAllow/applicationError` — código padrão
do Google, sem modificação. O patch real está em
`com.google.android.vending.licensing.ServerManagedPolicy.allowAccess()`:

```java
public boolean allowAccess() {
    long ts = System.currentTimeMillis();
    if (this.mLastResponse == 256) {
        if (ts <= this.mValidityTimestamp) {
            return true;
        }
    } else if (this.mLastResponse == 291 && ts < this.mLastResponseTime + 60000) {
        return (ts <= this.mRetryUntil || this.mRetryCount > this.mMaxRetries) ? true : true;
    }
    return true;   // original do Google: `return false;`
}
```

O retorno final foi trocado de `false` para `true`, e o ramo de retry foi
disfarçado num ternário que sempre dá `true` (`cond ? true : true`) — a
condição real não importa mais. Resultado: `allowAccess()` sempre libera,
independente de resposta do servidor, cache, ou contador de retries. É o
patch clássico "LVL always-true".

Localização para edição: `src/smali/com/google/android/vending/licensing/
ServerManagedPolicy.smali`, método `allowAccess()`.

## 4. Checagem de OBB — por que falta o arquivo

`FileChkActivity.onCreate()` chama `expansionFilesDelivered()`:

```java
private boolean expansionFilesDelivered() {
    File exdir = Environment.getExternalStorageDirectory();
    String obb_main_file_name = Helpers.getExpansionAPKFileName(this, true, BuildSettings.OBB_VERSION);
    File main_file = new File(exdir.getAbsolutePath() + "/Android/obb/" + getPackageName() + "/" + obb_main_file_name);
    return main_file.exists();
}
```

Checagem é só existência do arquivo (sem hash/tamanho). Nome/caminho
esperado (confirmado por string literal no DEX e por `versionCode=1002`):

```
/sdcard/Android/obb/com.square_enix.android_googleplay.FFT_en2/main.1002.com.square_enix.android_googleplay.FFT_en2.obb
```

Se o arquivo não existir, tenta baixar via `ObbDownloaderService`
(`DownloaderClientMarshaller.startDownloadServiceIfRequired`) — que fala
com a infraestrutura de expansion files do Google Play e, para um jogo
antigo/deslistado, não tem motivo pra funcionar.

Se o arquivo existir, `execute()` simplesmente abre `GL2JNIActivity`
(o jogo) e `finish()` — sem mais checagens.

**Importante:** patchear `expansionFilesDelivered()` para sempre retornar
`true` (mesma técnica usada no item 3) faz a Activity avançar, mas o
engine nativo ainda vai tentar ler `fftpack.bin`/`g2d.dat`/etc. de dentro
do diretório do OBB — sem o arquivo, o jogo deve crashar ou ficar em tela
preta/sem dados. Patch de código não substitui o dado que falta.

## 5. Assinatura

APK está assinado apenas com esquema v1 (JAR signing), sem APK Signing
Block v2/v3, usando a **chave de teste pública do AOSP**
(`CN=Android, emailAddress=android@android.com`,
SHA-256 `A4:0D:A8:0A:59:D1:70:CA:A9:50:CF:15:C1:8C:45:4D:47:A3:9B:26:98:9D:
8B:64:0E:CD:74:5B:A7:1B:F5:DC`) — chave pública e genérica, não a chave
original da Square Enix. Confirma reassinatura/repack, não indica por si
só o que foi alterado (isso veio das seções 3 e 4).

## 6. Classes do app (inventário completo via JADX, 57 classes)

```
com.square_enix.android_googleplay.FFT_en2.{BuildConfig,R,R$*}
com.square_enix.FFT_Android.{BuildSettings,FileChkActivity,FileChkActivity$1,
  GL2JNIActivity,GL2JNIActivity$1..9,GL2JNIActivity$9$1..3,GL2JNILib,
  GL2JNIView,GL2JNIView$ConfigChooser,GL2JNIView$ContextFactory,
  GL2JNIView$Renderer,LicenseCheckerActivity,LicenseCheckerActivity$1,
  LicenseCheckerActivity$MyLicenseCheckerCallback,ObbAlarmReceiver,
  ObbDownloaderService}
com.google.android.vending.licensing.*        (LVL padrão do Google)
com.google.android.vending.expansion.downloader.*  (downloader padrão do Google)
```

Nenhuma classe/pacote fora desse conjunto — não há biblioteca de terceiros
escondida nem código adicional do "cracker" (MortalGx) no DEX; a única
modificação de código encontrada é a do item 3.

## 7. OBB obtido — mismatch de versão corrigido

O `.obb` conseguido (`obb-data/main.202000.com.square_enix.android_googleplay.FFT_en2.obb`,
~815 MB) não é um ZIP — é uma **imagem de filesystem FAT32** (confirmado por
boot sector, OEM-ID `fat32lib`), o que é esperado: o jogo monta a OBB via
loopback (`StorageManager.mountObb`, visto em `GL2JNIActivity.mountObbAll()`
e nas strings `IsOBBPath`/`mountObb`/`getMountedObbPath` do `libgl2jni.so`).
Li o conteúdo sem precisar montar nada (parser FAT32 próprio em Python, sem
root). Estrutura:

```
base/fftpack.bin    213 MB
base/g2d.dat         22 MB
base/music.dat      132 MB
base/sound.dat      154 MB
base/font/*.tga
base/movie/00.mp4 .. 11.mp4   (12 cutscenes, ~290 MB)
```

O prefixo `base/` e os vídeos `movie/%02d.mp4` batem exatamente com strings
confirmadas dentro do `libgl2jni.so` (`/base/`, `movie/%02d.mp4`,
`_Z10movie_init...`) — a estrutura é compatível com o engine nativo deste
APK. Minha suspeita inicial de incompatibilidade de layout estava errada.

**O problema real era só o nome do arquivo.** O APK (como baixado,
versionCode 1002) constrói o nome esperado da OBB a partir de um inteiro de
versão que estava *inlined* (constant-folded pelo compilador) em três
pontos do bytecode — não dá pra corrigir só editando o campo
`BuildSettings.OBB_VERSION`:

| Arquivo | Local | Antes | Depois |
|---|---|---|---|
| `FileChkActivity.smali` | `expansionFilesDelivered()` | `const/16 v6, 0x3ea` | `const v6, 0x31510` |
| `GL2JNIActivity.smali` | `mountObbAll()` | `const/16 v1, 0x3ea` | `const v1, 0x31510` |
| `GL2JNIActivity.smali` | literal de string próximo | `"main.1002....obb"` | `"main.202000....obb"` |
| `BuildSettings.smali` | campo (só documentação, sem efeito) | `0x3ea` / `"1002"` | `0x31510` / `"202000"` |

`0x3ea` = 1002, `0x31510` = 202000. Detalhe importante: `202000` não cabe
em `const/16` (limite de 16 bits, máx. 32767) — foi preciso trocar a
própria instrução para `const` (32 bits), não só o valor, senão o
`apktool b` teria dado erro de overflow na montagem do smali.

Resultado validado: o `.dex` reconstruído contém `main.202000....obb` e não
contém mais nenhuma ocorrência de `main.1002....obb` (checado via
`zipfile` + busca de string no `classes.dex` final).

### Como instalar

```
scripts/build.sh        # gera o APK já apontando pra versão 202000
scripts/push-obb.sh      # copia obb-data/*.obb para /sdcard/Android/obb/<pkg>/
scripts/install.sh --launch
```

## 8. Ajustes para Android recente

Mudanças feitas no `AndroidManifest.xml`, todas de baixo risco (não alteram
comportamento em nada que já funcionava):

- `android:exported` explícito em todas as activities/service/receiver
  (`true` só na LAUNCHER; `false` nas demais). Não é exigido pelo
  `targetSdkVersion="21"` atual, mas é obrigatório pelo build do Android
  12+ (API 31+) para quem tem `<intent-filter>` — deixar explícito agora
  evita esse problema se o `targetSdkVersion` for elevado depois.
- `android:requestLegacyExternalStorage="true"` na `<application>` — rede
  de segurança para acesso a armazenamento externo caso o
  `targetSdkVersion` suba no futuro (acima de 29 essa flag é ignorada; hoje,
  com target 21, o comportamento legado já é o padrão do sistema).

**Decisão deliberada: não subi o `targetSdkVersion` (ficou 21).** Isso
pareceria "modernizar", mas na prática o Android passa a exigir *mais*
coisas de apps com target alto (scoped storage forçado, permissões em
runtime, `foreground service` com tipo declarado, restrições de broadcast)
— arriscaria quebrar mais do que resolve num app de 2012 sem o código-fonte
original pra ajustar. As duas flags acima dão compatibilidade futura sem
esse risco.

**Limitação real que nenhuma edição de manifesto/smali resolve:** as
únicas libs nativas no APK são `lib/armeabi/libgl2jni.so` (ABI genérica
ARMv5, descontinuada pelo NDK desde 2016) e `lib/x86/libgl2jni.so`
(32-bit). Não existe `arm64-v8a` nem `x86_64`. Em um device/emulador
64-bit-only (sem suporte a executar binário ARM/x86 de 32 bits), o sistema
não vai achar nenhuma lib compatível e o app falha ao carregar — isso não
tem solução via smali/manifest, exigiria recompilar `libgl2jni.so` a partir
do código-fonte C/C++ (que não temos) para `arm64-v8a`/`x86_64`.
Recomendação de teste: emulador AVD com imagem **x86** (32-bit) — a ABI
`lib/x86` já está no APK e esse caminho é o mais controlável para validar
sem depender de um device físico específico.

## 9. Engenharia reversa do `libgl2jni.so` nativo — módulos fora da IA de batalha (2026-10-14)

As seções 1–8 cobriram a camada Java/licenciamento/OBB. A IA de batalha
em si tem sua própria investigação, bem mais extensa, em
`docs/AI_DIFFICULTY_RESEARCH.md` (ver esse arquivo para `BattleRoutine`,
`FundamentalRoutine`, `EvaluationFunction` etc.). Esta seção cobre dois
módulos **fora** da IA, pedidos como itens de prioridade média/baixa
numa fila de engenharia reversa: o módulo de criptografia (`CCRYPT`) e o
parser de texturas TIM (`CG2D_LOADER_TIM`). Ferramenta: desmontagem
manual via Capstone (ARM), mesma técnica das seções de IA — Hopper
continua inutilizável neste ambiente (trava na inicialização).

### 9.1 Módulo `CCRYPT` — algoritmo decifrado por completo, e achado principal: não é usado

Localizado por nome exato no `.dynsym` (sem precisar adivinhar
endereço): `CCRYPT::Encrypt(uint8_t*, int, unsigned)` (`0xb6588`, 148 B,
lida por completo) e `CCRYPT::Decrypt(uint8_t*, int, unsigned)`
(`0xb661c`, só **4 bytes** — um `b 0xb6588` puro, ou seja, `Decrypt` é
literalmente um alias de `Encrypt`).

**O algoritmo é um XOR de 32 bits, não uma cifra real:**

```c
// CCRYPT::Encrypt == CCRYPT::Decrypt (mesma função, cifra simétrica)
int CCRYPT_EncryptDecrypt(uint8_t* buf, int len, uint32_t key) {
    uint32_t* p = (uint32_t*)buf;
    int n_words = len / 4;              // divisão com correção de sinal (idioma asr/lsr padrão)
    for (int i = 0; i < n_words; i++)
        p[i] ^= key;                     // XOR de 4 bytes por vez com a chave de 32 bits

    uint8_t key_bytes[4] = { (uint8_t)key, (uint8_t)(key>>8), (uint8_t)(key>>16), (uint8_t)(key>>24) };
    uint8_t* tail = buf + n_words*4;
    for (int i = 0; i < len % 4; i++)
        tail[i] ^= key_bytes[i];         // os 0–3 bytes finais, XOR com os bytes da chave em ordem
    return 0;
}
```

Sem S-boxes, sem rodadas, sem IV — é XOR direto com uma chave de 32 bits
repetida. Trivialmente reversível (por isso `Decrypt`==`Encrypt`: XOR é
sua própria inversa).

**Achado principal — rastreamento de XREFs (o que o item da fila
pedia):** varri o `.text` inteiro (2.4 MB) procurando por instruções
`bl`/`blx` cujo alvo calculado fosse `CCRYPT::Encrypt`/`Decrypt`, e
também por ocorrências do endereço dessas funções como dado bruto
(ponteiro de vtable/tabela de função) em `.rodata`, `.data`,
`.data.rel.ro*` e nos literal pools do próprio `.text`. **Zero
ocorrências em qualquer lugar.** Achei também `CFILE_DAT::Decrypt(int,
int, unsigned)` (`0xb6e38`, 56 B, lida por completo — é um wrapper fino:
`CCRYPT::Decrypt(CFILE_DAT::GetBuffer(idx), CFILE_DAT::GetSize(idx),
key)`), e **também não tem nenhum chamador** no binário ARM.

**Conclusão:** o módulo `CCRYPT` (e seu wrapper `CFILE_DAT::Decrypt`)
está presente no binário mas **não é alcançável por nenhum caminho de
execução** neste `.so` ARM — é código morto, quase certamente herdado de
uma base de código de engine compartilhada entre vários ports móveis da
Square Enix, não exercitado por este jogo especificamente. Isso é
consistente com o que a seção 7 já tinha documentado por outro ângulo:
o `.obb` lido diretamente (seção 7, `fftpack.bin`/`g2d.dat`/etc.) é
**legível sem nenhuma etapa de decriptação** — não há chave para
"extrair em tempo de execução ou memória estática" porque a cifra nunca
roda. Não verifiquei o binário x86 para esta seção (ficaria como
verificação rápida futura, mas o padrão de "classe de engine
compartilhada não usada neste jogo" não deve depender de arquitetura).

### 9.2 Parser de texturas TIM (`CG2D_LOADER_TIM`) — confirmado como código ativo, lido por completo

Ao contrário do `CCRYPT`, este módulo **é** alcançado por chamadas reais:
`CG2D_LOADER_TIM::Load(char*, uint8_t*, uint, uint)` (`0xa6cd0`, 204 B,
não lida em detalhe) chama `TIM_LoadFile` **ou** `TIM_LoadMemory`
dependendo do caminho de entrada; ambas chamam `TIM_AnalyzeFileHeader`
internamente. Os nomes e endereços exatos (achados direto no `.dynsym`,
sem precisar do Hopper):

| Função | Endereço/tamanho | Estado |
|---|---|---|
| `TIM_AnalyzeFileHeader(void*)` | `0xa6618`, 448 B | Lida por completo |
| `TIM_LoadFile(char*, uint)` | `0xa67d8`, 708 B | Lida por completo |
| `TIM_LoadMemory(uint8_t*)` | `0xa6a9c`, 500 B | Não lida (mesma forma geral, chama `TIM_AnalyzeFileHeader`) |

**`TIM_AnalyzeFileHeader` — bate exatamente com o formato TIM padrão do
PS1:**

```c
int TIM_AnalyzeFileHeader(TimState* out, const uint8_t* header) {
    uint32_t magic = read_u32_le(header);
    if (magic != 0x10) return 1;             // ID clássico do TIM (0x00000010)

    uint32_t flag = read_u32_le(header + 4);
    switch (flag & 7) {                       // bits 0–2 = modo de pixel, exatamente como o padrão TIM
    case 0: /* 4bpp com CLUT */   out->field14 = 0x18; out->field8 = 3; ... break;
    case 1: /* 8bpp com CLUT */   out->field14 = 0x10; out->field8 = 3; ... break;
    case 2: /* 16bpp direto */    if (!(flag & 8)) return 1; out->field14 = 8; ... break;
    case 3: /* 24bpp direto */    if (!(flag & 8)) return 1; out->field14 = 4; ... break;
    default: return 1;                        // modos 4–7 não existem no TIM, inválido
    }
    // em alguns sub-casos, grava uma mensagem (provável log/aviso,
    // formato tipo sprintf) num buffer em out+0x70 via uma função de
    // PLT não identificada (0x714b8), com um código numérico diferente
    // por ramo (0x16/0x19/0x1a) — não é um erro fatal, a função sempre
    // continua e devolve sucesso depois.
    return 0;
}
```

O bit 3 (`flag & 8`) é a flag clássica "tem CLUT" do formato TIM — exigida
para os modos 4bpp/8bpp (`flag&8` deve estar setada nesses dois casos
dentro do código, embora a leitura mostre o teste do lado contrário do
esperado para os modos diretos — documentei o comportamento real
observado, não o que o spec "deveria" exigir, já que pode haver uma
peculiaridade desta implementação específica).

**`TIM_LoadFile` — fluxo de leitura completo, com validações de
tamanho:**

```c
int TIM_LoadFile(TimOutput* out, char* path, void* scratch) {
    CFILE* file = new_cfile(path);               // aloca + construtor CFILE::CFILE
    if (CFILE::Open(file, 1) == 1 || CFILE::GetSize(file) <= 7) {
        if (file) { CFILE::~CFILE(file); free(file); }
        return 1;                                 // arquivo não abre ou é menor que o cabeçalho mínimo (8 B)
    }

    uint8_t header[8];
    CFILE::Read(file, header, scratch, 8, NULL);
    if (TIM_AnalyzeFileHeader(out, header) == 1) {
        if (file) { CFILE::~CFILE(file); free(file); }
        return 1;
    }

    if (out->modeField > 8) {                     // modos 4bpp/8bpp (têm CLUT)
        uint8_t clutHeader[12];
        CFILE::Read(file, clutHeader, scratch + 8, 12, NULL);
        // (tabela de salto de 21 casos para o tamanho declarado do
        // bloco de CLUT — maioria colapsa no caminho genérico; casos
        // especiais não decodificados individualmente)
        void* dst = alloc_or_validate(...);         // 0x2cdf8c, papel exato não resolvido
        out->paletteBuf = dst;
        CFILE::Read(file, dst, scratch + 8, clutSize, NULL);  // lê a paleta de verdade
    }

    if (out->modeField <= 8) {                     // modos 16bpp/24bpp direto (sem CLUT)
        uint16_t blockLen, orgX, orgY, width, height; // lidos via CFILE::Read de 12 bytes
        CFILE::Read(file, &pixelHeader, scratch, 12, NULL);
        uint32_t expectedPixelBytes = width * 2 * height;
        if (blockLen != expectedPixelBytes + 12) {
            goto FAIL;                              // validação de tamanho: rejeita TIM corrompido/malformado
        }
        CFILE::Read(file, out->pixelBuf, scratch, expectedPixelBytes, NULL);
    }

    CFILE::~CFILE(file); free(file);
    return 0;                                       // sucesso
}
```

Isso é um parser TIM **real e funcional**, com validação de tamanho de
bloco explícita (rejeita arquivos onde o tamanho declarado não bate com
`largura×altura×2+12`) — não é um stub nem código morto como `CCRYPT`.
Três chamadas de PLT não resolvidas (`0x2cdf6c`/`0x2cdf8c`/`0x2cdf9c`,
thunks de 12 bytes no fim do `.text`, perto de funções de runtime do
compilador como `__fixunsdfsi`) ficam sem nome — prováveis
alocador/validador de ponteiro, não essenciais para entender o formato
em si.

### 9.3 Estado da fila "prioridade média/baixa"
- **Item 6 (CCRYPT):** ✅ Concluído — algoritmo decifrado por completo
  (XOR de 32 bits), confirmado como código morto via varredura
  exaustiva de XREFs (nenhum chamador em `.text`, nenhuma referência de
  dado em nenhuma seção de dados).
- **Item 7 (parser TIM):** ✅ `TIM_AnalyzeFileHeader` e `TIM_LoadFile`
  concluídos. `TIM_LoadMemory` (caminho alternativo, mesma forma geral)
  e `CG2D_LOADER_TIM::Load` (o orquestrador que escolhe entre os dois)
  **não foram lidos** — ficam como extensão natural se for necessário.
- **Item 8 (outros motores — mapas, eventos/script, áudio, gráficos):**
  🔶 Levantamento inicial feito (seção 9.4) — não uma leitura completa,
  o escopo real é grande demais para isso numa sessão.

### 9.4 Item 8 — levantamento inicial dos "outros motores"

O `.dynsym` tem **6636 símbolos `FUNC`** no total — a IA de batalha
(seções 1–17 de `AI_DIFFICULTY_RESEARCH.md`) e os módulos das seções
9.1–9.2 cobrem uma fração pequena disso. Fiz um inventário por
contagem de métodos por classe C++ (via demangling do prefixo `_ZN`) e
por prefixo de função C simples, só para mapear onde cada motor mora —
**sem ler o código de nenhum deles em detalhe**, exceto um (`ScriptRead`,
abaixo) como prova de conceito.

**Gráficos:** `CEGL2_IF` (59 métodos), `CEGL2_SPRITE` (41),
`CEGL2_TEX_HYBRID` (25), `CEGL2_SHADER` (22), `CEGL2_FBO` (14),
`CEGL_PACKET` (31), `CGX_SCREEN_CORRECT` (34), `CSTEP`/`CSTEP_BATCH`
(39) — toda a stack é **EGL2** (OpenGL ES 2.0), não EGL1/fixed-function;
`CG2D_LOADER` + variantes (`_TIM`, `_BMP`, `_TGA`) é a família de
carregadores de textura (seção 9.2 cobriu só o `_TIM`).

**Áudio:** `CSOUND_IF` (45), `CSOUND_IF_SL` (39 — sufixo `SL` = OpenSL
ES, o backend de áudio real do Android), `CSOUND_LOADER_OGG` (14),
`CSOUND_LOADER_PCM` (11), mais funções C soltas (`SE_Play`, `SE_StopAll`,
`SE_SetVol`, `sound_request`, etc.) para efeitos sonoros.

**Save/Save-state:** prefixo `psp` em várias classes
(`pspSaveBase`/`pspSaveList`/`pspSaveAuto`/`pspFileManager`,
35+6+5+2 métodos) — **confirma que esta engine mobile descende de um
port PSP**, não é um port PS1 direto; `CAUTOSAVE`, `cSaveFFT`,
`iOS_CMenuTouchSaveLoad` complementam o sistema de save.

**Eventos/script (o mais relevante para "mapas, eventos"):** uma VM de
bytecode de eventos com pelo menos **60 funções** encontradas num grep
rápido (prefixos `event*`/`evt_*`) — exemplos: `event_init_system`,
`event_call(Match*, Match*)`, `MessageMake`, `ScriptRead(int,
TUTRIAL*)`, e **dezenas de handlers de opcode individuais**
(`evt_item`, `evt_eqp`, `evt_exit_jump`, `evt_dead_high`,
`evt_town_set`, `evt_rute_grow`, etc. — o nome de cada opcode já revela
sua função: equipar item, definir "vila"/estado de enredo, trocar de
mapa). Prefixo separado `mapclip_*` sugere um sistema de "clipping" de
mapa independente.

**`ScriptRead(int scriptId, TUTRIAL* out)` (`0x1a6530`, 88 B) — lida por
completo, como prova de conceito de que esta abordagem funciona para
este motor também:**

```c
void ScriptRead(int scriptId, TUTRIAL* out) {
    lock_or_init(&g_scriptTable[0x48]);              // 0x280678, papel exato não resolvido
    ScriptEntry* e = &g_scriptTable[scriptId - 1];     // tabela de 8 bytes por script
    void* data = LoadOrDecompressScriptBlock(e->offset /*+0x54*/, e->length /*+0x58*/); // 0x20ce14
    out->b[0x2a80] = g_someTable[scriptId - 1];        // outra tabela, 4 bytes/entrada
    out->b[0x2a84] = (uintptr_t)data;
}
```

É o **carregador** de um script individual (por ID), não o
interpretador/executor do bytecode em si — esse (provavelmente uma das
funções `event_*`/`evt_*` acima, ou uma rotina de despacho ainda não
localizada) não foi procurado nesta passada.

**Avaliação honesta de escopo:** este item sozinho (motor de
eventos/script, com dezenas a centenas de opcodes nomeados
individualmente) é comparável em tamanho a toda a investigação de IA de
batalha feita nas seções 1–17 do outro documento. Gráficos e áudio são
each, por si só, do tamanho de um motor de jogo completo. **Não é
razoável declarar o item 8 "concluído"** com o trabalho feito aqui — o
que existe é um mapa de onde cada peça mora, para quem quiser continuar
a partir de um ponto concreto em vez de do zero.

### 9.5 O interpretador de bytecode do motor de eventos/diálogo — achado e confirmado (2026-10-14, continuação)

Pedido explícito de continuação do item 8: achar o interpretador de
bytecode da VM de eventos. Processo de busca (documentado porque não é
óbvio e pode servir de referência para achar outras VMs no mesmo
binário): a primeira hipótese (`event_call`, a maior função da família
com 5456 B) **estava errada** — lendo-a por completo, ela não faz
busca/despacho de opcode nenhuma; é a função de **tick por frame** que
liga/desliga animações, música e vídeo ativos (um monte de `if
(slot>=0) call handler()` para cada tipo de recurso: animação de
modelo, animação VRAM, animação comprimida, música, filme). Isso por si
só é um achado útil, só que não é o que foi pedido.

**A busca real que funcionou:** nenhuma das 4 funções de opcode
testadas (`evt_item`, `evt_eqp`, `evt_town_set`, `evt_dead_high`) tem
**qualquer chamador direto** (`bl`) no binário — confirmando que são
chamadas indiretamente. Busquei os endereços dessas 4 funções como
**valor bruto de 4 bytes** em todas as seções de dado (`.rodata`,
`.data.rel.ro*`, `.data`) e achei os 4 juntos, lado a lado, em
`.data.rel.ro` a partir de `0x3455e4` — uma **tabela de ponteiros de
função**. Resolvendo as primeiras ~140 entradas (nome de cada endereço
via o `.dynsym`), a tabela tem exatamente **83 entradas válidas** a
partir desse ponto (índices "0–82" na numeração inicial) antes de virar
dado de outra natureza (vtables de `pspSaveBase`/`pspSaveList`/tabela de
unwind).

**Correção feita na continuação desta seção (ver `wld_event` abaixo):**
`0x3455e4` não é o início real da tabela — o dispatcher de verdade usa
uma base 12 entradas **antes** disso, em `0x3455b4`. A tabela completa
tem **95 entradas** (índices 0–94 a partir de `0x3455b4`):

- **Índices 0–4:** `evt_skip0`, `evt_flag`, `evt_flag_high`,
  `evt_flag_low`, `evt_chr` — 5 opcodes que a primeira varredura (a
  partir de `0x3455e4`) tinha perdido.
- **Índices 5–11:** 7 cópias repetidas de `evt_skip2` — slots de opcode
  reservados/não usados, todos apontando para o mesmo handler "no-op".
- **Índices 12–40 (29 opcodes `evt_*`):** `evt_item`, `evt_eqp`,
  `evt_gil_high/low`, `evt_date_high/low`, `evt_dead_high/low`,
  `evt_skip1/3/4`, `evt_exit_jump`, `evt_exit_sel`, `evt_flagset`,
  `evt_wldinfo`, `evt_deep`, `evt_fset_exit`, `evt_rute_grow/erase`,
  `evt_town_set/clr/cent`, `evt_brave_high/low`, `evt_faith_high/low`.
- **Índices 41–94 (54 opcodes `snpl_*`):** uma VM de script de
  **diálogo/novela visual** completa — saltos incondicionais/
  condicionais (`snpl_jp`, `snpl_je`/`jne`, `snpl_rndjp`,
  `snpl_jpageflg`/`jnpageflg`, `snpl_jstatflg`/`jnstatflg`,
  `snpl_jlocalflg`/`jnlocalflg`, `snpl_jparae`/`jparane`/`jparabig`/
  `jparasmall`), variáveis (`snpl_setpara`/`addpara`/`subpara`/
  `putpara`/`hidepara`/`chgpara`), flags (`snpl_setstat`/`clrstat`/
  `setlocal`/`clrlocal`), texto (`snpl_mesput`/`mesput2`/`mesput3`,
  `snpl_meswait`, `snpl_startpage`/`endpage`, `snpl_wordcol`),
  imagem (`snpl_picput`/`picclr`/`backput`), áudio
  (`snpl_sndreq`/`musicreq`/`sndstop`/`musicstop`/`envsndreq`/
  `volchg`), fade (`snpl_fadein`/`fadeout`/`mfadein`/`mfadeout`/
  `fadewait`), e controle (`snpl_wait`, `snpl_keywait`, `snpl_timeset`,
  `snpl_exit`, `snpl_scrdisp`, `snpl_effmode`, `snpl_selparacalc`).

**O dispatcher real: `wld_snpl()` (`0x26b0f4`, 456 B, lida por
completo).** Confirmado via um `blx r3` explícito em `0x26b12c`
(chamada indireta de verdade — o único jeito de ter certeza sem um
depurador rodando é achar a instrução `blx`/`bx` com registrador, o que
fiz varrendo o `.text` inteiro por esse padrão). O ponteiro base da
tabela usado aqui (`r8`, resolvido numericamente via a mesma cadeia
PC-relativa usada em toda a IA de batalha) é **`0x345658`, que é
exatamente `0x3455b4 + 41*4`** — ou seja, `wld_snpl` despacha só a
sub-tabela dos 54 opcodes `snpl_*` (a VM de diálogo), **não** os 29
`evt_*` (que devem ter um dispatcher próprio, ainda não localizado).

```c
// wld_snpl() — um "passo" do interpretador de script de diálogo
int wld_snpl(void) {
    SNPLINFO* s = g_currentScript;      // struct de estado do script atual
    void** opTable = (void**)0x345658;   // sub-tabela dos 54 opcodes snpl_*

DECODE:
    int opcode = s->b[8];                // opcode atual, 1 byte
    validate_or_log(opcode);             // 0x26b0e0, papel exato não resolvido
    opcode = s->b[8];
    ((void(*)())opTable[opcode])();      // *** blx r3 — A CHAMADA INDIRETA ***

    uint16_t flags = s->h[0xc] & ~0x10;
    if (flags & 0x28) { s->h[0xc] = flags; goto END; }
    s->h[0xc] = flags;

    // ... 3 leituras de parâmetro (0x103400) + snpl_effcheck + outro
    // helper (0x26abac) — contabilidade por frame, não ligada ao opcode em si

    uint16_t ip = s->h[0xc];
    if (ip & 2)  goto WAIT_OR_CALL;        // opcode pediu "espera" ou "chamada de sub-rotina"
    if (!(ip & 4)) goto DECODE;            // nada pendente -> busca o PRÓXIMO opcode já neste frame
    // ip&4: avança o ponteiro de dados do script para a próxima instrução
    // (lê uma palavra de uma tabela de dados do próprio script, grava em
    // s->b[8] como o novo opcode) e volta para DECODE sem passar por
    // validate_or_log() de novo.

WAIT_OR_CALL:   // ip&2 setado
    // se um contador de frames (via um global de "tempo") for > 4:
    //   copia um registro de 56 bytes (LDM/STM de 4+4+4+2 words) do
    //   estado atual do script para uma PILHA de chamadas indexada por
    //   esse contador -- GOSUB de sub-rotina de script, com pilha de
    //   retorno própria, não a pilha de chamadas C normal.
    // senão: recalcula o próximo ponteiro de instrução somando um
    // deslocamento lido dos dados do script a um "viés de carga"
    // (bias de PIC) reconstruído em tempo de execução -- confirma que
    // os PONTEIROS DENTRO DOS DADOS DO SCRIPT são relativos, não
    // absolutos (o script precisa ser "relocado" ao ser carregado).

END:
    ip &= ~0x18;
    s->h[0xc] = ip;
    return ((ip >> 5) ^ 1) & 1;    // 0 ou 1 -- provável "script ainda rodando?" ou "opcode pediu saída?"
}
```

### 9.6 O segundo dispatcher — `wld_event` (os 29 opcodes `evt_*`), fechando o item

Continuação direta do pedido ("continue com o que ainda falta"). Por
analogia de nome com `wld_snpl`, testei `wld_event(int, int)`
(`0x2590e8`, 236 B) — **achado de primeira**: tem um `blx r3` em
`0x259174`, mesmo padrão exato.

```c
// wld_event(int evtId, int flagMask) — um "passo" do interpretador evt_*
int wld_event(int evtId, int flagMask) {
    uint16_t* data = *g_eventDataBase;              // ponteiro global (dupla indireção GOT)
    uint16_t headerOff = data[evtId] & ~1;           // tabela de cabeçalho: 1 halfword por evtId
    uint16_t len = data[headerOff / 2];              // comprimento do bloco de instruções
    s->ptr[1] = (uint16_t*)data + headerOff/2;        // ponteiro pro bloco de instruções
    if (len == 0) return 0;                           // bloco vazio -> nada a fazer

    void** opTable = (void**)0x3455b4;                // a MESMA tabela, começando no índice 0 de verdade
    s->h[0xc] = 0; s->b[0] = 0;
    uint16_t* end = data + headerOff/2 + (len>>1)... ; // ponteiro de fim do bloco (aproximado)
    s->b[8] = end;                                      // (campo reaproveitado, papel exato não 100% isolado)
    int idx = 0;

DECODE:
    uint16_t opcode = instrBlock[idx++];
    ((void(*)())opTable[opcode])();                    // *** blx r3 — despacho real ***

    uint32_t flags = s->b[0];
    if ((flags & 3) == 0) goto DECODE;                  // continua lendo opcodes no mesmo passo
    if ((flags & 1) && (flags & flagMask)) return 1;     // opcode pediu parada "condicional ao chamador"
    // senão, avança para o próximo evtId na sequência (idx de evento, não de opcode) e repete
    ...
    return 0;
}
```

Confirmação numérica da tabela: `r5` (base usada no `blx`) resolve para
**`0x3455b4`** — a base REAL da tabela completa (corrigindo a seção 9.5:
o endereço `0x3455e4` usado ali era só onde a varredura inicial começou
a achar nomes conhecidos, não o início verdadeiro da tabela). Ou seja:
**`wld_event` usa a tabela completa desde o índice 0** (incluindo os 5
opcodes "novos" e os 7 `evt_skip2` de preenchimento), enquanto
`wld_snpl` usa só a sub-tabela a partir do índice 41. Isso é consistente
com os dois serem motores relacionados mas com numeração de opcode
independente dentro da mesma tabela física.

**Conclusão do item 8 (bytecode):** os dois interpretadores pedidos
estão achados e confirmados por instrução real (`blx r3`, não inferência):
`wld_snpl` (`0x26b0f4`) para o script de diálogo/novela visual e
`wld_event` (`0x2590e8`) para os eventos de mapa/mundo. A tabela de 95
opcodes está completamente resolvida por nome. O que resta do item 8 de
forma honesta: nenhum dos ~83 handlers de opcode individuais foi lido
por completo (só os nomes, que já são bastante autoexplicativos); o
restante do motor de mundo (`wld_*`, dezenas de funções de desenho/
UI/câmera do overworld) e os motores gráfico/áudio continuam como
levantamento de superfície (seção 9.4), não investigação.

### 9.7 Formato real da instrução — confirmado lendo 5 handlers pequenos (2026-10-14, continuação)

Para não parar só nos nomes, li por completo 5 dos handlers mais
simples (escolhidos por tamanho pequeno, para serem uma amostra rápida
e representativa): `evt_item`/`evt_eqp` (24 B cada), `snpl_jp` (32 B),
`snpl_je` (8 B) e `snpl_exit` (36 B). Isso é suficiente para confirmar
o **formato real da instrução** e o significado de vários bits do campo
de flags (`s->h[0xc]`) que `wld_snpl`/`wld_event` só tinham exposto por
fora (seção 9.5/9.6):

- **Instrução de 2 bytes:** opcode (1 byte, em `s->b[8]`) + 1 operando
  (1 byte, em `s->b[9]` — literalmente o byte seguinte no mesmo stream).
  `snpl_jp` lê `s->b[9]` como o índice de destino do salto e grava em
  `s->h[0xe]` (o mesmo campo que `wld_snpl` usa internamente como
  "próximo índice de dado a ler") — confirma que os saltos desta VM são
  por **índice de instrução**, não por endereço/offset de bytes.
- **Bit `0x20` de `s->h[0xc]` = "script terminou".** `snpl_exit` seta
  exatamente esse bit — e isso fecha o ciclo com o que `wld_snpl` testa
  depois de cada chamada de opcode (`flags & 0x28`, onde `0x28 =
  0x20|0x8`): é literalmente o jeito do opcode `exit` dizer ao
  interpretador "pare de rodar". `snpl_exit` também chama
  `0x28b034` (des-registro/limpeza, não identificado por nome) e
  termina com `mov r0,#4; b 0x153614` — um retorno para a família de
  funções de tarefa/thread vista no `event_call` (`asmTaskEntry`,
  `Wtask_status`), sugerindo que o script se desregistra do sistema de
  tarefas geral ao terminar.
- **Bit `0x2` de `s->h[0xc]` = "salto pendente"** (confirmado por
  `snpl_jp`, que seta esse bit depois de gravar o destino) — bate
  exatamente com o teste `if (ip & 2) goto WAIT_OR_CALL` já visto no
  pseudocódigo de `wld_snpl`.
- **Padrão "`_sub`" confirmado como helper compartilhado de verdade:**
  `snpl_je` é literalmente `{ mov r0,#1; b snpl_je_sub; }` (um
  tail-call de 8 bytes) — passa `r0=1` como "modo" para a implementação
  real em `snpl_je_sub` (`0x26ad5c`, 84 B, não lida). Por simetria quase
  certa, `snpl_jne` deve ser o mesmo tail-call com `r0=0`. O mesmo
  padrão deve valer para os outros 5 pares `_sub` já catalogados
  (`jpageflg`/`jnpageflg`, `jstatflg`/`jnstatflg`, `jlocalflg`/
  `jnlocalflg`).
- **Achado negativo, mas honesto:** `evt_item` e `evt_eqp` (ambos
  idênticos) só fazem `s->h[0xc] += 1` — não leem nenhum operando, não
  chamam nada. Isso pode significar que (a) são opcodes "marcador"
  cujo efeito real acontece em outro lugar lendo esse contador, ou (b)
  são vestigiais/nunca totalmente implementados nesta versão mobile.
  Não cheguei a uma conclusão definitiva com só esses dois exemplos.

**Estado final desta rodada:** os dois interpretadores (seção 9.5/9.6) e
o formato de instrução básico (esta seção) estão confirmados com alta
confiança, lendo instruções reais em vez de inferir pelos nomes. O que
sobra do item 8 — o restante dos ~90 handlers individuais, o motor de
mundo `wld_*` como um todo, e os motores gráfico/áudio — é trabalho
genuíno de escala grande, não uma lacuna pequena; continua em aberto.
