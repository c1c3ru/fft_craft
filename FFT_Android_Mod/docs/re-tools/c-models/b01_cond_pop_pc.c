/* Independent C11 model of conditional A32 LDMIA SP!, {...,PC}.
 * Does NOT model the real caller's stack-frame layout.
 */
#include <stdint.h>
#include <stddef.h>

extern int b01_pop_pc_model(uint32_t opcode, uint32_t regs[16],
                           const uint8_t *stack, size_t stack_size,
                           uint32_t *return_pc);

static int check_cond(unsigned c, uint32_t cpsr) {
    const unsigned n=(cpsr>>31)&1u, z=(cpsr>>30)&1u;
    const unsigned carry=(cpsr>>29)&1u, v=(cpsr>>28)&1u;
    switch (c) {
    case 0: return z != 0u;
    case 1: return z == 0u;
    case 2: return carry != 0u;
    case 3: return carry == 0u;
    case 4: return n != 0u;
    case 5: return n == 0u;
    case 6: return v != 0u;
    case 7: return v == 0u;
    case 8: return carry && !z;
    case 9: return !carry || z;
    case 10: return n == v;
    case 11: return n != v;
    case 12: return !z && (n==v);
    case 13: return z || (n!=v);
    case 14: return 1;
    default: return -1;
    }
}

int b01_cond_pop_pc_model(uint32_t opcode, uint32_t regs[16],
                          const uint8_t *stack, size_t length,
                          uint32_t cpsr, uint32_t current_pc,
                          uint32_t *next_pc, int *did_return) {
    if (!regs || !stack || !next_pc || !did_return)
        return -1;
    if ((opcode & 0x0fff0000u) != 0x08bd0000u ||
        !(opcode & 0x8000u) || (opcode & 0x2000u) ||
        (opcode >> 28) == 15u || current_pc > UINT32_MAX - 4u)
        return -2;
    const int execute=check_cond((opcode>>28)&15u,cpsr);
    if (execute<0)
        return -3;
    if (!execute) {
        regs[15]=current_pc+4u;
        *next_pc=current_pc+4u;
        *did_return=0;
        return 0;
    }
    uint32_t returned=0;
    const int result=b01_pop_pc_model((opcode & 0x0fffffffu) |
                                      0xe0000000u,
                                      regs,stack,length,&returned);
    if (result != 0)
        return result;
    *next_pc=returned;
    *did_return=1;
    return 0;
}
