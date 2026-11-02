/* Reconstruction of initsprt(tagSPRT*) (0xd6e48, 100 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 679.
 *
 * Composes SetSprt and SetShadeTex (both real calls, `bl`) with a
 * block of direct field writes, then ends in a genuine ARM tail call
 * (`b`, not `bl`) into SetSemiTrans(sprt, 1) -- the seventh tail call
 * confirmed this session. SetSprt/SetShadeTex/SetSemiTrans are
 * independently differential-tested in
 * c-models/t23_sprt_setters.c; here they are opaque function
 * pointers, this file makes no further claim about them.
 */
#include <stdint.h>

typedef void (*set_sprt_fn)(void *sprt);
typedef void (*set_shade_tex_fn)(void *sprt, int32_t flag);
typedef void (*set_semi_trans_fn)(void *sprt, int32_t flag);

void initsprt_model(
    uint8_t *sprt, set_sprt_fn SetSprt, set_shade_tex_fn SetShadeTex,
    set_semi_trans_fn SetSemiTrans) {
    SetSprt(sprt);
    SetShadeTex(sprt, 1);

    sprt[0x8] = 0x80;
    sprt[0x9] = 0x80;
    sprt[0xa] = 0x80;
    sprt[0x10] = 0;
    sprt[0x11] = 0;

    uint16_t h_0xc = 0x200;
    uint16_t h_0x12 = 0x7c3c;
    uint16_t zero16 = 0;
    sprt[0xc] = (uint8_t)(h_0xc & 0xff);
    sprt[0xd] = (uint8_t)(h_0xc >> 8);
    sprt[0x12] = (uint8_t)(h_0x12 & 0xff);
    sprt[0x13] = (uint8_t)(h_0x12 >> 8);
    sprt[0x14] = (uint8_t)(zero16 & 0xff);
    sprt[0x15] = (uint8_t)(zero16 >> 8);
    sprt[0x16] = (uint8_t)(zero16 & 0xff);
    sprt[0x17] = (uint8_t)(zero16 >> 8);
    sprt[0xe] = (uint8_t)(zero16 & 0xff);
    sprt[0xf] = (uint8_t)(zero16 >> 8);

    SetSemiTrans(sprt, 1);
}
