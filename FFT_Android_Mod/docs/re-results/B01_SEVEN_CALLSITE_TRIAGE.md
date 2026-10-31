# B01 — candidatos a chamadas diretas dos sete métodos C++

**Estado:** triagem de fontes A32 por leitura do ELF original; **sem prova
de execução**, sem alteração de certificado, `B01` permanece
`in_progress`.

## Objetivo

Os sete métodos de 12 bytes já possuem validações diferenciais ARM original
× C++ sob estados sintéticos, mas o contrato de chamada real do jogo
(`R0=this`, origem dos objetos, pré-condições e layout) não está demonstrado.

O script `b01_seven_caller_triage.py` varre somente segmentos PT_LOAD
executáveis do ELF de referência, procurando opcodes A32 B/BL/BLX de
destino imediato para os **sete endereços únicos**. Para cada candidata,
consulta a função proprietária declarada no inventário e os checkpoints
estruturais v3 existentes. A varredura pode encontrar palavras de dados
que Capstone interpreta como instruções, ou ignorar chamadas indiretas/
Thumb. Nenhum desses resultados prova reachability, BL executada, ABI
dos chamadores ou mesmo que todo alvo tenha um caller direto.

O relatório JSON registra:
- Fonte, opcode, alvo, tipo de candidata e proprietários possíveis;
- Categoria do checkpoint estrutural e razão de priorização;
- Quantidade de candidatas por alvo e por categoria;
- Gates explícitos a zero: `verified_original_callers`,
  `verified_this_pointer_sources`, `verified_object_layouts`,
  `semantic_certificates_added`, `B01_done=false`.

O workflow `re-b01-named-cpp-prologues.yml` executa agora oito testes
sintéticos de regressão e a triagem do ELF real, anexando o relatório de
candidatas à mesma evidência revisável dos métodos C++.

## Reproduzir

```bash
python3 FFT_Android_Mod/docs/re-tools/b01_seven_caller_triage.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --results FFT_Android_Mod/docs/re-results \
  --output /tmp/b01-seven-caller-candidates.json
```

## Próximo gate de equivalência

1. Selecionar uma candidata priorizada, validar se a fonte é realmente
   uma instrução atingível num CFG com origem conhecida e bytes
   correspondentes ao ELF.
2. Executar seu fluxo de entrada, preparar registros e memory map
   controlados e observar os valores reais em R0 e LR até a entrada
   do método C++.
3. Correlacionar criação e tamanho de objeto, preservar limites de
   memória e confrontar estados de retorno com a reimplementação
   nominal independente.
4. Cobrir todas as condições relevantes, caminhos alternativos e
   múltiplos chamadores antes de propor revisão independente e
   novo proof class no gate de certificação semântica.

**Restrições:** não classificar ausência de uma chamada direta como
inexistência de uso indireto; não executar um destino sem mapear sua
memória e contratos; não promover `certified` automaticamente.
