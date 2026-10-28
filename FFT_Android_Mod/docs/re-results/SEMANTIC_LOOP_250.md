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

**Status da expansão:** código e CI propostos; a execução dos novos testes diferenciais e suas contagens só são confirmadas quando o job do PR concluir com sucesso. Os 250 relatórios anteriores continuam válidos como evidência **estática**.

A validação do loop **não** equivale a reconstrução integral das 250 funções. Um salto validado para antes do destino não executa o destino. Dados sintéticos não demonstram estados reais da aplicação. Os 303 certificados formais existentes não são alterados e **nenhum novo certificado** é criado.

## Próxima etapa

Expandir contratos auditáveis para leitura/escrita de memória, efeitos de chamada, retornos e trajetórias condicionais, priorizados pelos relatórios da primeira rodada, mantendo checkpoints e revisão independente.
