#ifndef FFT_SOUND_PLAYDEF_PREFIX_H
#define FFT_SOUND_PLAYDEF_PREFIX_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Bounded reimplementation of SysSE_PlayDef's 3-instruction A32 forwarding
 * prefix, NOT of the sound playback routine. The target is a real native
 * address in the original ELF, not a callable location in a rebuilt program.
 */
typedef struct FFTSoundPrefix {
    uint32_t next_pc;
    uint32_t r0;
    uint32_t r1;
} FFTSoundPrefix;

/* Returns 1 on success, 0 for a null output pointer. No heap I/O or audio. */
int fft_sound_playdef_prefix(uint32_t input_r0, FFTSoundPrefix *out);

#ifdef __cplusplus
}
#endif

#endif /* FFT_SOUND_PLAYDEF_PREFIX_H */
