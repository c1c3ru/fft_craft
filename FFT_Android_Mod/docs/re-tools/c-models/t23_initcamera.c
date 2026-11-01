/* Reconstruction of InitCamera() (0x218dcc, 40 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 670.
 *
 * Real finding kept faithfully: the function has no prologue (no
 * push, no stack frame) and ends in a plain `b`, not `bl` -- a genuine
 * TAIL CALL, confirmed by address, not by pattern: InitCamera's own
 * start address (0x218dcc) is EXACTLY SetDefaultCamera()'s end address
 * (0x218cf4 + 216 B), so the branch target is that function's real
 * entry point, not an arbitrary offset into it. SetDefaultCamera
 * itself (NOTES line ~21288, only structurally checkpointed: calls
 * getMapScrollXYZ/getMapScale/getMapAngle) is NOT read here -- it is
 * passed in as an opaque function pointer, same tail-call-as-stub
 * treatment already validated for T20's iOSUnitListWinOnOff.
 *
 * `camera` is the global camera struct's base address (0x60593c,
 * resolved by hand from the real bytes -- PC-relative, no GOT
 * indirection, consistent with a local/static data symbol), passed in
 * as an already-resolved native pointer for the same host/ARM pointer
 * width reason as c-models/t14_boot_framemove.c and others. Only the
 * 5 fields this function itself writes (+0xa0, +0xa4, +0xa8, +0xac,
 * +0xb0) are modeled; the rest of the struct (sizeof unknown) is not.
 */
#include <stdint.h>
#include <string.h>

typedef void (*set_default_camera_fn)(void);

void InitCamera_model(uint8_t *camera, set_default_camera_fn SetDefaultCamera) {
    uint32_t zero = 0;
    memcpy(camera + 0xa0, &zero, 4);
    memcpy(camera + 0xa4, &zero, 4);
    memcpy(camera + 0xa8, &zero, 4);
    memcpy(camera + 0xac, &zero, 4);
    memcpy(camera + 0xb0, &zero, 4);
    SetDefaultCamera();
}
