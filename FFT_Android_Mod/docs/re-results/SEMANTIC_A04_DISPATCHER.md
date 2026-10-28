# A04 — execução integrada do dispatcher ARM e getter (ELF original)

ELF original SHA256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Hipótese semântica a validar com estado controlado

O destino `0x000b6c58`, identificado pela [auditoria estática original](SEMANTIC_A04_DESTINATIONS.md), possui estes 4 opcodes A32:

```asm
000b6c58  ldr r3, [r0, #8]
000b6c5c  add r2, r2, r1, lsl #2
000b6c60  ldr r0, [r3, r2, lsl #2]
000b6c64  bx  lr
```

Quatro endereços A02 carregam `R2` com 0, 1, 2 e 3 antes de `B 0x000b6c58`, sem modificar o restante. Com `R0` apontando para um objeto sintético e `R1=row`, o contrato independente é:

- ler ponteiro para vetor de palavras em `R0+8`, guardando-o em `R3`;
- calcular `R2 = column + 4*row` com wrap-around ARM32;
- ler palavra em `vetor + 4*R2`, retorná-la em `R0`;
- retornar ao `LR` original, preservando demais registros, SP/LR, flags e memória.

O outro destino curto `0x000b8a18` tem `LDR R0,[R0,#8]` e `BX LR`. Será comparado a um modelo independente de leitura de 32 bits.

**Gate exigido pelo CI:** quatro callers originais × quatro valores de row × oito seeds × quatro estados NZCV = **512 testes integrados**; getter = **32 testes**; total esperado **544**. Comparar PC trace real, duas leituras esperadas no dispatcher, uma no getter, ausência de escrituras, conteúdo integral de regiões sintéticas e sentinelas, R0–R12, SP/LR, CPSR e checkpoint reprodutível. Nenhum certificado novo.

**Estado:** gate ainda não executado na revisão deste relatório. O pipeline registrará o resultado medido após o run real.

**Fronteiras não resolvidas:** cinco dos sete destinos ainda não foram microexecutados (`000714dc`, `000714e8`, `000ab674`, `000b461c`, `002b1bb0`); duas sequências são saltos indiretos, outras têm chamadas/pilhas/retorno condicional. O auto-loop `002a1268` segue sem reachability e terminação provadas. Nenhum cenário sintético estabelece equivalência global do jogo ou dos valores reais de Android.
