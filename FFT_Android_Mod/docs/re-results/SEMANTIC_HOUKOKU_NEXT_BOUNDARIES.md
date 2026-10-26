# Próximos destinos ARM de houkoku_okng — auditoria estática

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

> Esta auditoria apenas decodifica janelas de instruções do ELF original. **Não executa os destinos nem certifica contratos**.

## sound_request branch destination

- Origem do desvio: `0x26b374` — `b #0x2168e0`
- Próximo destino: `0x2168e0`
- SHA-256 da janela: `ed63a1720ad39f4363f32685c44d246dc7696acd47200368634842691eaf68c1`

| Endereço | Instrução ARM |
|---|---|
| `0x2168e0` | `b #0x271314` |
| `0x2168e4` | `b #0x27131c` |
| `0x2168e8` | `ldr r3, [pc, #8]` |
| `0x2168ec` | `ldr r3, [pc, r3]` |
| `0x2168f0` | `str r0, [r3]` |
| `0x2168f4` | `b #0x271318` |
| `0x2168f8` | `andseq r0, r3, r4, lsr lr` |
| `0x2168fc` | `bx lr` |

Continuação da execução, estados de entrada, efeitos indiretos e valores de retorno **não verificados**.

## iOS_setV2Icon special destination

- Origem do desvio: `0x2b9cc4` — `b #0x2b8900`
- Próximo destino: `0x2b8900`
- SHA-256 da janela: `e594bf0914592d3db3c5494af7751b1dc8016800ffaa94cb5973ac9c27b1ffe3`

| Endereço | Instrução ARM |
|---|---|
| `0x2b8900` | `push {r4, r5, r6, r7, r8, sb, sl, fp, lr}` |
| `0x2b8904` | `ldr r3, [pc, #0xff8]` |
| `0x2b8908` | `sub sp, sp, #0x24` |
| `0x2b890c` | `ldr sl, [pc, #0xff4]` |
| `0x2b8910` | `add r3, pc, r3` |
| `0x2b8914` | `str r3, [sp, #0xc]` |
| `0x2b8918` | `ldr r2, [sp, #0xc]` |
| `0x2b891c` | `ldr r3, [pc, #0xfe8]` |

Continuação da execução, estados de entrada, efeitos indiretos e valores de retorno **não verificados**.

