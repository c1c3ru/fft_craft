/* EDATA -- partial layout. First field-level evidence recovered for
 * this type (T08, 2026-10-31); docs/REVERSE_ENGINEERING_NOTES.md section
 * 72 names it "template de dados de inimigo" (enemy template data) from
 * usage context only, and explicitly states the layout was not mapped
 * field by field before this pass. sizeof(EDATA) is NOT known -- do not
 * assume any size; this header only places the 5 bytes actually read.
 *
 * Source for every field below: copy_entry_coord(BWORK*, EDATA*)
 * (0x1d9ee0, 120 B, 100% structural coverage, read directly in T08).
 */
#ifndef FFT_TYPES_EDATA_H
#define FFT_TYPES_EDATA_H

#include <stdint.h>

typedef struct EDATA {
    uint8_t _unknown_0x00_0x18[0x19];

    uint8_t byte_0x19;   /* copied verbatim into BWORK+0x4f by copy_entry_coord */
    uint8_t byte_0x1a;   /* copied verbatim into BWORK+0x50 by copy_entry_coord */
    /* +0x1b: source byte for BWORK+0x51's bit-packed field (see bwork.h):
     *   bit 7, bits 4-5, and bits 0-1 of this byte are copied into
     *   BWORK+0x51; bits 2-3 and bit 6 of EDATA+0x1b are NOT used. */
    uint8_t byte_0x1b;
    uint8_t _unknown_0x1c_0x1d[0x02];

    uint8_t byte_0x1e;   /* zero-extended into BWORK's 16-bit coord_x_0x184 -- likely a map-tile X coordinate */
    uint8_t byte_0x1f;   /* copied verbatim into BWORK+0x186 (coord_y) -- likely a map-tile Y coordinate */
} EDATA;

#endif
