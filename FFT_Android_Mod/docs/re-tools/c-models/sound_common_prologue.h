#ifndef FFT_SOUND_COMMON_PROLOGUE_H
#define FFT_SOUND_COMMON_PROLOGUE_H

#include <stdint.h>

typedef struct FFTSoundCommonPrologue {
    uint32_t next_pc;
    uint32_t sp;
    uint32_t r0;
    uint32_t r1;
    uint32_t r3;
    uint32_t r5;
    uint32_t r6;
    uint32_t saved[8];
} FFTSoundCommonPrologue;

/* Models ONLY five instructions of the original 0x2b2b7c A32 entry.
 * The C model is not an audio library or a replacement for the whole function.
 * Call with original r1 argument, original SP, original PC literal word, and
 * original register values (r4,r5,r6,r7,r8,r9,r10,lr) before the PUSH.
 * Returns 0 for NULL pointers and 1 for success.
 */
int fft_sound_common_prologue(uint32_t arg_r1, uint32_t sp, uint32_t literal_r3,
                              const uint32_t before_saved[8],
                              FFTSoundCommonPrologue *out);
#endif
