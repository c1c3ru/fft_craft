#ifndef FFT_A04_B6620_MODEL_H
#define FFT_A04_B6620_MODEL_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

/* Independent, bounds-checked C model for original ARM 0x000b6620.
 * source == NULL selects original R1 == 0; nonnull selects R1 != 0.
 * Returns 1 on accepted inputs, 0 on failed preconditions.
 * On failure, does not modify destination (unlike unchecked original strcpy).
 * On success the original ARM returned the destination pointer in R0;
 * this safety wrapper returns a status instead and documents that difference.
 * No overlapping buffers; no Android libc executed.
 */
int a04_b6620_model(uint8_t *destination, size_t destination_capacity,
                    const uint8_t *source, size_t source_capacity);

#ifdef __cplusplus
}
#endif
#endif
