/* tagSPRT -- partial layout. First field-level evidence recovered for
 * this type. sizeof(tagSPRT) is NOT known beyond 0x18 (the highest
 * offset touched, +0x16/+0x17 for a halfword) -- do not assume any
 * size.
 *
 * Source for every field below: initsprt(tagSPRT*) (0xd6e48) and
 * SetSprt/SetSprt8/SetSprt16/SetSemiTrans/SetShadeTex,
 * docs/REVERSE_ENGINEERING_NOTES.md section 679.
 */
#ifndef FFT_TYPES_TAGSPRT_H
#define FFT_TYPES_TAGSPRT_H

#include <stddef.h>
#include <stdint.h>

typedef struct tagSPRT {
    uint8_t _unknown_0x00_0x03[4];

    /* Primitive type/mode byte: 4 for SetSprt, 3 for both
     * SetSprt8/SetSprt16 -- the two groups are not otherwise
     * distinguished at this offset. */
    uint8_t prim_type; /* +0x04 */

    /* All three zeroed identically by SetSprt/SetSprt8/SetSprt16;
     * individual role not confirmed. */
    uint8_t _zeroed_by_setsprt[3]; /* +0x05 */

    /* RGB color bytes, set to 0x80/0x80/0x80 (mid-gray, no color
     * modulation) by initsprt. Not independently confirmed to be
     * exactly "RGB" beyond this one observed write. */
    uint8_t color_rgb[3]; /* +0x08 */

    /* GPU primitive "code" byte, PS1-style: a fixed base value from
     * SetSprt/SetSprt8/SetSprt16 (0x64/0x74/0x7c, low 2 bits already
     * clear) with bit 1 (SetSemiTrans) and bit 0 (SetShadeTex)
     * layered on top via read-modify-write OR/AND-NOT. Confirmed by
     * address: both flag setters read/write this exact offset, the
     * same one the three SetSprt variants initialize. */
    uint8_t code; /* +0x0b */

    uint16_t field_0x0c; /* 0x200 in initsprt */
    uint16_t field_0x0e; /* 0 in initsprt */
    uint8_t field_0x10;  /* 0 in initsprt */
    uint8_t field_0x11;  /* 0 in initsprt */
    uint16_t field_0x12; /* 0x7c3c in initsprt */
    uint16_t field_0x14; /* 0 in initsprt */
    uint16_t field_0x16; /* 0 in initsprt */
} tagSPRT;

#ifdef __cplusplus
static_assert(offsetof(tagSPRT, prim_type) == 0x04, "prim_type must stay at the confirmed real offset");
static_assert(offsetof(tagSPRT, color_rgb) == 0x08, "color_rgb must stay at the confirmed real offset");
static_assert(offsetof(tagSPRT, code) == 0x0b, "code must stay at the confirmed real offset");
#else
_Static_assert(offsetof(tagSPRT, prim_type) == 0x04, "prim_type must stay at the confirmed real offset");
_Static_assert(offsetof(tagSPRT, color_rgb) == 0x08, "color_rgb must stay at the confirmed real offset");
_Static_assert(offsetof(tagSPRT, code) == 0x0b, "code must stay at the confirmed real offset");
#endif

#endif
