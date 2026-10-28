# Loop completo dos candidatos A32 — lote original de 250 tarefas

**Entrada verificada:** ELF `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`; 25 manifestos; 250 relatórios `static_bounded` verificados por reinspeção.

## Objetivo

Avançar além da [primeira rodada de 24 candidatos e 768 cenários](SEMANTIC_LOOP_250.md). O workflow [Real ELF semantic manifest audit (250)](https://github.com/c1c3ru/fft_craft/actions/workflows/re-semantic-real-elf-250.yml) executa `semantic_loop_250.py` novamente com `--max-candidates 250 --round-size 16`, sem alterar certificados.

Na rodada anterior, 216 entradas atendiam aos contratos restritos do analisador, mas só 24 foram testadas. O novo gate deve selecionar todos os candidatos elegíveis e conferir `LOOP_FULL_DIFFERENTIAL_PASSED == LOOP_FULL_ENTRIES × 32`. A expectativa para os mesmos insumos é **216 × 32 = 6.912 microexecuções**; a contagem efetiva será registrada somente após sucesso do CI.

## Engenharia de loop

1. Validar hash do ELF, integridade dos 25 manifestos e as 250 saídas estáticas.
2. Selecionar apenas instruções A32 cujo comportamento restrito já é modelado, incluindo funções-folha de duas palavras e saltos isolados até antes do alvo.
3. Executar 32 estados determinísticos por candidato com Unicorn, comparando efeitos locais com o modelo Python independente.
4. Persistir checkpoints por rodada de até 16 entradas, repetir toda a microexecução e exigir que o checkpoint continue byte a byte idêntico.
5. Armazenar logs, relatórios e checkpoints no artifact `real-elf-250-static-audit`; nunca alterar `semantic-certificates.json`.

## Limites e próximo ciclo

Esta etapa **não certifica funções inteiras nem conclui o aplicativo**. Não executa destinos de saltos ou funções chamadas e não modela toda a memória, estados reais de Android, efeitos externos nem desvios condicionais arbitrários. As entradas não elegíveis ficam na fila para ampliação futura de contratos.

**Resultado do CI da expansão:** [workflow #40713115396](https://github.com/c1c3ru/fft_craft/actions/runs/40713115396), artifact `real-elf-250-static-audit` ID `12827346883` e commit `48c2db517267354054313133063a3ecc17045051`: **216 candidatos elegíveis selecionados, 14 rodadas, 6.912 microexecuções diferenciais aprovadas, zero falhas e zero novos certificados**. A repetição integral reproduziu byte a byte o mesmo checkpoint (comparação `cmp` no job). O artefato auditado contém **169 prefixos de salto A32** (o destino não é executado) e **47 funções-folha de duas palavras**, classificadas em **22 MOV, 16 LDR e 9 ADD**. As **34 entradas restantes** do lote foram excluídas por opcodes ou efeitos ainda não modelados. Esta é evidência local e parcial, não 216 funções completas.
