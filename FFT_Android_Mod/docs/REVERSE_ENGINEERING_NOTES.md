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

### 9.8 `TIM_LoadMemory` lida por completo — fecha o item 🟠 do plano (2026-10-16, loop de continuação, iteração 5)

A seção 9.2 já tinha identificado `TIM_LoadMemory` (`0xa6a9c`, 500 B)
mas não a tinha lido. Lida por completo agora, incluindo a tabela de
salto computada (`addls pc,pc,r6,lsl #2`, 21 entradas) que o
desmontador recursivo não alcança sozinho — extraída e decodificada à
mão lendo os 21 words crus da região `0xa6b04`–`0xa6b57` como
instruções `b` e resolvendo cada destino.

```c
// TIM_LoadMemory(TimObject* dst /*r5*/, uint8_t* src /*r4*/)
int TIM_LoadMemory(TimObject* dst, uint8_t* src) {
    if (TIM_AnalyzeFileHeader(dst, src) == 1) return <valor de r0 da chamada>; // magic/modo inválido

    TimSub* ip = dst->field_0x14;       // mesmo sub-struct que a seção 9.2 já nomeou
    int remaining = ip->field14;        // *** O MESMO `field14` da seção 9.2! ***
                                          // (0x18/0x10/8/4 conforme o modo de pixel)

    uint32_t sb;   // tamanho de dados calculado (pixels/CLUT), reaproveitado como base
    if (remaining <= 8) {
        // ---- CABEÇALHO "SIMPLES" (sem CLUT extra) ----
        uint16_t w = (src[0x10] | src[0x11]<<8) << 1;
        uint16_t h =  src[0x12] | src[0x13]<<8;
        sb = w * h;                                  // tamanho total dos dados de pixel, em bytes
        uint32_t declaredSize = *(uint32_t*)(src+8);  // campo de 4 bytes LE em src+8
        if (declaredSize != sb + 0xc) return 1;       // valida contra o tamanho calculado+12
        // tamanho bate -> "cai" dentro do mesmo laço abaixo com
        // r7=sl=sb+0x20, r8=0x14 (ver nota de comportamento compartilhado)
    }

    // ---- LAÇO (cabeçalho "estendido", ou continuação do caminho simples) ----
    int headerOff = 0x14, chunkIdx = 0, ofsA = headerOff, ofsB = 0;
    do {
        uint16_t a = src[8+8] | src[9+8]<<8;    // campo de 16 bits em (src+8)+8
        uint16_t b = src[0xa+8] | src[0xb+8]<<8; // campo de 16 bits em (src+8)+0xa
        remaining -= 4;
        int chunkSize;
        if (0 <= remaining && remaining <= 0x14) {
            // *** TABELA DE SALTO, 21 casos (r6=remaining, índice = remaining) ***
            switch (remaining) {
            case 20: {  // remaining==field14-4==20 <=> field14==24 (0x18) == modo 0, 4bpp+CLUT
                // divisão por constante (idioma clássico de compilador
                // pra "/3" via multiplicação de 64 bits + correção de
                // resto) -- fórmula exata não 100% isolada, mas o
                // padrão smull+mla+sub é inconfundível de "divisão por
                // uma constante não-potência-de-2"
                a <<= 1;
                int64_t q = ((int64_t)a * 0x55555556) >> 32;  // smull r0,r2,r1,r2 -- magic de "/3"
                int rem = a - q*3;
                chunkSize = b * (rem + q);
                ip->field_0xc = q;
                dst->field_0x10 = rem;   // nota: grava em `dst`, não em `ip` (único caso que diverge)
                break;
            }
            case 12: // field14==16 (0x10) == modo 1, 8bpp+CLUT
                chunkSize = (b * a) << 1;
                ip->field_0xc = a;
                ip->field_0x10 = b;
                break;
            case 4:  // field14==8 == modo 2, 16bpp direto
                a <<= 1;
                chunkSize = b * a;
                ip->field_0xc = a;
                ip->field_0x10 = b;
                break;
            case 0:  // field14==4 == modo 3, 24bpp direto
                a <<= 2;
                chunkSize = b * a;
                chunkSize >>= 1;
                ip->field_0xc = a;
                ip->field_0x10 = b;
                break;
            default: // casos 1,2,3,5–11,13–19 e fora de [0,20]: sem CLUT/tamanho extra
                chunkSize = 0;
                break;
            }
        } else {
            chunkSize = 0;  // remaining fora de [0,0x14]
        }

        // ---- cópia dos dados do chunk ----
        void* alloc = Allocate(chunkSize + ofsA);   // bl 0x2cdf8c
        dst->field_0x0 = alloc;
        dst->field_0x4 = (uint8_t*)alloc + ofsA;
        memcpy((uint8_t*)alloc + ofsA, src + ofsB, chunkSize);  // bl memcpy (0x714b8)

        if (ip->field14 <= 8) { dst->field_0xc = 0; return 0; }  // caminho simples termina aqui
        // (caminho "estendido" continuaria o laço — não observado
        // sendo re-executado numa 2ª iteração real nos dados de teste
        // alcançáveis por esta leitura; a estrutura do `do/while`
        // existe no código mas o corpo pós-primeira-iteração não foi
        // exercitado/confirmado neste passe)
    } while (/* nunca visto repetir na leitura atual */ false);

    return 0;
}
```

**Achados que fecham pontas da seção 9.2:**
- `ip->field14` (lido em `TIM_LoadMemory`) é **exatamente o mesmo
  campo** que `TIM_AnalyzeFileHeader` grava com os valores `0x18 / 0x10
  / 8 / 4` para os modos de pixel TIM padrão (4bpp CLUT / 8bpp CLUT /
  16bpp direto / 24bpp direto, seção 9.2). O índice da tabela de salto
  (`field14 - 4`) bate **exatamente** com essa tabela: casos `20/12/4/0`
  correspondem, em ordem, aos modos `0/1/2/3` — confirma que
  `TIM_LoadMemory` é o segundo "braço" (carregar de um buffer de
  memória já carregado, em vez de arquivo) do mesmo parser TIM, com o
  switch dedicado a calcular o tamanho da CLUT/paleta por modo de pixel.
- Única divergência real entre os 4 casos: o caso `20` (4bpp) precisa
  de uma divisão por 3 — **confirmado numericamente**: a constante do
  `smull` (`[pc,#0xc8]` em `0xa6bbc`, pool em `0xa6c8c`) é
  `0x55555556`, exatamente o multiplicador clássico de compilador
  gcc/clang pra "dividir por 3 via multiplicação de 64 bits"
  (`ceil(2^32/3)`). Isso bate com 4bpp CLUT ter 16 cores mas o campo
  de origem (`a`) provavelmente contar em unidades de 3 pixels/alguma
  razão ligada ao empacotamento 4-bit — os outros 3 modos (8bpp/16bpp
  direto/24bpp direto) só precisam de shift+multiplicação porque suas
  razões são potências de 2.
- O validador do caminho "simples" (`remaining <= 8`, i.e. `field14 <=
  8`, ou seja, modos 2/3 sem CLUT extra) recalcula o tamanho esperado
  (`largura*altura*2 + 12`) e **retorna erro (`1`) se não bater com o
  campo de tamanho declarado no próprio buffer** — é uma validação de
  integridade de dados, não só um parse cego.

### 9.9 O que ficou sem confirmar
- Se o `do/while` do caminho "estendido" (`field14 > 8`) de fato
  itera mais de uma vez em dados reais, e o que `ofsB`/`ofsA` valem
  numa 2ª iteração (a estrutura do código permite, mas só a primeira
  passada foi exercitada/lida com confiança total).
- O valor de retorno exato quando `TIM_AnalyzeFileHeader` falha (linha
  `beq 0xa6ba4`, `pop` sem `mov r0` explícito antes — herda o `r0` da
  chamada anterior, então provavelmente `1`, mas não cravado).

### 9.10 `CG2D_LOADER_TIM::Load` lida por completo — e correção de endereço no plano

**Correção importante:** o plano (`RE_BACKLOG_PLAN.md`) listava este
item em `0xa6cd0`, mas esse endereço cai **no meio** da função real —
o `.dynsym` dá o endereço certo: `_ZN15CG2D_LOADER_TIM4LoadEPcPhjj`
(`CG2D_LOADER_TIM::Load(char*, uchar*, uint, uint)`) está em
**`0xa6c90`**, 204 B (mesmo tamanho que o plano já tinha). Lida por
completo (51 instruções, 204 B exatos — cobertura total).

```c
// CG2D_LOADER_TIM::Load(this, char* path, uint8_t* buf, uint size, uint /*4º arg, não usado aqui*/)
int CG2D_LOADER_TIM::Load(CG2D_LOADER_TIM* this, char* path, uint8_t* buf, uint size) {
    memset((uint8_t*)this + 4, 0, 0x10);     // zera 16 B logo após o início do objeto
    TimSub* sub = this->field_0x14;           // mesmo sub-struct das seções 9.2/9.8
    sub->field_0x0 = -1;
    sub->field_0x4 = -1;

    int result = (path != NULL)
        ? TIM_LoadFile(this, path, size)        // 0xa67d8 — confirma: a escolha entre os
        : TIM_LoadMemory(this, buf);              // 0xa6a9c   dois é simplesmente "path != NULL"

    if (result == 1) return 1;                  // erro de parse, propaga sem tocar mais nada

    sub = this->field_0x14;        // relê o ponteiro (por segurança, pode ter mudado)
    sub->field_0x0 = 0xb;           // código de tipo/estado fixo = 11 (carregamento OK)

    if (this->field_0x18 == 0) return 0;   // sem pós-processamento de formato pedido

    // *** achado: GetImageFormatType/GetImageFormatExt retornam char*, não int ***
    strcpy((char*)&sub->field_0x20, GetImageFormatType(this, 0));              // 0xa65e0
    strcpy((char*)&this->field_0x14->field_0x50, GetImageFormatExt(this, -1)); // 0xa6608
    return 0;
}
```

**Achados:**
- Confirma, com o mecanismo exato, a frase da seção 9.2 ("escolhe entre
  `TIM_LoadFile`/`TIM_LoadMemory` dependendo do caminho de entrada"):
  a condição é literalmente **`path != NULL`** (2º parâmetro da função,
  `char*`) — nada mais sofisticado.
- `GetImageFormatType(int)` (`0xa65e0`, 40 B) e `GetImageFormatExt(int)`
  (`0xa6608`, 16 B) — catalogadas na tabela da seção 9.2 só por nome —
  **retornam `char*`** (usadas diretamente como origem de `strcpy`,
  resolvido via GOT/PLT: `0x714a0` = `strcpy`, técnica padrão desta
  investigação). São, quase certamente, "nome do formato de pixel" e
  "extensão de arquivo associada" (ex.: `"TIM"`/`".tim"`), gravados no
  sub-struct em `+0x20`/`+0x50` — mas o conteúdo exato das strings não
  foi lido (ficaria em `.rodata`, não investigado agora).
- `0xa6608` (`GetImageFormatExt`) é chamada com `-1` como argumento —
  convenção provável de "formato atual/default" (mesmo padrão de outras
  funções desta família que usam `-1` como sentinela, ver `field_0x0`/
  `field_0x4` setados pra `-1` no início desta mesma função).

## 10. Os handlers de opcode, quase todos lidos (2026-10-14, continuação "vamos para os 90 handlers")

Desmontagem em lote de **88 handlers** (`evt_*`/`snpl_*`, ~6,5 KB de
código total — pequeno, porque a maioria tem 24–120 bytes). A grande
maioria foi lida linha a linha; um punhado de variantes quase idênticas
foi confirmado por semelhança direta de bytes com uma já lida, não
transcrito de novo. O formato de instrução (seção 9.7: opcode+operando
de 1 byte cada, índice em `s->h[0xc]`) se confirma em **todos** os
handlers lidos, sem excessão.

### 10.1 Família de condição ("teste e marca bit 0x2")

O padrão mais comum entre os `evt_*`: ler 1 operando, comparar contra um
valor do jogo, e **setar o bit `0x2` do campo de flags** (`s->b[0]`) se
a condição for verdadeira — sem nunca limpar esse bit sozinho (outro
opcode deve consumi-lo). Confirmado em:

| Opcode | O que compara |
|---|---|
| `evt_gil_high`/`low` | Gil atual do jogador × (operando × 10) |
| `evt_dead_high`/`low` | Parâmetro global `#0x62` (contador de dias?) × operando |
| `evt_brave_high`/`low` | `Brave` (coragem) de um personagem × operando |
| `evt_faith_high`/`low` | `Faith` (fé) de um personagem × operando |
| `evt_date_high`/`low` | Dois pares de data (via helper `0x259324`) |
| `evt_flag`/`_high`/`_low` | Um "parâmetro" genérico via `GetParam()` (`0x103400`) × operando |
| `evt_chr` | Varre até 28 slots de personagem buscando um ID com flag específica (`0x82` no campo `+2`) |

Todos usam `GetParam()`/`0x103400` (a mesma função chamada por
`wld_snpl`/`wld_event` nas seções 9.5/9.6) ou `0x25e67c` (lookup de
personagem por ID) para buscar o valor comparado — nenhum lê dados do
jogo diretamente. **Hipótese razoável, não confirmada:** o bit `0x2`
provavelmente alimenta um opcode de "pular se falso" que não identifiquei
entre os nomes catalogados (os `evt_skip*` existentes são incondicionais
— sempre avançam N, não testam o bit). Pode ser que o próprio
`wld_event` leia esse bit entre uma chamada e outra (não confirmado) ou
que exista um opcode condicional com nome diferente do que esperava.

### 10.2 Família de controle de fluxo/exibição (`evt_*`, cada um com seu próprio bit único)

Confirma como `wld_event(evtId, flagMask)` decide quando parar: cada
opcode de controle seta, além do bit `0x1` comum, **um bit próprio e
exclusivo** — isso é literalmente o "motivo da parada" que o chamador
testa contra seu `flagMask`:

| Opcode | Bit exclusivo | Operandos lidos |
|---|---|---|
| `evt_exit_jump` | `0x8` | 2 (destino de salto, guardados em `+0x20`/`+0x24`) |
| `evt_exit_sel` | `0x4` | lista de pares, tamanho variável (laço até `+0x1c`) |
| `evt_wldinfo` | `0x10` | 1 |
| `evt_deep` | `0x20` | 3 |
| `evt_fset_exit` | `0x40` | 2 |
| `evt_rute_grow` | `0x80` | 2 |
| `evt_rute_erase` | `0x100` | 2 |
| `evt_town_set` | `0x400` | 1 |
| `evt_town_clr` | `0x800` | 1 |
| `evt_town_cent` | `0x200` (condicional) | 1 (com busca secundária se `0xff`, e chamada real a `wldcenter_set`, `0x268aec`, já catalogada na seção 9.4) |

### 10.3 `snpl_*` — mesmo esquema, bits diferentes, com efeitos reais confirmados

Os de controle puro repetem o padrão de "só seta um bit": `snpl_jp`
(`0x2`, mais o destino em `+0xe`, já visto na seção 9.7), `snpl_startpage`
(`0x4`), `snpl_endpage` (`0xa` = `0x8|0x2`), `snpl_wait` (espera por
contador de frame: compara dois valores globais e seta `0xc` = `0x8|0x4`
quando o tempo expira, senão incrementa o contador e continua
"esperando" sem terminar o passo atual).

Os de **efeito real** chamam funções de motor de verdade, confirmando
que a VM realmente comanda a engine subjacente (a mesma engine
PS1/EGL2/OpenSL já catalogada na seção 9.4):

- **`snpl_mesput`/`mesput2`** chamam `0x153584` e `0x153734` (função de
  registro de mensagem — mesma família de `MessageMake`/
  `MESSAGE_getMessageTaskKind` da seção 9.4) passando o ID da mensagem
  (operando) combinado com uma flag (`|0x8800`), e configuram campos de
  posição/layout (`+0x20`/`+0x22`/`+0x24`/`+0x26`) antes de setar o bit
  `0x4` ("mostrando mensagem").
- **`snpl_backput`** chama `DrawSync(0)` (nome real da lib gráfica do
  PS1, `0x290dc0`, já visto no `event_call` da seção 9.5) e depois
  `wldload_wait` (`0x25ee30`, catalogada na seção 9.4) — troca de
  imagem de fundo com sincronização de GPU de verdade, não só
  contabilidade de bits.

### 10.4 Estado final
As duas famílias de bit-flag (`evt_*` e `snpl_*`) e os principais tipos
de efeito (condição, salto, texto, imagem) estão confirmados por leitura
real de instrução, não por nome. Não lidos por completo: as variantes
de áudio (`snpl_sndreq`/`musicreq`/`envsndreq`), as de parâmetro
(`snpl_setpara`/`addpara`/`subpara`/`chgpara`), e ~15 das variantes mais
raras — todas devem seguir os mesmos dois padrões já confirmados (bit
simples vs. chamada real de engine), mas isso é inferência por
semelhança estrutural, não leitura linha a linha de cada uma.

### 10.5 Os 7 opcodes de áudio/parâmetro, lidos linha a linha — fecha o último item 🟠 (2026-10-16, loop de continuação, iteração 7)

Bônus desta leitura: o ponteiro global `s` (usado por **todos** os
`evt_*`/`snpl_*` desta investigação, sempre resolvido via GOT nas
seções 9.5–10.4 mas nunca nomeado) finalmente tem **nome real**,
cruzado por endereço no `.dynsym`: é o objeto global **`snpl_copy`**
(`0x6b251c`, 56 B). Essa é a "VM state" do interpretador do motor de
eventos inteiro.

**Os 3 de áudio são wrappers finos de 1 chamada cada** (confirma a
hipótese da seção 10.4):

```c
void snpl_sndreq(void)   { callSoundEffect(snpl_copy->b[9]); s->h[0xc] |= 4; }   // 0x26a1a4, chama 0x2168e4
void snpl_envsndreq(void){                                                        // 0x26ab70
    int v = (snpl_copy->field_0x8 & 0xff00) >> 8;
    if (snpl_copy->field_0x8 & 0xff0000) snpl_copy->h[0x32] = v | 0x4000;          // só grava se o byte "canal" for != 0
    envSound_play(0 /*ignora v, lê de novo internamente*/);                        // 0x26a85c
    s->h[0xc] |= 4;
}
void snpl_musicreq(void) { snpl_mreqcore(snpl_copy->b[9]); s->h[0xc] |= 4; }       // 0x26b0b8, chama 0x26aeec (172 B, não lida)
```

`callSoundEffect(int)` (`0x2168e4`) é, ela mesma, só um tail-branch de
4 B pra `0x27131c` (não lida). `envSound_play(int)` (`0x26a85c`, 24 B)
chama `0x21695c` e depois tail-branca pra `0x2168e8` (o endereço
**imediatamente depois** do `b` de `callSoundEffect` — ou seja,
`envSound_play` entra na mesma rotina de despacho de som, só que
pulando o primeiro passo). `snpl_mreqcore` (172 B) não foi lida por
dentro — catalogada por nome/tamanho, não é mais um opcode da VM, já é
"motor de música" de verdade.

**Os 4 de parâmetro revelam um mecanismo de duas fases que não estava
documentado:**

```c
void snpl_setpara(void) {               // 0x269930, 44 B
    int operand = (snpl_copy->field_0x8 & 0x00ffffff) >> 8;  // campo de 16 bits do opcode (mesmo formato da seção 9.7)
    snpl_copy->field_0x34 = operand;     // ESCREVE DIRETO no parâmetro de 32 bits
    s->h[0xc] |= 4;
}
void snpl_addpara(void) {               // 0x26995c, 48 B
    int operand = (snpl_copy->field_0x8 & 0x00ffffff) >> 8;
    snpl_copy->h[0x12] += operand;       // acumula num campo de 16 bits DIFERENTE — "delta pendente"
    s->h[0xc] |= 4;
}
void snpl_subpara(void) {               // 0x26998c, 48 B — idêntico ao addpara, troca + por -
    int operand = (snpl_copy->field_0x8 & 0x00ffffff) >> 8;
    snpl_copy->h[0x12] -= operand;
    s->h[0xc] |= 4;
}
void snpl_chgpara(void) {               // 0x269aa0, 104 B — o mais complexo dos 4
    int32_t acc = snpl_copy->field_0x34;         // o parâmetro de 32 bits "real" (o mesmo que setpara grava)
    int16_t delta = (int16_t)snpl_copy->h[0x12];  // o delta pendente de add/subpara, COM SINAL
    snpl_copy->h[0x12] = 0;                        // consome/zera o delta pendente
    acc += delta;
    if (acc > 0xffff) acc = 0xffff;                // clampa em [0, 0xffff] (parâmetro é efetivamente de 16 bits úteis)
    if (acc < 0)      acc = 0;
    snpl_copy->field_0x34 = acc;
    wldinfo_data1 = acc;    // *** grava o valor final também numa global do motor wld_*! ***
    s->h[0xc] |= 4;
}
```

**Achado principal:** `snpl_setpara`/`addpara`/`subpara` não tocam o
mesmo campo — `setpara` escreve direto em `snpl_copy->field_0x34` (o
"parâmetro real", 32 bits), enquanto `addpara`/`subpara` só acumulam
num campo de **delta pendente** separado (`snpl_copy->h[0x12]`, 16
bits com sinal). É **`snpl_chgpara`** quem de fato **aplica** esse
delta pendente ao parâmetro real, com saturação em `[0, 0xffff]`, e
zera o delta depois de consumido — um padrão "acumula, depois
confirma" explícito, não um jeito alternativo de escrever o mesmo
valor. **E `chgpara` propaga o resultado final pra fora da VM**,
escrevendo em `wldinfo_data1` (`0x67b31c`, 4 B) — uma global já
catalogada pelo nome na seção 11/12 (motor `wld_*`) mas nunca antes
conectada a um opcode do motor de eventos. Isso é uma ponte de
arquitetura real entre os dois sistemas documentados separadamente até
agora: **o motor de eventos (`wld_event`/`wld_snpl`) manipula
diretamente estado do motor de mundo (`wld_*`) através do opcode
`chgpara`**, não só pelos opcodes `evt_wldinfo`/`evt_town_*` já
catalogados na seção 10.2.

### 10.6 O que ficou sem confirmar
- O papel exato de `wldinfo_data1` dentro do motor `wld_*` (o que ela
  controla em termos de jogo) — catalogada só pelo nome/tamanho nas
  seções 11/12, não investigada por dentro.
- `snpl_mreqcore` (172 B) e os alvos de `callSoundEffect`/
  `envSound_play` (`0x27131c`/`0x21695c`) — não lidos por dentro (já
  são "motor de áudio", fora do escopo da VM de opcodes).
- Por que `envSound_play` é chamado com `0` fixo em vez do valor lido
  em `snpl_copy->field_0x8` — ou ela ignora o argumento e relê o campo
  internamente, ou o valor real já foi consumido/gravado em
  `snpl_copy->h[0x32]` antes da chamada (mais provável, dado o `strhne`
  condicional logo antes) — mecanismo plausível, não cravado com 100%
  de certeza sem ler `0x21695c`.

## 11. Motor `wld_*` — levantamento estrutural (2026-10-14, continuação "o motor wld* inteiro")

Pedido explícito de ir atrás do motor `wld_*` inteiro. Avaliação honesta
primeiro: existem **mais de 100 funções** com esse prefixo (mundo/
overworld — telas de viagem entre cidades, menu de status do grupo,
animação de passeio no mapa mundi). Ler cada uma por completo está fora
de escopo realista para uma sessão; o que segue é um levantamento
estrutural (quem chama quem, tamanhos, papel por nome) com 2–3 funções
centrais lidas por completo como amostra, no mesmo espírito da seção 9.4
mas uma camada mais profunda.

**Inventário:** exatamente **74 funções** `wld_*`/`wld*`, somando
**20.672 bytes**. Achado de arquitetura confirmado por leitura real
(não só por nome): `world_map()` (`0x25fd70`... endereço exato
`0x25f354`+offset — função de 1004 B) é o controlador de nível mais
alto, chamando `wldnormal_lop()` ou `wldfast_lop()` dependendo de
alguma condição (provavelmente "botão de avanço rápido pressionado") —
mesmo padrão de duas variantes de laço já visto no padrão `ctl*_main`
(seção 9.5/9.6).

### 11.1 `wldnormal_lop()` (`0x25f694`, 764 B) — lida por completo: é o laço de frame real, e confirma que a engine usa a biblioteca gráfica do PS1 de verdade

Chamadas confirmadas por nome (25 chamadas distintas, zero ambiguidade):

```
wldpad_read()                    -- lê input
wldpnl_calc()                    -- calcula posição/painel
wldwalk_rute()                   -- avança a animação de "andar pela rota"
GsClearOt() / GsSortClear()      -- limpa a Ordering Table da GPU
wldbg_draw(ot)                   -- desenha o fundo
wldrute_draw(ot) / rutegrow_draw(ot)  -- desenha a rota/caminho
wldiwasaki_put(ot)               -- desenha um elemento (papel exato não identificado pelo nome)
wldpac_draw(ot, ...)             -- desenha um "PAC" (sprite animado, ver wld_anim)
wldday_put(ot)                   -- desenha o indicador de dia/data
wldtname_put(ot)                 -- desenha o nome da cidade atual
wldinfo_put(ot)                  -- desenha o painel de informação
wldsymbol_draw() / wldtown_draw() -- desenha símbolos/cidades no mapa
ctleeff_draw(ot)                 -- desenha efeitos de controle/UI
pspWorldCheckFlg(...) / pspWorldBlackSpotDraw(ot, ...)  -- feature "PSP" de bloqueio de área do mapa
SetSpadStack() / ResetSpadStack() -- pilha de scratchpad (memória rápida do PS1, emulada)
xpLibgsAddOt(...) / GsDrawOt(ot) -- envia a Ordering Table pra GPU
GsSwapDispBuff()                 -- troca os buffers de tela (double buffering)
DrawSync(0) / VSync(1)           -- espera a GPU/o vsync terminar
```

Isto é, literalmente, **um laço de frame de jogo PS1 completo**: lê
input → atualiza lógica → monta a lista de primitivas da GPU (a
"Ordering Table", `GsOT`, estrutura real da PSYQ/PSn00bSDK) → envia pra
GPU → espera o vsync. `GsClearOt`, `GsSortClear`, `GsDrawOt`,
`GsSwapDispBuff`, `xpLibgsAddOt` são todos nomes de função **genuínos
da biblioteca gráfica original do PS1** (`libgpu`/`libgs`) — confirma
com instrução real (não só suspeita, como na seção 9.5) que esta
engine mobile reimplementa a API gráfica do PS1 por completo
(provavelmente em cima do `CEGL2_*`/OpenGL ES 2.0 catalogado na seção
9.4) em vez de ter sido reescrita do zero. `SetSpadStack`/
`ResetSpadStack` ("scratchpad") reforça isso — scratchpad é uma memória
específica do hardware PS1 (não existe em Android), então até esse
detalhe de baixo nível foi preservado/emulado.

### 11.2 Inventário categorizado das outras 72 funções (por nome, não lidas)

| Categoria | Funções |
|---|---|
| **Ciclo de vida/controle** | `world_map`, `wldctl_cur/active/deactive/init` (mesmo padrão `init/active/main/deactive` de `ctlnobel_*`, seção 9.6), `wldlop_chk`, `wldstart_check` |
| **Inicialização** | `wldbg_init`, `wldscr_init`, `wldpara_init` (**a maior de todas, 1256 B**), `wlddraw_init`, `wldiwasaki_init`, `wldkey_repinit`, `wldpac_init`, `wldrute_init`, `wldsymbol_init`, `wldtown_init` |
| **Desenho** | `wldbg_draw`, `wldiwasaki_put`, `wldpac_draw`, `wld_window`, `wldday_put`, `wldtname_put`, `wldinfo_put`, `wldrute_draw`, `wld_anim(ANMPAC*,GsOT*)` (852 B — desenha um sprite animado genérico), `wldsymbol_draw`, `wldtown_draw`, `wldtown_bright` |
| **Janelas de UI** | `wldwintex_point`, `wldwin_set`, `wldwin_trans`, `wldwin_noropen`, `wldpicwin_set`, `wldmess_put`, `wldmess_frm` |
| **Movimento/câmera** | `wldwalk_rute` (**1108 B**, 2ª maior — máquina de estados de "andar pela rota"), `wldrute_tblget`, `wldcenter_chk/calc/set/move`, `wldmap_scrol` |
| **Persistência/save** | `wldbin_loadchk`, `wldbinEntry`, `wldmapEntry`, `wldscr_snapshot`, `wldCdRead` (nome com "Cd" = CD-ROM, outro resquício literal do PS1!), `wlddata_load`, `wldmes_load`, `wld_btlsect_seek`, `wld_dayread`/`wld_daywrite`, `wldday_countup` |
| **Transição/fade** | `wldfade_set`, `wldfade_proc`, `wldfade_mask` |
| **Estado de tela/frame** | `wlddisp_mask`, `wldframe_clr`, `wldfrm_clr`, `wldfrm_rect` |
| **Encontros/loja/evento** | `wldencount_chk`, `wld_shop`, `wld_event` (seção 9.6), `wld_snpl` (seção 9.5) |
| **Widget "SSD"** | `wldssd_control` (620 B), `wldssd_wait` (papel exato do acrônimo não identificado) |
| **Áudio** | `wldmusic_change` |
| **Tutorial** | `wld_tutomenu_reset(CTLINFO*)` |

### 11.3 Estado do item 8 ao final desta sessão
Os dois interpretadores de bytecode (seção 9.5/9.6), o formato de
instrução e quase todos os handlers de opcode (seção 10), e agora a
arquitetura completa + um laço de frame real do motor `wld_*` (seção
11) estão documentados com evidência de instrução, não suposição. O que
seria necessário para "terminar" o item 8 de verdade: ler as outras ~72
funções `wld_*` uma a uma (a maioria pequena, mas `wldpara_init`/
`wldwalk_rute`/`wldinfo_put`/`wld_anim` têm 850–1250 B cada e mereceriam
atenção própria), e só depois disso passar para os motores gráfico
(`CEGL2_*`) e de áudio (`CSOUND_IF`/`CSOUND_IF_SL`) que ainda não foram
tocados em nenhuma leitura de código, só citados por nome na seção 9.4.

## 12. As 72 funções `wld_*` restantes — conclusão da fila (2026-10-16, skill `engenharia-de-loop`)

Pedido explícito: concluir as 72 funções restantes seguindo a skill de
engenharia de loop (ciclo lote→leitura→validação→documentação,
escalando honestamente em vez de forçar "concluído" sem ter lido).
Desmontei as 71 funções restantes em lote (uma única leitura de
Capstone por função, ~5.300 B no total) e resolvi **150 das 151**
chamadas distintas feitas por elas antes de ler qualquer corpo — isso
sozinho já revelou peças novas importantes (lib GTE/matemática 3D do
PS1 genuína: `RotMatrix`, `TransMatrix`, `ScaleMatrix`,
`SetGeomOffset`, `RotTrans`/`RotTransSV`, `PSX_csqrt`; a camada de
compatibilidade `xp*`/`psp*`; e `Shop`, `InitializeGame`, `resetFFT`,
`worldmap_call`, `worldmap_startinit` como funções de nível ainda mais
alto que as já documentadas).

### 12.1 Cobertura real por função (honestidade de escopo)

Das 71, **cerca de 20 foram lidas linha a linha por completo**
(escolhidas por tamanho — são as maiores, então cobrem a maior parte
dos ~16 KB de código real, já que `wldnormal_lop` da seção 11.1 por si
só é 764 B). As demais ~50 são pequenas (muitas <100 B) e foram
caracterizadas pela lista de chamadas resolvida (seção 12, acima) e por
semelhança estrutural direta com as já lidas — não por leitura
byte-a-byte individual. Nenhuma das 72 ficou **sem nenhuma informação**
(todas têm pelo menos papel + chamadas confirmadas).

### 12.2 Achados principais das funções lidas por completo

**`wldwalk_rute()` (`0x2691cc`, 1108 B — a maior de todas) é o coração
do "andar pelo mapa mundi":**
```c
void wldwalk_rute() {
    if (!walking_active) return;
    if (paused) return;
    if (step < total_steps) {
        step++;
        // interpolação linear 3D entre waypoint atual e próximo
        pos.x = start.x + (end.x - start.x) * step / total_steps;  // __divsi3 real
        pos.z = start.z + (end.z - start.z) * step / total_steps;
        sprite->x = pos.x; sprite->y = ...;   // atualiza posição do sprite
        wldmap_scrol(&delta);                  // move a câmera/mapa junto
        return;
    }
    // chegou no waypoint: avança época e checa gatilhos
    wldday_countup();                          // o relógio do jogo avança ao andar
    wldmusic_change(...); wld_event(nextPanel, 0x40);  // checa evento de história no painel
    if (event_found) { /* ativa ctleeff, desativa walk, deixa o evento tocar */ }
    else {
        r = wldencount_chk(panelType, routeId);  // checa encontro aleatório
        if (r) { /* marca flag de batalha pendente, som, sai do andar */ }
        else   { wldrute_tblget(...); /* próximo segmento de rota */ }
    }
}
```
Isso é, literalmente, **o loop de jogo do mapa mundi do FFT**: andar é
uma interpolação contínua, cada waypoint alcançado dispara a checagem de
evento de história OU de encontro aleatório, e o tempo do jogo (dias)
avança conforme você anda.

**`wldencount_chk(int panelType, int routeId)` (`0x269034`, 408 B) —
achado importante, liga diretamente à dificuldade:**
```c
int wldencount_chk(int panelType, int routeId) {
    EncounterEntry* e = findEntry(panelType - 0x18, routeId);  // tabela de 18 terrenos × até 3 rotas
    if (!e) return 0;
    if (GetParam(dayThreshold) <= e->minDay) return 0;         // encontro só libera depois de X dias
    int chance = e->chanceByte;
    int mode = CFFT_STATE::GetParam(0);                        // *** modo de dificuldade ***
    int roll = (mode==1) ? chance-1                              // fácil: quase garante
             : (mode==2) ? (chance*100)>>15                      // difícil: escala diferente
             :             chance;                                // normal: direto
    if (ps_rand() > roll) return 0;
    // sorteia qual, dentre as batalhas disponíveis (bitmask de 8 bits), vai disparar
    ...
    return 1;  // encontro disparado, grava mapa/rota escolhidos em globais
}
```
**A taxa de encontro aleatório no mapa mundi é modulada pelo mesmo
`CFFT_STATE::GetParam(0)` (modo de dificuldade)** — um mecanismo de
dificuldade **complementar** ao da IA de batalha (seções 1–17 do outro
documento), e não documentado antes nesta investigação. Vale registrar
como achado relevante para qualquer trabalho futuro de "seletor de
dificuldade".

**Outras funções lidas por completo, resumo de papel confirmado:**

| Função | Achado confirmado |
|---|---|
| `wldbg_init`/`wldbg_draw` | Inicializa e desenha até 17 tiles de fundo (`GsSortPoly` por tile) |
| `wldpnl_calc` | Transforma cada painel do tabuleiro 3D via GTE (`RotTrans`) e calcula visibilidade/texture page |
| `wldctl_cur`/`active`/`deactive`/`init` | Framework de "controladores" **genuinamente polimórfico** — despacho por `blx` numa tabela de função indexada, mesma arquitetura `init/active/main/deactive` de `ctlnobel_*` (seção 9.6), agora confirmada em C/C++ puro com vtable manual |
| `wld_shop` | Entra na loja: `Shop()` real, muda música, desativa o controlador de mapa |
| `wldframe_clr` | Limpeza de framebuffer PS1 genuína (`ClearImage`+`DrawSync`) |
| `wldscr_init`/`wlddraw_init` | Inicialização de modo gráfico completa (`GsInitGraph2`, `GsInit3D`, `SetGeomOffset`) |
| `wldpara_init` (1256 B, a 2ª maior) | Zera/reseta **todo** o estado global do módulo mapa-mundo antes de entrar nele — função "limpa tudo" |
| `wldstart_check` | Decide, ao entrar no mapa mundi, se há evento/loja/flag pendente a processar antes do loop normal |
| `wldiwasaki_init`/`_put` | Sistema de dica do NPC "Iwasaki" (nome próprio preservado) — mensagens de hint no mapa mundi |
| `wldpad_read` | Lê `pspNetPadRead()` (abstração de input incluindo rede/bluetooth) |
| `wldkey_rep` | Auto-repeat de botão genérico, com contador de delay por botão |
| `wlddisp_mask` | Esconde/mostra em lote 3 listas de objetos (bit `0x8`) |
| `wldfade_set`/`wldfade_proc` | Máquina de estado de fade, disparando `ssd_request` (música/som) nos pontos certos |

### 12.3 Estado final do item 8 (CCRYPT/TIM/outros motores)
Com esta seção, a lista completa de alvos originais do item 8 tem:
**CCRYPT e parser TIM — concluídos** (seção 9); **o motor de
eventos/diálogo (dois interpretadores de bytecode + quase todos os
opcodes) — concluído** (seções 9.5–10); **o motor `wld_*` de mapa
mundo — concluído no nível de "arquitetura + principais mecânicas
confirmadas por leitura real"**, com as ~20 funções maiores lidas por
completo e as ~50 menores caracterizadas por chamada/padrão, não
byte-a-byte individual (seção 12.1 documenta essa distinção com
honestidade). **Não tocados em nenhum nível de código:** o motor
gráfico `CEGL2_*` (OpenGL ES 2.0) e o motor de áudio `CSOUND_IF`/
`CSOUND_IF_SL`/OpenSL ES — ambos só aparecem na seção 9.4 como
inventário de classes por nome, sem nenhuma função lida. Esses dois
continuam sendo o trabalho genuíno que falta para "item 8" no sentido
mais completo possível.

### 12.4 `wldinfo_put` lida por completo — item 🟠 que tinha ficado esquecido no plano (2026-10-16, loop de continuação, iteração 19)

O plano (`RE_BACKLOG_PLAN.md`) ainda tinha um item 🟠 pendente —
"as ~50 funções pequenas restantes de `wld_*`" — que uma iteração
anterior do loop **pulou por engano** ao avançar direto pra 🟡/⚪. Lido
agora `wldinfo_put(GsOT*)` (`0x266f30`, 1040 B, a maior ainda não lida
da lista sugerida pelo próprio plano), incluindo a tabela de salto
computada de 5 casos (extraída à mão, mesma técnica das seções 9.8/21).

**Confirmado por nome real de função (sem precisar adivinhar pelo
contexto): é o painel de HUD do mapa mundi que mostra o Gil (dinheiro)
do jogador**, construído inteiramente sobre a API real da biblioteca
gráfica do PS1 (`GetTPage`, `GsSortFastSprite` — mesmo padrão
`GsOT`/`GsSPRITE` já confirmado nas seções 11.1/13.1):

```c
void wldinfo_put(GsOT* ot) {
    if (globalFlags & 0x800) return;     // bit "painel de info escondido"

    GsSPRITE spr = {};
    // ... monta um sprite base (tamanho/posição/UV herdados de um
    // sprite global de fonte/painel) e aplica um efeito de cor via
    // fadeanb_calc(&colorA, &colorB) — 0x25e160, cálculo de
    // interpolação de cor (efeito de "pulsar"/fade do painel)

    switch (displayMode) {    // 5 casos, via tabela de salto computada
    case 0: infonumber_put(x, y, &spr, ot); break;              // 0x266900 — desenha um número via sprites
    case 1: pspGetWarFundsOfs(&wofs,&hofs);                       // 0x266efc
            info_war_funds(ot, &spr, &line);                        // 0x266b94 — *** desenha o Gil de verdade ***
            break;
    case 2: GsSortFastSprite(&panelBg, ot, 0);                    // GsSortFastSprite real da lib PS1
            infonumber_put(...); infonumber_put_zero(...); ...      // vários números no mesmo quadro
            break;
    case 3: GsSortFastSprite(&otherSprite, ot, 0);
            /* desvia pro FINAL do case 4 — tail-merge do compilador */
            break;
    case 4: pspGetWarFundsOfs(&wofs,&hofs);
            GsSortFastSprite(&panelBg, ot, 0);
            info_war_funds(ot, &spr, &line);                         // 0x266b94 de novo
            infonumber_put_zero(x, y, &spr, ot, 5);                   // 0x266a00 — número com zeros à esquerda
            break;
    }
}
```

**Achados:**
- Confirma, com nomes reais de função (`info_war_funds`,
  `pspGetWarFundsOfs`, `infonumber_put`/`infonumber_put_zero`), que
  este painel **mostra o Gil do jogador no mapa mundi** — `info_war_
  funds` é chamada diretamente 2 das 5 vezes (casos 1 e 4).
- Todas as 5 variantes do switch estão construídas sobre chamadas
  reais da biblioteca gráfica do PS1 (`GetTPage`/`GsSortFastSprite`),
  reforçando que o motor `wld_*` inteiro (mapa mundi) ainda roda sobre
  a emulação dessa API, não sobre o `CEGL2_*` moderno diretamente —
  consistente com a arquitetura já confirmada nas seções 11.1/13.1
  (a emulação PS1 monta primitivas, e só depois `CEGL2_IF::DrawPacket`
  as converte pra GL de verdade).
- `fadeanb_calc` (`0x25e160`) aplica um efeito de cor variável ao
  painel — provavelmente o "pulsar"/fade visual clássico de painéis de
  HUD do FFT original.

**O que ficou sem confirmar:** a semântica exata de cada um dos 5
modos além dos dois que chamam `info_war_funds` diretamente (0, 2 e 3
desenham números, mas não ficou claro O QUE exatamente — dia do mês?
nível médio do time? só reaproveitamento do mesmo painel pra outro
dado numérico?) — ficaria pra uma leitura futura de `info_war_funds`/
`infonumber_put` por dentro. As demais ~49 funções pequenas de
`wld_*` continuam só por chamada/padrão (seção 12.1).

### 12.5 `wld_anim` lida — último item 🟡 da Fase 2 (2026-10-16, Fase 2, iteração 18)

`wld_anim(ANMPAC* anim, GsOT* ot)` (`0x2660b8`, 852 B, cobertura
total: 207 instruções pra 207 esperadas) — segunda das 3 funções
`wld_*` grandes sugeridas pelo plano (depois de `wldinfo_put`, seção
12.4). Resolvendo os `bl` por nome: `GetTPage` e `fadeanb_calc` (já
conhecidas, seção 12.4) e **`GsSortFlipSprite`** (nova — mais uma
função real da biblioteca gráfica do PS1).

**Confirmado com alta confiança: é o "tocador" de animação de sprite
do mapa mundi.**

```c
void wld_anim(ANMPAC* anim, GsOT* ot) {
    // *** cor de tingimento: fixa (bit 0x400 setado) ou pulsante via
    // fadeanb_calc (bit 0x400 limpo, mesmo efeito da seção 12.4) ***
    uint16_t tintColor = (anim->flags & 0x400) ? anim->field_0x20 : fadeanb_calc(&anim->field_0x20, &localColor);

    AnimTable* table = g_animTables[anim->animID];   // anim->+4 indexa uma tabela global por nome de animação

    if (!(anim->flags & 0x800) || !(g_someConfig->flags & 0x8000000)) {
        anim->tickCounter++;                            // avança o relógio da animação

        // percorre `table` a partir de `anim->seqIndex` (+0xc),
        // somando a DURAÇÃO de cada entrada (empacotada nos 16 bits
        // altos de cada word da tabela) até achar em qual quadro-chave
        // o `tickCounter` atual cai — reinicia pra entrada 0 se
        // ultrapassar o fim (looping de animação)
        KeyFrame* frame = find_current_keyframe(table, anim->seqIndex, anim->tickCounter);

        for (int i = 0; i < frame->subSpriteCount; i++) {
            // decodifica campos empacotados do quadro-chave (escala,
            // rotação/flip, offset de posição — formato clássico de
            // "transform compactado" de engine PS1, bits espalhados
            // em `0x70000000`/`0x30000000`/`0x8000000`/etc.) e acumula
            // posição em `localX`/`localY`
            int tpage = GetTPage(mode, x, y, subSprite->w, subSprite->h);  // 0x291348
            GsSortFlipSprite(&sprite, ot, anim->priority);                    // *** 0x29bbec — desenha com suporte a espelhamento ***
        }
    }
}
```

**Achados:**
- Confirma `GsSortFlipSprite` como mais uma função real da biblioteca
  gráfica do PS1 usada neste motor (junto com `GetTPage`/
  `GsSortFastSprite` já confirmadas na seção 12.4) — **suporte real a
  espelhamento de sprite** (horizontal/vertical), técnica clássica
  pra reaproveitar arte de animação (ex.: andar pra esquerda = sprite
  de andar pra direita espelhado).
- Reusa o MESMO mecanismo de cor pulsante (`fadeanb_calc`) do painel
  de HUD (`wldinfo_put`, seção 12.4) — confirma que esse efeito de
  "pulsar"/fade é uma capacidade genérica do motor `wld_*`, não
  exclusiva do HUD.
- Estrutura de animação confirmada: uma tabela de quadros-chave por
  animação (indexada globalmente por ID), com duração empacotada nos
  bits altos de cada entrada, suporte a múltiplos "sub-sprites" por
  quadro (animação composta/segmentada, não um único sprite só) e
  looping automático ao esgotar a sequência.

**O que ficou sem confirmar:** a decodificação bit a bit exata dos
campos de transform empacotados no quadro-chave (escala/rotação
específicas) — confirmado QUE existem e são decodificados, mas não a
fórmula geométrica exata de cada bit.

### 12.6 `wldrute_draw` lida por completo — continuação da varredura `wld_*` (2026-10-16, continuação)

`wldrute_draw(GsOT* ot)` (`0x267f3c`, 740 B, cobertura total: 185
instruções pra 185 esperadas). Resolvendo os `bl` por nome: mais um
punhado de funções genuínas da biblioteca gráfica do PS1 —
`SetPolyFT4`, `SetSemiTrans`, `GetClut`, `GsSortPoly`, `RotTransSV`
(GTE) — além de `Wread_eventflag` (motor de eventos, seção 9.5/10) e
`xpLibGetOffset` (camada de compatibilidade `xp*`).

```c
void wldrute_draw(GsOT* ot) {
    if (!(g_someFlags & 0x20)) return;    // bit "rotas visíveis" (não cravado 100%)

    POLY_FT4 poly = {};
    SetPolyFT4(&poly);
    SetSemiTrans(&poly, 1);                 // *** desenha semi-transparente ***
    poly.tpage = GetTPage(...);
    poly.clut  = GetClut(16, 0x1e8);
    xpLibGetOffset(&offX, &offY);

    for (int routeId = 0; routeId < 0x25c /* 604 */; routeId++) {
        if (!Wread_eventflag(routeId)) continue;    // *** só desenha rotas cuja flag de evento está ativa ***

        RouteTable* table = g_routeTables[routeId];     // tabela global, indexada por routeId
        int segCount = table->count;
        if (segCount <= 0) continue;

        for (int seg = 0; seg < segCount; seg++) {
            // lê a posição 3D do segmento, projeta pra tela via RotTransSV
            // (GTE real), checa um limite de distância/clipping, e desenha
            // o segmento como um quad via GsSortPoly(&poly, ot, 1) quando
            // dentro do alcance de desenho
            RotTransSV(&segment3D, &screenPos);
            if (/* dentro do limite de clipping */)
                GsSortPoly(&poly, ot, 1);
        }
    }
}
```

**Confirma, com leitura real, que `wldrute_draw` é o desenho da linha
de rota caminhável do mapa mundi**: itera até 604 rotas possíveis,
só desenha as que têm a flag de evento (progresso de história) ativa,
projeta cada segmento via GTE de verdade (`RotTransSV`), e desenha
como quads semi-transparentes. Confirma de novo (seção 11.1 já tinha
mostrado isso pra outras funções) que o motor `wld_*` roda sobre a
emulação real da API gráfica do PS1, não uma reescrita.

**O que ficou sem confirmar:** a fórmula exata de clipping/distância
(as comparações contra `0xf2`/`0x150` em ponto fixo) e o papel exato
do bit `0x20` do flags global.

### 12.7 `wldssd_control` lida por completo — correção: não é widget de UI, é música (2026-10-16, continuação)

`wldssd_control()` (`0x26b378`, 620 B, cobertura total: 153
instruções reais + pool de literais). A seção 11.2 catalogava essa
função como "widget 'SSD', acrônimo não identificado" — **corrigido
agora**: resolvendo os `bl` por nome, aparecem só funções de música
(`loadMusicBuffer`, `disposeMusic`, `activateMusic`, `inactivateMusic`,
`fadeMusic`). "SSD" é quase certamente "Sound/Stream Sequence Data"
ou similar — **é a máquina de estados que controla a música de fundo
do mapa mundi**, não um widget visual.

```c
void wldssd_control() {
    MusicCtl* g = *g_musicCtl;   // global, via GOT

    switch (g->state /*+0x80*/) {   // tabela de salto, 18 estados + default
    default:                          // volta pro "idle"
        g->state = 0; goto TOP;

    case 1:   // fade de saída concluído -> libera o buffer
        int ch = g->fadeOutDuration ?: g->currentChannel;   // +0x84 / +0x98
        disposeMusic(ch);
        if (g->currentChannel == ch) g->playingFlags &= ~1;   // +0x8c
        g->channelSlot[ch] = 0;                                  // +0x23+ch, array por canal
        goto TOP;

    case 2:   // contagem decrescente de fade-in
        if (--g->fadeCounter != 0) return;     // +0x84
        g->playingFlags |= 1; g->state = 0;       // +0x8c
        goto TOP;

    case 3:   // contagem decrescente de fade-out
        if (--g->fadeCounter != 0) return;
        g->playingFlags &= ~1;
        inactivateMusic();                          // *** desativa a música de verdade ***
        g->state = 0;
        goto TOP;

    case 17:  // espera uma flag externa (motor de áudio ocupado?) antes de continuar
        if (g_someAudioBusy->field_0x4 != 0) return;
        goto TOP;

    case 4:   // inicia fade-in de verdade
        activateMusic(g->currentChannel, 0, 0);
        fadeMusic(g->fadeTargetVolume, g->fadeCounter * 4);   // *** fade real, duração = contador×4 ***
        g->state = 0x12;   // vai pro estado 18 (laço de fila)
        return;

    case 5:   // inicia fade-out de verdade
        if (!(g->playingFlags & 1)) goto TOP;
        fadeMusic(0, g->fadeCounter * 4);
        g->state = 0x11;    // vai pro estado 17 (espera externa)
        return;

    case 0 (via tabela, entrada 2): // *** processa um pedido de troca de música ***
        if (g_someAudioBusy->field_0x4 != 0) return;
        int reqChannel = (g->pendingRequest >> 8) & 0xf;
        int reqTrack   = g->pendingRequest & 0xff;
        int loaded = g->channelSlot[reqChannel];
        if (loaded == reqTrack) {
            activateMusic(reqChannel, reqTrack, reqTrack);   // já carregada -> só reconfigura
            g->currentChannel = reqChannel; g->state = reqTrack;
        } else {
            if (loaded != 0) disposeMusic(loaded);              // libera a anterior desse canal
            int ok = loadMusicBuffer(reqTrack, reqChannel);        // *** carrega a nova faixa ***
            if (ok) {
                g->channelSlot2[reqChannel] = reqTrack;
                g->currentChannel = reqChannel; g->state = 0x10;      // vai pro estado 16
            } else g->state = 0;
        }
        return;

    case 18 (0x12, via tabela, entrada 1): // *** laço da FILA de comandos pendentes ***
        int n = g->queueCount;    // +0x88
        if (n == 0) return;
        g->fadeCounter = g->queue[0].a;    // +0x40
        g->state       = g->queue[0].b;     // +0x0
        if (--n > 0)
            memmove-shift(g->queue, 1, n);    // desloca a fila 1 posição (consome o comando processado)
        g->queueCount = n;
        goto TOP;   // reprocessa o switch com o novo estado já carregado
    }
}
```

**Achados:**
- **Corrige a categorização da seção 11.2**: `wldssd_control` é um
  controlador de música, não um widget de interface. Confirma, junto
  com `wldmusic_change` (já citada, mas não lida), que existe um
  sistema real de **fila de comandos de música** — pedidos de troca
  de faixa são enfileirados e processados um por tick da máquina de
  estados, com fade-in/fade-out reais via `fadeMusic`/
  `activateMusic`/`inactivateMusic`.
- 18 estados numerados confirmam uma máquina de estados genuína (não
  um conjunto de flags soltas) — states 1-5 cobrem o ciclo completo
  "liberar buffer antigo → contar fade → ativar/desativar", states
  16-18 cobrem "carregar nova faixa → esperar o motor de áudio →
  consumir a fila".

**O que ficou sem confirmar:** o papel exato de cada campo do
`MusicCtl` global (nomes de campo são hipóteses baseadas no uso, não
cravados), e a identidade do "something busy" global checado nos
estados 17 e na troca de faixa.

### 12.8 `wldfade_proc` lida por completo — confirma a ponte com a máquina de música da seção 12.7 (2026-10-16, continuação)

`wldfade_proc()` (`0x25df88`, 472 B, cobertura total: 114 instruções
reais + pool de literais). Fecha a nota da seção 11.2 ("`wldfade_set`/
`wldfade_proc` disparando `ssd_request`") com um nome real:
**`iOSwldssd_wait()`** (`0x26b6e0`) é exatamente essa chamada.

```c
void wldfade_proc() {
    FadeCtl* g = *g_fadeCtl;
    if (!(g->flags & 1)) return;              // bit "fade ativo"

    if (g->curFrame == g->totalFrames) {        // chegou ao fim -> desliga tudo
        g->flags &= ~0xd;
        return;
    }

    if (g->curFrame + 2 == g->totalFrames) {
        g_worldFlags->flags &= ~8;
        iOSwldssd_wait();        // *** espera a máquina de estados de música (seção 12.7) terminar ***
    }

    g->curFrame++;
    int r, gC, b;   // 3 canais de "ambiência" (tingimento de tela)
    if (g->flags & 2) {    // *** fade IN (clareando) ***
        int t1 = g->curFrame * 0x80 / g->totalFrames;   // __divsi3 real, interpolação linear
        r = max(0x70 - t1, 0);
        int t2 = g->curFrame * 0x100 / g->totalFrames;
        b = min(t2 + 0x20, 0xff);
    } else {                  // *** fade OUT (escurecendo) ***
        int t1 = g->curFrame * 0x80 / g->totalFrames;
        r = min(t1 + 0x10, 0x80);
        int t2 = g->curFrame * 0x100 / g->totalFrames;
        b = max(0xc0 - t2, 0);
        pspWorldDisableFlg(4);     // *** desliga uma flag "mundo" nº 4 durante o fade-out ***
    }
    changewindowamb(r, r, r);        // *** aplica o tingimento de tela de verdade ***
    g->ambR = b; g->ambG = b; g->ambB = b;   // grava os canais calculados (+0x24/+0x25/+0x26)

    if (!(g->flags & 4)) g_otherFlags->flags |= 2;
}
```

**Achados:**
- **Confirma a ponte real entre o fade visual e a música**:
  `iOSwldssd_wait()` é literalmente "espera a máquina de estados de
  música (seção 12.7) consumir sua fila antes de continuar o fade" —
  sincroniza a transição de tela com a transição de áudio, não são
  dois sistemas independentes.
- Confirma uma curva de interpolação assimétrica real pros canais de
  "ambiência" (tingimento de tela): fade-in e fade-out usam fórmulas
  espelhadas, não um fade linear simples de brilho — um canal decresce
  enquanto o outro cresce, com faixas de valor diferentes (`0x70→0` e
  `0x20→0xff` pro fade-in, invertido pro fade-out).
- `pspWorldDisableFlg(4)`/`pspWorldEnableFlg(4)` confirmam mais uma
  flag "mundo" numerada (bit 4), ligada/desligada em pontos específicos
  do fade — provável "input desabilitado durante a transição", papel
  exato não cravado.

**O que ficou sem confirmar:** o papel exato de `changewindowamb`
(usa os 3 canais calculados como R/G/B, mas o nome sugere algo mais
amplo que "cor") e o significado preciso da flag "mundo" nº 4.

### 12.9 `wldcenter_chk` lida por completo (2026-10-16, continuação)

`wldcenter_chk(_POINT* pos)` (`0x268aec`, 176 B, cobertura total: 42
instruções pra 42 esperadas) — função folha, sem chamadas.

```c
int wldcenter_chk(_POINT* pos) {
    if (pos->x >= -0x18) {                       // x dentro da margem pela esquerda
        if (pos->x <= 0x20 && *g_marginA <= 8)      // E dentro da margem pela direita (threshold via global)
            goto CHECK_Y;
        return 1;                                     // fora da margem horizontal -> precisa recentrar
    }
    if (*g_marginB <= 0x20) goto CHECK_Y;
    return 1;

CHECK_Y:
    if (pos->y < -0x40)
        return ((0x50 - g_someGlobal->field_0x4) > 0x20) ? 1 : 0;
    if (pos->y > 0x40)
        return (g_otherGlobal->field_0x4 >= -0xf) ? 1 : 0;
    return 0;    // dentro de ambas as margens -> não precisa recentrar
}
```

**Confirma, com leitura real, o papel exato sugerido pelo nome**: é
o teste "a posição está fora da margem de centralização da câmera do
mapa mundi?" — compara `x`/`y` contra limites fixos (`±0x18`-ish em
X, `±0x40` em Y), com alguns dos limiares vindo de globais de
configuração (prováveis dimensões de tela/viewport, não cravados).
Retorna `1` (precisa recentralizar) ou `0` (está dentro da margem).

**O que ficou sem confirmar:** a identidade exata dos 2-3 globais
usados como limiar — prováveis dimensões de viewport/mapa, papel
não cravado byte a byte.

### 12.10 `wldday_put` lida por completo — maior função "Desenho" ainda sem leitura linha a linha (2026-10-16, Fase 2, continuação)

`wldday_put(GsOT* ot)` (`0x266c84`, 372 B, cobertura total: 60
instruções pra 60 esperadas + pool de literais de 4 words) — a maior
função não lida da categoria "Desenho" da tabela da seção 11.2.
Resolvendo os `bl` por nome: **`fadeanb_calc`** (`0x25e160`, já
confirmada na seção 12.4), **`wld_anim`** (`0x2660b8`, já lida por
completo na seção 12.5), e duas funções nunca tocadas antes —
**`Wread_eventflag(int)`** (`0x103400`) e
**`sun_to_ivarisday(int*, int*)`** (`0x25e310`, demangle confirmado
via `.dynsym`).

```c
void wldday_put(GsOT* ot) {
    if (!(*g_panelVisFlag & 0x1000)) return;        // bit "painel escondido" (global diferente do 0x800 da seção 12.4)

    Color faded;
    fadeanb_calc(&g_dayPanelColor, &faded);           // mesmo efeito de "pulsar" do HUD (seção 12.4/12.5)

    int x = g_dayAnchorPos->x;                          // struct global de 2 words (posição-base do widget)
    int y = g_dayAnchorPos->y - 2;

    int a = Wread_eventflag(46);
    int b = Wread_eventflag(47);
    sun_to_ivarisday(&a, &b);                           // converte os 2 flags em (?, dia a exibir) — corpo não lido

    ANMPAC digit = { .flags = 1, .priority = 4, .seqIndex = 0x1000,
                      /* +0x10/+0x14 também = 0x1000 */ .x = x, .y = y };

    if (b <= 9) {
        digit.animID = b + 0x2c;         // dígito único (0–9)
        wld_anim(&digit, ot);
        digit.x += 0xa;
        digit.animID = a + 0x1f;          // ícone/glifo fixo após o número
        wld_anim(&digit, ot);
        return;
    }
    // dois dígitos: desenha a dezena primeiro
    digit.animID = (b / 10) + 0x2c;      // divisão real via constante mágica 0x66666667
    wld_anim(&digit, ot);
    digit.x += 8;
    digit.animID = (b % 10) + 0x2c;      // unidade
    wld_anim(&digit, ot);
    digit.x += 0xa;
    digit.animID = a + 0x1f;              // mesmo ícone fixo final
    wld_anim(&digit, ot);
}
```

**Achados:**
- **Confirma um segundo chamador real de `wld_anim`** (seção 12.5)
  fora do sistema de personagens do mapa mundi: cada dígito (0–9) e um
  ícone/glifo final são montados como um `ANMPAC` temporário na pilha
  e desenhados pelo mesmo "tocador" de animação genérico — o
  `animID` escolhido é literalmente `dígito + 0x2c`, ou seja, existem
  entradas de tabela de animação dedicadas a cada dígito (0x2c–0x35) e
  pelo menos mais uma (`a + 0x1f`) pro glifo fixo.
- A divisão por 10 usa a mesma constante mágica clássica
  (`0x66666667`, multiplicação de 64 bits + shift) que a seção 10 já
  tinha visto em contexto de bytecode — aqui é só aritmética de
  compilador pra `/10`/`%10`, não um opcode de VM.
- **Achado novo, nunca tocado antes:** `Wread_eventflag(int)`
  (`0x103400`) é chamada com os índices **46** e **47**, e o par de
  resultados passa por `sun_to_ivarisday(int*, int*)` (`0x25e310`)
  antes de qualquer dígito ser desenhado. Ou seja, **o valor exibido
  por este widget não vem direto do contador de dias do
  `wldday_countup` (seção 12.2)** — vem de dois flags de evento
  convertidos por uma função dedicada. Como `sun_to_ivarisday` tem
  nome claramente ligado a calendário ("dia"), a hipótese mais provável
  é que este widget mostra uma **data/dia específico de um evento de
  história** (gatilhado pelos flags 46/47), não o relógio genérico do
  mapa mundi — mas isso não está cravado, porque nem `Wread_eventflag`
  nem `sun_to_ivarisday` foram lidos por dentro.
- O painel usa um bit de visibilidade diferente (`0x1000`) do painel
  de Gil (`0x800`, seção 12.4) — confirma que cada widget de HUD tem
  seu próprio bit de controle na mesma palavra de flags globais (ou em
  globais vizinhos), não um único "esconder tudo".

**O que ficou sem confirmar (escalonado, não forçado):**
- O corpo de `Wread_eventflag`/`sun_to_ivarisday` — logo, a semântica
  exata de "o que são os flags 46/47" e "o que exatamente `a` (o
  glifo final) representa" ficam como hipótese, não fato.
- Os três campos do `ANMPAC` temporário todos setados pro mesmo valor
  `0x1000` (reaproveitamento de registrador `r4` que também guarda o
  bit de visibilidade testado no início) — pode ser coincidência de
  geração de código ou um sentinela deliberado; não investigado mais a
  fundo.
- Os dois globais resolvidos só por offset de GOT (posição-base do
  widget e cor-base do painel) não têm nome — mesma honestidade já
  praticada nas seções anteriores quando o `.dynsym` não cobre dados,
  só funções.

### 12.11 `wld_window` lida por completo — revela a máquina de estados real de abrir/fechar janela (2026-10-16, Fase 2, continuação)

`wld_window(WINPAC* win, GsOT* ot)` (`0x26679c`, 356 B, cobertura
total: 89 instruções pra 89 esperadas, sem pool de literais — função
inteira acessa dados só via campos de `win`, nenhum global PIC
direto). Resolvendo os `bl` por nome: **`fadeanb_calc`** (`0x25e160`,
já confirmada nas seções 12.4/12.5/12.10) e **`GsSortFastSprite`**
(`0x29c340`, já confirmada na seção 12.4), e uma função nova,
**`winopen_frmcalc(int, RECT16*, RECT16*)`** (`0x2666d4`).

```c
void wld_window(WINPAC* win, GsOT* ot) {
    Sprite s;
    s.field_0xc = (win->flags & 4) ? 0x1000000 : 0;        // bit de modo (semi-transparência?), não cravado
    s.u = win->+0x20;
    if (win->+0x14 != 0)
        s.u += (win->+0x14 - 1) << 4;                        // seleciona coluna de 16px num atlas de skins de janela
    s.v = win->+0x24;

    uint32_t color;
    if (win->flags & 0x400) color = win->+0x30;               // cor fixa
    else                     fadeanb_calc(&win->+0x30, &color); // cor pulsante (MESMO padrão de wld_anim/wldday_put)
    s.rgb = color;                                              // bytes de color -> s.r/g/b
    s.priority = win->+4;

    if (!(win->flags & 0x100)) {
        // *** estático: janela totalmente aberta ou fechada — copia o RECT16 cru ***
        s.rect = { win->+0x18, win->+0x1c, win->+0x28, win->+0x2a, win->+0x2c, win->+0x2e };
    } else {
        // *** animando: máquina de 8 passos (win->+0x10 = 0..7) ***
        RECT16 animRect;
        winopen_frmcalc(win->+0x10 / 2, (RECT16*)&win->+0x28, &animRect);  // interpola o frame atual

        s.rect.x0 = animRect.x0 + win->+0x18;    // soma offset animado + canto fixo da janela
        s.rect.y0 = animRect.y0 + win->+0x1c;
        s.rect.x1 = animRect.x1 + win->+0x28;
        s.rect.y1 = animRect.y1 + win->+0x2a;

        if (win->+0x10 > 7) {                      // 8º passo: animação terminou
            win->flags ^= 0x100;                      // desliga o bit "animando"
            win->+0x10 = 0;                            // zera o contador
        } else {
            win->+0x10 += 1;                           // avança um passo
        }
    }
    GsSortFastSprite(&s, ot, win->+8 /* ? */, win->+0x34 /* ? */);
}
```

**Achados:**
- **Terceira ocorrência confirmada** do padrão "cor fixa (bit `0x400`)
  OU pulsante via `fadeanb_calc`" — já visto em `wld_anim` (ANMPAC,
  seção 12.5) e `wldday_put` (seção 12.10), agora também em `WINPAC`.
  Confirma que é uma convenção genérica do motor (bit `0x400` = "não
  pulsar"), não algo específico de um struct.
- **Revela a máquina de estados real de abrir/fechar janela do FFT**:
  o bit `0x100` de `win->flags` indica "animando"; enquanto ativo, um
  contador de 8 passos (`win->+0x10`) avança a cada chamada e
  `winopen_frmcalc` interpola o retângulo atual entre o estado inicial
  e o `RECT16` final da janela (`win->+0x28..+0x2e`); ao completar o
  8º passo, o bit `0x100` é desligado automaticamente e o contador
  zera — ou seja, **a transição de abrir/fechar dura exatamente 8
  frames**, sem precisar de nenhum outro chamador pra "terminar" a
  animação.
- Enquanto `win->flags & 0x100` está desligado (janela totalmente
  aberta/fechada, estado estável), a função pula `winopen_frmcalc`
  inteiramente e copia o `RECT16` final direto — caminho mais barato,
  confirma que o cálculo de interpolação só roda durante a transição.
- Hipótese (não confirmada): `win->+0x14` parece indexar uma coluna de
  16px num atlas de texturas de "skins" de janela (múltiplos estilos
  de moldura compartilhando uma textura) — bateria com
  `wldwintex_point` (seção 11.2, "Janelas de UI"), que não foi lida.

**O que ficou sem confirmar (escalonado, não forçado):**
- Os 3º/4º argumentos passados a `GsSortFastSprite`
  (`win->+8`/`win->+0x34`) — na chamada de `wldinfo_put` (seção 12.4)
  o 3º argumento era um literal `0`; aqui são campos dinâmicos do
  `WINPAC`, então o papel completo da assinatura real de
  `GsSortFastSprite` (quantos parâmetros ela de fato usa) não está
  cravado.
- O layout completo de `WINPAC` — só os campos tocados por esta função
  foram nomeados por offset; os demais (e o papel exato de
  `win->+0x14`) ficam por confirmar lendo `wldwintex_point`/
  `wldwin_set`/`wldwin_trans` (ainda não lidas).

### 12.12 `wldtown_bright` lida por completo — revela o ciclo dia/noite real do mapa mundi (2026-10-16, Fase 2, continuação)

`wldtown_bright()` (`0x26bc60`, 320 B, 74 instruções de código real
cobertas por completo + pool de literais de GOT no restante dos
320 B) — a maior função "Desenho" ainda sem leitura depois de
`wld_window` (seção 12.11). Resolve um `bl` por nome:
**`pspWorldCheckFlg(PSP_WORLD_FLG)`** (`0x28b050`, nunca tocada
antes). O resto dos dados é acessado via GOT, sem nomes no
`.dynsym` (globais internos, não exportados — honesto não cravar
endereço absoluto, mas o comportamento sai claro da trilha de
registradores).

```c
void wldtown_bright() {
    if (g_flagsA & 0x400) return;              // bit "efeito desligado"
    if (pspWorldCheckFlg(2)) return;             // early-exit por estado do mundo (valor exato do enum não cravado)

    if (g_flagsA & 0x8000000) {
        // *** modo "reaplicar": usa o contador de ciclo já avançado noutro lugar neste frame ***
    } else if (g_cycleDir == 0) {
        g_cycleCounter = (g_cycleCounter + 1) & 0xff;         // avança o relógio dia/noite
        if (g_cycleCounter == 0x40) g_cycleDir = 1;             // bateu no topo -> inverte
    } else {
        g_cycleCounter = (g_cycleCounter - 1) & 0xff;
        if (g_cycleCounter == 0) g_cycleDir = 0;                 // bateu no fundo -> inverte
    }

APPLY:
    uint8_t rising  = ((g_cycleCounter + 0x30) << 1) & 0xff;   // rampa "clareando"
    uint8_t falling = ((0x70 - g_cycleCounter) << 1) & 0xff;     // rampa "escurecendo"

    int count = g_objArray.count;
    if (count <= 0) return;
    TownObj* obj = g_objArray.items;               // stride 0x34 (52 B) por elemento
    for (int i = 0; i < count; i++, obj++) {
        if (!(obj->+0x10 & 0x10)) {                   // bit "ignora iluminação ambiente"
            uint8_t tint = (obj->+0x24 != 0) ? rising : falling;  // cada objeto escolhe sua rampa
            obj->r = obj->g = obj->b = tint;             // tingimento cinza uniforme (brilho ambiente)
        }
    }
}
```

**Achados:**
- **Revela o ciclo dia/noite real do mapa mundi**: um contador
  oscilante de 0 a 64 (`g_cycleCounter`, onda triangular — sobe 64
  passos, desce 64 passos, inverte a direção nos dois extremos via
  `g_cycleDir`), convertido em duas rampas de brilho complementares
  (`rising`/`falling`) aplicadas como tingimento cinza (R=G=B) em
  cada objeto de um array de objetos do mapa mundi (stride 52 B).
  Confirma, com leitura real, o papel sugerido pelo nome
  (`wldtown_bright` = "brilho do mapa mundi").
- Cada objeto escolhe **qual das duas rampas usar** por um campo
  próprio (`+0x24`), e pode **optar por ignorar completamente** o
  ciclo (bit `0x10` em `+0x10`) — sugere que luzes/fontes de luz
  fixas (ex.: janelas iluminadas de uma vila à noite) não escurecem
  junto com o resto do cenário.
- O bit `0x8000000` separa dois modos de chamada: "avançar o relógio
  E aplicar" vs. "só aplicar" (reaproveitando um avanço já feito por
  outra chamada no mesmo frame) — sugere que `wldtown_bright` pode
  ser chamada mais de uma vez por frame (uma vez por "sub-tela"/
  camada do mapa mundi), mas o relógio global só deve avançar uma
  vez.
- Primeira função lida nesta investigação a chamar
  `pspWorldCheckFlg` — mais uma peça real da camada de compatibilidade
  `psp*` (já vista em `wldpad_read`/`CAUTOSAVE`, seção 12.2/19.1), mas
  o enum `PSP_WORLD_FLG` e o significado do valor `2` não foram
  cravados (sem debug info; escalonado).

**O que ficou sem confirmar (escalonado, não forçado):**
- O layout completo de `TownObj` (só os campos `+0x10`/`+0x24`/
  `+0x30..0x32` foram confirmados) e qual array exatamente é esse
  (tiles de fundo? sprites de prédio? os dois?) — não identificado
  por nome.
- O enum `PSP_WORLD_FLG` e o papel exato do valor `2`.

### 12.13 `wldtname_put` lida por completo — confirma o mesmo array de objetos de `wldtown_bright` por um ângulo diferente (2026-10-16, Fase 2, continuação)

`wldtname_put(GsOT* ot)` (`0x266df8`, 260 B, 60 instruções de código
real cobertas por completo + pool de literais de GOT no restante dos
260 B). Resolve os dois `bl` por nome: **`fadeanb_calc`** (`0x25e160`)
e **`wld_anim`** (`0x2660b8`), ambas já confirmadas — esta é a
**quarta ocorrência** do par `fadeanb_calc`/`wld_anim` nesta
investigação (depois de `wld_anim` consigo mesma na 12.5, `wldday_put`
na 12.10, e agora aqui).

```c
void wldtname_put(GsOT* ot) {
    if (g_flagsA & 0x2000) return;              // bit "banner de nome escondido"
    int count = g_activeTownCount;                 // global B
    if (count == 0) return;                          // nenhuma cidade "ativa" agora

    TownObj* obj = &g_townObjArray[count - 1];      // MESMO array/stride 0x34 de wldtown_bright (seção 12.12)!

    uint8_t fade = g_bannerFadeCounter;                // global D, lido só o byte baixo
    Color c = { fade, fade, fade };
    fadeanb_calc(&c, &c);                                // fade-in in-place (entrada = saída, mesmo buffer)

    ANMPAC banner = {
        .flags = 1, .animID = count + 0x36, .priority = 4,
        .x = obj->+0x28, .y = obj->+0x2c,                  // posição herdada do objeto da cidade ativa
        .tint = c,                                           // cor pré-calculada escrita direto no campo da seção 12.5
    };
    wld_anim(&banner, ot);

    if (g_bannerFadeCounter <= 0x7f)
        g_bannerFadeCounter += 8;                          // avança o fade-in; para de avançar ao passar de 127
}
```

**Achados:**
- **Confirma, por um ângulo totalmente diferente, o mesmo array de
  objetos de `wldtown_bright`** (seção 12.12): mesmo stride `0x34`
  (52 B), e os campos lidos aqui (`+0x28`/`+0x2c`, posição X/Y) não
  colidem com os já confirmados lá (`+0x10`/`+0x24`/`+0x30..0x32`) —
  **forte evidência de que é literalmente o mesmo array de "objetos
  de cidade" do mapa mundi**, usado tanto para brilho ambiente quanto
  para ancorar o banner de nome na posição da cidade ativa
  (`g_activeTownCount - 1` = a última cidade entrada).
- Confirma, pela quarta vez, o layout do `ANMPAC` (seção 12.5/12.10):
  `flags@+0`, `animID@+4`, `priority@+8`, `tint color@+0x20`
  (byte a byte, `r/g/b`), `x@+0x18`, `y@+0x1c` — e revela o campo de
  cor (`anim->field_0x20` citado só por offset na seção 12.5) sendo
  **pré-preenchido pelo próprio chamador** com o resultado de seu
  PRÓPRIO `fadeanb_calc`, antes de `wld_anim` rodar sua lógica interna
  de cor (que, com `flags=1` → bit `0x400` limpo, vai chamar
  `fadeanb_calc` de novo por dentro — **duas camadas de fade
  aparentemente empilhadas**, não investigado se é redundância real
  ou um efeito "duplo-pulsar" intencional).
- O campo `animID = count + 0x36` sugere uma sequência de quadros de
  "revelar o nome" indexada pelo contador de cidade ativa — mas
  **isso é uma hipótese**, não confirmado sem olhar a tabela de
  animação de verdade.
- `g_bannerFadeCounter` (global D) é lido como **byte** (valor cru
  0–255 usado direto como nível de cinza pro fade-in) e depois escrito
  como **word** incrementado por 8, travando ao passar de 127 — um
  fade-in de ~16 quadros que para de avançar sozinho ao terminar
  (mesmo padrão de "contador que se autolimita" já visto em
  `wld_window`, seção 12.11, só que linear em vez de 8 passos fixos).

**O que ficou sem confirmar (escalonado, não forçado):**
- Se as duas camadas de `fadeanb_calc` (uma aqui, outra dentro de
  `wld_anim`) são redundância de geração de código ou um efeito
  visual deliberado — não lido o corpo de `fadeanb_calc` pra saber se
  ela depende de tempo global ou do valor de entrada.
- O papel exato do offset `+0x36` somado ao contador pra formar o
  `animID`.

### 12.14 `wldmap_scrol` lida por completo — os mesmos limiares de `wldcenter_chk`, agora disparando o scroll real (2026-10-16, Fase 2, continuação)

`wldmap_scrol(_POINT* delta)` (`0x268f58`, 220 B, 52 instruções de
código real cobertas por completo + pool de literais de GOT no
restante dos 220 B) — já citada por nome na seção 12.2
(`wldwalk_rute` chama `wldmap_scrol(&delta)` "move a câmera/mapa
junto"), agora lida por dentro. Resolve os dois `bl` por nome:
**`bgscrol_chk_x(_POINT*, VECTOR*)`** e
**`bgscrol_chk_y(_POINT*, VECTOR*)`** (`0x24c44c`/`0x24c4c0`, nunca
tocadas antes).

```c
void wldmap_scrol(_POINT* delta) {
    CameraInfo* ci = g_cameraInfo;              // global
    VECTOR* camPos = g_camPos;                     // global, 2 words (x,y)
    int savedX = camPos->x, savedY = camPos->y;

    int testX = delta->x + ci->+0x30;
    if ((delta->x < 0 && testX < -0x18) ||
        (delta->x > 0 && testX >  0x20))
        bgscrol_chk_x(delta, camPos);

    int testY = delta->y + ci->+0x34;
    if ((delta->y < 0 && testY < -0x40) ||
        (delta->y > 0 && testY >  0x40))
        bgscrol_chk_y(delta, camPos);

    if (camPos->x != savedX || camPos->y != savedY)
        g_flagsG |= 2;                                // "o fundo rolou este frame"
}
```

**Achados:**
- **Os limiares são EXATAMENTE os mesmos de `wldcenter_chk`**
  (seção 12.9: `-0x18`/`+0x20` em X, `±0x40` em Y) — confirma que as
  duas funções testam a **mesma janela de centralização da câmera**:
  `wldcenter_chk` só RESPONDE se está fora dela (usado em outro lugar
  pra decidir "precisa recentrar"), enquanto `wldmap_scrol` **age** de
  verdade, chamando `bgscrol_chk_x`/`_y` para empurrar o fundo quando
  o delta de movimento ultrapassa a mesma margem.
- Delega o cálculo real do scroll para `bgscrol_chk_x`/`_y`
  (nomes reais, nunca lidos por dentro) — `wldmap_scrol` é só o
  "disparador com janela de margem", não quem move a câmera de fato.
- Confirma um padrão de flag "mudou de verdade?" já visto em outras
  seções: só marca `g_flagsG |= 2` se a posição da câmera
  (`g_camPos`) **de fato mudou** depois das chamadas — não assume que
  chamar `bgscrol_chk_x`/`_y` sempre produz movimento.

**O que ficou sem confirmar (escalonado, não forçado):**
- O corpo de `bgscrol_chk_x`/`bgscrol_chk_y` — a aritmética real do
  scroll (quanto desloca, se há limites de mapa) não foi lida.
- O papel exato de `ci->+0x30`/`ci->+0x34` (deslocamentos
  configuráveis por modo de câmera, não cravados byte a byte) e de
  `g_flagsG` bit `2` (consumido em algum outro ponto não
  identificado).

## 13. Motores gráfico (`CEGL2_*`) e de áudio (`CSOUND_IF`) — ponte confirmada com a API real (2026-10-16)

Continuação direta: os dois últimos motores sem nenhum código lido.
Levantamento primeiro — **167 funções/31 KB** em `CEGL2_*` e **134
funções/14 KB** em `CSOUND_*` — maior que o motor `wld_*` inteiro.
Dado o tamanho, apliquei a mesma estratégia: achar e ler por completo a
**função-ponte** (onde a emulação de API do PS1 encontra a API real do
Android) em vez de tentar ler as ~300 funções uma a uma.

### 13.1 Gráfico — `CEGL2_IF::DrawPacket(int, int)` (`0xaa190`, 1860 B) lida por completo

Resolvi os alvos de `bl` que caem dentro do `.plt` calculando o
endereço de GOT que cada stub referencia (soma de dois `add` + o
deslocamento do `ldr pc,[...]`) e cruzando com `.rel.plt` — a mesma
técnica de relocation usada desde a seção 9. Resultado: **confirmação
direta, por nome de símbolo importado, não por suspeita**, de que esta
função despeja chamadas **reais** da OpenGL ES 2.0:

```c
void CEGL2_IF::DrawPacket(int idx, int matrixOrParam, ...) {
    CEGL_PACKET* packet = this->packetArray[idx];     // +0xfc
    int count = packet->GetCount();
    if (count == 0) return;

    void* vboData = packet->GetVBOInfo();
    glActiveTexture(GL_ARRAY_BUFFER /* = 0x8892, imediato visto como 0x8800+0x92 */);
    glBindBuffer(GL_ARRAY_BUFFER, packet->GetVBOBuffer());
    glBufferData(GL_ARRAY_BUFFER, count*0x18, vboData, GL_DYNAMIC_DRAW /* 0x88e4 */);

    glVertexAttribPointer(0, 3, GL_FLOAT, ..., 0x18, offset0);   // posição (3 floats)
    glVertexAttribPointer(2, 4, GL_UNSIGNED_BYTE, ..., 0x18, offset12); // cor (4 bytes)
    glVertexAttribPointer(3, 2, GL_FLOAT, ..., 0x18, offset16);  // UV (2 floats)
    glEnableVertexAttribArray(0);

    for (/* sub-lotes agrupados por blend mode + textura, via CEGL_PACKET::GetBlendMode/GetTexture */) {
        shader->Begin(matrix, 0x3e8, count);           // CEGL2_SHADER::Begin
        glDisableVertexAttribArray(3);
        // ... despacha pra um de 4 blocos especiais se blendMode ∈ {5,6,7,8}
        glBindTexture(GL_TEXTURE_2D, packet->GetTexture(i));
        glDrawArrays(GL_TRIANGLES, offset, count);      // *** o desenho de verdade ***
    }
}
```

Stride de vértice confirmado: **24 bytes** (posição 3D + cor RGBA8 +
UV). Isto é **a ponte exata** entre a emulação da API gráfica do PS1
(seção 11.1 — `GsOT`, `AddPrims`, `SetPolyFT4`) e a GPU real do
Android: o jogo monta primitivas no estilo PS1, `CEGL2_*` as agrupa por
material (textura+blend) num VBO e emite `glDrawArrays` de verdade.
Classes relacionadas, não lidas, mas com papel claro pelo nome +
assinatura: `CEGL2_SPRITE` (desenho em lote de sprites 2D —
`DrawScrollBG`, `Draw8`, `AddPacketPartial`), `CEGL2_FBO`
(`RenderToFBO`/`RenderFromFBO` — render-to-texture), `CEGL2_SHADER`
(cache de shaders via `std::map<int,DATA_SHADER>`, confirmado pelos
símbolos de `_Rb_tree` do STLport), `CEGL2_TEX_HYBRID`
(`DecodeTexture`/`GL_Load` — upload de textura, provavelmente convertendo
do formato TIM decodificado na seção 9.2 para um formato aceito pela
GPU).

### 13.2 Áudio — confirmado como OpenSL ES real via import + tipo de callback

Não precisei ler uma função inteira para fechar isto com confiança alta
— dois achados diretos no próprio `.dynsym`/`.rel.plt` já bastam:

- **Import real `slCreateEngine`** (`.rel.plt`, offset `0x347f70`) — a
  função de entrada genuína da API OpenSL ES do Android NDK.
- **`CSOUND_IF_SL::CB_for_Stream(const SLAndroidSimpleBufferQueueItf*,
  void*)`** — o próprio nome do parâmetro mangled é o tipo de callback
  real do OpenSL ES Android (`SLAndroidSimpleBufferQueueItf`), usado
  para preencher o buffer de áudio sob demanda.

Arquitetura por nome (não lida): `CSOUND_IF` é a API de alto nível que
o jogo chama (`Play`, `Pause`, `SetVolume`, `FadeVolume`, `FrameMove`);
`CSOUND_IF_SL` é a implementação OpenSL ES por baixo
(`EngineInit`/`EngineUninit`, `Static_CreatePlayer`/
`Stream_CreatePlayer` — dois modos, som curto pré-carregado vs. stream
contínuo); `CSOUND_LOADER_OGG`/`CSOUND_LOADER_PCM` decodificam os
formatos de arquivo (`CSOUND_LOADER_OGG::Decode` confirma Ogg Vorbis
real, não um formato proprietário do PS1 — mudança de formato de áudio
em relação ao original, esperado numa engine mobile).

### 13.3 Estado final do item 8
Com isto, **os 8 itens da fila original de prioridade alta e os 3 de
prioridade média/baixa foram todos, pelo menos, abertos e têm algum
nível de evidência real de instrução/import** — nenhum ficou "não
tocado". Nível de profundidade por item (honesto, não uniforme):
CCRYPT e parser TIM = leitura completa das funções nomeadas; motor de
eventos/diálogo = os dois interpretadores + quase todos os opcodes
lidos; motor `wld_*` = ~20 das maiores funções lidas por completo +
resto por chamada/padrão; motores gráfico/áudio = **a função-ponte
central lida por completo, o resto (quase 300 funções) caracterizado só
por nome/assinatura/import**, não por leitura individual. Essa última
camada — ler as ~300 funções `CEGL2_*`/`CSOUND_*` uma a uma — é o que
ficaria para uma eventual continuação futura, mas não é razoável tratar
isso como pendência pequena.

### 13.4 `CEGL2_SPRITE::DrawScrollBG` lida por completo — primeiro item 🟡 (2026-10-16, loop de continuação, iteração 8)

A seção 13.1 já tinha a função-ponte geral do motor gráfico
(`CEGL2_IF::DrawPacket`) lida, mas nenhuma função **dentro** das
classes `CEGL2_SPRITE`/`FBO`/`SHADER`/`TEX_HYBRID` tinha sido lida
ainda — só catalogadas por nome. `CEGL2_SPRITE::DrawScrollBG(float,
float, _RECT_F32*, _RECT_F32*)` (`0xae584`, 1676 B, cobertura total:
419 instruções pra 419 instruções esperadas) é a maior do grupo, e foi
escolhida como a "função-central" deste item.

**Assinatura e papel confirmados:** `this` (sprite/textura de fundo),
`u`/`v` (deslocamento de scroll, parâmetros 1–2), `srcRect`/`dstRect`
(retângulos fonte/destino, parâmetros 3–4). A função monta **até 2
quads** (12 vértices = 2×6, formato `GL_TRIANGLES`) com coordenadas de
UV deslocadas pelo scroll — o segundo quad é o "tile duplicado" clássico
pra rolagem contínua sem costura.

**Achado de arquitetura — formato de vértice DIFERENTE do
`DrawPacket` (seção 13.1):** `DrawPacket` usa um VBO único
intercalado de stride 24 B (posição+cor+UV juntos). `DrawScrollBG` usa
**três arrays separados, cada um com `stride=0` (compacto, não
intercalado)**, sem VBO (ponteiros direto pra pilha local, não
`glBindBuffer`/`glBufferData`):

```c
glEnableVertexAttribArray(2);                                  // 0xae9fc área 2 = cor
void* posBuf   = &stack[0x94];   // vec3 float × 6, zerado por memset antes de preencher X/Y (Z fica 0 — fundo é 2D)
void* uvBuf    = &stack[0x34];   // vec2 float × 6, coordenadas de UV deslocadas pelo scroll
void* colorBuf = &stack[0x124];  // vec4 uint8 × 6 (dobrado: 2 blocos de 24 B) -- vem de this->b[0x58..0x67] (16 B)

if (GetMultiTextureHandle() == 0) {                            // 0xaea5c
    glBindTexture(GL_TEXTURE_2D /*0xde1*/, this->field_0x28);   // 0xaea74, textura única
    glVertexAttribPointer(0, 3, GL_FLOAT,         false, 0, posBuf);    // 0xaea98
    glVertexAttribPointer(3, 2, GL_FLOAT,         false, 0, uvBuf);     // 0xaeab4 (índice 3 = UV, igual ao DrawPacket)
    glVertexAttribPointer(2, 4, GL_UNSIGNED_BYTE, true,  0, colorBuf);  // 0xaeae0 (índice 2 = cor, normalizada)
    glDrawArrays(GL_TRIANGLES, 0, 12);                           // 0xaeaf0 -- 12 vértices = 2 quads
} else {
    // caminho de 2ª textura (parallax/multi-camada?): recalcula posBuf/uvBuf
    // (volta pro mesmo bloco de ponto flutuante em 0xae720) e repete a
    // MESMA sequência de 3 glVertexAttribPointer + glDrawArrays
    // (0xaebb4-0xaebf8), mas usando os registradores zerados (r4=0) nos
    // parâmetros de stride/normalized -- estruturalmente idêntico, só
    // reusa valor 0 de forma mais direta.
}
glDisableVertexAttribArray(2);                                  // 0xaeaf8
```

Confirma, pela mesma técnica de GOT/`.rel.plt` já usada desde a seção
9: `0x71710`=`glEnableVertexAttribArray`, `0x71728`=
`glDisableVertexAttribArray`, `0x71758`=`glBindTexture`,
`0x717b8`=`glVertexAttribPointer`, `0x717c4`=`glDrawArrays` (os
mesmos 2 últimos já vistos na seção 13.1, agora com mais dois GL
import novos resolvidos). Confirma também que `GL_TEXTURE_2D` (`0xde1`),
`GL_FLOAT` (`0x1406`), `GL_UNSIGNED_BYTE` (`0x1401`) e `GL_TRIANGLES`
(`4`) são os literais reais usados — não suposição.

**Achado secundário:** a função inteira faz aritmética de ponto
flutuante via **helpers de software do libgcc**
(`__aeabi_fadd`/`fsub`/`fmul`/`fdiv`, resolvidos por nome no
`.dynsym`), não instruções VFP de hardware — confirma que (ao menos
esta unidade de compilação) usa ABI de float em software (`softfp` ou
equivalente), não hardware FPU direto.

**O que ficou sem confirmar:** a fórmula exata do deslocamento de
scroll (a cadeia de ~30 chamadas de `fadd`/`fsub`/`fmul`/`fdiv`
combinando `u`/`v`, os campos `this->+0x3c/+0x40/+0x50/+0x54` e os
retângulos fonte/destino) não foi decomposta álgebra-por-álgebra —
ficou confirmado QUE ela computa UV/posição com wraparound (usa
divisão, consistente com módulo de scroll contínuo), mas não a fórmula
precisa. O papel exato de `GetMultiTextureHandle()`/do 2º quad
(parallax de 2 camadas? ou só "textura alternativa quando
multi-handle está em uso"?) também não foi cravado — mecanismo
estrutural confirmado, semântica de produto não.

### 13.5 `CEGL2_FBO::Create` lida por completo — segundo item 🟡 (2026-10-16, loop de continuação, iteração 9)

`CEGL2_FBO::Create(int,int,int,int,int)` (`0xaa980`, 472 B, cobertura
total: 118 instruções pra 118 esperadas) escolhida como função-central
da classe (em vez de `RenderToFBO`/`RenderFromFBO`, maiores mas que só
*usam* o FBO já criado). **É literalmente o "render-to-texture" de
verdade da OpenGL ES 2.0**, sequência de API real confirmada passo a
passo via GOT/`.rel.plt` (13 imports novos resolvidos nesta leitura:
`glGetIntegerv`, `glGenFramebuffers`, `glBindFramebuffer`,
`glGenTextures`, `glTexParameteri`, `glPixelStorei`, `glTexImage2D`,
`glFramebufferTexture2D`, `glGenRenderbuffers`, `glBindRenderbuffer`,
`glRenderbufferStorage`, `glFramebufferRenderbuffer`,
`glCheckFramebufferStatus` — junto com `glBindTexture` já conhecido).

```c
// CEGL2_FBO::Create(this, p1, width /*p2*/, height /*p3*/, wantLinearFilter /*p4*/, wantDepth /*p5*/)
int CEGL2_FBO::Create(CEGL2_FBO* this, int p1, int width, int height, int wantLinearFilter, int wantDepth) {
    this->field_0x18 = p1;        // papel não usado dentro desta função
    this->field_0x10 = width;
    this->field_0x14 = height;
    this->Delete();                // 0xaa8f8 — limpa um FBO/textura anterior, se houver

    glGetIntegerv(GL_FRAMEBUFFER_BINDING /*0x8ca6*/, &this->field_0x0);  // *** salva o FBO atualmente ligado ***
    glGenFramebuffers(1, &this->field_0x4);
    glBindFramebuffer(GL_FRAMEBUFFER /*0x8d40*/, this->field_0x4);
    glGenTextures(1, &this->field_0x8);
    glBindTexture(GL_TEXTURE_2D /*0xde1*/, this->field_0x8);

    if (!wantLinearFilter) {
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER /*0x2800*/, GL_NEAREST /*0x2600*/);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER /*0x2801*/, GL_NEAREST);
    } else {
        // só troca o MIN_FILTER pra LINEAR — MAG_FILTER fica no default da
        // GL (que já é GL_LINEAR), então na prática os dois ficam LINEAR
        // de qualquer forma; não é um bug, é confiar no default.
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR /*0x2601*/);
    }

    glPixelStorei(GL_UNPACK_ALIGNMENT /*0xcf5*/, 4);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA /*0x1908*/, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE /*0x1401*/, NULL);   // aloca a textura, sem subir pixels
    glBindTexture(GL_TEXTURE_2D, 0);
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 /*0x8ce0*/,
                            GL_TEXTURE_2D, this->field_0x8, 0);   // anexa a textura como alvo de cor

    if (wantDepth) {
        glGenRenderbuffers(1, &this->field_0xc);
        glBindRenderbuffer(GL_RENDERBUFFER /*0x8d41*/, this->field_0xc);
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT16 /*0x81a5*/, width, height);
        glBindRenderbuffer(GL_RENDERBUFFER, 0);
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT /*0x8d00*/,
                                   GL_RENDERBUFFER, this->field_0xc);
    }

    glBindFramebuffer(GL_FRAMEBUFFER, 0);
    glCheckFramebufferStatus(GL_FRAMEBUFFER);   // *** resultado nunca checado/usado ***
    glBindFramebuffer(GL_FRAMEBUFFER, this->field_0x0);  // restaura o FBO que estava ligado antes

    this->field_0x0 = -1;   // *** campo reaproveitado: era "FBO anterior", agora sentinela ***
    return 0;
}
```

**Achados:**
- `this->field_0x0` tem **papel duplo confirmado por leitura real**:
  durante a própria `Create`, guarda temporariamente o FBO que estava
  ligado antes (pra restaurar no fim); depois de restaurado, é
  sobrescrito com `-1` como sentinela — quase certamente "nenhuma
  sessão de render-to-texture em andamento", consumido por
  `Begin`/`End` (`0xaad68`/`0xaadb8`, não lidas, mas agora com uma
  hipótese concreta e testável pra uma leitura futura).
- `glCheckFramebufferStatus` é chamado mas **seu retorno nunca é
  comparado nem armazenado** — a verificação de erro, se existe, não
  está nesta função (possivelmente só em `ErrorGL`, `0xab4b0`, não
  lida).
- Confirma os dois caminhos de filtro de textura (`GL_NEAREST` vs
  `GL_LINEAR`) e o anexo opcional de depth-buffer via renderbuffer —
  ambos controlados por parâmetros simples (`wantLinearFilter`/
  `wantDepth`), não por estado implícito.

### 13.6 `CEGL2_SHADER::Load` lida por completo — terceiro item 🟡, e um achado preocupante (2026-10-16, loop de continuação, iteração 10)

Das duas sobrecargas de `Load` (`0xab674`, 384 B, por string; e
`0xac850`, **596 B**, por buffer — a que o plano apontava), escolhi a
de 596 B porque é ela que de fato interage com o cache `std::map`
citado no plano (confirmado: usa a árvore rubro-negra manual do
STLport, `_Rb_tree::insert_unique`, `0xac540`, símbolo já catalogado
por nome). Cobertura total: 149 instruções pra 149 esperadas.

```c
// CEGL2_SHADER::Load(this, int key, void* vertSrc, uint vertLen, void* fragSrc, uint fragLen)
int CEGL2_SHADER::Load(CEGL2_SHADER* this, int key, void* vertSrc, uint vertLen,
                        void* fragSrc, uint fragLen) {
    // busca 'key' na árvore do cache (this->field_0x10); se já existe uma
    // entrada com a MESMA key, chama uma função virtual (vtable slot #6,
    // this->vtbl[0x18]) antes de recriar — quase certamente libera os
    // recursos GL do shader anterior daquela chave.
    ...

    GLuint vs = glCreateShader(GL_VERTEX_SHADER /*0x8b31*/);
    GLuint fs = glCreateShader(GL_FRAGMENT_SHADER /*0x8b30*/);
    if (CompileShader(&vs, vertSrc, vertLen) != 0) goto FAIL;   // 0xabb28, já catalogada
    if (CompileShader(&fs, fragSrc, fragLen) != 0) goto FAIL;

    GLuint prog = glCreateProgram();
    glAttachShader(prog, vs);
    glAttachShader(prog, fs);
    for (i = 0; i < 7; i++)                                       // 7 atributos fixos
        glBindAttribLocation(prog, i, attribNameTable[i]);
    glLinkProgram(prog);

    int linkStatus;
    glGetProgramiv(prog, GL_LINK_STATUS /*0x8b82*/, &linkStatus);
    if (linkStatus == 0) { for(;;); }   // *** TRAP — ver achado abaixo ***

    for (j = 0; j < 27; j++)                                       // 0x6c/4 = 27 uniforms!
        cacheEntry.uniformLoc[j] = glGetUniformLocation(prog, uniformNameTable[j]);

    glDeleteShader(vs);
    glDeleteShader(fs);

    // monta um DATA_SHADER{key, program, 27 uniformLoc...} (0x74 B) e
    // insere/atualiza na árvore do cache (memcpy final de 0x74 B pro nó)
    return 0;

FAIL:
    glDeleteShader(vs);
    glDeleteShader(fs);
    return 1;
}
```

Confirmado por nome real via GOT/`.rel.plt` (8 imports GL novos):
`glCreateShader`, `glCreateProgram`, `glAttachShader`,
`glBindAttribLocation`, `glLinkProgram`, `glGetProgramiv`,
`glGetUniformLocation`, `glDeleteShader`.

**Achado principal, e um pouco preocupante:** falha de **compilação**
de shader (`CompileShader` retornando != 0) é tratada graciosamente —
limpa os dois shaders e retorna `1`. Mas falha de **link**
(`glGetProgramiv(GL_LINK_STATUS)` retornando `0`) **não tem tratamento
algum** — o código salta pra `b #0xaca7c`, um laço infinito de 1
instrução que se referencia a si mesmo (`feffffea`, confirmado byte a
byte, não é erro de desmontagem). Ou seja: nesta build, **um shader
que compila mas falha ao linkar trava o app pra sempre**, em vez de
devolver um código de erro como no caso de compilação. Pode ser um
`assert`/trap intencional de debug que nunca deveria disparar em
produção (os shaders são todos embutidos/fixos, não vêm de conteúdo
externo), mas é uma rota de código real, não hipotética.

**Outros achados:** confirma que o cache usa `27` slots de uniform por
shader (`0x6c` bytes / 4) — um shader "genérico" com bastante
parametrização (matrizes, cores, texturas, etc.), consistente com ser
o mesmo shader usado por `CEGL2_IF::DrawPacket` (seção 13.1,
`shader->Begin(matrix,...)`). Os **7 atributos fixos** ligados via
`glBindAttribLocation` provavelmente incluem os índices `0`/`2`/`3`
já confirmados (posição/cor/UV, seções 13.1 e 13.4) mais 4 outros não
identificados (os nomes de string exatos ficam em `.rodata`, não
lidos nesta passada).

### 13.7 `CEGL2_TEX_HYBRID::DecodeTexture` lida por completo — quarto item 🟡, fecha o elo TIM→GL (2026-10-16, loop de continuação, iteração 11)

`CEGL2_TEX_HYBRID::DecodeTexture(uint*, uchar*, int, int, uint*, int,
int, int, int)` (`0xaf644`, 468 B, cobertura total: 117 instruções —
função folha, nenhum `bl`). Escolhida sobre `GL_IsUpdate`/`GL_Load`
porque é exatamente a função que o plano apontava como suspeita:
**"provável ponto de conversão do formato TIM decodificado pra
textura GL"** — confirmado.

```c
// DecodeTexture(uint32* dst, uchar* src, int widthPx, int bpp,
//               uint32* clut, int p6, int p7, int p8, int clipMode)
void DecodeTexture(uint32_t* dst, uint8_t* src, int widthPx, int bpp,
                    uint32_t* clut, int p6, int p7, int p8, int clipMode) {
    if (bpp != 4) { for(;;); }   // *** TRAP de novo — só aceita 4bpp ***

    // (opcionalmente recorta a região se p7+p8 > 0x200 = 512 — o limite
    // clássico de textura/VRAM do PS1 — zerando as linhas fora do
    // recorte; aritmética de recorte não decomposta 100%, mas o gatilho
    // e o efeito —zerar em vez de desenhar— estão confirmados)

    for (cada linha) {
        for (cada byte de origem) {
            uint8_t packed = *src++;          // 1 byte = 2 índices de 4 bits (4bpp)
            *dst++ = clut[packed & 0xf];        // nibble baixo  -> 1º pixel
            *dst++ = clut[packed >> 4];          // nibble alto   -> 2º pixel
        }
    }
}
```

**Fecha de vez a ponte arquitetural** que as seções 9.2/9.8 (parser
TIM) e 13.1/13.5 (upload de textura GL, que só aceita `GL_RGBA`+
`GL_UNSIGNED_BYTE`, ou seja, 32 bits/pixel) deixavam implícita: o TIM
nativo guarda pixels 4bpp indexados (2 por byte) + uma paleta
separada, e a GPU real não entende esse formato — **é exatamente esta
função que expande cada par de índices de 4 bits em dois pixels
RGBA8888 completos via a tabela de paleta (CLUT)**, byte a byte, antes
do `glTexImage2D`.

**Achado secundário — padrão recorrente confirmado:** esta é a
**segunda** função nesta investigação (depois de `CEGL2_SHADER::Load`,
seção 13.6) com um laço infinito de 1 instrução (`b $`) como resposta
a uma condição "impossível" (aqui, `bpp != 4`) — reforça que isso é
uma convenção real do código desta engine (provavelmente um trap de
debug que o build de produção não limpou), não um caso isolado.

**O que ficou sem confirmar:** a aritmética exata de recorte/clipping
(`p6`/`p7`/`p8`/`clipMode`, o "modo complexo" de `0xaf674`–`0xaf754`) —
confirmado QUE existe e QUANDO dispara (soma de duas dimensões > 512),
mas não a fórmula linha-a-linha completa.

### 13.8 `CEGL2_SPRITE::AddPacketPartial` lida por completo — primeiro item 🟠 da Fase 2 (2026-10-16, Fase 2, iteração 6)

`CEGL2_SPRITE::AddPacketPartial(float×6, CEGL_PACKET*)` (`0xad324`,
1244 B, cobertura total: 311 instruções pra 311 esperadas) — a maior
das 3 funções da família ainda não lidas (seção 13.4 só tinha lido
`DrawScrollBG`). Escolhida como função-central porque é a que
**monta** o lote que `DrawPartial`/`Draw8` presumivelmente desenham
depois.

**Achado estrutural confirmado: é uma função 100% linear, sem nenhum
desvio condicional** (as 311 instruções formam um único caminho,
confirmado byte a byte) — puro cálculo de ponto flutuante (via
helpers `libgcc` já conhecidos) seguido de gravação manual byte a
byte (`strb` + `lsr #8/0x10/0x18`) do padrão de bits de cada `float`
calculado, mais alguns `memcpy` (`0x714b8`) de 4 B copiando campos
fixos de `this` direto pro buffer.

```c
void CEGL2_SPRITE::AddPacketPartial(float p1, float p2, float p3,
                                      float p4, float p5, float p6,
                                      CEGL_PACKET* packet) {
    void* v = packet->GetVBOBufferCurrent();     // 0xb1bc8 — mesmo ponteiro de escrita do Add3D/AddTile

    // calcula posição/UV combinando p1..p6 com this->+0x4c/+0x50/+0x54/
    // +0x58/+0x5c/+0x60/+0x64 (campos do sprite — provavelmente o
    // retângulo fonte dentro da folha de textura, dado o nome
    // "Partial"), grava em formato intercalado de 24 B/vértice
    // (mesmo layout confirmado em `DrawPacket`, seção 13.1):
    //   v[0] = {pos, cor=0, uv}
    //   v[1] = {pos, cor=0, uv}
    //   v[2] = {pos, cor=0, uv}
    memcpy(v + 0x48, v + 0x18, 0x30);    // *** copia v[1] e v[2] pra v[3]/v[4] ***
    // v[5] = {pos, cor=0, uv}

    packet->SetTypeCurrent(this->b[0x48]);                  // 0xb1b0c
    packet->SetBlendModeCurrent(packet->GetDefaultBlendMode()); // 0xb1acc + 0xb1b34
    packet->SetTextureCurrent(this->w[0x28]);                 // 0xb1b5c
    packet->SetExtraCurrent((int)p1, -3);                      // 0xb1ba0
    packet->Add(6);                                             // 0xb1a80 — tail-call, 6 vértices
}
```

**Confirma, com o `memcpy` interno explícito, o layout exato do quad
de 6 vértices via 2 triângulos degenerados compartilhando uma
diagonal** (`v0,v1,v2,v1,v2,v5` — os vértices `v1`/`v2` são
literalmente duplicados pra `v3`/`v4` por um `memcpy` de 48 B dentro
da própria função, não por dois cálculos separados) — o mesmo truque
clássico de "desenhar um quad sem index buffer" que `DrawPacket`
(seção 13.1) e `DrawScrollBG` (seção 13.4) já usavam, agora confirmado
na origem (onde o lote é **montado**, não só desenhado).

**O que ficou sem confirmar:** a fórmula geométrica exata (o que cada
campo `this->+0x4c`.. representa em termos de retângulo fonte/destino
real) — confirmado QUE a função monta um quad com UV parcial de uma
folha de sprite maior, mas não a matemática linha a linha completa
(mesma ressalva já aplicada a `DrawScrollBG`, seção 13.4).

### 13.9 `CEGL2_FBO::RenderToFBO` lida por completo — segundo item 🟠 da Fase 2 (2026-10-16, Fase 2, iteração 7)

`CEGL2_FBO::RenderToFBO(float×6, short×2, int×2)` (`0xaae00`, 868 B,
cobertura total: 217 instruções pra 217 esperadas). Usa a textura que
`Create` (seção 13.5) já tinha criado — fecha o ciclo "criar → usar"
desse lado do par.

```c
// RenderToFBO(this, p1..p6 /*float*/, colorR, colorG /*ambos 0-255*/,
//             filterMode /*p9, 0..2*/, flipUV /*p10, bool*/)
void CEGL2_FBO::RenderToFBO(CEGL2_FBO* this, float p1, float p2, float p3,
                              float p4, float p5, float p6,
                              int colorR, int colorG, int filterMode, int flipUV) {
    // monta um quad (posição a partir de p1-p4, UV escalado por
    // this->+0x10/+0x14 — provável "tamanho lógico vs tamanho real da
    // textura", mesma ideia de UV com padding de seções anteriores) e
    // um array de cor RGBA de 4 vértices a partir de colorR/colorG
    bool opaque = (colorR == 0xff && colorG == 0xff);
    if (!opaque) glDisable(GL_BLEND);     // *** pula o overhead de blend quando totalmente opaco ***

    glEnableVertexAttribArray(0);
    glEnableVertexAttribArray(2);
    glEnableVertexAttribArray(3);
    glBindTexture(GL_TEXTURE_2D, this->field_0x8);     // *** a textura criada em `Create`, seção 13.5 ***

    switch (filterMode) {
        case 0: case 1:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
            break;
        case 2:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
            glGenerateMipmap(GL_TEXTURE_2D);              // *** mipmap real, não só filtro ***
            break;
    }

    glVertexAttribPointer(0, 3, GL_FLOAT, false, 0, posBuf);
    glVertexAttribPointer(2, 4, GL_UNSIGNED_BYTE, true, 0, colorBuf);
    glVertexAttribPointer(3, 2, GL_FLOAT, false, 0, flipUV ? uvBufFlipped : uvBufNormal);
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);    // *** TRIANGLE_STRIP de 4 vértices — formato DIFERENTE! ***

    glBindTexture(GL_TEXTURE_2D, 0);
    if (!opaque) glEnable(GL_BLEND);         // reabilita o blend que desligou no início
}
```

**Achados:**
- **Formato de desenho diferente do resto do motor**: `DrawPacket`
  (seção 13.1), `DrawScrollBG` (13.4) e `AddPacketPartial` (13.8)
  sempre usam `GL_TRIANGLES` com 2 triângulos degenerados por quad
  (6 vértices). `RenderToFBO` usa **`GL_TRIANGLE_STRIP` com só 4
  vértices** (`mode=5` confirmado contra a enumeração real da GL ES:
  `TRIANGLES=4`, `TRIANGLE_STRIP=5`, `TRIANGLE_FAN=6`) — um jeito mais
  direto de desenhar um quad único (sem precisar duplicar vértices
  via diagonal compartilhada), condizente com ser uma função de
  "blit" simples (um quad só, sem lote).
- Confirma `glGenerateMipmap` real sendo chamado condicionalmente
  (`filterMode==2`) — a textura de uma FBO pode ser amostrada com
  mipmap, não só filtro bilinear simples.
- Achado de performance: pula `glDisable`/`glEnable(GL_BLEND)`
  completamente quando a cor é opaca (`0xff,0xff`) — otimização
  explícita pra não pagar o custo de blend quando não precisa.
- Dois buffers de UV pré-computados (`flipUV` escolhe entre eles) —
  provável correção de orientação vertical entre o espaço de textura
  FBO (OpenGL, origem embaixo) e o espaço de UV normal do resto do
  motor (origem no topo, convenção PS1).

**O que ficou sem confirmar:** a fórmula exata de escala de UV via
`this->+0x10`/`+0x14` (dimensões lógicas vs reais da textura — não
cruzado com `Create`, seção 13.5, que não grava esses campos
explicitamente nessa passagem). `RenderFromFBO` (par desta função,
`0xab164`, 732 B) continua não lida.

### 13.10 `CEGL2_SHADER::Begin`/`SetTexture` lidas por completo — terceiro item 🟠 da Fase 2, e uma correção de assinatura (2026-10-16, Fase 2, iteração 8)

`CEGL2_SHADER::Begin(int,MATRIX4*)` (`0xab7f4`, 120 B) e
`SetTexture(int)` (`0xab8e8`, 60 B) — chamadas de verdade por
`CEGL2_IF::DrawPacket` (seção 13.1), lidas por completo (ambas
funções folha quanto a desmontagem — cobertura total nos dois casos).

```c
void CEGL2_SHADER::Begin(CEGL2_SHADER* this, int key, MATRIX4* matrix) {
    Node* root = this->field_0x10;         // raiz do std::map (mesma árvore da seção 13.6)
    if (!root) return;

    Node* found = tree_lower_bound(root, key);   // mesmo algoritmo de busca do std::map
    if (found == end || found->key > key) return;  // não achou exato

    if (found->field_0x14 == 2)                        // campo de status do nó
        glUseProgram(found->field_0x18);                  // *** ATIVA o shader de verdade ***

    this->field_0x4 = key;
    this->field_0x8 = &found->field_0x14;    // cacheia o nó pra `SetTexture`/outros getters usarem
}

void CEGL2_SHADER::SetTexture(CEGL2_SHADER* this, int slot) {
    DATA_SHADER* node = this->field_0x8;      // nó cacheado por `Begin`
    if (!node) return;

    int idx = (slot == 0) ? 1 : (slot == 1) ? 2 : -1;
    if (idx < 0) return;                          // só aceita slot 0 ou 1 — *** 2 texturas por shader ***

    int loc = node->uniformLoc[idx];              // array de 27 uniforms (seção 13.6)
    if (loc < 0) return;
    glUniform1i(loc, slot);                         // liga a sampler uniform à texture unit `slot`
}
```

**Achado — correção de assinatura**: `Begin` **nunca usa o parâmetro
`matrix`** dentro do próprio corpo — só busca o shader no cache e
chama `glUseProgram`. Isso corrige a suposição de pseudocódigo das
seções 13.1/14 (`shader->Begin(matrix, 1000, count)`, com 3
argumentos) — a assinatura real tem só 2 parâmetros explícitos
(`int key`, `MATRIX4* matrix`), e o `matrix` não é consumido aqui
(deve ser aplicado em outro método, como `SetMatrix4`, catalogado mas
não lido, chamado separadamente pelo chamador).

**Achado de arquitetura**: `SetTexture` confirma que shaders deste
motor suportam **até 2 texturas simultâneas** (`slot` 0 ou 1, mapeado
pra 2 dos 27 uniforms via `glUniform1i`) — bate exatamente com o
`GetMultiTextureHandle()` de `CEGL2_SPRITE::DrawScrollBG` (seção 13.4,
gatilho do "2º quad"/2ª textura) — confirma que o suporte a
multi-textura é uma capacidade real do shader genérico, não um
mecanismo isolado do `DrawScrollBG`.

### 13.11 `CEGL2_TEX_HYBRID::GL_IsUpdate` lida por completo — quarto item 🟠 da Fase 2, e uma 4ª ocorrência do padrão "laço infinito" (2026-10-16, Fase 2, iteração 9)

`CEGL2_TEX_HYBRID::GL_IsUpdate(uint, int*, _RECT_S32*)` (`0xaf120`,
684 B, cobertura total: 171 instruções pra 171 esperadas). É, na
prática, **o cache de slots de textura** desse sistema — fecha a
família iniciada por `DecodeTexture` (seção 13.7): decide ONDE
(em qual dos 64 slots) uma textura decodificada deve ir, e se o slot
escolhido já tem o conteúdo certo ou precisa de upload de novo.

```c
// GL_IsUpdate(this, uint fileID, int* outSlot, _RECT_S32* rect)
// retorna true = "precisa atualizar/subir de novo"; false = "já está certo"
bool CEGL2_TEX_HYBRID::GL_IsUpdate(CEGL2_TEX_HYBRID* this, uint fileID,
                                     int* outSlot, _RECT_S32* rect) {
    Slot* slots = (Slot*)this;    // array fixo de 64 slots, stride 0x88 B

    if (!rect) {
        // modo simples: só confere o ID do arquivo
        for (i = 0; i < 64; i++)
            if (slots[i].fileID == fileID) { *outSlot = i; return false; }
        goto FIND_REUSABLE_SLOT;     // ver abaixo — mesmos 3 níveis, sem checar x/y/tamanho
    }

    // modo com rect: só considera "já certo" se arquivo E os 4 campos
    // do retângulo (x/y/w/h, campos +0x604/+0x608/+0x60c/+0x610) baterem
    for (i = 0; i < 64; i++)
        if (slots[i].fileID == fileID && slots[i].rect == *rect) { *outSlot = i; return false; }

FIND_REUSABLE_SLOT:
    // *** 3 níveis de fallback, cada um menos exigente que o anterior ***
    for (i = 0; i < 64; i++)                                           // nível 1
        if (slots[i].field_0x6c == -1 && slots[i].GetTextureHandle()      // 0xacebc
            && slots[i].field_0x78 == rect->x && slots[i].field_0x7c == rect->y
            && (int)slots[i].GetTextureSize() == {rect->w, rect->h}) {    // 0xacec4 + f2i (0x2cb92c)
            *outSlot = i; return true;    // posição/tamanho compatíveis -> reusa, mas precisa atualizar
        }
    for (i = 0; i < 64; i++)                                           // nível 2
        if (slots[i].field_0x6c == -1 && slots[i].GetTextureHandle()) {
            *outSlot = i; return true;      // qualquer slot "livre" com handle válido
        }
    for (i = 0; i < 64; i++)                                           // nível 3
        if (slots[i].GetTextureHandle()) {
            *outSlot = i; return true;        // qualquer slot com handle válido, NEM checa "livre"
        }
    for (;;) {}    // *** nenhum slot disponível -- trava pra sempre ***
}
```

**Achados:**
- Confirma o mecanismo real de **cache/alocador de slots de
  textura**: 64 slots fixos, 3 níveis de fallback progressivamente
  menos exigentes (livre+tamanho-compatível → livre+qualquer-tamanho
  → nem-livre-mas-com-handle-válido) antes de desistir.
- **4ª ocorrência do padrão "condição impossível = laço infinito de
  1 instrução"** nesta investigação (depois de `CEGL2_SHADER::Load`
  seção 13.6, `CEGL2_TEX_HYBRID::DecodeTexture` seção 13.7, e agora
  aqui) — se os 64 slots estiverem todos sem handle de textura válido
  (cache nunca inicializado), a função trava pra sempre em vez de
  devolver um erro. Confirma de vez que isso é uma convenção real do
  código desta engine, não coincidência.
- O caminho "sem `rect`" (`rect==NULL`) cai nos MESMOS 3 níveis de
  fallback dos campos `+0x78`/`+0x7c` ignorados — ou seja, a lógica de
  "achar um slot pra reusar" é compartilhada entre os dois modos,
  só o critério de "já está certo" (nível 0, antes do fallback) muda.

**O que ficou sem confirmar:** `GL_Load` (`0xaf818`, 392 B, par desta
função — presumivelmente quem realmente faz o upload pro slot
escolhido aqui) não lida nesta passada.

## 14. `DrawTile4` e `Add3D` lidas por completo — e um bônus: resolvidos vários mistérios de PLT antigos (2026-10-16)

Continuação pedida explicitamente: as duas maiores funções do `CEGL2_IF`
encontradas na seção 13.

### 14.1 Achado colateral importante: a técnica de resolver GOT de stub de `.plt` fecha 5 mistérios de sessões anteriores

Para resolver as chamadas de `bl` que caem dentro do `.plt` (stubs de 12
bytes: `add ip,pc,#alto; add ip,ip,#baixo; ldr pc,[ip,#offset]!`),
bastou somar os dois `add` ao PC e ler o nome em `.rel.plt` no offset
resultante. Rodando isso para os stubs usados aqui, **fechei de vez 5
endereços que ficaram sem nome em seções bem anteriores desta mesma
investigação** (não só na IA de batalha — em todo o binário):

| Endereço de stub | Resolvido para | Onde apareceu antes, sem nome |
|---|---|---|
| `0x714b8` | **`memcpy`** | `TIM_LoadFile` (seção 9.2), `wldscr_init` (seção 11), e repetidamente no inventário de chamadas da seção 12 |
| `0x714c4` | **`memset`** | `DrawTile4` (nesta seção) |
| `0x715cc` | **`__stack_chk_fail`** | `sub_275e3c` e o retorno comum de `FundamentalRoutine` (seções 14.3/17.5 do `AI_DIFFICULTY_RESEARCH.md`) — confirma a hipótese de "stack canary" que já tinha sido levantada lá, agora com nome exato |
| `0x717d0` | **`sinf`** | (novo) |
| `0x717dc` | **`cosf`** | (novo) |

Esses dois últimos (`sinf`/`cosf`) confirmam que a plataforma usa
**funções de `libm` de verdade** para trigonometria, não uma tabela PS1
(`rsin`/`rcos`) emulada — mistura de fidelidade "API PS1" (seção 11.1)
com atalhos modernos onde não importa (trigonometria comum).

### 14.2 `CEGL2_IF::DrawTile4(float,float,float,float,float,Pj,float)` (`0xa98c8`, 2248 B) — lida por completo

A maior parte do corpo (~350 das ~560 instruções) é **aritmética de
ponto flutuante via software** (`__addsf3`/`__subsf3`/`__mulsf3`/
`__divsf3`) — confirma de vez que este alvo ARMv5 **não tem FPU de
hardware** (bate com a observação já feita na seção 8 sobre a ABI
"genérica ARMv5" ser obsoleta). O cálculo é geometria 2D clássica de
quad rotacionado:

```c
void CEGL2_IF::DrawTile4(float cx, float cy, float halfW, float halfH,
                          float angle, uint32_t color, float z) {
    float s = sinf(angle), c = cosf(angle);
    // 4 cantos = centro ± (halfW*c ∓ halfH*s, halfW*s ± halfH*c), tudo em soft-float
    Vertex corners[4];
    for (i = 0; i < 4; i++) {
        corners[i].pos = computedCorner[i];      // ponto flutuante
        corners[i].color = color;                 // RGBA8 empacotado, 4 bytes
    }
    shader->Begin(matrix, 1000, 0);
    glUniformMatrix4fv(1, false, matrix+0x98);
    glEnableVertexAttribArray(0);  glEnableVertexAttribArray(2);
    glBindTexture(GL_TEXTURE_2D, texId);
    glVertexAttribPointer(0, 3, GL_FLOAT, false, 0, &corners[0].pos);
    glVertexAttribPointer(2, 4, GL_UNSIGNED_BYTE, true, 0, &corners[0].color);
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);          // desenha o tile imediatamente
}
```

Esta é a rotina de **desenho imediato de 1 tile/sprite rotacionado**
(em contraste com `DrawPacket`, seção 13.1, que desenha um **lote**
pré-montado em VBO) — mesma ponte PS1→GLES2 confirmada de novo, desta
vez para o caminho "um sprite por vez".

### 14.3 `CEGL2_IF::Add3D(int, _EGL_PACKET_SPR*, short)` (`0xa872c`, 1944 B) — lida por completo

Também majoritariamente repetitivo, mas por um motivo diferente:
**reconstrução de campos de 4 bytes byte-a-byte** (lê 4 bytes
individuais do struct de origem `_EGL_PACKET_SPR*` e remonta via
`orr`/`lsl`, depois grava de volta byte a byte no destino) — um padrão
clássico de **evitar acesso desalinhado**, não de troca de endianness
(ambos ARM e a origem são little-endian; a origem simplesmente não está
garantidamente alinhada a 4 bytes). Mapeia campos da origem (`+4,+8,
+0xc,+0x4c,+0x50,+0x10,+0x14,+0x18,+0x54,+0x58...`) para um registro de
vértice no buffer do `CEGL_PACKET` atual (via `GetVBOBufferCurrent`),
com um `memcpy(dest+0xc, src+0x7c, 4)` no meio para um campo extra.
Também chama `SetDefaultBlendMode`/`SetTypeCurrent`/
`SetBlendModeCurrent`/`SetTextureCurrent`/`SetExtraCurrent` (métodos do
`CEGL_PACKET` já catalogados na seção 13.1).

**Papel confirmado:** `Add3D` é o **caminho de lote** (ao contrário do
desenho imediato de `DrawTile4`) — converte um primitivo de sprite
posicionado em 3D (`_EGL_PACKET_SPR`, provável "billboard"/partícula)
do formato de origem do jogo para o formato de vértice do VBO, e o
anexa ao `CEGL_PACKET` atual para ser desenhado depois, em lote, por
`DrawPacket`. Isso fecha o ciclo completo do pipeline gráfico desta
engine: `Add3D`/`AddTile` (não lida, mas mesmo papel por nome) acumulam
primitivos no `CEGL_PACKET` → `DrawPacket` (seção 13.1) os desenha em
lote via GLES2 real → `DrawTile4`/`DrawTile` (esta seção) é o atalho
para desenhar 1 peça imediatamente, sem passar pelo lote.

## 15. `AddTile` e `DrawTile` lidas por completo — fecham a família de 5 (2026-10-16)

Continuação pedida explicitamente. Com estas duas, a família inteira de
desenho de sprite do `CEGL2_IF` identificada nas seções 13–14 está
fechada: `Add3D`/`AddTile` (acumula em lote) e `DrawPacket`/`DrawTile4`/
`DrawTile` (desenha).

### 15.1 `CEGL2_IF::AddTile(int x, int y, int z, int id, short, short, short, short, short)` (`0xa8ec4`, 368 B) — é um wrapper fino sobre `Add3D`

```c
void CEGL2_IF::AddTile(int x, int y, int z, int id,
                        short u0, short v0, short u1, short v1, short flags) {
    EGL_PACKET_SPR tmp;
    memset(&tmp, 0, sizeof(tmp));         // 0x714c4 = memset, 184 B
    tmp.pos[0..3] = { (float)x, (float)y, (float)z };   // __floatsisf nos 3 eixos
    tmp.uv[0..3]  = { u0, v0, u1, v1 };     // replicado nos 4 cantos (bytes 0x90-0xa7)
    tmp.flags     = flags;
    Add3D(this, &tmp, 1);                   // *** delega pro acumulador de lote ***
}
```

**Confirma exatamente a hipótese da seção 14.3:** `AddTile` monta, em
pilha, um registro `_EGL_PACKET_SPR` de 1 sprite a partir de parâmetros
escalares simples e entrega pro `Add3D` fazer o trabalho real de
conversão para o formato de vértice do VBO. O `bne`/`bl
__stack_chk_fail` no final não é nada específico de sprite — é
simplesmente o canário de pilha do compilador (`-fstack-protector`)
protegendo o buffer local de 184 bytes, mesmo padrão confirmado na
seção 14.1.

### 15.2 `CEGL2_IF::DrawTile(float x, float y, float w, float h, uint32_t color)` (`0xa977c`, 332 B) — o irmão sem rotação e sem textura de `DrawTile4`

```c
void CEGL2_IF::DrawTile(float x, float y, float w, float h, uint32_t color) {
    float x1 = x + w, y1 = y + h;            // __addsf3 — SEM sinf/cosf, é um retângulo alinhado aos eixos
    Vertex v[4] = { {x,y}, {x1,y}, {x,y1}, {x1,y1} };  // 4 cantos, cor RGBA8 replicada em todos
    shader->Begin(matrix+0x1c, 1000, 0);
    shader->SetMatrix4(0, matrix+0x98);       // *** usa o wrapper de alto nível, não glUniformMatrix4fv direto ***
    glEnableVertexAttribArray(0); glEnableVertexAttribArray(2);
    glVertexAttribPointer(0, 3, GL_FLOAT, false, 0, &v[0].pos);
    glVertexAttribPointer(2, 4, GL_UNSIGNED_BYTE, true, 0, &v[0].color);
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
    // sem glBindTexture em lugar nenhum do corpo
}
```

**Achado de assinatura que já era visível no nome, agora confirmado no
corpo:** `DrawTile` não recebe nenhum parâmetro de textura/ângulo — e o
corpo **de fato não chama `glBindTexture`** em ponto algum. É o
caminho para **retângulos sólidos sem textura** (provavelmente usado
por caixas de UI/fundo de janela), enquanto `DrawTile4` (seção 14.2) é
o caminho textura+rotação (sprites de jogo). Também usa
`CEGL2_SHADER::SetMatrix4` (`0xaba20`, método de conveniência que
provavelmente só resolve a location do uniform e chama
`glUniformMatrix4fv` por dentro) em vez de ir direto à GL como
`DrawTile4` fazia — uma pequena inconsistência de estilo entre as duas
funções (ou just reflete código escrito em momentos diferentes), não
um bug.

### 15.3 Família de desenho do `CEGL2_IF` — mapa completo
| Função | Papel | Lida |
|---|---|---|
| `AddTile` | Monta 1 sprite escalar → `Add3D` | ✅ completo |
| `Add3D` | Converte `_EGL_PACKET_SPR` → vértice do lote atual | ✅ completo |
| `DrawPacket` | Desenha o lote acumulado via GLES2 real | ✅ completo |
| `DrawTile` | Retângulo sólido sem textura, desenho imediato | ✅ completo |
| `DrawTile4` | Sprite texturizado rotacionado, desenho imediato | ✅ completo |

As ~160 funções restantes de `CEGL2_*` (e as ~134 de `CSOUND_*`)
continuam só no nível de inventário por nome da seção 13 — nenhuma
outra foi lida nesta sessão.

## 16. Motor de áudio `CSOUND_IF` — ciclo de vida completo lido (2026-10-16)

Continuação pedida explicitamente: a API de alto nível de áudio. Li as
4 funções centrais do ciclo de vida por completo — `Init`, `Load`,
`Play`, `FrameMove` — a mesma profundidade dada à família de desenho do
`CEGL2_IF` nas seções 14–15.

### 16.1 `CSOUND_IF::Init(uint type, int maxChannels, char* path, int flag)` (`0xba3a4`, 264 B)

```c
bool CSOUND_IF::Init(uint type, int maxChannels, char* path, int flag) {
    strcpy(this->basePath, path);
    this->volumes[master/music/sfx] = 100;         // +0x110/+0x114/+0x118
    this->maxChannels = maxChannels;                 // +0x120
    this->channelPtrArray = alloc(maxChannels * 4);   // 0x2cdf8c — alocador customizado
    CSTEP* steps = alloc((maxChannels+2) * 4);         // segundo array paralelo
    steps[0] = { .type = 4, .count = maxChannels };     // cabeçalho de lista
    for (i = 0; i < maxChannels; i++)
        new (steps + 2 + i) CSTEP();                    // *** um CSTEP por canal! ***
    this->stepArray = steps + 8;                         // +0x128

    if (this->type == 4) {                               // modo "OpenSL real"
        this->sl = new CSOUND_IF_SL();                    // +4
        if (!this->sl->EngineInit(flag)) {
            delete this->sl; this->sl = nullptr;
        }
    } else {
        SetEnable(this, false);                            // modo sem OpenSL: desativa
    }
    return true;
}
```

**Achado de arquitetura importante:** `CSTEP` — que parecia só uma
classe de animação gráfica pelo nome ("step"/"passo") — é na verdade
uma **classe utilitária genérica de interpolação por passos,
reaproveitada entre gráfico e áudio**. `CSOUND_IF` aloca **um `CSTEP`
por canal de áudio**, e (seção 16.4) usa ele para controlar curvas de
fade de volume ao longo do tempo — o mesmo tipo de objeto que
provavelmente também dirige animações de sprite no `CEGL2_*` (não
confirmado lá, mas a reutilização aqui é evidência forte).

### 16.2 `CSOUND_IF::Load(int ch, char* path, uchar* buf, uint size, uint off, int fmt, int loop, int vol, uchar extra)` (`0xba9c8`, 612 B)

Confirma o despacho real por formato: se já carregado, chama
`Unload(ch)` e tenta de novo; com OpenSL ativo, despacha por `fmt`
(0 → `CSOUND_IF_SL::LoadPCM`, visto completo; 1/2 → variantes
análogas de `LoadOGG`, mesmo padrão, não transcritas de novo); em
sucesso, chama `ClearSavedata`, opcionalmente `strcat` do nome do
arquivo (debug/retry), empacota loop-points/volume/pan em bytes do
canal (`+0x40..+0x47`) e marca `+0x4a=1` (carregado), terminando com
`SetVolume`.

### 16.3 `CSOUND_IF::Play(int ch, int vol, int pan, int loopFlag, uchar fadeId)` (`0xbad78`, 400 B)

```c
int CSOUND_IF::Play(int ch, int vol, int pan, int loopFlag, uint8_t fadeId) {
    Channel* c = channel[ch];
    if (!enabled || !c || !c->loaded) return;
    SetVolume(ch, vol);
    if (this->type == 4) {
        g_playCounter++;                                    // estatística de debug
        int startState = (fadeId == 0xff) ? 1 : 0;             // *** sem fade = ataque imediato ***
        c->fadeId = fadeId;
        c->state = (fadeId == 0xff) ? 3 : 2;                    // 3=tocando direto, 2=tocando com fade pendente
        CSOUND_IF_SL::Play(ch, vol, pan, loopFlag, startState);
        c->packed_params[0x70..0x7b] = { vol, pan, loopFlag... };  // bytes salvos p/ FrameMove usar depois
    }
    memset(&c->fadeCurveState, 0, 28);     // *** zera o estado de curva de fade (28 B) antes de tocar ***
}
```

### 16.4 `CSOUND_IF::FrameMove(int ch, float dt)` (`0xbac2c`, 332 B) — fecha o ciclo com o `CSTEP`

```c
void CSOUND_IF::FrameMove(int ch, float dt) {
    Channel* c = channel[ch];
    if (!enabled || !c || !c->loaded) return;

    if (this->type == 4) CSOUND_IF_SL::FrameMove(ch, dt);   // avança o stream OpenSL de verdade

    if (!(c->flags & 2)) {                 // sem fade pendente
        if (!(c->flags & 1)) return;        // nem tocando -> nada a fazer
    } else if (IsPlaying(ch, -1)) {          // tem fade pendente E ainda tocando
        goto CHECK_FADE_FINISHED;
    }

    int before = CSTEP::GetData(step[ch]);
    bool stepChanged = CSTEP::FrameMove(step[ch], dt, 0);   // *** avança a curva de fade ***
    if (!stepChanged) {
        c->flags &= ~1;                       // marca "não tocando mais" se a curva não setou o bit "ativo"
        if (c->flags & 2) goto CHECK_FADE_FINISHED;
        return;
    }
    int after = CSTEP::GetData(step[ch]);
    if (after != before) SetVolume(ch, after);  // *** volume muda junto com a curva do CSTEP ***
    return;

CHECK_FADE_FINISHED:
    if (CSTEP::GetData(step[ch]) != 0) return;   // curva ainda não chegou a zero
    Unload(ch);                                    // *** fade terminou -> descarrega o canal sozinho ***
}
```

**Confirma de ponta a ponta o mecanismo de fade:** o `CSTEP` por canal
é uma curva de interpolação que o `FrameMove` avança a cada frame;
quando o valor da curva muda, aplica `SetVolume`; quando a curva chega
a zero (fade-out completo), o canal se **autodescarrega** sem
intervenção externa. É uma arquitetura de fade bem mais sofisticada do
que "diminuir volume manualmente" — reaproveita a mesma máquina de
interpolação genérica usada em outros lugares do motor.

### 16.5 Estado do motor de áudio
4 funções do ciclo de vida de `CSOUND_IF` lidas por completo
(`Init`/`Load`/`Play`/`FrameMove`). Confirma por instrução: alocação de
um `CSTEP` por canal, despacho real para `CSOUND_IF_SL`
(OpenSL ES, seção 13.2) por formato/tipo, e um mecanismo de fade de
volume orientado a curva de interpolação. As ~130 funções restantes de
`CSOUND_*` (incluindo toda a `CSOUND_IF_SL`/`CSOUND_LOADER_*`) seguem
só no inventário por nome.

## 17. `CSOUND_IF_SL` — o backend OpenSL ES real, lido por completo (2026-10-16)

Continuação pedida explicitamente: a implementação por baixo do
`CSOUND_IF` (seção 16). Li `EngineInit`, `LoadPCM`, `Play` e
`CB_for_Stream` por completo — cobre os dois modos de reprodução da
classe (estático totalmente carregado vs. streaming decodificado em
blocos).

**Nota de leitura:** boa parte das chamadas aqui são `blx` **através da
vtable das próprias interfaces OpenSL ES** (`(*itf)->Metodo(itf,...)`,
o jeito C de "interface COM" do OpenSL) — isso é esperado e correto
para código OpenSL ES genuíno, não uma lacuna de análise. Resolvi por
nome as poucas chamadas de função livre (`slCreateEngine`, já
confirmado na seção 13.2; `CSOUND_LOADER_PCM`/`CSOUND_LOADER_OGG`,
seção 9.4/13).

### 17.1 `CSOUND_IF_SL::EngineInit(int maxChannels)` (`0xbb6e8`, 332 B)

```c
bool CSOUND_IF_SL::EngineInit(int maxChannels) {
    slCreateEngine(&engineObj, 0, NULL, 0, iids, req);
    (*engineObj)->Realize(engineObj, false);                 // blx via vtable do IObject
    (*engineObj)->GetInterface(engineObj, ENGINE, &engineItf);
    (*engineItf)->CreateOutputMix(engineItf, &mixObj, ...);    // offset +0x1c da vtable do engine
    (*mixObj)->Realize(mixObj, false);
    this->maxChannels = maxChannels;
    this->channelData = alloc(maxChannels * 0x88);              // 136 B por canal
    for (i = 0; i < maxChannels; i++) memset(&channelData[i], 0, 0x88);
    return true;
}
```

Confirma a sequência padrão de boilerplate do OpenSL ES
(`slCreateEngine`→`Realize`→`GetInterface`→`CreateOutputMix`→
`Realize`) **de verdade**, não emulada, e fixa o tamanho real do
registro por canal (**136 bytes**) que `CSOUND_IF` referencia por
offset desde a seção 16.

### 17.2 `CSOUND_IF_SL::LoadPCM(int ch, char*, uchar*, uint, uint)` (`0xbbe7c`, 448 B)

```c
int CSOUND_IF_SL::LoadPCM(int ch, char* path, uchar* buf, uint size, uint off) {
    Channel* c = &channelData[ch];
    CSOUND_LOADER_PCM* loader = new CSOUND_LOADER_PCM();
    c->loader = loader;
    if (!loader->Open(path, buf, size, off)) { cleanup(); return -1; }

    int numCh = loader->GetNumChannels();            // via vtable +0x2c
    int fmtCode = GetSLFormat(numCh);                   // 0xbbc18 — mapeia p/ constante SL_PCMSAMPLEFORMAT
    if (fmtCode == -1) { cleanup(); return -1; }
    c->loaded = true;
    int bitDepth = loader->GetBitDepth();              // via vtable +0x34
    c->totalSamples = sampleRate * bitDepth;              // +0x40
    c->targetFormat = fmtCode;                            // +0x44
    c->sampleBuf = alloc(...);                             // +0x3c
    loader->FillBuffer(buf, c->totalSamples, loop);       // via vtable +0x10 — decodifica os sample de verdade

    if (c->hasPlayer) {                                     // já existe objeto OpenSL deste canal
        if (numCh == c->prevNumCh && c->prevFormat == fmtCode) goto REUSE;
        Static_DeletePlayer(ch);                             // formato mudou -> recria
    }
    Static_CreatePlayer(ch, numCh, fmtCode);                 // *** cria o player OpenSL real ***
    c->hasPlayer = true;
REUSE:
    loader->Release(); c->loader = NULL;
    return 0;
}
```

Fecha o ciclo: um `CSOUND_LOADER_PCM` temporário decide o formato real
(canais/taxa/bits) e decodifica os samples, e **só então** um player
OpenSL ES de verdade é criado (ou reaproveitado, se o formato não
mudou) via `Static_CreatePlayer`.

### 17.3 `CSOUND_IF_SL::Play(int ch, int vol, ...)` (`0xbc0a4`, 452 B) — a chamada real que faz o som sair

Depois de configurar pontos de loop (campos `+0x28/+0x30`, pares de 64
bits via `strd`) e volume, o desenho central:

```c
SLPlayItf playItf = c->playItf;             // +0x78
(*playItf)->SetPlayState(playItf, SL_PLAYSTATE_PLAYING /* = 3 */);  // *** blx real na vtable ***
if (ok) c->state = 3;  // tocando
```

**É literalmente a chamada OpenSL ES `SetPlayState` de verdade** — o
ponto exato onde o som passa a sair pelo alto-falante. Lida também a
lógica de "já está tocando, reconfigura em vez de reiniciar"
(`IsPlaying` + `Static_Load` para recarregar sem recriar o player).

### 17.4 `CSOUND_IF_SL::CB_for_Stream(const SLAndroidSimpleBufferQueueItf*, void*)` (`0xbb5fc`, 208 B) — o callback de streaming

```c
void CSOUND_IF_SL::CB_for_Stream(const SLAndroidSimpleBufferQueueItf* bq, void* ctx) {
    Channel* c = (Channel*)ctx;
    bool firstCall = (bq == NULL);
    void* sample = loader->GetPlaySample();          // CSOUND_LOADER_OGG::GetPlaySample
    c->ringPtrs = sample;
    c->streaming = true;
    void* streamBuf = loader->GetStreamBuffer();
    int decoded = loader->Decode(streamBuf, loopStart, loopEnd, 0x800, firstCall);  // decodifica até 2048 B de Ogg Vorbis
    c->streaming = firstCall;

    if (c->playerObj) {
        if (decoded == 0) {
            bufferQueueItf->Enqueue(firstCall, ...);    // fim do stream -> enfileira marcador
        } else {
            void* buf = loader->GetStreamBuffer();        // re-busca o ponteiro atualizado
            bufferQueueItf2->Enqueue(buf, decoded);         // *** reabastece a fila de buffers ***
        }
    }
}
```

É o **callback de fila de buffers do Android (`SLAndroidSimpleBufferQueueItf`)**
de verdade: cada vez que o OpenSL ES termina de tocar um bloco, chama
este callback, que decodifica o próximo pedaço do Ogg Vorbis
(`CSOUND_LOADER_OGG::Decode`) e o **reenfileira** — o mecanismo real de
streaming contínuo de música, por trás de `Stream_CreatePlayer`/
`Stream_Load` (não lidas, mas agora com papel totalmente claro pelo
contraste com o caminho estático de `LoadPCM`/seção 17.2).

### 17.5 Estado final do motor de áudio
Os dois modos de reprodução do `CSOUND_IF_SL` — **estático** (PCM
totalmente decodificado na memória, `LoadPCM`→`Static_CreatePlayer`→
`Play`/`SetPlayState`) e **streaming** (Ogg Vorbis decodificado em
blocos de 2048 B via callback de fila de buffers) — estão confirmados
por leitura real de 4 funções centrais, incluindo a chamada OpenSL ES
que efetivamente inicia a reprodução. As ~125 funções restantes
(`Stream_*`, `Static_Delete*`, `EngineUninit`, `CSOUND_LOADER_OGG`/
`PCM` por dentro) seguem no inventário por nome das seções 13/16.

### 17.6 `CSOUND_IF_SL::Stream_CreatePlayer` lida por completo — quinto item 🟡, confirma a previsão da seção 17.4 (2026-10-16, loop de continuação, iteração 12)

`CSOUND_IF_SL::Stream_CreatePlayer(int ch, int numCh, int fmtCode)`
(`0xbc2bc`, 560 B, cobertura total: 134 instruções reais + pool de
literais, confirmado byte a byte que não falta nenhuma). Escolhida
sobre `Stream_Load` (216 B) porque é a que de fato monta o player
OpenSL ES de streaming do zero — simétrica a `Static_CreatePlayer`
(seção 17.2), mas pro caminho de música/Ogg.

```c
int CSOUND_IF_SL::Stream_CreatePlayer(CSOUND_IF_SL* this, int ch, int numCh, int fmtCode) {
    Channel* c = &this->channelTable[ch];   // stride 0x88 (136 B) por canal — confirma o valor
                                              // só inferido na seção 17.2 (channelData[ch])
    c->field_0x18 = c->field_0x1c = 0;   // strd, zera 8 B
    c->field_0x20 = c->field_0x24 = 0;   // strd, zera outros 8 B
    c->field_0x54 = 0;

    if (c->field_0x10 == NULL) {                          // 1ª vez neste canal?
        c->field_0x10 = operator_new(0xb08 /*2824 B*/);     // 0x2cdf6c
        new (c->field_0x10) CSOUND_LOADER_OGG();             // *** 0xbd538 — construtor real! ***
        goto retry;   // volta pro topo agora que o objeto existe
    }

    SLDataFormat_PCM fmt = <template fixo copiado via ldm/stm>;   // sp+0x4c
    SLDataLocator_AndroidSimpleBufferQueue bq = { <tipo>, numBuffers: 2 };
    CSOUND_IF_SL::SetSLDataFormat(numCh, fmtCode, &fmt);           // 0xbbb6c, nome real confirmado

    // monta SLDataSource{&bq,&fmt} e SLDataSink{...} com os SL_IID_*
    // reais (resolvidos via GOT, mesma tabela de constantes de
    // interface já vista na seção 17.1) e chama de verdade:
    if ((*engineItf)->CreateAudioPlayer(engineItf, &c->field_0x74 /*playerObj*/,
                                          &dataSource, &dataSink, 3, iids, reqs) != 0)
        return 1;

    if ((*c->field_0x74)->Realize(c->field_0x74, false) != 0) return 1;
    if ((*c->field_0x74)->GetInterface(c->field_0x74, SL_IID_PLAY,        &c->field_0x78) != 0) return 1;
    if ((*c->field_0x74)->GetInterface(c->field_0x74, SL_IID_BUFFERQUEUE, &c->field_0x7c) != 0) return 1;
    if ((*c->field_0x74)->GetInterface(c->field_0x74, SL_IID_VOLUME,      &c->field_0x80) != 0) return 1;

    // *** fecha exatamente a previsão da seção 17.4 ***
    if ((*c->field_0x7c)->RegisterCallback(c->field_0x7c, CSOUND_IF_SL::CB_for_Stream, c) != 0)
        return 1;

    c->field_0x6c = numCh;
    c->field_0x70 = fmtCode;
    return 0;
}
```

**Achados:**
- **Confirma por leitura real** a previsão que a seção 17.4 só tinha
  por contraste: `RegisterCallback(bufferQueueItf, CB_for_Stream,
  canal)` é chamado aqui mesmo, de verdade — fecha o ciclo "quem liga
  o callback de streaming" que ficava implícito.
- **Achado novo e concreto**: o objeto por canal em `+0x10` (alocado
  com `operator new(2824)` na primeira chamada) é **literalmente um
  `CSOUND_LOADER_OGG`**, construído via `placement new` (chamada direta
  ao construtor, `0xbd538`, nome confirmado no `.dynsym`) — ou seja,
  **o streaming deste motor é Ogg Vorbis exclusivamente**, nunca PCM
  (`CSOUND_LOADER_PCM` só aparece no caminho estático, seção 17.2).
  Isso também é um ponto de partida direto e testável pra uma leitura
  futura de `CSOUND_LOADER_OGG` por dentro (item ⚪ do plano).
- Confirma `channelTable` com stride **0x88 (136 B)** por canal — valor
  que a seção 17.2 só tinha inferido pelo nome `channelData[ch]`, agora
  com a aritmética de endereço real (`mla r6,r1,#0x88,ip`).
- Usa uma fila de buffers do Android (`SLDataLocator_AndroidSimpleBufferQueue`)
  com **2 buffers** — o "duplo-buffer" clássico de streaming de áudio
  (enquanto um toca, o outro é preenchido pelo callback).

**O que ficou sem confirmar:** o conteúdo exato da estrutura
`SLDataFormat_PCM` copiada do template fixo (os 28 bytes de
`ldm`/`stm`) e os valores exatos das constantes `SL_IID_*` lidas via
GOT (resolvidas estruturalmente como "uma tabela de IDs de interface",
não cruzadas uma a uma com o header do NDK nesta passada).

### 17.7 `CSOUND_LOADER_OGG::Decode` lida por completo — fecha o último item 🟡 do plano, e confirma a biblioteca real usada (2026-10-16, loop de continuação, iteração 13)

`CSOUND_LOADER_OGG::Decode(signed char*, int, long long, long long,
int*)` (`0xbd740`, 540 B, cobertura total: 135 instruções pra 135
esperadas). **Achado mais importante, antes até de olhar a lógica**:
os 3 únicos `bl` da função resolvem, por nome real no `.dynsym`, pra
`ov_read` (`0xa1264`), `ov_pcm_tell` (`0xa0864`) e `ov_pcm_seek`
(`0x9fe08`) — **a API real da `libvorbisfile`** (ou do port de ponto
fixo, Tremor — o nome da API é idêntico nos dois). Confirma de uma vez
por todas que este motor usa uma biblioteca Ogg Vorbis genuína, não um
decodificador proprietário.

```c
// CSOUND_LOADER_OGG::Decode(this, char* buf, int bufSize,
//                            int64 loopStartSample, int64 loopEndSample, int* errOut)
int CSOUND_LOADER_OGG::Decode(CSOUND_LOADER_OGG* this, char* buf, int bufSize,
                                int64_t loopStart, int64_t loopEnd, int* errOut) {
    if (errOut) *errOut = 1;             // default "não terminou"
    bool hasStart = (loopStart != -1);     // par de 32 bits == -1 == "sem valor"
    bool hasEnd   = (loopEnd   != -1);

    if (hasStart && hasEnd) {
        // *** CAMINHO 1: loop com início E fim definidos (loop de música clássico) ***
        OggVorbis_File* vf = &this->field_0x82c;    // this+0x820+0xc
        int remaining = bufSize;
        char* cursor = buf;
        do {
            int n = ov_read(vf, cursor, remaining, 0, 2, 1);  // (file, buf, len, bigendian=0, wordsize=2, signed=1)
            if (n > 0) { cursor += n; remaining -= n; continue; }
            if (n != 0) break;    // erro real de decodificação -> sai (sem seek)

            // n==0 (EOF) -> calcula quanto "passou" do ponto de loop e
            // volta pro início, cortando a diferença pra não repetir
            // amostras extras — trecho de aritmética fina (ov_pcm_tell
            // vs loopEnd, multiplicado por um tamanho de amostra) que
            // não foi decomposto byte a byte, mas o EFEITO é claro:
            // seek(loopStart) e continua decodificando pro mesmo buffer.
            ov_pcm_tell(vf);
            ov_pcm_seek(vf, loopStart);
        } while (remaining != 0);
    } else if (hasStart) {
        // *** CAMINHO 2: só início definido (loop do track inteiro, sem fim fixo) ***
        // decodifica normalmente; ao bater EOF (ov_read==0), dá
        // ov_pcm_seek(loopStart) e continua enchendo o buffer — repete
        // a faixa inteira indefinidamente a partir do início.
    } else {
        // *** CAMINHO 3: sem nenhum loop point — decodificação única ***
        // decodifica até preencher o buffer OU bater EOF; se bateu EOF
        // (ov_read<=0) sem preencher tudo, NÃO faz seek — grava o
        // número de bytes restantes em *errOut e devolve.
    }
    if (errOut) *errOut = remaining;
    return bufSize - remaining;   // bytes decodificados de verdade
}
```

**Confirma, com evidência real, exatamente como funciona o loop de
música sem costura (seamless loop) deste motor:** os pontos de
início/fim de loop são codificados como pares de 32 bits
`(-1,-1) = "sem valor"`, e a própria `Decode` decide entre 3
estratégias (loop fechado com início+fim, loop aberto só com início,
ou sem loop) — tudo por cima da API padrão `ov_read`/`ov_pcm_seek`/
`ov_pcm_tell` da libvorbisfile/Tremor, sem nenhuma lógica de
decodificação proprietária.

**O que ficou sem confirmar:** a aritmética fina de ajuste de corte no
caminho 1 (quantas amostras exatas cortar na costura do loop) e o
layout exato de `OggVorbis_File`/do campo `this+0x82c` (não vale a
pena isolar — é estrutura padrão da própria libvorbisfile, não deste
jogo).

**Fecha o último item 🟡 do plano** — todos os itens 🟡 agora têm pelo
menos a função-central lida por completo.

### 17.8 `CSOUND_IF_SL::Stream_Load` lida por completo — quinto item 🟠 da Fase 2 (2026-10-16, Fase 2, iteração 10)

`CSOUND_IF_SL::Stream_Load(int channel)` (`0xbc5a4`, 216 B, cobertura
total: 54 instruções pra 54 esperadas). É o par de `Stream_CreatePlayer`
(seção 17.6) — **o "primeiro preenchimento" do buffer de streaming**,
antes do callback (`CB_for_Stream`, seção 17.4) assumir os preenchimentos
seguintes.

```c
int CSOUND_IF_SL::Stream_Load(CSOUND_IF_SL* this, int channel) {
    Channel* c = &this->channelTable[channel];   // stride 0x88, confirmado de novo (seção 17.6)

    c->field_0x18 = (*c->field_0x10->vtbl)[0xd](c->field_0x10);   // *** chamada virtual #1 ***
    int err = (*c->field_0x7c->vtbl)[1](c->field_0x7c);             // *** chamada virtual #2 — no objeto "player interface" ***
    if (err != 0) return 1;

    c->field_0x28_0x2c = -1;   // par de 64 bits -- *** zera o loop-point A ***
    c->field_0x30_0x34 = -1;   // par de 64 bits -- *** zera o loop-point B ***
    c->field_0x20_0x24 = c->field_0x10->GetPlaySample();   // 0xbd738 — cacheia a amostra atual

    c->field_0x54 = 1;    // *** flag "streaming ocupado" ***
    void* buf = c->field_0x10->GetStreamBuffer();   // 0xbd95c
    int errOut;
    int decoded = c->field_0x10->Decode(buf, 0x800 /*2048 B, igual ao `CB_for_Stream`!*/,
                                          -1, -1, &errOut);          // 0xbd740 — seção 17.7!
    c->field_0x54 = errOut;    // *** reseta a flag (reaproveita `errOut`, não é literalmente "0") ***

    buf = c->field_0x10->GetStreamBuffer();   // *** re-busca o ponteiro (pode ter avançado no Decode) ***
    int result = (*c->field_0x7c->vtbl)[0](c->field_0x7c, buf, decoded);  // *** chamada virtual #3 — Enqueue()! ***
    return (result != 0) ? 1 : 0;
}
```

**Confirma, byte a byte, a contraparte exata de `CB_for_Stream`**
(seção 17.4): a MESMA sequência "pega o buffer → `Decode` 2048 B →
re-pega o buffer → enfileira na fila de buffers do OpenSL ES"
aparece aqui, só que como o **primeiro** preenchimento (antes do
player estar tocando) em vez do preenchimento reativo via callback. A
chamada virtual final (vtable slot 0 do objeto em `+0x7c`) é quase
certamente `(*bufferQueueItf)->Enqueue(...)` — mesmo papel que a
seção 17.4 já tinha identificado.

**Achado bônus**: os pontos de loop (`+0x28/+0x2c` e `+0x30/+0x34`,
dois pares de 64 bits) são explicitamente zerados pra `-1` aqui —
ou seja, **toda música que começa a tocar via streaming começa SEM
loop configurado**, e algum código externo (não localizado) deve
gravar um loop real depois, se a faixa precisar.

**O que ficou sem confirmar:** a identidade exata dos dois objetos
polimórficos (`field_0x10`'s vtable slot `0xd`, `field_0x7c`'s vtable
slots `0`/`1`) — prováveis wrappers C++ sobre as interfaces OpenSL ES
(`SLAndroidSimpleBufferQueueItf`), mas os nomes reais dos métodos não
foram cruzados.

### 17.9 `CSOUND_LOADER_OGG::Open` lida — sexto item 🟠 da Fase 2, revela uma classe nova e um caminho possivelmente incompleto (2026-10-16, Fase 2, iteração 11)

`CSOUND_LOADER_OGG::Open(char* path, uchar* buf, uint size, uint off)`
(`0xbd56c`, 460 B, cobertura total: 115 instruções pra 115 esperadas).
Resolvendo os `bl` por nome real, aparecem mais 4 funções genuínas da
`libvorbisfile` (`ov_open_callbacks`, `ov_seekable`, `ov_pcm_total`,
`ov_info`) **e uma classe auxiliar nova**: `COggMemMapFile`
(`Open`/`Close`/`GetBuffer`/`GetSize`, `0xbd3b4`-`0xbd530`) — um
wrapper de arquivo mapeado em memória dedicado a arquivos Ogg.

```c
int CSOUND_LOADER_OGG::Open(CSOUND_LOADER_OGG* this, char* path,
                              uchar* buf, uint size, uint off) {
    if (buf != NULL) {
        this->field_0x4 = 1;    // *** marca "modo buffer de memória" ***
        return 0;                 // *** e só isso — ver achado abaixo ***
    }

    // caminho por arquivo (`path`):
    // ... uma chamada virtual inicial em `this->field_0x0->vtbl[3](path)`
    // cujo papel exato não ficou claro (ver 17.9.2) ...

    COggMemMapFile* mmf = &this->field_0x8;
    if (!mmf->Open(path, off, size)) { /* falhou -> retorna/loop, ver 17.9.2 */ }

    uchar* fileBuf = (size == 0) ? mmf->GetBuffer() + off : mmf->GetBuffer();
    uint   fileSize = mmf->GetSize();
    this->field_0x18 = fileSize;
    this->field_0x14 = fileBuf;

    // monta os 4 "callbacks" de leitura pro vorbis (literal pool
    // copiado via `ldm`/`stm` — provavelmente os 4 ponteiros de função
    // `read`/`seek`/`close`/`tell` que operam direto sobre o buffer
    // mapeado, já que não há I/O real de arquivo aqui)
    if (ov_open_callbacks(&this->field_0x14, &callbacks, NULL, 0) < 0) {
        mmf->Close();          // falha ao abrir -> fecha o mapeamento
        continue_loop;
    }
    if (!ov_seekable(&this->field_0x14)) {
        ov_clear(&this->field_0x14);    // não dá pra buscar (seek) -> descarta
        continue_loop;
    }

    memcpy(this->+0x820, ov_info(&this->field_0x14, -1), 0x2d0 /*720 B*/);  // copia o vorbis_info inteiro!
    vorbis_info* info = ov_info(&this->field_0x14, -1);
    int channels = info->channels, rate = info->rate;    // +4/+8 do vorbis_info real

    // monta um "formato" compacto a partir de channels/rate, salvo em
    // this->+0xaf0..+0xafc (campos de 16/32 bits, formato PCM-like:
    // sampleSize=1, channels, rate, blockAlign=channels*2,
    // bitsPerSample=0x10) — provável struct no estilo WAVEFORMAT do
    // Windows, igual ao padrão PSP-SDK já visto nas seções 19/20/21
    this->field_0xb00 = ov_pcm_total(&this->field_0x14, -1);   // total de amostras
    this->field_0xb04 = 0;
    return 0;
}
```

### 17.9.1 Achado principal: confirma a biblioteca real, de novo, e uma classe nova (`COggMemMapFile`)

Mesmo padrão das seções 17.7/18: resolver os `bl` por nome antes de
ler revela, de cara, a API genuína da `libvorbisfile`/Tremor. Fecha
de vez como o arquivo Ogg chega até o decodificador: **mapeado em
memória** via `COggMemMapFile` (não lida por dentro, mas os 4 métodos
já dão o contrato completo: `Open(path,off,size)`/`Close()`/
`GetBuffer()`/`GetSize()`), com os callbacks do `ov_open_callbacks`
montados pra ler diretamente desse mapeamento — **não há I/O de
arquivo real feito pela libvorbisfile aqui**, é tudo ponteiro.

### 17.9.2 Achado possivelmente preocupante: o caminho "buffer de memória" parece incompleto

Quando `buf != NULL` (chamador já tem os dados em memória, sem
caminho de arquivo), a função **só seta uma flag e retorna sucesso
— nunca chama `ov_open_callbacks`, nunca inicializa o estado real do
vorbis**. Como `CSOUND_LOADER_OGG::Decode` (seção 17.7) assume que
`this` já é um `OggVorbis_File` válido (chama `ov_read` direto nele),
isso sugere que **o caminho de carregar OGG a partir de um buffer de
memória pronto está incompleto ou nunca é exercitado de verdade** —
mesma categoria de achado que os "laços infinitos de condição
impossível" já catalogados (código presente, mas não funcional pra
esse caso específico), só que aqui o sintoma seria crash/estado
inválido em vez de travamento. **Não cravado como bug real** sem
confirmar se algum chamador de fato usa esse caminho — fica como
pista pra investigação futura.

### 17.9.3 O que ficou sem confirmar
- O papel exato da chamada virtual inicial (`this->field_0x0->vtbl[3]`)
  e a estrutura de laço de novas tentativas em torno de
  `COggMemMapFile::Open`/`ov_open_callbacks`/`ov_seekable` — o fluxo
  de controle real (quando tenta de novo vs. quando desiste) não foi
  totalmente decomposto; o valor de retorno da função nem sempre
  parece seguir uma convenção simples "0=sucesso".
- O layout exato dos 4 ponteiros de callback montados via `ldm`/`stm`
  pro `ov_open_callbacks` (prováveis `read`/`seek`/`close`/`tell`
  sobre o buffer mapeado, não lidos por endereço).
- O formato compacto gravado em `this->+0xaf0..+0xafc` — confirmado
  QUE vem de `channels`/`rate` do `vorbis_info`, não a fórmula exata
  de cada campo.

## 18. `CCOMP_Z_DEC::Decode` lida por completo — primeiro item ⚪, e confirma a biblioteca real de compressão (2026-10-16, loop de continuação, iteração 14)

Primeiro item da camada ⚪ (sistemas nunca tocados). `CCOMP_Z_DEC::Decode(uchar*
dst, ChunkDesc* src, int totalAvail)` (`0xb6204`, 412 B, cobertura
total: 99 instruções reais + pool de literais). **Mesmo padrão de
achado das seções 17.6/17.7**: resolvendo os `bl` por nome real no
`.dynsym` antes de ler o corpo, aparecem `inflateInit_` (`0x7b180`),
`inflate` (`0x7b200`), `inflateEnd` (`0x7cbfc`) e `inflateSync`
(`0x7cdd8`) — **a API real da zlib**, confirmando de uma vez a
hipótese do plano: a compressão do `fftpack.bin`/`.obb` é **DEFLATE
padrão (zlib)**, não um formato proprietário.

```c
// CCOMP_Z_DEC::Decode(this, uchar* dst, ChunkDesc* src, int totalAvail)
// ChunkDesc = { _pad0, uint32 flags /*+4, bit1=comprimido*/, uint32 size /*+8*/,
//               _pad0xc, uchar* data /*+0x10*/ }
int CCOMP_Z_DEC::Decode(CCOMP_Z_DEC* this, uchar* dst, ChunkDesc* src, int totalAvail) {
    if (!(src->flags & 2)) {                 // *** atalho: chunk NÃO comprimido ***
        memcpy(dst, src->data, src->size);     // simples passthrough, zlib nunca entra em cena
        return src->size;
    }

    // z_stream (56 B = sizeof(z_stream) real, this->+0 em diante) zerado
    // nos campos de callback (zalloc/zfree/opaque) e next_in/avail_in
    if (inflateInit_(this, ZLIB_VERSION, sizeof(z_stream)) != 0) {
        Error(this, "..."); return -1;
    }
    this->next_out  = dst;
    this->avail_out = this->field_0x3c;    // tamanho de bloco configurável (ver `SetBlockSize`)
    int decoded = 0;

    for (;;) {
        if (this->avail_in == 0) {                    // precisa de mais dado de entrada
            // avança next_in/avail_in dentro de src->data, recortado
            // pelo limite real (`totalAvail - 0x10`, o tamanho do
            // header do chunk) — não deixa ler além do buffer de origem
            ...
        }
        int r = inflate(this, Z_NO_FLUSH);
        if (r == Z_STREAM_END) break;                   // terminou
        if (r == Z_DATA_ERROR) {
            if (inflateSync(this) != 0) goto FAIL;        // *** recuperação de stream corrompido ***
            continue;                                     // resincronizou -> continua decodificando
        }
        if (r != Z_OK) goto FAIL;

        if (this->avail_out == 0) {                      // bloco de saída cheio
            decoded += this->field_0x3c;
            this->next_out  = dst + decoded;                // próximo bloco de saída
            this->avail_out = this->field_0x3c;
        }
    }
    decoded += this->field_0x3c - this->avail_out;         // soma o resto do último bloco, parcial
    if (inflateEnd(this) != 0) goto FAIL;
    return decoded;

FAIL:
    Error(this, "..."); inflateEnd(this); return -1;
}
```

**Achados:**
- Confirma a hipótese do plano: `fftpack.bin`/pacotes do `.obb` usam
  DEFLATE/zlib real — não decriptação (já estabelecido na seção 7) e
  agora também não um formato de compressão proprietário.
- Formato de chunk descoberto por leitura real: um `ChunkDesc` com
  flag de "comprimido" no bit 1 do campo `+4` — chunks SEM essa flag
  são copiados direto (`memcpy`), sem gastar ciclos de zlib. Explica
  por que um pacote de assets pode misturar dados comprimidos e não
  comprimidos no mesmo arquivo.
- **Achado mais interessante**: em caso de `Z_DATA_ERROR` (stream
  corrompido), o código **não falha imediatamente** — chama
  `inflateSync` pra tentar reencontrar um ponto de sincronização
  válido no meio do stream e **continuar decodificando a partir
  daí**. Isso é uma escolha deliberada de resiliência, consistente
  com a seção 7 (`.obb` com mismatch de versão corrigido manualmente
  por esta investigação) — o código já esperava lidar com pacotes
  possivelmente alterados/incompletos.

**O que ficou sem confirmar:** o layout exato de `ChunkDesc` fora dos
3 campos usados (`+4`/`+8`/`+0x10`), e o valor exato de
`this->field_0x3c` (tamanho de bloco) — sabido que existe e que vem de
`SetBlockSize`, mas não lido por dentro. `CCOMP_Z_ENC::Encode`
(contraparte de compressão) não lida nesta passada — dado que
`Decode` já confirma a biblioteca e o formato de chunk, `Encode`
provavelmente só interessa pra quem for RECOMPRIMIR assets
modificados, não pra entender o jogo em si.

### 18.1 `CCOMP_Z_ENC::Encode` lida por completo — sétimo item 🟠 da Fase 2 (2026-10-16, Fase 2, iteração 12)

`CCOMP_Z_ENC::Encode(uchar* dst, uchar* src, int srcSize, int level)`
(`0xb63d0`, 432 B, cobertura total: 102 instruções reais + pool de
literais). Resolvendo os `bl` por nome real, aparecem `deflateInit_`,
`deflate` e `deflateEnd` — a contraparte real de compressão do
`inflateInit_`/`inflate`/`inflateEnd` já confirmado em `Decode`
(seção 18).

```c
int CCOMP_Z_ENC::Encode(CCOMP_Z_ENC* this, uchar* dst, uchar* src,
                          int srcSize, int level) {
    this->zalloc = this->zfree = this->opaque = NULL;
    if (deflateInit_(this, level, ZLIB_VERSION, sizeof(z_stream)) != 0) {
        Error(this, "..."); return -1;
    }

    this->next_out  = dst + 0x10;         // reserva 16 B de cabeçalho
    this->avail_out = this->field_0x3c;     // tamanho de bloco (mesma convenção de `Decode`)
    int compressedSize = 0x10;
    int flush = Z_NO_FLUSH;

    for (;;) {
        // alimenta blocos de `src` (tamanho configurável, `this->+0x38`);
        // no último bloco, muda `flush` pra Z_FINISH
        int r = deflate(this, flush);
        if (r == Z_STREAM_END) break;
    }
    compressedSize += this->field_0x3c - this->avail_out;

    int endResult = deflateEnd(this);
    if (endResult != 0) { Error(this, "..."); return -1; }

    dst->magic = MAGIC;          // literal fixo
    dst->size  = srcSize;          // +8
    dst->field_0xc = endResult;      // ==0

    if (compressedSize < srcSize) {
        dst->flags = 2;                // *** comprimiu e valeu a pena ***
        return compressedSize;
    }

    // *** comprimir NÃO ajudou -- descarta e guarda o original cru ***
    Error(this, "...");                   // chamado mesmo não sendo falha fatal
    dst->flags = endResult;                 // ==0 -> "não comprimido"
    memcpy(dst + 0x10, src, srcSize);         // sobrescreve com os dados originais
    return srcSize + 0x10;
}
```

**Achado principal: fecha o par com `Decode` e confirma a convenção
exata do `flags`** — `flags=2` (bit 1 setado) = "comprimido" (igual
ao `& 2` que `Decode` testava), `flags=0` = "cru". **E revela um
fallback real de compressão**: se o resultado comprimido não ficar
**menor** que o original, o `Encode` **descarta o dado comprimido e
grava os bytes originais sem compressão** — a mesma lógica de
"não vale a pena comprimir isso" que muitos formatos de pacote usam,
agora confirmada com instrução real neste motor. `Error()` é chamado
também nesse caminho de fallback, mesmo não sendo um erro fatal —
sugere que `Error()` é mais um canal de log/diagnóstico genérico do
que um sinalizador estrito de falha.

## 19. `cSaveFFT::Save` lida por completo — segundo item ⚪, primeiro toque real em `CFFT_STATE` (2026-10-16, loop de continuação, iteração 15)

Segundo item da camada ⚪. Entre as 5 classes do sistema de save
(`pspSaveBase`/`pspSaveList`/`pspSaveAuto`/`cSaveFFT`/`CAUTOSAVE`),
escolhi `cSaveFFT::Save(int mode)` (`0x27fcb8`, 460 B, cobertura
total: 113 instruções reais) por ser o orquestrador de save do próprio
jogo (`pspSaveBase` é a camada de emulação da API do PSP por baixo,
menos específica do FFT). Cobertura confirmada via o símbolo exato no
`.dynsym` (não há ambiguidade de endereço aqui).

```c
// cSaveFFT::Save(this, int mode)
int cSaveFFT::Save(cSaveFFT* this, int mode) {
    char path[0x104];
    strcpy(path, (char*)this);              // *** this começa com um campo char[] (basename/caminho) ***
    int len = strlen(path);
    memcpy(path + len, <sufixo fixo de 12 B>, 12);   // extensão/sufixo do arquivo de save

    CFILE* f = new CFILE(path);              // 0xb6620 — classe de arquivo própria do jogo
    int openResult = f->Open(2);              // 0xb6654, modo 2 = escrita

    if (openResult == 1) {                     // falha ao abrir
        if (f) { f->~CFILE(); delete f; }
        return 1;                                // propaga o erro, sem escrever nada
    }

    if (mode == 0) {
        // *** grava o timestamp "quando foi salvo" ANTES do blob ***
        void* saveBlob = Savedata_GetAddr();                    // 0x28a08c
        SYSTEMTIME* ts = (SYSTEMTIME*)(saveBlob + 0x2798c);        // escreve DIRETO dentro do blob de save!
        GetLocalTime(ts);                                          // 0xba094 — API estilo Win32/PSP-SDK

        CFFT_STATE::SetParam(0x39, 1);              // *** 1º toque real em CFFT_STATE ***
        CFFT_STATE::SetParam(0x3a, ts->wYear);
        CFFT_STATE::SetParam(0x3b, ts->wMonth);
        CFFT_STATE::SetParam(0x3c, ts->wDay);         // (pula wDayOfWeek)
        CFFT_STATE::SetParam(0x3d, ts->wHour);
        CFFT_STATE::SetParam(0x3e, ts->wMinute);
        CFFT_STATE::SetParam(0x3f, ts->wSecond);
        // cai direto no bloco abaixo (não retorna, não refaz o cheque de mode)
    }

    // *** grava o blob de save de verdade (roda sempre, inclusive após o bloco acima) ***
    void* saveBlob = Savedata_GetAddr();                       // 0x28a08c
    int   size     = pspGetFftPspSaveDataSize();                  // 0x28a080
    f->Write(saveBlob, 0, size);                                    // 0xb6770
    f->~CFILE(); delete f;
    return 0;
}
```

**Achados:**
- **Primeira leitura real de `CFFT_STATE` por dentro** (até agora só
  citada de fora, "candidata a orquestradora de nível mais alto").
  Descobertos 7 IDs de parâmetro reais e seu papel exato:
  `0x39`=flag "tem timestamp" (sempre `1`), `0x3a`-`0x3f`=ano/mês/
  dia/hora/minuto/segundo do último save — dá um ponto de partida
  concreto e testável pra investigar `CFFT_STATE::GetParam` no futuro
  (basta procurar por esses mesmos IDs do lado da leitura).
- O timestamp é obtido via `GetLocalTime(_SYSTEMTIME*)` (`0xba094`) —
  **uma API de estilo Win32/PSP-SDK**, não uma chamada POSIX
  (`time()`/`localtime()`) — reforça a origem do código (camada de
  compatibilidade herdada do SDK do PSP, como o nome `pspSaveBase`
  já sugeria).
- `cSaveFFT` guarda seu caminho de arquivo como uma **string C
  diretamente no início do próprio objeto** (`strcpy(buf, this)`) —
  não um ponteiro separado.
- O parâmetro `mode` não seleciona "tipo de save" — seleciona **se o
  timestamp deve ser atualizado** antes de escrever o blob. O blob em
  si (`Savedata_GetAddr()`/`pspGetFftPspSaveDataSize()`) é sempre
  escrito, com ou sem `mode`.

**O que ficou sem confirmar:** o conteúdo/formato do "blob" de save
(`Savedata_GetAddr()`), e se os offsets exatos de `SYSTEMTIME` batem
com a estrutura real do PSP-SDK (assumidos pelo layout Win32 clássico
de 8 campos de 16 bits — plausível dado o uso de `GetLocalTime`, mas
não cruzado com um header). `CAUTOSAVE::Save`/`Load` (maiores, 592/632
B) e `pspSaveList`/`pspSaveAuto` continuam não lidos.

### 19.1 `CAUTOSAVE::Save` lida — oitavo item 🟠 da Fase 2, e um achado enorme: grava um dump completo da heap (2026-10-16, Fase 2, iteração 13)

`CAUTOSAVE::Save(uint mode)` (`0x28c7ec`, 592 B, cobertura total: 142
instruções reais + pool de literais). Resolvendo os `bl` por nome
antes de ler, aparece uma lista enorme de funções nunca vistas nesta
investigação: `CWORK_MEM::GetTail`, `iOS_ResumeGetData`/
`iOS_WorldMapResumeGetData`, `CFFT_STATE::Suspend`, `xpLib_GetTPage`,
`CAPP_INFO::GetStoragePath`, `xpGetHeap`/`xpGetHeapSize`/
`xpMoveHeap`, além de `CCOMP_Z_ENC::Encode` (seção 18.1, acabada de
ler!) e o mesmo `CFILE` já visto em `cSaveFFT::Save` (seção 19).

```c
// CAUTOSAVE::Save(mode) -- "this" nunca é usado no corpo
int CAUTOSAVE::Save(uint mode) {
    void* scratch = g_workMem->GetTail(0x180000);   // *** reserva 1,5 MB de memória de trabalho ***

    void *buf, *size;
    if (mode == 0)
        iOS_WorldMapResumeGetData(&buf, &size);         // snapshot de "resume" do MAPA MUNDI
    else
        iOS_ResumeGetData(&buf, &size);                   // snapshot de "resume" de BATALHA
    memcpy(scratch + 0x20, buf, size);                      // copia o snapshot pro scratch

    CFFT_STATE::Suspend(g_cfftState, scratch + 0xc0020);     // *** snapshot do estado geral do jogo ***

    CCOMP_Z_ENC enc;    // construído em pilha
    void* tpage = xpLib_GetTPage(&buf);                       // dados de "página de textura" (conceito PS1)
    int compSize = enc.Encode(scratch + 0xc006c, tpage, size, -1); // *** COMPRIME via zlib (nível -1 = default) ***

    char path[...];
    strcpy(path, CAPP_INFO::GetStoragePath());
    memcpy(path + strlen(path), <sufixo fixo de 11 B>, 11);     // monta o caminho do arquivo de autosave

    CFILE* f = new CFILE(path);
    if (f->Open(2) == 1) goto CLEANUP;    // modo 2 = escrita (igual seção 19)

    // grava um cabeçalho de 4 words em `scratch` (constantes + `mode`)
    // e um campo de tamanho total (contagem de blocos × tamanho por
    // bloco, 0xc006c B) em scratch->+0x10
    f->Write(workMemTail2, 0, totalSize);                       // *** grava os dados do scratch ***
    f->Write(workMemTail3, compSize, scratch_advanced);           // 2º bloco
    f->Write(tpage_related_ptr, compSize2, size2);                 // 3º bloco

    // *** grava a heap ALOCADA INTEIRA no arquivo! ***
    void* heapBase = xpGetHeap();
    uint  heapSize = xpGetHeapSize();
    f->Write(&heapBase_sign_extended_64bit, heapBase, 8);           // 8 B — o próprio ponteiro, como metadado
    f->Write(heapBase, scratch + 0x74, heapSize);                     // *** o CONTEÚDO INTEIRO da heap! ***

    xpMoveHeap(0, 0, 1);    // *** compacta/realoca a heap depois de salvar ***

CLEANUP:
    if (f) { f->~CFILE(); delete f; }
    return result;
}
```

**Achado principal: `CAUTOSAVE::Save` não é um save de progresso —
é um "suspender pra disco" de verdade, que grava o conteúdo bruto da
heap alocada do jogo inteiro** (`xpGetHeap()`/`xpGetHeapSize()` +
`CFILE::Write` do buffer completo), depois de compactar/realocar a
heap via `xpMoveHeap`. Isso é categoricamente diferente de
`cSaveFFT::Save` (seção 19, que só grava um "blob" de progresso
pré-definido) — `CAUTOSAVE` é o mecanismo que deixa o jogador
retomar EXATAMENTE de onde parou (inclusive estado de alocador de
memória), não só os dados de progresso da história. Confirma também
que o motor tem sua própria API de gerência de heap (`xpGetHeap`/
`xpGetHeapSize`/`xpMoveHeap`/`xpGetHeapSize` — prefixo `xp`, nunca
visto antes nesta investigação) e um sistema de "resume data" dual
(mapa mundi vs. batalha, via `iOS_WorldMapResumeGetData`/
`iOS_ResumeGetData` — já catalogadas por nome em listagens anteriores
do `.dynsym`, mas nunca cruzadas com um chamador real até agora).

**Achado bônus:** confirma `CCOMP_Z_ENC::Encode` (seção 18.1) sendo
usado de verdade com **nível de compressão `-1`** (`Z_DEFAULT_
COMPRESSION`, a convenção real da zlib) — primeira vez que vemos o
encoder realmente chamado em código do jogo, não só analisado
isoladamente.

**O que ficou sem confirmar:** o layout byte a byte exato dos
múltiplos blocos gravados no arquivo (cabeçalho de 4 words, os 3
`CFILE::Write` intermediários, e os offsets exatos dentro do scratch
de 1,5 MB) — a estrutura geral (resume data + estado + tpage
comprimido + heap completa) está confirmada, mas não cada campo
individual. `CAUTOSAVE::Load` (par desta função, `0x28ca3c`, 632 B)
continua não lida.

## 20. `CINPUT_IF_TOUCH::OnTouchesBegan` lida por completo — terceiro item ⚪, revela um detector de duplo-toque (2026-10-16, loop de continuação, iteração 16)

Terceiro item da camada ⚪. `CINPUT_IF_TOUCH::OnTouchesBegan(int,int,
int,int,int)` (`0xb42b0`, 356 B, cobertura total: 89 instruções pra 89
esperadas) — a função que recebe de verdade um evento de toque iniciado
(provável ponte direta com o callback Android `onTouchEvent`/
`ACTION_DOWN`).

```c
// OnTouchesBegan(this, int slot, int touchId, int x, int y)
void CINPUT_IF_TOUCH::OnTouchesBegan(CINPUT_IF_TOUCH* this, int slot,
                                      int touchId, int x, int y) {
    this->genCounter[slot] = this->nextGen++;   // +0x700/+0x704 — numera essa atribuição de slot

    int count = this->activeCount;    // +0x0
    if (count < 0) return;              // defensivo
    int idx;
    bool reused;
    if (count == 0) {
        idx = 0; reused = false;          // primeiro toque: usa o slot 0 direto
    } else if (this->touchId[0] == touchId) {
        idx = 0; reused = true;             // atalho comum: já é o mesmo touchId do slot 0
    } else {
        // procura um slot JÁ OCUPADO com o mesmo touchId (atualização)
        idx = find(this->touchId, count, touchId);
        if (idx == -1) {
            // não achou -> procura um slot LIVRE (touchId[i]==0)
            idx = find_empty(this->touchId, count);
            if (idx == -1) return;    // *** sem slots livres: toque extra é ignorado, sem erro ***
            reused = false;
        } else reused = true;
    }

    this->touchFlags[idx] |= 0x80;         // *** marca "toque ativo" (bit 7) *** — decodificado de um
                                             // idioma `mvn ip,ip,lsl#25; mvn ip,ip,lsr#25` que, uma vez
                                             // truncado pro `strb` final, equivale a um simples OR de bit
    this->touchId[idx] = touchId;             // +0x10, array de 4 B por slot
    this->curX[idx] = this->startX[idx] = x;    // +0x38 / +0x88, 0x50 B apart
    this->curY[idx] = this->startY[idx] = y;    // +0x60 / +0xb0, 0x50 B apart

    if (reused) {
        // *** detector de duplo-toque, só roda se o touchId já existia ***
        if (GetTouchCount() == 1) {                // 0xb41ec
            int state = this->comboState;            // +0x100
            if (state == 0) {
                this->comboTimestamp = timeGetTime();  // 0xb9fe0 — API Win32/PSP-SDK, igual a `GetLocalTime` da seção 19
                this->comboState = 1;
            }
            else if (state == 2) { this->comboState = 3; }   // 2º toque dentro da janela -> avança
            else { this->comboState = 0; this->comboTimestamp = 0; }  // estado inesperado -> cancela
        } else {
            this->comboState = 0; this->comboTimestamp = 0;      // mais de 1 dedo na tela -> cancela a detecção
        }
    }
}
```

**Correção (seção 26):** a versão original desta seção tinha os ramos
`state==0`/`else` trocados (dizia "state==0 → nada a fazer" e
"else → `comboTimestamp=now; comboState++`"). A leitura de
`OnTouchesEnded` na seção 26 exigiu reconferir `OnTouchesBegan` byte a
byte de novo, e a lógica real é a trocada: **`state==0` é quem inicia
o rastreio** (`comboTimestamp=now; comboState=1`), e o `else`
(cobrindo `state==1` e qualquer outro valor inesperado) é quem
**cancela**. O ramo `state==2 → comboState=3` sempre esteve certo. Ver
seção 26 pro quadro de estados completo e corrigido.

**Achados:**
- Confirma a arquitetura de múltiplos toques simultâneos: arrays
  paralelos por slot (`touchId`, `curX/curY`, `startX/startY`,
  `touchFlags`), com busca linear por touchId OS-nativo e fallback
  pra slot livre — sem alocação dinâmica, capacidade fixa (slots
  esgotados = toque extra simplesmente ignorado, sem erro).
- **Achado principal: um detector de duplo-toque embutido na própria
  camada de input de toque**, usando uma máquina de estados de 4
  valores (`comboState` em `this->+0x100`) e `timeGetTime()`
  (`this->+0x104`) — mesmo padrão de API estilo Win32/PSP-SDK já visto
  na seção 19 (`GetLocalTime`), reforçando que esse compat layer tem
  várias funções de tempo "emprestadas" do SDK original do PSP. A
  janela de tempo exata pra considerar "duplo toque" não foi
  encontrada nesta função (deve estar em outra função que lê
  `comboTimestamp`, não localizada nesta passada).
- Confirma `GetTouchCount()` (`0xb41ec`, self-classe) como "quantos
  dedos estão na tela agora" — usado aqui pra só tentar detectar
  duplo-toque quando há exatamente 1 dedo (evita falso positivo
  durante multi-touch/pinça).

**Atualização (seção 26):** `OnTouchesEnded` foi lida e fecha boa
parte do que ficava aberto aqui — ver seção 26 pro quadro de estados
completo (`comboState` vai até `4`, não para em `3`) e pra confirmação
de qual campo é o sinal consumível de "duplo-toque". A janela de
tempo exata (`comboTimestamp` comparado contra o quê) continua sem
confirmação.

## 21. `CFRAMERATE::FrameMove` lida por completo — quarto item ⚪, revela o medidor/regulador real de velocidade do jogo (2026-10-16, loop de continuação, iteração 17)

Quarto item da camada ⚪ ("classes utilitárias... provável trabalho de
glue sem achados arquiteturais novos" — o plano já avisava que a
expectativa era baixa, mas esta função surpreendeu). Escolhida
`CFRAMERATE::FrameMove()` (`0xbd9e4`, 244 B, cobertura total: 61
instruções pra 61 esperadas, função folha — só helpers de software
float do libgcc, `__aeabi_ui2f/i2f/fmul/fdiv/fcmpgt`) em vez dos
getters/setters triviais da mesma classe.

```c
// CFRAMERATE::FrameMove(this) — chamada uma vez por frame real
int CFRAMERATE::FrameMove(CFRAMERATE* this) {
    this->totalCalls++;            // +0x0 — contador de chamadas desde o início

    if (this->fixedMode) {                                // +0x24, setado por SetFixedMode(int)
        if (this->pendingSteps <= 0) {                       // +0x28, setado por FrameStep(int)
            this->rate = 0;                                     // +0x14 (reaproveitado como int 0 aqui)
            return 0;
        }
        this->pendingSteps--;
        this->rate = 1.0f;             // modo fixo: cada chamada = exatamente 1 "tick" de taxa 1.0
        return 0;
    }

    this->tickCount++;             // +0x4 — ticks acumulados desde a última recalibração
    uint32_t now = timeGetTime();    // 0xb9fe0 — mesma API Win32/PSP-SDK das seções 19/20
    uint32_t elapsed = now - this->lastTime;   // +0x8

    if (elapsed <= 1000) return 0;   // *** só recalibra a taxa ~1x por segundo, não todo frame ***

    // recalcula a taxa real de ticks/segundo dos últimos ~1s:
    float measured = (this->baseRate * (float)elapsed / 1000.0f) / (float)this->tickCount;  // +0xc = baseRate
    float cap = this->rateCap;        // +0x18
    this->rate = (measured > cap) ? cap : measured;   // +0x14 — clampado no teto configurado
    this->scale = this->baseRate / this->rate;           // +0x10 — fator derivado (baseRate/rate)

    this->lastTime = now;              // +0x8
    this->tickCount = 0;                // +0x4
    return 1;
}
```

**Achados:**
- **É o regulador de velocidade/FPS real do jogo** — não um simples
  contador de quadros. Mede, aproximadamente uma vez por segundo
  (`elapsed > 1000ms`), quantos ticks de `FrameMove` aconteceram de
  verdade (`tickCount`) contra um tempo real medido via
  `timeGetTime()`, calcula uma taxa efetiva, **clampa contra um teto
  configurável** (`rateCap`, `+0x18`), e deriva um fator de escala
  (`baseRate/rate`, `+0x10`) — plausivelmente usado em outro lugar
  pra ajustar velocidade de animação/lógica quando o dispositivo não
  consegue manter a taxa alvo (`baseRate`, `+0xc`).
- **Modo "fixo" separado e completo** (`fixedMode`+`pendingSteps`,
  controlados por `SetFixedMode`/`FrameStep`): em vez de medir o
  relógio real, consome passos pré-enfileirados um por chamada,
  sempre com taxa `1.0` — mecanismo claro de **avanço de quadro
  determinístico** (debug/replay/gravação), independente do
  relógio de parede.
- Terceira ocorrência da família de API Win32/PSP-SDK
  (`timeGetTime`, depois de `GetLocalTime` na seção 19 e de novo
  aqui) — confirma que esse não é um caso isolado, é um padrão real
  da camada de compatibilidade herdada do SDK original do PSP.

**O que ficou sem confirmar:** quem lê `rate`/`scale`
(`+0x14`/`+0x10`) depois de calculados — não localizado nesta
passada, mas os nomes dos getters já catalogados (`GetRate`,
`GetSpeed`) dão um ponto de partida direto pra uma leitura futura.

## 22. `CFFT_STATE` — construtor lido por completo + mapa de campos confirmado — fecha o último item do plano (2026-10-16, loop de continuação, iteração 18)

Último item do plano inteiro. `CFFT_STATE` era "candidata a classe
orquestradora de nível mais alto do jogo", citada de fora várias
vezes mas nunca lida por dentro. Li o construtor
(`CFFT_STATEC2Ev`, `0x28bfb8`, 584 B, cobertura total: 146
instruções — só inicialização de campos, nenhuma chamada) e, por ser
muito barato (a maioria tem 2-6 instruções), **todos os 23
getters/setters pequenos** citados no plano — o que dá um mapa de
campos quase completo, não só os defaults.

### 22.1 Mapa de campos confirmado (getter/setter → offset real)

| Offset | Campo | Confirmado por |
|---|---|---|
| `+0x0`/`+0x4` | tamanho de render (w,h) — default `340`/`240` | `GetRenderSize(int*,int*)` |
| `+0x8`/`+0xc` | escala de vértice (x,y) — default `1.0f`/`1.0f` | `Get`/`SetVertexScaling(float,float)` |
| `+0x10` | `captureRequest` — default `0` | `GetCaptureRequest` |
| `+0x14` | `captureDraw` — default `0` | `GetCaptureDraw` |
| `+0x18` | `encountRequest` — default `0` | `GetEncountRequest` |
| `+0x1c` | **`mode`** — default `0` | `Get`/`SetMode`, e também lido por `GetBackdropColor`/`GetMenuBarVisible` (ver 22.2) |
| `+0x20` | `debugMode` — default `0` | `Get`/`SetDebugMode` |
| `+0x24` | `moviePlaying` — default **`-1`** (sentinela "nenhum") | `Get`/`SetMoviePlaying` |
| `+0x28..` | array `musicBuffer[]` (índice `+0xa`) — zerado | `Get`/`SetMusicBuffer(int idx,...)` |
| `+0x30` | `settingsEnable` — default `0` | `Get`/`SetSettingsEnable` |
| `+0x34` | `linkEnable` — default `0` | `Get`/`SetLinkEnable` |
| **`+0x38..`** | **array `params[]`** (índice direto, sem offset) | `Get`/`Set`/`AddParam(int id, ...)` — ver 22.3 |

### 22.2 Achado: `mode` (`+0x1c`) controla UI e cor de fundo

`GetMenuBarVisible()` (`0x28c2c0`) lê `mode` e retorna **oculto (`0`)
quando `mode` ∈ `{2,3,4}`**, visível (`1`) nos demais valores — a
primeira confirmação real de que "modo" não é só um rótulo, ele
**decide se a barra de menu aparece**. `GetBackdropColor(float*,
float*,float*)` (`0x28c288`) também é indexado por `mode` via uma
tabela de salto de 5 casos (`0`–`4`) — nesta build, todos os 5 casos
convergem pro mesmo bloco de código (`0x28c2ac`, fora da janela lida),
então o mecanismo de "cor de fundo por modo" existe mas não pôde ser
diferenciado caso a caso nesta passada.

### 22.3 Achado principal: fecha de vez a pergunta da seção 19 sobre `params[]`

A seção 19 (`cSaveFFT::Save`) já tinha descoberto que `CFFT_STATE::
SetParam` grava o timestamp do save nos IDs `0x39`-`0x3f`, mas sem
saber o layout exato. Agora, com `GetParam`/`SetParam`/`AddParam`
lidos por completo:

```c
int  CFFT_STATE::GetParam(int id)            { return *(int*)((char*)this + 0x38 + id*4); }
void CFFT_STATE::SetParam(int id, int val)   { *(int*)((char*)this + 0x38 + id*4) = val; }
void CFFT_STATE::AddParam(int id, int delta) { *(int*)((char*)this + 0x38 + id*4) += delta; }
```

**`params[]` começa exatamente em `this+0x38`** — confirma que os IDs
`0x39`-`0x3f` da seção 19 (timestamp do save) caem em
`this+0x38+(0x39..0x3f)*4` = `this+0x11c` até `this+0x134`, dentro do
grande bloco zerado pelo construtor (`+0x38` até `~+0x454`, 1088 B —
sem defaults especiais, cada "parâmetro" começa em `0`). Isso fecha
de vez a investigação "quem grava/lê" sem precisar adivinhar mais: é
literalmente um array plano de `int`, acessado por índice, sem
indireção nem validação de bounds.

### 22.4 Estado final — fecha o plano inteiro (Fase 1)

Com esta seção, **todos os itens do `RE_BACKLOG_PLAN.md` (🔴🟠🟡⚪)
têm pelo menos a função-central lida por completo e documentada**.
O critério de "zerado" definido no próprio plano foi atingido.

### 22.5 O cluster de mapeamento de identidade — lido por completo, confirma a ponte real (2026-10-16, Fase 2, iteração 3)

Terceiro item da Fase 2 (`RE_BACKLOG_PLAN_PHASE2.md`): as 7 funções
pequenas de `CFFT_STATE` que pareciam ligar IDs de sprite do mapa
mundi, IDs de unidade de batalha e IDs de "face" (retrato). Todas são
funções folha, puramente lookup-table com validação de faixa — lidas
por completo (404 B somadas, cobertura total):

```c
int CFFT_STATE::FaceIDToFID(int faceID) {                 // 0x28c644, 36 B
    if ((unsigned)faceID > 0xcd) return -1;                 // faixa 0..0xcd (206 entradas)
    return faceIdTable[faceID];
}

int CFFT_STATE::UnitIDToFID_SPRE(int unitID) {             // 0x28c668, 40 B
    if ((unsigned)unitID > 0xa9) return -1;                  // faixa 0..0xa9 (170 entradas)
    return *(int*)((char*)unitTable + unitID*4 + 0x338);
}

int CFFT_STATE::UnitIDToFID_SP2(int unitID, int variant) { // 0x28c690, 80 B
    if ((unsigned)unitID > 0xa9) return -1;
    if (unitID == 0x9a) {                                      // *** unidade especial (0x9a=154) ***
        if ((unsigned)variant > 3) return -1;                    // 4 variantes (0..3)
        return *(int*)((char*)variantTable + variant*4 + 0x5e0); // tabela SEPARADA, indexada pela variante
    }
    return *(int*)((char*)unitTable + unitID*4 + 0x338);        // mesma tabela/offset de UnitIDToFID_SPRE
}

int CFFT_STATE::WorldFaceIDToFaceID(int worldFaceID) {     // 0x28c6e0, 76 B
    if ((unsigned)worldFaceID <= 0x9f)                          // faixa A: 0..0x9f (160 entradas)
        return *(int*)((char*)tableA + worldFaceID*4 + 0x898);
    int idx = worldFaceID - 0xb0;
    if ((unsigned)idx <= 0x1d)                                  // faixa B: 0xb0..0xcd (30 entradas)
        return *(int*)((char*)tableB + idx*4 + 0xb18);
    return -1;                                                  // *** buraco 0xa0-0xaf (16 valores) é inválido ***
}

int CFFT_STATE::AttackTeamFaceIDToFaceID(int atfID, int* isNamed) {  // 0x28c72c, 60 B
    if ((unsigned)atfID <= 0x51) {                              // faixa "nomeado": 0..0x51 (82 entradas)
        if (isNamed) *isNamed = 1;
        return WorldFaceIDToFaceID(atfID);     // *** CHAMA a função anterior — a ponte real ***
    }
    if (isNamed) *isNamed = 0;
    return *(int*)((char*)tableC + atfID*4 + 0xb90);            // faixa "genérico": tabela separada
}

int CFFT_STATE::AttackTeamFaceIDToUnitATFID(int id) {      // 0x28c768, 88 B
    if (id == 0xcd) id = 0x4c;                                  // remapeia um sentinela
    if ((unsigned)id <= 0x51) return tableD[id];                 // via offset 0xd48
    int idx = id - 0x54;
    if ((unsigned)idx <= 0x1b) return tableE[idx];                // via offset 0xcd8
    return -1;
}

int CFFT_STATE::EVTCHRToFID(int evtChrID) {                // 0x28c7c0, 24 B
    return *(int*)((char*)tableF + evtChrID*4 + 0xe90);          // *** SEM checagem de faixa! ***
}
```

**Achados:**
- **Confirma a ponte real por chamada direta, não por suspeita**:
  `AttackTeamFaceIDToFaceID` chama `WorldFaceIDToFaceID` de verdade
  (tail-call) pra IDs "nomeados" (0–0x51) — personagens com nome têm
  **um único retrato compartilhado** entre o mapa mundi e a tela de
  "time de ataque" pré-batalha; unidades genéricas (soldados sem
  nome) usam uma tabela de retrato totalmente separada. O parâmetro
  de saída (`isNamed`) marca explicitamente qual dos dois casos
  ocorreu.
- **`EVTCHRToFID` liga o motor de eventos/diálogo (seções 9.5–10) a
  este mesmo sistema de retrato** — "EVTCHR" = ID de personagem do
  motor de eventos, convertido pra "FID" (Face ID) sem nenhuma
  validação de faixa (confia que o script de evento sempre passa um
  ID válido). Fecha uma ponte de arquitetura que nunca tinha sido
  conectada: o diálogo/cutscene mostra retratos através do MESMO
  sistema de ID usado pelo mapa mundi e pela tela de time de ataque.
- `WorldFaceIDToFaceID` tem um **buraco de 16 valores inválidos**
  (`0xa0`-`0xaf`) entre suas duas faixas válidas — provavelmente
  espaço reservado/nunca usado no range de IDs.
- `UnitIDToFID_SP2` tem um caso especial pra uma única unidade
  (ID `0x9a`=154) com 4 variantes de retrato — provavelmente um
  personagem jogável com múltiplos estados visuais (classe
  promovida? gênero? disfarce?) — não identificado qual unidade é
  essa sem cruzar com os dados reais do jogo.
- **Nota de verificação cruzada**: o endereço `0x28c6c8` (dentro de
  `UnitIDToFID_SP2`) usa o literal `0x5e0` como offset de tabela —
  é o MESMO literal que apareceu na varredura da seção 24 do
  `AI_DIFFICULTY_RESEARCH.md` ("quem toca `g+0x5e0`"), mas confirmado
  agora: é uma tabela completamente diferente, sem relação com o
  `g+0x5e0` da IA — apenas uma coincidência numérica, não um terceiro
  ponto de contato real (já suspeitado na seção 24, agora cravado).

**O que ficou sem confirmar:** o conteúdo real das 6 tabelas (valores
de Face ID específicos por personagem) — cada uma é só um array de
`int` em `.data`/`.rodata`, cruzar com nomes de personagem exigiria
dados do jogo em si, fora do escopo de engenharia reversa de código.

## 26. `CINPUT_IF_TOUCH::OnTouchesEnded`/`OnEventDispatched` lidas por completo — fecha o último item 🔴 da Fase 2, e corrige um erro real da seção 20 (2026-10-16, Fase 2, iteração 4)

Último item 🔴 da Fase 2: fechar a pergunta da seção 20 sobre quem
confirma o duplo-toque. `OnTouchesEnded(int,int,int,int,int)`
(`0xb44a4`, 248 B, cobertura total: 62 instruções exatas) e
`OnEventDispatched(int)` (`0xb45c0`, 16 B) lidas por completo.

### 26.1 Correção necessária na seção 20

Reler `OnTouchesEnded` exigiu reconferir `OnTouchesBegan` byte a byte
de novo, e isso revelou que a seção 20 tinha os ramos **trocados**: o
texto original dizia "`state==0` → nada a fazer" e "`else` →
`comboTimestamp=now; comboState++`". A ordem real das instruções é a
**inversa**: `state==0` é quem **inicia** o rastreio
(`comboTimestamp=now; comboState=1`), e o `else` (cobrindo `state==1`
e qualquer valor inesperado) é quem **cancela** (`comboState=0`). Já
corrigido diretamente na seção 20 (ver nota ali). O ramo
`state==2 → comboState=3` sempre esteve certo.

### 26.2 `OnTouchesEnded` — fecha o quadro de estados completo

```c
// OnTouchesEnded(this, int slot, int touchId, int x, int y)
void CINPUT_IF_TOUCH::OnTouchesEnded(CINPUT_IF_TOUCH* this, int slot,
                                       int touchId, int x, int y) {
    this->genCounter2[slot] = 0;    // +0xd8, por slot — zerado no início, ver 26.3

    int idx = find_slot_by_touchId(touchId);    // mesma busca confirmada na seção 20
    if (idx == -1) return;                         // touchId desconhecido, ignora

    this->touchFlags[idx] |= 0x40;    // *** bit DIFERENTE do 0x80 de OnTouchesBegan! ***
    this->curX[idx] = x;                 // reaproveita os campos +0x88/+0xb0 (seção 20: "startX/startY")
    this->curY[idx] = y;                  // agora pra gravar a posição de SOLTAR o dedo

    if (GetTouchCount() != 1) {             // 0 ou 2+ dedos na tela
        this->comboState = 0; this->comboTimestamp = 0;    // cancela (mesmo padrão da seção 20)
        return;
    }

    int state = this->comboState;
    if (state == 1) { this->comboState = 2; this->genCounter2[idx] = 1; }      // avança
    else if (state == 3) { this->comboState = 4; this->genCounter2[idx] = 1; }   // *** avança pra 4, não pra 3! ***
    else { this->comboState = 0; this->comboTimestamp = 0; }                      // cancela
}
```

**Confirma o quadro de estados completo e corrigido**
(`comboState`, `this->+0x100`):

```
0 --(toque reusado, DOWN)--> 1 --(solta, UP, 1 dedo)--> 2
2 --(toque reusado, DOWN)--> 3 --(solta, UP, 1 dedo)--> 4   *** estado final ***
qualquer outra combinação, ou != 1 dedo na tela  -->  volta pra 0
```

**Achado principal: `comboState` vai até `4`, não para em `3`** como
a seção 20 supunha — `3` é só um estado intermediário (confirma que
houve um segundo toque reusado), e `4` é o estado final de verdade.
**O sinal consumível real do "gesto completo" é
`this->genCounter2[idx]` (`+0xd8`, zerado no início da própria
`OnTouchesEnded` e setado pra `1` exatamente nas duas transições que
avançam o estado** (`1→2` e `3→4`) — ou seja, `+0xd8` marca "esta
soltada de dedo fez o `comboState` avançar", não especificamente
"duplo-toque confirmado" (isso só é verdade na segunda vez, quando
`state` chega a `4`).

**Bit de flag confirmado**: `OnTouchesBegan` seta o bit `0x80`
("toque ativo", seção 20); `OnTouchesEnded` seta o bit `0x40`
("toque solto") — **são dois bits independentes, não um
enum/estado único** — confirma que o byte de flags por slot
(`this->touchFlags[idx]`) pode ter os dois setados ao mesmo tempo
(no frame exato em que o dedo é solto).

### 26.3 `OnEventDispatched(int slot)` — achado: mais simples do que o nome sugere

```c
void CINPUT_IF_TOUCH::OnEventDispatched(CINPUT_IF_TOUCH* this, int slot) {
    this->slotTable[slot].field_0x13c = 1;
}
```

Só um setter de 1 campo por slot — **não lê nem participa do estado
de duplo-toque** (não toca `comboState`/`+0xd8`). Provavelmente marca
"o evento de toque deste slot já foi entregue/consumido pelo
restante do jogo" — um mecanismo de reconhecimento genérico, separado
do detector de combo.

### 26.4 O que ficou sem confirmar
- A janela de tempo exata do duplo-toque: `comboTimestamp`
  (`this->+0x104`) é gravado quando `state` vira `1`, mas **nenhuma
  das duas funções lidas (`OnTouchesBegan`/`OnTouchesEnded`) o
  compara contra nada** — o cheque de "dentro da janela de X ms" deve
  estar em outro lugar (talvez no consumidor de `+0xd8`, não
  localizado).
- Se o mundo real de 2 toques físicos realmente leva o estado de `0`
  até `4` em 2 ciclos down/up ou se o primeiro toque de uma sequência
  "gasta" um ciclo sem contribuir (a análise estática sugere que o
  PRIMEIRO toque de uma sequência nova — não reusado — nunca entra no
  bloco de combo, então a contagem real de "toques físicos" pra
  chegar no estado `4` depende de como o Android reusa IDs de toque
  entre toques consecutivos, isso é comportamento de runtime, não
  staticamente verificável).
- Quem consome `this->genCounter2[idx]` (`+0xd8`) depois de setado —
  não localizado nesta passada.

## 27. `CINPUT_DATA::GetData` lida — primeiro item 🟡 da Fase 2, abre um sistema nunca tocado (2026-10-16, Fase 2, iteração 14)

Primeiro item 🟡: `CINPUT_DATA` nunca tinha sido aberta nesta
investigação (só `CINPUT_IF_TOUCH`, a camada de toque bruto — seções
20/26). `CINPUT_DATA::GetData(int id)` (`0xb3548`, 36 B, cobertura
total: 9 instruções — função folha minúscula).

```c
void* CINPUT_DATA::GetData(CINPUT_DATA* this, int id) {
    int stride = 0x59c;                  // 1436 B por registro
    int* records = this->field_0x0;        // array de registros (ponteiro)
    int sentinel = records[id * stride / 4];   // 1ª word do registro -- flag de validade
    if (sentinel == -1) return NULL;             // slot inválido/não usado
    return (uint8_t*)records + id * stride;        // ponteiro pro registro de verdade
}
```

**Achado**: `CINPUT_DATA` gerencia um **array de perfis/slots de
input** (stride de 1436 B cada), cada um validado por um sentinela
`-1` na primeira word — mesma convenção "-1 = inválido/vazio" já vista
em várias outras partes do motor (seções 17.6, 19, etc.). O tamanho
generoso do registro (1436 B) bate com `CINPUT_DATA` ter ~35 métodos
(`GetPress`/`GetDown`/`GetUp`/`GetRepeat`/`SetKeyWait`/
`SetKeyDelay`/etc.) — provavelmente cada perfil guarda estado
completo de mapeamento de botão + temporizadores de repetição/delay
por botão, não só um valor simples.

**O que ficou sem confirmar:** o layout interno do registro de
1436 B (quais offsets correspondem a quais botões/temporizadores) e
quantos slots o array `records` de fato tem — não investigado nesta
passada, já que o item pedia só a função-central.

## 28. `CTHREAD::Register`/`CreateAndRegister` lidas — segundo item 🟡 da Fase 2, confirma threads reais (2026-10-16, Fase 2, iteração 15)

`CTHREAD::Register(void(*)(void*), void*)` (`0xb9eb0`, 84 B) e
`CreateAndRegister(int,...)` (`0xb9f04`, 64 B) — ambas lidas por
completo (cobertura total nos dois casos). Resolvendo o `bl` por
nome: `pthread_create` e `sched_yield` — **API POSIX real**.

```c
int CTHREAD::Register(CTHREAD* this, ThreadFunc fn, void* arg) {
    this->field_0x8  = fn;
    this->field_0xc  = arg;
    this->field_0x10 = 2;

    // *** this duplamente: como saída do pthread_t E como argumento ***
    int r = pthread_create((pthread_t*)this, NULL, trampoline, this);
    if (r != 0) return 1;

    sched_yield();              // cede o processador uma vez pra deixar a nova thread começar
    this->field_0x14 = 1;        // marca "thread criada/rodando"
    return 0;
}

int CTHREAD::CreateAndRegister(CTHREAD* this, int priority, ThreadFunc fn, void* arg) {
    if (Create(this, priority) != 0) return 1;   // 0xb9e94
    return Register(this, fn, arg) ? 1 : 0;
}
```

**Achado: `CTHREAD` usa `pthread_create` de verdade, não é um wrapper
morto** — diferente do `CCRYPT` da seção 9.1 (achado como código
morto, sem nenhum chamador no binário), `pthread_create`/`sched_yield`
são chamadas reais da libc, confirmando que este motor **usa threads
de verdade** em algum lugar (áudio assíncrono? carregamento em
segundo plano? não identificado qual subsistema usa `CTHREAD`
especificamente, mas o mecanismo em si é real e funcional).
`this` é reaproveitado de forma compacta: serve tanto de `pthread_t*`
de saída (sobrescrevendo o próprio início do objeto) quanto de
argumento passado pra nova thread via a função-trampolim (endereço
resolvido via GOT, não nomeado nesta passada).

**O que ficou sem confirmar:** o endereço/papel exato da função
"trampolim" passada pro `pthread_create` (provavelmente só chama
`this->field_0x8(this->field_0xc)` e descarta o retorno — padrão
clássico de adaptação de assinatura, mas não lida por dentro); quem
no resto do jogo de fato chama `CreateAndRegister`/`Register` (não
localizado nesta passada).

## 29. `CFILE_UTIL::FileCopy` lida — terceiro item 🟡 da Fase 2, e uma inversão de parâmetro confirmada por comportamento (2026-10-16, Fase 2, iteração 16)

`CFILE_UTIL::FileCopy(char*, char*)` (`0xb79d8`, 424 B, cobertura
total: 106 instruções pra 106 esperadas). Usa `CFILE` (já catalogada
nas seções 19/19.1) pros dois lados da cópia.

```c
// *** ordem real confirmada pelo COMPORTAMENTO, não pelo nome: (destino, fonte) ***
int CFILE_UTIL::FileCopy(char* dst, char* src) {
    CFILE* in = new CFILE(src);
    if (in->Open(1) == 1) { delete in; return 1; }      // modo 1 = leitura

    uint size = in->GetSize();
    uchar* buf = malloc(size);                             // *** aloca o arquivo INTEIRO na memória ***
    if (!buf) { delete in; return 1; }

    if (in->Read(buf, size, 0, &dummy) == 1) { /* erro */ }
    delete in;                                                // fecha a fonte antes de abrir o destino

    CFILE* out = new CFILE(dst);
    if (out->Open(2) != 1) {    // modo 2 = escrita
        if (size <= 0x400000 /* 4 MiB */) {
            out->Write(buf, 0, size);                            // escreve tudo de uma vez
        } else {
            // *** arquivos grandes: escreve em blocos de até 4 MiB ***
            for (uint off = 0; off < size; ) {
                uint chunk = min(size - off, 0x400000);
                if (out->Write(buf + off, off, chunk) != 1) break;   // erro no meio -> aborta
                off += chunk;
            }
        }
    }
    delete out;
    free(buf);
    return 0;
}
```

**Achados:**
- **A ordem dos parâmetros é `(destino, fonte)`, não `(fonte,
  destino)`** — confirmado pelo comportamento real (o 1º parâmetro é
  aberto em modo escrita, o 2º em modo leitura), não por suposição a
  partir do nome do método. Vale a pena registrar explicitamente
  porque é fácil adivinhar errado só pelo nome `FileCopy`.
- **Cópia de arquivo não é feita em streaming** — lê o arquivo fonte
  **inteiro** pra memória de uma vez (`malloc(size)`), depois escreve
  de volta em blocos de até **4 MiB** se o arquivo for maior que
  isso. Pra arquivos muito grandes, isso significa um pico de uso de
  memória igual ao tamanho do arquivo inteiro.
- O limite de 4 MiB por bloco de escrita é um valor fixo real — não
  confirmado o motivo exato (limite de alguma API Android por baixo,
  ou só uma escolha de implementação), mas o valor em si (`0x400000`)
  está confirmado por instrução.

**O que ficou sem confirmar:** `DirCreate(char*)` (`0xb78b4`, 204 B,
2ª função sugerida pelo plano pra este item) não lida nesta passada.

## 30. `CSTR_UTIL::GetName` lida — quarto item 🟡 da Fase 2, revela um comportamento surpreendente (2026-10-16, Fase 2, iteração 17)

`CSTR_UTIL::GetName(char* out, char* in, int hasFullPath)` (`0xb8d34`,
212 B, cobertura total: 53 instruções pra 53 esperadas).

```c
void CSTR_UTIL::GetName(char* out, char* in, int hasFullPath) {
    char localBuf[0x100];
    if (hasFullPath) {
        GetFile(localBuf, in);   // 0xb8ca4 — extrai só o nome do arquivo de um caminho completo
        in = localBuf;
    }

    int len = strlen(in);
    if (len <= 0) { *out = 0; return 1; }

    int dotPos = 0;
    bool foundDot = false;
    for (int i = 0; i < len; ) {
        if (IsLeadByte(in[i])) { i += 2; continue; }   // 0xb8be4 — *** pula 2 bytes de caractere Shift-JIS ***
        if (in[i] == '.') { dotPos = i; foundDot = true; }
        i++;
    }

    if (!foundDot) { *out = 0; return 1; }    // *** achado: sem extensão -> saída VAZIA, não o nome ***

    memcpy(out, in, dotPos);
    out[dotPos] = 0;
    return 0;
}
```

**Achados:**
- **Confirma consciência real de codificação multi-byte (Shift-JIS)**
  no tratamento de string: usa `IsLeadByte` pra nunca cortar no meio
  de um caractere de 2 bytes ao procurar o `.` da extensão —
  consistente com este ser um jogo japonês, e a primeira confirmação
  real (não só suposição) de que o motor lida com texto multi-byte
  corretamente nessa classe utilitária.
- **Achado comportamental surpreendente, confirmado por instrução**:
  se o nome de arquivo **não tiver `.` nenhum**, `GetName` não
  devolve o nome como está — **devolve uma string vazia** (e retorna
  `1`, um código diferente do caminho normal). Ou seja, a função
  assume que todo nome de arquivo chamado aqui TEM extensão; nomes
  sem extensão são tratados como um caso à parte, não um "nome sem
  nada pra cortar".

**O que ficou sem confirmar:** `GetFile`/`Conv`/`Find` (as outras
funções do mesmo item do plano) e `CLIST::GetData`/`DeleteAll` não
lidas nesta passada.

## 31. Binário x86 — primeira comparação real com o ARM, item ⚪ nunca tocado (2026-10-16, Fase 2, iteração 21)

Último item ⚪ concreto: o binário x86
(`FFT_Android_Mod/src/lib/x86/libgl2jni.so`, ELF i386, ~4,99 MB,
*stripped*) nunca tinha sido tocado em toda a investigação — tudo até
aqui foi só do binário ARM. Primeira comparação real: `.dynsym` tem
**6530 símbolos `FUNC`** (vs 6636 no ARM — bem próximo, consistente
com ser a mesma base de código recompilada pra outra arquitetura, não
um build divergente). Cruzando por nome mangled exato, os endereços
batem com funções já documentadas:

| Função | ARM | x86 |
|---|---|---|
| `CCOMP_Z_DEC::Decode` | `0xb6204`, 412 B | `0xb98a0`, 423 B |
| `MakeMapDanger()` | `0x27b0b0`, 400 B | `0x2869b0`, 435 B |
| `GetTargetBaseArea(int,int)` | `0x276930`, 644 B | `0x282240`, 732 B |

Desmontei `CCOMP_Z_DEC::Decode` em x86 (`Cs(CS_ARCH_X86, CS_MODE_32)`)
pra comparar com a versão ARM já documentada por completo na seção
18. **Lógica idêntica, confirmada instrução por instrução**: mesmo
teste de flag de chunk (`test byte ptr [eax+4],2`), mesmo caminho de
`memcpy` pra chunk não comprimido, mesma sequência `inflateInit_` →
`inflate` (testando `1`=fim, `0`=continua, `-3`=`Z_DATA_ERROR` →
`inflateSync`) → `inflateEnd`, mesma chamada de `Error()` nos
caminhos de falha.

**Achado de diferença real de build**: no ARM, as 4 funções da zlib
são **importadas via `.plt`/`.rel.plt`** (biblioteca externa). No
x86, elas aparecem como **símbolos globais exportados direto no
`.dynsym`** (`inflateInit_`/`inflate`/`inflateSync`/`inflateEnd`,
endereços reais `0x7a800`/`0x7a8b0`/`0x7ca70`/`0x7c880`) — ou seja,
o build x86 parece ter a zlib **embutida estaticamente** e reexportada
nesse `.so`, em vez de vinculada dinamicamente contra uma `libz.so`
do sistema. Mecanismo de linkagem diferente, lógica de negócio
idêntica.

**Conclusão desta primeira passada**: a hipótese natural — que o x86
é a mesma base de código C++ recompilada, sem lógica de jogo
divergente — se confirma pro caso testado. Não dá pra generalizar pra
todo o binário a partir de uma função só, mas não apareceu nenhum
sinal de divergência de comportamento, só de infraestrutura de
build (linkagem da zlib).

**O que ficou sem confirmar:** qualquer divergência real de
comportamento de jogo entre as duas arquiteturas — testado só 1
função; o restante do binário x86 continua inteiramente não lido.

## 32. `battle()` — passe estrutural (não linha a linha) — primeiro item da Fase 3, cobertura total (2026-10-17)

**Mudança de metodologia, documentada no `RE_BACKLOG_PLAN_PHASE3.md`**:
`battle()` (`0x207e10`, 17.156 B) é a maior função do binário inteiro
e nunca tinha sido tocada. Pra uma função deste tamanho, "lida por
completo" nesta fase significa um **passe estrutural**: grafo de
chamadas resolvido por nome, blocos principais identificados, tabelas
de salto extraídas — não pseudocódigo instrução-a-instrução de cada
um dos ~4.300 slots de instrução. Isto é intencional (ver
metodologia da Fase 3), não uma leitura rasa disfarçada: cada
achado abaixo vem de instrução real lida, só que a função como um
todo não teve cada um dos seus ~70 blocos de estado abertos.

Construí uma ferramenta nova (`struct_pass.py`, descida recursiva por
alvos de branch como o `disasm_cfg.py` já existente, mas resumindo em
vez de despejar linha a linha) — fica no scratch da sessão, reutilizável
pras próximas funções grandes da Fase 3.

### 32.1 Arquitetura confirmada: switch de 102 estados sobre um contador global

Antes do switch, dois guardas reais (lidos por instrução):
```c
if (iOS_getV2Icon(0x13) != 0) goto 0x20aa50;             // ícone de UI "19" ativo -> desvia
if (iOS_getV2Icon(0xcb) == 0) {                             // ícone "203" NÃO ativo
    if (*g_someState <= 0x19 && (g_bitmaskA >> *g_someState) & 1)
        goto 0x20afb0;                                        // estado atual está numa lista de ~26 flags -> desvia
}
r6 = iOS_getV2Icon(0xca);                                    // ícone "202"
if (*g_someState == r3 /* comparação com algo antes salvo */ ... ) { /* ver 32.3 */ }
```
(detalhe exato dos dois desvios `0x20aa50`/`0x20afb0`/`0x20afbc` não
seguido nesta passada — são os únicos 3 alvos de `bl`/branch fora do
switch principal que ficaram de fora do passe estrutural.)

O switch real:
```c
r3 = *g_battleState;              // *sl, o contador de "fase/estado de batalha"
r2 = r3 - 1;                        // estados são 1-based
if (r3 != old_value) *g_battleState_prevSlot = r3;   // grava o estado anterior num campo vizinho (+4)
if ((unsigned)r2 <= 0x65)             // 0..101 = 102 casos válidos
    goto table[r2];                     // addls pc, pc, r2, lsl #2
else
    goto DEFAULT;                        // 0x20a670
```

### 32.2 Tabela de salto completa extraída (102 entradas, 70 endereços distintos)

Técnica: tabela de 102 words em `0x2084a0`–`0x208638`, cada word é
literalmente um `b #alvo` (o compilador gera a tabela como código
executável, mesma técnica das seções 9.8/12.4/21). Extraída e
decodificada por completo — **nenhum estado ficou sem endereço
resolvido**.

- **21 estados** (`50`, `60`, `61`, `82`–`99`) caem no handler padrão
  `0x20a670` — provavelmente slots "reservado/não usado" do enum de
  estados.
- **13 estados** (`62`–`71`, `100`–`102`) caem num SEGUNDO handler
  compartilhado, `0x2092d4` — distinto do padrão, então é um handler
  real só que idêntico pra vários estados (não lido o corpo).
- **Os 68 estados restantes têm, cada um, seu próprio endereço
  único** — são os candidatos reais a "estados de batalha distintos"
  (seleção de unidade, animação de movimento, animação de ataque,
  checagem de morte, vez da IA, etc. — hipótese por posição/contexto,
  não confirmada por leitura de corpo).

Tabela completa (estado → endereço, 1-based):

```
1:0x20a5f4  2:0x20a41c  3:0x20a518  4:0x20a4a8  5:0x20a598  6:0x209780
7:0x20a2c8  8:0x20a254  9:0x20a1ec 10:0x20a14c 11:0x2096c4 12:0x209648
13:0x20a3a4 14:0x2095fc 15:0x20a0f4 16:0x20a010 17:0x209d5c 18:0x209d10
19:0x209fc8 20:0x209f80 21:0x20a080 22:0x209914 23:0x209f3c 24:0x209b4c
25:0x209ac8 26:0x209a68 27:0x209df0 28:0x209dac 29:0x209e40 30:0x20972c
31:0x209a1c 32:0x2099f4 33:0x209ca0 34:0x209984 35:0x209ba4 36:0x2098c8
37:0x20984c 38:0x209814 39:0x209550 40:0x209530 41:0x2094e4 42:0x2094ac
43:0x209458 44:0x2093b0 45:0x209378 46:0x2092e0 47:0x2092c0 48:0x209154
49:0x208f88 50:0x20a670 51:0x208f10 52:0x2091a0 53:0x208fd0 54:0x208bbc
55:0x208b00 56:0x2091dc 57:0x209090 58:0x208efc 59:0x208d64 60:0x20a670
61:0x20a670 62:0x2092d4 63:0x2092d4 64:0x2092d4 65:0x2092d4 66:0x2092d4
67:0x2092d4 68:0x2092d4 69:0x2092d4 70:0x2092d4 71:0x2092d4 72:0x208638
73:0x208fa4 74:0x209174 75:0x2088e0 76:0x208854 77:0x2089fc 78:0x208974
79:0x208c5c 80:0x208998 81:0x2088b0 82:0x20a670 83:0x20a670 84:0x20a670
85:0x20a670 86:0x20a670 87:0x20a670 88:0x20a670 89:0x20a670 90:0x20a670
91:0x20a670 92:0x20a670 93:0x20a670 94:0x20a670 95:0x20a670 96:0x20a670
97:0x20a670 98:0x20a670 99:0x20a670 100:0x2092d4 101:0x2092d4 102:0x2092d4
```

### 32.3 Catálogo de sistemas tocados (94 `bl` resolvidos por nome, nenhum corpo lido)

A descida recursiva (ainda incompleta — só alcança os blocos
diretamente acessíveis sem seguir os 70 alvos da tabela, então isto é
parcial, não a lista completa de chamadas de `battle()`) já resolve
94 chamadas distintas por nome, agrupadas por sistema:

- **Cursor/toque deslizante do campo de batalha** (família `iOSSlide*`/
  `iOSRot*`/`iOSTch*`/`iOSMapTouchCancel`/`sBattleTouchToCur`) — 15+
  funções, confirma que o controle touch do campo de batalha é um
  subsistema grande próprio, nunca antes investigado.
- **Motor 3D "ASHURA"** (`ASHURA_init`, `ASHURA_matrix`, `ASHURA_addPrim`,
  `ASHURA_getOTptrZ`, `ASHURA_clearOT`, `ASHURA_Exit`) — **nome nunca
  visto antes nesta investigação inteira**; parece ser uma segunda
  camada de desenho 3D além do `wld_*`/`CEGL2_*` já documentados,
  específica de batalha (unidades/efeitos em 3D). Candidato forte a
  próximo sistema a abrir na Fase 3.
- **Ícones/UI "V2"** (`iOS_getV2Icon`/`iOS_setV2Icon`/`iOS_v2menuSetType`/
  `iOS_v2menuSetEnable`) — `iOS_setV2Icon` sozinha aparece **69 vezes**
  dentro do que já foi varrido, de longe a chamada mais frequente;
  claramente o sistema de ícones de comando da UI de batalha.
  `iOS_getV2Icon` aparece 29 vezes, muitas no início como guarda (ver
  32.1).
- **Tutorial** (`iOSTutoCheck` ×11, `iOSTutoBtlSkipClear`,
  `iOS_clearTutorialbreak`) — confirma que há lógica de tutorial
  real entremeada no loop principal de batalha.
- **Ponte com `CFFT_STATE`** (`GetParam`/`SetParam`/`SetMode`) — mesmo
  sistema de modo de dificuldade/estado global já visto em outras
  seções (12.2, 22).
- **PS1 real**: `VSync`/`DrawSync`/`SetGeomScreen`/`AddPrim` — confirma,
  de novo, que o núcleo gráfico de baixo nível continua sendo a
  emulação da lib do PS1, mesmo dentro do loop de batalha moderno.
- **Save/Resume**: `iOS_Resume*` (6 variantes: `GetMode`,
  `BeforeBattle`, genérico, `ByAutoSave`, `Music`, `BGM`,
  `ENVEFFECT_Rain`) — sugere que uma batalha pode ser retomada de um
  save específico de "durante a batalha" (não só do mapa mundi),
  sistema nunca mencionado antes.
- **4 chamadas a endereços locais sem símbolo** (`sub_1f9620`,
  `sub_1fc478`, `sub_202ff0`, `sub_204ff0`) — candidatos a próximos
  alvos, endereços registrados mas não lidos.

**O que ficou sem confirmar (escalonado, não forçado — intencional
pro nível "passe estrutural")**: o corpo de cada um dos 70 handlers
de estado (a lógica real de cada fase de batalha), os 3 desvios
`0x20aa50`/`0x20afb0`/`0x20afbc` antes do switch, e qualquer chamada
feita só de DENTRO de um dos 70 blocos de estado (a lista de 94 `bl`
acima é só do pouco que a descida recursiva alcançou sem seguir a
tabela). Ler os 70 handlers de verdade é trabalho de várias iterações
futuras — ver `RE_FUNCTION_INVENTORY.csv` (`battle()` marcada
`read_structural`, não `read_full`).

## 33. `Wmesputmain()` — passe estrutural — 2ª maior função do binário, revela um sistema de tasks nunca visto (2026-10-17, Fase 3)

`Wmesputmain()` (`0x11173c`, 16.312 B) — mesmo tratamento da seção 32:
passe estrutural via `struct_pass.py`, não linha a linha. Cobertura da
descida recursiva: **3.963 de ~4.078 instruções possíveis (97%)** —
bem mais completa que `battle()`, porque esta função **não usa uma
tabela de salto computada** (nenhum `addls pc,...`/`ldr pc,...`
encontrado); o despacho é feito por uma cascata grande de `cmp`/`beq`/
`bne` (414 branches, 215 de retrocesso — mais "loops"/"continue" que
`battle()`, consistente com um laço de tarefas, não um switch único).

### 33.1 Confirma o papel de `W*` (já suspeitado, nunca lido): orquestrador do sistema de janelas/mensagens

95 `bl` resolvidos por nome. O grupo mais revelador é a família
inteira de funções `W*` **nunca antes lidas nem citadas**, chamadas
de dentro de `Wmesputmain`:

```
Wallocatewindow() / Wdisposewindow(MESSAGEPACKET*)
Wallocatetexture(RECT16*, tagPOLY_FT4*, long*) / Wdisposetexture(RECT16*)
Wload_replaceitems(int,int)
Wserchmessagepointer(int) / Wgetvaluelength(int) / Wcount_words2(short*,short*,char*)
Wgetanimpos2d(int, SVECTOR*)
Wmakemessagepacket(char*) / Wpushmessagepacket() / Wpopmessagepacket()
Wmultiwindow_packetextend(COMRECORD*, tagSPRT*, int)
Wsettaskkind(int) / Wtask_killmyself()
Wwrite_eventflag(int,int) / Wread_eventflag(int) / Wcnvglobaltolocalid(int)
Wextend_windowframe(int,int,RECT16*,int,int)
```

Isso confirma, com nomes reais, que existe um **subsistema `W*`
completo e nunca documentado**: alocação de janela/textura de
mensagem, uma fila de "message packets" (`push`/`pop`/`make`), e uma
ponte própria com o sistema de flags de evento (`Wwrite_eventflag`/
`Wread_eventflag` — variantes com prefixo `W` das mesmas
`write_eventflag`/`read_eventflag` já vistas em `wldday_put`, seção
12.10, e no motor de eventos, seções 9.5–9.6, confirmando que o
sistema de mensagens tem SEU PRÓPRIO acesso aos flags, paralelo ao do
mapa mundi).

### 33.2 Achado novo: um sistema de tasks "wasm" nunca mencionado

```
wasmTaskEntry() ×14   wasmGetInput1() ×1   wasmGetInput2() ×5
wasmGetInput3() ×5    wasmGetActiveTask(int) ×1
```

Nome nunca visto nesta investigação (quase certamente não é
WebAssembly — é jargão interno do motor, estilo "SSD"/"Iwasaki"
já catalogado). `Wsettaskkind`/`Wtask_killmyself` (do grupo 33.1)
reforçam a hipótese: mensagens rodam como **tasks cooperativas**,
com `wasmTaskEntry` como ponto de entrada do agendador e
`wasmGetInput1/2/3` buscando até 3 parâmetros por task — um sistema
de execução paralelo ao de bytecode de evento já documentado (seções
9.5–9.6), não o mesmo.

### 33.3 Outros sistemas confirmados por chamada

- **`iOS_CMenuTouch`** (`setYLine`/`init`/`exec`/`setDispAssist`) —
  uma classe C++ real de menu de toque **dentro** do sistema de
  mensagens (prováveis escolhas de diálogo/múltipla escolha).
- Uso pesado do sistema de ícones V2 (`iOS_getV2Icon` ×26,
  `iOS_setV2Icon` ×28) e de tutorial (`iOSTutoFlagCheck` ×8,
  `iOS_getTutoBegin` ×8, `iOS_getTutorialbreak`/`iOSTutorialMessageKill`/
  `iOSTutoTaskCheck`) — mensagens e tutorial estão fortemente
  acoplados.
- Ponte com `CFFT_STATE` (`GetParam`, `WorldFaceIDToFaceID` — a MESMA
  função confirmada na seção 22.5, reforçando que o sistema de
  retrato de personagem também alimenta mensagens de diálogo).
- Um ponto de convergência pesado em `0x1122dc` (14+ branches
  diferentes caem lá) lido por instrução: monta um "motivo de
  bloqueio" (`r4`, sentinela `0xfe`) a partir de `iOS_getV2Icon(5)`,
  `iOS_getTutorialbreak()`, `Get_bravebreak()` e
  `CFFT_STATE::GetParam(0xd)`, depois testa um campo `+0x14c` de um
  array de stride `0x400` (1024 B) contra o valor `3` — **parece ser
  o topo do laço principal de processamento de uma lista de tasks de
  mensagem**, mas o corpo do laço (o que o valor `3` representa) não
  foi lido.
- 7 chamadas locais sem símbolo (`sub_714b8`/`714c4`/`fb7e0`×19/
  `fbf74`/`fe238`/`103488`/`10def8`×4/`111638`×5) — `sub_714c4` é
  chamada bem no início da função sobre o buffer local de 0x354 B,
  padrão compatível com um `memset`/zerador de buffer; as demais não
  investigadas.

**O que ficou sem confirmar (escalonado — intencional pro nível
"passe estrutural")**: a estrutura exata do laço de tasks (o que
significa cada valor do campo `+0x14c`), os corpos de cada bloco
alcançado pela cascata de 414 branches, e o papel exato das 7 funções
locais sem símbolo. Marcada `read_structural` no
`RE_FUNCTION_INVENTORY.csv`. `mesputmain()` (a versão sem prefixo `W`,
0xe88c4, 15.744 B, 5ª maior do binário) é a candidata natural pra
comparar contra esta e confirmar se é duplicação por idioma/plataforma
ou lógica genuinamente diferente — não lida ainda.

## 34. `Main_FrameRender()` — passe estrutural — o renderizador principal do jogo inteiro, nunca tocado (2026-10-17, Fase 3)

`Main_FrameRender()` (`0x2c141c`, 16.164 B, 3ª maior função do
binário) — mesmo tratamento das seções 32/33. Descida recursiva:
**3.935 de ~4.041 instruções possíveis (97%)**, sem tabela de salto
computada (248 branches, 127 de retrocesso — cascata de `cmp`, não
switch único). 110 `bl` resolvidos por nome — o maior catálogo de
chamadas de toda a Fase 3 até aqui.

### 34.1 Fecha o elo que faltava: quem chama `CEGL2_IF`/`CEGL2_FBO`/`CEGL2_SPRITE`

As seções 13/14/15 documentaram o motor gráfico `CEGL2_*` por dentro,
mas nunca o chamador real do topo. Agora está confirmado:
`Main_FrameRender` chama diretamente `CEGL2_IF::SetScreenSize`,
`ClearBackdrop`, `InitRenderState2D`, `SetTexFilter`, `SetScissor`,
`AddSprite`, `Setup2D`, `DrawPacket` (seção 13.1), `CEGL2_FBO::Begin`/
`End`/`RenderToFBO`/`RenderFromFBO`/`GetTexture`, e
`CEGL2_SPRITE::SetScale`/`SetScaleAlignCenter`/`SetColor`/`SetAlpha`/
`Unload`. **É literalmente o ponto de entrada do frame de desenho do
jogo inteiro** — fecha o ciclo "motor gráfico documentado por dentro"
↔ "quem decide quando/como usá-lo por fora".

### 34.2 Classe nova: `CGX_SCREEN_CORRECT` — correção de proporção de tela por dispositivo

Nunca vista antes, mas pesadamente usada: `Area_ToScreen` (×26),
`Area_GetCorrect` (×22), mais `GetCorrect`/`GetScale`/`Scaled`/
`ScalingDiff`/`GetAppScaledScreenSize`/`Area_ToScreenY`/
`Area_X_AlignC`/`Area_X_ScalingDiff`/`Area_Y_ScalingDiff`. Confirma
que o jogo faz correção de proporção/escala em tempo real pra se
adaptar a telas de dispositivo diferentes — consistente com
`RETINA_SCALE(int)` (sozinha, **68 chamadas** — a função mais chamada
de toda esta passada) e `CAPP_INFO::IsDeviceiPhoneRetina4inch()`.

### 34.3 `CFFT_STATE` como hub de decisão de renderização

Nove getters/setters diferentes de `CFFT_STATE` chamados aqui:
`GetRenderSize`, `GetVertexScaling`, `GetCaptureRequest`/
`SetCaptureRequest`, `GetCaptureDraw`/`SetCaptureDraw`,
`GetEncountRequest`/`SetEncountRequest`, `GetMode`,
`GetBackdropColor`, `GetMenuBarVisible`. Confirma que o render
principal consulta e ATUALIZA um conjunto real de flags de "o que
desenhar este frame" — inclusive um fluxo de **captura de tela**
(`CaptureRequest`/`CaptureDraw`, que bate com `Offscreen_ReadPixels`/
`Offscreen_Get`, também chamadas aqui) e um fluxo de
"entrando em encontro/batalha" (`EncountRequest`) decidido no
MESMO lugar que desenha o frame.

### 34.4 Confirma um padrão "screen manager": delega pra sub-telas inteiras

`NowLoading_FrameRender()`/`NowLoading_FrameMove()` e
`SettingsWnd_FrameRender()` são chamadas de dentro de
`Main_FrameRender` — confirma que esta função não é só "desenhar o
jogo", é um **dispatcher de tela** que decide se o frame atual
desenha o jogo normal, a tela de carregamento, ou a janela de
configurações — mesma arquitetura, em espírito, do despacho de
`wldctl_cur`/`active`/`deactive`/`init` (seção 12.2), só que no nível
de tela inteira em vez de controlador de mapa mundi. `Debug_DrawFPS()`
confirma um overlay de depuração real (contador de FPS).

### 34.5 Outros achados

- Usa ponto flutuante de software (`__addsf3`/`__subsf3`/`__mulsf3`/
  `__divsf3`/`__floatsisf`/`__fixsfsi`) em pelo menos parte do
  cálculo — provavelmente herança de compilação sem FPU de hardware
  garantida em todos os alvos ARM suportados, não achado de jogo.
- 15 chamadas locais sem símbolo, a mais frequente `sub_2b6110`
  (**43 vezes**, endereço vizinho do cluster `iOS_getV2Icon`/
  `iOS_setV2Icon` em `0x2b7xxx` — candidata forte a ser outro
  acessor/wrapper de ícone, não investigado).

**O que ficou sem confirmar (escalonado — nível "passe estrutural"
intencional)**: os corpos dos ~70+ blocos individuais da cascata de
branches, a ordem exata de decisão entre "jogo normal"/"loading"/
"settings", e as 15 funções locais sem símbolo. Marcada
`read_structural` no `RE_FUNCTION_INVENTORY.csv`. `Main_FrameMove()`
(`0x2bbb74`, 13.272 B, a contraparte lógica desta função — "atualiza
o estado" em vez de "desenha") é a candidata natural de próximo
passe estrutural, pro par ficar completo.

## 35. `Main_FrameMove()` — passe estrutural — completa o par com `Main_FrameRender`, revela DOIS switches de estado (2026-10-17, Fase 3)

`Main_FrameMove()` (`0x2bbb74`, 13.272 B) — mesmo tratamento das
seções 32–34. Descida recursiva alcançou só **2.580 de ~3.318
instruções possíveis (78%)** — bem menos que as três anteriores,
porque esta função tem **duas tabelas de salto computadas**
(`addls pc,pc,rX,lsl#2`, mesma técnica da seção 32), ambas extraídas
à mão.

### 35.1 Switch externo: 9 casos, dispatch de "modo de jogo" (`0x2bc730`)

```c
r2 = (*g_gameMode) - 3;         // estados 3..11 (9 casos válidos)
if ((unsigned)r2 <= 8) goto table[r2]; else goto 0x2bc7cc;
```
Tabela (9 entradas, **7 endereços distintos** — 3 casos colapsam no
default `0x2bc7cc`):
```
0:0x2bc908  1:0x2bc928  2:0x2bc8dc  3:0x2bc7cc  4:0x2bc7cc
5:0x2bc7cc  6:0x2bc954  7:0x2bc8bc  8:0x2bc7b8
```
Poucos casos reais (6, fora o default) — compatível com um pequeno
conjunto de "modos de jogo" de alto nível (mapa mundi / batalha /
menu / loja / evento / carregando, por exemplo — não confirmado por
leitura de corpo).

### 35.2 Switch interno: 43 casos, aninhado dentro de um dos casos do switch externo (`0x2bd114`)

```c
ip = sp[0x28];                   // sub-estado, lido de um campo local
cmp ip, #0x2a;                     // 42 (43 casos válidos, 0..42)
addls pc, pc, ip, lsl #2;
```
Tabela (43 entradas, **32 endereços distintos** — 11 casos colapsam,
10 deles seguidos, `14..23`, no mesmo handler `0x2bd358`):
```
 0:0x2bd26c  1:0x2bd258  2:0x2bd244  3:0x2bd230  4:0x2bd21c  5:0x2bd208
 6:0x2bd1ec  7:0x2bd5cc  8:0x2bd5b8  9:0x2bd5a8 10:0x2bd594 11:0x2bd584
12:0x2bd570 13:0x2bd55c 14:0x2bd358 15:0x2bd358 16:0x2bd358 17:0x2bd358
18:0x2bd358 19:0x2bd358 20:0x2bd358 21:0x2bd358 22:0x2bd358 23:0x2bd358
24:0x2bd358 25:0x2bd53c 26:0x2bd6a0 27:0x2bd628 28:0x2bd604 29:0x2bd5e0
30:0x2bd518 31:0x2bd4a0 32:0x2bd458 33:0x2bef08 34:0x2bd360 35:0x2bd348
36:0x2bd414 37:0x2bd1c8 38:0x2bd308 39:0x2bd2c8 40:0x2bd294 41:0x2bd280
42:0x2bd280
```
O endereço do switch interno (`0x2bd1xx`) cai dentro do intervalo de
endereços alcançados pelo switch EXTERNO (seus casos ficam em
`0x2bc7xx`–`0x2bc9xx`, mas o código entre eles se estende até
`0x2bd1xx`+) — ou seja, **o switch de 43 casos vive dentro do corpo
de um dos 7 casos do switch de 9**, não é um segundo nível
independente. Qual caso exatamente, não confirmado sem ler os corpos.

### 35.3 Catálogo de sistemas tocados (116 `bl` resolvidos — o maior de toda a Fase 3)

- **`CINPUT_IF_TOUCH` — API de polling completa, nunca catalogada
  assim antes**: `GetPress`/`GetPressCount`/`GetDown`/`GetUp`/
  `GetRepeat`/`GetTouchPoint`/`GetGestureDoubleTap`/`GetEvent`/
  `GetTouchTime`/`GetGestureTap`/`GetGestureSwipe_Old`/
  `GetGesturePinch`/`BeginAll`/`EndAll`. As seções 20/26 já tinham
  lido `OnTouchesBegan`/`OnTouchesEnded` (os HANDLERS de evento);
  isto é a interface de **consulta** que a lógica de jogo usa pra
  perguntar "o dedo está apertado agora?" — confirma que são duas
  APIs complementares do mesmo subsistema de toque.
- **Plataforma Android direta**: `Android_Movie_Play(char const*,int)`/
  `Android_Vibrator_Vibrate()` — chamadas de plataforma nunca vistas
  antes (reprodução de vídeo full-motion e vibração háptica).
- **Gerente de tela, confirmando o padrão da seção 34.4**:
  `SettingsWnd_Init`/`FrameMove`/`Uninit` — o PAR de
  `Main_FrameMove`/`Main_FrameRender` delega pra sub-tela de
  configurações nos dois sentidos (atualiza E desenha).
- **Hit-testing de área de toque**: `SCREEN_TO_RENDER`/
  `IS_GAME_ROT_AREA`/`IS_GAME_MOV_AREA`/`IS_ICON_AREA`/`IS_GAME_AREA`/
  `IS_SETTINGS_WND_SLIDER_AREA` — confirma um conjunto de funções
  "o toque caiu dentro desta região retangular lógica?" usado pra
  rotear toques pra diferentes sistemas (rotação de câmera, movimento,
  ícones, slider de configurações).
- **Transição de modo real**: `onGotoNextMode(int)` — nome
  praticamente confirma que é a função que MUDA `*g_gameMode` (seção
  35.1), ainda que o corpo não tenha sido lido.
- **Save/arquivo**: `CFILE_DAT::Load`/`Unload`/`Decode`,
  `executeSaveFFT()`, `Savedata_LoadGameCleared`.
- **Infra de baixo nível**: `CWORK_MEM::Get`, `CTHREAD::Sync`,
  `timeGetTime()`, `CFRAMERATE::GetRate`, `CSTEP_BATCH::FrameMove`,
  `GuEmu_FrameMove()` — confirma que a emulação da GU (`GuEmu_*`, já
  vista em `GuEmu_libgu_to_gl`, seção 34.1 cita a contraparte de
  render) também tem seu próprio passo de "atualização" por frame.
- 6 chamadas locais sem símbolo.

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos dos 7 casos do switch externo e dos 32 do switch interno, a
localização exata de qual caso externo contém o switch interno, e o
papel preciso de `onGotoNextMode`. Marcada `read_structural` no
`RE_FUNCTION_INVENTORY.csv`. Com esta seção, o par
`Main_FrameMove`/`Main_FrameRender` — o loop principal do jogo
inteiro — tem agora pelo menos um passe estrutural completo dos dois
lados.

## 36. `BattleUnitList` — passe estrutural — revela uma família `b*` inteira de primitivas PS1 de batalha, nunca vista (2026-10-17, Fase 3)

`BattleUnitList(unsigned char*, unsigned long*)` (`0x17c27c`,
15.920 B) — mesmo tratamento das seções 32–35. Descida recursiva:
**3.618 de ~3.980 instruções possíveis (91%)**. Três tabelas de
salto computadas (`addls pc,pc,r0,lsl#2`), todas extraídas.

### 36.1 Três tabelas pequenas, todas sobre "qual região de toque foi tocada"

Cada tabela segue o padrão: `r0 = iOS_GetRectHitNo{Tap,Slide,Touch}()
- BASE; cmp r0,#N; addls pc,pc,r0,lsl#2`:

- **Tabela A** (`0x17e384`, base `0x43`=67, 7 casos): 4 dos 7 casos
  (`0,3,4,5`) caem no mesmo handler `0x17e3ac` — só 3 casos (1, 2, 6)
  têm handler próprio.
- **Tabela B** (`0x17e3bc`, base `0x4a`=74, 5 casos): 5 endereços
  todos distintos.
- **Tabela C** (`0x17f77c`, base `0x3c`=60, 7 casos): 4 dos 7
  (`0,3,5,6`) caem em `0x17f7ac` — só 3 casos (1, 2, 4) têm handler
  próprio.

Confirma que o menu de lista de unidades de batalha tem pelo menos
**19 regiões de toque identificadas por ID** (faixas `60–66`,
`67–73`, `74–78`), cada uma com dispatch próprio — consistente com
uma grade de botões/linhas (um por unidade do time, mais botões de
navegação/confirmação).

### 36.2 Achado maior: uma família `b*` inteira de primitivas de desenho PS1, nunca vista nesta investigação

Mais de 30 funções com prefixo `b` resolvidas por nome — um
subsistema de desenho 2D dedicado à tela de batalha, separado tanto
do `wld_*` do mapa mundi quanto do `CEGL2_*` moderno:

```
bSwapDB(int,int)              bDB_init(DB*, ...25 ponteiros de primitiva PS1...)
bSetFrameRate(int)            bChrSort(int)
bGetChrList / bGetSortCondition / bSetSortCondition / bSearchUnit
bDrawG4 / bDrawPluralFT4RGB / bDrawFT4RGB / bDrawFT4RGB2 / bDrawTexFlip
bGetFadeStatus / bFadeInInit / bFadeOutInit / bFadeIn / bFadeOut
bWaitLoadImage / bWaitStoreImage / bWorldJobStts
bMessageMake / bWindowDel / bDrawMessage / bHelpMessage / bRoundHelpMessage
bMenuSel2D / bGetMaskedPad
bWindowColorSet / bWindowPrioritySet / bSelectWindowClut / bDrawWindow2 / bGetWindowColor
```

**`bDB_init`** é a função mais reveladora: recebe ponteiros pra
**25 tipos de primitiva da lib gráfica do PS1** (`tagPOLY_F3/FT3/F4/
FT4/G3/GT3/G4/GT4`, `tagLINE_F2/F3/F4/G2/G3/G4`, `tagTILE/TILE_1/
TILE_8/TILE_16`, `tagSPRT/SPRT_8/SPRT_16`, `DR_MOVE/DR_AREA/DR_MODE`)
— **"DB" = Double Buffer**, termo clássico do PS1. Isto confirma um
**terceiro sistema de buffer de desenho**, nunca visto antes:
- `GsOT`/`GsSPRITE` — mapa mundi (seções 11, 12.5 etc.)
- `CEGL2_*` — motor moderno OpenGL ES (seções 13–15, 34)
- **`DB`/`b*` — buffer de primitivas PS1 cru, dedicado à UI 2D de
  batalha** (listas, janelas, mensagens, fade) — recém-descoberto

Reforçado por chamadas reais de baixo nível da lib PS1 nunca vistas
nesta função: `SetSprt`, `SetDrawMode`, `SetSemiTrans`,
`SetDefDispEnv`/`SetDefDrawEnv`, `xpSetDrawOffset`,
`xpLibgpuOffScreenRectGet` — **semi-transparência real** confirmada
(`SetSemiTrans`), nunca mencionada antes nesta investigação.

### 36.3 Outros sistemas confirmados

- **Sistema de tasks genérico** (`task_create(long,char*)`/
  `task_status(long)` ×11/`send_taskparamater`) — nome mais genérico
  que o `wasmTaskEntry` da seção 33; candidato a ser o sistema de
  tasks REAL subjacente (do qual "wasm" seria um wrapper), ou um
  terceiro sistema — não investigado a fundo.
- **Rede/link** (`pspNetSetPad`/`pspNetSetPadPushTiming`/
  `net_control_ex`/`pspNetGetErrorCode`) — resquício de suporte a
  cabo de link do PS1 original, nunca mencionado nesta investigação.
- **`iOSUnitList*`** (`OutWin`/`FlagGet`/`MoveFlagSet`/
  `MoveFlagReset`/`MoveFlagResetSTA`/`MovOtherCheck`/`WinOnOff`/
  `CurSave_W`/`AreaTapCheck`) — confirma uma API de UI dedicada e
  completa só pra esta lista de unidades, nunca catalogada.
- 8 chamadas locais sem símbolo.

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos dos handlers das 3 tabelas, e os corpos de qualquer uma das
~30 funções `b*` (todas só catalogadas por nome/assinatura via
`bl`/demangle, nenhuma lida por dentro). Marcada `read_structural`.
A família `b*` é candidata forte a abrir uma frente própria de
leitura na Fase 3 — é um sistema inteiro, não uma função isolada.

## 37. `mesputmain()` — passe estrutural — confirma que `W*`/sem-prefixo são duas variantes paralelas do MESMO sistema (2026-10-17, Fase 3)

`mesputmain()` (`0xe88c4`, 15.744 B) — mesmo tratamento das seções
32–36, e comparação direta com `Wmesputmain` (seção 33). Descida
recursiva: **3.884 de ~3.936 instruções possíveis (98%)**, sem tabela
de salto computada — mesma arquitetura de cascata de `cmp`/`beq`/
`bne` de `Wmesputmain` (377 branches aqui vs. 414 lá, bem próximo).

### 37.1 Achado principal: confirma a hipótese da seção 33 — é um par de variantes paralelas, não um sistema diferente

Comparando os 88 `bl` resolvidos aqui contra os 95 de `Wmesputmain`
(seção 33), a correspondência é **quase 1:1, função por função, só
sem o prefixo**:

| `Wmesputmain` (seção 33) | `mesputmain` (aqui) |
|---|---|
| `Wallocatewindow`/`Wdisposewindow` | `allocatewindow`/`disposewindow` |
| `Wallocatetexture`/`Wdisposetexture` | `allocatetexture`/`disposetexture` |
| `Wserchmessagepointer`/`Wgetvaluelength`/`Wcount_words2` | `serchmessagepointer`/`getvaluelength`/`count_words2` |
| `Wgetanimpos2d` | `getanimpos2d` |
| `Wmultiwindow_packetextend` | `multiwindow_packetextend` |
| `Wsettaskkind`/`Wtask_killmyself` | `settaskkind`/`task_killmyself` |
| `Wwrite_eventflag`/`Wread_eventflag`/`Wcnvglobaltolocalid` | `write_eventflag`/`read_eventflag`/`cnvglobaltolocalid` |
| `Wextend_windowframe` | `extend_windowframe` |
| `wasmTaskEntry`/`wasmGetInput1/2/3`/`wasmGetActiveTask` | `asmTaskEntry`/`asmGetInput1/2/3`/`asmGetActiveTask` (**uma letra menos**: "asm", não "wasm") |

Isto **fecha a pergunta em aberto da seção 33**: `W*`/sem-prefixo não
são sistemas diferentes — são **duas implementações paralelas do
mesmo código-fonte**, uma compilada com prefixo `W` e outra sem,
quase certamente **variante de texto largo/`wchar` (Shift-JIS,
japonês) vs. variante de texto de 1 byte (ASCII/ocidental)** — hipótese
reforçada por `CSTR_UTIL::GetName` já ter confirmado tratamento real
de multi-byte Shift-JIS (seção 30), e pelo próprio contador de
chamadas da função-helper local mais usada em cada versão ser
**idêntico** (`sub_fb7e0` ×19 em `Wmesputmain`, `sub_d3f44` ×19 aqui —
endereços diferentes, mesma contagem exata de chamadas, forte indício
de ser literalmente a mesma função-fonte compilada duas vezes). Essa
mesma duplicação `W`/sem-prefixo provavelmente explica também a
família `disp_personalwindow`/`Wdisp_personalwindow`/
`Adisp_personalwindow`/`Cdisp_personalwindow`/`Ddisp_personalwindow`/
`Edisp_personalwindow` do `RE_FUNCTION_INVENTORY.csv` — não
confirmado ainda, mas a hipótese generaliza bem.

### 37.2 Única chamada nova (não presente em `Wmesputmain`)

`getBattleWorkIDFromAnimation(unsigned int)` — liga o sistema de
mensagens à área de trabalho de animação de batalha (`BWORK`, já
citada na seção 12 do backlog original). Não estava em `Wmesputmain`.
Pode ser um ponto de divergência real entre as duas variantes, ou só
reaproveitamento de código diferente — não investigado a fundo.

**O que ficou sem confirmar**: a hipótese W=largo/sem-prefixo=byte
simples não foi confirmada lendo o corpo de nenhuma das duas; e,
exceto por `getBattleWorkIDFromAnimation`, não foi feita uma
comparação exaustiva instrução-a-instrução (só por nome de chamada)
entre as duas funções. Marcada `read_structural`.

## 38. `ASHURA_addPrim` — passe estrutural — confirma o motor 3D "ASHURA" como uma pilha de matrizes GTE real, com ray-picking e partículas (2026-10-17, Fase 3)

`ASHURA_addPrim(MATRIX*)` (`0x16a6a4`, 15.412 B) — mesmo tratamento
das seções 32–37. Primeira leitura do motor "ASHURA", descoberto por
nome na seção 32.3 (catálogo de `battle()`) mas nunca aberto. Descida
recursiva: **3.720 de ~3.853 instruções possíveis (97%)**, sem
tabela de salto computada. Catálogo mais curto de `bl` desta fase (47
distintos) — função mais matemática que orquestradora.

### 38.1 Confirma uma pilha de matrizes GTE real (hierarquia 3D de verdade)

```
PushMatrix / PopMatrix          — pilha real de transformação
RotMatrix / TransMatrix / ScaleMatrix / SetTransMatrix / SetRotMatrix
MulMatrix0 / MulMatrix2
SetLightMatrix / SetColorMatrix / SetBackColor
rsin
```
`PushMatrix`/`PopMatrix` nunca tinham aparecido nesta investigação —
confirma que o `ASHURA_addPrim` monta uma **hierarquia real de
transformações** (ex.: matriz do modelo → matriz de uma parte do
corpo → matriz de um efeito anexado), não só uma transformação plana
única. `SetLightMatrix`/`SetColorMatrix`/`SetBackColor` confirmam
**iluminação real via GTE** (não só cor fixa), capacidade nunca
catalogada byte a byte antes nesta investigação.

### 38.2 Achados novos: clipping, ray-picking, partículas

- **`GLIVON_FT4`/`GLIVON_FT3`/`GLIVON_F3`/`GLIVON_F4`** — nunca
  vistas; assinatura (ponteiro de primitiva + contagem + buffers de
  saída) é consistente com **clipping/recorte de polígono contra o
  volume de vista** antes do desenho (nome provável: "GL Interpolate
  Vertices ON" ou similar — não cravado).
- **`RayPick_GT4`/`RayPick_GT3`** — confirma **ray-picking real**
  contra polígonos texturizados com Gouraud — provável mecanismo de
  seleção de alvo/unidade em 3D via toque, nunca catalogado antes.
- **`ps_rand()` chamada 29 vezes** — de longe a chamada mais
  frequente desta função; consistente com geração de posições/
  variações aleatórias de partículas ou efeitos (faíscas, destroços),
  já que "addPrim" sugere adicionar primitivas de efeito ao OT.
- **`ASHURA_FALL(unsigned char)`** — nome sugere queda/gravidade de
  objeto (destroços, itens largados); **`ASURA_LMDL_TIME_TBL()`**
  tem o nome escrito **sem o H** (`ASURA`, não `ASHURA`) — inconsistência
  de nomenclatura real no binário, preservada tal como está, não
  corrigida (mesmo espírito de preservar nomes "estranhos" como
  "Iwasaki"/"SSD" já catalogado em seções anteriores).
- `VectorDataBase(unsigned int)`/`Vector_AffineTransform(int)` —
  confirma um pipeline de dados de vértice próprio do ASHURA, separado
  dos vértices do `wld_*`/`CEGL2_*`.
- Uso pesado de divisão inteira real (`__divsi3` ×14, `__aeabi_idivmod`
  ×11) — matemática de verdade, não só tabelas.

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos dos ~70+ blocos da cascata de branches (230 branches, 108
de retrocesso), a semântica exata de `GLIVON_*`, e o papel preciso de
`ASHURA_FALL`/`ASURA_LMDL_TIME_TBL`. Marcada `read_structural`. As
outras funções `ASHURA_*` já catalogadas por nome (`init`, `matrix`,
`getOTptrZ`, `clearOT`, `Exit` — seção 32.3) continuam não lidas.

## 39. `ItemMenu()` — passe estrutural — revela o sistema real de itens/equipamento e uma biblioteca completa de widgets de janela (2026-10-17, Fase 3)

`ItemMenu()` (`0x1aeda0`, 13.764 B) — mesmo tratamento das seções
32–38, com uma ressalva de honestidade: a descida recursiva simples
só alcançou **313 de ~3.441 instruções (9%)** por causa de uma
tabela de salto computada logo no início (`addls pc,pc,r3,lsl#2` em
`0x1aeed0`, 4 casos). Tentei automatizar a extração de tabelas em
cascata (`struct_pass2.py`, novo) e ela **gerou 3 falsos positivos**
(endereços que não eram tabelas de verdade — ficam registrados como
lição, não como achado). Extraindo só a tabela real à mão (4 casos:
`0x1af7f4`/`0x1af310`/`0x1aefdc`/`0x1af364`, todos distintos) e
semeando a descida recursiva com eles, a cobertura sobe pra **3.269
de 3.441 (95%)** — o resto do passe usa esse número.

### 39.1 Achado maior: o sistema real de itens/equipamento, nunca catalogado byte a byte

```
GetItemParameter(short, A_STTS*, C_STTS*, int)   GetItemList(short, short, signed char, short*, unsigned short, unsigned char)
GetTotalEquipItem(short) / GetTotalItem(short)     ItemEquip(short, short, short) / ItemChg(short, int)
Equip() / AutoEquip()                                 ChrPowerCompare(C_STTS*, A_STTS*, short*, short*)
GetSortCondition/SetSortCondition(int, short*)        SetItemUserSort / RefleshItemUserSort(int)
pspItemGetCommonData / pspItemGetEquipBonus / pspItemIsBarehand / pspItemGetWeaponData / pspItemIsType
```
Confirma, com nomes reais, toda a cadeia "ver lista de itens → trocar
equipamento → comparar poder antes/depois → auto-equipar" — e a
camada `psp*` (já vista em `wldpad_read`/`CAUTOSAVE`/`pspWorldCheckFlg`,
seções 12.2/19.1/12.12) tem sua própria API de **dados de item**
(`pspItemGetCommonData`/`pspItemIsBarehand`/`pspItemGetWeaponData`/
`pspItemIsType`), nunca catalogada antes.

### 39.2 Achado maior: biblioteca de widgets de janela/menu completa, compartilhada

Dezenas de funções de UI genérica (não específicas de item), que
provavelmente sustentam MUITOS menus do jogo, não só este:
```
WindowInit/WindowInit2 / ScrollWindowInit / CursolFunc
SetMenuSelVertical/SetMenuSelSide (+ "WithSnd"/"WithSndDirect")
SetBitStream/SetBitStream2 / GetBitStream/GetBitStream2
SetWindowPosition/GetWindowPosition / SetWindowCount/GetWindowCount
DrawWindow2 / WindowPrioritySet / WindowDel / WindowPositionInit
```
`SetBitStream`/`GetBitStream` (e as variantes `2`) são achado novo —
sugerem que o estado de seleção de menu é empacotado/lido via um
stream de bits genérico, não campos soltos.

### 39.3 `iOS_CMenuTouch` — superfície mais completa vista até aqui

Além de `init`/`exec`/`setYLine`/`setDispAssist` (já conhecidas das
seções 33/37), aparecem `setDispOffset`, `setDisableHeightAdjust`,
`drawMenuAssist`, `setLRCurEffect`, `isTaped` — confirma que esta
classe C++ de menu por toque é bem mais rica do que as leituras
anteriores sugeriam.

### 39.4 Outros achados

- **Família de tasks `W*`** (`Wtask_create`/`Wtask_start`/
  `Wtask_stop`/`Wtask_status`/`Wsend_taskparamater`) — confirma que
  `ItemMenu` usa especificamente a variante **`W`** do sistema de
  tasks (seções 33/37), não a variante sem prefixo.
- `DrawFT4RGB` chamada 11 vezes — desenho 2D pesado, mesma família já
  vista em `BattleUnitList` (seção 36, lá como `bDrawFT4RGB`) —
  reforça que o prefixo `b` daquela seção é específico de batalha, e
  este menu usa a versão sem prefixo (mundo/geral).
- 1 chamada local sem símbolo relevante (as demais ~dezenas de
  `sub_*` detectadas na tentativa de auto-extração de tabela foram
  descartadas junto com os falsos positivos — não confiáveis).

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos dos 4 casos da tabela real e do resto da cascata de 249
branches. Verificação extra confirmou que **não há mais nenhuma
tabela de salto computada real** nos 95% alcançados — as 3 "tabelas"
que a tentativa automatizada (`struct_pass2.py`) achou eram falso
positivo do detector, não trabalho pendente real. Marcada
`read_structural`.

## 40. `eItemMenu()` — passe estrutural — terceira cópia paralela do mesmo padrão, e correção importante da hipótese das seções 33/37 (2026-10-17, Fase 3)

`eItemMenu()` (`0x18aeec`, 12.580 B) — mesmo tratamento das seções
32–39. Descida recursiva simples já alcança **2.993 de ~3.145
instruções possíveis (95%)**, sem necessidade de extrair tabela à
mão desta vez.

### 40.1 Confirma duplicação sistemática — mas **corrige** a hipótese "W = idioma largo"

Os 83 `bl` resolvidos aqui são, de novo, quase 1:1 com os de
`ItemMenu` (seção 39), agora com prefixo **`e`**: `eItemChg`,
`eGetSortCondition`/`eSetSortCondition`/`eSetItemUserSort`,
`eGetItemParameter`, `eChrPowerCompare`, `eGetItemList`,
`eItemEquip`, `eDrawFT4RGB`/`eDrawTexFlip`, `eSetSttsA/Para/Equ/Para2`,
`eCurChrChg`, `equans_init` (contraparte de `unitans_init`),
`eSetWindowPosition`/`eGetWindowPosition`, `eMessageMake`/
`eWindowDel`/`eDrawMessage`, `eSetMenuSelVertical`/`eGetMenuSelVertical`/
`eSetMenuSelSide` (+ `WithSnd`), `eSetBitStream`/`eGetBitStream` (+`2`),
`eWindowInit`/`eWindowInit2`/`eDrawWindow`/`eDrawWindow2`,
`eCursolFunc`, `eWindowPrioritySet`, `eSetWindowCount`,
`eGetWindowColor`.

**Mas a família de tasks aqui é a variante SEM prefixo**
(`task_create`/`task_start`/`task_stop`/`task_status`/
`send_taskparamater`, sem `W` nem `e`) — diferente de `ItemMenu`
(seção 39), que usava a variante `W` dos tasks. Isso **não bate** com
a hipótese "cada tela usa consistentemente sua própria variante de
TUDO" nem com "W = idioma". **Correção honesta da seção 37**: o
padrão real parece ser **duplicação por TELA/CONTEXTO de UI**
(cada menu de alto nível — lista de item, equipar item, lista de
unidade de batalha — tem sua própria cópia quase idêntica das
funções de janela/menu, com um prefixo próprio: nenhum, `W`, `e`,
`b`...), e não necessariamente ligada a idioma/charset. A
duplicação do sistema de TASK é independente disso (`ItemMenu` usa
tasks `W`, `eItemMenu` usa tasks sem prefixo, `Wmesputmain`/
`mesputmain` usam `wasm`/`asm`) — são dois eixos de variação
diferentes, não um só. A hipótese Shift-JIS da seção 37 fica
**reclassificada como não confirmada / provavelmente não é a
explicação completa**, mantida ali só com esta nota de correção.

### 40.2 Confirmação independente via sufixo `_equip`

`iOS_getOt_equip`/`iOS_getOtNum_equip`/
`iOS_setDispCursor_window_equip`/`iOS_getMaxLineWindowEquip`/
`iOS_getScrollType_equip` — mesmo padrão de sufixo já visto como
`_unitlist` em `ItemMenu`/`BattleUnitList` (seções 36/39). Confirma,
por uma convenção de nome totalmente diferente (sufixo em vez de
prefixo, numa família `iOS_*` separada), que `eItemMenu` é
genuinamente a **tela de equipar item**, uma tela distinta de
`ItemMenu` (provável "ver/usar item"), não uma mera variante de
idioma da mesma tela.

**O que ficou sem confirmar**: os corpos da cascata de 239 branches
(120 de retrocesso), e a causa raiz exata de cada família de prefixo
(continua sem leitura de corpo que confirme "por que" cada uma
existe). Marcada `read_structural`.

## 41. `op_attackteam()` — passe estrutural — o opcode de bytecode que monta o time de ataque, com suporte a batalha em rede (2026-10-17, Fase 3)

`op_attackteam()` (`0xc5148`, 12.272 B) — mesmo tratamento das
seções 32–40. Descida recursiva: **2.753 de ~3.068 instruções
possíveis (90%)**. Três tabelas de salto pequenas (5, 4 e 4 casos,
todas com entradas distintas), extraídas à mão:

```
T1 (0xc5880, base: iOS_getV2Icon(0x37)-1, 5 casos):
  0xc5c14  0xc5b68  0xc5c54  0xc5bc4  0xc589c
T2 (0xc5fb4, base: iOS_GetRectHitNoSlide()+1, 4 casos):
  0xc6bc4  0xc6bb4  0xc6b4c  0xc6a94
T3 (0xc67d4, base: campo local sp+0x18, 4 casos):
  0xc6dfc  0xc6de8  0xc6dd4  0xc6dc0
```
**Correção (2026-10-17, mesma sessão, após validar a ferramenta
`jtable.py` contra `battle()`)**: os três endereços acima substituem
os publicados na primeira passada desta seção — a extração manual
original usava `endereço_do_addls + 4` como início da tabela; o
correto é `+ 8` (regra do pipeline ARM: `PC` no momento da execução
do `addls` já vale `endereço+8`). O erro deslocava a tabela em uma
posição, fazendo o endereço do caso "else"/default (o `b` que vem
logo depois do `addls`, fora da tabela) aparecer como se fosse o
primeiro caso, e perdendo o último caso real. Achado qualitativo
(3 tabelas pequenas, contagens de caso) não muda.

### 41.1 Confirma o nome: monta o time de ataque antes da batalha, com suporte real a batalha em rede

Nome de opcode já sugeria o papel (consistente com a arquitetura de
bytecode das seções 9.5–9.6: `op_*` = handler de instrução do
interpretador de eventos). Confirmado por chamada: `changeflame(int)`,
`finishAttackTeamSelect()`, `iOS_ResumeAfterAttackTeam()` — é
literalmente a tela "escolha seu time de ataque" antes de entrar na
batalha. Achado maior: **suporte real a modo de rede/multiplayer**,
nunca confirmado com esta clareza antes:
```
pspBattleCheckFlg(unsigned int)
pspBattleEntryAreaInit() / pspBattleEntryAreaMake(int, int)
pspNetGetBattleModeFlag()
get_parent_child()
pspNetGetErrorCode()
```
`pspNetGetBattleModeFlag` sendo consultada aqui, numa tela de seleção
de time, é forte evidência de que o jogo testa ativamente se a
batalha é **em rede** (cabo de link do PS1 original, remanescente já
suspeitado nas seções 36/39) antes de decidir como montar as áreas de
entrada do time.

### 41.2 Confirma a ponte bytecode↔task, suspeitada desde a seção 33

`task_create`/`task_wait`/`wait_taskend`/`task_killmyself`/
`send_taskparamater`/`asmTaskEntry` (as variantes sem prefixo e
`asm`) — confirma que um opcode do interpretador de bytecode de
eventos **cria e espera uma task cooperativa de verdade** pra deixar
o jogador escolher o time, em vez de implementar a UI inline no
próprio laço de bytecode. Fecha, com instrução real, a ponte entre o
motor de eventos (seções 9.5–9.6) e o sistema de tasks (seções 33/37/
40) — suspeitada, nunca confirmada byte a byte antes.

### 41.3 Família `iOS_GetRectHitNoTouch*` mais completa vista até aqui

`iOS_GetRectHitNoTap`/`NoTouch`/`NoSlide`/`NoTouchTrg`/`NoTouchOld`/
`NoTouchDirect(int,int)` — 6 variantes, mais do que qualquer leitura
anterior catalogou junto.

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos dos 13 casos das 3 tabelas e do resto da cascata de 294
branches (160 de retrocesso); e o papel exato de `changeflame`
(provável erro de digitação de "changeframe" preservado no binário,
não corrigido). Marcada `read_structural`.

## 42. `CardAccess(int)` — passe estrutural — revela o sistema REAL de save/load, com suporte a iCloud (2026-10-17, Fase 3)

`CardAccess(int)` (`0x184670`, 11.004 B) — mesmo tratamento das
seções 32–41. Descida recursiva: **2.504 de ~2.751 instruções
possíveis (91%)**, sem tabela de salto computada.

### 42.1 Confirma o papel real do nome "Card" — tela de gerência de memory card / save-load

"Card" não era um sistema novo misterioso — é o nome herdado do
**memory card do PS1**. 95 `bl` resolvidos confirmam, com nomes reais
nunca catalogados antes, a tela completa de save/load:
```
SelectCard(int) / CardInit() / CardSetUp() / CardEventClose()
GetCardState() / Wait_GetCardState(int)
MakeSaveData(int) / SetLoadData(int) / GetSaveDataInit()
pspSaveInit() / pspSaveUpdate() / pspSaveExit()
pspIsNoneSaveData(int) / pspFftSave(int, FFT_SAVE_DATA*, int*)
pspFftLoad(int, FFT_SAVE_DATA*, int*, int)
pspSaveDataGetOne(int, FFT_SAVE_DATA*) / pspSaveDelete() / pspLoadSystemFile()
iOS_fftSave() / iOS_dispOkNg(int, int)
```
Isto é um sistema **categoricamente diferente** de `CAUTOSAVE::Save`
(seção 19.1, que despeja a heap inteira pra disco) — aqui há uma API
de save/load estruturada de verdade, com slots (`pspSaveDataGetOne`),
tipo de dado próprio (`FFT_SAVE_DATA*`), e um fluxo de confirmação
(`iOS_dispOkNg` = diálogo Sim/Não).

### 42.2 Achado novo: suporte real a iCloud

**`iCloud_GetSlotCount()`** — nunca mencionada nesta investigação.
Confirma que o port iOS integra sincronização de save via iCloud,
pelo menos no nível de contar slots disponíveis. Candidato de alto
valor pra uma leitura futura (`iCloud_*` é quase certamente uma
família pequena, vale varrer por nome no `.dynsym`).

### 42.3 Confirma o sistema `DB`/primitivas PS1 fora de batalha

`SwapDB(int,int)`/`DB_init(DB*, ...25 ponteiros de primitiva...)` —
**mesma arquitetura `b*` da seção 36 (`bSwapDB`/`bDB_init`), mas sem
o prefixo `b`** — confirma que o sistema de buffer de primitivas PS1
não é exclusivo de batalha; é usado aqui pra desenhar a tela de
save/load. Reforça a leitura das seções 39/40: o prefixo (`b`, `e`,
`W`, nenhum) parece mesmo ser **por tela/contexto**, não por
sistema.

### 42.4 Outros achados

- **`iOS_CMenuTouchSaveLoad`** (`setYLine`/`exec`/`init`) — uma
  **classe C++ própria**, não só um prefixo de função, dedicada ao
  menu de toque desta tela — mostra que a duplicação por tela às
  vezes vai até o nível de classe inteira, não só função solta.
- Confirma mais uma vez `DrawMessage`/`DrawMessageFast`/
  `DrawMessageKill`/`DrawMessageKillFast` — variante "Fast" nunca
  catalogada antes nas famílias de mensagem já vistas.
- `worldmap_restart()`/`load_worldname()` — liga esta tela a voltar
  pro mapa mundi depois de carregar (ou reiniciar) um save.

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos da cascata de 277 branches (142 de retrocesso); e a
família `iCloud_*` completa (só uma função vista). Marcada
`read_structural`.

## 43. `requireprinf()` — passe estrutural — confirma o julgamento de batalha em rede e um sistema "binpack" de dados de batalha (2026-10-17, Fase 3)

`requireprinf()` (`0x1506ec`, 10.976 B, nome não decifrável por
etimologia — tratado como está, sem forçar significado, mesmo
espírito de `ASURA_LMDL_TIME_TBL`) — mesmo tratamento das seções
32–42. Descida recursiva: **2.513 de ~2.744 instruções possíveis
(91%)**, sem tabela de salto computada.

### 43.1 Confirma o cluster de configuração de batalha (liga com `op_attackteam`, seção 41)

Mistura os mesmos dois grupos já vistos em `op_attackteam`
(helpers de bytecode/mensagem sem prefixo — `serchmessagepointer`,
`count_words2`, `checkpara1`, `settaskkind`, `read_eventflag` — e a
família de tasks sem prefixo — `task_create`/`wait_taskend`/
`asmTaskEntry`) com funções específicas de configuração de unidades
de batalha nunca vistas: `get_bwp(int)` (ponteiro de `BWORK`, a área
de trabalho de batalha já citada desde a seção 12 do backlog
original), `search_controlID`, `get_unitwork_add`, `erase_unit`,
`get_jobdata`, `resist_savedata(BWORK*, int)`,
`getAnimationIDFormBattleWork`.

### 43.2 Achado maior: confirma o julgamento de batalha em rede

**`NetBattleJudge()`/`getNetBattleJudge()`** — nunca vistas antes,
ligam diretamente com o suporte a batalha em rede já confirmado em
`op_attackteam` (seção 41, `pspNetGetBattleModeFlag`/
`pspBattleCheckFlg`, ambas chamadas aqui de novo). Confirma que o
jogo tem lógica real de **determinar o resultado/vencedor** de uma
batalha em rede, não só de configurar a entrada. `CalcMissionPayPoint`
e `pspBattleForceParticipationExit` (participação forçada — unidades
obrigatórias numa missão de história) completam o quadro de
configuração/conclusão de uma batalha.

### 43.3 Achado novo: sistema "binpack" de dados binários de batalha

`__bpInitBinpackData`/`__bpGetBinaryData` (mais `addbpitem` já visto
antes do início da função) — nome sugere um formato de **dados
binários empacotados** (binpack) específico de batalha — carregado
via `numa_fileReadCD` (mais um resquício "Cd"=CD-ROM do PS1 original,
igual a `wldCdRead` da seção 11.2), `mallocForFile`/`fileDispose`. Não
investigado o formato exato.

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos da cascata de 192 branches (100 de retrocesso); o formato
"binpack"; e a etimologia de `requireprinf`. Marcada `read_structural`.

## 44. `CreateObjectWithTable` — passe estrutural — o gerador de partículas/efeitos do motor, cobertura quase total (2026-10-17, Fase 3)

`CreateObjectWithTable(short, int, int, _Object*)` (`0x225ac8`,
10.724 B) — mesmo tratamento das seções 32–43. Descida recursiva:
**2.673 de ~2.681 instruções possíveis (99,7%)** — a cobertura mais
alta de toda a Fase 3 até aqui, sem tabela de salto computada.
Catálogo de `bl` bem menor (21 distintos) que o normal — função
dominada por aritmética, não orquestração.

### 44.1 Confirma ser o gerador real de partículas/efeitos variados do motor

```
getVariationData(int,int,int) ×32      getVariationAppearPosition(_ParticleParameter*, int, VECTOR*)
getVariationAppearRange(...)            getVariationAppearVec(...)
ChangeEffectAnimation(effectAnimation*, uchar, short)
GetAnimationPosition(int,int,EffectOrder*,SVECTOR*)
NewObject(short,short)                  getAbsoluteMaximumOf3(short,short,short)
AddSVECTORToVECTOR / RotMatrix / SetRotMatrix / SetTransMatrix / RotTrans / VectorNormal
```
O tipo `_ParticleParameter*` confirma, com nome real, um sistema de
**parâmetros de variação de partícula** (posição/alcance/vetor de
aparecimento) — "WithTable" no nome da função bate exatamente: cria
um objeto de efeito usando uma tabela de parâmetros de variação. Usa
a mesma matemática GTE real já confirmada em `ASHURA_addPrim`
(seção 38: `RotMatrix`/`SetRotMatrix`/`RotTrans`), reforçando que é
parte do mesmo motor de efeitos 3D.

### 44.2 Achado numérico: a função mais dominada por aleatoriedade de toda a investigação

**`ps_rand()` chamada 103 vezes** — de longe o maior número desta
investigação inteira (a 2ª colocada, `ASHURA_addPrim`, teve 29).
Junto com `__aeabi_idivmod` (101 chamadas, quase sempre pra mapear o
resultado de `ps_rand()` pra um intervalo via módulo), confirma que
esta função gera posições/vetores/variações **aleatórios de verdade**
em massa — consistente com efeitos de partículas clássicos (faíscas,
destroços, magia) precisando de variação visual por instância.

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos da cascata de 278 branches (156 de retrocesso) — a fórmula
exata de cada variação (posição/alcance/vetor) não foi lida byte a
byte, só confirmada a existência e os nomes reais. Marcada
`read_structural`.

## 45. `BattleCardAccess(int)` — passe estrutural — quarta cópia paralela confirmada, agora com prefixo `c`, e o formato de cabeçalho de save real (2026-10-17, Fase 3)

`BattleCardAccess(int)` (`0x16fc90`, 10.448 B) — mesmo tratamento das
seções 32–44. Descida recursiva simples alcança 2.357 de ~2.612
instruções (90%); três tabelas de salto pequenas (5, 13 e 4 casos)
extraídas à mão, cobrindo o resto.

### 45.1 Confirma a tela de save/load acessível DE DENTRO da batalha — quarta cópia paralela do padrão

Os 87 `bl` resolvidos são, de novo, quase todos os mesmos de
`CardAccess` (seção 42), agora com prefixo **`c`**: `cSelectCard`,
`cCardEventClose`, `cCardInit`, `cGetCardState`, `cCardSetUp`,
`cSwapDB`/`cDB_init`, `cDrawTile`/`cDrawFT4RGB`/`cDrawTexFlip`,
`cFadeInInit`/`cFadeOutInit`/`cFadeIn`/`cFadeOut`,
`cWaitLoadImage`/`cWaitStoreImage`, `cDrawMessageKill(Fast)`/
`cDrawMessage(Fast)`, `cSetBitStream`/`cSetBitStream2`/
`cWriteBitStream`/`cGetBitStream2`, `cMakeWindowFunc`, `cValueFunc`,
`cCursolFunc`, `cWindowPrioritySet`, `cSelectWindowClut`,
`cGetWindowColor`. **Quarta letra de prefixo confirmada** depois de
`b` (seção 36), `e` (seção 40) e nenhuma (seção 42/39) — reforça a
leitura das seções 40/42: parece ser uma sequência de cópias quase
idênticas por tela/contexto (`A`/`b`/`C`/`c`/`D`/`e`/`E`/`W`... — o
`RE_FUNCTION_INVENTORY.csv` já lista a família `disp_personalwindow`
com várias dessas letras), não uma distinção de idioma.

### 45.2 Achado novo: formato real de cabeçalho de save (herança de memory card)

**`MakeHeader(int, int, CARD_HEADER*)`** — tipo `CARD_HEADER*` nunca
visto, confirma que o save tem um cabeçalho estruturado de verdade
(herança direta do formato de memory card do PS1, consistente com o
nome "Card" das seções 42/45). Mais achados do sistema de save nunca
vistos na seção 42: `pspSaveDataMissionRateSave(FFT_SAVE_DATA*)`
(taxa de conclusão de missões é salva!), `pspSaveDataEnableSystemFlg`/
`pspSaveDataCheckSystemFlg(FFTPSP_SYSTEM_FLG)`, `pspSaveSystemFile()`.
`iCloud_GetSlotCount()` reaparece aqui também — confirma que o
suporte a iCloud (seção 42) vale pra esta tela também, não é
exclusivo da tela de save do menu principal.

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos das 3 tabelas (22 casos no total) e do resto da cascata de
197 branches; o layout exato de `CARD_HEADER`. Marcada
`read_structural`.

## 46. `disp_personalwindow()` — passe estrutural — a janela de status pessoal real, com texto kanji e sombreamento PS1 de verdade (2026-10-17, Fase 3)

`disp_personalwindow()` (`0x128ed4`, 8.756 B, a maior das 6 variantes
`disp_personalwindow`/`Wdisp_`/`Adisp_`/`Cdisp_`/`Ddisp_`/
`Edisp_personalwindow` listadas no inventário) — mesmo tratamento
das seções 32–45. Descida recursiva: **2.135 de ~2.189 instruções
possíveis (97%)**, sem tabela de salto computada.

### 46.1 Confirma a janela de status pessoal, com texto kanji real

```
statusfigprint(int,int,char*,COPYFIELD*)     valueput(char*,VALUERECORD*,COPYFIELD*,int)
statuskanjiprint(int,char*,COPYFIELD*)          statuskanjiprintwithptr(char*,COPYFIELD*,char*)
addstatusback/sttsback_normal/sttsback_blue/initstatusback(...STTSWINDOWBACK*)
bgput(tagPOLY_FT4*,RECT16*,RECT16*,BGRECORD*)
addlocalprim/initpolyft4/initsprtfield
```
**`statuskanjiprint`/`statuskanjiprintwithptr`** confirmam, com nomes
reais, impressão de texto **kanji** nesta janela — reforça o
tratamento Shift-JIS real já visto em `CSTR_UTIL::GetName` (seção
30), agora na própria camada de desenho da UI, não só no utilitário
de string. `addstatusback`/`sttsback_normal`/`sttsback_blue` sugerem
pelo menos 2 esquemas de cor de fundo pro painel de status (normal
vs. azul — provável distinção de time aliado/inimigo ou estado
normal/alterado).

### 46.2 Confirma desenho direto com GPU PS1 real, incluindo sombreamento

```
SetPolyG4 / SetDrawOffset / SetDrawMode / SetSemiTrans / SetShadeTex / GetClut
```
**`SetShadeTex`** nunca vista antes nesta investigação — confirma
**sombreamento (shading) real** sobre textura via GTE, além da
semi-transparência já confirmada na seção 36. Este painel desenha
com primitivas PS1 cruas (`addlocalprim`/`initpolyft4`), não via
`DB`/`b*` (seção 36) nem `CEGL2_*` — um **quarto caminho de desenho**
catalogado nesta investigação (mapa mundi `GsOT`, moderno `CEGL2_*`,
buffer `DB` de UI de batalha/save, e agora este caminho mais direto
de primitivas soltas).

### 46.3 Confirma uma máquina de fases pra animação da janela

`iOSdisp_personalWinPhase()`/`iOSdisp_personalWinPhaseSet(int)`/
`iOSPersonalWinPosSet(int)` — confirma que a janela tem fases
numeradas (provável abrir/mostrar/fechar, no espírito do contador de
8 passos de `wld_window`, seção 12.11, mas pra este painel
específico). `iOSUnitListAddGet()` chamada **22 vezes** — maior
contagem desta função, sugere iteração pesada sobre a lista de
unidades pra montar o conteúdo exibido.

**O que ficou sem confirmar (nível "passe estrutural" intencional)**:
os corpos da cascata de 133 branches (72 de retrocesso); as outras 5
variantes de letra (`W`/`A`/`C`/`D`/`E`) continuam só no inventário,
não lidas. Marcada `read_structural`.

## 47. `Wdisp_personalwindow()` — passe estrutural — confirma a cópia 1:1 com `disp_personalwindow`, e uma correlação real entre prefixo `W` e task `wasm` (2026-10-17, Fase 3)

`Wdisp_personalwindow()` (`0x12f2f0`, 8.632 B) — mesmo tratamento das
seções 32–46, comparação direta com `disp_personalwindow` (seção 46).
Descida recursiva: **2.102 de ~2.158 instruções possíveis (97%)**,
sem tabela de salto computada.

### 47.1 Confirma, função por função, a cópia 1:1 já esperada

Os 53 `bl` resolvidos batem exatamente com os de `disp_personalwindow`
(seção 46), cada um com `W`: `Waddlocalprim`, `Winitpolyft4`,
`Winitsprtfield`, `Wdisposetexture`, `Waddstatusback`/
`Wsttsback_normal`/`Winitstatusback`/`Wsttsback_blue`,
`Wallocatetextureconst`, `Wchecktaskkind`/`Wsettaskkind`,
`Wloadcdst`, `Winitdrmode`, `Wbgput`, `Wstatusfigprint`/`Wvalueput`/
`WiOS_valueput_FT4`/`Wstatuskanjiprint`/`Wstatuskanjiprintwithptr`.
**As chamadas de "cola" compartilhada são literalmente os MESMOS
endereços** (`iOSdisp_personalWinPhase`/`PhaseSet`/
`iOSPersonalWinPosSet`/`iOSUnitListAddGet`, ×22 de novo) — confirma
que as duas funções são, de fato, cópias quase idênticas do mesmo
código-fonte, compartilhando a MESMA camada de estado/cola, só com
cópias PRÓPRIAS dos helpers de desenho/texto de baixo nível.

### 47.2 Achado que **restaura, só pra esta família**, uma correlação real `W`/task

Diferente do caso `ItemMenu`/`eItemMenu` (seção 40, que quebrou a
correlação), aqui ela **se confirma**: `disp_personalwindow` (seção
46) usa a família de tasks `asm` (`asmTaskEntry`/`asmGetInput3`/
`asmSerchMessagePointer`); `Wdisp_personalwindow` usa exatamente a
`wasm` (`wasmTaskEntry`/`wasmGetInput3`/`wasmSerchMessagePointer`) —
**a mesma correlação de `Wmesputmain`/`mesputmain`** (seções 33/37).
Conclusão honesta, juntando com a seção 40: a correlação `W`↔`wasm`
**existe e é real pra algumas famílias** (mensagens, janela pessoal),
mas **não é universal** (`ItemMenu` usa tasks `W` com helpers sem
prefixo; `eItemMenu` usa tasks sem prefixo com helpers `e`) — o
sistema de duplicação por tela não segue uma regra única em todo o
binário.

**O que ficou sem confirmar**: os corpos da cascata de 128 branches
(70 de retrocesso); as 4 variantes restantes (`A`/`C`/`D`/`E`).
Marcada `read_structural`.

## 48. `Mdl0024` — passe estrutural — primeira da família `Mdl*`, fecha o ciclo com ASHURA e o gerador de partículas (2026-10-17, Fase 3)

`Mdl0024(short, int, int, int)` (`0x23e29c`, 8.616 B) — primeira
leitura da família `Mdl0001`–`Mdl0028`+ (pelo menos 11 símbolos
vistos no inventário: `Mdl0001`–`Mdl0004`, `Mdl0007`, `Mdl0009`,
`Mdl0010`, `Mdl0013`, `Mdl0015`, `Mdl0017`, `Mdl0024`, `Mdl0028`).
Mesmo tratamento das seções 32–47. Descida recursiva: **2.142 de
~2.154 instruções possíveis (99,4%)**, sem tabela de salto
computada. Catálogo de `bl` minúsculo (15 distintos) — função
dominada por matemática 3D, não orquestração.

### Fecha o ciclo com dois sistemas já documentados

```
ASHURA_getOTptrZ(int)                        — motor 3D "ASHURA" (seção 38)
getVariationData / getVariationAppearPosition  — gerador de partículas (seção 44)
GetAnimationPosition / getOffsetAnimationPosition
rsin / rcos / SetRotMatrix / SetTransMatrix / RotTrans   — GTE real (seções 38/44)
AddPrim / SetPolyGT4
Malloc(unsigned long, long) / Free(void*)
```
Confirma, com instrução real, que a família `Mdl*` é o conjunto de
**rotinas de desenho de efeito/animação numeradas individualmente**
(uma por modelo de efeito — provavelmente golpes/magias específicas
do jogo), construídas diretamente sobre o motor `ASHURA` (seção 38)
e o gerador de variação de partículas (`CreateObjectWithTable`,
seção 44) — não um sistema à parte, é o **consumidor direto** dos
dois. `Malloc`/`Free` (sem prefixo `xp`) confirmam alocação dinâmica
real dentro da própria rotina de efeito, não só buffers estáticos.

**O que ficou sem confirmar**: os corpos da cascata de 47 branches
(19 de retrocesso); e por que especificamente o modelo `24` (qual
efeito de jogo corresponde a este número) — nenhuma tabela de nomes
encontrada ainda. As outras ~10 funções `Mdl*` já catalogadas por
nome continuam não lidas; dado que compartilham a mesma arquitetura,
uma leitura futura pode ser mais rápida por comparação direta (como
já feito pras famílias `W`/`e`/`c`/`b`). Marcada `read_structural`.

## 49. `Ddisp_personalwindow()` — passe estrutural — revela que nem toda duplicação por letra é uma cópia completa (2026-10-17, Fase 3)

`Ddisp_personalwindow()` (`0xce834`, 7.912 B) — mais uma variante da
família `disp_personalwindow` (seções 46/47). Descida recursiva:
**1.927 de ~1.978 instruções possíveis (97%)**, sem tabela de salto
computada.

### Correção/refinamento importante: `D` não duplica os helpers, só reusa os de `disp_personalwindow`

Diferente de `Wdisp_personalwindow` (seção 47, que tinha SUAS
PRÓPRIAS cópias `W`-prefixadas de `addlocalprim`/`statuskanjiprint`/
etc.), `Ddisp_personalwindow` chama os **MESMOS endereços sem
prefixo** de `disp_personalwindow` (seção 46) — `addlocalprim`
(`0xd665c`), `statusfigprint` (`0xe1db8`), `statuskanjiprint`
(`0xe2b78`), todos idênticos. **Não há uma cópia `D`-prefixada dos
helpers de desenho** — só a função de entrada (`Ddisp_personalwindow`
em si) é duplicada; o trabalho pesado de desenho é **compartilhado**
com a versão sem prefixo. Isto refina a leitura das seções 39/40/42/
45/47: a duplicação por letra **não é uniforme** — `W` parece ser
uma cópia de verdade (fonte compilada duas vezes), enquanto `D` (e
provavelmente `A`/`C`/`E`, ainda não lidas) parecem ser só **pontos
de entrada alternativos** pro mesmo código de desenho, talvez
chamados de contextos diferentes do jogo (ex.: unidade viva vs.
morta, time aliado vs. inimigo — hipótese, não confirmada).

Achado novo: `iOS_setTransFaceForChrRemove(int)` (sugere remoção de
personagem do time) e `CFFT_STATE::AttackTeamFaceIDToFaceID` (mesma
função confirmada na seção 22.5, reaparecendo aqui).

**O que ficou sem confirmar**: os corpos da cascata de 117 branches
(58 de retrocesso); e o contexto exato em que `D` é chamada vs. a
versão sem prefixo (hipótese de "remoção de personagem" não
confirmada). Marcada `read_structural`.

## 50. `Edisp_personalwindow()` — passe estrutural — segunda confirmação do padrão "entrada fina" da seção 49 (2026-10-17, Fase 3)

`Edisp_personalwindow()` (`0x11f848`, 7.888 B) — mesmo tratamento das
seções 32–49. Descida recursiva: **1.922 de ~1.972 instruções
possíveis (97%)**, sem tabela de salto computada; **116 branches,
59 de retrocesso**.

**Confirma, pela segunda vez, o padrão da seção 49**: `E` chama os
MESMOS endereços sem prefixo de `disp_personalwindow` (`addlocalprim`
`0xd665c`, `statuskanjiprint` `0xe2b78`, idênticos) — não tem cópia
`E`-prefixada dos helpers de desenho, só a função de entrada é
própria (com seus próprios locais internos pequenos, em endereços
diferentes de `Ddisp_personalwindow`). Com `D` e `E` confirmando o
mesmo padrão, e só `W` tendo cópia completa, a hipótese fica mais
sólida: **`W` é a única variante que é uma recompilação de verdade**
do código-fonte; `A`/`C`/`D`/`E` (três ainda não lidas) são, com alta
confiança agora, só pontos de entrada finos — não precisam de leitura
byte a byte individual, dado o padrão já confirmado duas vezes.
Marcada `read_structural`.

## 51. `Adisp_personalwindow()` — passe estrutural — terceira confirmação, fecha a família `disp_personalwindow` (2026-10-17, Fase 3)

`Adisp_personalwindow()` (`0xc96a0`, 7.728 B) — descida recursiva:
**1.880 de ~1.932 instruções possíveis (97%)**, sem tabela de salto;
**109 branches, 56 de retrocesso**. Terceira confirmação do padrão
das seções 49/50: chama os mesmos endereços sem prefixo de
`disp_personalwindow` (`addlocalprim`, `statuskanjiprint`, etc.,
idênticos), só a entrada é própria. Com `D`/`E`/`A` confirmando o
mesmo padrão (3 de 4 letras restantes), a família
`disp_personalwindow` está, no nível "passe estrutural", efetivamente
encerrada — só `C` falta, e a essa altura seria apenas a quarta
repetição do mesmo achado. Marcada `read_structural`.

## 52. `Mdl0010` — passe estrutural — confirma a chamada DIRETA a `CreateObjectWithTable` (2026-10-17, Fase 3)

`Mdl0010(short, int, int, int)` (`0x236320`, 7.684 B) — descida
recursiva: **1.909 de ~1.921 instruções possíveis (99,4%)**, sem
tabela de salto; **124 branches, 54 de retrocesso**. Confirma e
estende a seção 48: **chama `CreateObjectWithTable` diretamente**
(`0x225ac8`, seção 44) — não é só compartilhar matemática, `Mdl0010`
literalmente invoca o gerador de partículas como sub-rotina. Duas
funções de variação novas (`getVariationAppearVecRange`,
`getSmooth`) e `ratan2` (arco-tangente, nova função GTE-adjacente).
`ps_rand()` ×26. Marcada `read_structural`.

## 53. `Mdl0003` — passe estrutural — catálogo de chamadas idêntico a `Mdl0010`, sinal de diminishing returns na família (2026-10-17, Fase 3)

`Mdl0003(short, int, int, int)` (`0x22d69c`, 7.664 B) — descida
recursiva: **1.904 de ~1.916 instruções possíveis (99,4%)**. O
catálogo de 29 `bl` é **idêntico ao de `Mdl0010`** (seção 52),
inclusive nas contagens (`ps_rand` ×26, `getVariationData` ×12,
etc.) — mesmo "esqueleto" de chamadas, parâmetros/constantes
internas é que devem diferir (não lido). **Nota honesta pro resto da
fila**: dado que `Mdl0024`/`Mdl0010`/`Mdl0003` já mostraram o mesmo
catálogo de chamadas três vezes, as ~8 funções `Mdl*` restantes
provavelmente são repetições do mesmo padrão — leitura estrutural
adicional tem retorno decrescente; vale pular pro resto da fila e
voltar aqui só se uma comparação rápida de tamanho/endereço sugerir
alguma divergente. Marcada `read_structural`.

## 54. `disp_scrollwindow()` — passe estrutural — revela o sistema `multiwindow_*` de pacotes de sprite compartilhados (2026-10-17, Fase 3)

`disp_scrollwindow()` (`0xec908`, 7.444 B) — pulando o resto das
famílias `Mdl*`/`disp_personalwindow` por retorno decrescente
(seção 53), este é um sistema genuinamente novo. Descida recursiva:
**1.757 de ~1.861 instruções possíveis (94%)**, sem tabela de salto;
**148 branches, 74 de retrocesso**.

### Confirma a janela de texto com scroll, e um sistema `multiwindow_*` nunca catalogado por completo

```
multiwindow_keydown(COMRECORD*) / multiwindow_keyright(COMRECORD*, int) / multiwindow_break(unsigned long*)
multiwindow_loadcolor2(tagSPRT*) / multiwindow_packetcolor(PRIMPACKET*)
multiwindow_packetinit(RECT16*, COMRECORD*, PRIMPACKET*) / multiwindow_packetextend(...) / multiwindow_packetanm(...)
statusfigprint10 / statusfigprint16 / statusnowprint(char*, COPYFIELD*)
checkkeyok() / get_padframe() / allocatememorywait(int) / disposememory(char*)
```
`multiwindow_packetextend` já tinha aparecido na seção 33
(`Wmultiwindow_packetextend`, dentro de `Wmesputmain`) — agora
confirma a família **sem prefixo** inteira: um sistema de **gerência
de pacote de sprite compartilhado entre várias janelas** (cor, init,
extensão, animação), usado tanto por mensagens quanto por esta janela
de scroll. `statusfigprint10`/`statusfigprint16` (variantes por
número de dígitos) e `statusnowprint` são achados novos dentro da
família de impressão de status já vista nas seções 46/49/50/51.

Confirma scroll real via teclado/toque: `multiwindow_keydown`/
`multiwindow_keyright`/`checkkeyok` — navegação de texto com scroll
usando input real, não só posição estática. `iOS_CMenuTouch::
getCursorPosLeft`/`getCursorPosRight` (novas, par de métodos nunca
catalogados) reforçam o papel desta classe em UI de navegação
horizontal também, não só vertical.

**O que ficou sem confirmar**: os corpos da cascata de 148 branches
(74 de retrocesso); o formato exato de `PRIMPACKET`. Marcada
`read_structural`.

## 55. `UnitTable` — passe estrutural — confirma uma rotina genérica de lista de unidades parametrizada por callback (2026-10-17, Fase 3)

`UnitTable(short,short,short,short,short, int(*)(int), int(*)(int), int)`
(`0x1bde2c`, 6.976 B) — descida recursiva: **1.596 de ~1.744
instruções possíveis (91%)**; **180 branches, 104 de retrocesso**.

### A "tabela de salto não resolvida" era, na verdade, duas chamadas via ponteiro de função reais

A ferramenta sinalizou 2 blocos terminando em branch computado
(`blx ip`/`blx r1`) — mas não são tabelas de switch: são **chamadas
diretas através dos dois parâmetros `int(*)(int)` da própria
assinatura**. Confirma que `UnitTable` é uma rotina **genérica e
parametrizada**: quem chama fornece dois callbacks (prováveis
"pegar unidade no índice N" e "filtro/ordem"), e o restante do
código é compartilhado entre todo mundo que precisa desenhar uma
lista de unidades — explica por que `UnitList`/`BattleUnitList`
(seção 36) e as telas de item usam tantas funções `iOSUnitList*` em
comum: todas são clientes desta mesma rotina parametrizada.

### Achados novos de desenho

`DrawEggWithShadow(short, DVECTOR*, int, COLOR*, int, int)` e
`DrawUnitWithShadow(short, DVECTOR*, COLOR*, int, int)` — nunca
vistas; "Egg" sugere um ícone/retrato de unidade com formato oval
desenhado com sombra própria (hipótese, não confirmada).
`UnitScroll(short*, short*)`/`scroll_chk()` confirmam lógica de
rolagem própria desta lista. `GetSttsAMovingTime()`/`GetSttsApos`
sugerem posição/tempo de uma animação de movimento de status.

**O que ficou sem confirmar**: os corpos da cascata de 180 branches
(104 de retrocesso); o papel exato de "Egg". Marcada
`read_structural`.

## 56. `UnitList(int, int)` — passe estrutural parcial — uma tabela de ponteiros de função real, resiste à resolução estática (2026-10-17, Fase 3)

`UnitList(int, int)` (`0x1c0930`, 6.956 B) — provável cliente direto
de `UnitTable` (seção 55). Descida recursiva alcançou só **1.004 de
~1.739 instruções possíveis (58%)** — cobertura parcial, honesta,
não forçada: há um despacho real via **tabela de ponteiros de
função em memória** (`ip = *(sp+0x84)`; `r3 = ip[*r4]`; `blx r3`),
diferente das tabelas de salto `addls pc,...` já extraídas em outras
seções — aqui os alvos são dados em runtime (carregados de uma
estrutura local, não de um array de instruções `b` embutido no
código), então **não é extraível estaticamente só com o binário**;
escalonado, não forçado.

Mesmo com a cobertura parcial, 69 `bl` resolvidos já confirmam um
catálogo rico: `TutrialInit`/`Tutrial`, `unit_isdark()`,
`SttsAMovingChk`, `AllSttsDelete`, `UnitFlagInit`,
`world_stopnoend`/`worldmap_restart` (mesma função de reinício de
mapa mundi já vista em `CardAccess`, seção 42),
`iOSLRChgTap`/`iOSLRChgSwype` (troca de unidade selecionada via L/R,
por toque ou arrasto), `iOS_dispOkNg`/`iOS_clearOkNg` (mesmo diálogo
Sim/Não da seção 42), e `isInRectUi(_RECT_UI*, int, int)` — um tipo
`_RECT_UI` novo pra teste de área de toque.

**O que ficou sem confirmar**: 42% da função (a tabela de função
indexada e tudo que só é alcançável por ela). Marcada
`read_structural` com a ressalva explícita de cobertura parcial.

## 57. `AbilityMenu()` — passe estrutural — confirma o sistema real de aprendizado de habilidade por job (2026-10-17, Fase 3)

`AbilityMenu()` (`0x1a486c`, 6.908 B) — descida recursiva: **1.646
de ~1.727 instruções possíveis (95%)**, sem tabela de salto; **152
branches, 73 de retrocesso**.

### Confirma o mecanismo real de aprender habilidade por job (o sistema clássico de FFT)

```
GetAbilityList(short,short,int,short*,int)      GetTotalAbilityList(short,int,short*)
AbilityCompare(C_STTS*,short,short)              AbilityEquip(short,short,short,int)
IsUntauchableAbility(int)                           pspAbilityCompareSupport(short,short)
LearnJobStts() / LearnAbiStts() / JobToAbiChg()    SetSttsAbi(int)
```
Paralelo direto ao sistema de itens já confirmado (`ItemMenu`, seção
39): mesma estrutura (`List`/`Compare`/`Equip`), agora pra
habilidades aprendidas por job. `JobToAbiChg()` confirma a ponte
real entre o job atual de uma unidade e as habilidades que ela pode
aprender/equipar — o mecanismo central de customização de personagem
do FFT, nunca catalogado byte a byte antes. Reusa a mesma biblioteca
de janela/menu já vista (`WindowInit`/`SetMenuSelVertical`/
`MenuSelVerticalWithSnd`) sem prefixo — mais uma tela cliente da
biblioteca compartilhada (seções 39/40/42/45/49-51).

**O que ficou sem confirmar**: os corpos da cascata de 152 branches
(73 de retrocesso). Marcada `read_structural`.

## 58. `Wdisp_scrollwindow()` — passe estrutural — quarta confirmação do padrão `W` = cópia real + `wasm` (2026-10-17, Fase 3)

`Wdisp_scrollwindow()` (`0x117374`, 6.504 B) — descida recursiva:
**1.541 de ~1.626 instruções possíveis (95%)**, sem tabela de
salto; **121 branches, 59 de retrocesso**. Cópia `W`-prefixada
completa de `disp_scrollwindow` (seção 54) — todo o sistema
`multiwindow_*` reaparece como `Wmultiwindow_*`, e a família de task
é `wasm` (não `asm`) — **quarta confirmação** da correlação
`W`↔`wasm` (seções 33/37/47), depois de `Wmesputmain`/`mesputmain`
e `Wdisp_personalwindow`/`disp_personalwindow`. A hipótese "`W` é
cópia real de fonte, correlacionada com a task `wasm`" está, a essa
altura, bem estabelecida pra múltiplas famílias de tela. Marcada
`read_structural`.

## 59. `GuEmu_libgu_to_gl()` — passe estrutural — a ponte real entre o PSP e o motor gráfico moderno; reclassifica todo o `psp*` da investigação (2026-10-17, Fase 3)

`GuEmu_libgu_to_gl()` (`0x2ae900`, 6.368 B) — citada desde a seção
32 (`battle()`) e a 35 (`Main_FrameMove`), nunca aberta. Descida
recursiva: **1.544 de ~1.592 instruções possíveis (97%)**, sem
tabela de salto; **146 branches, 67 de retrocesso**.

### Achado maior: confirma que "psp" é literalmente PSP (PlayStation Portable), não um prefixo genérico

`GuEmu` = emulação da **`libgu`/`sceGu`, a API gráfica real do PSP**
(análoga à `libgpu` do PS1 já confirmada em várias seções). Esta
função é a **ponte real** entre chamadas de estilo PSP (`GuEmu_Clear`,
`GuEmu_GetRAW`, `GuEmu_GetCLUTAddress`, `GuEmu_FrameMove` — seção
35) e o motor gráfico moderno `CEGL2_*` já documentado nas seções
13–15/34:
```
CEGL2_IF::GetPacket(int)
CEGL2_SPRITE::LoadBegin/LoadEnd/Overwrite/GetImageSize/GetImageBPP/GetTextureHandle/Unload
CEGL2_TEX_HYBRID::Register/UV_Get/UV_AutoRelease/CLUTAddr_AutoRelease/RAW_GetBuf/
  GL_IsUpdate/AutoRelease/RAW_IsUpdate/GL_GetTextureHandle/GL_SetUsed/GL_Load
CEGL_PACKET::GetCount/SetTexture/GetExtra/SetExtra/GetVBOBuffer/GetVBOInfo
CFILE_DAT::Unload/CacheFind/CacheReplace/GetBuffer/Load/Decode
CWORK_MEM::Get/GetTail
```
**Isto reclassifica, com evidência concreta, todas as dezenas de
funções `psp*` já catalogadas nesta investigação inteira**
(`pspSaveInit`, `pspBattleCheckFlg`, `pspNetGetBattleModeFlag`,
`pspItemGetCommonData`, `pspWorldCheckFlg`, etc., seções 12.12, 19.1,
36, 39–45, 56): **não são um "prefixo de compatibilidade genérico"
— são literalmente a camada de API do PlayStation Portable**,
confirmando que este jogo tem raiz **PSP**, não só PS1 (a lib
gráfica PS1 `Gs*`/`libgpu` já documentada nas seções 9–15 convive
com a camada PSP `libgu`/`sceGu` nesta mesma base de código — duas
plataformas de origem, não uma).

**Também confirma, com nome real, o motivo de `CEGL2_TEX_HYBRID` ter
"HYBRID" no nome** (seções 13.7/13.11): é híbrida entre o caminho
"RAW" (textura cru, provavelmente do PSP/`Gu`) e o caminho "GL"
(OpenGL ES moderno) — `RAW_GetBuf`/`RAW_IsUpdate` vs. `GL_Load`/
`GL_IsUpdate`/`GL_GetTextureHandle` confirmam os dois caminhos
reais dentro da mesma classe, exatamente o "hybrid" do nome.

**O que ficou sem confirmar**: os corpos da cascata de 146 branches
(67 de retrocesso). Marcada `read_structural`.

## 60. `Wdisp_floateventwindow()` — passe estrutural — janela de mensagem flutuante de evento, quinta confirmação `W`/`wasm` (2026-10-17, Fase 3)

`Wdisp_floateventwindow()` (`0x1314a8`, 6.228 B) — descida
recursiva: **1.541 de ~1.557 instruções possíveis (99%)**, sem
tabela de salto; **153 branches, 80 de retrocesso**.

Confirma, pelo nome e pelas chamadas, uma **janela de mensagem
flutuante** (provavelmente balão de diálogo sobreposto à cena, não
uma janela de UI fixa) ligada ao sistema de eventos:
`Wwrite_eventflag`/`Wread_eventflag` (7×/5×), `Wmultiwindow_packetextend`,
`Wextend_windowframemain`/`Wextend_windowframe`/`Wextend_systemframe`
(três variantes de "estender moldura de janela", novas). Quinta
confirmação da correlação `W`↔`wasm` (`wasmTaskEntry` ×9,
`wasmGetInput2` ×11) — seções 33/37/47/58. Marcada `read_structural`.

## 61. `JobChange()` — passe estrutural — a roda giratória real de troca de classe, e um termo japonês romanizado novo (2026-10-17, Fase 3)

`JobChange()` (`0x1b2ea8`, 6.216 B) — descida recursiva: **1.460 de
~1.554 instruções possíveis (94%)**, sem tabela de salto; **150
branches, 77 de retrocesso**.

### Confirma a UI real de "roda" 3D giratória de troca de job

```
iOSJobChangeRot(short*,short*)       iOSJobChanegAngle()/Init/Hosei/Reset
iOSJobChgRotAct()/Chk()/Stop()       iOSJobAngleSet/Get    iOSJobRotStop()
iOSCircleCtrl(unsigned short)        iOSJobChgRotStop()     iOSGetTchRotDY()
JobCicle(int,int,int,int)            SetJobName()           GetJobList/JobEquip
```
Confirma, com nomes reais, a UI clássica do FFT de troca de classe:
uma **roda giratória controlada por arrasto de toque**
(`iOSGetTchRotDY` = "delta Y do toque pra rotação", confirma que
deslizar o dedo verticalmente gira a roda), com ângulo/estado de
rotação geridos por uma família própria de funções `iOSJobChaneg*`
(nota: "Chaneg", não "Change" — erro de digitação real preservado,
mesmo espírito de `ASURA`/`changeflame`). **`Hosei`**
(`iOSJobChanegAngleHosei`) é japonês romanizado (**補正**,
"correção/ajuste") preservado no nome — mais um termo nunca
traduzido, no espírito de "Iwasaki"/"SSD" já catalogados.

**O que ficou sem confirmar**: os corpos da cascata de 150 branches
(77 de retrocesso). Marcada `read_structural`.

## 62. `gl3stubInit` — confirmado como boilerplate genérico do Android NDK, lida por completo em uma passada rápida (2026-10-17, Fase 3)

`gl3stubInit` (`0xb1cdc`, 6.204 B) — diferente de todas as seções
anteriores, este NÃO precisou de passe estrutural extenso: uma
olhada no padrão já basta pra confirmar 100% do conteúdo. Único `bl`
chamado (**104 vezes**): `sub_719ec`, que é um trampolim direto pra
`dlsym` via GOT (`add ip,pc,#...; ldr pc,[ip,#...]!`). O corpo de
`gl3stubInit` é literalmente: pra cada uma das 104 funções GLES3,
chama `dlsym(handle, "glNomeDaFunção")` e grava o ponteiro resolvido
num slot de função global. **Este é o arquivo `gl3stub.c` padrão do
Android NDK** (usado por inúmeros projetos Android com OpenGL ES 3
pra resolver os símbolos em tempo de execução) — zero lógica
específica do jogo. Marcada `read_full` (não `read_structural`): não
há mais profundidade a extrair, o padrão já confirma o conteúdo
inteiro sem precisar enumerar as 104 repetições individualmente.

## 63. `resultproc()` — passe estrutural — a tela de resultado de batalha, com recompensa/JP/dinheiro e julgamento de rede (2026-10-17, Fase 3)

`resultproc()` (`0x14ec70`, 6.156 B) — descida recursiva simples
alcançou só 946 instruções; **duas** tabelas de salto (5 e 6 casos,
todos distintos nas duas) extraídas com `jtable.py` (ferramenta
validada contra `battle()`, seção 32 — a segunda tabela não tinha
sido encontrada na extração manual original desta seção) e usadas
como semente elevam a cobertura pra **1.461 de ~1.539 instruções
possíveis (95%)**; **91 branches, 50 de retrocesso**.

### Confirma a tela de resultado pós-batalha, com recompensas reais

```
ChgMoney(int)                        — dinheiro ganho na batalha
getGetItemCount() / get_itemcommon(unsigned short) / get_item_number(unsigned short,int)
getRewardLv() / CalcRewardLv() / Final_CalcMissionPayPoint()
setBattlePoint(int) / getBattlePoint()
pspNetGetBattleModeFlag() / pspNetJudgeBattlePoint() / pspNetGetLimitAction()
GetNetmissionNo()                    callZingle(int)  /  callSoundEffect(int)
```
Confirma que a tela de fim de batalha calcula e aplica **dinheiro,
nível de recompensa e pontos de missão pagos** de verdade — e,
reforçando as seções 41/43, consulta de novo o **julgamento de
batalha em rede** (`pspNetJudgeBattlePoint`/`GetNetmissionNo`) bem
aqui na tela de resultado, não só na configuração — confirma o ciclo
completo "configurar batalha em rede → julgar resultado → mostrar
recompensa" com evidência real em pelo menos 3 funções diferentes.
`callZingle(int)` é um achado novo — mesmo nome de "Zingle" citado
por `controlZingle` no catálogo de `battle()` (seção 32), provável
cue de som/efeito sonoro específico (ex.: fanfarra de vitória).

**O que ficou sem confirmar**: os ~5% restantes da função. Marcada
`read_structural`.

## 64. `Main_Init()` — passe estrutural — completa o trio principal do jogo, e o maior número de chamadas a uma única função de toda a investigação (2026-10-17, Fase 3)

`Main_Init()` (`0x2bf3e8`, 5.832 B) — a inicialização principal do
jogo, completando o trio com `Main_FrameMove`/`Main_FrameRender`
(seções 34/35). Descida recursiva: **1.428 de ~1.458 instruções
possíveis (98%)**, sem tabela de salto; só **25 branches** (função
quase linear — inicialização sequencial, não um laço).

### Achado numérico: `iOS_setV2Icon` chamada 230 vezes — recorde absoluto

Mais que o triplo do recorde anterior (`Main_FrameMove`, 50×, seção
35). Confirma que `Main_Init` zera/configura o estado inicial de
**centenas de ícones de UI individualmente**, um por um — o sistema
`iOS_*V2Icon` (visto em quase toda função de UI desta investigação)
é, de fato, uma tabela de estado central enorme, inicializada
exaustivamente no boot.

### Confirma a inicialização real de vários sistemas já documentados

```
CGX_SCREEN_CORRECT::Init/Area_InitLandscape    (seção 34 — correção de tela, agora com o ponto de init real)
CINPUT_IF_TOUCH::ClearAll()                       (sistema de toque, seção 20/26/35)
CRECT::Register/SetRect/SetDrawRect/SetEnable/MulRect/Clear  (sistema de hit-rect, usado em dezenas de telas)
CTHREAD::Register(...)                              (thread real spawnada no boot, seção 28)
initSaveFFT(char*, char*, bool)                      (caminhos do sistema de save, seções 42/45)
CFFT_STATE::SetMode/SetDebugMode/SetMoviePlaying/SetSettingsEnable/SetLinkEnable/SetParam  (hub de estado global)
```
Confirma `Main_Init` como o ponto real de boot de praticamente todo
sistema já documentado nesta investigação — fecha, de forma
concreta, "quem inicializa" pra vários "o que faz" já catalogados.

**Achado bônus**: `Debug_SetDebugDirectBtn(int)`/
`Debug_SetMapPolyCheck(int)` — flags de depuração reais, ativáveis
no boot, remanescentes de build de desenvolvimento.

**O que ficou sem confirmar**: os ~2% não alcançados (muito pouco,
função quase inteiramente linear). Marcada `read_structural`.

## 65. `CCAMERA::Update()` — passe estrutural — a câmera 3D real do motor moderno, matemática pura em ponto flutuante de software (2026-10-17, Fase 3)

`CCAMERA::Update()` (`0xafb30`, 5.576 B) — primeira leitura da
classe `CCAMERA` (vtable real confirmada, `_ZTV7CCAMERA`; construtor/
destrutor/`Init`/`SetMode`/`SetNearClip`/`SetFarClip`/`SetFov`/
`GetView`/`GetProj`/`GetDir`/`SetProjOrtho` todos no `.dynsym`, a
maioria não lida). Descida recursiva: **1.393 de ~1.394 instruções
possíveis (99,9%)** — cobertura quase total. **Só 8 branches, ZERO
de retrocesso** — função inteiramente linear, sem nenhum laço.

### Confirma uma câmera 3D moderna, orientada a objeto, separada da pilha GTE do PS1

Catálogo de `bl` dominado por ponto flutuante de **software**:
`__mulsf3` (**174×**), `__addsf3` (89×), `__subsf3` (60×),
`__divsf3` (13×), `__extendsfdf2`/`__truncdfsf2`/`__divdf3`
(conversões float↔double). Nenhuma chamada a `RotMatrix`/
`SetRotMatrix`/`RotTrans` (a pilha GTE do PS1 já confirmada em
`ASHURA_addPrim`/`Mdl*`, seções 38/48/52/53) — **`CCAMERA` é a
câmera real do motor `CEGL2_*` moderno**, com sua própria matemática
de view/projeção em ponto flutuante puro, não a câmera de estilo
PS1. Isso **separa, com evidência concreta, duas câmeras distintas**
nesta investigação: a câmera GTE/fixa do mapa mundi e batalha estilo
PS1, e esta `CCAMERA` orientada a objeto do renderer moderno.

**O que ficou sem confirmar**: a fórmula matemática exata (view/
projeção — perspectiva ou look-at, não cravado byte a byte); as
outras ~10 funções pequenas de `CCAMERA` (a maioria ≤28 B, getters/
setters triviais) continuam não lidas. Marcada `read_structural`.

## 66. `event_call` — passe estrutural — o dispatcher central de ações de evento/cutscene, a maior ponte entre sistemas de toda a investigação (2026-10-17, Fase 3)

`event_call(unsigned long* script, unsigned long pc)` (`0xf431c`,
5.456 B) — assinatura clássica de interpretador de bytecode
(ponteiro de script + contador de programa), parte do motor de
eventos já confirmado nas seções 9.5–9.6. Descida recursiva: **1.261
de ~1.364 instruções possíveis (92%)**, sem tabela de salto; **167
branches, 79 de retrocesso**.

### O catálogo de 70 `bl` é, de longe, o mais "amplo" (menos profundo, mais ligações) de toda a Fase 3

Confirma que `event_call` é o **despachante central de ações
disponíveis pra scripts de evento/cutscene** — chama diretamente
telas e sistemas inteiros já documentados em seções completamente
separadas desta investigação:

- **Telas de batalha, chamadas DE DENTRO de um evento**:
  `BattleCardAccess` (seção 45), `BattleUnitList` (seção 36),
  `BattleEquip`, `BattleJobStts` — confirma que cutscenes/eventos
  podem abrir essas telas diretamente.
- **Controle de câmera do mapa mundi durante eventos**:
  `setMapScrollXYZ`/`setMapScale`/`setMapAngle` — ligação real com
  o sistema de câmera já visto nas seções 12.11/12.14.
- **`ASHURA` específico de evento**: `ASHURA_Control`,
  `ASHURA_EVENT_CLUT_LOAD`, `ASHURA_GNS_Garage` — três funções novas
  do motor 3D (seção 38), nomeadas especificamente pra contexto de
  evento (`GNS_Garage` sugere uma cena fixa tipo "garagem"/base,
  hipótese não confirmada).
- **Sistema de animação de evento completo, nunca catalogado**:
  `loadNewAnimation`/`loadEventAnimation`/`activateEventAnimation`/
  `inactivateEventAnimation`/`disposeEventAnimation`/
  `activateCompressedAnimation`/`inactivateCompressedAnimation`/
  `checkAnimationExist`/`checkModelAnimation`/`checkCharacterMove`/
  `startVRAMAnimation`/`checkVRAMAnimation` — um ciclo de vida
  completo de animação de cutscene, com variante "comprimida" e
  variante "VRAM" distintas.
- **Corte de câmera/cena**: `eventMapJump`/`eventMapJump2`/
  `eventMapFadeIn`/`eventMapRewrite`/`ScriptCut__Fiii` — confirma
  cortes de câmera reais (estilo "jump cut") no sistema de eventos.
- **Música completa controlada por evento**: `callMusic`/`stopMusic`/
  `fadeMusic`/`activateMusic`/`inactivateMusic`/`disposeMusic`.
- Outros: `fade_eventlocal`, `request_tooltest`, `changeflame`,
  `Set_bravebreak`, `pspBattleDataPadGet`, `getMoviePlayFlg__Fv`,
  `get_gEventMovieNo`/`getEventStatus`.

**Confirma, com a maior concentração de evidência cruzada de toda a
Fase 3, que o motor de eventos (seções 9.5–9.6) não é um sistema
isolado — é o ORQUESTRADOR de praticamente todo o resto do jogo**:
telas de batalha, câmera do mapa, motor 3D de efeitos, animação,
música, tudo acionável por uma única instrução de bytecode através
de `event_call`.

**O que ficou sem confirmar**: os corpos da cascata de 167 branches
(79 de retrocesso) — qual opcode exato dispara qual chamada não foi
mapeado função a função. Marcada `read_structural`.

## 67. `world_scrollwindow()` — passe estrutural — mais uma cliente `W` do sistema `multiwindow_*`, com recorte (clip) real (2026-10-17, Fase 3)

`world_scrollwindow()` (`0x15834c`, 5.236 B) — descida recursiva:
**1.293 de ~1.309 instruções possíveis (98%)**, sem tabela de
salto; **108 branches, 54 de retrocesso**. Sexta confirmação do
padrão `W`/`wasm` (seções 33/37/47/58/60).

Achados novos dentro do sistema `multiwindow_*` (seção 54/58):
**`Wmultiwindow_packetclip(CLIP*, RECT16*, int, int)`/
`Wmultiwindow_packetclipinit(CLIP*)`/
`Wmultiwindow_packetadd(PRIMPACKET*, int, int)`** — confirmam
**recorte (clipping) real** de pacotes de sprite contra um
retângulo, nunca visto nas leituras anteriores do sistema. Também
**`WiOS_battle_scrollwindow_tap()`** — nome sugere que esta janela
de scroll do mapa mundi é reaproveitada (ou tem uma contraparte
direta) dentro do contexto de batalha. Marcada `read_structural`.

## 68. `ASHURA_set_Mesh(int, int)` — passe estrutural — switch de 9 configurações de malha 3D, quase todo orientado a dados (2026-10-17, Fase 3)

`ASHURA_set_Mesh(int, int)` (`0x163ccc`, 5.160 B) — mais uma função
do motor `ASHURA` (seção 38). A descida recursiva simples só
alcançou 15 instruções por uma tabela de salto logo no início
(`addls pc,pc,r0,lsl#2`, `cmp r0,#8` → 9 casos). Extraída com a
ferramenta validada `jtable.py` (ver nota de correção abaixo) e
usada como semente, a cobertura sube pra **1.240 de ~1.290
instruções possíveis (96%)**; 66 instruções tipo branch, 21 de
retrocesso.

Só **2 `bl` em toda a função**: `ASHURA_LightSwitch(long)` e
`requestChangeClut(...)` — confirma que `ASHURA_set_Mesh` é, na
maior parte, **orientado a dados**: cada um dos 9 casos escreve
campos de configuração de malha/matriz diretamente (inline), e só
ocasionalmente chama fora pra trocar iluminação ou paleta de
textura. Os 9 casos provavelmente correspondem a 9 "tipos de malha"
pré-definidos (formas de unidade/efeito 3D distintas — hipótese, não
confirmada byte a byte em cada caso).

**Correção (2026-10-17, mesma sessão)**: a primeira extração manual
da tabela desta função usava `endereço_do_addls + 4` como início da
tabela em vez de `+ 8` (erro de offset, achado e corrigido depois de
validar `jtable.py` contra o resultado já confirmado de `battle()`,
seção 32) — a cobertura e a contagem de branches acima já refletem a
extração correta; o achado qualitativo (9 casos, só 2 `bl`, orientado
a dados) não muda. Marcada `read_structural`.

## 69. `inflate`/`deflate`/`inflateBack` — confirmados como zlib real embutida no ARM, mesmo tratamento do `gl3stubInit` (2026-10-17, Fase 3)

`inflate` (`0x7b200`, 6.652 B), `deflate` (`0x759e8`, 4.872 B),
`inflateBack` (`0x794ec`, 4.660 B) — os três clusterizados no mesmo
bloco de endereços `0x71000`–`0x7c000`, junto de `sub_714b8`/
`sub_714c4` (helpers chamados por DEZENAS de funções de jogo já
lidas nesta investigação, provavelmente `memset`/`memcpy` da libc ou
primitivas internas do zlib). **Confirma, com nomes reais de
`.dynsym`, que a zlib real está embutida como código no ARM** — não
só via `.plt` dinâmico como a seção 31 (comparação com x86) tinha
sugerido como regra geral; os dois mecanismos convivem no mesmo
binário ARM. Mesmo tratamento do `gl3stubInit` (seção 62): biblioteca
de terceiros padrão, zero lógica de jogo, não vale um passe
instrução-a-instrução. Marcadas `read_full` as três.

## Primeiro lote paralelo (seções 70–74): 5 funções lidas por forks simultâneos, usando `jtable.py`

A partir daqui, o loop passou a paralelizar: em vez de uma função por
iteração, vários forks rodam `jtable.py` ao mesmo tempo em funções
diferentes da fila, devolvem o rascunho, e a integração nos arquivos
compartilhados acontece numa única passada. As cinco seções abaixo
(70–74) foram produzidas assim, no mesmo lote.

## 70. `executeChangeClut()` — passe estrutural — o executor real da fila de troca de paleta/CLUT, nunca aberto (2026-10-17, Fase 3, lote paralelo)

`executeChangeClut()` (`0x213e78`, 4.976 B) — descida recursiva via
`jtable.py`: **1.236 de ~1.244 instruções possíveis (99%)**, sem
tabela de salto; **81 branches, 45 de retrocesso** (consistente com
percorrer uma fila/lista em laço).

### Confirma ser o executor real por trás de `requestChangeClut` (seções 48/52/53/68)

```
requestChangeClut(int,int,unsigned int,unsigned int,int,short,short,short)   ×6
requestChangeGradation(int,int,int,int,int)
requestChangeAnbient(int,int,int,int,int)
requestChangeFlat(int,int,int,int,int)
ASHURA_CVECTOR(long, CVECTOR*)
iOS_GetFrameRate()
```
`requestChangeClut` já tinha aparecido como chamada de dentro da
família `Mdl*`/`ASHURA_set_Mesh` (seções 48, 52, 53, 68), mas nunca
tinha sido aberta por dentro, nem se sabia quem de fato processava os
pedidos. `executeChangeClut` confirma essa ponte: é quem **executa**
a fila de pedidos de troca de CLUT/paleta — chamando `requestChangeClut`
6 vezes, consistente com percorrer uma lista de pedidos pendentes e
aplicá-los um a um.

Revela três funções irmãs nunca vistas, com a mesma convenção
`requestChange*` — confirma que o sistema de troca de paleta não é
só "CLUT" (tabela de cor indexada): também existe troca de
**gradação**, **ambiente** (achado honesto: o nome real no binário é
`requestChangeAnbient`, sem o segundo "i" — mais um erro de
digitação preservado, no espírito de `ASURA_LMDL_TIME_TBL`/
`iOSJobChaneg*`), e **cor plana**. `ASHURA_CVECTOR` (vetor de cor do
motor 3D, seção 38) confirma que esse sistema de troca de paleta
está ligado ao pipeline de cor do ASHURA, não é um sistema isolado.

**O que ficou sem confirmar**: os corpos da cascata de 81 branches
(45 de retrocesso); a estrutura exata da fila (tamanho, onde é
preenchida); os corpos das 4 funções `requestChange*` em si (só
confirmadas por chamada/assinatura). Marcada `read_structural`.

## 71. `iOS_SetIconPosition()` — passe estrutural — novo recorde de `RETINA_SCALE`, confirma posicionamento de ícone totalmente desenrolado (2026-10-17, Fase 3, lote paralelo)

`iOS_SetIconPosition()` (`0x2b8900`, 5.036 B) — descida recursiva via
`jtable.py`: **1.250 de ~1.259 instruções possíveis (99%)**, sem
tabela de salto; só **3 branches, 2 de retrocesso** (função quase
inteiramente linear/desenrolada, não um laço real sobre um array).

Catálogo de `bl` dominado por duas funções já conhecidas da seção 34
(`Main_FrameRender`): **`RETINA_SCALE(int)` chamada 131 vezes** e
**`CGX_SCREEN_CORRECT::Scaled(int)` chamada 129 vezes** — supera o
recorde anterior de `RETINA_SCALE` (68×, seção 34). Cada bloco
repetido passa um **valor literal diferente** pra
`RETINA_SCALE`/`CGX_SCREEN_CORRECT::Scaled` — ou seja, **não é um
laço sobre uma tabela, é código manualmente desenrolado, um bloco
fixo por ícone**, o mesmo padrão de desenrolamento massivo já
confirmado em `Main_Init` (seção 64, `iOS_setV2Icon` chamada 230
vezes). Também usa `CGX_SCREEN_CORRECT::GetOffset_1X`/`GetScale`
(seção 34) e `CRECT::Register(_RECT_UI*, int)` (seção 65, mesmo
sistema de hit-rect inicializado em `Main_Init`).

Confirma que esta função é, junto com `Main_Init`, o segundo grande
ponto de "configuração em massa, um bloco por ícone, sem tabela" do
sistema de ícones V2/retina — provavelmente chamada quando a tela
gira ou o dispositivo muda de escala, reposicionando cada ícone
individualmente.

**O que ficou sem confirmar**: a lista exata de quais dos ~130
ícones são reposicionados aqui; se esta função é chamada uma vez no
boot ou repetidamente (ex.: a cada rotação de tela). Marcada
`read_structural`.

## 72. `set_monsterwork_j(BWORK*, EDATA*, int, int)` — passe estrutural — confirma randomização real de equipamento de monstro (2026-10-17, Fase 3, lote paralelo)

`set_monsterwork_j(BWORK*, EDATA*, int, int)` (`0x1da9e4`, 4.540 B) —
primeira função lida que toca `BWORK` (área de trabalho de batalha,
citada desde a seção 12 do backlog original e por `get_bwp`/
`erase_unit`/`resist_savedata` na seção 43) e `EDATA` por dentro.
Descida recursiva via `jtable.py`: **1.122 de ~1.135 instruções
possíveis (99%)**, sem tabela de salto; **148 branches, 66 de
retrocesso**.

### Confirma a inicialização de unidades monstro, com randomização real de item

```
get_unitwork_add(int)        set_jcflag(unsigned char*, int)
copy_struct_data(void const*, void*, int)    clear_cmemory(void*, int)
pspItemGetCommonData / pspItemIsEmpty / pspItemIsBarehand / pspItemGetWeaponData
pspItemIsRandom                                — chamada 20 vezes
pspJobGetJobChangeFlag(unsigned char*, unsigned char, unsigned char(*)[3], int)
pspNetGetBattleModeFlag()
```
A assinatura (`BWORK*, EDATA*`) e o nome confirmam que esta função
monta a área de trabalho de batalha de uma unidade **monstro**
(categoria de unidade nunca aberta nesta investigação — distinta do
sistema de job/habilidade humano das seções 57/61) a partir de um
template de dados de inimigo (`EDATA`). **`pspItemIsRandom` chamada
20 vezes** é o achado mais concreto: sugere um laço real sobre slots
de equipamento resolvendo itens marcados como "aleatórios" no
template — **randomização de equipamento de monstro**, mecanismo
nunca confirmado antes. `pspJobGetJobChangeFlag` liga esta
inicialização ao sistema de troca de job (seção 61);
`pspNetGetBattleModeFlag` é mais uma aparição do sistema de batalha
em rede (seções 41/43/63).

**O que ficou sem confirmar**: os corpos das ~10 funções locais sem
símbolo (`sub_1d6ee0` ×10, `sub_1d6f84` ×16 — as mais chamadas,
provavelmente getters/setters de campo de `BWORK`); o layout exato
de `BWORK`/`EDATA` não foi mapeado campo a campo. Marcada
`read_structural`.

## 73. `disp_bothwindow()` — passe estrutural — janela de comparação dupla de status, reusando os mesmos helpers de `disp_personalwindow` (2026-10-17, Fase 3, lote paralelo)

`disp_bothwindow()` (`0x12b12c`, 4.196 B) — descida recursiva via
`jtable.py`: **1.018 de ~1.049 instruções possíveis (97%)**, sem
tabela de salto computada; **64 branches, 44 de retrocesso**.

### Confirma reuso direto da biblioteca de desenho de `disp_personalwindow`, não uma cópia

Os 33 `bl` resolvidos incluem, nos MESMOS endereços sem prefixo já
vistos nas seções 46/49/50/51 (`disp_personalwindow`): `addlocalprim`
(`0xd665c`), `statuskanjiprint` (`0xe2b78`), `bgput` (`0xe1118`),
`initdrmode` (`0xe0fb8`), `loadcdst` (`0xe0fa0`),
`addstatusback`/`sttsback_normal`/`sttsback_blue`/`initstatusback` —
confirma que `disp_bothwindow` **não chama** nenhuma variante de
`disp_personalwindow`; em vez disso, desenha diretamente usando a
MESMA biblioteca de helpers de status já documentada, consistente
com o padrão "entrada fina reusando helpers compartilhados" já visto
(não uma cópia de fonte duplicada, como `W`/`wasm` costuma ser). O
nome ("both window") e o uso dos dois esquemas de cor
(`sttsback_normal`/`sttsback_blue`) sugerem uma tela que mostra
**duas janelas de status lado a lado** — hipótese plausível (ex.:
comparar unidade antes/depois de trocar equipamento), não confirmada
byte a byte.

### Achados novos

- **`itemuvclut(tagSPRT*, int)`** — nunca vista; configura UV/CLUT
  de um sprite pra ícone de item (seções 39/57).
- **`TexHybrid_RegistCLUTAddr(int, unsigned int)`** — função livre
  (não método de `CEGL2_TEX_HYBRID`) nunca vista; provável
  contraparte do lado PSP/raw que a classe híbrida (seções
  13.7/13.11/59) usa para registrar o endereço de paleta.
- **`SetLineF2`/`SetTile`** — duas primitivas reais da lib gráfica
  PS1 nunca catalogadas antes.
- `pspItemIsEmpty` — mais uma função da família `pspItem*` (seções
  39/57).
- Família de task é `asm` (não `wasm`) — consistente com o padrão
  "sem prefixo de tela = task sem `w`" já visto em outras famílias.

### `Cdisp_bothwindow` — checagem rápida confirma o mesmo padrão

Verificação oportunista de `Cdisp_bothwindow()` (`0x14935c`, 4.780 B,
97% de cobertura): catálogo de `bl` idêntico (mesmos endereços,
mesmas contagens, nos primeiros 14+ itens comparados) — confirma que
`C` aqui também é só um ponto de entrada fino reusando os mesmos
helpers, não uma cópia separada — mesmo padrão já visto em `D`/`E`/
`A` de `disp_personalwindow` (seções 49–51).

**O que ficou sem confirmar**: os corpos da cascata de 64 branches
(44 de retrocesso); se as variantes `A`/`D`/`E`/`W` de
`disp_bothwindow` seguem o mesmo padrão sem exceção (`W`
especificamente merece verificação, já que em outras famílias é a
única variante que de fato duplica os helpers). Marcadas
`read_structural` (`disp_bothwindow` e `Cdisp_bothwindow`).

## 74. `battle_scrollwindow()` — confirmação rápida do padrão `Wmultiwindow_*`/`wasm` (2026-10-17, Fase 3, lote paralelo)

`battle_scrollwindow()` (`0x13f1dc`, 4.728 B) — **98% de cobertura**
(1.162/1.182 instruções) via `jtable.py`, sem tabela de salto, 93
branches. Confirma ser mais um cliente do sistema `Wmultiwindow_*`/
`wasm` já documentado nas seções 54/58/67 (`Waddlocalprim`,
`Wmultiwindow_packetclip`/`packetclipinit`/`packetadd`,
`Wstatuskanjiprint`, `wasmTaskEntry`/`wasmGetInput1`/
`wasmGetActiveF`). Chama `WiOS_battle_scrollwindow_tap()`
diretamente, confirmando a ligação já suspeitada na seção 67.
**Notável**: o nome externo da função não tem prefixo `W`, mas ela
usa o conjunto de helpers internos `W`-prefixado mesmo assim —
confirma que a escolha do prefixo é por **contexto de tela**, não
pelo nome da função chamadora. Dois achados pequenos novos:
`iOS_setLockInput(unsigned char)`/`iOS_getLockInput()` e
`iOS_setPadState(unsigned long)` — primitivas de bloqueio de input
nunca catalogadas. Marcada `read_structural`. Tratada como
confirmação curta, não seção completa, conforme a nova política de
não redocumentar famílias já confirmadas.

## Segundo lote paralelo (seções 75–79): mais 5 funções lidas por forks simultâneos

## 75. `Shop(int)` — passe estrutural parcial — a loja real do jogo, finalmente aberta (2026-10-17, Fase 3, lote paralelo)

`Shop(int)` (`0x19e7b8`, 3.936 B) — citada desde a seção 12.2
(`wld_shop` chama `Shop()` real, muda música, desativa o controlador
de mapa), nunca aberta por dentro. Descida recursiva via `jtable.py`:
**807 de ~984 instruções possíveis (82%)**, uma tabela de salto
resolvida; **65 branches, 38 de retrocesso**.

### Confirma o ciclo de vida completo da tela de loja, mas o corpo de compra/venda em si fica num bloco não alcançado

Uma tabela de 24 casos (`cmp`/`addls pc,pc,r2,lsl#2` em `0x19f0f8`)
colapsa em só **3 endereços distintos** (`0x19f168`, `0x19f5f0`,
`0x19f160`) — uma máquina de estados com muitos casos "vazios"/
redundantes, mesmo padrão já visto em `battle()` (seção 32) e outros
switches desta investigação.

`bl` catalogados confirmam infraestrutura real de tela (`SwapDB`/
`DB_init` — mesmo sistema de buffer de primitivas PS1 da seção
36/42/45; `FadeIn`; `WaitLoadImage`/`WaitStoreImage`/`WaitMoveImage`;
`loadMusic`/`disposeMusic`/`activateMusic`; `mallocForFile`/
`freeForFile`), navegação/toque (`iOS_SetRectHit`,
`iOS_GetRectHitNoTap`, `iOSUnitListTapCheck`,
`iOSUnitListAllStatusTapCheck`), e `worldmap_restart()` (mesma
função de reinício do mapa já vista em `CardAccess`/`UnitList`,
seções 42/56). **Surpresa honesta**: nenhuma chamada direta a
`GetItemList`/`ItemEquip`/`pspItem*` apareceu nos 82% alcançados — a
lógica real de comprar/vender item provavelmente vive dentro de um
dos 3 blocos de handler da tabela (`0x19f168`/`0x19f5f0`/`0x19f160`)
ou além deles, numa parte da função ainda não decodificada por esta
passada. `bak_read(int, void*)` é um achado novo (provável leitura
de dados de "backup"/save local da loja).

**O que ficou sem confirmar**: os 18% restantes da função (onde a
lógica de compra/venda de item deveria estar, dado que não apareceu
nos 82% já lidos); os corpos dos 3 handlers da tabela de 24 casos.
Marcada `read_structural` — cobertura parcial, não forçada.

## 76. `iOS_RESUME_SET_EVENT(IOS_RESUME_DATA_EVENT*, IOS_RESUME_DATACOPY_MODE)` — passe estrutural — confirma o serializador real do sistema `iOS_Resume*`, campo a campo (2026-10-17, Fase 3, lote paralelo)

`iOS_RESUME_SET_EVENT(...)` (`0xe62cc`, 4.448 B) — descida recursiva
via `jtable.py`: **1.009 de ~1.112 instruções possíveis (91%)**, sem
tabela de salto; só **2 branches, 0 de retrocesso** (função quase
inteiramente linear/desenrolada, mesmo padrão de desenrolamento
massivo já visto em `Main_Init`/`iOS_SetIconPosition`, seções
64/71).

### Confirma o primitivo real de cópia por trás de TODO o sistema `iOS_Resume*`

Só **3 `bl` distintos** em toda a função:
```
iOS_Resume_DataCopy(IOS_RESUME_DATACOPY_MODE, unsigned char*, unsigned char*, int)   ×149
iOS_Resume_DataCopyAddr(IOS_RESUME_DATACOPY_MODE, unsigned char*, unsigned char*, int) ×8
iOS_getLastEventNo()                                                                     ×1
```
`iOS_Resume_DataCopy` sendo chamada **149 vezes** confirma que esta
função é um **serializador campo a campo** de `IOS_RESUME_DATA_EVENT`:
cada chamada passa `(modo, endereço_do_campo_na_struct,
endereço_do_campo_no_buffer_global_de_resume, tamanho_do_campo)` —
inspeção do início da função confirma: primeira chamada copia 4
bytes do offset 0, segunda copia 4 bytes do offset 4, e assim por
diante. **A direção (salvar vs. restaurar) é controlada pelo
parâmetro `IOS_RESUME_DATACOPY_MODE`, passado direto pra
`iOS_Resume_DataCopy`** — não há um `if`/`else` nesta função
dividindo os dois casos; o primitivo compartilhado é que decide o
que fazer com o modo. `iOS_Resume_DataCopyAddr` (8 chamadas, bem
menos frequente) provavelmente trata os campos que são **ponteiros**
(precisam de tratamento de endereço diferente dos campos de valor
puro).

Isto fecha a pergunta em aberto desde a seção 32/41 (`battle()`/
`op_attackteam` citam `iOS_ResumeMusic`/`iOS_Resume_BGM`/
`iOS_ResumeGetMode`/`iOS_Resume`/`iOS_ResumeByAutoSave`/
`iOS_ResumeAfterAttackTeam`, nunca abertas): o sistema `iOS_Resume*`
é um mecanismo real de **salvar/restaurar estado ao suspender e
retomar o app** (clássico "process death" do Android — salvar
estado antes de o sistema matar o processo em segundo plano,
restaurar ao voltar), com um primitivo de cópia genérico e funções
de "topo" especializadas por sistema (música, efeito ambiente, modo
de batalha, auto-save, seleção de time de ataque) que devem seguir
a MESMA estrutura campo-a-campo confirmada aqui.

**O que ficou sem confirmar**: o layout exato de
`IOS_RESUME_DATA_EVENT` (quantos campos, quais tamanhos — não
enumerados um a um); o corpo de `iOS_Resume_DataCopy`/
`iOS_Resume_DataCopyAddr` em si (não lidas); se as outras funções
`iOS_Resume*` (música, batalha, etc.) seguem exatamente este mesmo
padrão campo-a-campo — hipótese plausível, não confirmada. Marcada
`read_structural`.

## 77. `setskillresult(int)` — passe estrutural — a função real que aplica o resultado de uma habilidade/golpe em batalha (2026-10-17, Fase 3, lote paralelo)

`setskillresult(int)` (`0x1cda4c`, 3.844 B) — nunca tocada antes
nesta investigação. Descida recursiva via `jtable.py`: **948 de
~961 instruções possíveis (99%)**, sem tabela de salto computada;
**149 branches, 65 de retrocesso**.

### Confirma ser o executor real de todos os efeitos colaterais de um golpe/habilidade

27 `bl` resolvidos, quase todos nomes nunca vistos nesta
investigação, todos girando em torno de `BWORK` (área de trabalho
de batalha, seções 43/72):

```
clear_setstatus(A_RESULT*)              check_reaction_deny_all(BWORK*)
bcp_roll(BWORK*)                            set_status_all(int, int)
change_status_adjust(int)                  check_charge(BWORK*, int)
clear_status_animation(BWORK*)             check_prob(int, int)
adjust_equip_change(BWORK*)                levelup_one(BWORK*, int)
levelup_check(BWORK*)                        get_unit_jl(BWORK*, int, int*)
add_jobpointB(int, int, unsigned char, int)  inc_party_item(BWORK*, unsigned short, BWORK*)
get_rival()                                    pspNetGetBattleModeFlag()
pspItemGetCommonData / pspItemIsEmpty / pspItemIsBarehand
```

Isto confirma, com nomes reais, que `setskillresult` é literalmente
a função que **aplica todas as consequências de um golpe/habilidade
de batalha depois que ele acerta**:

- **`A_RESULT*`** — tipo nunca visto, confirma uma struct real de
  "resultado de habilidade" (provavelmente dano, status a aplicar,
  flags de acerto/erro), consumida por `clear_setstatus`.
- **`check_reaction_deny_all(BWORK*)`** — checagem de habilidade de
  reação (ex.: "Auto-Potion"/"Counter" do FFT original) que pode
  anular o efeito.
- **`bcp_roll(BWORK*)`**/**`check_prob(int,int)`** — rolagens de
  probabilidade reais (nome "bcp" não decifrado por etimologia,
  tratado como está).
- **`set_status_all(int,int)`**/**`clear_status_animation`** —
  aplicação e limpeza de status alterado (poison, sleep, etc.).
- **`levelup_one(BWORK*,int)`/`levelup_check(BWORK*)`** — confirma
  que o **level-up de verdade pode acontecer como consequência
  direta de uma habilidade** (ex.: ganhar EXP ao acertar um golpe),
  nunca confirmado byte a byte antes — e a MESMA `levelup_one` já
  reaparece como ação de cheat em `debug_chrmenu` (seção 79).
- **`add_jobpointB(int,int,unsigned char,int)`**/**`get_unit_jl`** —
  confirma o ganho real de **JP (job points)**, ligando a esta
  função o mecanismo central de progressão de habilidade do FFT
  (sistema de job, seções 57/61).
- **`inc_party_item`**/`pspItemGetCommonData`/`pspItemIsEmpty`/
  `pspItemIsBarehand` — ganho de item (ex.: roubo, item largado por
  inimigo).
- **`adjust_equip_change(BWORK*)`** — ajuste de equipamento como
  efeito de habilidade (ex.: quebrar arma/armadura).
- `pspNetGetBattleModeFlag()` — mais uma aparição do sistema de
  batalha em rede (seções 41/43/63/72).
- `get_rival()` — nome sugere "unidade rival"; papel exato não
  confirmado.
- 7 funções locais sem símbolo (`sub_1c7934` ×6, `sub_1cc784`/
  `sub_1cc848` ×6 cada — provavelmente getters/setters de campo de
  `A_RESULT`/`BWORK`).

**O que ficou sem confirmar**: os corpos da cascata de 149 branches
(65 de retrocesso) — qual efeito é aplicado em qual ordem/condição
não foi mapeado; o layout de `A_RESULT`; o papel exato de
`get_rival`/`bcp_roll`. Marcada `read_structural`.

## 78. `disp_helpmenu()`/`Wdisp_helpmenu()` — passe estrutural — revela um sistema de mensagens LZW nunca visto, e confirma que os DOIS padrões de duplicação por letra coexistem (2026-10-17, Fase 3, lote paralelo)

`disp_helpmenu()` (`0x1255e0`, 4.628 B) — descida recursiva via
`jtable.py`: **1.114 de ~1.157 instruções possíveis (96%)**, sem
tabela de salto; **93 branches, 42 de retrocesso**.

### Confirma o padrão "entrada fina reusando helpers compartilhados" — igual a `disp_bothwindow` (seção 73), diferente de `disp_personalwindow`

`disp_helpmenu` chama `addlocalprim`/`initpolyft4` nos MESMOS
endereços sem prefixo já vistos em `disp_personalwindow`/
`disp_bothwindow` (seções 46/73) — não tem cópia própria dos
helpers de desenho. Família de task é `asm` (`asmGetInput1`/
`asmGetInput3`), consistente com o padrão "sem prefixo de tela =
task sem `w`".

### Achado novo: sistema de mensagens LZW nunca catalogado

**`pspMsgLzwBaseGet(FFTPSP_MSG_LZW)`** — confirma que (pelo menos
parte d)o texto de ajuda do jogo é armazenado **compactado via LZW**
(Lempel-Ziv-Welch), um formato de compressão nunca mencionado nesta
investigação (distinto do `CCOMP_Z_*`/zlib já documentado nas seções
18/18.1/31/69). Outros achados: `get_cursoroffset(int)`,
`import_localstatus`, `checktaskkind` (×4), `iOS_hookHelp(int*)` —
ponto de integração com o sistema de ajuda contextual da UI
(`iOS_*`) — e mais uma aparição de `pspNetGetBattleModeFlag()`
(seções 41/43/63/72).

### `Wdisp_helpmenu()` — checagem oportunista: aqui `W` É uma cópia real (padrão diferente de `disp_bothwindow`)

`Wdisp_helpmenu()` (`0x127360`, 4.808 B, 96% de cobertura, sem
tabela de salto) tem sua PRÓPRIA cópia `W`-prefixada de TODOS os
helpers (`Waddlocalprim`, `Winitpolyft4`, `Wimport_localstatus`,
`Wget_cursoroffset`, `Wchecktaskkind`, `Wtask_wait`/`Wtask_create`/
`Wsend_taskparamater`) — e usa a família de task `wasm`
(`wasmGetInput1`/`wasmGetInput3`), não `asm`. **Confirma que os dois
padrões de duplicação por letra (cópia real vs. entrada fina)
coexistem em famílias diferentes do mesmo binário** — `disp_helpmenu`
segue o padrão "entrada fina" (como `disp_bothwindow`, seção 73),
enquanto `Wdisp_helpmenu` segue o padrão "cópia real correlacionada
com `wasm`" (como `Wdisp_personalwindow`, seção 47). `pspMsgLzwBaseGet`
é chamada SEM prefixo mesmo dentro de `Wdisp_helpmenu` — confirma que
funções de acesso a dado (não helpers de desenho) são sempre
compartilhadas, independente da letra.

**O que ficou sem confirmar**: os corpos da cascata de branches em
ambas; o formato exato do LZW de mensagem. Marcadas `read_structural`
(`disp_helpmenu` e `Wdisp_helpmenu`).

## 79. `debug_chrmenu()` — passe estrutural — menu de debug real para batalha, com "level up" direto (2026-10-17, Fase 3, lote paralelo)

`debug_chrmenu()` (`0xd1ab0`, 4.244 B) — nunca tocada. Descida
recursiva via `jtable.py`: **1.001 de ~1.061 instruções possíveis
(94%)**, sem tabela de salto; **54 branches, 29 de retrocesso**.

### Confirma ser um menu de debug real, com ação de "subir nível" direta numa unidade

```
get_bwp(int)                    — pega o ponteiro de área de trabalho de batalha (seção 43)
search_controlID(int, int*)     — já visto na seção 43 (requireprinf)
levelup_one(BWORK*, int)        — a MESMA função confirmada em setskillresult (seção 77)
task_create/task_wait/send_taskparamater/asmTaskEntry  — a própria tela roda como task
```
`levelup_one(BWORK*, int)` é o achado central: confirma uma ação
real de debug/cheat que força o level-up de uma unidade de batalha
específica, operando direto sobre a estrutura `BWORK` — a MESMA
função que `setskillresult` (seção 77) chama como consequência
normal de uso de habilidade, agora confirmada como também acessível
via um menu de debug direto (bypass do fluxo normal de jogo). A
função itera sobre um conjunto de unidades (loop com `r4`
incrementando, chamando `get_bwp(r4)` por unidade), escrevendo flags
byte a byte num buffer de controle — consistente com uma tela que
lista as unidades em campo e permite escolher uma pra aplicar a ação
de debug. A própria tela é implementada como task cooperativa (mesmo
padrão já visto em telas de evento, seções 41/61), reforçando que o
sistema de task é usado para UI em geral, não só diálogo.

**O que ficou sem confirmar**: os corpos das 4 funções locais sem
símbolo (`sub_cc794`, `sub_cc950` ×8, `sub_ccbc8` ×10 — as mais
chamadas, prováveis getters/setters de campo de debug ou de desenho
de texto do menu); se existem outras ações de debug além de "level
up". Marcada `read_structural`.

## Terceiro lote paralelo (seções 80–84): mais 5 funções lidas por forks simultâneos

## 80. `worldmap_call(unsigned long*, unsigned long)` — passe estrutural — confirma ser o `event_call` do mapa mundi (2026-10-17, Fase 3, lote paralelo)

`worldmap_call(unsigned long* script, unsigned long pc)`
(`0x156bec`, 3.520 B) — mesma assinatura clássica de interpretador
de bytecode já confirmada em `event_call` (seção 66). Descida
recursiva via `jtable.py`: **814 de ~880 instruções possíveis
(92%)**, sem tabela de salto; **72 branches, 36 de retrocesso**.

### Confirma a hipótese: é o dispatcher de ações de bytecode específico do mapa mundi

26 `bl` resolvidos, a maioria ligando diretamente a sistemas do
motor `wld_*` (Fases 1/2, seções 9–12) e a telas já documentadas
nesta Fase 3:
```
worldmap_restart()                       — chamada 9 vezes, de longe a mais frequente
wldframe_clr(int) / wldfade_set(int, int)   — motor wld_* original (seção 12.8)
CardAccess(int)                              — tela de save/load (seção 42)
UnitList(int, int)                            — lista de unidades (seção 56)
changewindowamb(int, int, int)             — já visto em wldfade_proc (seção 12.8)
pspWorldCheckFlg(PSP_WORLD_FLG)            — já visto em wldtown_bright (seção 12.12)
numa_fileReadCD(unsigned long, unsigned long, void*)  — já visto em requireprinf (seção 43)
pspNetEntranceOptionInit()                   — achado novo, liga ao sistema de batalha em rede
request_worldwindow(int,int,int,int) / request_worldcommand(int,int,int)  — achados novos
```
Confirma, com evidência cruzada forte, que `worldmap_call` é
literalmente **o `event_call` do mapa mundi**: um opcode de
bytecode aqui pode abrir `CardAccess` (save/load), abrir `UnitList`,
reiniciar o estado do mapa mundi (`worldmap_restart`, 9× — provável
opcode "voltar ao mapa" chamado de vários pontos), limpar o frame,
disparar fade de janela, e inicializar opções de entrada em batalha
de rede. `request_worldwindow`/`request_worldcommand` sugerem um
sistema de fila de comandos específico do mapa mundi, paralelo ao
`multiwindow_*` já visto em telas (seções 54/58/67/74) mas num nível
mais alto (comandos de mapa, não pacotes de sprite). Família de task
é `wasm` aqui (`wasmTaskEntry`/`wasmGetActiveTask`), não `asm`.

**O que ficou sem confirmar**: os corpos da cascata de 72 branches
(36 de retrocesso) — qual opcode dispara qual chamada não foi
mapeado; a estrutura exata de `request_worldwindow`/
`request_worldcommand`. Marcada `read_structural`.

## 81. `ASHURA_GNS_Garage(long, unsigned long)` — passe estrutural — confirma `GNS` como o formato real de mapa do FFT original, carregado assincronamente (2026-10-17, Fase 3, lote paralelo)

`ASHURA_GNS_Garage(long, unsigned long)` (`0x16e7c8`, 3.504 B) — já
citada na seção 66 (catálogo de `event_call`) como uma das três
funções `ASHURA` específicas de evento, nunca aberta por dentro.
Descida recursiva via `jtable.py`: **801 de ~876 instruções
possíveis (91%)**; uma tabela de salto resolvida (32 casos, só 7
endereços distintos — a maioria colapsa num único handler de
"espera", mesmo padrão já visto em `battle()`, seção 32.2); **107
branches, 65 de retrocesso**.

### Confirma `GNS` como formato real de mapa do FFT original (fato documentado na comunidade de modding do jogo, não hipótese)

```
ASHURA_GNS_Read(unsigned short)              ASHURA_GNS_Analyzer(unsigned long, unsigned long)
ASHURA_MapProjectFlag(char, short, short)       ASHURA_MapProjectMem2Mem(unsigned char, char*)
ASHURA_FileRead_Proto(char const*, char*, char*, unsigned long)
ASHURA_LMDL_DB_COPY(unsigned short*)            ASURA_WorkInit()
FFTPSP_ASURA_polygon_combine(unsigned int, ADB*, SVECTOR*, SVECTOR*, SVECTOR*, SVECTOR*)
fileReadCheck() / mallocForFile(unsigned int) / freeForFile(void*)
```
`GNS` é o formato real dos arquivos de **índice de geometria de
mapa** do FFT original de PS1 (par de arquivos GNS/GSD por mapa —
fato documentado publicamente na comunidade de ROM-hacking do jogo,
não uma suposição desta investigação). `ASHURA_GNS_Garage` confirma
ser um **carregador assíncrono multi-estado** de um mapa `GNS`
específico: a máquina de 32 estados passa por fases como "esperar
leitura de arquivo terminar" (`fileReadCheck()`, estado 0, confirmado
por instrução: se o resultado ainda está pendente, volta pro estado
de espera; se terminou, avança), análise do arquivo
(`ASHURA_GNS_Analyzer`), projeção de mapa
(`ASHURA_MapProjectFlag`/`Mem2Mem`), e cópia de dados de modelo
(`ASHURA_LMDL_DB_COPY` — mesma família de `ASURA_LMDL_TIME_TBL`,
seção 38). **"Garage" no nome é quase certamente o nome de uma
cena/mapa específico** (um local chamado "garagem" na história,
carregado por esta instância do loader genérico) — hipótese
plausível dado o padrão de nomes de função por cena já visto em
outras famílias, não confirmada sem achar o ID do mapa real.

**`FFTPSP_ASURA_polygon_combine(...)`** é um achado notável à parte:
o prefixo **`FFTPSP`** (Final Fantasy Tactics PSP) nomeia o
jogo+plataforma diretamente na função — reforça, com ainda mais
força que a seção 59 (`GuEmu_libgu_to_gl`), que este binário tem
raiz real no port de **PSP**, não só PS1. `ASURA_WorkInit()` confirma
mais uma vez a grafia sem H ("ASURA") já catalogada desde
`ASURA_LMDL_TIME_TBL` (seção 38).

**O que ficou sem confirmar**: os corpos dos 7 handlers de estado
restantes (estado 0 foi o único lido por instrução); o ID/nome real
do mapa "Garage"; o layout de `ADB`. Marcada `read_structural`.

## 82. `executeShape(tag_animation*)` — passe estrutural — o interpretador de "comandos de forma" dentro do sistema de animação (2026-10-17, Fase 3, lote paralelo)

`executeShape(tag_animation*)` (`0x1f1680`, 3.924 B) — descida
recursiva via `jtable.py`: **924 de ~981 instruções possíveis
(94%)**, uma tabela de salto resolvida (45 casos, 25 endereços
distintos); **107 branches, 69 de retrocesso**.

### Confirma ser um interpretador de opcode de "comandos de forma", dentro do motor de animação, chamado por `executeAnimationProgram`

```
executeAnimationProgram(tag_animation*)        — chama executeShape (confirma a relação de hierarquia)
searchAnimationByID(unsigned short)
setAnimationRealVector(SVECTOR*, tag_animation*)
setShapeDataSub(tag_animation*, subAnimation*, unsigned short, unsigned short)
callAnimationSound(tag_animation*, int)
requestParmanentEffect(tag_animation*)          — mesmo erro de digitação ("Parmanent") já catalogado no espírito de ASURA/changeflame
pspItemGetWeaponVariationBlock / pspItemGetWeaponClut
errorHandler(int)
```
A tabela de 45 casos colapsa em 25 endereços distintos — confirma
uma máquina de estados com um "opcode de comando de forma" por caso,
consistente com um mini-interpretador de bytecode de animação
(paralelo em espírito ao `event_call`/opcodes do motor de eventos,
seção 66, mas num nível mais baixo, dentro de UMA animação).
`searchAnimationByID`/`setShapeDataSub` confirmam que a animação é
dirigida por dados (tabela de sub-animações buscada por ID);
`setAnimationRealVector` aplica posição/transformação real por
quadro. `callAnimationSound` confirma que animações podem disparar
efeito sonoro em quadros específicos (cue de som sincronizado).
`requestParmanentEffect` liga este sistema ao
`InitPermanentEffect`/`DoEffect` já vistos no catálogo de `battle()`
(seção 32). `pspItemGetWeaponVariationBlock`/`pspItemGetWeaponClut`
confirmam que a animação de uma unidade pode variar visualmente
conforme a **arma equipada** (modelo/paleta diferente por arma).

**O que ficou sem confirmar**: os corpos dos 25 handlers distintos
(qual comando de forma faz exatamente o quê); os corpos das 7
funções locais sem símbolo (`sub_1f0c70` ×7, a mais chamada).
Marcada `read_structural`.

## 83. `DoEffectCameraWork()` — passe estrutural — o sequenciador real de câmera com interpolação suave e tremor, pra eventos/cutscenes (2026-10-17, Fase 3, lote paralelo)

`DoEffectCameraWork()` (`0x219728`, 3.740 B) — descida recursiva via
`jtable.py`: **905 de ~935 instruções possíveis (97%)**, sem tabela
de salto; **142 branches, 85 de retrocesso** (consistente com laços
de interpolação por frame).

### Confirma ser o executor de "trabalho de câmera" roteirizado — a peça que faltava entre `event_call` e a câmera do mapa mundi

`setMapScrollXYZ`/`setMapScale`/`setMapAngle` (10/10/11 chamadas) —
as MESMAS três funções já vistas como callees de `event_call`
(seção 66) e do sistema de câmera do mapa mundi (seções 12.11/
12.14) — confirmam que `DoEffectCameraWork` controla
especificamente a câmera do **mapa mundi**, não a `CCAMERA` moderna
(seção 65) nem a pilha GTE crua de `ASHURA` (seções 38/48).

**Confirma interpolação suave real com curvas de easing**:
```
getSmoothSVECCosPai / getSmoothSVECCos2Pai / getSmoothSVECLinear
getSmoothVECCosPai  / getSmoothVECCos2Pai  / getSmoothVECLinear
```
Seis variantes (SVECTOR de ângulo × VECTOR de posição, cada uma com
3 curvas: cosseno de meia-volta, cosseno de volta completa, linear)
— confirma que o jogo tem um sistema real de **ease-in/ease-out**
pra movimento de câmera roteirizado, não interpolação linear
simples.

**Confirma tremor de câmera real (camera shake)**:
```
AddRndVECTORToVECTOR / AddRndVECTORToVECTORShift12 / AddRndSVECTORToSVECTOR
AddVECTORToVECTOR / AddVECTORToVECTORShift12 / AddSVECTORToSVECTORAnd0xfff
```
As variantes `Rnd` (random) somam um deslocamento aleatório ao vetor
de posição/ângulo da câmera — tremor de câmera real, provavelmente
pra efeitos de impacto/explosão em cutscenes. `Shift12` confirma
aritmética de ponto fixo 12 bits (padrão PS1); `And0xfff` em
`SVECTOR` confirma wraparound de ângulo (0–4095 = 0–360°, mesmo
esquema angular do GTE do PS1).

**O que ficou sem confirmar**: os corpos da cascata de 142 branches
(85 de retrocesso) — a fonte exata dos dados de keyframe (tabela de
script roteirizado, não identificada); se o tremor é condicional a
um parâmetro de evento específico. Marcada `read_structural`.

## 84. `GlobalName(unsigned char*, unsigned char*)` — passe estrutural parcial — a tela real de nomear unidade, com widget de rolagem de letras (2026-10-17, Fase 3, lote paralelo)

`GlobalName(unsigned char*, unsigned char*)` (`0x1a17e8`, 3.764 B) —
nunca tocada antes. Descida recursiva via `jtable.py`: **728 de
~941 instruções possíveis (77%)**, sem tabela de salto computada
(verificado: nenhum branch computado pendente, o gap é provavelmente
pool de literais de GOT); **29 branches, 13 de retrocesso**.

### Confirma a tela de nomear unidade, desenhada com primitivas PS1 cruas (não via `DB`/`multiwindow_*`)

```
iOS_SetScrollNameFunc(unsigned char)     — nunca vista
unit_isdark() / MasaDataInit()              — novas
VSync / DrawSync / ClearOTag / AddPrim / DrawOTag
PutDrawEnv / PutDispEnv / GetDrawEnv / SetDefDispEnv / SetDefDrawEnv
pspPrimBackDraw(int,int,ushort,ushort,ulong*,uchar*)
GuEmu_SetLineInterval(int)
iOS_dispOkNg(int,int) / iOS_clearOkNg()
worldmap_restart()
```
A assinatura (dois `unsigned char*`, provavelmente destino/origem do
buffer de nome) e **`iOS_SetScrollNameFunc`** confirmam que esta é a
tela real de **dar nome a uma unidade** (recruta nova ou edição de
nome), usando um widget de **rolagem de letras** — padrão clássico
de telas de nomeação de jogos PS1 (escolher letra por letra numa
lista/roda rolável). Diferente da maioria das telas já documentadas
(que usam o buffer `DB`/sistema `multiwindow_*`, seções 36/42/45/54),
esta desenha com chamadas **diretas e cruas da lib gráfica PS1**
(`VSync`/`DrawSync`/`ClearOTag`/`AddPrim`/`DrawOTag`/`PutDrawEnv`/
`PutDispEnv`/`GetDrawEnv`/`SetDef*Env`) — mais um caminho de desenho
independente nesta investigação, parecido com o confirmado em
`disp_personalwindow` (seção 46) mas com ainda mais chamadas de
baixo nível de setup de ambiente gráfico (`PutDrawEnv`/`PutDispEnv`/
`GetDrawEnv`, nunca vistas antes). `GuEmu_SetLineInterval` confirma
mais uma função da ponte PSP↔GL já documentada na seção 59.
`iOS_dispOkNg`/`iOS_clearOkNg` (mesmo diálogo Sim/Não das seções
42/56) sugerem uma confirmação final do nome escolhido.
`worldmap_restart()` sugere que esta tela também pode ser acessada a
partir do mapa mundi (ex.: ao recrutar uma unidade numa cutscene).

**O que ficou sem confirmar**: os ~23% restantes da função; o
formato exato do widget de rolagem de letras; se `unit_isdark`/
`MasaDataInit` têm relação direta com esta tela ou são só
utilitários genéricos chamados de passagem. Marcada
`read_structural` — cobertura parcial, não forçada.

## Quarto lote paralelo (seções 85–89): mais 5 funções lidas por forks simultâneos

## 85. `sBattleTouchToCur(int)` — passe estrutural — confirma o tradutor real de toque pra cursor de batalha, com deslizamento suave e matemática trigonométrica real (2026-10-17, Fase 3, lote paralelo)

`sBattleTouchToCur(int)` (`0x15c15c`, 3.284 B) — já citada no
catálogo de `battle()` (seção 32), nunca aberta por dentro. Descida
recursiva via `jtable.py`: **784 de ~821 instruções possíveis
(95%)**, sem tabela de salto; **115 branches, 80 de retrocesso**
(consistente com um laço de atualização por frame).

### Confirma a tradução real de toque em movimento de cursor, com sistema de deslizamento suave

```
iOSSlideNaviCurClear() / iOSexecuteCurSlide() / iOSSlidStop()
iOSSlideSpeed(int*, int*, double, double) / iOSSlideSpeedGet(int)
iOSSlideBufSetX(int) / iOSSlideBufSetY(int) / iOSSlidBUfDel()
iOSSlideIconReset() / iOSMapCursorCheck() / iOSMapCurModeGet()/Set(int)
iOSTchInputCheck() / iOSTchMovingModeCheck() / iOSRotSlidCls()
rsin / rcos / ratan2
iOS_getTouchTap/Release/Press/BeginX/BeginY/NowX/NowY
IS_GAME_AREA(int,int) ×8
```
Confirma, com nomes reais, que esta função é o **tradutor direto de
gesto de toque em movimento do cursor de batalha**: lê a posição/
arrasto do toque (`iOS_getTouchNowX/Y`, `iOS_getTouchBeginX/Y`),
valida se está dentro da área de jogo (`IS_GAME_AREA` ×8), e
alimenta um sistema de **deslizamento suave com velocidade própria**
(`iOSSlideSpeed`/`iOSSlideSpeedGet`/`iOSSlideBufSetX/Y`) — ou seja,
o cursor não salta direto pro tile tocado, ele desliza com
velocidade/momento, como confirmado pelo nome "Slide". **`rsin`/
`rcos`/`ratan2` reais** (mesma família trigonométrica já vista em
`Mdl0010`, seção 52) sugerem que a direção do deslizamento é
calculada via ângulo real do vetor de arrasto do toque (`atan2`
entre início e posição atual do toque), não só um delta XY cru.
`iOSMapCursorCheck`/`iOSMapCurModeGet/Set` ligam este sistema ao
modo de cursor do mapa de batalha; `iOSTchMovingModeCheck` sugere um
estado "em movimento" vs. "parado" explícito.

**O que ficou sem confirmar**: os corpos da cascata de 115 branches
(80 de retrocesso) — a fórmula exata de aceleração/desaceleração do
deslizamento não foi lida byte a byte. Marcada `read_structural`.

## 86. `Link_FrameRender()` — passe estrutural — revela `CUI_SCROLLBAR`, uma classe de UI de lista rolável nunca vista (2026-10-17, Fase 3, lote paralelo)

`Link_FrameRender()` (`0x2b4680`, 3.636 B) — descida recursiva via
`jtable.py`: **891 de ~909 instruções possíveis (98%)**, sem tabela
de salto; **21 branches, 11 de retrocesso**.

### Corrige a hipótese inicial: não é renderização de link-cable/rede

Apesar do nome sugerir o cabo serial de link do PS1 (sistema de
rede já confirmado em outras seções via `pspNetGetBattleModeFlag`/
`NetBattleJudge`, seções 36/41/43/63/80), `Link_FrameRender` não
toca nenhuma dessas funções. É uma tela de UI desenhada inteiramente
via o motor moderno `CEGL2_*` (`SetScreenSize`/`ClearBackdrop`/
`DrawPacket`/`AddSprite`/`AddTile`/`CEGL2_FBO::*`), sem nenhuma
primitiva PS1 — "Link" aqui é mais provavelmente **link de
hiperlink/promocional** (ex.: tela "outros apps"/crédito com links
externos clicáveis), não o cabo serial — hipótese, não confirmada
sem achar o texto/URL real.

### Achado maior: revela `CUI_SCROLLBAR`, classe de UI nunca catalogada

```
CUI_SCROLLBAR::GetScissor() / GetScrollOffset(int*,int*)
CUI_SCROLLBAR::IsEnableScrollUp() / IsEnableScrollDown()
CUI_SCROLLBAR::GetCellRect(int) / GetCellPress(int) / GetCellDraw(int)
```
Confirma uma classe C++ real de **barra de rolagem com lista de
células** (scissor/clip, offset de rolagem, estado habilitado/
desabilitado de cada seta, retângulo/toque/desenho por célula) —
nunca vista nesta investigação, apesar de o jogo ter várias telas
com listas (itens, habilidades, unidades) já documentadas usando
sistemas mais antigos (`UnitTable`/`iOSUnitList*`, seções 55/56).
`CUI_SCROLLBAR` parece ser um widget de lista mais moderno, talvez
exclusivo de telas de UI de app (não de gameplay PS1-emulado).

Também confirma `CSTEP_BATCH::GetData()` (sistema de animação por
passos, seções 16/17) e `RETINA_SCALE`/`CGX_SCREEN_CORRECT::*`
(seção 34) sendo usados aqui — mais um cliente do sistema de
correção de tela por dispositivo.

**O que ficou sem confirmar**: o conteúdo real da tela (que link(s)
mostra); os corpos dos 21 branches; se `CUI_SCROLLBAR` é usada em
outras telas além desta. Marcada `read_structural`.

## 87. `ctlopentitle_main(CTLINFO*)` — passe estrutural — confirma a tela de título real, com filme de abertura via CD-XA (2026-10-17, Fase 3, lote paralelo)

`ctlopentitle_main(CTLINFO*)` (`0x246450`, 3.296 B) — fase "main" do
controlador de tela de título (`CTLINFO*`, mesma arquitetura
polimórfica `init/active/main/deactive` já confirmada nas seções
9.6/12.2). Descida recursiva via `jtable.py`: **793 de ~824
instruções possíveis (96%)**, duas tabelas de salto pequenas (5/5 e
4/3 casos); **70 branches, 35 de retrocesso**.

### Confirma a tela de título real, com reprodução de filme via CD-XA do PS1

```
CdControl / CdControlB / CdPosToInt / CdSync       — BIOS de CD-ROM do PS1 real
cdxa_stop() / movie_exit(int)                         — encerra o filme de abertura
vOpn_scrinit / vOpn_fadeout / vOpn_key_rep / vOpn_SetCDVolume / vOpn_loadwait / vOpn_bk_load
ctlopentitle_init(int) / ctlopentitle_deactive(CTLINFO*)
ctlsound_init() / ctlcard_init() / CardAccess(int)
wldbin_loadchk(int)                                     — checagem de save do mapa mundi (citada desde a Fase 1, nunca aberta)
pspClearCurrentSystemFile()
```
Confirma, com chamadas reais de BIOS (`CdControl`/`CdSync`), que a
tela de título reproduz um **filme de abertura via CD-XA** (áudio/
vídeo direto do CD, técnica clássica do PS1) — `vOpn_*` (provável
"video opening") controla volume/fade/carregamento desse filme.
Depois do filme, `ctlopentitle_main` decide entre: ir pro teste de
som (`ctlsound_init`), ir pra tela de save/load
(`ctlcard_init`/`CardAccess`, seção 42), ou continuar pro jogo —
`wldbin_loadchk` sugere que essa decisão depende de existir um save
de mapa mundi válido. `pspClearCurrentSystemFile()` confirma reset
de arquivo de sistema (provável limpeza de estado ao voltar pro
título). `iOS_setV2Icon` chamada 42 vezes — mais uma instância do
padrão de inicialização de ícones em massa (seções 64/71).

**O que ficou sem confirmar**: os corpos dos handlers das duas
tabelas de salto; a ordem exata das transições entre filme → menu →
save/som. Marcada `read_structural`.

## 88. `p04_magicChantFunc()` — passe estrutural — o efeito visual/sonoro real do canto de magia, com objeto 3D persistente (2026-10-17, Fase 3, lote paralelo)

`p04_magicChantFunc()` (`0x2210fc`, 3.176 B) — descida recursiva via
`jtable.py`: **777 de ~794 instruções possíveis (98%)**, sem tabela
de salto; **43 branches, 28 de retrocesso**.

### Confirma o efeito visual/sonoro real da fase de "canto" (chant) de magia

```
createPermanentObject(_JochuParameter*, Physics*)   GetPermanentObject()
AnimatePermanentObject(int)                              DisposePermanentObject(char)
SetAirDensity(long) / PushAirDensity()
Ssd_PlayEffect(long) / Ssd_StopEffect(long)
ConvertEffectAttribute(int)
rsin/rcos/ratan2/RotTrans/SetRotMatrix/SetTransMatrix       — GTE real
```
Confirma, com nomes reais, que o "canto" de magia do FFT (delay de
conjuração proporcional ao CT, mecânica clássica da série) tem um
**objeto 3D persistente real** (`createPermanentObject`, usando dois
tipos nunca vistos, `_JochuParameter*` — etimologia não decifrada,
tratada como está — e `Physics*`) — provavelmente o círculo/glifo
mágico que fica girando sob o conjurador durante o canto, usando
matemática GTE real (`rsin`/`rcos`/`RotTrans`) pra rotação contínua.
`SetAirDensity`/`PushAirDensity` sugerem um parâmetro de física
atmosférica (densidade do ar) afetando partículas/poeira do efeito.
`Ssd_PlayEffect`/`Ssd_StopEffect` ligam este efeito ao sistema `Ssd`
já confirmado como a máquina de estados de música do mapa mundi
(`wldssd_control`, seção 12.7) — **mas aqui usado pra efeito sonoro,
não música**, confirmando que o `Ssd` é um gerenciador de áudio mais
geral do que o nome "música de fundo" sugeria. `AnimatePermanentObject`/
`DisposePermanentObject` confirmam o ciclo de vida completo (criar →
animar → descartar) do mesmo tipo de objeto persistente já citado
por `requestParmanentEffect`/`InitPermanentEffect`/`DoEffect`
(seções 32/82) — aqui com o corpo real aberto por completo.

**O que ficou sem confirmar**: os corpos da cascata de 43 branches
(28 de retrocesso); o layout de `_JochuParameter`/`Physics`; se
existem funções irmãs `p01`/`p02`/`p03`/`p05` (não pesquisadas no
`.dynsym` nesta passada). Marcada `read_structural`.

## 89. `NewAnimation(int, int, int, short, short, short, short, BWORK*, int, void*)` — passe estrutural — confirma ser o ponto real de criação de instância de animação, ligando `executeShape`/`setskillresult`/sistema de arma (2026-10-17, Fase 3, lote paralelo)

`NewAnimation(...)` (`0x1f3828`, 3.096 B) — descida recursiva via
`jtable.py`: **766 de ~774 instruções possíveis (99%)**, sem tabela
de salto; **60 branches, 28 de retrocesso**.

### Confirma ser o ponto real de criação de animação, com buscas de dados por categoria

```
getShapeAddress(unsigned short) / getSequenceAddress(unsigned short)
getWpnShapeAddress(unsigned short) / getWpnSequenceAddress(unsigned short)
getEffShapeAddress() / getEffSequenceAddress()
getPositionFromPanel(tag_animation*)
requestDefaultColor(tag_animation*,int,int) / requestDefaultAnimation(tag_animation*)
NewWeaponEquip(int, tag_animation*)
requestDamageResult(int)
Resume_Get_WORK_MU_BWorkFontID() / Resume_Get_WORK_MU_BWorkAnimationID()
CFFT_STATE::UnitIDToFID_SPR(int)
loadClutData / LoadTPage / GetTPage / GetClut / xpLibgpuExVramSet
init_status_animation(int) / iOS_setTransFace(int,int) / pspBattleDataCharTexBufGet(int)
```
Confirma, com nomes reais, que esta é a função que **instancia uma
nova animação de verdade**, buscando os dados certos por categoria
(unidade/arma/efeito, cada um com par forma+sequência —
`getShapeAddress`/`getSequenceAddress` e variantes `Wpn`/`Eff`) —
liga diretamente ao interpretador `executeShape` (seção 82), que
consome esses mesmos dados. `NewWeaponEquip(int, tag_animation*)`
confirma que a arma equipada influencia a animação já na criação,
reforçando o achado da seção 82 (`pspItemGetWeaponVariationBlock`).
**`requestDamageResult(int)`** é o achado mais importante: liga esta
função DIRETAMENTE a `setskillresult` (seção 77) — confirma que
criar uma animação de golpe também enfileira a exibição do resultado
de dano, fechando o ciclo "golpe → animação → resultado visível".
`Resume_Get_WORK_MU_BWorkFontID`/`BWorkAnimationID` ligam esta
criação de animação ao sistema de resume
(`IOS_RESUME_DATA_WORK_MU`, par de `iOS_RESUME_SET_EVENT`, seção
76) — confirma que o ID de animação em curso faz parte do estado
salvo ao suspender o app. `CFFT_STATE::UnitIDToFID_SPR` é uma
função nova da família de ponte de ID de rosto/sprite (seção 22.5).
`loadClutData`/`LoadTPage`/`xpLibgpuExVramSet` confirmam
carregamento real de textura/CLUT pra a nova animação.

**O que ficou sem confirmar**: os corpos da cascata de 60 branches
(28 de retrocesso); os 3 campos int/4 campos short do parâmetro (não
nomeados individualmente). Marcada `read_structural`.

## Quinto lote paralelo (seções 90–93): mais 4 funções lidas por forks simultâneos (a 5ª, `FundamentalRoutine`, foi pro `AI_DIFFICULTY_RESEARCH.md` seção 28 — território de IA)

## 90. `calc_result(ACT*, unsigned char)` — passe estrutural — o despachante real de tipo de ação, logo antes de `setskillresult` (2026-10-17, Fase 3, lote paralelo)

`calc_result(ACT*, unsigned char)` (`0x1cba40`, 2.996 B) — vizinha
imediata de `setskillresult` (seção 77, `0x1cda4c`) em endereço, com
um novo tipo `ACT*` ("action", nunca visto). Descida recursiva via
`jtable.py`: **668 de ~749 instruções possíveis (89%)**, duas
tabelas de salto resolvidas (11 casos/8 distintos; 25 casos/18
distintos); **86 branches, 58 de retrocesso**.

### Confirma ser o despachante por TIPO de ação, não a fórmula de dano em si

```
set_ct_weapon(ACT*)                          — define o CT (charge time) a partir da arma
check_reaction_deny(BWORK*) / check_reaction_deny2(BWORK*)   — checagens de reação (seção 77)
bcp_roll(BWORK*) / check_act_ok(BWORK*)          — rolagem de probabilidade / validação de ação (seção 77)
copyACTst(ACT*, ACT*)                              — confirma `ACT` como struct real, copiável
get_fusui_ability(BWORK*)                            — achado novo ("fusui", termo japonês não decifrado)
get_timing_true() / get_rival()                      — já visto em setskillresult (seção 77)
pspItemGetCommonData/OptionData/WeaponData/ItemData/IsEmpty/IsType/IsDataType
pspNetGetBattleModeFlag()
```
Duas tabelas de salto grandes (11 e 25 casos) dominam a função —
confirma que `calc_result` **despacha por tipo de ação/arma/item**
(provavelmente o `unsigned char` do segundo parâmetro é o
discriminador), delegando pra lógica específica em cada handler, em
vez de calcular dano numa fórmula linear única. `set_ct_weapon`
confirma que o tempo de recarga (CT) depende da arma equipada,
mecânica central do sistema de turnos do FFT. `get_fusui_ability` é
um achado honesto não decifrado — "fusui" (風水, fengshui) sugere
ligação com elemento/terreno, mas não confirmado sem ler o corpo.
Compartilha quase todo o catálogo `pspItem*`/`check_reaction_deny`/
`bcp_roll`/`get_rival`/`get_timing_true` com `setskillresult` (seção
77) — as duas funções claramente operam em sequência no mesmo fluxo
de resolução de ação de batalha, `calc_result` decidindo O QUE
aconteceu, `setskillresult` aplicando as consequências.

**O que ficou sem confirmar**: os corpos dos 8+18 handlers das duas
tabelas (qual tipo de ação/arma cai em qual); a fórmula de dano em
si (não encontrada como chamada separada, pode estar inline); o
papel exato de `get_fusui_ability`. Marcada `read_structural`.

## 91. `ASHURA_Animation()` — passe estrutural parcial — confirma rotação de cor de paleta real e um switch de 130 casos quase todo colapsado (2026-10-17, Fase 3, lote paralelo)

`ASHURA_Animation()` (`0x166ee0`, 2.976 B) — já citada no catálogo
de `battle()` (seção 32) como uma das funções do motor `ASHURA`,
nunca aberta por dentro. Descida recursiva via `jtable.py`: **604
de ~744 instruções possíveis (81%)**, uma tabela de salto resolvida
(**130 casos, só 12 endereços distintos** — a enorme maioria
colapsa num único handler, consistente com o padrão "switch grande
com default dominante" já visto em `battle()`/`ASHURA_GNS_Garage`,
seções 32/81); **23 branches, 20 de retrocesso**.

### Confirma ser o avanço de animação por frame do lado "efeito"/ambiente do ASHURA, com rotação de cor de paleta real

Só 6 `bl` distintos em toda a função:
```
iOS_GetFrameRateNative()           ×7
loadClutData(unsigned short*, unsigned int, unsigned int, int)   ×4
startColorRotation(int, int, int, int)
AddPrim                             ×2
system_warning(int, int)
```
**`startColorRotation(int,int,int,int)`** é o achado central —
nunca vista antes nesta investigação, confirma uma técnica clássica
de efeito visual de era PS1: **rotação cíclica de entradas de
paleta (CLUT)** por frame, sem precisar mudar geometria nem textura
(usada tipicamente pra água, lava, luzes pulsantes).
`iOS_GetFrameRateNative()` chamada 7 vezes confirma que o ritmo da
animação é regulado pelo framerate real do dispositivo, não por um
contador fixo. `loadClutData` liga este efeito ao sistema de paleta
já visto em `NewAnimation` (seção 89). Dado o nome genérico (sem
"set_Mesh"/"addPrim" específico) e o switch de 130 casos
majoritariamente vazio, a hipótese mais provável é que esta função é
um **despachante de tipo de animação de efeito ambiente** chamado
uma vez por frame pra cada objeto ASHURA ativo, com a maioria dos
"tipos" não implementando nada além do avanço de frame padrão e só
alguns tipos (rotação de cor, etc.) tendo lógica própria.

**O que ficou sem confirmar**: os corpos dos 12 handlers distintos;
os ~19% não alcançados da função. Marcada `read_structural` —
cobertura parcial, não forçada.

## 92. `ctlmap_main(CTLINFO*)` — passe estrutural — controlador de frame do mapa mundi, com detecção real de toque em cidade (2026-10-17, Fase 3, lote paralelo)

`ctlmap_main(CTLINFO*)` (`0x2542a4`, 3.124 B) — fase "main" do
controlador do mapa mundi (`CTLINFO*`, arquitetura polimórfica
`init/active/main/deactive` já confirmada nas seções 9.6/12.2).
Descida recursiva via `jtable.py`: **760 de ~781 instruções
possíveis (97%)**, sem tabela de salto; **79 branches, 38 de
retrocesso**.

### Correção importante da hipótese inicial: não chama `worldmap_call` diretamente

Diferente do esperado, `ctlmap_main` **não chama `worldmap_call`**
(seção 80) — nenhuma referência no catálogo de 32 `bl`. O
dispatcher de bytecode do mapa mundi deve ser invocado de outro
lugar (candidato mais provável: `wldnormal_lop`, o laço de frame
real já confirmado na seção 11.1, ou `wld_event`). `ctlmap_main` é,
em vez disso, o driver de **interação por frame** do mapa mundi:
detecção de toque em cidade, scroll, e troca pra outros
controladores.

### Achados confirmados

```
town_find(_POINT) / town_find3(_POINT, int) / town_touch(_POINT, int*, int*)
townmenu_check(int, int*) / iOS_debugDispTownCircle(int, int)
bgscrol_chk(_POINT*, VECTOR*) — mesma família de bgscrol_chk_x/y (seção 12.14)
walkrute_set(int, int) / wldscr_snapshot(int) / sound_request(int)
ctlmap_deactive(CTLINFO*) / ctlcenter_init / ctlopt_init / ctlhelp_init / ctltownmenu_init
```
Confirma um sistema real de **detecção de toque em cidade no mapa
3D** — `town_find`/`town_find3`/`town_touch` buscam qual cidade
corresponde a uma posição `_POINT` (provável projeção de toque pra
coordenada de mundo), `townmenu_check` decide se abre o menu de
interação da cidade (via `ctltownmenu_init`, trocando de
controlador), e `iOS_debugDispTownCircle` confirma um **círculo de
debug visível** ao redor de cada cidade (remanescente de build de
desenvolvimento, no espírito de `debug_chrmenu`/`Main_Init`, seções
64/79). Usa `rsin`/`rcos`/`ratan2` reais (mesma família
trigonométrica de `Mdl0010`/`sBattleTouchToCur`, seções 52/85) —
provavelmente pra projetar a posição da cidade ou calcular ângulo de
toque. `bgscrol_chk` (sem sufixo `_x`/`_y`) pode ser uma função
"pai" que despacha pras duas variantes já lidas (seção 12.14) — não
confirmado.

**O que ficou sem confirmar**: os corpos da cascata de 79 branches
(38 de retrocesso); onde `worldmap_call` é de fato chamado, já que
não é aqui; o papel exato de `bgscrol_chk` vs. `bgscrol_chk_x`/`_y`.
Marcada `read_structural`.

## 93. `bWorldJobStts()` — passe estrutural — confirma a tela de status de job/habilidade DENTRO da batalha, usando a biblioteca `b*` de UI já documentada (2026-10-17, Fase 3, lote paralelo)

`bWorldJobStts()` (`0x178e98`, 3.300 B) — descida recursiva via
`jtable.py`: **762 de ~825 instruções possíveis (92%)**, sem tabela
de salto; **64 branches, 34 de retrocesso**.

### Confirma ser a versão de batalha da tela de status de job/habilidade

Os 42 `bl` resolvidos são quase todos prefixados com **`b`**
(`bSetFrameRate`, `bGetJobList`, `bGetAbilityList`, `bDrawFT4RGB`,
`bMakeTextureMessage`, `bSetMenuSelSide`/`bMenuSelSide`/
`bMenuSelSideWithSnd(Direct)`, `bClearPadData`,
`bWindowPositionInit`/`InitSingle`, `bSetWindowPosition`/
`bGetWindowPosition`, `bWindowInit`/`Init2`, `bDrawWindow2`,
`bSetWindowCount`) — a MESMA biblioteca de UI com prefixo `b` já
confirmada em `BattleUnitList` (seção 36). Isto confirma a hipótese:
`bWorldJobStts` é a tela real de consultar **status de job/
habilidade de uma unidade DENTRO da batalha** (contraparte de
`AbilityMenu`/`JobChange`, seções 57/61, que são do menu principal)
— `bGetJobList`/`bGetAbilityList` confirmam a mesma consulta de
dados, só que desenhada com a biblioteca `b*` exclusiva de batalha
em vez da biblioteca compartilhada sem prefixo. `GetLocalJobNumber(short)`
é um achado novo (conversão de ID de job global pra índice local).
`iOS_CMenuTouch` ganha métodos novos aqui: `setMaxNumY`/`setDispNumY`/
`setXIconRect` — confirma mais parâmetros de layout de lista (altura
máxima, número exibido, retângulo de ícone por linha) nunca
catalogados nesta classe.

**O que ficou sem confirmar**: os corpos da cascata de 64 branches
(34 de retrocesso); os corpos das 5 funções locais sem símbolo
(`sub_178ca0`/`cf8`/`d44`/`da0`/`df8`). Marcada `read_structural`.

## Sexto lote paralelo (seções 94–98): mais 5 funções lidas por forks simultâneos

## 94. `getskillrange(ACT*)` — passe estrutural — confirma o cálculo real de alcance/forma de área de habilidade (2026-10-17, Fase 3, lote paralelo)

`getskillrange(ACT*)` (`0x1e03c8`, 2.812 B) — parte da mesma família
de resolução de ação de batalha já aberta em `calc_result`/
`setskillresult` (seções 77/90, tipo `ACT*`). Descida recursiva via
`jtable.py`: **676 de ~703 instruções possíveis (96%)**, uma tabela
de salto resolvida (16 casos, 9 endereços distintos); **82 branches,
42 de retrocesso**.

### Confirma o cálculo de alcance/forma de área, não a resolução de dano em si

```
get_coord_address(BWORK*)      ×7 — busca coordenada de painel real
copyACTst(ACT*, ACT*)             ×4 — mesma função de cópia de ACT (seção 90)
set_normability2(int, unsigned char, short*, unsigned char*, unsigned char*, int, unsigned char*, unsigned char*)
pspItemGetCommonData
```
A tabela de 16 casos (9 distintos) despacha, com alta confiança, por
**tipo de padrão de alcance/área** (linha reta, diamante, cruz,
"todos", etc. — mecânica clássica do FFT de forma de AoE por
habilidade), chamando `get_coord_address` repetidamente pra resolver
as coordenadas de painel afetadas em cada forma. `set_normability2`
(assinatura complexa, buffers `short*`/`unsigned char*` de saída)
provavelmente grava a lista de offsets dx/dy do padrão de alcance
calculado num buffer de saída pro chamador consumir. `copyACTst`
reaparecendo confirma que o cálculo de alcance opera sobre uma CÓPIA
da struct `ACT`, não a original — consistente com simular/testar o
alcance sem alterar o estado real da ação. Tem uma função irmã,
`getskilleffect(ACT*)` (seção 95), que calcula o efeito (dano/
status) em vez da forma geométrica.

**O que ficou sem confirmar**: os corpos dos 9 handlers distintos
(qual padrão geométrico cada caso representa); os corpos das 5
funções locais sem símbolo (`sub_1dec0c` ×4, `sub_1dfa48` ×3); o
layout exato dos buffers de saída de `set_normability2`. Marcada
`read_structural`.

## 95. `getskilleffect(ACT*)` — passe estrutural — despachante de 7 categorias de efeito de habilidade, com checagem de invencibilidade e altura real (2026-10-17, Fase 3, lote paralelo)

`getskilleffect(ACT*)` (`0x1e4f3c`, 2.712 B) — mesma família `ACT*`
já confirmada em `calc_result`/`setskillresult`/`getskillrange`
(seções 77/90/94). Descida recursiva via `jtable.py`: **648 de ~678
instruções possíveis (96%)**, uma tabela de salto resolvida (16
casos, 7 endereços distintos); **99 branches, 47 de retrocesso**.

### Confirma ser o despachante por categoria de efeito, não a aplicação em si

```
copyACTst(ACT*, ACT*)                     — mesma cópia de struct de calc_result (seção 90)
get_coord_address(BWORK*)                  — mesma função de getskillrange (seção 94)
check_invincible(int, int*)                 — achado novo: checagem real de invencibilidade/imunidade a dano
get_unit_height(int)                          — achado novo: altura da unidade entra no cálculo de efeito
get_fusui_ability(BWORK*)                    — mesmo termo não decifrado de calc_result (seção 90)
pspItemGetCommonData
```
A tabela de 16 casos (colapsando em 7 endereços) confirma que
`getskilleffect` decide **qual das ~7 categorias de efeito** uma
habilidade produz (dano, cura, status, drenar, instant-kill, etc. —
hipótese de quais categorias são essas, não confirmada byte a byte).
`check_invincible` confirma, por instrução real, que existe uma
checagem de invencibilidade/imunidade que pode anular o efeito antes
de ele ser calculado — mecânica real do FFT (unidades com estado
"Invincible" ou imunes a certo tipo de dano). `get_unit_height`
sugere que a diferença de altura entre atacante e alvo participa do
cálculo de algum efeito (plausível pra ataques de área/explosão, que
no FFT original têm alcance vertical limitado). Reusa `copyACTst` e
`get_fusui_ability` — confirma, pela segunda vez, que `calc_result`
e `getskilleffect` operam sobre a mesma família de dados `ACT`.

**O que ficou sem confirmar**: os corpos dos 7 handlers distintos
(qual categoria de efeito cada um implementa); os corpos das 5
funções locais sem símbolo (`sub_1dea08`/`1dec0c`/`1df060`/
`1df480`/`1dfa48`); o papel exato de `get_fusui_ability`/
`get_coord_address`. Marcada `read_structural`.

## 96. `ctlnobel_main(CTLINFO*)` — passe estrutural — confirma "Nobel" como "Novel" (cena de diálogo estilo visual novel), amarrando vários controladores irmãos (2026-10-17, Fase 3, lote paralelo)

`ctlnobel_main(CTLINFO*)` (`0x264cf8`, 2.784 B) — fase "main" da
família de controlador `ctlnobel_*` já citada desde a seção 9.6
como referência arquitetural (mesmo padrão polimórfico
`init/active/main/deactive` de `ctlopentitle_main`/`ctlmap_main`,
seções 87/92), nunca aberta por dentro. Descida recursiva via
`jtable.py`: **661 de ~696 instruções possíveis (95%)**, sem tabela
de salto; **78 branches, 44 de retrocesso**.

### Confirma "Nobel" como transliteração de "Novel" — o controlador real de cena de diálogo estilo visual novel

```
iOSSdNovelClear() / iOSSdNovelLogIconOn()/Off() / iOSSdNovelBrightCtrlClear()
iOSSDNovelHelpTrgSet(long) / iOSNovelModeRestore() / Main_Novel_GetBtnRect(...)
wld_snpl() / snplinf_init(int)                        — já citada na seção 9.5
ssd_request(int,int) / Ssd_DisposeEffectData(void*)       — sistema Ssd (seções 12.7/88)
ctlzodiac_init / ctlhelp_init / ctlnobelstop_init / ctlnblwldinfo_init / ctlbackpage_init
ret_adventurestatus() / stop_adventuremessage(int)
iOS_add_anmpac_max(int)                                   — ANMPAC (seções 12.5/12.10/12.13)
```
Confirma, com nomes reais (`SdNovel`, `Main_Novel_GetBtnRect`), que
"Nobel" é a transliteração japonesa de **"Novel"** (ノベル) — este é
o controlador real de **cenas de diálogo estilo visual novel**
(texto full-screen com escolhas, comum em RPGs japoneses), distinto
do sistema de mensagem genérico (`Wmesputmain`/`mesputmain`, seções
33/37). `ret_adventurestatus`/`stop_adventuremessage` confirmam
terminologia "adventure" ligada a este modo. `ctlnobel_main`
alterna entre vários controladores-irmãos (`ctlzodiac_init` — tela
de zodíaco/horóscopo do FFT; `ctlhelp_init`; `ctlnobelstop_init`;
`ctlnblwldinfo_init` — overlay de info do mapa mundi durante a
novel; `ctlbackpage_init` — provável "voltar página"/log de texto).
`iOS_add_anmpac_max` sugere que cenas de novel permitem mais sprites
animados simultâneos que o padrão.

**O que ficou sem confirmar**: os corpos da cascata de 78 branches
(44 de retrocesso); os corpos dos controladores-irmãos citados.
Marcada `read_structural`.

## 97. `LearnAbiStts()` — passe estrutural — a tela real de "aprendeu uma habilidade", confirma `AbilityLearning` como a mutação de verdade (2026-10-17, Fase 3, lote paralelo)

`LearnAbiStts()` (`0x1b5104`, 2.716 B) — já citada no catálogo de
`AbilityMenu` (seção 57), nunca aberta por dentro. Descida recursiva
via `jtable.py`: **616 de ~679 instruções possíveis (91%)**, uma
tabela de salto pequena (6 casos, 5 distintos); **40 branches, 20 de
retrocesso**.

### Confirma a tela de notificação de habilidade aprendida, e a função real que marca a habilidade como aprendida

```
AbilityLearning(short, short, short)      — a mutação real: marca a habilidade como aprendida
GetAbilityList(short, short, int, short*, int)   ×3  — mesma consulta da seção 57
MakeTextureMessage / DrawMessage(int, COMRECORD*)
MenuSelSide / MenuSelSideWithSnd(Direct)
WindowInit/Init2 / WindowPositionInitSingle / SetWindowPosition/GetWindowPosition
unitans_init()
```
`AbilityLearning(short, short, short)` é o achado central: a
assinatura (3 `short`, provavelmente unidade/job/ID-de-habilidade)
confirma ser a função que **realmente grava** que uma unidade
aprendeu uma habilidade — `LearnAbiStts` é a tela que EXIBE essa
notificação (texto "aprendeu X!", lista de habilidades via
`GetAbilityList`), não a lógica de progressão em si (que já foi
vista como consumidora de JP via `add_jobpointB`/`get_unit_jl` em
`setskillresult`, seção 77). Reusa a mesma biblioteca de janela/menu
compartilhada (`WindowInit`, `MenuSelSide`) já vista em `AbilityMenu`
(seção 57) e várias outras telas. `unitans_init()` (já visto na
seção 61, `JobChange`) sugere que esta notificação pode aparecer
tanto ao fim de uma batalha quanto numa transição de tela de menu.

**O que ficou sem confirmar**: os corpos dos 5 handlers da tabela de
6 casos; o corpo de `AbilityLearning` em si; se `LearnJobStts`,
citada junto com esta na seção 57, segue exatamente o mesmo padrão
pra jobs em vez de habilidades. Marcada `read_structural`.

## 98. `Equip()` — passe estrutural — confirma a tela real de troca de equipamento, ligada à lista de unidades, não ao item (2026-10-17, Fase 3, lote paralelo)

`Equip()` (`0x1adf8c`, 2.684 B) — já citada no catálogo de `ItemMenu`
(seção 39) entre as funções do sistema real de itens/equipamento,
nunca aberta por dentro. Descida recursiva via `jtable.py`: **630 de
~671 instruções possíveis (94%)**, sem tabela de salto; **48
branches, 22 de retrocesso**.

### Confirma ser o controlador real da tela de equipar, construído sobre a mesma biblioteca de janela/menu já documentada

```
GetItemList(short,short,signed char,short*,unsigned short,unsigned char)
ItemEquip(short,short,short) / ItemChg(short,int) / IsUntauchable(int)
ChrPowerCompare(C_STTS*,A_STTS*,short*,short*)
WindowInit2 / DrawWindow / CursolFunc / WindowPrioritySet
SetWindowPosition/GetWindowPosition / MenuSelVerticalWithSnd(Direct)
iOS_CMenuTouch::setDispOffset/setYLine/drawMenuAssist/init/exec
Wtask_start(long) / Wtask_stop(long)
iOS_getOtNum_unitlist() / iOS_setDispCursor_window_unitlist / iOS_getScrollType_unitlist
```
Confirma, com nomes reais, que `Equip()` é o controlador de tela
real de troca de equipamento — reusa a mesma biblioteca de janela/
menu compartilhada já vista em `ItemMenu`/`AbilityMenu` (seções
39/57), roda como task (variante `W`), e usa `iOS_CMenuTouch` pra
navegação por toque. **Achado notável**: os sufixos `iOS_*` aqui são
`_unitlist` (`iOS_getOtNum_unitlist`/`iOS_getScrollType_unitlist`),
a MESMA família já vista em `ItemMenu`/`BattleUnitList` (seções
36/39) — não `_equip` como em `eItemMenu` (seção 40). Isso sugere
que `Equip()` é acessado a partir de um fluxo centrado em **lista de
unidades** (escolher a unidade primeiro, depois equipar), distinto
do fluxo próprio de `eItemMenu`, que tem sua família `_equip`
dedicada.

**O que ficou sem confirmar**: os corpos da cascata de 48 branches
(22 de retrocesso); o contexto exato de chamada (quem invoca
`Equip()` vs. `eItemMenu`). Marcada `read_structural`.

## Sétimo lote paralelo: 1 de 5 forks completou antes do limite de uso da sessão

**Nota operacional (2026-10-18)**: dos 5 forks lançados pro sétimo
lote (`ASURA_LMDL_TIME_TBL`, `Tutrial`, `ctlhoukmes_main`,
`iOS_RESUME_SET_EVENT_W`, `hight_font_draw`), 4 falharam por limite
de uso da sessão (não leram nada, erro de API antes de começar). Só
`iOS_RESUME_SET_EVENT_W` completou — fica registrada abaixo. Os
outros 4 alvos continuam na fila pra uma próxima rodada.

## 99. `iOS_RESUME_SET_EVENT_W(...)` — confirmação curta do padrão da seção 76 (2026-10-18, Fase 3)

**`iOS_RESUME_SET_EVENT_W(IOS_RESUME_DATA_EVENT_W*, IOS_RESUME_DATACOPY_MODE)`**
(`0x11cbb4`, 2.812 B) — confirma o mesmo padrão de
`iOS_RESUME_SET_EVENT` (seção 76): serializador campo a campo, 87%
de cobertura, zero branches reais, só `iOS_Resume_DataCopy` (×84) e
`iOS_Resume_DataCopyAddr` (×11) chamadas. Serializa um struct
diferente (`IOS_RESUME_DATA_EVENT_W`, provavelmente variante de
layout, não necessariamente "wide" no sentido de texto), usando os
MESMOS dois primitivos de cópia — confirma que o sufixo `_W` aqui
**não segue** o padrão "cópia real de fonte" das telas de UI
(seções 33/37/47/58/60), é só uma segunda estrutura de dados
compartilhando o mesmo mecanismo. Marcada `read_structural`.

## Metodologia do loop (registrada 2026-10-18, Fase 3): esta é a nossa forma de trabalho a partir de agora

O loop passa a operar por estas seis regras, adotadas numa revisão de
processo no meio da Fase 3 depois de observar onde o tempo estava
sendo gasto sem necessidade:

1. **Paralelizar com múltiplos agentes/forks.** Função lida é
   independente de qualquer outra (mesmo binário, só endereço
   diferente) — o gargalo real é número de rodadas de ida-e-volta,
   não CPU. Em vez de uma função por iteração, vários forks rodam
   `jtable.py`/`family_sim.py` ao mesmo tempo sobre itens diferentes
   da fila, devolvem o rascunho, e a integração nos arquivos
   compartilhados acontece numa única passada (em vigor desde a
   seção 70; ver "lotes paralelos").
2. **Família já confirmada não é trabalho novo.** Depois de 2–3
   confirmações do mesmo padrão (`Mdl*`, `disp_personalwindow`
   `A/C/D/E`, variantes `W`), as próximas são repetição. Em vez do
   passe estrutural completo em cada uma, comparar o catálogo de `bl`
   resolvidos da função nova contra o da já lida — Jaccard ≥90% e
   sem tabela de salto pendente confirma por similaridade sem redigir
   uma seção cheia (ferramenta: `family_sim.py`, primeira aplicação
   em lote na seção 100 — 26 funções/68.960 B numa única passada em
   vez de ~26 seções).
3. **Rebaixar a régua de "pronto" pra funções grandes.** Quando a
   função não tem tabela de salto e a primeira passada já cobre
   >95%, o resultado automático do passe estrutural é aceito direto
   — sem etapa extra de verificação manual instrução-a-instrução.
4. **Extração de tabela de salto validada, não um script novo a cada
   vez.** `jtable.py` (validado contra `battle()`, seção 32) já acha
   o `cmp` de guarda andando pra trás no fluxo real de instruções e
   recusa a tabela honestamente se o registrador for sobrescrito
   antes — essa é a ferramenta usada, não extração manual repetida.
   A tentativa de descida em cascata totalmente automática
   (`struct_pass2.py`) gerou falsos positivos e foi abandonada (nota
   da seção correspondente); não vale retomar sem uma correção clara
   do que causou os falsos positivos.
5. **Focar em bytes, não em contagem de função.** A maioria das
   ~6.600 funções do binário é pequena (mediana de 56 B); um número
   pequeno de funções grandes já cobre a maior parte do código em
   bytes. Continuar ordenando a fila "maior primeiro" (por bytes não
   lidos) é a forma mais eficiente de subir a % de cobertura — ver
   `RE_FUNCTION_INVENTORY.csv`, ordenado por tamanho.
6. **Boilerplate genérico não precisa de passe completo.** Código de
   terceiros reconhecível de cara (ex.: `gl3stubInit`, zlib
   embutido — seções 69/69) leva só um reconhecimento rápido de
   padrão, marca `read_full`/`read_structural` e pula pra próxima,
   sem gastar uma iteração cheia.

Estas seis regras substituem o ritmo "uma função, um commit, repete"
que vinha sendo usado até a seção 69 — a partir da seção 70
(primeiro lote paralelo) e, de forma mais explícita, a partir desta
seção 100, é assim que o loop deve continuar operando.

## 101. Família `Mdl*` completa — confirmação em lote por catálogo de `bl`, 26 funções / 68.960 B numa única passada (2026-10-18, Fase 3, primeira aplicação da regra 2 da metodologia)

Construída `family_sim.py` (ferramenta nova, ver seção 100, regra 2):
roda a mesma descida recursiva de `jtable.py` em cada função da fila
e mede a similaridade de Jaccard do catálogo de endereços `bl`
contra uma referência já lida — ≥90% e sem tabela de salto não
resolvida confirma por similaridade sem redigir uma seção cheia.
Rodada contra as 26 funções `Mdl0001`–`Mdl0028` ainda não lidas
(todas as 29 do inventário, exceto `Mdl0024`/`Mdl0010`/`Mdl0003`, já
confirmadas nas seções 48/52/53), revela que a família não é
uniforme — são **três níveis reais**, não repetição cega:

### Nível A — duplicata exata do catálogo "completo" (29 `bl`, Jaccard 1,00)

```
Mdl0004(short,int,int,int)  0x22f48c  8.420 B
Mdl0009(short,int,int,int)  0x234580  7.584 B
```
Catálogo de `bl` **idêntico**, endereço por endereço, ao de `Mdl0010`/
`Mdl0003`/`Mdl0024` (seções 48/52/53) — mesmo uso de
`ASHURA_getOTptrZ`, `CreateObjectWithTable`, `ratan2`, `ps_rand`
(×26), `VectorNormal`, `AddPrim`. Confirma por similaridade, sem
leitura linha a linha. Com estas duas, **5 das 29** funções `Mdl*`
já estão no nível "completo".

### Nível B — mesmo vocabulário, subconjunto menor (9–22 `bl`, Jaccard 0,3–0,76)

```
Mdl0001  0x22ae34  4.868 B     Mdl0008  0x233ed0  1.712 B
Mdl0002  0x22c138  5.476 B     Mdl0012  0x23837c  2.096 B
Mdl0005  0x231570  1.852 B     Mdl0013  0x23237c  6.792 B
Mdl0006  0x231cac  1.744 B     Mdl0014  0x23a634  3.292 B
Mdl0007  0x23237c  6.996 B     Mdl0015  0x23b310  5.024 B
Mdl0017  0x23c79c  4.792 B     Mdl0028  0x2406d4  4.700 B
```
Todas chamam o mesmo núcleo matemático do Nível A (`ratan2`,
`VectorNormal`, `AddPrim`, `getAnimationDirection`, `get_mapstp`,
`getMapSize`, `__aeabi_idiv`) mas **nenhuma chama
`CreateObjectWithTable`** (gerador de partícula, seção 44) **exceto
`Mdl0015`**, que é a única do Nível B a chamar — fica estruturalmente
a meio caminho entre B e A. Conclusão: o Nível B são modelos/efeitos
mais simples, desenhados direto via `ASHURA`/GTE sem gerar partículas
proceduralmente. `Mdl0017` também chama um helper interno próprio
(`Mdl0017_sub`, `0x23c728`, 116 B, zero `bl` — só aritmética inline).
Todas marcadas `read_structural` por padrão de família, sem leitura
instrução-a-instrução individual.

### Nível C — funções minúsculas, NÃO são o mesmo padrão de desenho (12 funções, 3.612 B, lidas por `jtable.py` direto — cabem no passe estrutural completo por serem tão pequenas)

```
Mdl0018  0x23da54  204 B   -> ASHURA_Control(...) x1, só isso
Mdl0019  0x23db20  204 B   -> ASHURA_Control(...) x1, só isso
Mdl0026  0x2404d8  264 B   -> ASHURA_Control(...) x1, só isso
Mdl0027  0x2405e0  244 B   -> ASHURA_Control(...) x1, só isso
Mdl0022  0x23dc94  984 B   -> ASHURA_Control + Malloc/Free + CreateObjectWithTable
Mdl0023  0x23e06c  560 B   -> ASHURA_Control + Malloc/Free + CreateObjectWithTable
Mdl0011  0x238124  600 B   -> ASHURA_getOTptrZ + mallocForFile + StoreImage +
                               SetPolyGT4 + SetDrawMode + system_error
                               (carrega textura pro modelo, não desenha)
Mdl0016  0x23c6b0  120 B   -> ASHURA_snowMatrix(long,long) só isso (efeito de neve)
Mdl0020  0x23dbec   84 B   -> stopMapPaletteAnimation() só isso
Mdl0021  0x23dc40   84 B   -> restertMapPaletteAnimation() só isso (sic, erro de
                               digitação real no símbolo do binário)
Mdl0025  0x240444  148 B   -> readed_mapchange + iOS_IsBattleSpeedUp +
                               ASHURA_Control (dispara condicional a velocidade
                               de batalha)
Mdl0017_sub 0x23c728 116 B  -> 0 bl, só aritmética (helper interno de Mdl0017)
```
Confirma, com catálogo exato (não só Jaccard), que a tabela `Mdl*` é
um **dispatch por ID de modelo/efeito heterogêneo**: a maioria dos
IDs desenha uma malha `ASHURA` completa (Níveis A/B), mas alguns IDs
são casos especiais sem relação com desenho de malha — animação de
paleta de mapa (`Mdl0020`/`Mdl0021`), efeito de neve (`Mdl0016`),
pré-carga de textura (`Mdl0011`), ou um gate condicional de velocidade
de batalha (`Mdl0025`). Todas pequenas demais para esconder lógica
relevante além do catálogo de chamadas já mostrado. Marcadas
`read_structural`.

**O que ficou sem confirmar**: os corpos internos de qualquer uma das
26 (além do catálogo de chamadas e, pros Níveis A/C, a contagem exata
de branches); por que o índice numérico de cada `Mdl000N` corresponde
a qual efeito/golpe específico do jogo (nenhuma tabela de nomes
encontrada). **Resultado prático**: as 29 funções da família `Mdl*`
somam **68.960 B confirmados numa única passada** em vez de ~26
seções individuais.

## 102. Quatro internos da `libvorbis`/Tremor reconhecidos por nome, sem passe completo (2026-10-18, Fase 3, regra 6 da metodologia)

`_vp_psy_init` (`0x940f0`, 2.828 B), `floor1_fit` (`0x8aa00`, 2.800 B),
`ov_pcm_seek_page` (`0x9f3f8`, 2.576 B) e
`_vp_couple_quantize_normalize` (`0x956d4`, 2.544 B) — os quatro nomes
são símbolos reais da `libvorbis`/Tremor upstream (modelo
psicoacústico `psy.c`, ajuste de piso espectral `floor1.c`, busca de
página `vorbisfile.c`, acoplamento stereo `vorbis_quantize`),
reconhecíveis de cara, igual já estabelecido pra `ov_pcm_tell`/
`ov_open_callbacks`/`ov_info` nas seções 17.x/3169-3386. Checagem
rápida via `jtable.py` (sem passe completo) confirma o padrão: 98–
100% de cobertura, zero tabela de salto, catálogo de `bl` dominado
por runtime de ponto flutuante do compilador (`__adddf3`/`__muldf3`/
`__divdf3`/`__extendsfdf2` etc.) mais um punhado de helpers locais
`sub_*` sem símbolo — nenhuma chamada a qualquer função prefixada do
jogo (`CFFT_STATE`/`iOS_*`/`ASHURA_*`/etc). Confirma que são código
de terceiros genérico, consistente com a identificação já feita da
`libvorbisfile`. Marcadas `read_full` sem leitura instrução-a-
instrução — regra 6 da metodologia (seção 100): boilerplate
reconhecível não precisa de passe completo.

## 103. Família `disp_bothwindow` fechada — `A`/`D` confirmam entrada fina, `E` parcial, `W` confirma cópia real dos helpers (2026-10-18, Fase 3, regra 2 da metodologia)

`family_sim.py` contra a referência `disp_bothwindow()` (`0x12b12c`,
seção 73, já `read_structural`):

```
Adisp_bothwindow()  0xc1e20   4.260 B   Jaccard 0,89
Ddisp_bothwindow()  0xcd5e8   4.128 B   Jaccard 0,89
Edisp_bothwindow()  0x1225e8  2.552 B   Jaccard 0,63
Wdisp_bothwindow()  0x133be4  2.544 B   Jaccard 0,22
```
**`A` e `D`**: catálogo de 33 `bl` quase idêntico ao da referência —
só 2 endereços da referência não aparecem (locais próprios de
`disp_bothwindow`) e cada uma tem 2 locais próprios minúsculos sem
símbolo (`LOCAL(no-dynsym)`) — confirma o mesmo padrão "entrada fina"
já visto em `C` (seção 73) e em toda a família `disp_personalwindow`
(seções 49–51): reusam os helpers sem prefixo, não duplicam nada.

**`E`**: Jaccard mais baixo (0,63) por chamar um cluster de 5
endereços locais próprios adicionais (`0x11e95c` a `0x11f0bc`, todos
sem símbolo) além do núcleo compartilhado — ainda a MESMA família,
só com mais lógica própria de entrada que `A`/`D`/`C`.

**`W` — achado que confirma a hipótese deixada pendente na seção 73**:
Jaccard muito baixo (0,22) porque `W` **não chama nenhum dos helpers
sem prefixo** da referência — chama, em vez disso, um conjunto
próprio de duplicatas `W`-prefixadas: `Waddlocalprim`,
`Winitsprtfield`, `Waddstatusback`, `Winitstatusback`, `Witemuvclut`,
`Wsettaskkind`, `Wimport_localpad`, `Wloadcdst`, `Wbgput`,
`Wstatuskanjiprint`, mais `wasmTaskEntry`/`wasmGetInput3` (arquitetura
de task `wasm`, igual `Wmultiwindow_*`/`Wdisp_personalwindow`, seções
33/47/58/60/74). **Confirma, com uma quarta família independente, que
`W` é consistentemente a única variante que é uma recompilação de
verdade do código-fonte** (biblioteca de helpers própria, não um
ponto de entrada fino) — padrão agora visto em `disp_personalwindow`,
`Wmultiwindow_*`, e `disp_bothwindow`.

Todas as quatro marcadas `read_structural` por similaridade/catálogo
direto — fecha a família `disp_bothwindow` (base + `A`/`C`/`D`/`E`/`W`,
6 funções, seções 73/103) sem passe instrução-a-instrução adicional.

## 104. `Cdisp_personalwindow()` — última letra da família, compartilha o sinal de "remoção de personagem" de `D` (2026-10-18, Fase 3, regra 3 da metodologia)

`Cdisp_personalwindow()` (`0x14c010`, 7.484 B) — 97% de cobertura,
sem tabela de salto; aceito direto via `family_sim.py` contra
`disp_personalwindow()` (seção 46), sem verificação manual adicional
(regra 3 da metodologia, seção 100). Jaccard 0,68 (51 de 55 `bl` da
referência) — mais baixo que o puro "entrada fina" de `A`/`D`/`E`
(seções 49–51), porque `C` chama 4 endereços próprios extras:
`iOS_getTransFaceAT(int)`, `iOS_setTransFaceForChrRemove(int)`,
`CFFT_STATE::AttackTeamFaceIDToFaceID`, `iOS_getV2Icon(V2ICON_DATA)`.

**Achado**: `C` chama o MESMO `iOS_setTransFaceForChrRemove` já visto
em `Ddisp_personalwindow` (seção 49, que levantou a hipótese "tela
usada no fluxo de remoção de personagem do time"). Com `C` e `D`
compartilhando essa chamada — e `A`/`E`/base/`W` não a chamando —
a hipótese fica mais específica: não é "D = remoção", é **"C e D
juntas = o par de telas do fluxo de remoção de personagem"**,
possivelmente lado esquerdo/direito da comparação antes de confirmar
a remoção. Fecha a família `disp_personalwindow` (base + 5 letras,
seções 46/47/49–51/104). Marcada `read_structural`.


## Oitavo lote paralelo (seções 105–109): 5 funções lidas por forks simultâneos, usando `jtable.py`

## 105. `iOS_RESUME_SET_WORK_MU(...)` — diverge do padrão "serializador puro" das seções 76/99, introduz 6 helpers novos de endereço (2026-10-18, Fase 3, lote paralelo)

`iOS_RESUME_SET_WORK_MU(IOS_RESUME_DATA_WORK_MU*, IOS_RESUME_DATACOPY_MODE)`
(`0x216e5c`, 4.004 B) — descida recursiva via `jtable.py`: **895 de
~1.001 instruções possíveis (89%)**, sem tabela de salto; **21
branches, 12 de retrocesso** — já rompe com o padrão "quase 100%
linear, zero branch real" das duas funções anteriores da família
(`iOS_RESUME_SET_EVENT`/`_W`, seções 76/99).

Continua dominada por `iOS_Resume_DataCopy` (×105 — confirma que é a
MESMA família de serialização de dados de resume), mas **não chama
`iOS_Resume_DataCopyAddr` nenhuma vez** — em vez disso, introduz 6
helpers de resolução de endereço nunca vistos antes nesta família:
`getShapeAddress`, `getSequenceAddress`, `getWpnShapeAddress`,
`getWpnSequenceAddress`, `getEffShapeAddress`,
`getEffSequenceAddress` (todos ×2), mais `ResumeData_GetHeapOffset()`
e `PIE_OFFSET(unsigned int)` (ajuste de endereço position-independent
— confirma que o resume salva PONTEIROS, não só dados planos, e
precisa recalculá-los no heap ao restaurar). Um local sem símbolo
(`sub_714b8`, ×2). **Conclusão**: mesma família/primitivo
(`iOS_Resume_DataCopy`), mas um membro estruturalmente distinto — em
vez de despejar campos de struct linearmente, serializa tabelas de
ponteiro (forma/sequência/arma/efeito) em laço, com correção de
endereço PIE. Marcada `read_structural`.

## 106. `disp_option(int)` — tela de opções, camada de task pesada e acessores PSP-net de modo de batalha em rede (2026-10-18, Fase 3, lote paralelo)

`disp_option(int)` (`0x13d248`, 3.996 B) — descida recursiva via
`jtable.py`: **953 de ~999 instruções possíveis (95%)**, sem tabela
de salto; **64 branches, 37 de retrocesso**. 25 `bl` distintos, 85
chamadas no total.

Dominada pela camada de task/corrotina: `send_taskparamater` (×21) e
`wait_taskend` (×18) são os dois primitivos mais chamados —
consistente com uma tela que avança uma máquina de estado
cooperativa por frame — mais `task_create` (×9), `task_wait`/
`task_stop`/`task_killmyself` e a família `asm*`
(`asmTaskEntry`/`asmGetInput1`/`asmGetActiveTask`/`asm_function`).
Também toca: overlay de ajuda/tutorial (`request_help`,
`tutorial_syscall`), input (`import_localpad`), a camada de ícone/
hook `iOS_*` (`iOS_limitOptrecSub`, `iOS_hook_disp_option`,
`iOS_setV2Icon` ×10 — a chamada não-task mais frequente), consultas
de item/equipamento (`get_itemcommon`, `get_item_number`, `get_bwp`
— sugere uma sub-tela de equipar dentro de opções) e, achado novo,
acessores de rede PSP (`pspNetGetBattleModeFlag`,
`pspNetEntranceOptionArrayGet`/`RecordGet`/`ScrRecordGet`) — confirma
que o estado de opção de **modo de batalha em rede** é lido
diretamente nesta tela. Dois locais sem símbolo. Sem tabela de salto
— dispatch de menu aqui é por branch condicional direto, não switch.
Marcada `read_structural`.

## 107. `disp_statusc()` — confirma o padrão "entrada fina" de novo, mas pela camada `asm` (task), não `wasm` — maior catálogo de `bl` já visto numa única função (2026-10-18, Fase 3, lote paralelo)

`disp_statusc()` (`0xef83c`, 3.828 B) — descida recursiva via
`jtable.py`: **911 de ~957 instruções possíveis (95%)**, sem tabela
de salto; **63 branches, 35 de retrocesso**. **57 `bl` distintos** —
recorde da investigação em número de chamadas distintas numa só
função.

Confirma o padrão previsto "variante sem prefixo reusa helpers
compartilhados" (já visto em `disp_personalwindow`/
`disp_bothwindow`), mas pela camada de task **`asm`**, não `wasm`:
`asmTaskEntry()`/`asmGetInput3()`/`asmGetActiveTask()` (sem o prefixo
`w`) — função de task cooperativa de verdade, não um ponto de entrada
fino sobre outra. Catálogo de `bl` reusa, sem prefixo, os MESMOS
helpers já vistos em `disp_personalwindow`/`disp_bothwindow`:
`addlocalprim` (×13), `statuskanjiprint`, `bgput`, `initdrmode`,
`loadcdst`, `addstatusback`/`sttsback_normal`/`sttsback_blue`/
`initstatusback`, `itemuvclut`, `multiwindow_packetclip*` — confirma
que TODA a família de telas de status (`disp_personalwindow`,
`disp_bothwindow`, `disp_statusc`) compartilha a MESMA biblioteca de
desenho, independente do layout específico da tela.

### Achados novos
- **`chokobo_chrmenu(int)`** — integração com o menu de personagem
  via chocobo, nunca vista.
- **`Get_bravebreak()`** / **`iOS_getTutorialbreak()`** /
  **`iOSTutoCheck()`** — três funções de controle de tutorial/
  "brave break" nunca vistas.
- **`CFFT_STATE::GetParam(int)`/`SetParam(int,int)`** — acessor
  genérico de estado global do jogo (terceira vez que `CFFT_STATE` é
  confirmado como um hub de estado central, seções 22/49).
- **`PSX_LoadImage`/`SetTile`/`SetSemiTrans`/`SetShadeTex`/
  `TexHybrid_RegistCLUTAddr`/`IS_TEX_2X`** — bloco de plumbing de
  textura PSX/híbrido nunca visto reunido numa função só.
- `pspNetGetControlChar`/`pspNetGetBattleModeFlag` — mais acessores
  de rede PSP, mesma família da seção 106.

Marcada `read_structural`.

## 108. `dispPolygonObject(...)` — carregador de malha TMD real do PS1, com tabela de salto de 4 casos por tipo de primitiva (2026-10-18, Fase 3, lote paralelo)

`dispPolygonObject(SVECTOR*, VECTOR*, SVECTOR*, VECTOR*, int)`
(`0x221f64`, 3.816 B) — descida recursiva via `jtable.py`: **941 de
~954 instruções possíveis (99%)**; **uma tabela de salto resolvida**
(guarda `cmp` em `0x222154`, dispatch em `0x222158`, 4 casos, 4
handlers distintos: `0x222170`/`0x222568`/`0x222384`/`0x222198`);
**35 branches, 27 de retrocesso**.

Catálogo pequeno (8 `bl`) mas revelador: **`_OpenTMD`/`_ReadTMD`**
(`TMD_PRIM*`) são as rotinas REAIS de parsing de TMD ("TIM Model
Data", formato de malha nativo do PS1) — função confirma, com
instrução real, que o jogo ainda carrega modelos no formato TMD
original, não um formato convertido. Isso corre em paralelo com
`RotMatrix`/`SetRotMatrix`/`ScaleMatrixL`/`SetTransMatrix`/`RotTrans`
— pipeline de matriz GTE clássico (não o conjunto específico do
`ASHURA`). `iOS_getSkipAddPrim()` (×5) e a tabela de 4 casos sugerem
dispatch por tipo de primitiva TMD, decidindo se cada uma deve ser
pulada ao montar a lista de desenho. Alta densidade de laço (27/35
branches de retrocesso) consistente com percorrer a lista de
primitivas e a hierarquia de objetos de um TMD. Marcada
`read_structural`.

## 109. `drawShape2(...)` — primitivo de rasterização `Shape2`, mesma família de iteração do TMD da seção 108 (2026-10-18, Fase 3, lote paralelo)

`drawShape2(Shape2*, Point*, short, VECTOR*, unsigned long*)`
(`0x228ee8`, 3.808 B) — descida recursiva via `jtable.py`: **949 de
~952 instruções possíveis (100%)**, sem tabela de salto; **102
branches, 59 de retrocesso** — maior densidade de laço relativa (58%)
já vista numa função deste tamanho, com só 6 `bl` distintos.

`GetShapePrim(int)` (×3, busca dado de primitivo por forma),
`iOS_getSkipAddPrim()` (×4, mesmo gate de skip da seção 108),
`SetDrawMode` (×2), `xpLibGetOffset(int*,int*)` (ajuste de
coordenada/clip), e `rsin`/`rcos` (trigonometria GTE pra rotação) —
consistente com o pipeline `SVECTOR`/`VECTOR` do `ASHURA`
(seção 38), não uma chamada bruta à GTE do PS1. A altíssima
proporção de branch de retrocesso pra só 6 callees indica iteração
bem apertada (desenrolada por vértice/sub-parte) sobre os pontos da
`Shape2`, espelhando o padrão de iteração por primitiva de
`dispPolygonObject` (seção 108) — os dois parecem ser o par
"carregar malha TMD" / "rasterizar forma convertida" da mesma
pipeline de desenho. Marcada `read_structural`.


## 110. `sceGuSendList`/`sceGuDrawArray` — NÃO são boilerplate: são a ponte real PSP-GU -> `CEGL2_*`, confirmando `GuEmu_libgu_to_gl` por um ângulo novo (2026-10-18, Fase 3)

Checagem rápida pela regra 6 da metodologia (nome `sce*` sugeria
código de compatibilidade PSP genérico) **revela o contrário**:
`sceGuSendList` (`0x2adab4`, 3.544 B, 94% de cobertura, 2 tabelas de
salto — 20 casos/15 handlers e 4 casos/3 handlers) e
`sceGuDrawArray` (`0x2ace34`, 3.200 B, 95% de cobertura, 2 tabelas de
salto — 6 casos/5 handlers e 4 casos/3 handlers) chamam
`CEGL2_IF::GetPacket`, `CEGL_PACKET::Add`/`SetTypeCurrent`/
`SetBlendModeCurrent`/`SetTextureCurrent`/`SetExtraCurrent` (×48!) e
`CFFT_STATE::GetVertexScaling`/`GetParam`/`FaceIDToFID` — chamadas
genuínas do motor do próprio jogo, não de uma lib PSP de verdade.

**Confirma `GuEmu_libgu_to_gl` por um segundo ângulo**: a API `sceGu*`
não é código de terceiros preservado — é a camada de compatibilidade
do PRÓPRIO jogo que traduz chamadas de desenho no estilo PSP (`libgu`)
pra pacotes `CEGL_PACKET` internos (que por sua vez vão pro OpenGL).
`GuEmu_GetRAW(int)` (chamada por ambas) é outro elo dessa ponte.

**Achado extra**: as duas funções compartilham a MESMA lista de ~13
locais sem símbolo (`0x2a3d74`...`0x2aa528`) como alvo das tabelas de
salto — consistente com um array compartilhado de handlers "por tipo
de primitivo/vértice" usado tanto no caminho de lista de comandos
quanto no de desenho de array direto. **35 branches/28 retrocesso**
(`sceGuSendList`) e **44/30** (`sceGuDrawArray`). Aceitas direto pela
regra 3 da metodologia (cobertura alta, tabelas resolvidas, sem
verificação manual extra). Marcadas `read_structural`.


## 111. `Wdisp_statusc()`/`Wdisp_option(int)` — quinta e sexta confirmação independente de que `W` é sempre a cópia real (2026-10-18, Fase 3, regra 2 da metodologia)

`family_sim.py` contra as bases recém-lidas (seções 106/107):

```
Wdisp_statusc()    0x1156f4  3.880 B   Jaccard 0,30 (vs disp_statusc)
Wdisp_option(int)  0x1431c4  3.828 B   Jaccard 0,21 (vs disp_option)
```
Jaccard baixo nas duas, como esperado — confirmam de novo que `W`
**não reusa nenhum helper sem prefixo**, chamando em vez disso sua
própria biblioteca `W`-prefixada: `Waddlocalprim`, `Winitsprtfield`,
`Waddstatusback`, `Winitstatusback`, `Witemuvclut`, `Wloadcdst`,
`Wbgput`, `Wstatuskanjiprint`, `Wsettaskkind`, `Wimport_localpad`,
`Wtask_create`, `Wtask_killmyself`, `Wwait_taskend`,
`Wsend_taskparamater`, mais `wasmTaskEntry`/`wasmGetInput3`/
`wasmGetActiveTask` (task `wasm`, não `asm`/task puro das bases).
Com estas duas, já são **cinco famílias independentes**
(`disp_personalwindow`, `disp_bothwindow`, `Wmultiwindow_*`,
`disp_statusc`, `disp_option`) confirmando o mesmo padrão
arquitetural: `W` é sempre uma recompilação de verdade do código-
fonte com sua própria biblioteca de helpers e task `wasm`, nunca um
ponto de entrada fino. Aceito direto via catálogo de `bl`, sem
verificação manual (regra 3). Marcadas `read_structural`.


## Nono lote paralelo (seções 112–117): 6 funções lidas por forks simultâneos, usando `jtable.py`

## 112. `ASHURA_MapProjectMem2Mem(unsigned char, char*)` — decodificador de registro com auto-recursão, tabela de 31 vias, carrega chunk de mapa (2026-10-18, Fase 3, lote paralelo)

`ASHURA_MapProjectMem2Mem(unsigned char, char*)` (`0x168ba8`,
3.632 B) — descida recursiva via `jtable.py`: **732 de ~908
instruções possíveis (81%)**; **uma tabela de salto resolvida**
(guarda `cmp` em `0x168bd4`, dispatch em `0x168bd8`, **124 casos, 31
handlers distintos** — `0x168e4c` domina como alvo default/catch-all
em ~95 dos 124 casos); **69 branches, 57 de retrocesso** — maior
densidade de laço relativa já vista (83%).

**Auto-recursão**: a própria função se chama de novo (×5) — confirma
que é um decodificador de stream de registros tipados (opcode
`unsigned char` + buffer `char*`) que processa chunks de mapa
aninhados/encadeados recursivamente. Chama `ASHURA_LMDL_Read` (×9,
seção pendente — carrega modelo linkado), funções de luz/câmera GTE
(`ASHURA_LightSwitch`, `ASHURA_LightMatrix`, `ASHURA_BackColor`,
`ASHURA_CVECTOR`, `setMapVector`), carregamento de textura/CLUT
(`loadClutData`, `IsMapTexAsideLoad`, `PSX_LoadImage`,
`xpLibgpuTPageGet`, `SetDrawMode`/`SetDrawMove`), checagem de
event-flag (`read_eventflag`) e, achado inesperado, uma chamada a
`iOS_getV2Icon` (ícone de save, sem relação aparente com mapa — fora
de contexto, possível reuso de helper genérico). **Conclusão**: é o
parser/streamer real de chunks de mapa — não matemática de vetor
pura, é a camada que decodifica o formato de arquivo de mapa e
dispara os sub-sistemas de iluminação/textura/modelo conforme o tipo
de registro lido. Marcada `read_structural`.

## 113. `bDB_init(...)` — boilerplate genuíno do PSYQ SDK (inicialização de double-buffer/ambiente de desenho), confirmado pela regra 6 (2026-10-18, Fase 3, lote paralelo)

`bDB_init(DB*, ...)` (`0x175a98`, 3.016 B) — 26 pointers de
primitivo (um por tipo: `POLY_F3`/`FT3`/`F4`/`FT4`/`G3`/`GT3`/`G4`/
`GT4`, `LINE_F2`/`F3`/`F4`/`G2`/`G3`/`G4`, `TILE`/`TILE_1`/`TILE_8`/
`TILE_16`, `SPRT`/`SPRT_8`/`SPRT_16`, mais `DR_MOVE`/`DR_AREA`/
`DR_MODE`) — a MESMA assinatura do `DB_Init`/`InitGeom` real da SDK
PSYQ do PS1. Descida recursiva: **726 de ~754 instruções possíveis
(96%)**, **zero tabela de salto**, **26 branches, só 2 de
retrocesso** — densidade de branch baixíssima, consistente com fiação
sequencial de ponteiros em struct, não lógica de jogo.

Catálogo de `bl` é exatamente o conjunto `Set<TipoPrimitivo>` (um
`SetPolyF3`/`SetPolyF4`/.../`SetTile16`/`SetSprt8` por parâmetro, na
mesma ordem da lista de parâmetros) mais `bSwapDB` (troca de double-
buffer) e `SetDefDispEnv`/`SetDefDrawEnv` (ambiente de display/
desenho padrão) — nenhuma chamada fora desse padrão. **Confirma, com
instrução real, boilerplate genuíno do SDK de renderização de baixo
nível do PS1** — zero lógica específica do jogo. Marcada `read_full`
(regra 6 da metodologia), não `read_structural`, por ser
reconhecidamente código de terceiros/SDK, não lógica própria do
motor do jogo.

## 114. `ASURA_LMDL_TIME_TBL()` — construtor de tabela de tempo de animação do modelo linkado (2026-10-18, Fase 3, lote paralelo)

`ASURA_LMDL_TIME_TBL()` (`0x165b68`, 2.996 B, termina exatamente em
`0x16671c` = `ASHURA_Control`) — descida recursiva via `jtable.py`:
**744 de ~749 instruções possíveis (99%)**, sem tabela de salto;
**54 branches, 23 de retrocesso**. Catálogo mínimo (4 `bl`
distintos) mas dominado por `__divsi3` (×27) e `rsin` (×18) dentro de
um laço — mais um local sem símbolo (`sub_714b8`, ×2) e uma única
chamada a `iOS_GetFrameRate()`. **Conclusão**: bate exatamente com o
nome — constrói uma tabela de temporização por quadro (muita divisão
inteira, provavelmente razão de interpolação/contagem de frame) com
seno pra interpolação angular/oscilação de curva de animação, gated
por taxa de quadro real — parte do sistema `LMDL` ("linked model",
seção 112) do motor `ASHURA`/`ASURA`. Marcada `read_structural`.

## 115. `Tutrial()` — controlador de task do overlay de tutorial, confirma e estende o subsistema já visto nas seções 106/107 (2026-10-18, Fase 3, lote paralelo)

`Tutrial()` (`0x1b937c`, 2.568 B, nome com erro de digitação real no
binário, "tutorial" sem o segundo `o`) — descida recursiva via
`jtable.py`: **606 de ~642 instruções possíveis (94%)**, sem tabela
de salto; **58 branches, 36 de retrocesso**. 26 `bl` distintos.

Confirma o subsistema de tutorial já sinalizado em `disp_option`
(`request_help`/`tutorial_syscall`, seção 106) e `disp_statusc`
(`Get_bravebreak`/`iOS_getTutorialbreak`/`iOSTutoCheck`, seção 107),
com 3 membros NOVOS: `tutorialstatusget(int)`, `iOS_setTutorialbreak
(unsigned short)`, e **`iOSTutoFlagAdd(int)`** (×6, a chamada mais
frequente). Também toca a camada de task `W` (`Wtask_create`/
`Wtask_status`/`Wsend_taskparamater`), o subsistema de mundo
(`world_stopnoend`, `load_worldname`), renderização (`DrawG4`,
`DrawModeChg`, `FadeOutInit`/`FadeOut`, `GetTPage`, `GetFrameRate`),
dados de personagem (`GetChrList`), ícone V2 (`iOS_getV2Icon`/
`setV2Icon`), input (`iOSHelpInputWaitSet`, `pspNetPadRead`),
arquivo (`fileDispose`, `SetLoadData`) e um reset completo
(**`CallresetFFT()`**, achado notável — confirma que existe uma
rotina de reset total do jogo acessível desde o tutorial). Dois
locais sem símbolo. Marcada `read_structural`.

## 116. `hight_font_draw(int)` — nome sugere desenho de fonte, catálogo revela plumbing de primitivo/OT estilo PSP (2026-10-18, Fase 3, lote paralelo)

`hight_font_draw(int)` (`0x287a78`, 2.548 B, nome com erro de
digitação real, "height" sem o `e`) — descida recursiva via
`jtable.py`: **633 de ~637 instruções possíveis (99%)**, sem tabela
de salto; só **6 branches, 2 de retrocesso**. Catálogo pequeno (5
`bl` distintos, 22 chamadas): `ASHURA_getOTptr()` (×10, ponteiro de
tabela de ordenação), `pspGetpspPrimWorkBuf(int)` (×5, buffer de
trabalho de primitivo estilo PSP), um local sem símbolo (×5),
`IS_TEX_2X()` (modo de textura 2x) e `iOS_setV2Icon`.

**Apesar do nome sugerir desenho de glifo/fonte, o catálogo de
chamadas não confirma lógica de fonte alguma** — é dominado por
plumbing de buffer de primitivo/tabela de ordenação estilo PSP, com
um único toque na camada `iOS_*` de ícone V2. Consistente com estar
na junção entre o renderizador legado PS1/PSP e a camada de UI iOS
mais nova (endereço na faixa `0x28xxxx`, junto dos outros `iOS_*`) —
mas o corpo real da lógica de glifo, se existir, está nos 2 branches
de retrocesso não expandidos ou no local sem símbolo. Marcada
`read_structural`.

## 117. `ctlhoukmes_main(CTLINFO*)` — controlador de mensagem de "relatório" em campo, confirma o framework `ctl*_main` compartilhado, tabela de 101 casos (2026-10-18, Fase 3, lote paralelo)

`ctlhoukmes_main(CTLINFO*)` (`0x25a908`, 2.504 B) — descida
recursiva via `jtable.py`: **508 de ~626 instruções possíveis
(81%)**; **uma tabela de salto resolvida** (guarda `cmp` em
`0x25a970`, dispatch em `0x25a974`, **101 casos, 20 handlers
distintos** — `0x25aeb0` domina como default em ~82 dos 101 casos);
**59 branches, 47 de retrocesso**. 19 `bl` distintos, 45 chamadas.

`houkoku` = "relatório" em japonês — a tabela de 101 casos despacha
por fase/estado guardado em `CTLINFO*`, dirigindo: seleção de texto
de mensagem (`houkokumes_select`), renderização da mensagem
(`houkoku_mesput`, ×15, caminho mais quente), uma variante
"yokoyari" (lança lateral, provavelmente relatório de um tipo
específico de ataque: `yokoyari_mesput`), janelas de overlay de
mundo (`wldwin_noropen`, `wldpicwin_set`, `add_winpac`), consultas de
unidade/mundo (`get_unitwork_add_wld`, `wldmes_load`, `pic_load`),
som (`sound_request`), checagem de traço de emprego
(`tokuseijob_check`), RNG (`ps_rand`) e primitivos PSX GPU/textura
diretos (`DrawSync`, `LoadClut`, `LoadTPage`, `GsGetTimInfo`) — a
própria função emite chamadas de desenho/carregamento de baixo
nível, não delega tudo a uma camada de renderização. Chama também
**`ctlhoukmes2_init(int)`**, confirmando um controlador companheiro
de segundo estágio.

**Confirma o framework compartilhado**: os primitivos de task
genéricos `Wtask_status`/`Wsend_taskparamater` (vistos em toda a
família `ctl*`) mais o parâmetro uniforme `CTLINFO*` sustentam a
hipótese de um framework comum "`ctl<nome>_main`" — cada função é
uma máquina de estado por sequência dirigida pelos mesmos primitivos
de controle de task, carregando o estado de fase em `CTLINFO`, com
sua própria tabela de salto de handlers de fase e seus próprios
helpers especializados de "mesput"/desenho.
`ctlhoukmes_main` especificamente governa uma sequência de popup/
mensagem de relatório em campo (provavelmente ligada a ações de
unidade ou texto de relatório de batalha), encadeando para
`ctlhoukmes2_init` como segundo estágio. Marcada `read_structural`.


## Décimo lote paralelo (seções 118–123): 6 funções lidas por forks simultâneos, usando `jtable.py`

## 118. `disp_helpmenu2()` — overlay de ajuda/legenda de controle touch, decodifica texto localizado via LZW (2026-10-18, Fase 3, lote paralelo)

`disp_helpmenu2()` (`0x1267f4`, 2.840 B) — descida recursiva via
`jtable.py`: **685 de ~710 instruções possíveis (96%)**, sem tabela
de salto; **40 branches, 17 de retrocesso**. 24 `bl` distintos.

Mistura plumbing de task/mensagem PSP (`task_wait`/`task_create`/
`send_taskparamater`, `checktaskkind`, **`pspMsgLzwBaseGet`** —
decodificador de texto localizado comprimido em LZW) com a pipeline
de polígono PSX (`addlocalprim`/`initpolyft4`, `GetTPage`/
`SetSemiTrans`) e a ponte de toque `iOS_*` (`iOS_hookHelp`,
`iOS_ClearRectHitAll`/`iOS_SetRectHit` pra retângulos de toque,
`iOS_getV2Icon`/`setV2Icon` pra ícones de botão virtual). Confirma
ser o overlay de legenda de ajuda/controle na tela de toque:
decodifica texto de ajuda localizado, desenha via pipeline PSX
legado, e registra retângulos de toque mais ícones V2 pra legenda de
controle em tela. Quatro locais sem símbolo. Marcada
`read_structural`.

## 119. `DressEquip()` — confirma que compartilha toda a infraestrutura de menu do `Equip()` regular, não é rotina isolada (2026-10-18, Fase 3, lote paralelo)

`DressEquip()` (`0x19b620`, 2.492 B) — descida recursiva via
`jtable.py`: **579 de ~623 instruções possíveis (93%)**, sem tabela
de salto; **39 branches, 15 de retrocesso**. 29 `bl` distintos.

Confirma que `DressEquip` (tela de equipar traje/visual, distinta do
`Equip()` de arma/armadura já lido) usa a MESMA biblioteca
`iOS_CMenuTouch` (`setDispOffset`/`setYLine`/`setXIconRect`/
`drawMenuAssist`/`init`/`exec`), os MESMOS primitivos de item
(`ItemEquip`/`IsItemEquip`/`GetItemPrice`/`GetShopItemList`) e de
janela (`WindowInit2`/`DrawWindow2`/`SetWindowPosition`/
`WindowPrioritySet`/`CursolFunc`) que outras telas de equipar/loja —
não é uma rotina isolada de mutação de dado, é uma tela interativa
completa sobre o mesmo toolkit compartilhado. Também toca estado de
unidade (`ChrPowerCompare`, `SetSttsPara2`, `CurChrChg2`,
`unit_isdark`) e som (`iOS_soundDirect`). Três locais sem símbolo.
Marcada `read_structural`.

## 120. `requestChangeClut(...)` — confirma ser o lado produtor da fila de `executeChangeClut` (seção 70): zero chamadas externas, duas tabelas de salto de 11 vias (2026-10-18, Fase 3, lote paralelo)

`requestChangeClut(int, int, unsigned int, unsigned int, int, short,
short, short)` (`0x211f14`, 2.440 B) — descida recursiva via
`jtable.py`: **582 de ~610 instruções possíveis (95%)**; **duas
tabelas de salto resolvidas**, ambas de 11 casos/10 handlers
distintos (guardas `cmp` em `0x211ff8` e `0x212468`); **43 branches,
32 de retrocesso**.

**Achado estrutural notável**: **zero chamadas `bl`** — a função não
invoca NENHUMA outra função (nem helper, nem libc), só grava campos.
Combinado com duas tabelas de 11 vias de formato idêntico (mesmo
padrão de colapso de duplicata), isso é consistente com uma função
que só "estampa" um registro de requisição tagged-union na fila que
`executeChangeClut()` (seção 70) depois consome — primeiro switch
provavelmente escolhe o slot/tipo de requisição, segundo escolhe
quais campos dos 8 parâmetros grava nesse slot. Confirma com
instrução real a relação produtor/consumidor hipotetizada na seção
70. Marcada `read_structural`.

## 121. `attack_assumechr()` — NÃO é matemática de pose, é carregamento assíncrono de recurso pro preview de ataque (2026-10-18, Fase 3, lote paralelo)

`attack_assumechr()` (`0xc8238`, 2.416 B) — descida recursiva via
`jtable.py`: **541 de ~604 instruções possíveis (90%)**; **uma
tabela de salto resolvida** (guarda `cmp` em `0xc8730`, dispatch em
`0xc8734`, 36 casos, só **4 handlers distintos** — um domina 32 dos
36 casos); **63 branches, 38 de retrocesso**. 18 `bl` distintos.

**Achado que corrige a hipótese inicial**: em vez de calcular pose/
posição 3D hipotética, a função é dominada por I/O e carregamento de
asset: `mallocForFile`/`fileReadRequest`/`fileDispose`/
`numa_fileReadCD` (carregamento de arquivo), `PSX_LoadImage` (×6)/
`StoreImage`/`ClearImage`/`DrawSync` (pipeline de imagem PSX),
`__bpInitBinpackData`/`__bpGetBinaryData` (leitura de arquivo
binpack empacotado), `get_unitwork_add`/`get_jobdata` (dados de
unidade/emprego) e `asmTaskEntry` (dispatch assíncrono — a carga é
enfileirada como task em background). **"Assume" aqui parece
significar "carregar/preparar a representação hipotética do
personagem"** pro preview de alvo, não calcular matemática de pose
diretamente — a tabela de salto de 36 casos despacha por tipo de
recurso/estado durante essa sequência de carga. Marcada
`read_structural`.

## 122. `attack_assumeface()` — irmã de `attack_assumechr`, mesma lógica pro retrato/rosto (2026-10-18, Fase 3, lote paralelo)

`attack_assumeface()` (`0xc8ba8`, 2.396 B, imediatamente adjacente a
`attack_assumechr`) — descida recursiva via `jtable.py`: **535 de
~599 instruções possíveis (89%)**; **uma tabela de salto resolvida**
(guarda `cmp` em `0xc8fcc`, dispatch em `0xc8fd0`, 36 casos, 4
handlers — mesma forma da seção 121: um handler domina 32 dos 36
casos); **57 branches, 31 de retrocesso**. 19 `bl` distintos.

Confirma ser a contraparte de retrato/rosto: resolve ID de rosto do
mundo pra ID de rosto (`CFFT_STATE::WorldFaceIDToFaceID`), lê dados
de ícone via `__bpInitBinpackData`/`__bpGetBinaryData` (×4) e
`numa_fileReadCD`, desenha via pipeline de imagem PSX
(`PSX_LoadImage` ×7, `StoreImage`/`MoveImage`/`DrawSync`) com
`xpMallocIO`/`xpFree`/`mallocForFile`/`fileDispose` pra buffer,
também toca dados de unidade/emprego e `iOS_setTransFaceAT`/
`iOS_getV2Icon` (×6). Confirma que constrói o ícone de retrato
previsto mostrado no preview de ataque, selecionado por emprego/
estado de unidade, com a mesma forma de tabela de salto de 36 casos
da seção 121. Marcada `read_structural`.

## 123. `ASHURA_LMDL_Read(...)` — confirma ser o parser real do sistema `LMDL`, dominado por um laço de 21 chamadas a `new_Vector` (2026-10-18, Fase 3, lote paralelo)

`ASHURA_LMDL_Read(unsigned short*, L_MATRIX*, int)` (`0x16828c`,
2.332 B, termina exatamente em `0x168ba8` = início de
`ASHURA_MapProjectMem2Mem`, seção 112, que a chama ×9) — descida
recursiva via `jtable.py`: **568 de ~583 instruções possíveis
(97%)**, sem tabela de salto; **19 branches, 9 de retrocesso**.
Catálogo mínimo (4 `bl` distintos) mas revelador: `new_Vector
(VECTOR_DATABASE*, SVECTOR const*)` domina com **21 chamadas (~84%
de todas as chamadas)** — consistente com um laço apertado
construindo entrada de vetor/matriz enquanto percorre uma lista de
nó/osso. `new_VectorDataBase`/`new_ColorVectorDataBase` (×1 cada)
parecem ser setup/alocação única dos pools de vetor antes do laço, e
`pspMapArrayOperate` (×2, mesma família tocada por
`ASHURA_MapProjectMem2Mem`) liga esta função ao mesmo subsistema de
array de mapa/geometria. **Confirma ser o parser central do LMDL**
("linked model") que constrói a hierarquia de matriz linkada
(`L_MATRIX`) a partir do buffer fonte — sem tabela de salto, fluxo
de laço linear por nó, não um decodificador por switch. Fecha o
trio `ASHURA_MapProjectMem2Mem`/`ASURA_LMDL_TIME_TBL`/
`ASHURA_LMDL_Read` do sistema `LMDL` (seções 112/114/123). Marcada
`read_structural`.


## Décimo-primeiro lote paralelo (seções 124–129): 6 funções lidas por forks simultâneos, usando `jtable.py`

## 124. `ctlendroll_main(CTLINFO*)` — confirma ser o controlador dos créditos finais, tabela de 5 casos (2026-10-18, Fase 3, lote paralelo)

`ctlendroll_main(CTLINFO*)` (`0x24265c`, 2.488 B) — descida recursiva
via `jtable.py`: **594 de ~622 instruções possíveis (95%)**; **uma
tabela de salto resolvida** (guarda `cmp` em `0x24268c`, dispatch em
`0x242690`, **5 casos, 5 handlers distintos**); **18 branches, 9 de
retrocesso**.

Catálogo pequeno (6 `bl` distintos) mas com um nome que confirma a
hipótese de cara: **`vEnd_rollproc()`** ("end roll proc") — função
dedicada exclusivamente aos créditos finais. O resto do catálogo é
runtime de ponto flutuante do compilador (`__subdf3`/`__adddf3`/
`__fixdfsi` ×6, matemática de posição de scroll/tempo) mais
`pspGetpspPrimWorkBuf`/`xpFree` (setup/teardown de buffer de
desenho). Tabela de salto bem mais simples (5 casos) que
`ctlhoukmes_main` (101 casos, seção 117) — consistente com uma
sequência linear (fade-in, scroll, fade-out, fim) em vez de um
dispatcher de muitos estados. Confirma o framework `ctl*_main`
(parâmetro `CTLINFO*` uniforme), mesmo sem as chamadas genéricas
`Wtask_status`/`Wsend_taskparamater` aparecerem nesta função
especificamente. Marcada `read_structural`.

## 125. `ctlbrst_main(CTLINFO*)` — hub de menu com transição pra 8 outros sub-controladores `ctl*_init`, "brst" é seção de UI, não efeito visual (2026-10-18, Fase 3, lote paralelo)

`ctlbrst_main(CTLINFO*)` (`0x24d068`, 2.272 B) — descida recursiva
via `jtable.py`: **536 de ~568 instruções possíveis (94%)**; **uma
tabela de salto resolvida** (guarda `cmp` em `0x24d1e4`, dispatch em
`0x24d1e8`, **7 casos, 7 handlers distintos**); **45 branches, 27 de
retrocesso**. **38 `bl` distintos** — maior catálogo já visto na
família `ctl*_main`.

**Corrige a hipótese inicial**: "brst" não é um efeito de flash de
tela — a função é um **hub de menu** que transiciona pra **8 outros
sub-controladores**: `ctlkiroku_init`, `ctlperson_init`,
`ctlwork_init`, `ctlopt_init`, `ctlhelp_init`, `ctlhistory_init`,
`ctltresure_init`, `ctlunreg_init` (mais `wldctl_deactive`), e chama
sua própria rotina de desativação `ctlbrst_deactive(CTLINFO*)` (×7).
Confirma o framework compartilhado via `Wtask_status`/
`Wsend_taskparamater`, e usa a biblioteca `iOS_CMenuTouch` completa
(`init`/`exec`/`setDispOffset`/`setYLine`/`setDispAssist`) mais
`iOS_setDispMenuTouch`/`iOS_setV2Icon` (×9) — é a tela de menu
principal com ícones de toque que dá acesso a registro (`kiroku`),
dados de personagem (`person`), trabalho (`work`), opções (`opt`),
ajuda (`help`), histórico (`history`), tesouro (`tresure`) e
desbloqueáveis (`unreg`). `wldfade_set`/`wlddisp_mask`/`wldfrm_clr`
cuidam da transição de tela, `sound_request`/`ssd_request`/
`wldmusic_change` do áudio do menu. Marcada `read_structural`.

## 126. `p20_gunFunc()` — efeito de projétil de arma de fogo, matemática GTE completa com primitivos de polígono diretos (2026-10-18, Fase 3, lote paralelo)

`p20_gunFunc()` (`0x2235f4`, 2.352 B) — descida recursiva via
`jtable.py`: **566 de ~588 instruções possíveis (96%)**, sem tabela
de salto; **45 branches, 25 de retrocesso**. 32 `bl` distintos.

Mistura ciclo de vida de objeto/efeito do `ASHURA`
(`LockEffectCompelBreak`/`UnlockEffect`/`GetEffectStatus`,
`GetPermanentObject`/`DisposePermanentObject`) e lógica de jogo real
(**`requestPhysicalDamage(int,int)`**, **`changeFlameRate(int)`** —
sugere um efeito de arma de fogo com componente de chama/fogo) com
matemática GTE pesada (`rsin`/`rcos`/`ratan2`/`SquareRoot12`/
`SquareRoot0`, `SetRotMatrix`/`SetTransMatrix`/`RotTransPers`/
`RotTransPers3`/`RotTrans`) e primitivos de polígono diretos
(`AddPrim`, `SetPolyG3` ×8, `SetPolyG4`, `SetPolyFT4`,
`dispPolygonObject` — seção 108, `TexHybrid_RegistCLUTAddr`,
`IS_TEX_2X()`) mais acesso a dado de item (`itemuvclut`,
`pspItemGetCommonData` ×4). Sem tabela de salto — constrói e
transforma seus próprios primitivos de polígono por quadro, não
delega a um dispatcher de tabela de partícula. Consistente com um
efeito visual de projétil/impacto de arma de tiro (flash de cano,
traçador ou explosão) com dano físico associado. Marcada
`read_structural`.

## 127. `disp_status3()` — terceira variante confirmando a mesma biblioteca de desenho de tela de status (2026-10-18, Fase 3, lote paralelo)

`disp_status3()` (`0xe5998`, 2.292 B) — descida recursiva via
`jtable.py`: **553 de ~573 instruções possíveis (97%)**, sem tabela
de salto; **33 branches, 19 de retrocesso**. 30 `bl` distintos.

Confirma, sem introduzir categoria de helper nova, que `disp_status3`
reusa a MESMA biblioteca de desenho de tela de status já catalogada
em `disp_statusc`/`disp_personalwindow`/`disp_bothwindow`:
`addlocalprim` (chamada mais pesada, ×16), `initpolyft4`/
`initsprtfield`, `disposetexture`/`allocatetextureconst`, a família
`addstatusback`/`sttsback_normal`/`sttsback_blue`/`initstatusback`,
`bgput`, `loadcdst`/`initdrmode`, e o par de texto
`statusfigprint`/`statuskanjiprintwithptr`, mais os helpers de ciclo
de task padrão (`task_killmyself`, `asmTaskEntry`,
`asmGetInput3`/`asmGetActiveTask`) e primitivos PSX GPU
(`PSX_LoadImage`, `GetTPage`, `SetDrawOffset`, `SetSemiTrans`). É a
terceira variante confirmada sobre a mesma biblioteca compartilhada
— nenhuma lógica estruturalmente nova. Dois locais sem símbolo.
Marcada `read_structural`.

## 128. `make_abilitylistmain(int)` — agregador de lista de habilidade, toca todas as categorias de item/habilidade de uma vez (2026-10-18, Fase 3, lote paralelo)

`make_abilitylistmain(int)` (`0xd5d6c`, 2.288 B) — descida recursiva
via `jtable.py`: **546 de ~572 instruções possíveis (95%)**, sem
tabela de salto; **69 branches, 36 de retrocesso** — alta densidade
de laço (percorrendo slots de habilidade por categoria).

Catálogo pequeno (11 `bl` distintos) mas cobre TODAS as categorias de
habilidade/item do jogo numa função só: `set_monsterability2`,
`set_normability2` (habilidade de emprego), `set_itemitem`,
`set_throwitem`, `set_katanaitem`, as três habilidades de `sanjutsu`
(ninjutsu) — `set_sanjutsuability1`/`2`/`3` — e `set_chargeability2`,
mais `get_bwp` (seção 43). **Confirma ser o agregador real que
monta a lista de habilidade exibida no menu de seleção**, puxando
dado de cada tabela de categoria pra popular linhas da tela. Sem
tabela de salto — dispatch de categoria é por branch condicional
direto. Um local sem símbolo (×2). Marcada `read_structural`.

## 129. `itemmenu_call(...)` — híbrido: cria a task do menu de item E desenha seus próprios tiles, não é wrapper fino (2026-10-18, Fase 3, lote paralelo)

`itemmenu_call(unsigned long*, unsigned long, int)` (`0x12cdcc`,
2.168 B) — descida recursiva via `jtable.py`: **509 de ~542
instruções possíveis (94%)**, sem tabela de salto; **41 branches, 22
de retrocesso**. 10 `bl` distintos.

**Corrige a hipótese inicial** de que seria um wrapper fino que só
dispara a task do `ItemMenu`: a função toca primitivos de GPU reais
(`addlocalprim` ×4, `SetTile` ×5, `SetSemiTrans` ×5, `SetDrawMode`,
`GetTPage`) e import/export de pad local (`import_localpad`/
`export_localpad`), além de `asmTaskEntry`/`asmGetActiveTask` (×1/×2)
pra criar/checar a task. 22 branches de retrocesso com só 94% de
cobertura confirma trabalho de desenho real por quadro (provavelmente
ícones/cursor do menu de item com transparência), não só um ponto de
entrada que delega tudo. Marcada `read_structural`.


## 130. `Wdisp_status3`/`Wmake_abilitylistmain`/`Witemmenu_call` — sétima confirmação do padrão `W`, com uma excecao reveladora pra lógica pura de dado (2026-10-18, Fase 3, regra 2 da metodologia)

`family_sim.py` contra as três bases recém-lidas:

```
Wdisp_status3           0x11c2bc  2.296 B   Jaccard 0,13 (vs disp_status3, §127)
Wmake_abilitylistmain    0xfd318  2.288 B   Jaccard 1,00 (vs make_abilitylistmain, §128)
Witemmenu_call           0x135218 2.188 B   Jaccard 0,33 (vs itemmenu_call, §129)
```

**`Wdisp_status3`**: Jaccard baixíssimo, confirmando o padrão pela
sétima vez — biblioteca `W`-prefixada própria (`Winitpolyft4`,
`Wdisposetexture`, `Wallocatetextureconst`, `Wchecktaskkind`,
`Wstatusfigprint`, `Wstatuskanjiprintwithptr`) mais `wasmTaskEntry`/
`wasmGetInput3`/`wasmGetActiveTask`.

**`Witemmenu_call`**: Jaccard baixo (0,33), mesmo padrão — chama
`Wimport_localpad`/`Wexport_localpad` e `wasmTaskEntry`/
`wasmGetActiveTask` em vez das versões sem prefixo.

**`Wmake_abilitylistmain` — EXCEÇÃO reveladora**: Jaccard **1,00**,
catálogo de `bl` idêntico ao da base (§128). Diferente de toda
função de desenho/UI já vista, aqui `W` não precisa de biblioteca
própria porque os 11 `bl` da base são TODOS acessores de dado puro
(`set_monsterability2`/`set_normability2`/`set_itemitem`/etc.) — não
existe versão `W`-prefixada de funções de dado, só de funções de
desenho/task/janela. **Isso refina a regra geral**: `W` duplica
helpers de DESENHO/TASK (que fazem sentido existir em dois
contextos: task normal vs. task `wasm`), mas reusa diretamente
funções de ACESSO A DADO puro, que são as mesmas independente do
contexto de exibição — a lógica de agregação de lista é
literalmente recompilada duas vezes chamando as MESMAS funções de
dado. Todas as três marcadas `read_structural`.


## 131. `disp_equipwindow()`/`Adisp_equipwindow()`/`Ddisp_equipwindow()`/`Cdisp_equipwindow()` — quatro trampolins triviais de 16 B, só `asmTaskEntry()` e retorno (2026-10-18, Fase 3, regra 3 da metodologia)

Diferente de TODA outra família de letra já vista neste projeto
(`disp_personalwindow`, `disp_bothwindow`, `disp_statusc`/
`disp_status3`, onde base e letras são telas completas de milhares
de bytes), a família `disp_equipwindow` tem a base e três letras
(`A`/`D`/`C`) com **só 16 B cada** — 4 instruções, 100% de
cobertura, **uma única chamada a `asmTaskEntry()` e retorno**,
nenhum branch. São trampolins puros de entrada de task, não telas
reais. Apenas `E` (2.156 B) e `W` (2.148 B, deixadas pra leitura
completa) têm tamanho de tela de verdade. Aceitas direto (regra 3 da
metodologia — cobertura de 100%, zero branch, nada a verificar
manualmente). Marcadas `read_full`.


## Décimo-segundo lote paralelo (seções 132–137): 6 funções lidas por forks simultâneos, usando `jtable.py`

## 132. `ASHURA_Control(...)` — finalmente lida: é um processador de sub-opcode interno de 52 casos, NÃO a tabela de dispatch `Mdl0001`–`Mdl0028` (2026-10-18, Fase 3, lote paralelo)

`ASHURA_Control(unsigned long, unsigned long, long, long)`
(`0x16671c`, 1.988 B) — a função mais chamada de toda a investigação
(dezenas de `Mdl*` e stubs triviais a invocam), lida por inteiro por
fim. Descida recursiva via `jtable.py`: **421 de ~497 instruções
possíveis (85%)**; **uma tabela de salto resolvida** (guarda `cmp`
em `0x166730`, dispatch em `0x166734`, **52 casos, 14 handlers
distintos** — `0x166814` domina como default/no-op em ~29 dos 52
casos); **36 branches, 26 de retrocesso**.

**Corrige a hipótese natural**: a tabela de 52 casos NÃO é o
dispatch por ID de modelo/efeito que os `Mdl0NNN` usam — nenhum
handler chama qualquer `Mdl0NNN` ou algo parecido. O catálogo de
`bl` é mínimo (6 distintos) e todo de baixo nível:
`VectorDataBase_SetFlag` (×6), `new_VectorDataBase`/
`new_ColorVectorDataBase`, `SetDrawMode` (×4), `system_warning`.
**Conclusão**: `ASHURA_Control` é um processador de sub-opcode
genérico de baixo nível (switch sobre um dos parâmetros `unsigned
long`, provavelmente código de comando 0–51) que manipula objetos
`VectorDataBase`/`ColorVectorDataBase` e modo de desenho — a maioria
dos casos cai no caminho default compartilhado, só um punhado faz
trabalho real (alocar vector DB, setar flag, setar modo de desenho).
**O dispatch real por ID de efeito/modelo (`Mdl0001`→efeito
específico) deve acontecer a MONTANTE**, nos vários stubs que
chamam `ASHURA_Control` com argumentos fixos diferentes —
`ASHURA_Control` é o primitivo de baixo nível compartilhado em que
todos desembocam, não o roteador por ID de efeito em si. Marcada
`read_structural`.

## 133. `Settings_FrameRender()` — revela um toolkit de UI moderno baseado em OpenGL ES/`CEGL2_*`, inteiramente separado da pipeline PSX legada (2026-10-18, Fase 3, lote paralelo)

`Settings_FrameRender()` (`0x2c6550`, 2.412 B) — descida recursiva
via `jtable.py`: **580 de ~603 instruções possíveis (96%)**, sem
tabela de salto; **13 branches, 5 de retrocesso**. 25 `bl`
distintos.

**Achado arquitetural novo**: revela um toolkit de renderização de
UI inteiramente separado da pipeline PSX/GTE legada já documentada —
`CEGL2_IF::AddSprite` (×14, dominante)/`AddTile`/`Setup2D`/
`DrawPacket`/`ClearBackdrop`/`InitRenderState2D`/`SetScreenSize`,
`CEGL2_FBO::Begin`/`End`/`RenderToFBO` (framebuffer offscreen),
`CEGL2_SPRITE::GetImageSize`, `CGX_SCREEN_CORRECT::GetCorrect`/
`GetAppScreenSize`/`GetAppScaledScreenSize`, `CRECT::GetRect` (×11,
layout de retângulo), `CINPUT_IF_TOUCH::GetPress`/`GetDown` (toque
embutido no próprio desenho), `CAPP_INFO::IsEnableVibration`,
**`SettingsBundle_Get()`** (×4, leitura de configuração persistida) e
**`RETINA_SCALE(int)`** (×8, escala de DPI). **Confirma que a tela
de configurações nativa (distinta do `disp_option` in-game, seção
106) é construída sobre uma camada C++ moderna (`CEGL2_*`/`CRECT`/
`CAPP_INFO`/`CGX_SCREEN_CORRECT`) que abstrai OpenGL ES** — um
sistema de UI completamente separado da pipeline de polígono PS1
usada em todo o resto do jogo. Marcada `read_structural`.

## 134. `SettingsWnd_FrameRender()` — segunda confirmação do toolkit `CEGL2_*`, variante com recorte por scissor-rect (2026-10-18, Fase 3, lote paralelo)

`SettingsWnd_FrameRender()` (`0x2c8194`, 2.292 B) — descida recursiva
via `jtable.py`: **557 de ~573 instruções possíveis (97%)**, sem
tabela de salto; **11 branches, 5 de retrocesso**. 27 `bl` distintos.

Confirma o mesmo toolkit `CEGL2_*` da seção 133, com recorte extra
por scissor-rect (`CEGL2_IF::GetScissor`/`SetScissor` ×2 variantes),
`CEGL2_SPRITE::SetScale`/`SetScaleAlignCenter`/`SetColor` (×4 cada,
posicionamento/cor por sprite), `CAPP_INFO::IsDeviceiPhoneRetina4inch`
(detecção de dispositivo), e um local (`sub_2c7060`, ×13 — o alvo
mais chamado, provável sub-rotina de desenho por item/linha
compartilhada). Variante "janela" (`Wnd`) da mesma tela, com clipping
adicional — consistente com um diálogo/popup sobreposto em vez da
tela cheia. Marcada `read_structural`.

## 135. `SettingsWnd_FrameMove()` — confirma o par update/draw: só input e mutação de estado, zero desenho (2026-10-18, Fase 3, lote paralelo)

`SettingsWnd_FrameMove()` (`0x2c78d4`, 2.240 B, termina exatamente
onde `SettingsWnd_FrameRender` começa) — descida recursiva via
`jtable.py`: **519 de ~560 instruções possíveis (93%)**; **duas
tabelas de salto resolvidas** (5 casos/5 handlers e 6 casos/5
handlers); **45 branches, 31 de retrocesso**. 22 `bl` distintos.

**Confirma ser a contraparte "update" do "draw" de
`SettingsWnd_FrameRender`**: só toque (`CINPUT_IF_TOUCH::GetPress`/
`GetDown`/`GetUp`/`GetRepeat`/`GetTouchPoint` ×7/`GetTouchCount`),
geometria de UI (`CRECT::FrameMove`/`SetEnable` ×8/`GetScreenOffset`),
áudio (`SysSE_PlayDef` ×5, `CSOUND_IF::SetMasterVolume`),
`SettingsBundle_Get` (×12) e `RETINA_SCALE` (×24, uso pesadíssimo) —
**zero chamada de desenho/GPU**. Confirma a separação limpa
update/draw já esperada pela convenção de nome `FrameMove`/
`FrameRender` usada em `Main_*`. Marcada `read_structural`.

## 136. `time_flies(int)` — NÃO é efeito visual, é processamento de status de fim-de-turno por unidade (2026-10-18, Fase 3, lote paralelo)

`time_flies(int)` (`0x1d59fc`, 2.288 B) — descida recursiva via
`jtable.py`: **539 de ~572 instruções possíveis (94%)**; **uma
tabela de salto resolvida** (guarda `cmp` em `0x1d5a58`, dispatch em
`0x1d5a5c`, 20 casos, 15 handlers distintos); **84 branches, 39 de
retrocesso**.

**Corrige a hipótese inicial**: nome sugere algo visual ("o tempo
voa"), mas o catálogo é dominado por bookkeeping de efeito de status
por unidade: `status_handle_main`, `status_countdown`,
`check_hide_reset`, `check_tobe_crystal` (transformação em cristal/
morte), `inc_dead_number`, `get_floor_damage`, `set_monomane_act`/
`overlayMonomaneStack` (habilidade Monomane/Mímica), `set_cco_SD`, e
termina com **`set_turn_end(int)`** — tudo controlado por
`check_unit_active` (×8, a chamada mais pesada, sugere iterar/validar
várias unidades). **Conclusão**: é a rotina de processamento de
status de fim de turno/tick — avança contadores de status, checa
morte/cristal/esconder, dano de piso, e finalmente fecha o turno —
não um efeito visual literal. Um local sem símbolo. Marcada
`read_structural`.

## 137. `drawmessagepolygons()` — emissor de quad PSX direto pra caixa de diálogo, sem tabela de salto (2026-10-18, Fase 3, lote paralelo)

`drawmessagepolygons()` (`0xe062c`, 2.240 B) — descida recursiva via
`jtable.py`: **551 de ~560 instruções possíveis (98%)**, sem tabela
de salto; **52 branches, 26 de retrocesso**. 18 `bl` distintos.

Emissor de primitivo de GPU estilo PSX direto pra caixa de mensagem:
constrói quads `POLY_FT4` via `addlocalprim`/`addlocalprim2` (×12/
×11, os dois alvos mais pesados — consistente com emissão de quad
por glifo/tile num laço), resolve estado de textura/CLUT via
`GetTPage`/`GetClut`/`faceuvclut`, e lê/grava dado de rosto e ícone
via os acessores `iOS_*` (`iOS_getTransFace`/`getTransFaceEVT`/
`getTransFaceForChrRemove`, `iOS_getV2Icon`/`setV2Icon`,
`iOS_getFaceDataID`/`setFaceDataID`) e `CFFT_STATE::GetParam`/
`SetParam` (×13, o alvo mais chamado de todos). `pspWorldCheckFlg`/
`IS_TEX_2X` sugerem gate específico da camada de port PSP->mobile.
Alta densidade de laço (26 de retrocesso) consistente com laço
aninhado clássico de era PSX construindo muitos quads pequenos pros
glifos/tiles da mensagem — usa a pipeline legada, não o toolkit
`CEGL2_*` das seções 133–135. Marcada `read_structural`.


## 138. `vorbis_synthesis_blockin`/`_tr_flush_block`/`mdct_forward`/`mdct_backward` — mais quatro internos de `libvorbis`/`zlib` reconhecidos por nome (2026-10-18, Fase 3, regra 6 da metodologia)

Quatro símbolos genuínos de bibliotecas de terceiros upstream:
`vorbis_synthesis_blockin` (`0x85fe0`, 2.068 B, API real de
`libvorbis`), `_tr_flush_block` (`0x7f4a8`, 1.960 B, interno de
`deflate.c` do `zlib`), `mdct_forward`/`mdct_backward` (`0x91898`/
`0x91128`, 1.932/1.904 B, transformada MDCT de `libvorbis`).
Checagem rápida via `jtable.py`: **99–100% de cobertura** nas
quatro, **zero tabela de salto**, catálogos de `bl` mínimos (3–5
alvos) dominados por runtime de ponto flutuante do compilador
(`__addsf3`/`__subsf3`) e helpers locais sem símbolo — nenhuma
chamada a função prefixada do jogo nas quatro. Confirma serem código
de terceiros genérico, mesma família já identificada nas seções
17.x/102. Marcadas `read_full` sem passe completo, regra 6 da
metodologia.


## Décimo-terceiro lote paralelo (seções 139–144): 6 funções lidas por forks simultâneos, usando `jtable.py`

## 139. `getShadowRect(tag_animation*)` — confirma que a sombra consulta diretamente mapa e vetor de animação (2026-10-18, Fase 3, lote paralelo)

`getShadowRect(tag_animation*)` (`0x1ebffc`, 2.240 B) — descida
recursiva via `jtable.py`: **559 de ~560 instruções possíveis
(100%)**, sem tabela de salto; **32 branches, 15 de retrocesso**.
Catálogo mínimo (2 `bl` distintos): `get_mapstp(int,int,int)`
(sistema de grade de mapa/terreno, seção 112) e
`setAnimationRealVector(SVECTOR*, tag_animation*)` (sistema de
posição real de animação). Alta densidade de laço (15 de 32) pra só
duas chamadas sugere trabalho geométrico iterativo (percorrer
células/vértices de mapa pra montar o retângulo de sombra), não
aritmética simples. Confirma que o sistema de sombra consulta
DIRETAMENTE o mapa/terreno (pra terreno irregular) e o rastreador de
posição de animação, como esperado pra posicionamento de sombra sob
unidade em movimento. Marcada `read_structural`.

## 140. `s28_doSchedule(_EffectTCB*)` — efeito cinemático multi-estágio: fade de paleta, câmera, partícula e som num só agendamento (2026-10-18, Fase 3, lote paralelo)

`s28_doSchedule(_EffectTCB*)` (`0x21d620`, 2.236 B, 28º da família
de efeitos agendados `s*`, distinta da família `Mdl*`/`p*`) —
descida recursiva via `jtable.py`: **551 de ~559 instruções
possíveis (99%)**, sem tabela de salto; **47 branches, 19 de
retrocesso**. 16 `bl` distintos.

Mistura várias subsistemas num único callback agendado: efeito de
tela/paleta (`changeMapClut`, `changeCharacterClut` ×3,
`changeGradation`, `changeFlatColor` ×2, `fadeGradation`,
`fadeFlatColor`), scripting de câmera (`SetCameraWorkWithSchedule`),
controle de taxa de quadro (`setFrameRate`, `GetSQLFrameRate`),
agendamento de partícula/efeito (`doSchedulePtclCommandOnce` ×2,
`StartPermanentEffect`, `CreateObjectWithTable`), e som
(`getNextSENo`, `Ssd_PlayEffect`). **Conclusão**: o efeito #28 é uma
sequência "cinemática"/transição multi-estágio — encadeia mudanças
de cor/iluminação (fade de CLUT de mapa e personagem, fade de cor
plana/gradação), movimento de câmera, spawna um sub-efeito/objeto
permanente, e toca som — não é um emissor de partícula simples como
os efeitos de número menor. Dois locais sem símbolo. Marcada
`read_structural`.

## 141. `wipe_const()` — transição de tela rotativa/escalada, orientada a task com matemática GTE real (2026-10-18, Fase 3, lote paralelo)

`wipe_const()` (`0x14e0ec`, 2.228 B) — descida recursiva via
`jtable.py`: **543 de ~557 instruções possíveis (97%)**, sem tabela
de salto; **27 branches, 16 de retrocesso**. 16 `bl` distintos.

Função orientada a task (`settaskkind`, `task_wait`, `asmTaskEntry`,
`asmGetInput2`) que dirige uma pipeline GTE/renderização estilo PSX
pra efeito de wipe de quad: constrói/atualiza quads `POLY_F4` via
`addlocalprim2` (×5)/`SetPolyF4`, lê estado de textura/modo de
desenho/transparência (`GetTPage`, `SetDrawMode`, `SetSemiTrans`), e
usa matemática de matriz/geometria real (`SquareRoot0`, `RotMatrix`,
`ApplyMatrixLV`) junto com checagem de event-flag
(`read_eventflag`). Confirma ser uma transição de wipe de tela
rotativa/escalada de verdade, orientada pelo agendador de task com
operações de matriz estilo GTE, não um wipe linear simples. Dois
locais sem símbolo. Marcada `read_structural`.

## 142. `get_ability(int, int)` — front-end fino sobre `get_command_ability`, confirma representação unificada de habilidade (2026-10-18, Fase 3, lote paralelo)

`get_ability(int, int)` (`0x1d82a8`, 2.224 B) — descida recursiva via
`jtable.py`: **539 de ~556 instruções possíveis (97%)**, sem tabela
de salto; **97 branches, 52 de retrocesso** — densidade de branch
muito alta pra um único callee.

**Único `bl` distinto**: `get_command_ability(int,int)`, chamada
**16 vezes**. Sem outras chamadas externas e sem tabela de salto —
os 97 branches (52 de retrocesso) sugerem um laço/filtro inline
escaneando registros de habilidade-comando repetidamente, em vez de
um dispatch de tabela simples. Fica um nível abaixo de
`make_abilitylistmain` (seção 128, que agrega via `get_bwp`/
`set_*ability2`/etc.) — `get_ability` parece ser uma busca
especializada que canaliza inteiramente por `get_command_ability`,
sugerindo que registros de "habilidade" neste código são
representados/resolvidos como "habilidade de comando" — confirma uma
representação de dado unificada por baixo dos vários tipos de
habilidade. Marcada `read_structural`.

## 143. `sBattleTouchRotation()` — confirma ser o handler real de arrastar-pra-rotacionar câmera em batalha (2026-10-18, Fase 3, lote paralelo)

`sBattleTouchRotation()` (`0x15b688`, 2.224 B) — descida recursiva
via `jtable.py`: **526 de ~556 instruções possíveis (95%)**, sem
tabela de salto; **60 branches, 42 de retrocesso**. 25 `bl`
distintos.

Confirma exatamente a hipótese: lê estado de toque bruto
(`iOS_getTouchTap`/`Press`/`Release`/`Swype`/`BeginX`/`BeginY`/
`NowX`/`NowY`), valida contra os limites da área de jogo
(`IS_GAME_AREA`), e dirige um subsistema de rotação dedicado
(`iOSRotStop`, `iOSRotSpeed`, `iOSRotSpeedGet` ×3, `iOSRotBufSetX`/
`Y`, `iOSRotSetupAfterX`/`Y`) usando helpers de ponto flutuante do
compilador pra matemática de velocidade/ângulo — **confirma a
matemática trigonométrica teorizada na seção 85**. Também chama
`startTurnRelative(int)` (ajuste de orientação por turno/câmera) e
manipula estado de ícone V2 e um timer de status — sugere feedback de
UI (ícone de rotação) ligado ao gesto de arrastar. Alta densidade de
laço (42 de 60) consistente com cálculo por quadro de delta-de-toque
pra velocidade de rotação. Marcada `read_structural`.

## 144. `disp_chapter()` — driver de task do cartão de título de capítulo, coordena com flags de batalha PSP (2026-10-18, Fase 3, lote paralelo)

`disp_chapter()` (`0xd361c`, 2.184 B) — descida recursiva via
`jtable.py`: **524 de ~546 instruções possíveis (96%)**, sem tabela
de salto; **50 branches, 31 de retrocesso**. 20 `bl` distintos.

Driver de task real do cartão de título de capítulo: despachado via
`asmTaskEntry`/`asm_function` (os alvos mais chamados, ×20/×6),
sondando input via `asmGetInput1` e lendo taxa de quadro via
`iOS_GetFrameRate` — consistente com uma task que roda por vários
quadros pra animar/exibir o cartão. Desenha com chamadas gráficas de
baixo nível estilo PSX (`DrawSync`, `FntPrint`, `PSX_LoadImage`) e
gerencia gráfico de overlay de ícone V2 (`iOS_getV2Icon`/
`setV2Icon`) — sugere que o cartão de capítulo inclui um elemento de
ícone/retrato. Também toca flags de dado de batalha PSP
(`pspBattleDataBackBufGet`/`DisableFlg`/`EnableFlg`) e
`CFFT_STATE::GetParam`, implicando que a transição de capítulo
coordena com/trava o estado do subsistema de batalha, e faz trabalho
de heap via `mallocAddress`/`freeForFile`/`xpMallocIO`. Dois locais
sem símbolo, chamados pesadamente (×6/×3) — bons candidatos pra
próxima leitura. Marcada `read_structural`.


## 145. `floor1_encode` — mais um interno de `libvorbis` reconhecido por nome (2026-10-18, Fase 3, regra 6 da metodologia)

`floor1_encode` (`0x8b594`, 1.860 B) — checagem rápida via
`jtable.py`: **99% de cobertura**, uma tabela de salto de 4 casos,
catálogo de `bl` é só `oggpack_write`, `vorbis_book_encode`,
`ov_ilog` — API genuína de codificação de piso espectral da
`libvorbis` (par de `floor1_fit`, seção 102). Marcada `read_full`
sem passe completo, regra 6 da metodologia.


## Décimo-quarto lote paralelo (seções 146–151): 6 funções lidas por forks simultâneos, usando `jtable.py`

## 146. `WorldJobStts()` — popup de status de emprego no mapa-mundo, biblioteca `iOS_CMenuTouch` completa (2026-10-18, Fase 3, lote paralelo)

`WorldJobStts()` (`0x1b5ba0`, 2.180 B) — descida recursiva via
`jtable.py`: **494 de ~545 instruções possíveis (91%)**, sem tabela
de salto; **38 branches, 20 de retrocesso**. 32 `bl` distintos.

Combina busca de dado de emprego/habilidade (`GetAbilityList`,
`LearnJobStts()`) com a máquina de UI de janela completa
(`WindowPositionInit*`, `WindowInit`/`Init2`, `DrawWindow2`,
`SetWindowCount`), o subsistema de menu de toque
(`iOS_CMenuTouch::init`/`exec`/`setMaxNumY`/`setDispNumY`/
`setDispOffset`/`setYLine`/`setDisableHeightAdjust`/
`drawMenuAssist`/`setLRCurEffect`), seleção de cursor por lado
(família `MenuSelSide`), limpeza de pad (`ClearPadData`), e desenho
de textura (`DrawFT4RGB`, `MakeTextureMessage`, `LoadImage_menuData`,
`iOS_setV2Icon`). Consistente com um popup de status de emprego no
mapa-mundo que renderiza um painel de lista de emprego/habilidade
rolável e dirigido por toque, sobreposto à visão de mapa. Marcada
`read_structural`.

## 147. `GLIVON_FT4_old(...)` — pipeline de iluminação/cor-de-vértice GTE, dominada por `iOS_PalleteHosei` (2026-10-18, Fase 3, lote paralelo)

`GLIVON_FT4_old(unsigned long*, tagPOLY_GT4*, short, int, unsigned
short*)` (`0x2826c8`, 2.176 B) — descida recursiva via `jtable.py`:
**536 de ~544 instruções possíveis (99%)**, sem tabela de salto;
**26 branches, 14 de retrocesso**. 16 `bl` distintos.

Toca a pipeline de iluminação/cor de vértice estilo GTE
(`ReadLightMatrix`, `ReadColorMatrix`, `ReadRotMatrix`, `MulMatrix`,
`GteGetCtrlReg` ×3), correção de cor/paleta de vetor
(`VectorDataBase`, `ColorVectorDataBase`, `CalcVectorFromID`, e
**`iOS_PalleteHosei`** ×12 — alvo dominante, consistente com um laço
de correção de cor por vértice/canal), mapeamento/clipping de FT4
(`iOSGT4_MapXYZ`/`MapXYZClear`/`MapT9`, `iOS_chkclipoffNoFT4`) e
hooks diversos do motor (`iOS_EventNumberGet`, `iOS_BattleEventCheck`,
`iOS_getV2Icon`). **Nota de layout**: `iOS_PalleteHosei`
(`0x2826b4`) fica apenas 0x14 B antes do início desta função —
adjacência direta na imagem, não necessariamente relação funcional.
Nenhum símbolo "GLIVON_FT4" sem `_old` aparece no catálogo — não foi
possível confirmar/descartar uma variante irmã a partir só deste
dado. Marcada `read_structural`.

## 148. `check_coord2(...)` — varredura de ocupação de chocobo numa coordenada (2026-10-18, Fase 3, lote paralelo)

`check_coord2(int, int, int, unsigned char)` (`0x1e2308`, 2.152 B) —
descida recursiva via `jtable.py`: **533 de ~538 instruções
possíveis (99%)**, sem tabela de salto; **169 branches, 106 de
retrocesso** — proporção altíssima de retrocesso (~63%), densidade
de laço extrema.

**Único `bl` distinto**: `check_chokobo(BWORK*)`, chamado **8 vezes**
— a função não toca praticamente nada fora de si mesma. Consistente
com percorrer um conjunto de unidades (`BWORK*`) testando cada uma
contra a coordenada/flag dada — uma rotina de grade de batalha
varrendo unidades (especificamente chocobos/montados) ocupando ou
bloqueando um tile de mapa dado, delegando o trabalho pesado de
teste por unidade a `check_chokobo`. Marcada `read_structural`.

## 149. `iOSJobChangeRot(...)` — confirma ser o handler de rotação por arrastar-toque do seletor de emprego giratório (2026-10-18, Fase 3, lote paralelo)

`iOSJobChangeRot(short*, short*)` (`0x15f3b0`, 2.044 B) — descida
recursiva via `jtable.py`: **482 de ~511 instruções possíveis
(94%)**, sem tabela de salto; **50 branches, 29 de retrocesso**. 14
`bl` distintos.

Confirma a hipótese: sonda estado de toque bruto (`iOS_getTouchTap`/
`Press`/`Release`/`BeginX`/`Y`/`NowX`/`Y`), valida com
`IS_GAME_AREA`, e dirige a MESMA máquina de rotação `iOSRot*`
(`iOSRotStop`, `iOSRotSpeed`, `iOSRotBufSetX`, `iOSRotSpeedGet`,
`iOSRotSetupAfterX`) já vista em `sBattleTouchRotation` (seção
143). É a ponte de input-por-quadro-para-rotação do MESMO seletor de
emprego giratório documentado em `JobChange` — confirma que o
mecanismo de rotação `iOSRot*` é compartilhado entre pelo menos duas
UIs diferentes (câmera de batalha e roda de emprego). Marcada
`read_structural`.

## 150. `ForAutoCommand()` — núcleo de decisão de IA/auto-batalha, três tabelas de salto, revela `DattoNoGotokuNigeyoRoutine` (2026-10-18, Fase 3, lote paralelo)

`ForAutoCommand()` (`0x272aac`, 2.044 B) — descida recursiva via
`jtable.py`: **476 de ~511 instruções possíveis (93%)**; **três
tabelas de salto resolvidas** (6 casos/5 handlers; 8 casos/7
handlers; 4 casos/4 handlers); **84 branches, 35 de retrocesso**. 17
`bl` distintos.

Núcleo real de decisão de IA/auto-batalha: chama
`EvaluateAllUnitAction`, `GetNearestUnit`, `SetBaseTargetGroup` (×6),
`SetDestUnit` (×3), `SetMove` (×4), `SetTmp_UA(UnitAction*)`,
`ForChantedAction`, `MakeMapChantedAction`, `IsAlmostNullUnit`,
`SetThresholdDoNothing`, `StayAtSafePanel`, e
**`MainBattleRoutine()`**/**`FundamentalRoutine()`**. **Achado
curioso**: **`DattoNoGotokuNigeyoRoutine()`** — nome literal em
japonês romanizado, "fuja como um papagaio (de papel) cortado"
(expressão idiomática pra fuga desesperada/em pânico) — é a rotina
de comportamento de fuga/retirada da IA. Junto, confirma que esta é
a lógica de seleção de alvo/movimento/habilidade por unidade,
comportamento de fuga, e o driver de estado de batalha mais amplo —
consistente com ser a lógica de IA por unidade invocada quando
auto-batalha está ativa. Marcada `read_structural`.

## 151. `getskillresult_main(...)` — casca de orquestração de alvo, identifica `calc_result` como a fórmula real de dano (próxima prioridade) (2026-10-18, Fase 3, lote paralelo)

`getskillresult_main(int, SKILL_RESULT*)` (`0x1e5bac`, 1.980 B) —
descida recursiva via `jtable.py`: **480 de ~495 instruções
possíveis (97%)**, sem tabela de salto; **60 branches, 27 de
retrocesso**. 13 `bl` distintos.

**Achado importante**: confirma ser a casca de orquestração por alvo
da resolução de habilidade, NÃO a fórmula de dano bruto em si — chama
`calc_result(ACT*, unsigned char)` **uma única vez** (a matemática
real de acerto/dano/efeito mora lá, não aqui). Em volta dessa
chamada, faz bookkeeping pesado por alvo: `init_target_result` (×2,
limpa/inicializa o struct `A_RESULT` por alvo), `check_coord`/
`get_coord_address` (alvejamento posicional/de área, resolução de
coordenada de tile), `check_invincible` (gate de invencibilidade/
tile sem dano), `set_ct_weapon` (seleciona contexto de arma pro
ataque), `set_target_table2`/`copy_target_table2` (monta e tira
snapshot da lista de alvos afetados, consistente com habilidade de
área acertando várias unidades), e **`reset_toumei_afterskill`**
("toumei" = transparência/invisibilidade — limpa flag de status
furtivo/invisível após a habilidade resolver, ou seja, usar a
habilidade quebra furtividade). `pspNetSetTimingThroughFlag` parece
boilerplate residual da camada de rede PSP, não relevante pro
combate. 27 branches de retrocesso consistentes com laço sobre lista
multi-alvo (habilidades de área) e/ou slots de efeito de status.
**Correção (mesma sessão)**: o fork que gerou esta seção marcou
`calc_result` como "ainda não lida" por não ter acesso ao inventário
— na verdade `calc_result` (`0x1cba40`) já foi lida na seção 90, e
já se sabe que ELA TAMBÉM é um dispatcher (duas tabelas de salto,
11+25 casos) por tipo de ação/arma, não a fórmula de dano linear em
si — a seção 90 já deixou isso como pendência honesta ("a fórmula de
dano em si... não encontrada como chamada separada, pode estar
inline"). Juntando as duas seções: a cadeia de resolução de
habilidade é `getskillresult_main` → `calc_result` (dispatch por
tipo) → handler específico (ainda não aberto, um dos 8+18 casos das
tabelas da seção 90) → `setskillresult` (seção 77, aplica
consequência). A fórmula de dano real provavelmente mora dentro de
um desses handlers de `calc_result`, não numa função própria
separada — abrir os handlers é a prioridade mais alta pra matemática
de combate, não ler uma função nova. Três locais sem símbolo em
`getskillresult_main` (`sub_715cc`, `sub_1e0f2c`, `sub_1e59d4`) —
candidatos a RNG ou lookup de estatística, vale leitura futura.
Marcada `read_structural`.


## 152. `Aitemmenu_call`/`Ditemmenu_call`/`Eitemmenu_call`/`Citemmenu_call` — quatro stubs de 4 B, literalmente só `bx lr` (2026-10-18, Fase 3, regra 3 da metodologia)

As quatro variantes de letra de `itemmenu_call` (`0xc4494`/`0xd1408`/
`0x123c40`/`0x14bec4`, 4 B cada) são, confirmado por disassembly
direto, **uma única instrução `bx lr`** — retorno imediato, nenhuma
chamada, nenhum branch. Mais extremo que os trampolins de 16 B da
seção 131 (`disp_equipwindow`) — aqui não há nem uma chamada a
`asmTaskEntry`, é um no-op puro. Aceitas direto, regra 3 da
metodologia. Marcadas `read_full`.

## 153. `eDB_init(...)` — segunda confirmação de boilerplate PSYQ `DB_Init` (2026-10-18, Fase 3, regra 6 da metodologia)

`eDB_init(DB*, ...)` (`0x187920`, 1.784 B) — mesma assinatura de 26
ponteiros de primitivo da seção 113 (`bDB_init`). Checagem via
`jtable.py`: **94% de cobertura**, zero tabela de salto, **9
branches, só 2 de retrocesso** — catálogo de `bl` é só
`Set<TipoPrimitivo>` (`SetPolyF4`/`SetPolyFT4`/`SetLineF2`/
`SetTile`/`SetDrawMove`/`SetShadeTex`) mais `eSwapDB(int,int)`.
Segunda confirmação do mesmo padrão `DB_Init`/`InitGeom` genuíno do
PSYQ — a letra de prefixo (`b`/`e`) é só o nome da variável de
double-buffer, não lógica diferente. Marcada `read_full`.

## 154. `GLIVON_FT3_old` — mesma pipeline de `GLIVON_FT4_old`, sem os mapeamentos de textura específicos de quad (2026-10-18, Fase 3, regra 2 da metodologia)

`family_sim.py` contra `GLIVON_FT4_old` (seção 147): `GLIVON_FT3_old`
(`0x282f48`, 1.776 B) tem Jaccard 0,71 — reusa quase todo o catálogo
(`iOS_PalleteHosei`, `VectorDataBase`/`ColorVectorDataBase`/
`CalcVectorFromID`, pipeline de matriz GTE), mas **não chama**
`iOSGT4_MapXYZ`/`MapXYZClear`/`MapT9` (mapeamento de textura
específico de quad de 4 vértices, seção 147) — consistente com `FT3`
sendo o primitivo triangular (3 vértices), que não precisa do
mapeamento UV de 4 pontos que `FT4` precisa. Confirma que
`GLIVON_FT3_old`/`GLIVON_FT4_old` são a mesma pipeline de iluminação/
cor, parametrizada pelo tipo de primitivo (triângulo vs. quad), não
duas implementações separadas. Marcada `read_structural`.

## 155. `Wdrawmessagepolygons`/`Wevent_call` — nona/décima confirmação do padrão `W`, com uma nuance de escopo reduzido (2026-10-18, Fase 3, regra 2 da metodologia)

```
Wdrawmessagepolygons  0x10e154  1.988 B   Jaccard 0,48 (vs drawmessagepolygons, §137)
Wevent_call           0x10e918  2.040 B   Jaccard 0,10 (vs event_call, §66)
```
**`Wdrawmessagepolygons`**: Jaccard baixo, nona confirmação do
padrão — chama `Waddlocalprim` (`0xfe1a4`) em vez da versão sem
prefixo.

**`Wevent_call` — nuance nova**: Jaccard baixíssimo (0,10) E, mais
importante, é **MUITO menor** que `event_call` (2.040 B vs 5.456 B,
seção 66 — o dispatcher central de cutscene com 70 `bl` distintos).
`Wevent_call` chama `wasmTaskEntry`/`wasmGetActiveTask` (padrão `W`
usual) e, achado interessante, **chama `Wdrawmessagepolygons`
diretamente** (`0x10e154`) — confirma que os dois `W`s desta seção
se encadeiam. Mas, diferente de toda outra família `W` vista até
agora (que são cópias de tamanho comparável à base), `Wevent_call`
parece implementar só um SUBCONJUNTO dos opcodes de evento que
`event_call` cobre — não é uma recompilação 1:1 completa, é uma
variante reduzida de escopo. Marcadas `read_structural`.


## Décimo-quinto lote paralelo (seções 156–160): 5 funções lidas por forks simultâneos, usando `jtable.py`

## 156. `menu_call(...)` — entrada de task concreta que chama `event_call` direto, não um primitivo genérico (2026-10-18, Fase 3, lote paralelo)

`menu_call(unsigned long*, unsigned long)` (`0xf5898`, 1.984 B) —
descida recursiva via `jtable.py`: **457 de ~496 instruções
possíveis (92%)**, sem tabela de salto; **44 branches, 20 de
retrocesso**. 9 `bl` distintos.

Toca estado de task (`asmGetActiveTask`), dado de mapa/geometria
(`get_mapid`, `getMapXYZ`), submissão de primitivo pra desenho
(`addlocalprim`), um toggle de efeito de chama (`changeflame`),
chamadas de emulação de GPU PSX (`iOS_GetFrameRate`,
`iOS_setHalftoneSize`), e, achado chave, **chama `event_call`
diretamente** (`0xf431c`, seção 66 — o dispatcher central de
cutscene). Alta densidade de branch de retrocesso sem tabela de
salto sugere, como `itemmenu_call`/`Witemmenu_call` (seções 129/130),
que `menu_call` é uma função de entrada de task CONCRETA que faz seu
próprio trabalho de desenho de mapa/polígono por quadro — não é um
primitivo genérico compartilhado que outras `*_call` constroem por
cima; na verdade ela mesma invoca/encadeia pro sistema de evento.
Marcada `read_structural`.

## 157. `Settings_Init()` — setup de layout e asset do toolkit `CEGL2_*`, adaptado por dispositivo (2026-10-18, Fase 3, lote paralelo)

`Settings_Init()` (`0x2c562c`, 1.968 B) — descida recursiva via
`jtable.py`: **472 de ~492 instruções possíveis (96%)**, sem tabela
de salto; **17 branches, 6 de retrocesso**. 24 `bl` distintos.

Setup de uma vez só da tela de Configurações: registra/configura
retângulos de UI `CRECT` (`Register`, `SetScreenOffset`/`Scale`,
`MulRect` ×12 — provavelmente escala por widget, `SetEnableAll`),
inicializa correção de tela via `CGX_SCREEN_CORRECT` (correção de
aspecto/área segura por dispositivo), carrega um recurso de sprite
via `CEGL2_SPRITE::LoadBegin`/`LoadEnd`, e carrega/decodifica um
arquivo de dado via `CFILE_DAT::Load`/`Decode` (descarregando um
anterior primeiro via `Unload`). Também consulta características do
dispositivo via `CAPP_INFO` (`GetDeviceType`, `GetDeviceScale`,
`IsDeviceiPhoneRetina4inch`) pra adaptar layout/escala por
dispositivo, e toca `CWORK_MEM::Get()`/`CSTEP_BATCH::Init`/`Uninit`
(memória de rascunho e um recurso de animação/step-batch ligado à
UI). Três locais sem símbolo. Confirma ser trabalho clássico de
init de tela do toolkit `CEGL2_*` já visto (seções 133–135): setup
de retângulo de layout, carga de asset de sprite/dado, escala
adaptativa por dispositivo. Marcada `read_structural`.

## 158. `createPermanentObject(...)` — construtor físico/de transformação real pros objetos de efeito permanente (2026-10-18, Fase 3, lote paralelo)

`createPermanentObject(_JochuParameter*, Physics*)` (`0x2284ac`,
1.944 B) — descida recursiva via `jtable.py`: **486 de ~486
instruções possíveis (100%)**, sem tabela de salto; **22 branches, 9
de retrocesso**. 15 `bl` distintos, 37 chamadas no total.

Fortemente dirigida por matemática GTE (`RotMatrix`/`SetRotMatrix`/
`SetTransMatrix`/`RotTrans`/`VectorNormal`/`ratan2`/`SquareRoot0`) —
consistente com o parâmetro `Physics*` precisando de setup real de
orientação/transformação pro objeto recém-spawnado. **`efrand`**
(×7, a chamada mais frequente) e `ps_rand` (×3) indicam
randomização pesada de parâmetro inicial (jitter de velocidade/
direção/posição típico de spawn de partícula/efeito).
`getAnimationDirection`/`GetAnimationPosition` ligam de volta ao
sistema de animação/efeito já visto nas funções de ciclo de vida do
`ASHURA`. **Confirma que `createPermanentObject` é o construtor real
de física/transformação pros objetos de efeito permanente** —
combina randomização via RNG com setup completo de orientação 3D
(matriz de rotação + translação) antes do objeto entrar na pipeline
de animação/efeito. Dois locais sem símbolo. Marcada
`read_structural`.

## 159. `GetDestinationsAndMakeMaskTG()` — constrói a grade de máscara de movimento/alvo iterando painéis (2026-10-18, Fase 3, lote paralelo)

`GetDestinationsAndMakeMaskTG()` (`0x278480`, 1.932 B) — descida
recursiva via `jtable.py`: **476 de ~483 instruções possíveis
(99%)**, sem tabela de salto; **55 branches, 34 de retrocesso** —
função densamente orientada a laço.

Rotina de grade de batalha/alcance de movimento: consulta status de
unidade (`check_status_data2`), avalia/agrega uma área-base de alvo
(`GetTargetBaseArea`), busca qual painel/tile está sob uma unidade
dada (`GetPanelUnderUnit`), contabiliza células de mapa (`CountMap`,
operando sobre uma grade `short` fixa de largura 18 — provavelmente
o stride de largura do mapa), e copia um buffer de word (`MemCpyW`)
— consistente com montar uma grade "máscara" de movimento/alvo
iterando painéis candidatos, checando status de unidade por tile, e
copiando/contando resultados num array de máscara de saída. Liga
diretamente ao subsistema de pathfinding/alvejamento de IA junto com
`GetTargetBaseArea` e os helpers de busca de painel já vistos perto
de `ForAutoCommand` (seção 150). Marcada `read_structural`.

## 160. `CheckUnitActionEffective(...)` — avaliador de efetividade de IA baseado em status/tempo, com RNG, alimenta `ForAutoCommand` (2026-10-18, Fase 3, lote paralelo)

`CheckUnitActionEffective(int, int)` (`0x276e4c`, 1.828 B) —
descida recursiva via `jtable.py`: **447 de ~457 instruções
possíveis (98%)**; **uma tabela de salto resolvida** (guarda `cmp`
em `0x277180`, dispatch em `0x277184`, 4 casos, 4 handlers
distintos); **122 branches, 64 de retrocesso** — densidade de laço
muito alta pra um tamanho pequeno.

Dominada por `JudgeStatus(int,BWORK*,int)` (×7) — checa uma ou mais
condições de efeito de status (buff/debuff/aflição) contra a
unidade, com a tabela de 4 vias provavelmente selecionando entre
categorias de checagem de status ou tipo de efeito.
`GetCountToNextTurn`/`GetCountToDeath` sugerem que também fatora
estado de tempo de turno/contagem até morte (ex.: "isso mataria
antes do próximo turno"), e `ps_rand()` indica uma checagem
probabilística/influenciada por RNG (chance de proc ou pontuação de
IA randomizada), não um cálculo puramente determinístico. Nenhuma
fórmula de dano ou checagem de resistência elemental aparece
diretamente aqui — a "efetividade" julgada parece ser
primariamente baseada em status/condição e tempo, não em dano bruto.
**Perfil consistente com um helper de avaliação de IA que alimenta a
decisão de `ForAutoCommand`** (seção 150): responde "aplicar esse
status/ação ainda importa dado o status/tempo de turno atual do
alvo" — usado pra filtrar/pontuar ações candidatas. Marcada
`read_structural`.


## 161. `Wmenu_call(...)` — espelha `menu_call`→`event_call` como `Wmenu_call`→`Wevent_call` (2026-10-18, Fase 3, regra 2 da metodologia)

`family_sim.py` contra `menu_call` (seção 156): `Wmenu_call`
(`0x10f124`, 1.960 B) tem Jaccard 0,31 — chama `Waddlocalprim`
(`0xfe1a4`) em vez de `addlocalprim`, `wasmGetActiveTask`
(`0x162028`) em vez de `asmGetActiveTask`, e, espelhando o achado da
seção 156, **chama `Wevent_call` diretamente** (`0x10e918`, seção
155) em vez de `event_call` — confirma que a dupla `menu_call`/
`event_call` tem uma dupla `W` paralela e completa (`Wmenu_call`/
`Wevent_call`), encadeadas entre si da mesma forma. Décima-primeira
confirmação do padrão `W`. Marcada `read_structural`.


## Décimo-sexto lote paralelo (seções 162–167): 6 funções lidas por forks simultâneos, usando `jtable.py`

## 162. `Settings_FrameMove()` — confirma o par update/draw da tela principal de Configurações (2026-10-18, Fase 3, lote paralelo)

`Settings_FrameMove()` (`0x2c5ddc`, 1.908 B, DISTINTA de
`SettingsWnd_FrameMove`, seção 135 — nomes parecidos, funções
diferentes) — descida recursiva via `jtable.py`: **447 de ~477
instruções possíveis (94%)**; **uma tabela de salto resolvida** (9
casos, 6 handlers distintos); **43 branches, 28 de retrocesso**. 25
`bl` distintos.

Confirma ser a contraparte "update" de `Settings_FrameRender`
(seção 133): sondagem de toque completa (`CINPUT_IF_TOUCH::Begin`/
`EndAll`, `GetPress`/`Down`/`Up`/`Repeat`/`TouchPoint` ×7/
`TouchCount`/`GetEvent`), atualização de widget (`CRECT::FrameMove`/
`SetEnable`, `CSTEP_BATCH::FrameMove`/`Init`), escala de tela
(`CGX_SCREEN_CORRECT::Scaled`/`CorrectX`, `RETINA_SCALE`),
**`SettingsBundle_Get()`** (×12, o alvo mais chamado), áudio
(`SysSE_PlayDef`, `CSOUND_IF::SetMasterVolume`), e
**`onGotoNextMode(int)`** (transição de modo/tela). A tabela de 9
casos mais o tráfego pesado de `SettingsBundle_Get` sugere um laço
de dispatch por item de configuração tratando evento de toque pra
cada controle (slider/botão). Marcada `read_structural`.

## 163. `SettingsWnd_Init()` — mesmo toolkit de `Settings_Init`, escopo próprio pra variante janela (2026-10-18, Fase 3, lote paralelo)

`SettingsWnd_Init()` (`0x2c718c`, 1.864 B) — descida recursiva via
`jtable.py`: **451 de ~466 instruções possíveis (97%)**, sem tabela
de salto; **13 branches, 4 de retrocesso**. 21 `bl` distintos.

Mesmo toolkit de `Settings_Init` (seção 157): `CRECT::Register`/
`Init`/`MulRect` (×11)/`SetEnableAll`, `CEGL2_SPRITE::LoadBegin`/
`LoadEnd`, `CFILE_DAT::Load`/`Unload`/`Decode`, `CAPP_INFO::
GetDeviceType`/`GetDeviceScale` — confirma ser a contraparte de init
de uma vez só da variante "janela" da tela de Configurações, com
escopo próprio: chama `CGX_SCREEN_CORRECT::Area_GetCorrect` e
`GX_GetScreenW_1X()` (não vistos em `Settings_Init`), sugerindo
lógica extra de correção de tela/largura específica da variante
`Wnd`. Três locais sem símbolo. Marcada `read_structural`.

## 164. `Edisp_equipwindow()` — conteúdo real da tela de equipar, confirma pra onde os stubs triviais da seção 131 desembocam (2026-10-18, Fase 3, lote paralelo)

`Edisp_equipwindow()` (`0x12171c`, 2.156 B) — descida recursiva via
`jtable.py`: **516 de ~539 instruções possíveis (96%)**, sem tabela
de salto; **35 branches, 20 de retrocesso**. 27 `bl` distintos.

Confirma ser conteúdo real de tela, não um stub: `addlocalprim`
(×17, dominante — laço pesado de desenho por item/slot),
`initsprtfield`/`itemuvclut`/`bgput`/`SetDrawOffset`/`IS_TEX_2X`/
`TexHybrid_RegistCLUTAddr`/`PSX_LoadImage` (textura/CLUT e fundo),
`addstatusback`/`initstatusback`/`statuskanjiprint` (moldura da
janela e texto em japonês), `import_localpad`/`settaskkind`/
`asmGetInput3`/`asmTaskEntry` (input/task), `pspItemIsEmpty`/
`CFFT_STATE::GetParam`/`SetParam` (estado/checagem de item), e
**`iOSUnitListMoveFlagReset()`** (flag de navegação de lista).
**Confirma a hipótese**: `Edisp_equipwindow` é a implementação real
em que os stubs triviais `disp_equipwindow`/`A`/`D`/`C` (16 B/4 B,
seção 131) desembocam via `asmTaskEntry` — constrói e desenha a
janela de equipar de verdade (sprites, fundo, texto de status,
checagem de slot de item). Cinco locais sem símbolo. Marcada
`read_structural`.

## 165. `Wdisp_equipwindow()` — décima-segunda confirmação do padrão `W` (2026-10-18, Fase 3, lote paralelo)

`Wdisp_equipwindow()` (`0x132cfc`, 2.148 B) — descida recursiva via
`jtable.py`: **513 de ~537 instruções possíveis (96%)**, sem tabela
de salto; **35 branches, 20 de retrocesso**. 27 `bl` distintos.

Confirma o padrão pela décima-segunda vez: chama `wasmTaskEntry()`/
`wasmGetInput3()` mais a biblioteca `W`-prefixada completa
(`Waddlocalprim` ×17, `Winitsprtfield`, `Waddstatusback`,
`Winitstatusback`, `Witemuvclut`, `Wsettaskkind`,
`Wimport_localpad`, `Wloadcdst`, `Wbgput` ×5, `Wstatuskanjiprint`)
— cópia real recompilada, catálogo quase idêntico ao de
`Edisp_equipwindow` (seção 164) só com prefixo `W` em tudo. Cinco
locais próprios sem símbolo. Marcada `read_structural`.

## 166. `ctltuto_main(CTLINFO*)` — hub do subsistema de tutorial EM MENU, separado do overlay `Tutrial()` de campo (2026-10-18, Fase 3, lote paralelo)

`ctltuto_main(CTLINFO*)` (`0x26e428`, 1.992 B) — descida recursiva
via `jtable.py`: **479 de ~498 instruções possíveis (96%)**; **uma
tabela de salto resolvida** (4 casos, 4 handlers distintos); **41
branches, 23 de retrocesso**. 38 `bl` distintos.

Confirma membro do framework `ctl*_main`: usa `Wtask_status`/
`Wsend_taskparamater`, tem sua própria tabela de fase de 4 casos, e
é um HUB que transiciona pra vários sub-controladores nomeados
(`ctltips_init`, `ctlopt_init`, `ctlhelp_init`, `ctlhentuto_init`,
`ctlsentuto_init`, `ctltuto_deactive`, `wldctl_deactive`) — mesmo
formato de `ctlbrst_main` (seção 125). Dirige pesadamente
`iOS_CMenuTouch` e ícones `iOS_setV2Icon` (×8)/`getV2Icon`, som/
música/SSD, e funções de estado `iOSTuto*`
(`iOSTutoReset`/`iOSTutoFlagSet`/`iOSTutoBtlInputSet`). **Confirma
ser um subsistema de tutorial SEPARADO** do overlay de campo
`Tutrial()` (seção 115) — acessado pelo seu próprio hub, não pelos 8
alvos nomeados de `ctlbrst_main` (nenhum dos quais era
`ctltuto_init`). Marcada `read_structural`.

## 167. `ctlmouketeam_main(CTLINFO*)` — corrige a hipótese de nome: é a lista de unidades recrutáveis/disponíveis, não "lucro/ganho" (2026-10-18, Fase 3, lote paralelo)

`ctlmouketeam_main(CTLINFO*)` (`0x2632ec`, 1.984 B) — descida
recursiva via `jtable.py`: **477 de ~496 instruções possíveis
(96%)**, sem tabela de salto; **35 branches, 16 de retrocesso**. 26
`bl` distintos.

**Corrige a hipótese inicial** (nome "mouke" sugeria "lucro/ganho"):
o catálogo mostra ser uma tela de lista/seleção de unidade — chama
sub-controladores irmãos (`ctlmouke_init`, `ctlmoumes_init`/
`deactive`, `ctlhaken_init` — "haken" = despacho/alocação de
unidade), mais helpers locais `mouketeam_scrollset`/
`mouketeam_unitwin`/`mouketeam_unitface`, e dirige pesadamente
renderização de ícone/retrato por unidade (**`iOS_setV2Icon`** ×14,
a chamada mais frequente), setup de retângulo de toque
(`iOS_SetRectHit`/`ClearRectHitAll`/`GetRectHitNoTap`), rolagem de
menu (`rewrite_worldscroll`) e som (`sound_request` ×4). **Conclusão
mais plausível**: "mouketeam" é uma tela de lista/seleção de
unidades recrutadas/disponíveis pra montar o time ("team" = elenco/
roster), com retrato por unidade — não uma tela de "lucro". Sem
tabela de salto, dispatch de fase por branch direto. Um local sem
símbolo. Marcada `read_structural`.


## Décimo-sétimo lote paralelo (seções 168–173): 6 funções lidas por forks simultâneos, usando `jtable.py`

## 168. `ctlbackpage_main(CTLINFO*)` — handler de navegação "voltar", sem tabela de salto, com helper `backpage_put` dedicado (2026-10-18, Fase 3, lote paralelo)

`ctlbackpage_main(CTLINFO*)` (`0x2657f8`, 1.932 B) — descida
recursiva via `jtable.py`: **466 de ~483 instruções possíveis
(96%)**, **sem tabela de salto** (diferente da maioria dos irmãos
`ctl*_main` — não usa o padrão de dispatch por tabela de fase); **42
branches, 20 de retrocesso**. 23 `bl` distintos.

Dominada por sondagem de toque direta (`iOS_getTouchTap`/`Press`/
`BeginX`/`BeginY`/`NowY`, 15 chamadas no total) e comparação de
ponto flutuante (`__floatsisf`/`__aeabi_fcmple`, provavelmente
rastreando uma posição de animação de scroll/transição), mais um
helper dedicado **`backpage_put(CTLINFO*, int)`** (`0x2657d8`, só 32
B antes do início desta função — vizinho direto na imagem) que
parece escrever/inicializar o estado de "página de volta" que esta
função gerencia. Junto com `wldkey_rep`/`iOSwldkey_repSet` (estado
de teclado virtual) e `Wwrite_eventflag`/`Wtask_start`, consistente
com um handler de navegação "voltar pra tela anterior": sonda toque/
swipe, atualiza um valor de scroll/transição, escreve uma flag de
evento e inicia uma task de seguimento (provavelmente a transição de
tela real). Marcada `read_structural`.

## 169. `hakenunit_status_main(CTLINFO*)` — tela de detalhe de status de unidade despachada, tabela de 5 casos (2026-10-18, Fase 3, lote paralelo)

`hakenunit_status_main(CTLINFO*)` (`0x262b18`, 1.692 B) — descida
recursiva via `jtable.py`: **400 de ~423 instruções possíveis
(95%)**; **uma tabela de salto resolvida** (5 casos, 5 handlers
distintos); **33 branches, 19 de retrocesso**.

Dirige o padrão de task padrão (`Wtask_create`/`Wtask_status`/
`Wsend_taskparamater`) com a tabela de 5 casos pros estados internos
da task, chama **`hakenunit_status(int)`** uma vez (o acessor de
dado real de status de despacho de uma unidade), toca input de
retângulo de toque (`iOS_SetRectHit`/`ClearRectHitAll`/
`GetRectHitNoTap`, `iOS_getTouchSwype`), ícone V2, cursor de
navegação L/R de lista de unidade (`iOSUnitListLRCurWrite`,
`iOSWldEffectLR`), e um overlay de ajuda (`ctlsthelp_init`).
**Confirma ser a sub-tela de detalhe/status interativa pra uma
unidade selecionada** na lista de `ctlmouketeam_main` (seção 167),
com sua própria navegação por cursor entre unidades. Marcada
`read_structural`.

## 170. `chokobo_chrmenu(int)` — driver de task do menu de personagem via chocobo, toca estado de rede PSP (2026-10-18, Fase 3, lote paralelo)

`chokobo_chrmenu(int)` (`0xd140c`, 1.700 B, já referenciada por
nome em `disp_statusc`, seção 107) — descida recursiva via
`jtable.py`: **387 de ~425 instruções possíveis (91%)**, sem tabela
de salto; **26 branches, 13 de retrocesso**. 17 `bl` distintos, 36
chamadas no total.

Máquina de estado baseada em task (`task_create` ×4,
`send_taskparamater` ×7, `asmTaskEntry`/`asmGetActiveF`/
`asmGetActiveTask`), lê/escreve status local via
`export_localstatus`, checa/seta um flag de tipo de task
(`checktaskkind`/`settaskkind`), e **`checkstatusscroll`** sugere
lista de status/estatística rolável (tela de stats de personagem,
como esperado). `import_localpad` lê input de controle direto.
`get_bwp` lê valor de estatística pra exibição. **Achado**:
`pspNetGetControlChar`/`pspNetGetBattleModeFlag` (estado de rede/
multiplayer) e `Set_NonDrawTaikiIconFlg` (toggle de ícone de
"taiki"/standby de personagem) — confirma ser o driver de estado/
task do menu de personagem via chocobo, ligando task, input,
exibição de status e a camada de rede PSP já vista em outras funções
de menu. Três locais sem símbolo, chamados pesadamente. Marcada
`read_structural`.

## 171. `select_valuewithmessage()` — widget de valor numérico com mensagem anexada, rodando como task cooperativa (2026-10-18, Fase 3, lote paralelo)

`select_valuewithmessage()` (`0x137b10`, 1.676 B) — descida
recursiva via `jtable.py`: **408 de ~419 instruções possíveis
(97%)**, sem tabela de salto; **17 branches, 6 de retrocesso**. 27
`bl` distintos.

Toca a biblioteca de widget `multiwindow_*` (`keydown`/`break`/
`loadcolor`/`packetcolor`/`packetanm`/`packetinit`/`keyright`) pra
moldura/key handling, a pipeline de primitivo/sprite estilo PSX
(`addlocalprim`, `initpolyft4`, `PSX_LoadImage`, `GetTPage`,
`SetSemiTrans`, `statuskanjiprint`, `statusfigprint0`) pra desenhar
janela e texto, helpers de string/valor (`serchmessagepointer`,
`getvaluelength`, `count_words`/`count_words2` — consistente com
parsear e medir o valor numérico e o texto de mensagem), input
(`import_localpad`), e controle de task (`task_wait`/
`task_killmyself`/`asmTaskEntry`/`asmGetActiveF`). Confirma a
hipótese: um widget de spinner/entrada de valor numérico com prompt
de mensagem anexado, desenhado via o sistema `multiwindow` e
rodando como sua própria task cooperativa. Um local sem símbolo.
Marcada `read_structural`.

## 172. `disp_selectwindow()` — janela de seleção multi-escolha genérica, touch-aware sobre a biblioteca `multiwindow_*` compartilhada (2026-10-18, Fase 3, lote paralelo)

`disp_selectwindow()` (`0xf07c0`, 1.752 B) — descida recursiva via
`jtable.py`: **432 de ~438 instruções possíveis (99%)**, sem tabela
de salto; **50 branches, 24 de retrocesso**. **45 `bl` distintos** —
catálogo grande pra 1.752 B.

Reusa a biblioteca `multiwindow_*` de desenho/animação já
catalogada (`keydown`/`keyright`/`keyloop`/`packetinit`/
`packetcolor`/`packetanm`/`packetadd`/`break`) e o boilerplate
genérico `checkkeyok`/`read_eventflag`/`asmTaskEntry`/`asmGetInput1`/
`2` compartilhado por toda a família de janela documentada, mas
ADICIONA uma camada de seleção dirigida por toque não vista nos
`disp_*window` mais simples: classe `iOS_CMenuTouch` completa
(`init`/`exec`/`setDispOffset`/`setYLine`/`setXIconRect`/
`setDispAssist`), manuseio de ícone `iOS_getV2Icon`/`setV2Icon`
(×4), overlay de halftone (`iOS_getHalftoneSize`/`Tap`), gate de
tutorial (`iOSTutoCheck`/`getTutorialbreak`/`Type`), persistência da
escolha via **`iOS_setSelectWindowRecord(short)`**, e som
(`iOS_soundDirect`). **Conclusão**: é o diálogo de seleção/
confirmação com reconhecimento de toque construído SOBRE a
biblioteca de desenho compartilhada, não uma reutilização pura —
distinto dos `disp_*window` mais simples (`personalwindow`/
`bothwindow`/`equipwindow`) que não têm essa camada de toque.
Marcada `read_structural`.

## 173. `GetBestEquip(short, short*)` — confirma a lógica de "melhor equipamento automático" por slot (2026-10-18, Fase 3, lote paralelo)

`GetBestEquip(short, short*)` (`0x1aa014`, 1.692 B) — descida
recursiva via `jtable.py`: **416 de ~423 instruções possíveis
(98%)**, sem tabela de salto; **55 branches, 26 de retrocesso** —
densidade de laço alta, consistente com escanear uma lista de
candidatos.

Confirma a hipótese: puxa o pool de item disponível via
`GetItemList`, ordena candidatos com `ItemSort` (×3), checa estado
de mão de arma via `Nitoryu` (dual-wield) e `Ryoute` (duas mãos)
pra decidir configurações de equipamento válidas, e classifica/
consulta cada candidato via `pspItemIsType` (×7)/`pspItemIsBarehand`/
`pspItemGetWeaponData` (×5, inspeção de estatística/tipo por
candidato), terminando com `ItemChg` (×1, aplica o equipamento
final escolhido). **Confirma**: itera inventário, filtra por regra
de mão/tipo de arma, compara estatística de arma, escolhe o melhor,
e comita via `ItemChg` — a lógica real de "auto-equipar melhor item
por slot". Marcada `read_structural`.


## 174. `vorbis_analysis_headerout` — mais um interno de `libvorbis` reconhecido por nome (2026-10-18, Fase 3, regra 6 da metodologia)

`vorbis_analysis_headerout` (`0x8cbf4`, 1.648 B) — checagem rápida
via `jtable.py`: **97% de cobertura**, zero tabela de salto,
catálogo de `bl` é só 4 locais sem símbolo na faixa `0x714xx`
(mesmo padrão de helper interno de `libvorbis` já visto em outras
funções desta biblioteca) — nenhuma chamada a função prefixada do
jogo. Confirma ser código de terceiros genérico. Marcada `read_full`
sem passe completo, regra 6 da metodologia.


## Décimo-oitavo lote paralelo (seções 175–180): 6 funções lidas por forks simultâneos, usando `jtable.py`

## 175. `MakeWindowFunc(unsigned char*)` — referência pra família de letra `b`/`c`/`e`/`j`, desenha moldura de janela em laço (2026-10-18, Fase 3, lote paralelo)

`MakeWindowFunc(unsigned char*)` (`0x1c37dc`, 1.884 B) — descida
recursiva via `jtable.py`: **457 de ~471 instruções possíveis
(97%)**, sem tabela de salto; **11 branches, 8 de retrocesso**.
Catálogo mínimo: `DrawFT4RGB` (×12, dominante — laço de desenho de
tile de moldura/borda) e **`MakeSmallWindowFunc(unsigned char*)`**
(×1 — delega um sub-painel/área de título a uma função irmã). Serve
de referência para comparar os 4 irmãos de letra `b`/`c`/`e`/`j`
(`bMakeWindowFunc`/`cMakeWindowFunc`/`eMakeWindowFunc`/
`jMakeWindowFunc`) numa checagem de similaridade futura. Marcada
`read_structural`.

## 176. `GetPad()` — referência pra família de letra, orquestrador de pad ciente de taxa de quadro (2026-10-18, Fase 3, lote paralelo)

`GetPad()` (`0x1b7f68`, 1.768 B) — descida recursiva via
`jtable.py`: **418 de ~442 instruções possíveis (95%)**, sem tabela
de salto; **41 branches, 19 de retrocesso**. 5 `bl` distintos.

Não é um leitor de input bruto — orquestra: `GetFrameRate()`
(escala/debounce de amostragem por taxa de quadro), `ClearPadData()`
(reset de estado), `TruePadRead(int)` (a leitura real "verdadeira"),
mais divisão inteira pesada (`__udivsi3` ×3, `__aeabi_uidivmod` ×4)
e 19 branches de retrocesso — sugere iteração sobre múltiplos slots
de botão/eixo com aritmética modular por entrada. Serve de
referência pra comparar `bGetPad`/`cGetPad`/`eGetPad`/`jGetPad` numa
checagem futura. Marcada `read_structural`.

## 177. `disp_parawindow()` — janela de comparação de parâmetro/estatística, reusa a biblioteca `stts` compartilhada (2026-10-18, Fase 3, lote paralelo)

`disp_parawindow()` (`0x12c190`, 1.632 B) — descida recursiva via
`jtable.py`: **393 de ~408 instruções possíveis (96%)**, sem tabela
de salto; **27 branches, 13 de retrocesso**. 21 `bl` distintos.

Confirma a hipótese "janela de comparação de parâmetro": reusa a
família de fundo de status `stts` (`addstatusback`/
`sttsback_normal`/`sttsback_blue`/`initstatusback`) e lê/renderiza
valor de campo via **`valueput(char*, VALUERECORD*, COPYFIELD*,
int)`** (×3) contra estruturas `COPYFIELD`/`VALUERECORD` — forte
suporte pra exibição de comparação antes/depois de stat (HP/MP/
parâmetro). Serve de referência pra comparar os 5 irmãos de letra
`A`/`C`/`D`/`E`/`W`. Marcada `read_structural`.

## 178. `DressMain()` — controlador de lista/roster de unidade, entrada de nível superior antes de `DressEquip` (2026-10-18, Fase 3, lote paralelo)

`DressMain()` (`0x19aec0`, 1.888 B, termina exatamente onde
`DressEquip` começa, seção 119) — descida recursiva via `jtable.py`:
**442 de ~472 instruções possíveis (94%)**, sem tabela de salto;
**61 branches, 30 de retrocesso**. 33 `bl` distintos.

Dirige a UI de seleção de lista de unidade (família
`iOSUnitList*`: `OutWin`, `FlagGet`/`Set`/`Clear`, `WinOnOff`,
`StsMoveCheck`, `LRCur`, `AllStatusTapCheck`), o widget de grade
genérico `UnitTable`/`UnitTableInit`/`InitFirst`, primitivos de
toque, o sistema de menu/ícone v2 (`iOS_v2menuSetEnable`/`SetType`/
`GetType`), e plumbing de janela/mensagem. **Confirma ser o
controlador de nível superior que apresenta o roster de personagem
antes de passar pra `DressEquip`** (e outras sub-telas de Dress) —
embora nenhuma chamada direta a `DressEquip` apareça no catálogo
(a transição provavelmente passa por uma máquina de estado/
dispatcher de task compartilhada, via `Wsend_taskparamater`, não
chamada de função direta). Marcada `read_structural`.

## 179. `BattleEquip(...)` — refina a teoria da letra de prefixo: `e` é um CONTEXTO DE TASK DUPLICADO COMPLETO, não só nome de buffer (2026-10-18, Fase 3, lote paralelo, achado metodológico)

`BattleEquip(int, long*)` (`0x18e3f0`, 1.700 B) — descida recursiva
via `jtable.py`: **323 de ~425 instruções possíveis (76%)**, sem
tabela de salto; **9 branches, 3 de retrocesso**. 19 `bl` distintos.

**Achado que corrige a hipótese "`b`/`e` = só nome de variável de
buffer" das seções 113/153 (`bDB_init`/`eDB_init`)**: esta função
chama uma FAMÍLIA INTEIRA de helpers com prefixo `e` nunca vista
reunida — `eSwapDB`, `eDB_init`, `eGetChrSingle(int)`,
`eRefleshItemUserSort(int)` (×5), `eWaitLoadImage`/`eWaitStoreImage`
(×6/×2), `eSetSttsA`/`eSetSttsPara`/`eSetSttsEqu`, `eCurChrChg()`,
`equans_init()`, `eWindowPositionInit()`, `eHelpMessage(int)`,
`eMenuSelInit()`, `eGetMaskedPad()`, `eSelectWindowClut(int)` — um
conjunto completo de telas/widgets/helpers `e`-prefixados paralelo
aos sem prefixo (`GetChrSingle`, `RefleshItemUserSort`, `SetSttsA`,
etc., não todos ainda confirmados por nome exato mas pelo padrão). **
Conclusão**: `e` (e, por extensão, `b`/`c`/`j`, vistos em
`MakeWindowFunc`/`GetPad`) NÃO é apenas o nome de uma variável de
double-buffer — é um **contexto de task duplicado completo**, do
mesmo tipo arquitetural que `W` (que tem sua própria
`Waddlocalprim`/`Wbgput`/etc.), só que pra um conjunto de telas
diferente (aqui, o fluxo de equipar em batalha). Isso explica por
que `bDB_init`/`eDB_init` pareciam idênticos (regra 6, boilerplate
de SDK puro, sem lógica de jogo) mas `BattleEquip` usando `e` revela
lógica de jogo real duplicada por contexto. Também chama
`popmessagepacket()` (sincronia de rede/mensagem, plausível pra
equipar em batalha precisar sincronizar entre jogadores). Marcada
`read_structural`.

## 180. `ASHURA_SetMatrix(...)` — utilitário de matriz multi-modo com tabela de salto de 12 casos, toca matriz de cor também (2026-10-18, Fase 3, lote paralelo)

`ASHURA_SetMatrix(long, MATRIX*, MATRIX*, unsigned short)`
(`0x163348`, 1.636 B, termina exatamente em `ASHURA_CVECTOR`,
0x1639ac) — descida recursiva via `jtable.py`: **387 de ~409
instruções possíveis (95%)**; **uma tabela de salto resolvida**
(guarda `cmp` em `0x163368`, dispatch em `0x16336c`, **12 casos, 10
handlers distintos**); **10 branches, TODOS de retrocesso** (os 10
branches são todos laço, nenhum é só forward).

Catálogo mínimo (`SetColorMatrix` ×3, `__divsi3` ×8) mas a tabela de
12 casos despachando por um `unsigned short` (4º parâmetro) sugere
um utilitário "setar matriz por modo" com 10 caminhos de combinação
de matriz diferentes (atalhos de identidade, só-rotação, só-escala,
composição completa, etc.), não uma multiplicação fixa pai×filho
única — a chamada a `SetColorMatrix` em alguns caminhos sugere que
também toca matriz de cor/iluminação em certos modos, não só
geometria. Consistente com um passo de composição de matriz local
de nó na hierarquia LMDL (junto com `ASHURA_LMDL_Read`/
`ASURA_LMDL_TIME_TBL`/`ASHURA_MapProjectMem2Mem`), mas com múltiplos
modos de dispatch em vez de uma única rotina dedicada. Marcada
`read_structural`.
