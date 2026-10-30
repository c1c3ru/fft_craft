package org.fftcraft.a04.probe;

import android.app.Activity;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import org.json.JSONObject;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;

/**
 * Diagnostic APK using target game's package identity on an isolated emulator.
 * DOES NOT contain or execute the original game. Mirrors the two Context
 * calls represented in StorageUtil.smali.
 */
public final class PathProbeActivity extends Activity {
    private static final String TAG = "A04_ANDROID_PATH";
    private static final int MAX_JNI_BYTES = 242;
    private static final String TARGET_PACKAGE =
        "com.square_enix.android_googleplay.FFT_en2";

    static { System.loadLibrary("a04_android_path_probe"); }
    private static native int getJniModifiedUtf8ByteLength(String text);
    private static native String getJniUtfBytesHex(String text);
    private static native int safeBuildPathWithinBound(String text);

    private static JSONObject measure(String source, String value) throws Exception {
        JSONObject out = new JSONObject();
        out.put("source", source);
        boolean exists = value != null;
        out.put("present", exists);
        int bytes = exists ? getJniModifiedUtf8ByteLength(value) : -1;
        out.put("jni_mutf8_byte_length", exists ? bytes : JSONObject.NULL);
        out.put("within_242_bytes", exists ? bytes <= MAX_JNI_BYTES : JSONObject.NULL);
        int safe = exists ? safeBuildPathWithinBound(value) : -1;
        if (exists && safe != (bytes <= MAX_JNI_BYTES ? 1 : 0)) {
            throw new IllegalStateException("Bounded native reference disagrees with JNI byte gate");
        }
        out.put("bounded_c_model_accepted", exists ? safe == 1 : JSONObject.NULL);
        out.put("java_utf16_length", exists ? value.length() : JSONObject.NULL);
        // No path contents are retained in CI artifacts.
        return out;
    }

    private void persist(JSONObject result) throws Exception {
        File output = new File(getFilesDir(), "a04_path_probe.json");
        try (OutputStreamWriter writer = new OutputStreamWriter(
                new FileOutputStream(output), StandardCharsets.UTF_8)) {
            writer.write(result.toString());
            writer.write("\n");
        }
        Log.i(TAG, "A04_ANDROID_PROBE_RESULT=" + result.toString());
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        try {
            JSONObject result = new JSONObject();
            result.put("schema", 2);
            result.put("android_sdk", Build.VERSION.SDK_INT);
            result.put("package_identity", getPackageName());
            result.put("same_package_name_as_original_game",
                    TARGET_PACKAGE.equals(getPackageName()));
            result.put("running_original_game_apk", false);
            result.put("native_method", "JNI GetStringUTFLength");
            result.put("original_strcpy_executed", false);
            String internal = getFilesDir().getPath();
            File externalDir = getExternalFilesDir(null);
            String external = externalDir == null ? null : externalDir.getPath();
            result.put("GetIntPath", measure("Context.getFilesDir.getPath", internal));
            result.put("GetExt1Path", measure(
                "Context.getExternalFilesDir_null.getPath", external));

            // Synthetic null exercises the JNI sentinel and absent-path contract.
            // It is NOT evidence that either Android getter returned null.
            JSONObject syntheticNull = measure("synthetic_null_path", null);
            if (syntheticNull.getBoolean("present")
                    || !syntheticNull.isNull("jni_mutf8_byte_length")
                    || !syntheticNull.isNull("within_242_bytes")
                    || !syntheticNull.isNull("bounded_c_model_accepted")) {
                throw new IllegalStateException("Null path was treated as a real string");
            }
            result.put("diagnostic_synthetic_null_path", syntheticNull);
            result.put("native_null_length_sentinel", getJniModifiedUtf8ByteLength(null));
            result.put("bounded_c_null_sentinel", safeBuildPathWithinBound(null));

            result.put("native_ascii_242", getJniModifiedUtf8ByteLength(
                    new String(new char[242]).replace('\0', 'x')));
            result.put("native_ascii_243", getJniModifiedUtf8ByteLength(
                    new String(new char[243]).replace('\0', 'x')));
            result.put("bounded_c_ascii_242", safeBuildPathWithinBound(
                    new String(new char[242]).replace('\0', 'x')));
            result.put("bounded_c_ascii_243", safeBuildPathWithinBound(
                    new String(new char[243]).replace('\0', 'x')));
            result.put("bounded_c_nul_java", safeBuildPathWithinBound("a\0b"));
            result.put("bounded_c_emoji_one", safeBuildPathWithinBound("\ud83d\ude00"));
            result.put("native_emoji_one", getJniModifiedUtf8ByteLength("\ud83d\ude00"));
            result.put("native_embedded_nul", getJniModifiedUtf8ByteLength("a\0b"));
            result.put("native_emoji_utf_bytes_hex", getJniUtfBytesHex("\ud83d\ude00"));
            result.put("native_nul_utf_bytes_hex", getJniUtfBytesHex("a\0b"));
            result.put("status", "sampled_not_a_global_bound");
            persist(result);
        } catch (Throwable failure) {
            Log.e(TAG, "A04 probe failed", failure);
            try {
                JSONObject err = new JSONObject();
                err.put("schema", 2);
                err.put("status", "error");
                err.put("error_type", failure.getClass().getName());
                persist(err);
            } catch (Throwable ignored) {
                Log.e(TAG, "Unable to persist failure", ignored);
            }
        } finally {
            finish();
        }
    }
}
