#!/bin/bash
# Envia o arquivo de expansão (.obb) para o caminho que o app espera no
# dispositivo/emulador conectado.
# Uso: scripts/push-obb.sh
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

ADB="/home/c1c3ru/Android/Sdk/platform-tools/adb"

if [ ! -f "$OBB_LOCAL_PATH" ]; then
  echo "Não encontrado: $OBB_LOCAL_PATH" >&2
  echo "Coloque o .obb em $OBB_DIR/ com esse nome exato." >&2
  exit 1
fi

echo "== criando diretório no device =="
"$ADB" shell mkdir -p "$OBB_DEVICE_DIR"

echo "== enviando $(basename "$OBB_LOCAL_PATH") ($(du -h "$OBB_LOCAL_PATH" | cut -f1)) =="
"$ADB" push "$OBB_LOCAL_PATH" "$OBB_DEVICE_DIR/"

echo "== confirmando no device =="
"$ADB" shell ls -la "$OBB_DEVICE_DIR/"
