/* B01 independent C11 three-A32-opcode bounded path model.
 * First two opcodes: checked ALU + controlled memory (two_op.c);
 * third: unconditional ALU S=0 into R1..R12, or exact BX LR.
 * This model is NOT a complete ARM core or proof of function identity.
 */
#include <stddef.h>
#include <stdint.h>

extern int b01_two_op_model(uint32_t first, uint32_t second,
                            uint32_t regs[13], uint8_t *mem, size_t size);

static uint32_t rotate_right(uint32_t val, unsigned shift) {
    shift &= 31u;
    return shift ? ((val >> shift) | (val << (32u - shift))) : val;
}

int b01_three_op_model(uint32_t first, uint32_t second, uint32_t third,
                       uint32_t regs[13], uint8_t *memory, size_t size,
                       uint32_t entry, uint32_t lr,
                       uint32_t *expected_pc, int *returned) {
    if (!regs || !memory || !expected_pc || !returned)
        return -1;
    if (entry > UINT32_MAX - 12u)
        return -2;
    const int is_return = third == 0xe12fff1eu;
    const unsigned operation = (third >> 21) & 15u;
    const unsigned dest = (third >> 12) & 15u;
    const unsigned src = (third >> 16) & 15u;
    uint32_t operand = 0;
    if (!is_return) {
        if ((third >> 28) != 14u || ((third >> 26) & 3u) != 0u ||
            ((third >> 20) & 1u) ||
            !(operation == 0u || operation == 1u || operation == 2u ||
              operation == 4u || operation == 12u || operation == 13u) ||
            dest == 0u || dest > 12u || (operation != 13u && src > 12u))
            return -3;
        if ((third >> 25) & 1u) {
            operand = rotate_right(third & 255u, 2u * ((third >> 8) & 15u));
        } else {
            if ((third & 0xff0u) || (third & 15u) > 12u)
                return -4;
            operand = regs[third & 15u];
        }
    }
    const int result = b01_two_op_model(first, second, regs, memory, size);
    if (result != 0)
        return result - 10;
    *returned = is_return ? 1 : 0;
    *expected_pc = is_return ? lr : entry + 12u;
    if (!is_return) {
        /* For register operands, fetch AFTER the first two operations.
         * Register dependencies are real; do not reuse a stale value. */
        if (!((third >> 25) & 1u))
            operand = regs[third & 15u];
        const uint32_t lhs = operation == 13u ? 0u : regs[src];
        uint32_t value;
        switch (operation) {
        case 0: value = lhs & operand; break;
        case 1: value = lhs ^ operand; break;
        case 2: value = lhs - operand; break;
        case 4: value = lhs + operand; break;
        case 12: value = lhs | operand; break;
        case 13: value = operand; break;
        default: return -5;
        }
        regs[dest] = value;
    }
    return 0;
}
