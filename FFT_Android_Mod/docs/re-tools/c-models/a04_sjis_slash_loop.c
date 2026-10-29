#include <stdint.h>
#include <stddef.h>

/* Independent C implementation of the bounded 0x000b942c loop.
 * Input is an already-copied NUL-terminated string. The caller supplies a
 * sufficient capacity, and all bytes are verified before mutation.
 * This model is NOT a replacement for strcpy or Android libc.
 */
extern uint32_t a04_sjis_lead_byte(uint32_t byte);

int a04_normalize_sjis_slashes(uint8_t *buffer, size_t capacity) {
    if (!buffer || capacity == 0u)
        return 0;
    size_t length = 0u;
    while (length < capacity && buffer[length] != 0u)
        ++length;
    if (length == capacity)
        return 0;
    size_t index = 0u;
    while (index < length) {
        if (a04_sjis_lead_byte(buffer[index])) {
            index += 2u;
        } else {
            if (buffer[index] == (uint8_t)'\\')
                buffer[index] = (uint8_t)'/';
            ++index;
        }
    }
    return 1;
}
