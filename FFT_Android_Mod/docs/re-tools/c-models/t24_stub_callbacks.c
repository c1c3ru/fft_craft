/* Reconstruction of 5 functions from the _EffectTCB/_Object callback
 * cluster, per docs/REVERSE_ENGINEERING_NOTES.md section 688:
 *
 *   dmyFnc(_EffectTCB*)                              (0x21c214, 24 B)
 *   CreateObjectWithTableWithParentData(short,int,int,int,_Object*)
 *                                                      (0x228c44, 24 B)
 *   system_error(int, int)                            (0x20c5d0, 4 B)
 *   objectLG2(_EffectTCB*, _Object*)                  (0x225a60, 4 B)
 *   dmyFnc2(_EffectTCB*, _Object*)                    (0x225a64, 4 B)
 *
 * Real finding, confirmed by bytes, not by name: `dmyFnc` and
 * `CreateObjectWithTableWithParentData` are NOT bare `bx lr` like
 * `objectLG2`/`dmyFnc2` -- both ignore every one of their real
 * parameters and instead call system_error() with a fixed category
 * (1) and a distinct fixed code (0x22 for dmyFnc, 0x50 for
 * CreateObjectWithTableWithParentData) before returning 0. But
 * system_error() ITSELF is a bare `bx lr` that also ignores both of
 * its arguments -- so the whole "report an error" mechanism is
 * currently inert in this build. The net observable effect of all
 * five functions is therefore the same (do nothing, optionally
 * return 0), but by two genuinely different code shapes: a real
 * "placeholder that reports an error" category, confirmed distinct
 * from a true no-op category, even though both are presently
 * equivalent in practice.
 */
#include <stdint.h>

typedef void (*system_error_fn)(int32_t category, int32_t code);

void system_error_model(int32_t category, int32_t code) {
    (void)category;
    (void)code;
}

int32_t dmyFnc_model(void *effect_tcb, system_error_fn system_error) {
    (void)effect_tcb;
    system_error(1, 0x22);
    return 0;
}

int32_t CreateObjectWithTableWithParentData_model(
    int16_t a0, int32_t a1, int32_t a2, int32_t a3, void *object,
    system_error_fn system_error) {
    (void)a0;
    (void)a1;
    (void)a2;
    (void)a3;
    (void)object;
    system_error(1, 0x50);
    return 0;
}

void objectLG2_model(void *effect_tcb, void *object) {
    (void)effect_tcb;
    (void)object;
}

void dmyFnc2_model(void *effect_tcb, void *object) {
    (void)effect_tcb;
    (void)object;
}
