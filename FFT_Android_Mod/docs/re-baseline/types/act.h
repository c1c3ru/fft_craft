/* ACT -- minimal partial layout. sizeof(ACT) is NOT known. Source for
 * every field below: set_ct_weapon(ACT*) (0x1caa10, 248 B), read fully
 * in docs/REVERSE_ENGINEERING_NOTES.md section 654 (2026-10-26, prior to
 * this session; consolidated into a shared header for the first time
 * in T08, 2026-10-31).
 */
#ifndef FFT_TYPES_ACT_H
#define FFT_TYPES_ACT_H

#include <stdint.h>

typedef struct ACT {
    uint8_t _unknown_0x00;

    uint8_t byte_0x1;    /* indexes g_itemSubtypeTable to resolve a weapon-class code 0-15 (NOTES sec. 654) */

    int16_t field_0x2;   /* item/weapon id; checked against 0x170 and indexed into g_itemRecordTable (stride 14 B) (NOTES sec. 654) */
    uint8_t _unknown_0x4_0x7[0x04];

    int32_t field_0x8;   /* used directly as a fallback "r5" value in two weapon-class cases (1, 7) (NOTES sec. 654) */
} ACT;

#endif
