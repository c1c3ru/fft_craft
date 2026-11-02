/* Reconstruction of resetTurnOrder() (0x1fd2ac, 24 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 673.
 *
 * Cross-referenced by address with nextTurnOrder() (NOTES sec. 673,
 * c-models/t15_nextturnorder.c): both resolve the same GOT slot to
 * the same global, 0x5dd8e0, confirmed by independently resolving
 * each function's literal-pool/GOT chain, not by name similarity.
 */
#include <stdint.h>

void resetTurnOrder_model(int32_t *turn_index) {
    *turn_index = 0;
}
