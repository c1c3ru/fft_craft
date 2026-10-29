#include <stdint.h>

/* Independent C contract for A32 0x000b8be4, Shift-JIS lead-byte test.
 * Only the low byte of the incoming R0 participates in the original
 * ADD/AND byte arithmetic. This model does not process a whole string.
 */
uint32_t a04_sjis_lead_byte(uint32_t incoming_r0) {
    uint32_t byte = incoming_r0 & UINT32_C(0xff);
    return ((byte >= UINT32_C(0x81) && byte <= UINT32_C(0x9f)) ||
            (byte >= UINT32_C(0xe0) && byte <= UINT32_C(0xfc))) ? 1u : 0u;
}
