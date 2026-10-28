# Engenharia de loop — lote real de 250 tarefas (28/10/2026)

**ELF original SHA-256:** `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

O [workflow Real ELF semantic manifest audit (250)](https://github.com/c1c3ru/fft_craft/actions/workflows/re-semantic-real-elf-250.yml) foi ampliado para executar o ciclo de engenharia de loop **classificar → priorizar → microexecutar ARM → comparar com modelo independente → registrar checkpoint → repetir/validar**.

## Insumos e escopo
- O lote já validado contém **250 inspeções estáticas reais**, **25 manifestos**, **170 funções de 4 bytes** e **80 funções de 8 bytes**.
- Sem `BL/BLX` identificado nos relatórios, com **15 funções** possuindo instruções candidatas de escrita em memória (fora do primeiro contrato).
- A seleção permite apenas saltos A32 incondicionais isolados de uma instrução e rotinas-folha de duas instruções (`MOV/ADD/SUB/AND/ORR/EOR/LDR` restritos seguidos por `BX LR`). Rejeita instruções com efeitos não modelados.
- Limites do primeiro ciclo: **até 24 candidatos**, lotes de **8 funções**, **32 estados** (8 entradas × 4 valores NZCV) por candidato.
- A microexecução usa os bytes exatos do ELF em Unicorn, compara o PC, registradores, CPSR e leituras/escritas de memória a um modelo Python explícito, e protege memória com sentinelas.
- Cada rodada gera um checkpoint JSON vinculado ao hash do ELF e ao conjunto exato de 250 resultados. A mesma rodada é repetida e o checkpoint deve permanecer idêntico; inconsistências impedem aprovação.
- A documentação completa produzida pelo job fica em `SEMANTIC_LOOP_250.md` dentro do artefato `real-elf-250-static-audit`, junto a `semantic-loop-checkpoint.json` e aos logs.

## Resultados e garantia

**Resultado verificado:** o [workflow real-ELF #40710246666](https://github.com/c1c3ru/fft_craft/actions/runs/40710246666), commit `533c78b7dad0ad20d13b16b18138a51a75bad5c7`, concluiu o job `real-elf-250` com **success**. Os logs registram `LOOP_ELIGIBLE=216`, `LOOP_SELECTED=24`, `LOOP_ROUNDS=3`, `LOOP_DIFFERENTIAL_PASSED=768`, `LOOP_FAILED=0`, `LOOP_NEW_CERTIFICATES=0`. O checkpoint do segundo ciclo de execução foi idêntico ao original (`cmp` aprovado). Os 24 candidatos executados são funções-folha A32: **12 LDR, 9 ADD e 3 MOV**, cada uma com 32 cenários. **34** dos 250 endereços não satisfizeram os contratos de opcode/efeitos desta rodada, e outros 192 elegíveis não foram executados por causa do limite de 24. As 250 inspeções estáticas continuam válidas e não devem ser confundidas com microexecução integral das 250 funções. Os dados brutos estão no artefato `real-elf-250-static-audit` (ID `12826152000`) do run citado.

A validação do loop **não** equivale a reconstrução integral das 250 funções. Um salto validado para antes do destino não executa o destino. Dados sintéticos não demonstram estados reais da aplicação. Os 303 certificados formais existentes não são alterados e **nenhum novo certificado** é criado.

## Próxima etapa

Expandir contratos auditáveis para leitura/escrita de memória, efeitos de chamada, retornos e trajetórias condicionais, priorizados pelos relatórios da primeira rodada, mantendo checkpoints e revisão independente.
