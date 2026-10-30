# B01 — fontes A32 por seção ELF e diferencial original × C11 com dois opcodes

**Estado:** B01 `in_progress`. Critério: prova de bytes e efeitos **somente para prefixos explicitamente admitidos**, não reconstrução integral de funções nem alcance do chamador.

## Problema analisado — issue #489

O gate anterior encontrou 2.126 referências diretas A32 pela varredura linear dos segmentos ELF marcados executáveis: 962 sem função declarada no CSV, 1.164 com proprietário mas sem prova v3 suficiente. **Estar em segmento PF_X não comprova código executável**. Também não há licença para classificar os 962 como dados somente porque não figuram no inventário.

`b01_source_section_partition.py` reconstrói os 2.126 registros do mesmo ELF SHA-256, sem deduplicação enganosa e rejeitando pares source/target duplicados. Anota seção ELF nomeada (incluindo flags executáveis), função declarada anterior/posterior, referência ao checkpoint de origem e categoria conservadora `inventory_gap_unproven`, `owned_unresolved_not_confirmed` ou `structural_candidate_still_not_runtime_proven`. Cada registro preserva `source_instruction_confirmed=false`, `edge_reachable_from_proven_entry=false` e `indirect_edges_resolved=false`. Os resultados **não provam** literal pools, veneers, PLT nem saltos indiretos; apenas localizam os próximos alvos de triagem.

## Primeiro diferencial de dois opcodes com efeitos de memória

`b01_two_op_c_differential.py` lê o ELF original, verifica SHA-256, ELF32 little-endian ARM e instrui Capstone a validar sequências de **duas instruções consecutivas**. O decodificador fail-closed admite somente:

- ALU A32 `MOV/AND/EOR/SUB/ADD/ORR` incondicional, sem alteração de flags, com destino R1–R12 e operando imediato ou registro sem deslocamento;
- seguida de `LDR/STR/LDRB/STRB [R0, #offset]`, imediato positivo, pré-indexado, sem writeback, offset até 0x500, R1–R12 como registrador de dado e alinhamento de palavra.

A biblioteca `c-models/b01_two_op.c` implementa as operações de forma independente em **C11**. Os cenários comparam C e Unicorn sobre os **bytes originais** para R0–R12, PC, SP/LR, CPSR, acessos de memória (endereço/largura/valor), todas as posições do buffer, inclusive canário de integridade. Entradas que não cumpram whitelist não são executadas. O lote é limitado a 32 pares de entrada e 12 casos por par, com seleção determinística, priorizando os 21 entrypoints sobrepostos. Se nenhum par existir, o gate deve falhar, em vez de anunciar evidência vazia.

**Limites:** duas instruções seguidas podem ser um prefixo que não corresponde ao caminho real do jogo. Não são acessados dados do APK original, do OBB, JNI ou funções externas. Não há prova de fluxo, de outros parâmetros, de execução integral ou de equivalência de função. São **microtestes limitados**, com zero certificados novos.

## Execução reproduzível e econômica

```bash
python3 -m pip install capstone==5.0.6 pyelftools==0.32 unicorn==2.1.3
python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools -p test_b01_two_op_c_diff.py -v
python3 FFT_Android_Mod/docs/re-tools/b01_source_section_partition.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --checkpoints FFT_Android_Mod/docs/re-results --output /tmp/b01-source-sections.json
python3 FFT_Android_Mod/docs/re-tools/b01_two_op_c_differential.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --output /tmp/b01-two-op-c-diff.json
```

Workflow: `.github/workflows/re-b01-two-op-c-differential.yml`. Usa host Linux e C11, não executa emulador Android e não transfere OBB. Publica JSONs e recusa alteração não revisada de 2.126 xrefs ou 6.329 entrypoints.

## Gates ainda abertos

1. Verificar as fontes dentro das regiões não cobertas com `jtable.py`/CFG recursivo, checar literais e saltos `BL/BLX` reais; preservar como `unresolved` todo salto indireto não provado.
2. Subir de dois opcodes para blocos com condições de entrada, flags, calls e memória, e ampliar diferencial C/C++ até retorno, sempre com evidência do ELF.
3. Completar vínculo JNI na execução autorizada do jogo (A04 #464) e inventário de OBB materializado sob controle de custo (#482).
4. Apenas depois de cumprir os critérios de B01, reavaliar sua conclusão e liberar formalmente A03/R01/R02.

**Regra de certificação:** nenhum número deste relatório deve incrementar `SEMANTIC_CERTIFIED` sem contrato de função integral auditável.
