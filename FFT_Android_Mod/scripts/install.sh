#!/bin/bash
# Instala o APK assinado mais recente em um dispositivo/emulador conectado.
# Uso: scripts/install.sh [--launch]
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

ADB="/home/c1c3ru/Android/Sdk/platform-tools/adb"

if [ ! -f "$SIGNED_APK" ]; then
  echo "Nenhum build encontrado. Rode scripts/build.sh primeiro." >&2
  exit 1
fi

"$ADB" install -r "$SIGNED_APK"

if [ "${1:-}" = "--launch" ]; then
  "$ADB" shell am start -n "$PACKAGE_NAME/$LAUNCHER_ACTIVITY"
fi

cat <<EOF

Lembrete: o jogo só passa da tela de verificação de arquivos se existir

  /sdcard/Android/obb/$PACKAGE_NAME/main.1002.$PACKAGE_NAME.obb

no dispositivo/emulador. Veja docs/REVERSE_ENGINEERING_NOTES.md.
EOF
