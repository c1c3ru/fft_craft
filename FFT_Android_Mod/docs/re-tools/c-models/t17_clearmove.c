/* Reconstruction of ClearMove(MOVE*) (0x27383c, 40 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 672.
 *
 * Only 5 of the struct's bytes are touched (+0x1, +0x3, +0x1c, +0x1d,
 * +0x1e/+0x1f as one halfword); +0x0, +0x2 and everything from +0x4
 * onward are left exactly as they were -- this is a partial reset,
 * not a full re-initialization, and this file does not claim a
 * `sizeof(MOVE)` or invent fields it does not write.
 */
#include <stdint.h>
#include <string.h>

void ClearMove_model(uint8_t *move) {
    move[0x1] = 0;
    move[0x3] = 5;
    move[0x1c] = 0;
    move[0x1d] = 0;
    uint16_t sentinel = 0x8001; /* likely an "invalid direction" sentinel angle, not confirmed by name */
    memcpy(move + 0x1e, &sentinel, 2);
}
