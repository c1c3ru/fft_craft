/* _Object -- partial layout. First field-level evidence recovered
 * for this type (T08 named it in 2026-10-31 as having "no reliable
 * field evidence" at all -- the fourth and last of the four types it
 * listed; this slice, 2026-11-02, closes it). sizeof(_Object) is NOT
 * known -- do not assume any size; this header only places the bytes
 * actually read.
 *
 * Pointer-shaped fields are kept as uint32_t, not real C pointers:
 * the real target is 32-bit ARM, and a genuine pointer type here
 * would be 8 bytes on a 64-bit host, breaking every offset below it
 * (same convention already used by the other headers in this
 * directory for fields that are pointers on the real target).
 *
 * Source for every field below: DisposeObject(short, _Object*)
 * (0x22599c, docs/REVERSE_ENGINEERING_NOTES.md section 677, read
 * directly by disassembly and confirmed by differential test against
 * the real ELF across 6 category/neighbor combinations).
 */
#ifndef FFT_TYPES_OBJECT_H
#define FFT_TYPES_OBJECT_H

#include <stddef.h>
#include <stdint.h>

typedef struct _Object {
    /* Intrusive doubly-linked list within the object's table slot.
     * Confirmed to be real pointers to other _Object instances on
     * the real (32-bit ARM) target -- dereferenced by DisposeObject
     * when unlinking. */
    uint32_t prev;   /* +0x00 */
    uint32_t next;   /* +0x04 -- reused as the global free-list link
                       * once the object is disposed */

    uint8_t _unknown_0x08_0x4b[0x44];

    /* High nibble selects DisposeObject's disposal path: 0x0000/
     * 0x1000/0x2000/0x3000 -> DisposeEffectAnimation(payload);
     * 0x4000 -> Free(payload); anything else -> neither is called.
     * Low 12 bits are masked off by DisposeObject and not confirmed
     * to mean anything here. */
    int16_t category_flags; /* +0x4c */

    uint8_t _unknown_0x4e_0x53[0x06];

    /* Opaque payload pointer (real target: 32-bit), passed verbatim
     * to whichever callee category_flags selects. Its pointee type
     * is NOT confirmed -- DisposeEffectAnimation's parameter type
     * (effectAnimation*) is known from the mangled name, but Free's
     * is just void*, and this field is read the same 4 bytes
     * regardless of category. */
    uint32_t payload; /* +0x54 */
} _Object;

#ifdef __cplusplus
static_assert(offsetof(_Object, prev) == 0x00, "prev must stay at the confirmed real offset");
static_assert(offsetof(_Object, next) == 0x04, "next must stay at the confirmed real offset");
static_assert(offsetof(_Object, category_flags) == 0x4c, "category_flags must stay at the confirmed real offset");
static_assert(offsetof(_Object, payload) == 0x54, "payload must stay at the confirmed real offset");
#else
_Static_assert(offsetof(_Object, prev) == 0x00, "prev must stay at the confirmed real offset");
_Static_assert(offsetof(_Object, next) == 0x04, "next must stay at the confirmed real offset");
_Static_assert(offsetof(_Object, category_flags) == 0x4c, "category_flags must stay at the confirmed real offset");
_Static_assert(offsetof(_Object, payload) == 0x54, "payload must stay at the confirmed real offset");
#endif

#endif
