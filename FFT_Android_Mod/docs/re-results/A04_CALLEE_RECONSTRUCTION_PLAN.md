# Ciclo A04 — aprofundamento dos callees

O alvo agora é **0x000b6620** e **0x000b45d0**: o pipeline analisa janelas ELF A32 originais de 512 bytes por entrada e emite instruções, candidatos a CFG, BL/BLX, acesso à memória e fronteiras desconhecidas. O relatório real é publicado como artefato de CI `a04-callee-original-elf-cfg`; não use esse inventário como prova de fluxo executado.

## Contratos iniciais

| Destino | Entradas | Efeitos ainda não determinados | Reimplementação |
|---|---|---|---|
| `0x000b6620` | contexto do BL alcançado a partir de `0x000ab674` | R0–R12, SP/LR, CPSR, globais, leituras/escritas, retornos, subchamadas | **Bloqueada** |
| `0x000b45d0` | contexto do BL em `0x000b461c`; prefixo anterior já testado | alterações do callee sobre pilha/estado, subchamadas e caminho de retorno | **Bloqueada** |

A informação de valores reais de registradores e ponteiros nas duas entradas **não está demonstrada**. O analisador separa candidatos e desconhecidos em vez de afirmar contratos fictícios. O primeiro teste executável só deve atravessar instruções cujos efeitos estejam integralmente modelados. O modelo C/C++ independente deve reproduzir um bloco comprovado antes de tentar substituir a rotina completa.

## Engenharia de loop

1. **Observar:** rodar o job com SHA fixo e consultar o relatório de CFG do ELF original.
2. **Decidir:** localizar o primeiro efeito não modelado de cada callee (memória, BL, indireto ou ramo).
3. **Contratar:** definir entradas, flags, aliasing, limites de memória, escrita e retorno.
4. **Implementar:** modelo C do primeiro bloco cujo comportamento tenha sido comprovado no ELF.
5. **Comparar:** testar Unicorn × C com os mesmos estados e sentinelas; persistir checkpoints reproduzíveis.
6. **Avançar:** ampliar por bloco, não por contagem de instruções; conservar status `in_progress` até demonstrar o caminho completo.

Não foram criados certificados nem declarada equivalência das duas funções.
