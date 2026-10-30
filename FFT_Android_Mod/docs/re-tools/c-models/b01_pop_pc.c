/* B01 isolated A32 POP {...,PC} model. This is not a call/stack-frame model. */
#include <stddef.h>
#include <stdint.h>

int b01_pop_pc_model(uint32_t opcode, uint32_t regs[16],
                     const uint8_t *stack, size_t stack_size,
                     uint32_t *return_pc) {
    if (!regs || !stack || !return_pc)
        return -1;
    /* AL-condition LDMIA SP! ({reglist}); force PC, disallow loading SP. */
    if ((opcode & 0xffff0000u) != 0xe8bd0000u ||
        !(opcode & 0x8000u) || (opcode & 0x2000u))
        return -2;
    const uint32_t reglist = opcode & 0xffffu;
    size_t bytes = 0;
    for (unsigned i=0;i<16u;i++)
        if ((reglist >> i) & 1u)
            bytes += 4u;
    if (bytes == 0 || bytes > stack_size)
        return -3;
    uint32_t vals[16] = {0};
    size_t pos = 0;
    for (unsigned i=0;i<16u;i++) {
        if (!(reglist & (1u << i)))
            continue;
        vals[i] = ((uint32_t)stack[pos]) |
                  ((uint32_t)stack[pos+1] << 8) |
                  ((uint32_t)stack[pos+2] << 16) |
                  ((uint32_t)stack[pos+3] << 24);
        pos += 4u;
    }
    const uint32_t old_sp = regs[13];
    if (old_sp > UINT32_MAX - (uint32_t)bytes)
        return -4;
    for (unsigned i=0;i<16u;i++)
        if (reglist & (1u << i))
            regs[i] = vals[i];
    regs[13] = old_sp + (uint32_t)bytes;
    *return_pc = vals[15];
    return 0;
}
