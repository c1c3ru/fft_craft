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
