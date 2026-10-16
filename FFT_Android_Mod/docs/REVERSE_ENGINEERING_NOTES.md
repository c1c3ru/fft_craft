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
