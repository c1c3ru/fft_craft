# A04 — análise dos destinos A32 após os saltos verificados

**Base:** [A02 / 352 testes delimitados](SEMANTIC_A02_BRANCHES.md), issue [#388](https://github.com/c1c3ru/fft_craft/issues/388). ELF original SHA256 `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Objetivo desta rodada

Desmontar, com proveniência verificável, os primeiros blocos candidatos de **sete destinos distintos**, total de dez entradas ARM externas. A análise ocorre diretamente nos bytes do segmento PT_LOAD executável do ELF original. Para cada destino, registrar 96 bytes, sequência A32 até o primeiro salto/chamada/retorno (ou 24 instruções), predecessores e referências de fluxo.

- `0x000b6c58` — quatro entradas com `R2=0..3`: primeira prioridade para reconstruir o dispatcher e seus efeitos.
- `0x000714dc` e `0x000714e8` — entradas de `MOV` e `MUL` vindas de `0x0008240c` e `0x00082404`.
- `0x002b1bb0` — entrada após `MOV R0,R2`.
- `0x000ab674` — entrada após `ADD R0,R0,#0x1c`.
- `0x000b461c` — entrada após `MOV R1,#0`.
- `0x000b8a18` — entrada após `LDR R0,[R0]`.

A entrada `0x002a1268` tem um salto para si mesma, sem terminação ou alcançabilidade dinâmica demonstradas. Não será executada indefinidamente.

## Validação conservadora

O analisador `semantic_a04_destinations.py` verifica SHA do ELF e bytes originais de **todas as 11 fontes A02**, usa Capstone para um scan linear delimitado dos sete destinos, grava checkpoint JSON, repete integralmente e exige reprodução idêntica. Não afirma que um segmento executável contém só código — uma desmontagem linear pode atravessar *inline data*. A auditoria não executa destinos nem promove certificados.

**Resultado de CI:** pendente. Gate esperado: `A04_DISTINCT_TARGETS=7`, `A04_AUDITED_FILE_BYTES=672`, `A04_TARGETS_EXECUTED=0`, `A04_NEW_CERTIFICATES=0` e checkpoint idêntico. A saída real do CI será anexada à documentação após aprovação.

## Próximos ciclos da A04

1. Consultar o relatório real gerado no CI, definir fronteiras de blocos, identificar possíveis dados, instruções condicionais, acessos à memória e destinos adicionais por função.
2. Construir oráculos independentes e microexecuções com estado controlado apenas para blocos de efeito compreendido. Desvios complexos e tabelas precisam de contratos explicitamente isolados.
3. Construir CFG de caminhos relevantes e contratos entre caller e target; só então comparar o comportamento C/C++ e efeitos de estado em fluxos completos.
4. Classificar o auto-loop por contexto/reachability, sem inventar terminação ou chamar salto local de função reconstruída.

A04 permanece **em andamento** após a auditoria estática, pois sua conclusão exige CFG e contratos semânticos de cada destino. Os 303 certificados existentes não sofrem alteração.
