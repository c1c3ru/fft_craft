#!/bin/bash
# Regenera src/ a partir do APK original em original/.
# Use isto só se quiser descartar todas as edições e recomeçar do zero,
# ou para comparar seu src/ atual contra um decode limpo (ex.: copie
# a saída para outra pasta e rode `diff -r` antes de sobrescrever).
#
# Uso: scripts/decode.sh
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

if [ -d "$SRC_DIR" ] && [ -n "$(ls -A "$SRC_DIR" 2>/dev/null)" ]; then
  echo "AVISO: $SRC_DIR já existe e não está vazio."
  echo "Isto vai SOBRESCREVER suas edições. Ctrl+C para cancelar, Enter para continuar."
  read -r _
fi

apktool d "$ORIGINAL_APK" -o "$SRC_DIR" -f

# apktool cria um diretório build/ interno dentro do decode; não faz parte
# do código-fonte editável e não deve ser versionado.
rm -rf "$SRC_DIR/build"

echo "Decodificado em: $SRC_DIR"
