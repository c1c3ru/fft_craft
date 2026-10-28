/*
 * Scoped reconstruction of the first FIVE A32 instructions at 0x2b2b7c.
 * Original ELF SHA-256:
 * bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc
 *
 * 0x2b2b7c PUSH {r4,r5,r6,r7,r8,r9,r10,lr} (32 bytes)
 * 0x2b2b80 LDR r3,[pc,#0x160]         (from original 0x2b2ce8)
 * 0x2b2b84 SUB sp,sp,#0x20           (another 32 bytes)
 * 0x2b2b88 MOV r6,r0                 (r0=0 from previous prefix)
 * 0x2b2b8c MOV r5,r1                 (r1=caller argument)
 * STOP before 0x2b2b90 LDR r0,[pc,r3].
 *
 * C describes the resulting register/stack words, not real audio or
 * out-of-bounds memory accesses. Actual ARM register and memory effects
 * are independently checked in Unicorn on the original ELF.
 */
#include <stddef.h>
#include "sound_common_prologue.h"

int fft_sound_common_prologue(uint32_t arg_r1, uint32_t sp, uint32_t literal_r3,
                              const uint32_t before_saved[8],
                              FFTSoundCommonPrologue *out)
{
    unsigned i;
    if (before_saved == NULL || out == NULL) {
        return 0;
    }
    out->next_pc = UINT32_C(0x2b2b90);
    out->sp = sp - UINT32_C(64);
    out->r0 = UINT32_C(0);
    out->r1 = arg_r1;
    out->r3 = literal_r3;
    out->r5 = arg_r1;
    out->r6 = UINT32_C(0);
    for (i = 0; i != 8U; ++i) {
        out->saved[i] = before_saved[i];
    }
    return 1;
}
