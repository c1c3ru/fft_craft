/* FFT_SAVE_DATA -- partial layout. First field-level evidence
 * recovered for this type (T08 named it in 2026-10-31 as having "no
 * reliable field evidence" at all; this slice, 2026-11-02, closes
 * that for exactly one field). sizeof(FFT_SAVE_DATA) is NOT known --
 * do not assume any size; this header only places the 32 bytes
 * actually read. ~28 other fields are used by ConvTutoData/
 * pspFftSave/pspFftLoad (all read_structural, batch lot 75, §557) but
 * were NOT cross-checked against this field or individually
 * offset-confirmed; do not assume they don't overlap +0x60.
 *
 * Source for the field below: pspSaveDataMissionRateSave/Load
 * (0x289ba8/0x289b8c, docs/REVERSE_ENGINEERING_NOTES.md section 675,
 * read directly by disassembly and confirmed by differential test
 * against the real ELF in both copy directions).
 */
#ifndef FFT_TYPES_FFT_SAVE_DATA_H
#define FFT_TYPES_FFT_SAVE_DATA_H

#include <stddef.h>
#include <stdint.h>

typedef struct FFT_SAVE_DATA {
    uint8_t _unknown_0x00_0x5f[0x60];

    /* "Mission rate" data blob: copied verbatim to/from the live
     * mission buffer returned by pspNetEntranceDataMissionBufferGet()
     * (already read_full elsewhere) via a real memcpy, confirmed by
     * disassembly of both pspSaveDataMissionRateSave (dest=this field)
     * and pspSaveDataMissionRateLoad (src=this field) -- the two
     * directions are exact opposites, not independently guessed. No
     * further internal structure of these 32 bytes is known. */
    uint8_t mission_rate_blob_0x60[0x20];
} FFT_SAVE_DATA;

#ifdef __cplusplus
static_assert(offsetof(FFT_SAVE_DATA, mission_rate_blob_0x60) == 0x60,
              "mission_rate_blob_0x60 must stay at the confirmed real offset");
#else
_Static_assert(offsetof(FFT_SAVE_DATA, mission_rate_blob_0x60) == 0x60,
               "mission_rate_blob_0x60 must stay at the confirmed real offset");
#endif

#endif
