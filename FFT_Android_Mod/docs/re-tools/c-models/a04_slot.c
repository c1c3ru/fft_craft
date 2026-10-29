#include <stdint.h>
#include <stddef.h>

/* Independent candidate for original A32 0x000b45d0.
 * Returns an offset rather than dereferencing a target-process pointer.
 * Only mapped, aligned, bounded inputs belong to the differential scope.
 */
uint32_t a04_slot_offset(const uint8_t *bytes, size_t size, uint32_t index) {
    uint64_t offset = UINT64_C(0x14c) + UINT64_C(12) * index;
    if (!bytes || offset > UINT32_MAX || offset + 4 > size)
        return 0;
    uint32_t value = (uint32_t)bytes[offset]
                   | (uint32_t)bytes[offset + 1] << 8
                   | (uint32_t)bytes[offset + 2] << 16
                   | (uint32_t)bytes[offset + 3] << 24;
    return value == UINT32_MAX ? 0 : (uint32_t)offset;
}
