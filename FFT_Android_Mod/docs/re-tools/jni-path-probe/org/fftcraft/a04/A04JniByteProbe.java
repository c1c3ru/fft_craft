package org.fftcraft.a04;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;

/**
 * Host JVM JNI byte-level probe, NOT an Android path length oracle.
 * Tests GetStringUTFLength/GetStringUTFChars against bounded A04 C model.
 */
public final class A04JniByteProbe {
    static {
        System.loadLibrary("a04_jni_probe");
    }

    private A04JniByteProbe() {}

    private static native int getUtfByteCount(String source);
    private static native byte[] getUtfBytes(String source);
    private static native byte[] safeConcat(String source);

    private static final byte[] SUFFIX =
        "/base/fftpack.bin\0".getBytes(StandardCharsets.US_ASCII);
    private static int assertions = 0;
    private static int accepted = 0;
    private static int rejected = 0;

    private static void check(boolean value, String message) {
        ++assertions;
        if (!value) throw new AssertionError(message);
    }

    private static void measure(String value, int expected) {
        int n = getUtfByteCount(value);
        check(n == expected, "JNI modified-UTF length mismatch: " + n + " vs " + expected);
        byte[] observed = getUtfBytes(value);
        check(observed != null && observed.length == n,
              "GetStringUTFChars byte length mismatch");
        byte[] output = safeConcat(value);
        if (n <= 242) {
            check(output != null && output.length == n + SUFFIX.length,
                  "Bounded C model must accept exactly " + n + " bytes");
            byte[] expectedOutput = new byte[n + SUFFIX.length];
            System.arraycopy(observed, 0, expectedOutput, 0, n);
            System.arraycopy(SUFFIX, 0, expectedOutput, n, SUFFIX.length);
            check(Arrays.equals(expectedOutput, output),
                  "C reconstruction changed output or NUL");
            ++accepted;
        } else {
            check(output == null, "C reconstruction accepted >242 MUTF8 bytes: " + n);
            ++rejected;
        }
    }

    public static void main(String[] args) {
        check(getUtfByteCount(null) == -1, "NULL JNI string must be rejected");
        check(getUtfBytes(null) == null, "NULL JNI bytes must not be accessed");
        check(safeConcat(null) == null, "NULL C model input must be rejected");

        for (int n = 0; n <= 260; ++n) {
            measure("x".repeat(n), n);
        }
        measure("\u00e9".repeat(121), 242);
        measure("\u00e9".repeat(122), 244);
        measure("\u4e2d".repeat(80), 240);
        measure("\u4e2d".repeat(81), 243);
        measure("\ud83d\ude00".repeat(40), 240);
        measure("\ud83d\ude00".repeat(41), 246);
        measure("\u0000".repeat(121), 242);
        measure("\u0000".repeat(122), 244);
        measure("a\u0000b", 4);
        measure("a\ud83d\ude00z", 8);

        byte[] nul = getUtfBytes("a\u0000b");
        check(Arrays.equals(nul, new byte[] {97, (byte)0xc0, (byte)0x80, 98}),
              "JNI NUL must encode to C0 80 in modified UTF-8");
        check("a\u0000b".getBytes(StandardCharsets.UTF_8).length == 3,
              "Host UTF-8 must differ from JNI modified UTF-8 on NUL");
        check("\ud83d\ude00".getBytes(StandardCharsets.UTF_8).length == 4,
              "Standard UTF-8 supplementary scalar is 4 bytes");
        check(getUtfByteCount("\ud83d\ude00") == 6,
              "JNI MUTF8 supplementary scalar must be six bytes");

        System.out.println("A04_JNI_HOST_CASES=271");
        System.out.println("A04_JNI_HOST_ACCEPTED=" + accepted);
        System.out.println("A04_JNI_HOST_REJECTED=" + rejected);
        System.out.println("A04_JNI_HOST_ASSERTIONS=" + assertions);
        System.out.println("A04_JNI_MODIFIED_UTF8_CONFIRMED=1");
        System.out.println("A04_JNI_REAL_ANDROID_PATH_SAMPLES=0");
        System.out.println("A04_JNI_NEW_SEMANTIC_CERTIFICATES=0");
    }
}
