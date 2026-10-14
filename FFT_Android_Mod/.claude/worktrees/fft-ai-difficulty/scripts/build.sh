#!/bin/bash
# Compila src/ -> APK alinhado e assinado em build/.
# Uso: scripts/build.sh
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"

mkdir -p "$BUILD_DIR"

if [ ! -f "$KEYSTORE" ]; then
  echo "== Nenhuma keystore encontrada; gerando uma de debug em $KEYSTORE =="
  keytool -genkeypair -v -keystore "$KEYSTORE" -storepass "$KEYSTORE_PASS" \
    -alias "$KEY_ALIAS" -keypass "$KEYSTORE_PASS" -keyalg RSA -keysize 2048 \
    -validity 10000 -dname "CN=Android Debug,O=Android,C=US"
fi

echo "== apktool build =="
apktool b "$SRC_DIR" -o "$UNSIGNED_APK"
rm -rf "$SRC_DIR/build"   # cache interno do apktool; não é fonte editável

echo "== zipalign =="
"$ZIPALIGN" -p -f 4 "$UNSIGNED_APK" "$ALIGNED_APK"

echo "== apksigner sign =="
"$APKSIGNER" sign \
  --ks "$KEYSTORE" --ks-pass "pass:$KEYSTORE_PASS" --key-pass "pass:$KEYSTORE_PASS" \
  --ks-key-alias "$KEY_ALIAS" \
  --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true \
  --out "$SIGNED_APK" "$ALIGNED_APK"

echo "== apksigner verify =="
"$APKSIGNER" verify --print-certs "$SIGNED_APK"

echo
echo "APK pronto: $SIGNED_APK"
