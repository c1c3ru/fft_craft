/* Reconstruction of iOSUnitListWinOnOff(int) (0x15ef7c), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 666.
 *
 * The real ARM body does NOT call its "other path" via bl: it pops its
 * own frame and does a plain branch (a genuine tail call) into a
 * different function (0x15ee2c), whose return value becomes this
 * function's own return value. That is modeled here as a direct call
 * to a function pointer with the same effect, since C has no tail-call
 * keyword to force -- the differential test checks the OBSERVABLE
 * effect (return value, globals untouched), not the calling convention
 * itself.
 *
 * iOSdisp_personalWinPosGet and the tail-call target are passed in as
 * function pointers: this file makes no claim about their behavior.
 */
#include <stdint.h>

typedef int32_t (*pos_get_fn)(void);
typedef int32_t (*other_path_fn)(void);

int32_t iOSUnitListWinOnOff_model(
    int32_t off_flag,
    int32_t *window_active,
    int32_t *window_x_offset,
    pos_get_fn iOSdisp_personalWinPosGet,
    other_path_fn other_path) {
    if (off_flag != 0) {
        return other_path();
    }
    *window_active = 1;
    int32_t pos_flag = iOSdisp_personalWinPosGet();
    *window_x_offset = (pos_flag == 0) ? -0x78 : 0x78;
    /* r0 is never reassigned after the call in the real body -- the
     * return value IS pos_flag, confirmed by execution, not assumed. */
    return pos_flag;
}
