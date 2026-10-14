#!/bin/bash
# Remove os artefatos de build (nunca toca em src/ nem em original/).
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

rm -rf "$BUILD_DIR"
rm -rf "$SRC_DIR/build"   # cache interno que o apktool às vezes recria
echo "build/ limpo."
