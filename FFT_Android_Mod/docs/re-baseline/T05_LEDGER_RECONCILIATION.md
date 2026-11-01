# T05 — Reconciliar histórico, checkpoints e cobertura

Depende de T04 (`ready_for_review`, parcial). Executado em 2026-10-31.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** Produzido um ledger canônico (`canonical_ledger.json`) com uma identidade por endereço, preservando a proveniência de cada status histórico e cruzando contra os checkpoints estruturais. A base é limpa (zero hash obsoleto, zero conflito de tamanho), mas um achado real de sobreposição não documentada foi encontrado (seção 3) e afeta diretamente o planejamento de T06.

## 1. Consistência da base — tudo confirmado, nenhum problema de integridade grave

| Verificação | Resultado |
|---|---:|
| Linhas totais no CSV | 6.455 |
| Endereços únicos no CSV | 6.329 |
| Linhas duplicadas por endereço (mesmo endereço, mais de uma linha) | 124 |
| Conflito de **tamanho** entre linhas duplicadas do mesmo endereço | **0** |
| Arquivos de checkpoint JSON (`docs/re-results/<addr>.json`) | 3.002 |
| Checkpoints com `binary_sha256` diferente do ELF atual (`bf913415...`) | **0** |
| Checkpoints com `status: "error"` | **0** |
| Endereços de checkpoint que NÃO existem no CSV | **0** |
| Conflito de **tamanho** entre CSV e checkpoint para o mesmo endereço | **0** |

Todos os números da seção 1 de `RE_COMPLETUDE_TASKS.md` (6.455 / 6.329 / 3.002 / 2.952 `auto_structural` / 50 `needs_review`) foram reconfirmados byte a byte nesta tarefa, sem regenerar nada — apenas lendo o CSV e os 3.002 JSONs existentes.

## 2. Métricas por eixo (exigido pelo critério de aceite de T05)

| Eixo | Valor | Observação |
|---|---:|---|
| Símbolos (`.dynsym`, `FUNC`/`OBJECT`) | 9.158 | Universo bruto de símbolos exportados, não filtrado |
| Funções (endereços únicos no CSV) | 6.329 | Não soma com o eixo de símbolos — é um subconjunto/derivado, critério de seleção não documentado nesta tarefa |
| União de bytes cobertos em `.text` pelas 6.329 funções | 1.826.552 de 2.475.500 (73,79%) | Mesmo número de T04; **não soma** com nenhuma contagem histórica de "5.932 registros" — overlaps já foram removidos aqui, ao contrário da nota de cautela da própria auditoria sobre esse número bruto |
| Certificados semânticos `certified` | 0 | `pending_count=0` estrutural **não é** completude semântica — nenhum certificado formal existe (ver `SEMANTIC_CERTIFICATION_POLICY.md`) |

## 3. Achado: 26 endereços promovidos a `read_full` com checkpoint estrutural ainda em `needs_review`

Cruzando o CSV (status histórico, de leitura manual/notas) contra o checkpoint JSON (status automático de `jtable.py`) por endereço, 26 funções têm **`historical_status = read_full`** no CSV mas **`checkpoint_status = needs_review`** no JSON correspondente — ou seja, a leitura manual documentada nas notas nunca disparou uma re-execução do passe estrutural automático que ainda está sinalizado como pendente.

**Isto inclui 8 dos 8 "primeiros alvos" que a própria `RE_COMPLETUDE_TASKS.md` lista em T06** como prioridade para os 50 `needs_review`:

| Função | Endereço | `historical_status` | `checkpoint_status` |
|---|---|---|---|
| `EnvSE_Play` | `0x2b2448` | `read_full` | `needs_review` |
| `unittoface` | `0x15813c` | `read_full` | `needs_review` |
| `getTrapResultDamage` | `0x1ccc3c` | `read_full` | `needs_review` |
| `asm_function` | `0x159aac` | `read_full` | `needs_review` |
| `wasm_function` | `0x162080` | `read_full` | `needs_review` |
| `iOSsetCursorByTouch` | `0x2031a4` | `read_full` | `needs_review` |
| `pspFftSave` | `0x2899a0` | `read_full` | `needs_review` |
| `Savedata_Load` | `0x27fe84` | `read_full` | `needs_review` |

As outras 18 (`Wload_replaceitems`, `siOS_TCurSucCheck`, `MessageDataSet`, `set_ct_weapon`, `get_mapid`, `get_shape2`, `set_casting_status`, `setCursorByTouch`, `initMap`, `getNextSENo`, `_ReadTMD`, `houkoku_talkunit`, `pspMsgGet`, `getMovieEventNum`, `pspFftDelete`, `CdControl`, `onGotoNextMode`, `Boot_Init`) estão listadas no ledger completo.

**Interpretação, sem decidir por quem vai executar T06:** as notas (`REVERSE_ENGINEERING_NOTES.md` §637–657, por exemplo) descrevem revisões byte a byte que corrigem exatamente os pontos de dispatch/tabela que `jtable.py` costuma sinalizar (ex.: "dispatch corrigido pra `{0,13,32}`→`sub_202ff0`, não `{1,13,32}`" para `setCursorByTouch`). Isso sugere que boa parte desses 26 pode já estar efetivamente resolvida, mas **não foi confirmado reexecutando `jtable.py`/o checkpoint** nesta tarefa — isso é o primeiro passo barato que T06 deveria fazer antes de gastar esforço novo nessas 26 (e nas outras 8 já citadas por nome em T06), ao contrário de tratá-las como desconhecidas do zero.

## 4. Heurística de "entradas só em notas" — descartada por ruído, não por ausência de achado

Tentativa de extrair todos os tokens `0x` de 5 a 8 dígitos hex em `REVERSE_ENGINEERING_NOTES.md` e comparar contra o CSV: 3.825 tokens distintos encontrados, 434 sem correspondência normalizada no CSV. **Este número não é confiável e não está no ledger**: a extração por regex não distingue endereço de qualquer outro hexadecimal citado no texto (tamanhos, hashes, valores de registrador, offsets de struct). Produzir essa lista de forma válida exige parsing estruturado das notas (ex.: só considerar hex que aparece em contexto de cabeçalho de função ou após palavras como "endereço"), não feito nesta tarefa. Registrado como pendência de método, não como resultado.

## 5. O que fica pendente (bloqueia `done`)

1. Confirmar (reexecutando `jtable.py`/checkpoint) se os 26 endereços da seção 3 realmente resolvem ao passe estrutural automático após a leitura manual — não presumido aqui.
2. Produzir uma extração confiável de "endereços citados apenas em notas" (seção 4) com parsing estruturado, não regex ingênua.
3. Vtables/tabelas de callback e os 303 intervalos de T04 ainda não têm identidade no ledger canônico (ficam fora de `canonical_ledger.json`, que por ora só cobre os 6.329 endereços já no CSV) — integrá-los é continuação natural de T04+T05, não feita aqui.
4. x86: sem CSV/ledger próprio (confirmado em T04), nada a reconciliar ainda.

## 6. Arquivos produzidos por esta tarefa

- `docs/re-baseline/canonical_ledger.json` — uma entrada por endereço único (6.329), com status histórico, proveniência (`section_ref` das linhas duplicadas), status de checkpoint e flags (`promoted_read_full_despite_open_structural_review`, `no_structural_checkpoint_on_record`, `size_conflict_csv_vs_checkpoint`).
- Este relatório.
