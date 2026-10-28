# A04 — fronteiras BL no ELF original, com prólogo delimitado

**ELF SHA-256:** `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Escopo do ciclo

A partir dos sete destinos [A04](SEMANTIC_A04_DESTINATIONS.md), analisar dois blocos que contém chamada direta:

| Bloco A04 | BL original esperado | Estado atual |
|---|---|---|
| `000ab674` | `000b6620` | Próximo alvo: prólogo com nove registros, acesso global e chamada não modelada |
| `000b461c` | `000b45d0` | Candidato de teste: entrada `000b4700` + prólogo PUSH/MOV, parada **antes** de BL |

O novo `semantic_a04_bl_boundaries.py` compara o SHA original, exige o checkpoint A04 dos sete destinos, confirma as onze fontes A02 e desmonta **96 bytes originais** de cada bloco BL, de seus dois possíveis callees, de duas continuações após o BL e do fallthrough `002b1bb8`. São **7 locais / 672 bytes** de análise estática delimitada; não declarar `code/data` provado só por estar em PT_LOAD executável.

No bloco `000b461c`, o candidato simples é `PUSH {r4,r5,r6,lr}; MOV r5,r0; MOV r4,r1; BL 000b45d0`. O fluxo inicial de `000b4700` prepara `R1=0` antes do desvio. Os testes usam bytes originais exatos e verificam, sob memória sintética: os quatro valores gravados pela PUSH, SP, R0–R12, LR, flags NZCV e a preservação de toda a memória fora dessas escritas. A execução interrompe no PC da instrução BL, **sem executar a chamada**.

**Gate previsto no CI:** 2 BL originais, 672 bytes auditados, 8 seeds × 4 flags = **32 microexecuções limitadas**, zero destinos de BL executados, zero falhas, zero certificados e checkpoint byte a byte reproduzível. Este número é uma expectativa até a confirmação do workflow.

## Próximas atividades

1. Com os bytes/CFG levantados, reconstruir os efeitos do callee `000b45d0`, incluindo o estado empilhado e os efeitos de memória, antes de permitir execução além da chamada.
2. Modelar os globais e registradores no bloco `000ab674`; depois, o `BL 000b6620` e seu retorno.
3. Analisar o caminho condicional `002b1bb8`, verificar os destinos reais dos veneers GOT e determinar a alcançabilidade do auto-loop `002a1268`.
4. Reimplementar apenas contratos fechados em C/C++ e comparar com o original até a mesma fronteira.

**A04 continua em andamento.** Nenhum resultado de execução local implica equivalência de função ou conclusão do aplicativo.
