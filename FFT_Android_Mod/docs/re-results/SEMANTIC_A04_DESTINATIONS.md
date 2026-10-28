# A04 — análise dos destinos A32 após os saltos verificados

**Base:** [A02 / 352 testes delimitados](SEMANTIC_A02_BRANCHES.md), issue [#388](https://github.com/c1c3ru/fft_craft/issues/388). ELF original SHA256 `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Objetivo desta rodada

Desmontar, com proveniência verificável, os primeiros blocos candidatos de **sete destinos distintos**, total de dez entradas ARM externas. A análise ocorre diretamente nos bytes do segmento PT_LOAD executável do ELF original. Para cada destino, registrar 96 bytes, sequência A32 até o primeiro salto/chamada/retorno (ou 24 instruções), predecessores e referências de fluxo.

- `0x000b6c58` — quatro entradas com `R2=0..3`: primeira prioridade para reconstruir o dispatcher e seus efeitos.
- `0x000714dc` e `0x000714e8` — entradas de `MOV` e `MUL` vindas de `0x0008240c` e `0x00082404`.
- `0x002b1bb0` — entrada após `MOV R0,R2`.
- `0x000ab674` — entrada após `ADD R0,R0,#0x1c`.
- `0x000b461c` — entrada após `MOV R1,#0`.
- `0x000b8a18` — entrada após `LDR R0,[R0]`.

A entrada `0x002a1268` tem um salto para si mesma, sem terminação ou alcançabilidade dinâmica demonstradas. Não será executada indefinidamente.

## Validação conservadora

O analisador `semantic_a04_destinations.py` verifica SHA do ELF e bytes originais de **todas as 11 fontes A02**, usa Capstone para um scan linear delimitado dos sete destinos, grava checkpoint JSON, repete integralmente e exige reprodução idêntica. Não afirma que um segmento executável contém só código — uma desmontagem linear pode atravessar *inline data*. A auditoria não executa destinos nem promove certificados.

**Resultado de CI confirmado:** [run #40748750630](https://github.com/c1c3ru/fft_craft/actions/runs/40748750630), artefato `real-elf-250-static-audit` ID `12841958525`, commit `ef66bf648ac5f2a9c2e7b28f2cba3032630c39ee`: **sete destinos únicos, 672 bytes reais inspecionados, zero destinos executados, zero certificados criados e checkpoint revalidado sem diferenças**.

### Primeiros blocos efetivamente observados no ELF

| Destino | Prefixo original A32 | Fronteira ainda desconhecida |
|---|---|---|
| `000714dc` | `ADD IP,PC,#0x200000`; `ADD IP,IP,#0xd6000`; `LDR PC,[IP,#0x8a0]!` | Salto indireto via ponteiro/tabela; destino runtime não provado |
| `000714e8` | Mesmo padrão, `LDR PC,[IP,#0x898]!` | Salto indireto; destino runtime não provado |
| `000ab674` | Prólogo `PUSH` de nove registradores; acesso a dados e `BL 0x000b6620` | Efeitos do callee ainda desconhecidos |
| `000b461c` | `PUSH {r4,r5,r6,lr}`; `MOV R5,R0`; `MOV R4,R1`; `BL 0x000b45d0` | Efeitos do callee ainda desconhecidos |
| `000b6c58` | `LDR R3,[R0,#8]`; `ADD R2,R2,R1,LSL#2`; `LDR R0,[R3,R2,LSL#2]`; `BX LR` | Candidato a dispatcher indexado, ainda sem valores reais de runtime |
| `000b8a18` | `LDR R0,[R0,#8]`; `BX LR` | Getter local, ainda sem valores reais de runtime |
| `002b1bb0` | `SUBS R2,R0,#0`; `BXNE LR` | Caminho alternativo quando condição não atendida ainda desconhecido |

Os dois primeiros destinos têm características de veneers/PLT, mas são apenas **candidatos**; a natureza do símbolo e a relocação precisam ser verificadas, não inferidas a partir da instrução isolada. Os dois alvos curtos com `BX LR` permitem iniciar a primeira execução diferencial além do salto A02.

## Próximos ciclos da A04

1. Consultar o relatório real gerado no CI, definir fronteiras de blocos, identificar possíveis dados, instruções condicionais, acessos à memória e destinos adicionais por função.
2. Construir oráculos independentes e microexecuções com estado controlado apenas para blocos de efeito compreendido. Desvios complexos e tabelas precisam de contratos explicitamente isolados.
3. Construir CFG de caminhos relevantes e contratos entre caller e target; só então comparar o comportamento C/C++ e efeitos de estado em fluxos completos.
4. Classificar o auto-loop por contexto/reachability, sem inventar terminação ou chamar salto local de função reconstruída.

A04 permanece **em andamento** após a auditoria estática, pois sua conclusão exige CFG e contratos semânticos de cada destino. Os 303 certificados existentes não sofrem alteração.
