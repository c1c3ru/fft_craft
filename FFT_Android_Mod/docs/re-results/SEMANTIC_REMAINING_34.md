# Issue #388 — próximos 34 endereços ARM, microexecução conservadora

## Origem

O [run #40713115396](https://github.com/c1c3ru/fft_craft/actions/runs/40713115396) auditou 250 tarefas do ELF original e executou 216 candidatos elegíveis em 6.912 cenários, sem falhas. Permanecem 34 funções não modeladas: 33 entradas de 8 bytes e uma de 4 bytes, das quais 15 tiveram candidatos estáticos de escrita. O hash original do ELF é `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Contrato do novo loop

O arquivo `docs/re-tools/semantic_remaining_34.py` calcula o complemento exato dos endereços registrados no checkpoint de 216 funções contra os 250 manifestos. Classifica e documenta **cada um dos 34 endereços**, incluindo bytes originais, instruções Capstone e motivo da exclusão.

O executor só aceita `STR` A32 incondicional, palavra de 32 bits, endereço pré-indexado com deslocamento positivo, sem writeback, bases e fontes R0–R3 e retorno `BX LR`. Para cada candidato reconhecido, executa **32 estados sintéticos** no Unicorn com limites de memória, sentinelas, rastreamento de escrita, preservação de registradores e CPSR, comparação a referência Python independente e parada antes do retorno externo.

O workflow `re-semantic-real-elf-250.yml` executa classificação, microexecução dos candidatos aprovados, checkpoints por até 8 funções, repetição integral e comparação byte a byte do checkpoint. O resultado completo será publicado no artefato `real-elf-250-static-audit`, nos arquivos `SEMANTIC_REMAINING_34.md` e `semantic-remaining-34-checkpoint.json`, se houver entradas executáveis.

## Estado

**Execução confirmada no ELF real:** o job [Real ELF semantic manifest audit](https://github.com/c1c3ru/fft_craft/actions/runs/40718099438) catalogou **34 entradas**, executou **13 rotinas STR/BX LR** com **416 cenários diferenciais**, em **2 rodadas**. Todas as verificações de escrita, retorno e registradores passaram, e o checkpoint foi reproduzido na segunda execução (`REMAINING_34_FAILED=0`, `REMAINING_34_NEW_CERTIFICATES=0`). Evidências brutas: artifact `real-elf-250-static-audit` ID `12829627339`.

**21 entradas ainda sem modelo de execução**, registradas por endereço e bytes no arquivo `SEMANTIC_REMAINING_34.md` do artefato: dois `STRB/BX LR` (0x000a9404, 0x000b1ad4); sete `LDR/BX LR` com deslocamento maior que o limite original (0x000ad8d0, 0x000ae088, 0x000af110, 0x000af118, 0x000b67b0, 0x000b682c, 0x000b6ac4); um `LDRB/BX LR` (0x000b1acc); nove sequências de operação seguida de salto (0x00072910, 0x00082404, 0x0008240c, 0x000a94bc, 0x000b4700, 0x000b6c68, 0x000b6cd0, 0x000b6ee0, 0x000b6ee8); um `LDR` seguido de salto externo (0x000b6f80); e um salto para o próprio endereço (0x002a1268). Não executar o salto infinito como função-folha.

A cobertura **local** do lote tornou-se 229/250 entradas com microexecuções (216 anteriores + 13 novas), sem novos certificados. Próximo loop: ampliar contratos byte (`STRB/LDRB`) e leitura controlada de deslocamentos maiores, depois tratar prefixos até **antes** dos destinos de salto, com modelos independentes.

Os certificados semânticos (303) não são alterados. Persistem limitações de estados sintéticos, aliasing real, efeitos externos e reconstrução de funções complexas.
