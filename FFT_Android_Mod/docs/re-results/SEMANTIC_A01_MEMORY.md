# A01 — memória ARM byte e palavra deslocada (issue #388)

**ELF original SHA-256:** `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

**Objetivo de engenharia de loop:** prosseguir após as 216 entradas A32 do lote estático e os 13 casos `STR/BX LR` com checkpoint imutável, cobrindo contratos conservadores dos 21 opcodes ainda excluídos.

## Contratos deliberadamente estreitos

- `STRB R1,[R0,#imm]` A32, AL, offset positivo, pré-indexado e sem writeback (endereços `000a9404` e `000b1ad4`). Verificar escrita de **1 byte**, preservação de vizinhos, R0–R12, SP/LR e CPSR.
- `LDRB R0,[R0,#4]` A32 com extensão para zero (endereço `000b1acc`). Verificar leitura de 1 byte sem escrita.
- `LDR R0,[R0,#imm]` A32 de offsets maiores (endereços `000ad8d0`, `000ae088`, `000af110`, `000af118`, `000b67b0`, `000b682c`, `000b6ac4`). Verificar leitura alinhada de 4 bytes, sem mutação.
- Todos devem terminar com `BX LR`; recusar PC como fonte/base, condicional, endereçamento negativo, writeback, acessos fora da região segura e fluxos desconhecidos. Usar Capstone e bytes lidos do PT_LOAD executável do ELF real.

**Validação:** 8 seeds × 4 estados NZCV = 32 testes diferenciais por entrada, memória sintética com sentinela e comparação byte a byte da região completa, eventos de leitura/escrita, registradores e PC. Checkpoint contém hash do ELF, hash do inventário, hash do checkpoint anterior e evidências por endereço; reexecução compara JSON byte a byte. Nenhum novo certificado.

## Próximas atividades após A01

A **A02** depende de A01. Restarão as sequências com operações e salto, `LDR+B` e `B` que retorna ao próprio endereço, para contratos específicos de prefixos com limite de execução e tratamento explícito de destinos. Não entrar em destinos desconhecidos ou em loop infinito.

**Resultado da rodada A01:** pendente de confirmação pelo CI do PR. Os 10 endereços acima são candidatos; as 320 microexecuções são um gate esperado, não evidência de execução até o workflow confirmar.

**Limites:** estas são verificações **locais sob estados sintéticos**, não prova da função completa, de equivalência do app, de valores reais em Android nem de reconstrução C/C++ integral. Os 303 certificados prévios não mudam.
