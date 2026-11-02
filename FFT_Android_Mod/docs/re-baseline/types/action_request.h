/* ActionRequest -- partial layout. First field-level evidence
 * recovered for this type (T08 named it in 2026-10-31 as having "no
 * reliable field evidence" at all; this slice, 2026-11-02, closes
 * that for exactly one field, corroborated from two independent
 * reads). sizeof(ActionRequest) is NOT known -- do not assume any
 * size; this header only places the 4 bytes actually read.
 *
 * Sources for the field below:
 *   - iOSCurSameProcs(ActionRequest*) (0x15da34,
 *     docs/REVERSE_ENGINEERING_NOTES.md section 676): reads this
 *     field, compares to 0xfe, conditionally writes 7.
 *   - AI_DIFFICULTY_RESEARCH.md section 14.4 (BattleRoutine's
 *     finalize block, a separate research effort, NOT this RE loop):
 *     observed writing 0 or 2 to the exact same offset (the function
 *     writes directly to *out, i.e. offset 0 of its ActionRequest*
 *     out-parameter).
 * Neither source assumed the other's meaning; the offset match was
 * confirmed independently by each.
 */
#ifndef FFT_TYPES_ACTION_REQUEST_H
#define FFT_TYPES_ACTION_REQUEST_H

#include <stddef.h>
#include <stdint.h>

typedef struct ActionRequest {
    /* Request/status code. Observed values: 0, 2 (written by
     * BattleRoutine's finalize block, AI research sec. 14.4); 0xfe
     * (a "pending" sentinel checked by iOSCurSameProcs, NOTES
     * sec. 676); 7 (written by iOSCurSameProcs on success). No
     * semantic name is claimed for any of these beyond what is
     * directly observed -- this is a code, not confirmed to be a
     * specific named enum. */
    int32_t status_code_0x00;
} ActionRequest;

#ifdef __cplusplus
static_assert(offsetof(ActionRequest, status_code_0x00) == 0x00,
              "status_code_0x00 must stay at the confirmed real offset");
#else
_Static_assert(offsetof(ActionRequest, status_code_0x00) == 0x00,
               "status_code_0x00 must stay at the confirmed real offset");
#endif

#endif
