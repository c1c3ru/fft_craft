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
