#include <stddef.h>
#include <stdint.h>

/* Independent bounded model of original A32 0xb6620, nonnull source branch.
 * The ELF calls imported strcpy, then SJIS-aware slash normalization and
 * clears the 32-bit field at destination+0x104. Only safe, separate buffers
 * with a NUL terminator within supplied bounds are accepted.
 */
extern int a04_normalize_sjis_slashes(uint8_t *buffer, size_t capacity);

int a04_copy_normalize_nonzero(uint8_t *dest, size_t dest_size,
                               const uint8_t *src, size_t src_size) {
    if (!dest || !src || dest_size < 0x108u || src_size == 0u)
        return 0;
    size_t count = 0u;
    while (count < src_size && src[count] != 0u)
        ++count;
    /* No cross-boundary copies and no overwrite of the metadata at +0x104. */
    if (count == src_size || count + 1u > 0x104u)
        return 0;
    for (size_t i = 0u; i <= count; ++i)
        dest[i] = src[i];
    if (!a04_normalize_sjis_slashes(dest, 0x104u))
        return 0;
    dest[0x104] = 0u;
    dest[0x105] = 0u;
    dest[0x106] = 0u;
    dest[0x107] = 0u;
    return 1;
}
