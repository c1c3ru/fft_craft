/* Reconstruction of evt_flagset() (0x2592fc, 40 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 684.
 *
 * Reads (flagIndex, value) from the event-script stream via
 * evt_get_flgdt (NOTES sec. 671, independently differential-tested
 * in test_t19_evt_get_flgdt.py) and writes it through directly via
 * Wwrite_eventflag -- no condition, no VM status bit, unlike
 * evt_flag/evt_flag_high/evt_flag_low. Confirmed by the absence of
 * any comparison in the real bytes: this is a pure two-argument
 * pass-through tail of the same operand-reading primitive.
 */
#include <stdint.h>

typedef void (*evt_get_flgdt_fn)(int32_t *out1, int32_t *out2);
typedef void (*wwrite_eventflag_fn)(int32_t index, int32_t value);

void evt_flagset_model(evt_get_flgdt_fn evt_get_flgdt, wwrite_eventflag_fn Wwrite_eventflag) {
    int32_t flag_index, value;
    evt_get_flgdt(&flag_index, &value);
    Wwrite_eventflag(flag_index, value);
}
