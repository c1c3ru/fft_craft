/* Reconstruction of iOS_ResumeMusic() (0xcbd90, 100 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 682.
 *
 * Composes two already-closed functions (CFFT_STATE::GetMusicBuffer,
 * NOTES-confirmed read_full; iOS_SetLastBGMFromResumeData, likewise)
 * and ends in a genuine ARM tail call (`b`, not `bl`) into an
 * unsymbolized local function -- the eighth tail call confirmed this
 * session.
 *
 * Real finding: iOS_SetLastBGMFromResumeData unconditionally
 * OVERWRITES both out-parameters with values read from a fixed
 * resume-data struct offset (+0x47c/+0x47e, confirmed by its own
 * disassembly) -- it does not merge, check, or fall back to whatever
 * GetMusicBuffer already wrote. So the two GetMusicBuffer calls'
 * results are discarded before ever being read back; the values
 * actually passed to the tail-called target come entirely from the
 * resume-data struct, not from CFFT_STATE's current music buffer.
 * This file reproduces that discard faithfully instead of "cleaning
 * it up" into skipping the GetMusicBuffer calls (which may still have
 * real side effects this function's own body does not depend on, but
 * which this file's own differential test does not re-verify).
 *
 * GetMusicBuffer/SetLastBGMFromResumeData are passed in as function
 * pointers; this file makes no further claim about their own
 * behavior beyond what is already independently confirmed elsewhere.
 */
#include <stdint.h>

typedef int32_t (*get_music_buffer_fn)(void *cfft_state, int32_t index);
typedef void (*set_last_bgm_fn)(uint16_t *out0, uint16_t *out1);
typedef void (*tail_target_fn)(uint16_t bgm0, uint16_t bgm1);

void iOS_ResumeMusic_model(
    void *cfft_state, get_music_buffer_fn GetMusicBuffer,
    set_last_bgm_fn SetLastBGMFromResumeData,
    uint16_t *g_lastBgm0, uint16_t *g_lastBgm1, tail_target_fn tail_target) {
    *g_lastBgm0 = (uint16_t)GetMusicBuffer(cfft_state, 0);
    *g_lastBgm1 = (uint16_t)GetMusicBuffer(cfft_state, 1);

    SetLastBGMFromResumeData(g_lastBgm0, g_lastBgm1);

    tail_target(*g_lastBgm0, *g_lastBgm1);
}
