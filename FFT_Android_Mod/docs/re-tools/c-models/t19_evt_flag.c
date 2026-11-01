/* Reconstruction of evt_flag() (0x259224, 72 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 671.
 *
 * Real finding kept faithfully: this is NOT a pure predicate. It
 * reads two operands from the event-script stream (flagIndex,
 * expectedValue, via evt_get_flgdt), reads the ACTUAL stored flag
 * value (Wread_eventflag(flagIndex)), and returns that actual value
 * unconditionally -- but if it does not match the script's expected
 * value, it ALSO sets bit 0x2 on a VM status word. r0 is never
 * reassigned after the Wread_eventflag call on either branch, so
 * the return value is the same real flag value regardless of the
 * match/mismatch outcome -- confirmed by disassembly, not assumed.
 *
 * Cross-referenced by address (not by name): the VM status word this
 * function writes (+0x0) lives in the EXACT SAME global struct as
 * evt_get_flgdt's buf/pos fields (+0x8/+0xc) -- same GOT slot
 * (0x347a80), same resolved base (0x67b35c). This is a previously
 * unnamed global; no claim is made that it is the same context struct
 * used by event_call/worldmap_call (T18), which take their script
 * pointer/pc as explicit arguments, not through this global.
 *
 * evt_get_flgdt and Wread_eventflag are passed in as function
 * pointers: this file makes no claim about Wread_eventflag's own
 * behavior (not read in this slice).
 */
#include <stdint.h>

typedef void (*evt_get_flgdt_fn)(int32_t *out1, int32_t *out2);
typedef int32_t (*wread_eventflag_fn)(int32_t index);

int32_t evt_flag_model(int32_t *vm_status, evt_get_flgdt_fn evt_get_flgdt,
                        wread_eventflag_fn Wread_eventflag) {
    int32_t flag_index, expected_value;
    evt_get_flgdt(&flag_index, &expected_value);

    int32_t actual_value = Wread_eventflag(flag_index);
    if (actual_value != expected_value) {
        *vm_status |= 0x2;
    }
    return actual_value;
}
