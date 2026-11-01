/* BWORK -- partial layout recovered from field-access evidence.
 * Source: docs/REVERSE_ENGINEERING_NOTES.md sections 349, 355, 653, 662,
 * and copy_entry_coord (0x1d9ee0, T08) / setskillresult_caster
 * (0x1ce950, T16 slice) read directly in this project.
 * sizeof(BWORK) confirmed = 0x1e6 (486) bytes, from set_status_all's
 * r8 = idx*0x1e6 indexing of a global BWORK[] array (section 349).
 *
 * Every named field below has a cited source in its comment. Unknown
 * gaps are explicit char[] padding, not guessed fields -- offsets are
 * declared in strict ascending order so the gap sizes below are also a
 * literal map of "what is NOT yet recovered". Do not add a field here
 * without equivalent evidence; do not reorder fields to "look complete".
 *
 * NOT placed here: a *different*, request-like struct read in section
 * 355 via a separate GOT-resolved global (not BWORK itself), with small
 * fields at +0x1d/0x1e/0x1f/0x21/0x22/0x24 relative to ITS OWN base --
 * see T08_TYPE_RECOVERY.md section on the "status-change request"
 * candidate. Do not confuse those offsets with BWORK's own layout.
 */
#ifndef FFT_TYPES_BWORK_H
#define FFT_TYPES_BWORK_H

#include <stdint.h>

#define SIZEOF_BWORK 0x1e6  /* 486 bytes; confirmed, see header comment */

typedef struct BWORK {
    uint8_t _unknown_0x00;
    uint8_t caster_ready_flag_0x1;           /* 0xff = "not castable" (setskillresult_caster returns -1); any other value proceeds (NOTES sec. 662) */
    uint8_t _unknown_0x02_0x22[0x21];        /* not mapped in this pass */

    uint8_t net_sync_pending_flag_0x23;      /* bit 0x40: network sync pending flag (NOTES sec. 349) */
    uint8_t _unknown_0x24_0x2d[0x0a];

    uint8_t guard_flag_0x2e;                 /* defender/guard flag, cleared by status 0x13 (NOTES sec. 349) */
    uint8_t _unknown_0x2f;

    uint8_t charge_time_0x30;                /* charge-time/CT; zeroed by sleep/stop-type status (NOTES sec. 349) */
    uint8_t _unknown_0x31_0x4e[0x1e];

    uint8_t coord_flag_byte_0x4f;            /* copy of EDATA+0x19 (copy_entry_coord, T08) */
    uint8_t coord_flag_byte_0x50;            /* copy of EDATA+0x1a (copy_entry_coord, T08) */
    /* +0x51: bit-packed from EDATA+0x1b by copy_entry_coord (T08):
     *   bit 7    = EDATA+0x1b bit 7
     *   bits 4-5 = EDATA+0x1b bits 4-5
     *   bit 6    = preserved from BWORK's own prior value (not from EDATA)
     *   bits 2-3 = cleared to 0 by copy_entry_coord
     *   bits 0-1 = EDATA+0x1b bits 0-1 */
    uint8_t packed_flags_0x51;
    uint8_t _unknown_0x52_0x56[0x05];

    uint8_t status_category_byte_0x57;       /* used in change_status_adjust's 5-iteration loop (NOTES sec. 355) */
    uint8_t _unknown_0x58_0x5b[0x04];

    uint8_t status_category_byte_0x5c;       /* used in change_status_adjust's 5-iteration loop (NOTES sec. 355) */
    uint8_t _unknown_0x5d_0x60[0x04];

    /* +0x61: multi-purpose status byte, two *overlapping concerns*
     * documented separately -- flagged here for reconciliation, NOT
     * resolved by this pass:
     *   - NOTES sec. 349: bits 0x0D (0,2,3) / 0x20 (5) = "incapacitated"
     *     category, checked by adjust_input_flag
     *   - NOTES sec. 653 (set_casting_status): bits 0-3 = 4-bit
     *     "casting stage" mask, diffed bit-by-bit to drive
     *     _changeAnimationStatus_ */
    uint8_t status_byte_0x61;

    uint8_t network_neighbor_bytes_0x62_0x63[2]; /* referenced as a pair near the 0x61/0x1dc flags (NOTES sec. 355); not individually typed */
    uint8_t _unknown_0x64_0x17c[0x119];

    uint8_t ui_dirty_flag_0x17d;             /* "UI dirty" flag (NOTES sec. 349); also set from byte_0x1ad or forced 0xff by set_casting_status (NOTES sec. 653) */
    uint8_t _unknown_0x17e_0x183[0x06];

    uint16_t coord_x_0x184;                  /* zero-extended from EDATA+0x1e byte by copy_entry_coord (T08) -- "entry coord" X */
    uint8_t coord_y_0x186;                   /* copy of EDATA+0x1f by copy_entry_coord (T08) -- "entry coord" Y */
    uint8_t _unknown_0x187_0x1ab[0x25];

    uint8_t byte_0x1ac;                      /* origByte1ac in set_casting_status (NOTES sec. 653); feeds `dir` into _changeAnimationStatus_ */
    uint8_t byte_0x1ad;                      /* copied into ui_dirty_flag_0x17d on one set_casting_status path (NOTES sec. 653) */
    /* +0x1ae..+0x1db (46 B): "skill result" sub-struct, reset by
     * setskillresult_caster via copy_struct_data from a global default
     * template before calling setskillresult(casterId) (NOTES sec. 662).
     * Only 2 of the 46 bytes are understood: */
    uint8_t skill_result_kind_0x1ae;         /* if 0 after setskillresult() runs, forced to a fallback (NOTES sec. 662) */
    uint8_t _unknown_0x1af;
    uint8_t skill_result_fallback_0x1b0;     /* set to 8 when skill_result_kind_0x1ae == 0 (NOTES sec. 662) */
    uint8_t _unknown_0x1b1_0x1db[0x2b];

    uint8_t status_secondary_0x1dc;          /* tested against mask 0xa in change_status_adjust (NOTES sec. 349/355) */
    uint8_t status_secondary_0x1dd;          /* secondary status byte (NOTES sec. 349) */
    uint8_t status_secondary_0x1de;          /* secondary status byte (NOTES sec. 349) */
    uint8_t status_primary_bitfield_0x1df;   /* primary status bitfield, ~40 status types, tested in a loop 0..0x27 (NOTES sec. 349) */

    uint8_t _unknown_0x1e0_0x1e5[0x06];      /* tail padding to sizeof(BWORK) */
} BWORK;

#endif
