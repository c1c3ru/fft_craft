/* Reconstruction of nextTurnOrder() (0x1fd1dc, 36 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 673.
 *
 * Advances a global turn-order index with wraparound: values 0..39
 * (40 slots -- the literal compared against is 0x27=39, "greater
 * than" resets to 0, confirmed inclusive by the `movgt` conditional,
 * not `movge`). Cross-referenced by address with resetTurnOrder()
 * (NOTES sec. 673, c-models/t15_resetturnorder.c): both resolve the
 * same GOT slot to the same global, 0x5dd8e0.
 *
 * `turn_index` is taken as an already-resolved native pointer to that
 * global, same convention as the other c-models in this directory.
 */
#include <stdint.h>

void nextTurnOrder_model(int32_t *turn_index) {
    int32_t next = *turn_index + 1;
    if (next > 39) {
        next = 0;
    }
    *turn_index = next;
}
