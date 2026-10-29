#include <jni.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

int a04_build_fftpack_path(uint8_t *out, size_t out_capacity,
                           const uint8_t *java_bytes, size_t java_len);

static void invariant_failure(JNIEnv *env, const char *reason) {
    jclass klass = (*env)->FindClass(env, "java/lang/IllegalStateException");
    if (klass) (*env)->ThrowNew(env, klass, reason);
}

JNIEXPORT jint JNICALL
Java_org_fftcraft_a04_A04JniByteProbe_getUtfByteCount
(JNIEnv *env, jclass owner, jstring source) {
    (void)owner;
    return source == NULL ? -1 : (*env)->GetStringUTFLength(env, source);
}

JNIEXPORT jbyteArray JNICALL
Java_org_fftcraft_a04_A04JniByteProbe_getUtfBytes
(JNIEnv *env, jclass owner, jstring source) {
    (void)owner;
    if (source == NULL) return NULL;
    jsize len = (*env)->GetStringUTFLength(env, source);
    if ((*env)->ExceptionCheck(env)) return NULL;
    const char *bytes = (*env)->GetStringUTFChars(env, source, NULL);
    if (bytes == NULL) return NULL;
    jbyteArray result = (*env)->NewByteArray(env, len);
    if (result != NULL)
        (*env)->SetByteArrayRegion(env, result, 0, len, (const jbyte *)bytes);
    (*env)->ReleaseStringUTFChars(env, source, bytes);
    return result;
}

JNIEXPORT jbyteArray JNICALL
Java_org_fftcraft_a04_A04JniByteProbe_safeConcat
(JNIEnv *env, jclass owner, jstring source) {
    (void)owner;
    if (source == NULL) return NULL;
    jsize len = (*env)->GetStringUTFLength(env, source);
    if ((*env)->ExceptionCheck(env)) return NULL;
    if (len > 242) return NULL;

    const char *bytes = (*env)->GetStringUTFChars(env, source, NULL);
    if (bytes == NULL) return NULL;
    uint8_t dst[276]; /* 260-byte field and 16 canary bytes */
    memset(dst, 0xa5, sizeof dst);
    int ok = a04_build_fftpack_path(dst, 260, (const uint8_t *)bytes, (size_t)len);
    (*env)->ReleaseStringUTFChars(env, source, bytes);

    if (!ok) {
        invariant_failure(env, "Unexpected failure for input <= 242 JNI bytes");
        return NULL;
    }
    for (size_t i = (size_t)len + 18; i < sizeof dst; ++i) {
        if (dst[i] != 0xa5) {
            invariant_failure(env, "Native builder wrote past output extent");
            return NULL;
        }
    }
    jbyteArray result = (*env)->NewByteArray(env, len + 18);
    if (result != NULL) {
        (*env)->SetByteArrayRegion(env, result, 0, len + 18,
                                  (const jbyte *)dst);
    }
    return result;
}
