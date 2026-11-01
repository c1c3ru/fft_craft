/* Reconstruction of CSOUND_IF_SL::Stop(int channel) (0xbb838, 88 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 667.
 *
 * Reuses two fields already confirmed by prior, independent reads of
 * this same engine's lifecycle (NOTES sec. 16-17), not re-derived here:
 *   - CSOUND_IF_SL+0x10 = base pointer of the per-channel array
 *     ("channelData"), channel stride 0x88 (confirmed in EngineInit,
 *     NOTES sec. 17.1 -- "this->channelData = alloc(maxChannels*0x88)").
 *   - Channel+0x78 = playItf (SLPlayItf), confirmed in Play()
 *     (NOTES sec. 17.3 -- "SLPlayItf playItf = c->playItf; // +0x78").
 * Channel+0x4, +0x3c (read only as a nonzero/null guard here, never
 * dereferenced), +0x48 and +0x50 are read/written by this function but
 * have no independently confirmed semantic name -- kept as field_0xNN,
 * not invented.
 *
 * `channel_data` (this->channelData) and `play_itf` (entry+0x78) are
 * taken as direct native-pointer parameters, already resolved by the
 * caller, instead of read via memcpy from a byte buffer laid out at
 * the real 32-bit ARM offsets: on a 64-bit host a genuinely
 * dereferenceable pointer does not fit in the 4 bytes the real ARM
 * struct gives it, the same cross-width problem c-models/t26's
 * xpPadKeyBufGet callback and c-models/t24_mdl0016.c's `g` parameter
 * sidestep the same way. entry+0x78 is only ever READ once by this
 * function, never written, so passing its already-resolved value
 * changes nothing observable. field_0x04/+0x3c are only ever compared
 * to zero (never dereferenced), so reading them as plain int32 at
 * their real offsets has no such width issue.
 *
 * playItf follows the standard OpenSL ES C object layout: a pointer to
 * an object whose first member is a vtable pointer, so
 * `*(void**)play_itf` is the vtable and `vtbl[0]` is SetPlayState,
 * called as SetPlayState(play_itf, 1). That literal `1` is read
 * directly off the real bytes (mov r5,#1 / mov r1,r5), not assumed
 * from the OpenSL ES header; it happens to equal SL_PLAYSTATE_STOPPED.
 *
 * Real finding kept faithfully, not "cleaned up": on the early-exit
 * path (field_0x04==0 AND field_0x3c==0), the real ARM body NEVER
 * rewrites r0 after function entry -- so it returns the ORIGINAL
 * `this` pointer, not 0. A model that assumed "returns 0 when there is
 * nothing to stop" would diverge from the real ELF on this path (see
 * the fault-injection test in test_t25_csoundifsl_stop.py).
 */
#include <stdint.h>
#include <string.h>

#define CSOUND_IF_SL_CHANNEL_STRIDE 0x88

typedef int32_t (*set_play_state_fn)(void *play_itf, int32_t state);

static int32_t call_set_play_state(void *play_itf) {
    void *vtbl;
    memcpy(&vtbl, play_itf, sizeof(vtbl));
    set_play_state_fn fn;
    memcpy(&fn, vtbl, sizeof(fn));
    return fn(play_itf, 1 /* SL_PLAYSTATE_STOPPED, literal from the real bytes */);
}

uint32_t CSOUND_IF_SL_Stop_model(
    uint8_t *channel_data, int32_t channel, void *play_itf, uint32_t this_value) {
    uint8_t *entry = channel_data + (uint32_t)channel * CSOUND_IF_SL_CHANNEL_STRIDE;

    int32_t field_0x04;
    memcpy(&field_0x04, entry + 0x4, 4);
    int32_t field_0x3c;
    memcpy(&field_0x3c, entry + 0x3c, 4);

    if (field_0x04 == 0 && field_0x3c == 0) {
        /* Nothing active and nothing loaded: real r0 is unchanged. */
        return this_value;
    }
    if (play_itf == NULL) {
        return 0;
    }

    int32_t one = 1;
    memcpy(entry + 0x48, &one, 4);
    int32_t result = call_set_play_state(play_itf);
    if (result == 0) {
        memcpy(entry + 0x50, &one, 4);
    }
    return (uint32_t)result;
}
