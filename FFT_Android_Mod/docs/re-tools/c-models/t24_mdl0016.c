/* Reconstruction of Mdl0016(short, int, int, int) (0x23c6b0), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 665 -- a 4-state machine
 * over one status byte of a per-model "snow effect" sub-struct.
 *
 * Only the first two of the four declared parameters are read by this
 * function's body (confirmed by execution, not assumed) -- p2/p3 are
 * accepted but unused, kept in the signature below only to match the
 * real ABI shape, not because this file claims they matter.
 *
 * ASHURA_snowMatrix is passed in as a function pointer: this file
 * makes no claim about its own behavior.
 */
#include <stdint.h>

#define MDL_STRIDE 0xf8

typedef void (*ashura_snow_matrix_fn)(int32_t, int32_t);

uint8_t Mdl0016_model(
    int16_t model_id, int32_t p1, int32_t p2, int32_t p3,
    uint8_t *mdl_array,       /* g_mdlArray base, stride 0xf8 */
    void **g,                 /* *global_ptr_slot: pointer to the global struct */
    ashura_snow_matrix_fn ASHURA_snowMatrix) {
    (void)p2;
    (void)p3;
    uint8_t *entry = mdl_array + (int32_t)model_id * MDL_STRIDE;
    uint8_t *sub = entry + p1 + 0x20;
    uint8_t state = sub[2];

    if (state == 3) {
        sub[2] = 0;
        return 0;
    }
    if (state != 1) {
        return state;
    }

    int16_t my_field = *(int16_t *)(entry + 0x28);        /* relative to entry, not sub */
    int16_t global_field = *(int16_t *)((uint8_t *)*g + 2); /* double indirection via g */
    ASHURA_snowMatrix(0x96, (int32_t)global_field - (int32_t)my_field);
    sub[2] = 2;
    return 2;
}
