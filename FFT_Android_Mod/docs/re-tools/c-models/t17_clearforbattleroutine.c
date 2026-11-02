/* Reconstruction of ClearForBattleRoutine() (0x279ed4, 24 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 672.
 *
 * Real finding kept faithfully: no prologue, no push -- this is a
 * genuine ARM tail call (`b`, not `bl`) into ClearMove(MOVE*)
 * (0x27383c, independently differential-tested in
 * c-models/t17_clearmove.c / test_t17_clearmove.py), the third such
 * tail call confirmed this session (after T20's
 * iOSUnitListWinOnOff and T23's InitCamera). The computed address
 * (a global base resolved by hand, +0x17c0+0x3c) is passed in as the
 * already-resolved MOVE* pointer -- same host/ARM pointer-width
 * reasoning as the other c-models in this directory.
 */
#include <stdint.h>

typedef void (*clear_move_fn)(uint8_t *move);

void ClearForBattleRoutine_model(uint8_t *move_ptr, clear_move_fn ClearMove) {
    ClearMove(move_ptr);
}
