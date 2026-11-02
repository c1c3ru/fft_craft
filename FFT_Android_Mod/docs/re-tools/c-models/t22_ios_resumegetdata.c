/* Reconstruction of iOS_ResumeGetData(unsigned char**, unsigned int*)
 * (0x27f620, 32 B), per docs/REVERSE_ENGINEERING_NOTES.md section 681.
 *
 * Trivial accessor: unconditionally writes the fixed address of the
 * global battle-resume snapshot buffer and its fixed size into the
 * two out-parameters -- both compile-time constants read directly
 * off the real bytes (the address via a direct PC-relative literal,
 * no GOT indirection, consistent with a local/static data symbol).
 * The size, 0x84558 (542040) bytes, is new evidence: callers (e.g.
 * CAUTOSAVE::Save) were already known to call this and memcpy its
 * result, but the actual buffer size was never previously confirmed
 * numerically.
 *
 * `BUFFER_ADDR` is a value chosen by the test to stand in for the
 * real ELF's own fixed address (0x6b4680) -- this file does not
 * claim to reproduce that exact numeric address, only that the
 * function always returns a fixed, caller-independent constant
 * address, exactly as the real bytes do.
 */
#include <stdint.h>

#define IOS_RESUME_GETDATA_SIZE 0x84558u

void iOS_ResumeGetData_model(void **out_buffer, uint32_t *out_size, void *fixed_buffer_addr) {
    *out_buffer = fixed_buffer_addr;
    *out_size = IOS_RESUME_GETDATA_SIZE;
}
