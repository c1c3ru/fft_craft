# T12 — Implementar classes de prova para funções não triviais

Depende de T08–T10 (`ready_for_review`/`done`, parciais). Executado em 2026-10-31.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** Até esta tarefa, `semantic_certificate_gate.py` só sabia validar **uma única classe de prova**: a instrução isolada `BX LR` (`SCOPE = original_a32_bxlr_normal_return_v1`, ver T11). Esta tarefa adiciona a **segunda classe**, para funções "getter/setter" no sentido do próprio T12 — bloco reto, sem branch, sem chamada, só leitura/escrita de campos em offset fixo (o padrão de `copy_entry_coord`, já lido em T08). Nenhum certificado novo foi criado; o gate foi estendido e testado, nada foi promovido a `certified` de verdade.

## 1. Nova classe de prova: `pure_leaf_copy_v1`

`docs/re-tools/semantic_leaf_copy_contract.py` define o requisito estrutural, verificável a partir dos bytes reais (não de uma afirmação no registro): `is_pure_leaf_copy(code, address, is_thumb)` desmonta o intervalo completo e rejeita se houver qualquer `bl`/`blx`, qualquer branch condicional ou incondicional além do retorno final, qualquer salto computado (`add`/`ldr`/`mov` escrevendo `pc` fora de `bx`/`pop{pc}`), ou qualquer byte que não decodifique — confirmado contra três funções reais: `copy_entry_coord` (aceita), `CdControl` (rejeitada — tem tabela de salto e `bl`), `JNIEnv::NewObject` (rejeitada — tem `bl`).

`semantic_certificate_gate.py` ganha `verify_leaf_copy(record, row, binary, digest, reader=None, differ=None)`, adicionada **sem alterar uma linha** de `verify_one` (a validação da BX LR já certificada) — risco zero de regressão nos 303 certificados existentes, confirmado pela suíte completa (seção 3).

## 2. Como `verify_leaf_copy` satisfaz o critério de aceite exato de T12

| Exigência do critério de aceite | Como é rejeitada |
|---|---|
| "gate rejeita prova BX LR aplicada a outra função" | `record["proof_class"]`/`scope` precisam ser exatamente `pure_leaf_copy_v1`; um registro com o valor da classe BX LR (`gate.SCOPE`) é rejeitado na primeira checagem. Mesmo que alguém escrevesse um valor de classe inventado, a rechecagem estrutural (seção 1) sobre os bytes reais rejeitaria qualquer coisa que não seja de fato um bloco reto sem chamada |
| "certificado incompleto" | Os 5 campos obrigatórios (`preconditions`, `postconditions`, `memory_effects`, `control_flow`, `test_evidence`) precisam existir como listas não vazias de strings — faltando qualquer um, rejeita. Testado removendo cada um individualmente (5 casos) |
| "callee desconhecido relevante" | A rechecagem estrutural roda sobre os bytes **lidos agora** do ELF (via `reader`, não um valor armazenado) — um registro que afirme "sem chamadas" mas cujo corpo real contenha um `bl` é rejeitado por `is_pure_leaf_copy`, testado com um corpo sintético contendo `bl` |
| "evidência de outro ELF" | `record["binary_sha256"] != digest` rejeita antes de qualquer outra checagem, testado com um hash sintético diferente |
| "nenhum contador sobe apenas por satisfazer o schema" | A reexecução diferencial (`differ`) é **sempre** chamada ao vivo; se `report["match"]` não for `True`, rejeita — testado forçando `match=False`. Sem um `differ` explícito, o gate **levanta `NotImplementedError`** em vez de usar um padrão permissivo silencioso (não existe nenhum "default" que aceite qualquer função) |

## 3. Testes (8 novos, nenhuma regressão)

`docs/re-tools/test_semantic_leaf_copy_gate.py`: caso positivo (registro bem formado passa) + 7 casos negativos, um por linha da tabela acima mais revisor ausente/bot. Suíte completa de `docs/re-tools`: **548 testes / 1.819 subtestes, todos passando** (540 antes + 8 novos); a suíte da classe BX LR (`test_semantic_certificate_gate.py`) roda sem alteração.

## 4. O que fica deliberadamente incompleto (bloqueia `done`)

1. **Nenhum certificado `pure_leaf_copy_v1` real foi criado.** Isso exigiria o fluxo de duas fases da política (T11): solicitação verificável, PR de revisão independente, aprovação humana real, depois promoção — nada disso foi simulado aqui. `copy_entry_coord` é o candidato natural (já tem harness pronto de T10), mas certificá-lo de verdade é trabalho de quem for abrir esses PRs, não desta tarefa.
2. **`_default_leaf_copy_differ` não está implementado** — de propósito: um "differ" genérico que funcionasse pra qualquer função exigiria adivinhar buffers/entradas, o que violaria "nenhuma estrutura inventada". Cada função precisa de um `differ` próprio (como fiz manualmente em T10 pra `copy_entry_coord`); integrar isso por função é continuação natural de T13.
3. **Só uma classe nova foi adicionada** (`pure_leaf_copy_v1`). O texto da tarefa cita aritmética, buffers, switches, loops e funções com chamadas/efeitos externos como categorias adicionais — nenhuma delas tem validador próprio ainda.
4. **Limites, overflow, signedness e float** (citados no texto da tarefa) não são verificados por `is_pure_leaf_copy` — a classe atual é deliberadamente restrita a cópia/merge de bits sem aritmética, justamente para manter o escopo pequeno e verificável; uma classe de aritmética precisaria de suas próprias checagens de limite/overflow/signedness, não feitas aqui.

## 5. Arquivos produzidos por esta tarefa

- `docs/re-tools/semantic_leaf_copy_contract.py` — contrato estrutural da nova classe.
- `docs/re-tools/semantic_certificate_gate.py` — `verify_leaf_copy` adicionada (sem alterar `verify_one`).
- `docs/re-tools/test_semantic_leaf_copy_gate.py` — 8 testes.
- Este relatório.
