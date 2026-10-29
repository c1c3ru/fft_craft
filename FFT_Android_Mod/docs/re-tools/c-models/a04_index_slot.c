#include <stdint.h>
#include <stddef.h>

/* Contract candidate for original ARM entry 0x000b45d0.
 * Returns an address offset from base, not a host pointer.
 * Caller guarantees that 0x14c + 12*index is readable and aligned.
 * No dereference outside the passed buffer is permitted.
 */
uint32_t a04_index_slot_offset(const uint8_t *bytes, size_t length,
                               uint32_t index) {
    uint64_t offset = UINT64_C(0x14c) + UINT64_C(12) * index;
    if (bytes == NULL || offset + 4 > length || offset > UINT32_MAX)
        return 0;
    /* ARM original reads an aligned little-endian u32. */
    uint32_t word = (uint32_t)bytes[offset] |
                    ((uint32_t)bytes[offset + 1] << 8) |
                    ((uint32_t)bytes[offset + 2] << 16) |
                    ((uint32_t)bytes[offset + 3] << 24);
    return word == UINT32_MAX ? 0 : (uint32_t)offset;
}
