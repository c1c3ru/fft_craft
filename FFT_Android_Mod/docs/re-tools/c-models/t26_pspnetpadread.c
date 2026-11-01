/* Reconstruction of pspNetPadRead() (0x28e5e0), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 663. Despite the "pspNet"
 * prefix, this has nothing to do with networking -- it combines two
 * local pad-button buffers, applies a one-shot disable mask, and
 * overlays a tutorial-mode pad reading.
 *
 * xpPadKeyBufGet, iOSTutoCheck, iOS_getTutorialPad are passed in as
 * function pointers: this file makes no claim about their own
 * behavior. xpPadKeyBufGet is modeled by its confirmed real signature:
 * it returns the ADDRESS OF a pointer variable (double indirection),
 * not the buffer pointer itself -- confirmed by execution, not assumed
 * (an earlier attempt without this indirection faulted immediately).
 */
#include <stdint.h>

typedef uint8_t **(*pad_key_buf_get_fn)(int32_t which);
typedef int32_t (*tuto_check_fn)(void);
typedef int32_t (*tutorial_pad_fn)(void);

uint32_t pspNetPadRead_model(
    uint32_t *pad_mask,
    pad_key_buf_get_fn xpPadKeyBufGet,
    tuto_check_fn iOSTutoCheck,
    tutorial_pad_fn iOS_getTutorialPad) {
    uint8_t **ptr_slot0 = xpPadKeyBufGet(0);
    uint8_t **ptr_slot1 = xpPadKeyBufGet(1);
    uint8_t *buf0 = *ptr_slot0;
    uint8_t *buf1 = *ptr_slot1;

    uint16_t v0 = (uint16_t)buf0[3] | ((uint16_t)buf0[2] << 8);
    uint16_t v1 = (uint16_t)buf1[3] | ((uint16_t)buf1[2] << 8);
    uint32_t combined = (uint32_t)v0 | ((uint32_t)v1 << 16);

    combined &= ~(*pad_mask);
    *pad_mask = 0;  /* one-shot: consumed on every read */

    int32_t tutorial_active = iOSTutoCheck();
    combined = ~combined;
    if (!tutorial_active) {
        return combined;
    }
    if (iOS_getTutorialPad() != 0) {
        combined |= (uint32_t)iOS_getTutorialPad();  /* called twice, by design */
    }
    return combined;
}
