/* Reconstruction of DisposeObject(short, _Object*) (0x22599c, 196 B),
 * per docs/REVERSE_ENGINEERING_NOTES.md section 677.
 *
 * First real field evidence for `_Object`, the fourth and last type
 * T08 (2026-10-31) listed with none at all. Fields confirmed by this
 * function's own body (not inherited from anywhere else):
 *   +0x00 prev  (intrusive doubly-linked list, within a per-table slot)
 *   +0x04 next  (same list; reused as the global free-list link below)
 *   +0x4c category (int16, high nibble selects the disposal path)
 *   +0x54 payload (opaque pointer, passed to whichever of Free()/
 *                  DisposeEffectAnimation() the category selects)
 *
 * Also gives the first field evidence for the per-slot object-table
 * entry this function indexes into (stride 0xf8, base already a
 * confirmed global elsewhere -- not a new type header here, since
 * only 2 of its fields are touched):
 *   +0x1c live-object count for this slot (uint16, decremented)
 *   +0xd0 head-of-list pointer for this slot (written only when the
 *         disposed object had no `prev`, i.e. it WAS the head)
 *
 * next_obj/prev_obj are taken as already-resolved, genuinely
 * dereferenceable pointers (or NULL) instead of read out of `obj`'s
 * own +0x00/+0x04 byte slots: the real function DOES read them from
 * there, but a real host pointer does not fit back into the 4 bytes
 * those ARM slots have -- same reasoning as the other c-models in
 * this directory. `obj`'s own +0x00/+0x04 bytes are still read
 * directly (as plain 4-byte values, never dereferenced by this
 * function itself) to get the VALUES written into next_obj/prev_obj/
 * table_entry.
 *
 * free_list_head is modeled as a plain uint32_t slot, not a
 * dereferenceable pointer-to-pointer: this function never dereferences
 * *free_list_head either, only copies its bits into obj+0x4 and then
 * overwrites it with obj's own address -- see
 * test_t08_disposeobject.c's comments for how the final "becomes obj"
 * write is verified without needing a cross-width address comparison.
 */
#include <stdint.h>
#include <string.h>

typedef void (*free_fn)(void *ptr);
typedef void (*dispose_effect_animation_fn)(void *effect_anim);

void DisposeObject_model(
    uint8_t *obj, void *next_obj, void *prev_obj, uint8_t *table_entry,
    int32_t *obj_count, uint32_t *free_list_head,
    free_fn Free, dispose_effect_animation_fn DisposeEffectAnimation) {
    uint32_t obj_prev, obj_next;
    memcpy(&obj_prev, obj + 0x00, 4);
    memcpy(&obj_next, obj + 0x04, 4);

    if (next_obj != NULL) {
        memcpy((uint8_t *)next_obj + 0x00, &obj_prev, 4);
    }
    if (prev_obj != NULL) {
        memcpy((uint8_t *)prev_obj + 0x04, &obj_next, 4);
    } else {
        memcpy(table_entry + 0xd0, &obj_next, 4);
    }

    int16_t category_raw;
    memcpy(&category_raw, obj + 0x4c, 2);
    int32_t category = category_raw & 0xf000;

    uint16_t count;
    memcpy(&count, table_entry + 0x1c, 2);
    count = (uint16_t)(count - 1);
    memcpy(table_entry + 0x1c, &count, 2);

    uint32_t payload_raw;
    memcpy(&payload_raw, obj + 0x54, 4);
    void *payload = (void *)(uintptr_t)payload_raw;

    if (category == 0x4000) {
        Free(payload);
    } else if (category == 0 || category == 0x1000 || category == 0x2000 || category == 0x3000) {
        DisposeEffectAnimation(payload);
    }
    /* Any other category (e.g. 0x5000 and above): neither callee is
     * invoked -- the real bytes' final `bne` falls straight to the
     * common tail below. */

    *obj_count -= 1;

    uint32_t old_head = *free_list_head;
    memcpy(obj + 0x04, &old_head, 4);
    *free_list_head = (uint32_t)(uintptr_t)obj;
}
