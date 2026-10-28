# A04 — dois saltos indiretos ARM via GOT: execução delimitada

ELF original SHA256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

A [auditoria estática A04](SEMANTIC_A04_DESTINATIONS.md) identificou duas sequências de três instruções ARM, alcançadas pelas entradas A02 `0x0008240c` (`MOV R0,R1`) e `0x00082404` (`MUL R0,R2,R1`).

| Entrada A02 | Veneer A04 | Instrução final | Endereço sintético de leitura |
|---|---|---|---|
| `0008240c` | `000714dc` | `LDR PC,[IP,#0x8a0]!` | `00347d84` |
| `00082404` | `000714e8` | `LDR PC,[IP,#0x898]!` | `00347d88` |

Os dois veneers executam primeiro `ADD IP,PC,#0x200000` e `ADD IP,IP,#0xd6000`. Para cada fonte, o analisador `semantic_a04_veneer_exec.py` calcula `PC=A+8` no início do veneer, soma os deslocamentos e compara o valor de `IP` após o *writeback* da leitura indireta.

### Limites e protocolo

Somente os 8 bytes originais de `MOV/MUL+B` e os 12 bytes originais de cada veneer são carregados no Unicorn. A região de tabela de ponteiros é **sintética**; seu slot contém endereço de armadilha conhecido e mapeado. O hook de instrução interrompe a emulação **antes** da primeira instrução do destino indireto. Nenhum endereço de callee real nem relocação do linker Android é inferido.

Oráculo independente: R0 depois do `MOV` ou `MUL`, R12/IP igual ao slot pós-writeback, preservação dos demais registradores e NZCV, SP/LR, PC no destino sintético, uma leitura de 32 bits do slot, nenhuma escrita na tabela e trace completo. O CI exige 8 seeds × 4 conjuntos de flags × 2 veneers = **64 execuções locais**, checkpoint idempotente e zero certificados.

**Validação confirmada no ELF original:** [GitHub Actions run #40751407523](https://github.com/c1c3ru/fft_craft/actions/runs/40751407523), artefato `real-elf-250-static-audit` ID `12843668897`, commit `312fafc518e092c1ec759e33ace2d15ddf0dc3c5`. Foram **64 execuções diferenciais**, dois slots GOT/IP verificados, zero diferenças, zero destinos indiretos externos executados e zero certificados criados. O segundo processamento reproduziu o mesmo checkpoint byte por byte. Isto demonstra somente os efeitos originais sob memória sintética, não o destino real das resoluções de linker. A04 continua em andamento.

### Próximas fronteiras

O destino real de cada `LDR PC` em runtime depende de relocação/GOT e precisa ser observado ou reconstruído. Permanecem também os blocos com prólogo/BL em `0x000ab674`, `0x000b461c`, o retorno condicional em `0x002b1bb0` e a alcançabilidade do auto-loop `0x002a1268`. Nada disso é certificado por testes do prefixo.
