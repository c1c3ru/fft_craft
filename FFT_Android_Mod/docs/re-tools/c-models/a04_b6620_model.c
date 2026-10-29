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
    /* This wrapper is not a drop-in ABI implementation. Only disjoint
     * non-overlapping source/destination buffers are within the contract.
     * The caller must enforce this precondition. */
    return a04_copy_normalize_nonzero(destination, destination_capacity,
                                     source, source_capacity);
}
