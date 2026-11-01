/* Reconstruction of pspFftSave (0x2899a0) and pspFftDelete (0x289c1c),
 * per docs/REVERSE_ENGINEERING_NOTES.md sections 641, 651, 661 (the
 * last one corrects section 641's claim that state never changes
 * during state==1 processing -- verified by executing the real ELF
 * under Unicorn, see test_t22_save_state_machine.py).
 *
 * The two functions share the external xpLibapiSave{Start,Check,End}
 * primitive and the SAME g_fftSaveState global in the real binary, but
 * their state==1 handling is genuinely different (confirmed by direct
 * execution, not assumed from the shared primitive): pspFftSave always
 * resets state to 0 after processing a check result; pspFftDelete sets
 * state to 2 for most results and leaves it at 1 for exactly one
 * result value. They are modeled as two separate functions, not one
 * shared helper, because collapsing them would silently paper over
 * that real difference.
 *
 * External dependencies are passed in as function pointers: this file
 * makes no claim about xpLibapiSave{Start,Check,End}'s own behavior,
 * only about the state machine built on top of them.
 */
#include <stdint.h>

typedef int32_t (*save_start_fn)(int32_t op);
typedef int32_t (*save_check_fn)(void);
typedef int32_t (*save_end_fn)(void);

static int32_t finalize(int32_t *state, int32_t *cached_arg, int32_t *out_param,
                         save_end_fn end) {
    end();
    *state = 0;
    int32_t cached = *cached_arg;
    *out_param = cached;
    return cached >> 31;  /* matches the real `asr r0, r0, #0x1f` exactly */
}

int32_t pspFftSave_model(int32_t *state, int32_t *cached_arg, int32_t *out_param,
                          save_start_fn start, save_check_fn check, save_end_fn end) {
    if (*state == 0) {
        start(1);
        *state = 1;
        *cached_arg = 0;
        return 1;
    }
    if (*state == 1) {
        int32_t result = check();
        int32_t idx = result + 0xd;
        if (idx != 13 && idx != 14 && idx != 15) {
            *cached_arg = result;
        }
        *state = 0;   /* unconditional, for every idx -- NOTES sec. 651 */
        return 1;
    }
    return finalize(state, cached_arg, out_param, end);
}

int32_t pspFftDelete_model(int32_t *state, int32_t *cached_arg, int32_t *out_param,
                            save_start_fn start, save_check_fn check, save_end_fn end) {
    if (*state == 0) {
        start(2);
        *state = 1;
        *cached_arg = 0;
        return 1;
    }
    if (*state == 1) {
        int32_t result = check();
        int32_t idx = result + 0xd;
        if (idx == 13) {
            return 1;                 /* state stays 1: nothing written -- NOTES sec. 661 */
        }
        if (idx == 14) {
            *state = 2;               /* state changes on THIS call -- NOTES sec. 661 */
            return result;             /* == 1, by construction of idx==14 */
        }
        *cached_arg = result;         /* idx in [0,12] or 15, or out of [0,15] */
        *state = 2;
        return 1;
    }
    return finalize(state, cached_arg, out_param, end);
}
