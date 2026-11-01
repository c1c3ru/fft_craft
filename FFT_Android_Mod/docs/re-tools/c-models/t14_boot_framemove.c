/* Reconstruction of Boot_FrameMove() (0x2b3590, 128 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 668.
 *
 * The three GOT-indirected globals this function reads are taken as
 * already-resolved values (flag_a, thread_this, gl_this) instead of
 * replaying the literal-pool -> GOT-slot -> global-address -> value
 * chain inside this file: that chain is generic PIC boilerplate, not
 * this function's own logic, and the real/model pointer-width
 * mismatch it would otherwise introduce is the same one already
 * sidestepped in c-models/t25_csoundifsl_stop.c and
 * c-models/t24_mdl0016.c's `g` parameter.
 *
 * Real finding, cross-referenced against Boot_Init() (NOTES sec. 650,
 * already read): the global this function's FIRST guard reads is the
 * exact same GOT slot (0x347cb4, resolving to the same .bss address
 * 0x19db208) that Boot_Init() writes 0 to only on its async-load path
 * ("*g_someBootFlag = 0" right after CTHREAD::Register). Confirmed by
 * independently resolving both functions' GOT-relative addressing by
 * hand, not by name similarity. This function's own exact semantics
 * for the flag (and for the other two globals -- the cached CTHREAD*
 * and CEGL2_IF* singletons) are not otherwise confirmed, so they are
 * NOT given invented names here.
 *
 * CTHREAD::Sync, CEGL2_IF::ClearBackdrop, onGotoNextMode are passed in
 * as function pointers: this file makes no claim about their own
 * behavior. The `1`/`0`/`0` SetPlayState-style second/third/fourth
 * ClearBackdrop args and the `3` passed to onGotoNextMode (confirmed
 * elsewhere, NOTES sec. 640, to mean "transition to Logo") are read
 * directly off the real bytes.
 */
#include <stdint.h>

typedef int32_t (*cthread_sync_fn)(void *this_ptr);
typedef void (*clear_backdrop_fn)(void *this_ptr, float r, float g, float b);
typedef void (*goto_next_mode_fn)(int32_t mode);

int32_t Boot_FrameMove_model(
    int32_t flag_a, void *thread_this, cthread_sync_fn CTHREAD_Sync,
    void *gl_this, clear_backdrop_fn ClearBackdrop, goto_next_mode_fn onGotoNextMode) {
    if (flag_a != 0) {
        return 0;
    }

    int32_t sync_result = CTHREAD_Sync(thread_this);
    if (sync_result != 0) {
        if (sync_result == 1) {
            return -1;
        }
        return 0;
    }

    ClearBackdrop(gl_this, 0.0f, 0.0f, 0.0f);
    onGotoNextMode(3 /* Logo, confirmed NOTES sec. 640 */);
    return 1;
}
