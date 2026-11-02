/* Reconstruction of pspSaveDataMissionRateSave(FFT_SAVE_DATA*)
 * (0x289ba8, 32 B) and pspSaveDataMissionRateLoad(FFT_SAVE_DATA*)
 * (0x289b8c, 28 B), per docs/REVERSE_ENGINEERING_NOTES.md section 675.
 *
 * First confirmed FFT_SAVE_DATA field evidence in the project: both
 * functions tail-call the REAL memcpy at 0x714b8 (already confirmed
 * elsewhere in the notes as glibc-style memcpy, not re-derived here)
 * with save+0x60 as one side and the live "mission buffer" (returned
 * by pspNetEntranceDataMissionBufferGet(), already read_full
 * elsewhere) as the other, size 0x20 (32 B) -- giving
 * FFT_SAVE_DATA+0x60, 32 B = a "mission rate" data blob.
 *
 * The dest/src order is the key finding, confirmed by the registers
 * at each tail call site, not assumed from the function names:
 *   Save: memcpy(dest=save+0x60,        src=missionBuffer, 0x20)
 *   Load: memcpy(dest=missionBuffer,    src=save+0x60,     0x20)
 * i.e. "Save" captures live state INTO the save struct; "Load"
 * restores it FROM the save struct -- the opposite directions are
 * exactly swapped between the two functions' register setup.
 *
 * Both end in a genuine ARM tail call (`b`, not `bl`) into memcpy --
 * the fourth and fifth such tail calls confirmed this session (after
 * T20/T23/T17's third).
 */
#include <stdint.h>

typedef void *(*mission_buffer_get_fn)(void);
typedef void (*memcpy_like_fn)(void *dest, void *src, int32_t size);

void pspSaveDataMissionRateSave_model(
    uint8_t *save, mission_buffer_get_fn GetMissionBuffer, memcpy_like_fn copy) {
    void *mission_buffer = GetMissionBuffer();
    copy(save + 0x60, mission_buffer, 0x20);
}

void pspSaveDataMissionRateLoad_model(
    uint8_t *save, mission_buffer_get_fn GetMissionBuffer, memcpy_like_fn copy) {
    void *mission_buffer = GetMissionBuffer();
    copy(mission_buffer, save + 0x60, 0x20);
}
