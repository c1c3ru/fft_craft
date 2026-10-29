#include <stddef.h>
#include <stdint.h>

/*
 * Safe host-side REFERENCE for the A04 rootpath→fftpack.bin layout.
 * NOT a byte-for-byte ABI replacement of Android JNI or the original ELF.
 * Input is already encoded as JNI/UTF bytes and its accessible size is a
 * caller-enforced precondition. Reject before any output write.
 */
#define A04_JAVA_MAX_BYTES 242u
#define A04_OVERHEAD 18u  /* "/base/" + "fftpack.bin" + NUL */

int a04_build_fftpack_path(uint8_t *out, size_t out_capacity,
                            const uint8_t *java_bytes, size_t java_len) {
    static const uint8_t suffix[] = {
        '/', 'b', 'a', 's', 'e', '/', 'f', 'f', 't',
        'p', 'a', 'c', 'k', '.', 'b', 'i', 'n', 0
    };
    if (!out || !java_bytes || out_capacity < A04_OVERHEAD ||
        java_len > A04_JAVA_MAX_BYTES ||
        java_len > out_capacity - A04_OVERHEAD)
        return 0;

    /* Only disjoint buffers: do not silently promise overlapping strcpy.
     * uintptr_t pointer comparisons are for this host reference, not a
     * universal guarantee across foreign ABIs/address spaces.
     */
    uintptr_t dst = (uintptr_t)out;
    uintptr_t src = (uintptr_t)java_bytes;
    if (out_capacity > UINTPTR_MAX - dst ||
        java_len > UINTPTR_MAX - src)
        return 0;
    if (src < dst + out_capacity && dst < src + java_len)
        return 0;
    for (size_t i = 0; i < java_len; ++i) {
        if (java_bytes[i] == 0)
            return 0;
    }
    for (size_t i = 0; i < java_len; ++i)
        out[i] = java_bytes[i];
    for (size_t j = 0; j < sizeof(suffix); ++j)
        out[java_len+j] = suffix[j];
    return 1;
}
