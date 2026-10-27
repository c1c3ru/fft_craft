# SysSE_PlayDef: auditoria estática da entrada A32 0x2b2cf8

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`
Janela A32: `0x2b2cf8..0x2b2d77` (128 bytes).
SHA-256 da janela: `75d51dbbb22c92e4ffcb59bc162ead48289fb1847bf608526c5cfd29d70444b1`.

## Proveniência

A cadeia 0x26b374 -> 0x2168e0 -> 0x271314 -> 0x2b2cf8 foi previamente microexecutada **somente até antes da instrução no destino**.
O script valida novamente os opcodes originais dos trampolins.

## Desmontagem linear (não constitui CFG validado)

| Endereço | Bytes | A32 | Marcadores conservadores |
|---|---|---|---|
| 0x2b2cf8 | `0010a0e1` | `mov r1, r0` | ordinary/undetermined |
| 0x2b2cfc | `0000a0e3` | `mov r0, #0` | ordinary/undetermined |
| 0x2b2d00 | `9dffffea` | `b #0x2b2b7c` | jump, target=0x2b2b7c |
| 0x2b2d04 | `0010a0e1` | `mov r1, r0` | ordinary/undetermined |
| 0x2b2d08 | `0100a0e3` | `mov r0, #1` | ordinary/undetermined |
| 0x2b2d0c | `9affffea` | `b #0x2b2b7c` | jump, target=0x2b2b7c |
| 0x2b2d10 | `f0432de9` | `push {r4, r5, r6, r7, r8, sb, lr}` | ordinary/undetermined |
| 0x2b2d14 | `18319fe5` | `ldr r3, [pc, #0x118]` | memory |
| 0x2b2d18 | `24d04de2` | `sub sp, sp, #0x24` | ordinary/undetermined |
| 0x2b2d1c | `0040a0e1` | `mov r4, r0` | ordinary/undetermined |
| 0x2b2d20 | `2810a0e3` | `mov r1, #0x28` | ordinary/undetermined |
| 0x2b2d24 | `03009fe7` | `ldr r0, [pc, r3]` | memory |
| 0x2b2d28 | `7c65ffeb` | `bl #0x28c320` | call, jump, target=0x28c320 |
| 0x2b2d2c | `000050e3` | `cmp r0, #0` | ordinary/undetermined |
| 0x2b2d30 | `0200000a` | `beq #0x2b2d40` | jump, target=0x2b2d40 |
| 0x2b2d34 | `013044e2` | `sub r3, r4, #1` | ordinary/undetermined |
| 0x2b2d38 | `040053e3` | `cmp r3, #4` | ordinary/undetermined |
| 0x2b2d3c | `0100009a` | `bls #0x2b2d48` | jump, target=0x2b2d48 |
| 0x2b2d40 | `24d08de2` | `add sp, sp, #0x24` | ordinary/undetermined |
| 0x2b2d44 | `f083bde8` | `pop {r4, r5, r6, r7, r8, sb, pc}` | possible-return, pc-register |
| 0x2b2d48 | `e8309fe5` | `ldr r3, [pc, #0xe8]` | memory |
| 0x2b2d4c | `e8609fe5` | `ldr r6, [pc, #0xe8]` | memory |
| 0x2b2d50 | `2b4084e2` | `add r4, r4, #0x2b` | ordinary/undetermined |
| 0x2b2d54 | `03309fe7` | `ldr r3, [pc, r3]` | memory |
| 0x2b2d58 | `085093e5` | `ldr r5, [r3, #8]` | memory |
| 0x2b2d5c | `06609fe7` | `ldr r6, [pc, r6]` | memory |
| 0x2b2d60 | `0410a0e1` | `mov r1, r4` | ordinary/undetermined |
| 0x2b2d64 | `0500a0e1` | `mov r0, r5` | ordinary/undetermined |
| 0x2b2d68 | `008096e5` | `ldr r8, [r6]` | memory |
| 0x2b2d6c | `bd0ff8eb` | `bl #0xb6c68` | call, jump, target=0xb6c68 |
| 0x2b2d70 | `0410a0e1` | `mov r1, r4` | ordinary/undetermined |
| 0x2b2d74 | `0090a0e1` | `mov sb, r0` | ordinary/undetermined |

## Limites de evidência

- **Nenhuma instrução de SysSE_PlayDef foi executada** neste relatório.
- Uma desmontagem linear pode conter dados inline; ramos condicionais, chamadas, acessos a memória e retornos exigem rastreamento separado.
- Não se inferem parâmetros, semântica do áudio, estado global ou retornos.
- Nenhuma função adicional é certificada; continuam 303 registros semânticos preexistentes, sujeitos à própria política de certificação.
- Próximo experimento: executar bloco básico somente com memória mapeada do ELF e hooks de memória, parando **antes** de BL/BX/PC indireto, syscall, leitura não inicializada ou escrita externa.
