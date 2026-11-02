/* Reconstruction of pspSaveDataGetOne(int, FFT_SAVE_DATA*) (0x289b64,
 * 20 B), per docs/REVERSE_ENGINEERING_NOTES.md section 675.
 *
 * Purely an argument-reordering shim: swaps (slot, save) into
 * (save, slot), adds a constant third argument (1), and tail-calls
 * (`b`, not `bl`) a local, unsymbolized function at 0x2898e0 -- the
 * sixth genuine ARM tail call confirmed this session. This file makes
 * no claim about that target's own behavior; it is passed in as an
 * opaque function pointer with 3 arguments, matching exactly the
 * registers the real tail call leaves set.
 */
#include <stdint.h>

typedef int32_t (*get_one_target_fn)(void *save, int32_t slot, int32_t flag);

int32_t pspSaveDataGetOne_model(int32_t slot, void *save, get_one_target_fn target) {
    return target(save, slot, 1);
}
