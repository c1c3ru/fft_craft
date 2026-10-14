# FFT Android Mod

Projeto de modificação do APK *Final Fantasy Tactics: The War of the Lions*
(Android, pacote `com.square_enix.android_googleplay.FFT_en2`, versionCode
1002). Base: decode/rebuild via `apktool`, assinatura via `apksigner` do
Android SDK.

## Estrutura

```
original/   APK original intocado (referência, com checksum). Nunca editar.
src/        Projeto editável: smali, res/, AndroidManifest.xml.
            É AQUI que você faz as modificações. Versionado no git.
obb-data/   Arquivo(s) .obb (dado do jogo, ~800MB). Fora do git (.gitignore).
build/      Saída dos builds (gerado, não versionado).
keystore/   Chave de assinatura (gerada automaticamente se faltar).
scripts/    build.sh / decode.sh / install.sh / push-obb.sh / clean.sh
docs/       Achados da engenharia reversa (ver REVERSE_ENGINEERING_NOTES.md).
```

## Fluxo de trabalho

1. Edite arquivos em `src/smali/...` (lógica) ou `src/res/...` (recursos,
   strings, layouts) ou `src/AndroidManifest.xml`.
2. `./scripts/build.sh` — gera `build/FFT_Android_Mod-signed.apk`.
3. `./scripts/push-obb.sh` — copia o `.obb` de `obb-data/` para
   `/sdcard/Android/obb/<package>/` no device/emulador conectado (só
   precisa rodar de novo se o dispositivo mudar ou o arquivo for apagado).
4. `./scripts/install.sh --launch` — instala o APK e abre o jogo.
5. Edições ficam em `src/`, que é um repositório git — use `git diff` /
   `git log` normalmente para acompanhar o que foi mudado.

Para descartar tudo e recomeçar do zero a partir do APK original:
`./scripts/decode.sh` (pede confirmação antes de sobrescrever `src/`).

## Requisitos já confirmados nesta máquina

- `apktool` 3.0.3 — `~/.local/share/apktool/apktool_3.0.3.jar` (wrapper em
  `~/.local/bin/apktool`)
- Android SDK build-tools 36.0.0 — `~/Android/Sdk/build-tools/36.0.0/`
  (`aapt2`, `zipalign`, `apksigner`)
- `adb` — `~/Android/Sdk/platform-tools/adb`
- JDK (`keytool`/`jarsigner`) — já presente no sistema

Pipeline testado de ponta a ponta: decode → build → zipalign → sign →
verify, sem erros.

## Arquivo de expansão (OBB)

O jogo precisa do arquivo abaixo presente no dispositivo para passar da
tela de verificação de arquivos:

```
/sdcard/Android/obb/com.square_enix.android_googleplay.FFT_en2/main.202000.com.square_enix.android_googleplay.FFT_en2.obb
```

O `.obb` original baixado estava na versão **202000**, enquanto o APK (como
baixado, versionCode 1002) esperava a versão **1002** — nome não batia e o
app ficava travado tentando baixar. **Corrigido**: editei os 3 pontos do
smali onde esse número de versão estava gravado em bytecode (não é um
único campo central — veja seção 7 das notas) para que o APK procure
exatamente pelo arquivo que você tem. Coloque o `.obb` em `obb-data/` com
esse nome e rode `scripts/push-obb.sh`.

## O que já foi mapeado no código (útil antes de editar)

Veja `docs/REVERSE_ENGINEERING_NOTES.md` para:
- onde está o patch que sempre libera a verificação de licença
  (`ServerManagedPolicy.allowAccess()`)
- a correção de versão do OBB (seção 7) e por que não bastava editar um
  campo só
- os ajustes de manifesto para Android recente e a limitação real que
  fica de fora — libs nativas só em 32-bit, sem `arm64-v8a`/`x86_64`
  (seção 8)
- lista de classes/métodos do app (57 classes, DEX pequeno — a lógica do
  jogo em si está nas libs nativas `lib/*/libgl2jni.so`, não no Java)
