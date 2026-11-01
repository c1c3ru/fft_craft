/* Reconstruction of pagenext_cursor(PAGEWININFO*) (0x270b04, 88 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 669.
 *
 * PAGEWININFO already has a confirmed role (NOTES sec. 381): a generic
 * paginated-window framework, and this exact function is already
 * named there as the "next page" cursor navigation callee of
 * pagewin_main. The three struct offsets this function itself touches
 * (+0x38 index, +0x50 "max page", +0x54 "current page") are read
 * directly off the real bytes here, not carried over from any
 * existing PAGEWININFO field table -- none exists yet.
 *
 * `cursor_flags_array` is CONFIRMED to be the exact same global on
 * both branches of the real function (same GOT slot 0x3479a4,
 * resolved by hand, both branches reuse it), base address 0x67e390,
 * stride 0x24 (36 B) per entry, indexed by PAGEWININFO+0x38. Only the
 * first 4 bytes of each entry are touched here; the other 32 bytes
 * are opaque to this function and not modeled.
 *
 * Passed in as a direct native pointer, already resolved, instead of
 * reconstructing the GOT->address->value chain inside this file --
 * generic PIC boilerplate, not this function's own logic, same
 * approach as c-models/t14_boot_framemove.c and t25_csoundifsl_stop.c.
 */
#include <stdint.h>
#include <string.h>

#define PAGENEXT_CURSOR_ENTRY_STRIDE 0x24
#define PAGENEXT_CURSOR_FLAG_BIT 0x10u

void pagenext_cursor_model(void *info, uint8_t *cursor_flags_array) {
    uint8_t *p = (uint8_t *)info;
    int32_t max_page, cur_page, index;
    memcpy(&max_page, p + 0x50, 4);
    memcpy(&cur_page, p + 0x54, 4);
    memcpy(&index, p + 0x38, 4);

    uint8_t *entry = cursor_flags_array + (uint32_t)index * PAGENEXT_CURSOR_ENTRY_STRIDE;
    uint32_t flags;
    memcpy(&flags, entry, 4);
    if (cur_page >= max_page) {
        /* On (or past) the last page: mark "no next page". */
        flags |= PAGENEXT_CURSOR_FLAG_BIT;
    } else {
        flags &= ~PAGENEXT_CURSOR_FLAG_BIT;
    }
    memcpy(entry, &flags, 4);
}
