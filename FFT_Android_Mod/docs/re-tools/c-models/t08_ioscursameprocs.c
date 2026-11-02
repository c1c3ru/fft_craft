/* Reconstruction of iOSCurSameProcs(ActionRequest*) (0x15da34, 44 B),
 * per docs/REVERSE_ENGINEERING_NOTES.md section 676.
 *
 * Second confirmed field for ActionRequest (the first being its role
 * as BattleRoutine's output parameter, AI_DIFFICULTY_RESEARCH.md
 * section 14.4: "grava um codigo em *out, valores 0 ou 2
 * observados" -- a write to the exact same offset, +0x0, this
 * function reads and conditionally rewrites). Cross-referenced by
 * address/offset, not by name: AI research observed 0/2 written
 * there by BattleRoutine's finalize path; this function separately
 * confirms 0xfe (a "pending" sentinel) is compared there and 7 is
 * written on success -- same field, independently corroborating that
 * ActionRequest+0x0 is a request/status code, widening the known
 * value set, not a single fixed enum guessed from one site alone.
 *
 * iOSCurSameOK() (0x15d748, 272 B, read_structural) is NOT read in
 * this slice -- passed in as an opaque function pointer. This file
 * makes no claim about its own behavior beyond its boolean-like
 * return already used here as a gate.
 */
#include <stdint.h>

typedef int32_t (*cur_same_ok_fn)(void);

void iOSCurSameProcs_model(int32_t *action_request, cur_same_ok_fn iOSCurSameOK) {
    if (*action_request != 0xfe) {
        return;
    }
    if (iOSCurSameOK() != 0) {
        *action_request = 7;
    }
}
