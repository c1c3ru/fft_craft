/* Reconstruction of wldlop_chk() (0x25f63c, 88 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 687.
 *
 * Syncs a destination flags word from a source flags word (bit 1 of
 * each, mask 0x2), but if the sync would CLEAR that bit in the
 * destination (src bit unset, dst bit currently set), it first calls
 * frmbuf_get() (already read_full elsewhere, not re-derived here) and
 * re-reads the source flags afterward, in case that call mutated them
 * -- confirmed by the real re-load (`ldr r2,[r5]` happens again after
 * the `bl`, not reused from before the call). In every other case the
 * net effect is a plain `*dst = *src`.
 */
#include <stdint.h>

typedef void (*frmbuf_get_fn)(void);

void wldlop_chk_model(int32_t *src_flags, int32_t *dst_flags, frmbuf_get_fn frmbuf_get) {
    int32_t src = *src_flags;
    if ((src & 2) == 0) {
        int32_t dst = *dst_flags;
        if ((dst & 2) != 0) {
            frmbuf_get();
            src = *src_flags;
        }
    }
    *dst_flags = src;
}
