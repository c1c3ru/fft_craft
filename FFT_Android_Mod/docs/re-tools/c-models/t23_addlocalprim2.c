/* Reconstruction of addlocalprim2(tagPOLY_FT4*) (0xe05bc, 112 B), per
 * docs/REVERSE_ENGINEERING_NOTES.md section 680.
 *
 * This is the classic PS1 GPU ordering-table (OT) head-insertion
 * primitive, done byte-by-byte (not as one aligned 32-bit load/store
 * -- the real bytes do 4 separate ldrb/strb pairs each way, not an
 * `ldr`/`str`, so this file keeps that shape instead of collapsing
 * it into a single 32-bit access that might hide an alignment
 * assumption the real code does not make):
 *
 *   prim->tag = *otHead;   // link new prim to whatever the OT
 *                          // currently points to
 *   *otHead = prim;        // OT head now points to this new prim
 *
 * Despite the parameter type (tagPOLY_FT4*), only the first 4 bytes
 * (the universal PS1 primitive "tag" field, shared by every GPU
 * primitive struct) are touched -- nothing POLY_FT4-specific.
 *
 * `ctx` is the already-resolved context base pointer (this
 * function's own "ldr r3,[r7,r3]; ldr r3,[r3]" GOT-pointer-variable
 * chain, a trivial single dereference not re-derived here); `+0x8`
 * within it is the OT head slot this function reads and overwrites.
 * `prim`'s own address is only ever stored into ctx+0x8..+0xb as
 * raw bytes (never dereferenced back out by this function), so no
 * host/ARM pointer-width issue arises from writing it there -- see
 * test_t23_addlocalprim2.c for why the raw stored bytes are still
 * not compared as a cross-architecture number.
 */
#include <stdint.h>

void addlocalprim2_model(uint8_t *prim, uint8_t *ctx) {
    uint32_t old_tag = (uint32_t)ctx[8] | ((uint32_t)ctx[9] << 8) |
                        ((uint32_t)ctx[10] << 16) | ((uint32_t)ctx[11] << 24);
    prim[0] = (uint8_t)(old_tag & 0xff);
    prim[1] = (uint8_t)((old_tag >> 8) & 0xff);
    prim[2] = (uint8_t)((old_tag >> 16) & 0xff);
    prim[3] = (uint8_t)((old_tag >> 24) & 0xff);

    uint32_t prim_addr = (uint32_t)(uintptr_t)prim;
    ctx[8] = (uint8_t)(prim_addr & 0xff);
    ctx[9] = (uint8_t)((prim_addr >> 8) & 0xff);
    ctx[10] = (uint8_t)((prim_addr >> 16) & 0xff);
    ctx[11] = (uint8_t)((prim_addr >> 24) & 0xff);
}
