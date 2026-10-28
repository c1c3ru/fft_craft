# A02 — prefixos ARM e saltos diretos do ELF original

**Identidade do ELF:** SHA-256 `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

**Origem:** issue [#388](https://github.com/c1c3ru/fft_craft/issues/388); seguindo os checkpoints de 216 entradas A32, 13 STR e 10 STRB/LDRB/LDR já verificados. O analisador `semantic_a02_branch_11.py` exige os bytes originais exatos dos 11 remanescentes e valida os três checkpoints anteriores.

## Critério do ciclo de engenharia

- Dez entradas têm um opcode AL de `MOV`, `MUL`, `ADD` ou `LDR`, seguido de um `B` A32 incondicional. Verificar o primeiro opcode e o salto direto, sem executar qualquer instrução do destino.
- A entrada `0x002a1268` é um `B` para si mesma: executar **somente uma instrução** com limite no Unicorn. Isso prova o salto local, **não** a terminação nem o comportamento completo.
- Rejeitar qualquer mudança nos bytes originais; conferir desmontagem Capstone, endereço de destino A32/PC+8, PC, R0–R12, SP/LR, NZCV, leituras e gravações de memória, sentinelas e modelo Python independente.
- Para o `LDR R0,[R0]` em `0x000b6f80`, usar endereço mapeado e valores sintéticos controlados. Não assumir ponteiro real do jogo.
- Executar 8 seeds × 4 estados de flags em cada uma das 11 entradas, por checkpoints de até quatro entradas; repetir e comparar JSON byte a byte. Não adicionar certificados semânticos.

## Mapa de fronteiras, antes da execução

| Entrada(s) original(is) | Primeiro efeito | Destino do salto (NÃO executado) |
|---|---|---|
| `00072910` | `MOV R0,R2` | `002b1bb0` |
| `00082404` | `MUL R0,R2,R1` | `000714e8` |
| `0008240c` | `MOV R0,R1` | `000714dc` |
| `000a94bc` | `ADD R0,R0,#28` | `000ab674` |
| `000b4700` | `MOV R1,#0` | `000b461c` |
| `000b6c68`, `000b6cd0`, `000b6ee0`, `000b6ee8` | `MOV R2,#0..3` | `000b6c58` |
| `000b6f80` | `LDR R0,[R0]` | `000b8a18` |
| `002a1268` | `B` para si mesmo | `002a1268` (um passo apenas) |

**Há sete destinos externos únicos, ainda sem garantia de comportamento.** O mesmo destino `000b6c58` é compartilhado por quatro entradas com valores diferentes de R2, e a prova do primeiro salto não cobre o dispatcher que recebe esse estado.

**Estado nesta revisão:** esperando evidência do CI do ELF original. O gate esperado é 11 entradas, 352 execuções delimitadas, 0 destinos executados, 0 falhas e 0 novos certificados. Não afirmar equivalência de função completa.

## Próxima atividade após A02

**A04 — reconstruir os sete destinos externos de salto**, com prova code-vs-data, CFG, ABI e contratos entrada/saída, começando pelo dispatcher compartilhado `0x000b6c58`. O auto-loop exige explicação de reachability, função e contexto; não mascarar sua ausência de terminação. Os certificados existentes não serão alterados automaticamente.
