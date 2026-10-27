/*
 * FFT Craft — reconstructed A32 sound dispatcher prefix, NOT a full sound API.
 *
 * Source bytes from original ELF SHA256:
 * bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc
 *   0x2b2cf8: MOV R1,R0
 *   0x2b2cfc: MOV R0,#0
 *   0x2b2d00: B   0x2b2b7c
 *
 * Preconditions: ARM A32 normal state, valid input in R0.
 * Postconditions at boundary BEFORE executing 0x2b2b7c: R0=0, R1=input,
 * PC=0x2b2b7c; all remaining general registers/NZCV unchanged; no data
 * accesses in this bounded prefix. No claim about the eventual audio effect.
 */
#include <stdint.h>
#include <stddef.h>

typedef struct {
    uint32_t next_pc;
    uint32_t r0;
    uint32_t r1;
} FFTSoundPrefix;

int fft_sound_playdef_prefix(uint32_t input_r0, FFTSoundPrefix *out)
{
    if (out == NULL) {
        return 0;
    }
    out->next_pc = UINT32_C(0x2b2b7c);
    out->r0 = UINT32_C(0);
    out->r1 = input_r0;
    return 1;
}
