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


## Ciclo seguinte — candidato semântico 0x000b45d0

A desmontagem no ELF original, verificada pelo run #40867844255, revelou uma rotina sem BL:
`MOV R3,#12; MUL R1,R3,R1; ADD R3,R0,R1; LDR R3,[R3,#0x14c]; CMN R3,#1; ADDNE R0,R0,R1; ADDNE R0,R0,#0x14c; MOVEQ R0,#0; BX LR`.

**Contrato proposto e limitado:** com R0 apontando para uma área sintética alinhada e índice R1 válido, a rotina lê a palavra em `R0 + 0x14c + 12*R1`, retornando zero se for `0xffffffff` ou o endereço dessa palavra caso contrário. O teste diferencial compara os valores finais de R0, R1, R3, R2 preservado, NZCV calculado independentemente, o único read de 4 bytes, nenhuma escrita de memória e a sequência completa de PCs. Usa seis índices × seis palavras × quatro flags = **144 casos pretendidos**.

Implementação C independente: `docs/re-tools/c-models/a04_index_slot.c`. Executor diferencial: `docs/re-tools/semantic_a04_leaf_differential.py`. O programa C valida os limites antes de ler. O original é emulado só com índices seguros, com bytes extraídos do ELF cuja identidade é fixada por SHA-256. O pipeline compila com `-Wall -Wextra -Werror` e exige zero divergências. Não há promoção para certificado formal nem cobertura de índices inválidos no ARM original.

**Importante:** a existência dos arquivos não é sucesso de execução; somente o status do GitHub Actions no commit final poderá fundamentar essa conclusão.
