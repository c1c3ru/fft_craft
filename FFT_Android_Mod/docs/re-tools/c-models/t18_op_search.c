/* Reconstruction of op_search(int, int) (0x26a674), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 664 -- a linear search
 * through a per-event list of 4-byte tagged entries, with a sentinel
 * tag (1) marking end-of-list and a hard 0x400-byte (256-entry) scan
 * cap. Unlike every other vertical slice in this project so far, this
 * function makes zero external calls: the whole mechanism (two levels
 * of GOT-resolved global indirection, pointer-tag masking, linear scan)
 * is self-contained.
 *
 * The three levels of indirection (table_ptr_slot -> g -> eventTable)
 * are passed in explicitly rather than hidden behind a struct, because
 * the real binary resolves them as two SEPARATE GOT slots -- collapsing
 * them would hide the exact mechanism this model is reconstructing.
 */
#include <stdint.h>

uint32_t op_search_model(
    int32_t event_id, int32_t search_tag,
    void **g,                 /* *table_ptr_slot: pointer to g */
    uint8_t *relocation_base   /* *base_val_slot */) {
    void **event_table = (void **)*g;
    uint32_t packed = ((uint32_t *)event_table)[event_id + 1];
    uint8_t *entry_list = relocation_base + (packed & ~3u);

    for (uint32_t offset = 0; offset < 0x400; offset += 4) {
        uint32_t word = *(uint32_t *)(entry_list + offset);
        uint8_t tag = (uint8_t)word;
        if (tag == (uint8_t)search_tag) {
            return word;
        }
        if (tag == 1) {
            break;  /* sentinel: end of list */
        }
    }
    return 0;
}
