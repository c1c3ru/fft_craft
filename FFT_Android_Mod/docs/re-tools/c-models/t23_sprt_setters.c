/* Reconstruction of 5 tiny tagSPRT setters, per
 * docs/REVERSE_ENGINEERING_NOTES.md section 679:
 *   SetSprt(tagSPRT*)       (0x2914e4, 36 B)
 *   SetSprt16(tagSPRT*)     (0x291508, 36 B)
 *   SetSprt8(tagSPRT*)      (0x29152c, 36 B)
 *   SetSemiTrans(tagSPRT*, int) (0x291a6c, 24 B)
 *   SetShadeTex(tagSPRT*, int)  (0x291a84, 24 B)
 *
 * First field evidence for tagSPRT. SetSprt/8/16 confirm +0x4 (a
 * primitive type/mode byte: 4 for SetSprt, 3 for both SetSprt8/16)
 * and +0xb (a byte whose high bits SetSprt/8/16 set to a fixed base
 * value -- 0x64/0x74/0x7c respectively, all with their low 2 bits
 * already clear) alongside +0x5/+0x6/+0x7 (all zeroed). SetSemiTrans
 * and SetShadeTex confirm +0xb is the SAME byte, read-modify-written
 * with OR/AND-NOT on bit 1 and bit 0 respectively -- the classic PS1
 * GPU primitive "code" byte, whose low bits are semi-transparency/
 * shaded-texture flags layered onto a fixed base code. Confirmed by
 * address (both functions read/write the identical +0xb offset that
 * SetSprt/8/16 also write), not assumed from the PS1 GPU convention
 * alone.
 */
#include <stdint.h>

void SetSprt_model(uint8_t *sprt) {
    sprt[0x4] = 4;
    sprt[0xb] = 0x64;
    sprt[0x5] = 0;
    sprt[0x6] = 0;
    sprt[0x7] = 0;
}

void SetSprt16_model(uint8_t *sprt) {
    sprt[0x4] = 3;
    sprt[0xb] = 0x7c;
    sprt[0x5] = 0;
    sprt[0x6] = 0;
    sprt[0x7] = 0;
}

void SetSprt8_model(uint8_t *sprt) {
    sprt[0x4] = 3;
    sprt[0xb] = 0x74;
    sprt[0x5] = 0;
    sprt[0x6] = 0;
    sprt[0x7] = 0;
}

void SetSemiTrans_model(uint8_t *sprt, int32_t flag) {
    if (flag != 0) {
        sprt[0xb] |= 2;
    } else {
        sprt[0xb] &= (uint8_t)~2;
    }
}

void SetShadeTex_model(uint8_t *sprt, int32_t flag) {
    if (flag != 0) {
        sprt[0xb] |= 1;
    } else {
        sprt[0xb] &= (uint8_t)~1;
    }
}
