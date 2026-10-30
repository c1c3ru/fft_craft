/* B01 independent, two-opcode A32 ALU -> memory model.
 *
 * Restricted to AL-condition non-flag-setting MOV/AND/EOR/SUB/ADD/ORR,
 * immediate or unshifted register operand, then LDR/STR/LDRB/STRB
 * [R0,#imm] preindexed, no writeback, with R1..R12 target.
 * No attempt to model calls, exceptions, stack or a complete function.
 */
#include <stddef.h>
#include <stdint.h>

#define MASK_CODE 3u
#define MEM_MAX_OFFSET 0x500u

static uint32_t ror32(uint32_t x, unsigned n) {
    n &= 31u;
    return n ? ((x >> n) | (x << (32u - n))) : x;
}

int b01_two_op_model(uint32_t first, uint32_t second,
                     uint32_t regs[13], uint8_t *mem, size_t size) {
    if (regs == NULL || mem == NULL || size == 0)
        return -1;
    if ((first >> 28) != 14u || ((first >> 26) & MASK_CODE) != 0u ||
        ((first >> 20) & 1u) != 0u)
        return -2;
    const unsigned op = (first >> 21) & 15u;
    if (!(op == 0u || op == 1u || op == 2u || op == 4u ||
          op == 12u || op == 13u))
        return -3;
    const unsigned rd = (first >> 12) & 15u;
    const unsigned rn = (first >> 16) & 15u;
    if (rd == 0u || rd > 12u || (op != 13u && rn > 12u))
        return -4;
    uint32_t operand;
    if ((first >> 25) & 1u) {
        operand = ror32(first & 255u, 2u * ((first >> 8) & 15u));
    } else {
        if ((first & 0xff0u) != 0u || (first & 15u) > 12u)
            return -5;
        operand = regs[first & 15u];
    }
    /* Data transfer: A32 immediate, pre-indexed, positive, no writeback. */
    if ((second >> 28) != 14u || ((second >> 26) & 3u) != 1u ||
        ((second >> 25) & 1u) || !((second >> 24) & 1u) ||
        !((second >> 23) & 1u) || ((second >> 21) & 1u) ||
        ((second >> 16) & 15u) != 0u)
        return -6;
    const unsigned rt = (second >> 12) & 15u;
    const unsigned offset = second & 0xfffu;
    const unsigned width = (second & (1u << 22)) ? 1u : 4u;
    const unsigned load = (second >> 20) & 1u;
    if (rt == 0u || rt > 12u || offset > MEM_MAX_OFFSET ||
        (width == 4u && (offset & 3u)) || (size < width) ||
        (offset > size - width))
        return -7;

    const uint32_t lhs = op == 13u ? 0u : regs[rn];
    uint32_t result = 0;
    switch (op) {
    case 0: result = lhs & operand; break;
    case 1: result = lhs ^ operand; break;
    case 2: result = lhs - operand; break;
    case 4: result = lhs + operand; break;
    case 12: result = lhs | operand; break;
    case 13: result = operand; break;
    default: return -8;
    }
    regs[rd] = result;

    if (load) {
        uint32_t value = 0;
        for (unsigned i = 0; i < width; ++i)
            value |= (uint32_t)mem[offset + i] << (8u * i);
        regs[rt] = value;
    } else {
        const uint32_t value = regs[rt];
        for (unsigned i = 0; i < width; ++i)
            mem[offset + i] = (uint8_t)((value >> (8u * i)) & 255u);
    }
    return 0;
}
