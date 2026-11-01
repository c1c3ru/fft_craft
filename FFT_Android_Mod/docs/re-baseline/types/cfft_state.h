/* CFFT_STATE -- near-complete layout for the first 0x38 bytes plus a
 * flat params[] array from 0x38 onward. All of this was already
 * recovered in docs/REVERSE_ENGINEERING_NOTES.md section 22 (2026-10-16,
 * prior to this session, from the constructor CFFT_STATE::C2Ev at
 * 0x28bfb8, 584 B, plus 23 small getters/setters read in full); T08
 * (2026-10-31) only consolidates it into a shared header, it adds no
 * new field evidence for this type.
 *
 * sizeof(CFFT_STATE) is NOT confirmed. The constructor zeroes a block
 * from +0x38 to ~+0x454 (1088 B) for params[], so the struct is at
 * least 0x38 + 1088 = 0x478 bytes, but nothing beyond params[] was
 * mapped.
 */
#ifndef FFT_TYPES_CFFT_STATE_H
#define FFT_TYPES_CFFT_STATE_H

#include <stdint.h>

#define CFFT_STATE_PARAMS_COUNT 272  /* 1088 B / 4, zeroed range per the constructor (NOTES sec. 22) */

typedef struct CFFT_STATE {
    int32_t renderWidth;       /* +0x0, default 340 (NOTES sec. 22, GetRenderSize) */
    int32_t renderHeight;      /* +0x4, default 240 (NOTES sec. 22, GetRenderSize) */
    float vertexScaleX;        /* +0x8, default 1.0f (NOTES sec. 22, Get/SetVertexScaling) */
    float vertexScaleY;        /* +0xc, default 1.0f (NOTES sec. 22, Get/SetVertexScaling) */
    int32_t captureRequest;    /* +0x10, default 0 (NOTES sec. 22) */
    int32_t captureDraw;       /* +0x14, default 0 (NOTES sec. 22) */
    int32_t encountRequest;    /* +0x18, default 0 (NOTES sec. 22) */
    /* +0x1c: controls UI visibility and backdrop color, not just a label
     * (NOTES sec. 22.2): GetMenuBarVisible() hides the menu bar for
     * mode in {2,3,4}; GetBackdropColor() switches on mode via a 5-case
     * jump table, but in this build all 5 cases converge to the same
     * block, so the per-mode color could not be told apart in that
     * pass. */
    int32_t mode;              /* +0x1c, default 0 (NOTES sec. 22) */
    int32_t debugMode;         /* +0x20, default 0 (NOTES sec. 22) */
    int32_t moviePlaying;      /* +0x24, default -1 ("none" sentinel) (NOTES sec. 22) */

    /* +0x28: musicBuffer[], zeroed by the constructor. The original note
     * describes it as indexed by "+0xa" without fully resolving the
     * indexing scheme -- not re-derived in T08; treat the exact element
     * size/stride as unresolved. */
    uint8_t musicBuffer_0x28[0x08];

    int32_t settingsEnable;    /* +0x30, default 0 (NOTES sec. 22) */
    int32_t linkEnable;        /* +0x34, default 0 (NOTES sec. 22) */

    /* +0x38: params[] -- a flat, unbounded-check int array, confirmed
     * by reading GetParam/SetParam/AddParam in full (NOTES sec. 22.3):
     *   int  GetParam(int id)            { return *(int*)((char*)this + 0x38 + id*4); }
     *   void SetParam(int id, int val)   { *(int*)((char*)this + 0x38 + id*4) = val; }
     *   void AddParam(int id, int delta) { *(int*)((char*)this + 0x38 + id*4) += delta; }
     * IDs 0x39-0x3f are known to hold the save timestamp (cSaveFFT::Save,
     * NOTES section 19/22.3). CFFT_STATE_PARAMS_COUNT reflects only the
     * zeroed range the constructor touches, not a confirmed hard bound --
     * the accessors themselves do no bounds check. */
    int32_t params[CFFT_STATE_PARAMS_COUNT];
} CFFT_STATE;

#endif
