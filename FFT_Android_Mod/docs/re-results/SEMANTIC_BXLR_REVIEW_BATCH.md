# Primeira fila de revisão formal: contratos BX LR

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Execução de origem do CI: `40890226832`

- Contratos locais preparados para revisão: **0**
- Microexecuções **novas neste passo**: **0** (reutiliza as 32 observações ARM/Thumb por candidato).
- Certificados integrais emitidos automaticamente: **0**.

**Nenhuma função está certificada por este pacote.** A revisão independente deve avaliar o escopo de execução normal, interworking, preservação dos registradores, efeitos de memória, alinhamento do LR e casos de exceção excluídos.

| Endereço | Função | Opcode original | Testes anteriores | Estado |
|---|---|---|---:|---|

## Como concluir a revisão

1. Conferir os registros individuais em `SEMANTIC_BXLR_REVIEW_BATCH.json` com o ELF original.
2. Verificar as pré/pós-condições e documentar ressalvas; o escopo **não** cobre o programa completo.
3. Submeter proposta explícita de certificados ao ledger em PR separado; jamais copiar aprovação fictícia de uma fixture.
4. Obter revisão independente registrada no GitHub. O gate verifica PR, identidade, commit, endereço e bytes do ELF antes de contar qualquer certificado.

Este arquivo é uma fila de revisão e não uma declaração de equivalência semântica integral.
