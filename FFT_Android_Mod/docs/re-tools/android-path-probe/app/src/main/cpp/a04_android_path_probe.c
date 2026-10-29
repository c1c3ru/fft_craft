#include <jni.h>

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
