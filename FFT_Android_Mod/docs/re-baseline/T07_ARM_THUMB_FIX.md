# T07 — Corrigir tratamento ARM/Thumb e runtimes

Depende de T04 (`ready_for_review`, parcial) e do achado de T06. Executado em 2026-10-31, com autorização explícita do mantenedor para corrigir as ferramentas (ver T06).

**Estado: `ready_for_review` (parcial) — NÃO `done`.** O bug de modo ARM/Thumb identificado em T06 foi corrigido em `jtable.py` e `struct_pass.py`, com testes de regressão novos, e os 8 checkpoints afetados foram regenerados com a ferramenta corrigida. T07 continua pendente para o restante do seu escopo (interworking em outros pontos do binário, trampolins PLT/GOT, helpers de ponto flutuante fora destes 8, unwind tables).

## 1. O que foi corrigido

`jtable.py` e `struct_pass.py` tinham `Cs(CS_ARCH_ARM, CS_MODE_ARM)` hardcoded. Ambos agora:

1. Detectam o bit de interworking Thumb no endereço de entrada (`is_thumb = bool(raw_start & 1)`), removem o bit antes de tocar no ELF (`start = raw_start & ~1`), e escolhem `CS_MODE_THUMB`/`CS_MODE_ARM` de acordo — seguindo o mesmo padrão já usado em `semantic_evidence.py`, `semantic_a04_alloc_provenance.py` e `semantic_a04_prefix_provider.py`.
2. Corrigem a estimativa de "slots esperados" usada no cálculo de cobertura: `length // 4` presumia 4 bytes por instrução (válido só em ARM); agora usa `length // 2` em modo Thumb (que mistura instruções de 2 e 4 bytes — usar o mínimo de 2 bytes só pode subestimar a cobertura, nunca inflar artificialmente um resultado).
3. O cabeçalho impresso agora mostra o endereço original com o bit de interworking e o modo detectado (`"... (N bytes, Thumb mode) ..."`), para que o log do checkpoint deixe isso explícito.

Nenhuma outra lógica foi alterada. O padrão de detecção de tabela de salto ARM (`add{cond} pc, pc, rX, lsl #2`) continua ARM-específico de propósito — nenhuma das funções Thumb no escopo desta correção usa esse idioma (confirmado por inspeção manual), e resolver tabelas de salto Thumb (`tbb`/`tbh`) fica fora do escopo desta correção pontual.

## 2. Prova de não-regressão

- Dois testes novos por ferramenta (`test_jtable.py`, `test_struct_pass.py`) usando um ELF32/ARM sintético mínimo (`elf_test_fixture.py`, sem depender do binário real de 4,46 MB): confirmam que um endereço par continua decodificando em modo ARM com o mesmo resultado de antes, que um endereço ímpar agora decodifica em modo Thumb, e que os mesmos bytes Thumb decodificados em ARM32 (o comportamento antigo) produzem instruções diferentes/sem sentido — documentando exatamente o bug corrigido.
- Suíte completa de `docs/re-tools`: **534 testes / 1.812 subtestes, todos passando** (528/1812 antes da correção + 6 testes novos).
- Regressão manual em funções ARM já conhecidas: `000724b0` (JNIEnv::NewObject, 56 B) continua `coverage: 14 of ~14 instruction slots (100%)`; `CdControl` (`0028e2e4`, 384 B) continua reportando a tabela de 27 casos / 9 handlers distintos já documentada em `REVERSE_ENGINEERING_NOTES.md` §648 — nenhum checkpoint ARM existente seria alterado por esta correção.

## 3. Checkpoints regenerados (os 8 endereços ímpares do CSV inteiro)

Usando `docs/re-tools/parallel_loop.py` real (não uma reimplementação paralela da lógica), com um inventário temporário contendo só estas 8 linhas, contra `docs/re-results/` de verdade:

| Endereço | Nome | Status antes | Cobertura antes | Status depois | Cobertura depois |
|---|---|---|---:|---|---:|
| `0x2c9115` | `operator delete(void*)` | `auto_structural` ⚠️ (falso-positivo) | 100% (vazio) | `needs_review` | 83,33% |
| `0x2c9a25` | `operator new[](unsigned int)` | `auto_structural` ⚠️ (falso-positivo) | 100% (vazio) | `needs_review` | 30,0% |
| `0x2ca125` | `__cxa_type_match` | `auto_structural` ⚠️ (falso-positivo) | 100% (vazio) | `needs_review` | 91,07% |
| `0x2c9121` | `operator delete[](void*)` | `needs_review` | 0% (garbage) | `needs_review` | 75,0% |
| `0x2c99b5` | `operator new(unsigned int)` | `needs_review` | 5,26% (garbage) | `needs_review` | 76,32% |
| `0x2c9b11` | `__gxx_personality_v0` | `needs_review` | 7,22% (garbage) | `needs_review` | 90,21% |
| `0x2ca195` | `__cxa_begin_cleanup` | `needs_review` | 66,67% (parcial por coincidência) | `needs_review` | 80,0% |
| `0x2ca215` | `__cxa_call_unexpected` | `needs_review` | 0% (garbage) | `needs_review` | 73,88% |

Todos os 8 ficam **`needs_review`** — nenhum atinge `auto_structural` porque nenhum chega a 95% de cobertura real. Isso é o resultado honesto esperado: a correção troca um falso "100%" vazio (3 casos) ou uma cobertura sem sentido (5 casos) por uma cobertura real e parcial, não por uma aprovação automática. `docs/re-results/PROGRESS.md` e `SUMMARY.md` foram regenerados pelas próprias ferramentas (`progress_report.py`, e o próprio `parallel_loop.py`) para refletir isso: `auto_structural` 2.952 → 2.949, `needs_review` 50 → 53 (`core needs_review` 34 → 36).

**Não regenerado:** `docs/re-results/STATUS_GERAL.md` — `status_geral.py` tenta verificar revisão humana remota no GitHub para os certificados semânticos e falha sem acesso de rede nesta sessão (`verify_remote_review`). Isso é o comportamento correto da ferramenta (não simular revisão humana), não um defeito; deixar para quem tiver acesso ao GitHub real regenerar esse painel específico.

## 4. O que ainda falta do escopo de T07 (bloqueia `done`)

1. Resolução semântica real das 8 funções (coverage parcial, não garbage — ainda precisam de leitura manual/estrutural, não só o conserto de modo). `__cxa_type_match` (91%) tem um `blx r3` (chamada indireta por registrador) não resolvido, provavelmente um ponteiro de função de RTTI — candidato natural a próximo passo.
2. Auditoria de interworking em outros pontos do binário não cobertos pelos 8 endereços ímpares do `.dynsym` — endereços de retorno de chamada indireta, ponteiros de função em tabelas de dados, e callbacks que possam alternar para Thumb sem ter um símbolo próprio no `.dynsym` (T04 encontrou 303 intervalos de `.text` fora do inventário; nenhum foi auditado por bit de interworking nesta tarefa).
3. Trampolins PLT/GOT e helpers de ponto flutuante fora dos 8 — não auditados.
4. Nenhuma das 8 funções foi certificada; todas seguem como material de T06 (categoria C agora, não mais B).

## 5. Arquivos produzidos/alterados por esta tarefa

- `docs/re-tools/jtable.py`, `docs/re-tools/struct_pass.py` — suporte a modo Thumb.
- `docs/re-tools/elf_test_fixture.py`, `docs/re-tools/test_jtable.py`, `docs/re-tools/test_struct_pass.py` — novos testes.
- `docs/re-results/002c9115.json`, `002c9121.json`, `002c99b5.json`, `002c9a25.json`, `002c9b11.json`, `002ca125.json`, `002ca195.json`, `002ca215.json` — checkpoints regenerados.
- `docs/re-results/PROGRESS.md`, `docs/re-results/SUMMARY.md` — regenerados pelas próprias ferramentas do projeto.
- Este relatório.
