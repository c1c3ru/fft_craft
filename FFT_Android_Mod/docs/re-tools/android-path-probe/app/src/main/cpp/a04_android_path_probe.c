#include <jni.h>
#include <stddef.h>

/* JNI implementation used ONLY in the independent Android test APK.
 * It neither links the original game ELF nor invokes the unsafe strcpy.
 */
JNIEXPORT jint JNICALL
Java_org_fftcraft_a04_probe_PathProbeActivity_getJniModifiedUtf8ByteLength(
    JNIEnv *env, jclass ignored, jstring text) {
    (void)ignored;
    if (text == NULL) return -1;
    return (*env)->GetStringUTFLength(env, text);
}

/* Confirm actual Android ART bytes, not only GetStringUTFLength's number.
 * Only short synthetic probe strings (up to 128 bytes) are supported.
 */
JNIEXPORT jstring JNICALL
Java_org_fftcraft_a04_probe_PathProbeActivity_getJniUtfBytesHex(
    JNIEnv *env, jclass ignored, jstring text) {
    (void)ignored;
    if (text == NULL) return NULL;
    jsize size = (*env)->GetStringUTFLength(env, text);
    if ((*env)->ExceptionCheck(env) || size < 0 || size > 128) return NULL;
    const char *raw = (*env)->GetStringUTFChars(env, text, NULL);
    if (raw == NULL) return NULL;
    static const char digits[] = "0123456789abcdef";
    char out[257];
    for (jsize i = 0; i < size; ++i) {
        unsigned char b = (unsigned char)raw[i];
        out[i * 2] = digits[b >> 4];
        out[i * 2 + 1] = digits[b & 15];
    }
    out[size * 2] = 0;
    (*env)->ReleaseStringUTFChars(env, text, raw);
    return (*env)->NewStringUTF(env, out); /* ASCII hex is JNI-safe */
}


/* Execute only the independent bounded reconstruction against ACTUAL ART
 * GetStringUTFChars bytes. Never invoke the original ELF/strcpy.
 *
 * Returns 1 on a clean bounded copy, 0 on a rejected length, -1 for absent
 * input and -2 for an internal invariant/canary failure (CI must fail).
 */
#include <stdint.h>
#include <string.h>
int a04_build_fftpack_path(uint8_t *out, size_t capacity,
                           const uint8_t *src, size_t length);

JNIEXPORT jint JNICALL
Java_org_fftcraft_a04_probe_PathProbeActivity_safeBuildPathWithinBound(
    JNIEnv *env, jclass ignored, jstring text) {
    (void)ignored;
    if (text == NULL) return -1;
    jsize size = (*env)->GetStringUTFLength(env, text);
    if ((*env)->ExceptionCheck(env) || size < 0) return -2;
    if (size > 242) return 0;
    const char *bytes = (*env)->GetStringUTFChars(env, text, NULL);
    if (bytes == NULL) return -2;
    uint8_t dst[276];
    memset(dst, 0xa5, sizeof dst);
    int ok = a04_build_fftpack_path(dst, 260,
                                   (const uint8_t *)bytes, (size_t)size);
    (*env)->ReleaseStringUTFChars(env, text, bytes);
    if (ok != 1) return -2;
    for (size_t i = (size_t)size + 18; i < sizeof dst; ++i) {
        if (dst[i] != 0xa5) return -2;
    }
    return 1;
}
