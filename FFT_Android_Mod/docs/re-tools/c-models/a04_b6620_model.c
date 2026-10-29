#include "a04_b6620_model.h"

extern int a04_zero_path(uint8_t *memory, size_t length, uint32_t selector);
extern int a04_copy_normalize_nonzero(uint8_t *dest, size_t dest_size,
                                      const uint8_t *src, size_t src_size);

int a04_b6620_model(uint8_t *destination, size_t destination_capacity,
                    const uint8_t *source, size_t source_capacity) {
    if (!destination || destination_capacity < 0x108u)
        return 0;
    if (!source)
        return a04_zero_path(destination, destination_capacity, 0u);
    if (source_capacity == 0u)
        return 0;

    /* Fail closed on overlap. Integer address conversion is an explicit
     * platform assumption for the separately built host C test artifact;
     * not a portable, all-address-spaces proof. */
    uintptr_t dst = (uintptr_t)destination;
    uintptr_t src = (uintptr_t)source;
    if (destination_capacity > UINTPTR_MAX - dst ||
            source_capacity > UINTPTR_MAX - src)
        return 0;
    if (dst < src + source_capacity && src < dst + destination_capacity)
        return 0;

    return a04_copy_normalize_nonzero(destination, destination_capacity,
                                     source, source_capacity);
}
