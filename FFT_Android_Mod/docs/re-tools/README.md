# Ferramentas do loop de engenharia reversa

Scripts usados pelo processo descrito em `REVERSE_ENGINEERING_NOTES.md`,
seção "Metodologia do loop". Dependências: `capstone`, `pyelftools`
(`pip install capstone pyelftools`), e `readelf`/`c++filt` do binutils
no PATH. Alvo: `src/lib/armeabi/libgl2jni.so`.

- **`jtable.py <so> <start_hex> <end_hex_ou_+len>`** — descida
  recursiva de uma função, resolve tabelas de salto ARM
  (`add{cond} pc, pc, rX, lsl #2`) achando o `cmp` de guarda real
  andando pra trás no fluxo de instruções (recusa honestamente se o
  registrador foi sobrescrito antes), usa as entradas resolvidas como
  semente e repete até não achar mais código novo. Imprime cobertura,
  tabelas resolvidas e o catálogo de `bl` (resolvido contra `.dynsym`
  + demangle). Ferramenta principal pro passe estrutural de uma
  função nova — validada contra `battle()`.

- **`struct_pass.py <so> <start_hex> <end_hex_ou_+len>`** — mesma
  descida recursiva sem resolução de tabela de salto; serve pra uma
  primeira olhada rápida (branches, `bl`, pontos de convergência) antes
  de decidir se vale a pena rodar `jtable.py` completo.

- **`family_sim.py <so> <ref_start> <ref_end_ou_+len> <nome:start:end_ou_+len>...`**
  — compara o catálogo de endereços `bl` de uma ou mais funções
  candidatas contra uma função de referência já confirmada
  (`read_structural`/`read_full`), via similaridade de Jaccard.
  ≥90% de Jaccard e zero tabela de salto não resolvida =
  `CONFIRMED-BY-SIMILARITY` — a função pode ser marcada sem passe
  estrutural individual. Usado pra fechar a família `Mdl*` em lote
  (ver NOTES §101).

`struct_pass2.py` (tentativa de descida em cascata totalmente
automática) foi testado e abandonado — gerou falsos positivos de
tabela de salto. Não está aqui; não vale retomar sem entender a causa
raiz dos falsos positivos.


## Orquestração paralela (nova)

```bash
cd FFT_Android_Mod
python3 -m pip install capstone pyelftools
python3 docs/re-tools/parallel_loop.py --workers 5 --limit 50
```

- A fila é ordenada por **bytes decrescentes** a partir de `RE_FUNCTION_INVENTORY.csv`. Funções já confirmadas no inventário são ignoradas por padrão.
- Cinco subprocessos podem analisar funções distintas em paralelo. Somente o coordenador grava os arquivos `docs/re-results/<address>.json` (escrita atômica) e `SUMMARY.md`. O binário é apenas lido, não modificado.
- Resultados são retomáveis: itens já analisados para o mesmo SHA-256 do binário e tamanho são ignorados. `--include-reviewed` habilita reanálise de funções já confirmadas.
- Para famílias identificadas, usa `family_sim.py` antes do passe completo. A similaridade exige Jaccard >= 90%, pelo menos 5 destinos `bl`, cobertura >= 95% nos dois membros e nenhuma tabela não resolvida.
- Na ausência de confirmação por similaridade, executa `jtable.py`. Sem tabelas de salto, com cobertura >=95% e nenhuma advertência de tabela não resolvida, sinaliza `auto_structural`; demais casos ficam `needs_review`.
- Status automáticos **não alteram o CSV nem equivalem a revisão semântica**. A aceitação é uma triagem estrutural; verifique chamadas indiretas, saltos computados não reconhecidos e lacunas relevantes antes de considerar uma função inteiramente compreendida.
- O script depende das ferramentas existentes e dos binutils `readelf` e `c++filt`. Há opção `--timeout` por função e erros ficam registrados individualmente no JSON. Para refazer uma análise, apague o JSON do respectivo endereço.
- Não rode dois coordenadores com a mesma pasta de resultados. Use pastas diferentes via `--output` para execuções independentes e consolide após a conclusão.

## Validação contínua

O workflow `.github/workflows/re-pipeline.yml` executa os testes de regressão nos pull requests que alteram as ferramentas de engenharia reversa. Para executar a análise real sob demanda, abra **Actions → Reverse engineering pipeline → Run workflow**, selecione a branch `feat/parallel-re-loop` e defina `limit`. O resultado da execução é enviado como artefato `reverse-engineering-report` (sem commit automático).

Os arquivos JSON em `docs/re-results` são intermediários descartáveis; acompanhe-os usando o SHA-256 do binário. O campo `pipeline_version` invalida checkpoints antigos após mudanças relevantes no processo. Resultados `error` são repetidos automaticamente; `--retry-review` repete também os `needs_review`.

**Importante:** o teste unitário não prova que a resolução ARM está correta para todas as funções. Rodar um lote pequeno e comparar amostras com as notas históricas permanece necessário antes de aprovar uma mesclagem.
