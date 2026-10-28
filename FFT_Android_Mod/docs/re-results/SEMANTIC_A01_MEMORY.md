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

A **A02** está liberada após esta A01: priorizar nove sequências operação+salto (`00072910`, `00082404`, `0008240c`, `000a94bc`, `000b4700`, `000b6c68`, `000b6cd0`, `000b6ee0`, `000b6ee8`), um `LDR+B` (`000b6f80`) e o auto-loop `002a1268`. Testar somente prefixos até antes dos destinos, com contratos específicos e limite de execução; não entrar em saltos próprios ou destinos desconhecidos. Não entrar em destinos desconhecidos ou em loop infinito.

**Resultado confirmado no ELF original:** [workflow #40730706242](https://github.com/c1c3ru/fft_craft/actions/runs/40730706242), commit `a6a2670d1ad1717135a92516840b123595fd1e2d`, artifact `real-elf-250-static-audit` ID `12833619024`: **21 entradas previamente não executadas auditadas, 10 rotinas novas microexecutadas em 320 cenários**, sendo **2 STRB, 1 LDRB e 7 LDR de offsets maiores**. O CI verificou `A01_FAILED=0`, `A01_NEW_CERTIFICATES=0` e que o checkpoint foi idêntico após a reexecução integral. Os 11 outros endereços não foram executados porque possuem saltos/fluxos não abrangidos pelo contrato. **Total acumulado do lote 250: 239 entradas com testes locais**, sem transformar microexecuções em certificados.

**Limites:** estas são verificações **locais sob estados sintéticos**, não prova da função completa, de equivalência do app, de valores reais em Android nem de reconstrução C/C++ integral. Os 303 certificados prévios não mudam.
