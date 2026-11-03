/* Reconstruction of evt_flag_high() (0x25926c, 72 B) and
 * evt_flag_low() (0x2592b4, 72 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 684.
 *
 * Same shape as evt_flag() (NOTES sec. 671, c-models/t19_evt_flag.c):
 * read (flagIndex, expectedValue) from the event-script stream via
 * evt_get_flgdt, read the actual stored flag value via
 * Wread_eventflag, and conditionally set bit 0x2 on the same VM
 * status word evt_flag/evt_get_flgdt share. The real finding here is
 * WHICH comparison triggers the bit, confirmed by the exact
 * conditional instruction (bge/ble), not assumed from the function
 * names alone:
 *   evt_flag_high: sets the bit when actual <  expected (bge skips the OR)
 *   evt_flag_low:  sets the bit when actual >  expected (ble skips the OR)
 * i.e. "high" checks actual is at or above a floor; "low" checks
 * actual is at or below a ceiling. Both, like evt_flag, return the
 * real flag value unconditionally -- r0 is never reassigned after
 * the Wread_eventflag call on either branch.
 */
#include <stdint.h>

typedef void (*evt_get_flgdt_fn)(int32_t *out1, int32_t *out2);
typedef int32_t (*wread_eventflag_fn)(int32_t index);

int32_t evt_flag_high_model(int32_t *vm_status, evt_get_flgdt_fn evt_get_flgdt,
                             wread_eventflag_fn Wread_eventflag) {
    int32_t flag_index, expected_value;
    evt_get_flgdt(&flag_index, &expected_value);

    int32_t actual_value = Wread_eventflag(flag_index);
    if (actual_value < expected_value) {
        *vm_status |= 0x2;
    }
    return actual_value;
}

int32_t evt_flag_low_model(int32_t *vm_status, evt_get_flgdt_fn evt_get_flgdt,
                            wread_eventflag_fn Wread_eventflag) {
    int32_t flag_index, expected_value;
    evt_get_flgdt(&flag_index, &expected_value);

    int32_t actual_value = Wread_eventflag(flag_index);
    if (actual_value > expected_value) {
        *vm_status |= 0x2;
    }
    return actual_value;
}
