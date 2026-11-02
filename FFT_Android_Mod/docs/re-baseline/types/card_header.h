/* CARD_HEADER -- partial layout. First and only field-level evidence
 * recovered for this type (T08 named it in 2026-10-31 as having "no
 * reliable field evidence" at all -- the fourth and last of the four
 * types it listed; this slice, 2026-11-02, closes it).
 * sizeof(CARD_HEADER) is NOT known beyond 0x100, the highest offset
 * MakeHeader itself touches -- do not assume this is the whole struct.
 *
 * Source for every field below: MakeHeader(int, int, CARD_HEADER*)
 * (0x187264, docs/REVERSE_ENGINEERING_NOTES.md section 678). The two-
 * byte Shift-JIS digit/colon/space sequences were confirmed by
 * empirical probing against the real ELF (distinct, recognizable
 * input values, read back the real output bytes), not by hand-
 * decoding the GCC divide-by-constant codegen -- see section 678 for
 * why.
 */
#ifndef FFT_TYPES_CARD_HEADER_H
#define FFT_TYPES_CARD_HEADER_H

#include <stddef.h>
#include <stdint.h>

typedef struct CARD_HEADER {
    /* Magic signature: 'S','C',0x11,0x01. */
    uint8_t magic[4]; /* +0x00 */

    /* Fixed Shift-JIS template, 22 B, decodes to
     * "ＦＦＴ　ＦＩＬＥ　　　" ("FFT FILE" + 3 full-width spaces).
     * Bytes +0x10..+0x13 (2 of the 3 trailing spaces, relative to
     * this array) are overwritten by MakeHeader with (a0+1) as two
     * full-width digit characters -- NOT clamped. */
    uint8_t title_template[22]; /* +0x04 */

    /* "HH：" -- min(hours, 99) as two full-width Shift-JIS digits
     * plus a full-width colon (0x81, 0x46). Clamp is inclusive
     * (99 itself is already clamped, confirmed by a real `movge`). */
    uint8_t hours_field[6]; /* +0x1a */

    /* "MM：" -- min(minutes, 59), same shape as hours_field. */
    uint8_t minutes_field[6]; /* +0x20 */

    /* "SS␣" -- min(seconds, 59) as two digits, followed by a
     * full-width SPACE (0x81, 0x40), not a colon. */
    uint8_t seconds_field[6]; /* +0x26 */

    /* Verbatim copy of an external event-flag-indexed table entry
     * (stride 20 B; flag index is the literal constant 0x31=49,
     * read directly off the bytes). The table's own layout is not
     * known beyond "20 bytes copied verbatim". */
    uint8_t event_flag_entry[20]; /* +0x2c */

    uint8_t _unknown_0x40_0x43[4];

    /* Explicitly zeroed by MakeHeader (memset), every time. */
    uint8_t reserved_zeroed[28]; /* +0x44 */

    uint8_t _unknown_0x60_0x7f[0x20];

    /* Verbatim copy of (external struct)+0x20, 128 B. That struct's
     * own identity/layout is not known beyond this. */
    uint8_t external_block[0x80]; /* +0x80 */
} CARD_HEADER;

#ifdef __cplusplus
static_assert(offsetof(CARD_HEADER, title_template) == 0x04, "title_template must stay at the confirmed real offset");
static_assert(offsetof(CARD_HEADER, hours_field) == 0x1a, "hours_field must stay at the confirmed real offset");
static_assert(offsetof(CARD_HEADER, minutes_field) == 0x20, "minutes_field must stay at the confirmed real offset");
static_assert(offsetof(CARD_HEADER, seconds_field) == 0x26, "seconds_field must stay at the confirmed real offset");
static_assert(offsetof(CARD_HEADER, event_flag_entry) == 0x2c, "event_flag_entry must stay at the confirmed real offset");
static_assert(offsetof(CARD_HEADER, reserved_zeroed) == 0x44, "reserved_zeroed must stay at the confirmed real offset");
static_assert(offsetof(CARD_HEADER, external_block) == 0x80, "external_block must stay at the confirmed real offset");
#else
_Static_assert(offsetof(CARD_HEADER, title_template) == 0x04, "title_template must stay at the confirmed real offset");
_Static_assert(offsetof(CARD_HEADER, hours_field) == 0x1a, "hours_field must stay at the confirmed real offset");
_Static_assert(offsetof(CARD_HEADER, minutes_field) == 0x20, "minutes_field must stay at the confirmed real offset");
_Static_assert(offsetof(CARD_HEADER, seconds_field) == 0x26, "seconds_field must stay at the confirmed real offset");
_Static_assert(offsetof(CARD_HEADER, event_flag_entry) == 0x2c, "event_flag_entry must stay at the confirmed real offset");
_Static_assert(offsetof(CARD_HEADER, reserved_zeroed) == 0x44, "reserved_zeroed must stay at the confirmed real offset");
_Static_assert(offsetof(CARD_HEADER, external_block) == 0x80, "external_block must stay at the confirmed real offset");
#endif

#endif
