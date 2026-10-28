# Issue #388 — próximos 34 endereços ARM, microexecução conservadora

## Origem

O [run #40713115396](https://github.com/c1c3ru/fft_craft/actions/runs/40713115396) auditou 250 tarefas do ELF original e executou 216 candidatos elegíveis em 6.912 cenários, sem falhas. Permanecem 34 funções não modeladas: 33 entradas de 8 bytes e uma de 4 bytes, das quais 15 tiveram candidatos estáticos de escrita. O hash original do ELF é `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Contrato do novo loop

O arquivo `docs/re-tools/semantic_remaining_34.py` calcula o complemento exato dos endereços registrados no checkpoint de 216 funções contra os 250 manifestos. Classifica e documenta **cada um dos 34 endereços**, incluindo bytes originais, instruções Capstone e motivo da exclusão.

O executor só aceita `STR` A32 incondicional, palavra de 32 bits, endereço pré-indexado com deslocamento positivo, sem writeback, bases e fontes R0–R3 e retorno `BX LR`. Para cada candidato reconhecido, executa **32 estados sintéticos** no Unicorn com limites de memória, sentinelas, rastreamento de escrita, preservação de registradores e CPSR, comparação a referência Python independente e parada antes do retorno externo.

O workflow `re-semantic-real-elf-250.yml` executa classificação, microexecução dos candidatos aprovados, checkpoints por até 8 funções, repetição integral e comparação byte a byte do checkpoint. O resultado completo será publicado no artefato `real-elf-250-static-audit`, nos arquivos `SEMANTIC_REMAINING_34.md` e `semantic-remaining-34-checkpoint.json`, se houver entradas executáveis.

## Estado

**Execução da nova etapa:** ainda não confirmada pelo CI deste PR. As 34 entradas não devem ser consideradas equivalentes nem executadas até que as métricas do run real sejam auditadas.

Os certificados semânticos (303) não são alterados. Persistem limitações de estados sintéticos, aliasing real, efeitos externos e reconstrução de funções complexas.
