/* Reconstruction of setskillresult_caster(int) (0x1ce950), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 662 -- first vertical slice
 * of T16 (combat). setskillresult(int) itself (0x1cda4c, 3844 B) is
 * treated as an opaque callback here, matching how it is stubbed in
 * the differential test against the real ELF: this file only claims to
 * reconstruct the wrapper, not the combat formula it calls into.
 *
 * bwork_array must point to a contiguous array of BWORK-sized (0x1e6
 * byte) entries; this model does not know BWORK's full layout, only
 * the two fields it touches (offsets 0x1 and 0x1ae, see bwork.h).
 */
#include <stdint.h>

#define BWORK_SIZE 0x1e6
#define RESULT_OFFSET 0x1ae
#define RESULT_SIZE 0x2e

typedef void (*copy_struct_data_fn)(const void *src, void *dst, int32_t size);
typedef void (*setskillresult_fn)(int32_t casterId);

int32_t setskillresult_caster_model(
    int32_t casterId,
    uint8_t *bwork_array,
    uint8_t **current_caster_bwork,     /* global pointer slot */
    uint8_t *current_caster_id_byte1,   /* global byte, written at +1 */
    uint8_t **current_result_slot_ptr,  /* global pointer slot */
    const uint8_t *default_result_template,
    copy_struct_data_fn copy_struct_data,
    setskillresult_fn setskillresult) {
    uint8_t *bw = bwork_array + (int64_t)casterId * BWORK_SIZE;
    *current_caster_bwork = bw;
    if (casterId > 20) {
        return -1;
    }
    uint8_t flag = bw[1];
    current_caster_id_byte1[1] = (uint8_t)casterId;
    uint8_t *result_slot = bw + RESULT_OFFSET;
    *current_result_slot_ptr = result_slot;
    if (flag == 0xff) {
        return -1;
    }
    copy_struct_data(default_result_template, result_slot, RESULT_SIZE);
    setskillresult(casterId);
    if (result_slot[0] == 0) {
        result_slot[2] = 8;
    }
    return 0;
}
