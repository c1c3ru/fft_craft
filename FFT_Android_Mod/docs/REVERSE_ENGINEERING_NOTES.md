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
