/* Reconstruction of Wdisposewindowbytask(int) (0xfeeb4, 112 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 685.
 *
 * `base` is a single global struct/array (one PC-relative literal,
 * no GOT indirection, resolved to the SAME address 0x4711fc for both
 * the three "owning task id" tracker fields AND the stride-0x1c0
 * window-slot array -- confirmed by resolving both literal chains
 * independently, not assumed). Three fixed fields (+0x5e8, +0x968,
 * +0xce8, stride 0x380 apart) each track which taskId currently owns
 * one of three window-slot PAIRS (indices 0&1, 2&3, 4&5 in the
 * stride-0x1c0 array that starts at the same base). If taskId
 * matches none of the three, the function is a no-op -- confirmed by
 * the real `bxne lr` on the third comparison, not assumed.
 */
#include <stdint.h>
#include <string.h>

#define WDISPOSE_SLOT_STRIDE 0x1c0

void Wdisposewindowbytask_model(int32_t task_id, uint8_t *base) {
    int32_t owner0, owner1, owner2;
    int32_t slot_pair;

    memcpy(&owner0, base + 0x5e8, 4);
    if (owner0 == task_id) {
        slot_pair = 0;
    } else {
        memcpy(&owner1, base + 0x968, 4);
        if (owner1 == task_id) {
            slot_pair = 2;
        } else {
            memcpy(&owner2, base + 0xce8, 4);
            if (owner2 != task_id) {
                return;
            }
            slot_pair = 4;
        }
    }

    int32_t zero = 0;
    memcpy(base + (int64_t)slot_pair * WDISPOSE_SLOT_STRIDE + 0x5e4, &zero, 4);
    memcpy(base + (int64_t)(slot_pair + 1) * WDISPOSE_SLOT_STRIDE + 0x5e4, &zero, 4);
}
