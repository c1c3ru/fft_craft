# B01 — filtro de origem A32 e diferenciais de prefixo sem efeitos

**Estado:** B01 `in_progress`; este ciclo não prova execução do jogo, semântica de função inteira ou JNI em runtime.

## Motivo do novo gate

A varredura dos segmentos executáveis havia identificado **2.126 referências diretas A32 candidatas** a 21 entradas, em nove grupos de intervalos sobrepostos. Uma instrução válida na varredura linear pode ser dado embutido. O filtro `b01_source_evidence_filter.py` exige a correspondência do SHA-256 do ELF, inventário com intervalos consistentes e, para cada possível origem, verifica se existe checkpoint estrutural v3 da *mesma versão* e endereço/tamanho.

O resultado separa `structurally_anchored_candidate`, `explicitly_unresolved_source` e `unresolved_source`. Mesmo o primeiro é apenas evidência estrutural, e não uma chamada comprovadamente executada. Checkpoints ausentes, antigos, com SHA divergente e posições `unexplained_slots` permanecem sem promoção. As 2.126 referências devem ser contabilizadas sem perda; qualquer mudança exige revisão explícita.

## Teste diferencial restrito

O segundo script `b01_safe_alu_differential.py` verifica exclusivamente a **primeira instrução** dos 21 entrypoints candidatos do ELF original, aceita somente operações A32 de dados `MOV/ADD/SUB/AND/EOR/ORR`, `cond=AL`, sem `S` e com registradores R0–R12. Rejeita efeitos em memória, SP, PC, instruções de salto, shifts, modos não suportados e chamadas.

Para cada prefixo elegível, realiza 10 cenários controlados com Unicorn e compara estado final R0–R12, SP/LR, PC, CPSR e ausência de acessos à memória com modelo aritmético independente em Python. Divergência falha o CI. Se nenhum prefixo cumprir a whitelist, registra zero testes reais sem inventar cobertura.

Os testes são **microexecuções de um único opcode**: não atravessam o fluxo de uma função, não representam valores concretos do aplicativo e não criam certificados semânticos.

## Reprodução

```bash
python3 -m pip install capstone==5.0.6 pyelftools==0.32 unicorn==2.1.3
python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools -p test_b01_source_differential.py -v
python3 FFT_Android_Mod/docs/re-tools/b01_source_evidence_filter.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --results FFT_Android_Mod/docs/re-results \
  --output /tmp/b01-source-evidence.json
python3 FFT_Android_Mod/docs/re-tools/b01_safe_alu_differential.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --output /tmp/b01-alu-differential.json
```

Workflow barato: `.github/workflows/re-b01-source-differential.yml`. Publica os relatórios sem emulador Android, sem OBB LFS e sem binários em artefatos.

## Critérios de avanço

1. Conferir amostras `structurally_anchored_candidate` em CFG recursivo do ELF original, rejeitando literal pools e ponteiros tratados como opcodes.
2. Ampliar os prefixos seguros para contratos com múltiplos passos somente quando os efeitos de memória, CPSR e chamadas estiverem modelados; comparar com C/C++ independente.
3. Verificar alcançabilidade, chamadas indiretas e possíveis entradas Thumb dos nove grupos; manter `needs_review` quando faltarem garantias.
4. Manter a A04 dependente de traces autorizados `StorageUtil → JNI → R1` e a B01 dependente do OBB materializado, cujo fluxo manual está na issue #482.

**Não elevar 2/17 atividades nem o número de certificados apenas por estes testes.**
