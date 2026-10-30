# B01 — nove grupos ARM por fluxo recursivo e diferencial C11 de três opcodes

**Estado formal:** `B01=in_progress`. Estas verificações não substituem contratos completos de função, JNI real nem inventário materializado do OBB.

## Evidência 1: caminhos recursivos delimitados dos grupos co-terminais

O analisador `b01_recursive_group_paths.py` percorre os **21 entrypoints** de **nove grupos** (15 pares sobrepostos), em ELF32 ARM de SHA-256 fixo. Cada caminho começa em entrada declarada, desmonta instruções A32 individuais de segmento file-backed executável e segue somente arestas diretas dentro do grupo, com limite de 1.024 slots e 4.096 arestas por entrada. Para desvios condicionais, registra os dois caminhos candidatos. Chamada externa fica explicitamente pendente, ainda que o analisador explore a continuação sob a hipótese de retorno.

- `BX LR` e `MOV PC,LR`: candidato a retorno, **não** prova do contrato global.
- `BX reg`, `BLX reg`, `POP {...,PC}`, `ADD/MOV/LDR PC`: fronteiras não resolvidas por padrão.
- `LDR PC,[PC,#imm]` somente para encoding AL incondicional sem writeback: examina slot literal no ELF; anota bytes/offset e existência de relocação. Um ponteiro bruto sem relocação é **alvo candidato**, não destino de execução comprovado, pois base de carga, contexto e registradores podem variar.
- Destinos fora da janela, bytes não decodificados, opções de Thumb e efeitos desconhecidos são mantidos como pendências. Não usa inferência de que todo `PF_X` seja código válido.

O relatório por entrypoint inclui opcodes, arestas visitadas, fronteiras desconhecidas, retornos candidatos e hashes de referência, preservando `all_groups_cfg_proven=false` e `all_indirect_edges_resolved=false`.

## Evidência 2: modelo C11 de terceiro opcode e possível retorno

O `c-models/b01_three_op.c` estende o modelo independente `b01_two_op.c`: aceita prefixo `ALU -> LDR/STR/LDRB/STRB` (a mesma whitelist prévia) seguido **apenas** de outra instrução ALU sem flags/controle ou da sequência exata `BX LR`. O modelo valida integralmente o encoding antes de executar, recusa PC/SP e mudanças não modeladas, e registra PC esperado (endereço seguinte ou LR).

O `b01_three_op_c_differential.py` compara os **bytes originais do ELF** com C11 compilado para estado sintético controlado, R0–R12, PC, SP/LR, CPSR, trace das três instruções, acessos de memória e buffer inteiro com canário. Se houver `BX LR`, valida o salto efetivo ao sentinel LR. Executa 12 cenários por prefixo elegível; seleciona até 40, priorizando sobreposições, sem conferir certificado de função integral. Um prefixo não comprova ser a rota usada pelo jogo; funções completas permanecem sem equivalência aprovada.

## Reproduzir sem custo de emulador Android

```bash
python3 -m pip install capstone==5.0.6 pyelftools==0.32 unicorn==2.1.3
python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools -p test_b01_recursive_three_op.py -v
python3 FFT_Android_Mod/docs/re-tools/b01_recursive_group_paths.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --output /tmp/b01-recursive-group-paths.json
python3 FFT_Android_Mod/docs/re-tools/b01_three_op_c_differential.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --output /tmp/b01-three-op-c-differential.json
```

Workflow `.github/workflows/re-b01-recursive-three-op.yml`: host Ubuntu; não baixa OBB Git LFS nem executa emulador Android. Apenas JSONs de evidência são publicados.

## Próximo gate depois do ciclo

1. Para cada caminho recursivo, identificar as fontes dos 21 entrypoints, distinguir entradas internas reais e dados, validar arestas indiretas por valores de registradores/relocações e testes diferenciais.
2. Para `BX LR` original em função pequena, expandir o contrato de entrada e memória do **corpo inteiro** antes de emitir certificação; prefixos e entradas artificiais não bastam.
3. Rastrear `StorageUtil → JNI → R1` em runtime autorizado na A04 #464 e OBB privado real via #482; **não marcar B01 done** antes desses gates.

**Proibição de promoção:** qualquer resultado `runtime_reachable=false`, `all_edges_proven=false` ou de três opcodes limitados não pode alterar o contador de certificados semânticos.
