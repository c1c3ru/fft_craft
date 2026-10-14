#!/bin/bash
# Variáveis compartilhadas por todos os scripts deste projeto.
# Dá "source" neste arquivo; não execute diretamente.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

APKTOOL_JAR="/home/c1c3ru/.local/share/apktool/apktool_3.0.3.jar"
BUILD_TOOLS="/home/c1c3ru/Android/Sdk/build-tools/36.0.0"
ZIPALIGN="$BUILD_TOOLS/zipalign"
APKSIGNER="$BUILD_TOOLS/apksigner"

ORIGINAL_APK="$PROJECT_ROOT/original/FFT_By_MortalGx.apk"
SRC_DIR="$PROJECT_ROOT/src"
BUILD_DIR="$PROJECT_ROOT/build"
KEYSTORE="$PROJECT_ROOT/keystore/debug.keystore"
KEYSTORE_PASS="android"
KEY_ALIAS="androiddebugkey"

PACKAGE_NAME="com.square_enix.android_googleplay.FFT_en2"
LAUNCHER_ACTIVITY="com.square_enix.FFT_Android.LicenseCheckerActivity"

OBB_DIR="$PROJECT_ROOT/obb-data"
OBB_FILE_NAME="main.202000.$PACKAGE_NAME.obb"
OBB_LOCAL_PATH="$OBB_DIR/$OBB_FILE_NAME"
OBB_DEVICE_DIR="/sdcard/Android/obb/$PACKAGE_NAME"

UNSIGNED_APK="$BUILD_DIR/FFT_Android_Mod-unsigned.apk"
ALIGNED_APK="$BUILD_DIR/FFT_Android_Mod-aligned.apk"
SIGNED_APK="$BUILD_DIR/FFT_Android_Mod-signed.apk"

apktool() {
  java -jar "$APKTOOL_JAR" "$@"
}
