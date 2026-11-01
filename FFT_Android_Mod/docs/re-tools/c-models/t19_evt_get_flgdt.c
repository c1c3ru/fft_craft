/* Reconstruction of evt_get_flgdt(int*, int*) (0x2591d4, 80 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 671.
 *
 * Reads two consecutive uint16 tokens from a script/data buffer at
 * the VM context's current read cursor, writes them (zero-extended)
 * to out1 and out2 (both dereferenced), and advances the cursor by 2 -- a "read next two
 * operands" primitive, confirmed real finding: the cursor is stored
 * back to memory TWICE (once after reading the first token, again
 * after the second), not just once at the end; this file reproduces
 * that intermediate store instead of collapsing it into a single
 * final write, since c-models in this project model the real
 * instruction sequence's observable memory effects, not just its net
 * final result.
 *
 * `buf`/`pos` (the VM context struct's +0x8/+0xc fields) are passed
 * in as already-resolved, separate native parameters instead of read
 * out of a byte blob at the real ARM struct's offsets -- same
 * host/ARM pointer-width reasoning as the other c-models in this
 * directory (c-models/t14_boot_framemove.c, etc.): `buf` is a real
 * pointer that does not fit in the 4 bytes the real struct gives it
 * on a 64-bit host.
 */
#include <stdint.h>

void evt_get_flgdt_model(uint16_t *buf, uint16_t *pos, int32_t *out1, int32_t *out2) {
    uint16_t p = *pos;
    uint16_t v1 = buf[p];
    uint16_t p1 = (uint16_t)(p + 1);
    *pos = p1;   /* intermediate store, matches the real instruction order */
    uint16_t v2 = buf[p1];

    *out1 = (int32_t)v1;
    *out2 = (int32_t)v2;

    *pos = (uint16_t)(p + 2);
}
