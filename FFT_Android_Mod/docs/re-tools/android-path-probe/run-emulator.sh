#!/usr/bin/env bash
set -euo pipefail
APK="$1"
OUT="/tmp/a04-android-path.json"
if [ "$#" -ge 2 ]; then OUT="$2"; fi
EXPECTED_API="${3:-}"
if [ -n "$EXPECTED_API" ]; then
  ACTUAL_API="$(adb shell getprop ro.build.version.sdk | tr -d '\r')"
  if [ "$ACTUAL_API" != "$EXPECTED_API" ]; then
    echo "Android API mismatch: expected $EXPECTED_API, got $ACTUAL_API" >&2
    exit 1
  fi
fi
PKG="com.square_enix.android_googleplay.FFT_en2"
# Never overwrite a real game installation or run this diagnostic on a phone.
if [ "$(adb shell getprop ro.kernel.qemu | tr -d '\r')" != "1" ]; then
  echo "A04 path probe is restricted to an Android emulator" >&2
  exit 1
fi
if adb shell pm path "$PKG" | grep -q '^package:'; then
  echo "Refusing to replace an existing installation with the same package ID" >&2
  exit 1
fi
adb install "$APK"
adb shell am start -W -n "$PKG/org.fftcraft.a04.probe.PathProbeActivity"
for attempt in $(seq 1 20); do
  if adb shell run-as "$PKG" cat files/a04_path_probe.json > "$OUT" 2>/dev/null; then
    if python3 -m json.tool "$OUT" >/dev/null 2>&1; then
      break
    fi
  fi
  sleep 1
done
python3 - "$OUT" "$EXPECTED_API" <<'PY'
import json
import sys
with open(sys.argv[1], encoding="utf-8") as stream:
    r=json.load(stream)
expected_api=sys.argv[2]
assert isinstance(r.get("android_sdk"),int), r
if expected_api:
    assert r["android_sdk"] == int(expected_api), r
assert r["schema"] == 2, r
assert r["status"] == "sampled_not_a_global_bound", r
assert r["running_original_game_apk"] is False, r
assert r["same_package_name_as_original_game"] is True, r
assert r["native_method"] == "JNI GetStringUTFLength", r
assert r["original_strcpy_executed"] is False, r
assert r["native_null_length_sentinel"] == -1, r
assert r["bounded_c_null_sentinel"] == -1, r
null_fixture = r["diagnostic_synthetic_null_path"]
assert null_fixture["source"] == "synthetic_null_path", null_fixture
assert null_fixture["present"] is False, null_fixture
for field in ("jni_mutf8_byte_length", "within_242_bytes",
              "bounded_c_model_accepted", "java_utf16_length"):
    assert null_fixture[field] is None, null_fixture
assert r["native_ascii_242"] == 242, r
assert r["native_ascii_243"] == 243, r
assert r["bounded_c_ascii_242"] == 1, r
assert r["bounded_c_ascii_243"] == 0, r
assert r["bounded_c_nul_java"] == 1, r
assert r["bounded_c_emoji_one"] == 1, r
assert r["native_emoji_one"] == 4, r
assert r["native_emoji_utf_bytes_hex"] == "f09f9880", r
assert r["native_nul_utf_bytes_hex"] == "61c08062", r
assert r["native_embedded_nul"] == 4, r
method_sources={"GetIntPath":"Context.getFilesDir.getPath",
                "GetExt1Path":"Context.getExternalFilesDir_null.getPath"}
for key in ("GetIntPath","GetExt1Path"):
    data=r[key]
    assert data["source"] == method_sources[key], data
    if data["present"]:
        n=data["jni_mutf8_byte_length"]
        assert type(n) is int and n >= 0, data
        assert type(data["java_utf16_length"]) is int and data["java_utf16_length"] >= 0, data
        assert data["within_242_bytes"] == (n <= 242), data
        assert data["bounded_c_model_accepted"] == (n <= 242), data
    else:
        assert data["jni_mutf8_byte_length"] is None, data
        assert data["within_242_bytes"] is None, data
        assert data["java_utf16_length"] is None, data
        assert data["bounded_c_model_accepted"] is None, data
assert r["GetIntPath"]["present"] is True, r
print("A04_ANDROID_EMULATOR_MEASUREMENT="+json.dumps(r,sort_keys=True))
print("A04_ANDROID_ORIGINAL_GAME_ELF_EXECUTED=0")
print("A04_ANDROID_JNI_BYTE_COUNTER_CONFIRMED=1")
PY
