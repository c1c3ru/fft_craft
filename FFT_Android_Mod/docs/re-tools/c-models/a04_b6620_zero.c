#include <stdint.h>
#include <stddef.h>

/* Only the R1==0 branch of A32 0x000b6620 is modeled.
 * The alternate BL 0x000714a0 is explicitly outside this contract.
 * Returns 1 for success and 0 for invalid input.
 */
int a04_zero_path(uint8_t *memory, size_t length, uint32_t selector) {
    if (!memory || selector != 0 || length < 0x108u)
        return 0;
    memory[0x104] = 0;
    memory[0x105] = 0;
    memory[0x106] = 0;
    memory[0x107] = 0;
    return 1;
}
