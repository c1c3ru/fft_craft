#!/usr/bin/env bash
set -euo pipefail
APK="$1"
OUT="/tmp/a04-android-path.json"
if [ "$#" -ge 2 ]; then OUT="$2"; fi
PKG="com.square_enix.android_googleplay.FFT_en2"
adb install -r "$APK"
adb shell am start -W -n "$PKG/org.fftcraft.a04.probe.PathProbeActivity"
for attempt in $(seq 1 20); do
  if adb shell run-as "$PKG" cat files/a04_path_probe.json > "$OUT" 2>/dev/null; then
    if python3 -m json.tool "$OUT" >/dev/null 2>&1; then
      break
    fi
  fi
  sleep 1
done
python3 - "$OUT" <<'PY'
import json
import sys
with open(sys.argv[1], encoding="utf-8") as stream:
    r=json.load(stream)
assert r["status"] == "sampled_not_a_global_bound", r
assert r["running_original_game_apk"] is False, r
assert r["same_package_name_as_original_game"] is True, r
assert r["native_method"] == "JNI GetStringUTFLength", r
assert r["original_strcpy_executed"] is False, r
assert r["native_ascii_242"] == 242, r
assert r["native_ascii_243"] == 243, r
assert r["native_emoji_one"] == 6, r
assert r["native_embedded_nul"] == 4, r
for key in ("GetIntPath","GetExt1Path"):
    data=r[key]
    if data["present"]:
        n=data["jni_mutf8_byte_length"]
        assert isinstance(n,int) and n >= 0, data
        assert data["within_242_bytes"] == (n <= 242), data
    else:
        assert data["jni_mutf8_byte_length"] is None, data
assert r["GetIntPath"]["present"] is True, r
print("A04_ANDROID_EMULATOR_MEASUREMENT="+json.dumps(r,sort_keys=True))
print("A04_ANDROID_ORIGINAL_GAME_ELF_EXECUTED=0")
print("A04_ANDROID_JNI_BYTE_COUNTER_CONFIRMED=1")
PY
