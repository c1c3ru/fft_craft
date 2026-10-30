# B01 — arestas e chamadores candidatos dos nove grupos ARM co-terminais

**Estado:** B01 `in_progress`, #478 aberta. Nenhuma classificação de CFG ou ligação JNI é promovida a prova sem execução/diferencial.

## Evidência acrescentada neste ciclo

O script `b01_overlap_cfg_callers.py` reutiliza o inventário `b01_overlap_elf_evidence.py`, exige o SHA-256 imutável do ELF ARM, reconstrói as nove janelas `[entrypoint mínimo, end)` e usa Capstone A32 junto com `semantic_cfg.build_cfg` para produzir:

- bytes e o primeiro opcode em cada uma das 21 entradas; testemunhos de `B`, `BL`, `BLX` imediatos; arestas internas e transferências externas;
- caminhos **modelados e limitados** a partir de cada entrada, com contagem de slots alcançáveis no CFG local;
- arestas `unknown` e indicação expressa quando o endereço final da janela não é alcançado **pelo modelo**;
- referências diretas de uma varredura A32 alinhada aos segmentos ELF `PT_LOAD` executáveis; cada referência contém origem, bytes e destino, mas permanece `candidate_only`;
- hash e offset dos intervalos, limitação de tamanho de varredura e de quantidade de testemunhos persistidos.

A varredura linear de segmentos ELF não consegue distinguir todas as ilhas de dados inline de instruções A32 válidas. Portanto, referências obtidas pela varredura são **candidatas** de chamadas/saltos, e não prova de caminho executável. O grafo local supõe retorno de callees nas arestas `call_returns` e não resolve o valor de saltos indiretos, exceções ou transições para Thumb. Nenhum caminho é declarado globalmente alcançável. O relatório mantém `all_groups_cfg_proven=false`, `B01_done=false` e `semantic_certificates_issued=0`.

## Reprodução barata

```bash
python3 -m pip install capstone==5.0.6 pyelftools==0.32
python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools -p test_b01_overlap_cfg_callers.py -v
python3 FFT_Android_Mod/docs/re-tools/b01_overlap_cfg_callers.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --output /tmp/b01-cfg-caller-evidence.json
```

Workflow: `.github/workflows/re-b01-cfg-callers.yml`. O output é um JSON de evidência de análise **estática** com nove grupos, sem executar APK ou emulador, nem baixar o OBB.

## Próximos gates concretos

1. Conferir se as arestas candidatas provêm de regiões de código validadas pelo fluxo recursivo (`jtable.py`), não de dados inline interpretados como A32; documentar origens de `BL` externas.
2. Revisar cada destino `unknown`, `BLX`/saltos indiretos e possíveis entradas Thumb; obter contratos e, quando seguro, testes diferenciados sobre o ELF original, com flags/memória controladas.
3. Verificar chamadas originadas no init JNI e `RegisterNatives` por traces observacionais autorizados no processo original (A04 #464). A correspondência `12/12` de exports permanece apenas estática.
4. Materializar e validar o OBB via processo opt-in da #482, após conferência de custos de Git LFS. Sem materialização, não afirmar inventário de recursos completo.

**Regra:** fechar #478 somente com as disposições e CFG verificáveis, não com base nas contagens do teste. B01 não habilita A03/R01/R02 até completar todo o seu gate de saída.
