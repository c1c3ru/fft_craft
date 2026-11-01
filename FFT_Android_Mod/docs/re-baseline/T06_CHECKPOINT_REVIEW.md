# T06 — Resolver os 50 checkpoints em revisão

Depende de T04–T05 (`ready_for_review`, parciais). Executado em 2026-10-31.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** Nenhum dos 50 é promovido a `done`/certificado nesta tarefa. O que foi produzido: uma triagem completa e fundamentada dos 50 em três categorias com causa raiz identificada, e um achado de maior severidade — **3 funções Thumb estão marcadas `auto_structural` (aprovadas) mas o checkpoint foi gerado decodificando os bytes no modo errado (ARM32 em vez de Thumb), produzindo 0% de cobertura real disfarçada por um "100%" relatado sobre uma análise vazia/sem sentido.**

## 1. Triagem dos 50 `needs_review` — três categorias com causa raiz

| Categoria | Quantidade | Causa |
|---|---:|---|
| **A — já `read_full` no histórico** | 26 | Leitura manual (notas) já supera o que o checkpoint automático flagged; checkpoint nunca foi reexecutado. Ver `T05_LEDGER_RECONCILIATION.md` §3 — inclui os 8 "primeiros alvos" citados nesta própria tarefa. |
| **B — bug de modo ARM/Thumb na ferramenta** | 5 | `jtable.py` (usado para gerar todos os 3.002 checkpoints) **não suporta modo Thumb** — hardcoded `CS_MODE_ARM`. Essas 5 funções têm endereço ímpar (convenção ARM de interworking = código Thumb), são decodificadas como ARM32 e produzem instruções sem sentido ou nada decodificável, gerando cobertura artificialmente baixa (0%–67%). Ver seção 2. |
| **C — cobertura genuinamente parcial, sem bug de modo (endereço par, ARM32 correto)** | 19 | Funções de runtime (libgcc/libunwind soft-float e EHABI) e algumas do motor (`CEGL2_IF::SetBlendMode`, `GetNearestUnit`, etc.) com cobertura real entre 56% e 97% — requerem revisão função a função, não feita por completo nesta tarefa. Ver seção 3. |

## 2. Achado de maior severidade: 3 funções Thumb aprovadas com análise vazia

`jtable.py` e `struct_pass.py` (as duas ferramentas de passe estrutural usadas por `parallel_loop.py` para gerar todos os checkpoints) importam só `CS_MODE_ARM`:

```
docs/re-tools/jtable.py:18:    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
docs/re-tools/jtable.py:172:   md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
docs/re-tools/struct_pass.py:11: from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
docs/re-tools/struct_pass.py:59:   md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
```

Outras ferramentas do mesmo projeto (`semantic_evidence.py`, `semantic_a04_alloc_provenance.py`, `semantic_a04_prefix_provider.py`) já tratam isso corretamente com o padrão `mode = CS_MODE_THUMB if destination & 1 else CS_MODE_ARM` — ou seja, o conserto tem precedente direto no próprio código-base, só não foi aplicado às duas ferramentas de triagem estrutural.

Existem exatamente **8 endereços ímpares em todo o CSV de 6.329 entradas** (universo pequeno e totalmente auditável). Resultado da auditoria dos 8:

| Endereço | Nome | `checkpoint_status` atual | Cobertura relatada (ARM32, errado) | O que o modo Thumb (correto) mostra |
|---|---|---|---:|---|
| `0x2c9115` | `operator delete(void*)` | **`auto_structural`** ⚠️ | não aplicável (ARM32 decodifica 1 instrução sem sentido) | `push {r3,lr}; cmp r0,#0; beq ...; bl 0x2ce07c; pop {r3,pc}` — função real e coerente |
| `0x2c9a25` | `operator new[](unsigned int)` | **`auto_structural`** ⚠️ | não aplicável (ARM32 não decodifica nada) | `push {r3,lr}; bl 0x2c99b4; pop {r3,pc}` — trampolim real para `operator new` |
| `0x2ca125` | `__cxa_type_match` | **`auto_structural`** ⚠️ | não aplicável (ARM32 não decodifica nada) | `push {r4-r7,lr}; ...` — prólogo real, função substancial (112 B) |
| `0x2c9121` | `operator delete[](void*)` | `needs_review` | 0% | `push {r3,lr}; bl 0x2c9114; pop {r3,pc}` — trampolim para `operator delete` |
| `0x2c99b5` | `operator new(unsigned int)` | `needs_review` | 5% | `push {r4,lr}; adds r4,r0,#0; b ...; bl ...; bl 0x2ca214 (__cxa_call_unexpected)` |
| `0x2c9b11` | `__gxx_personality_v0` | `needs_review` | 7% | `push {r4-fp,lr}; mov r7,sl; ...` — prólogo real, função grande (388 B) |
| `0x2ca195` | `__cxa_begin_cleanup` | `needs_review` | 67% (parcial, por coincidência de bytes) | `push {r4,lr}; adds r4,r0,#0; subs r4,#0x38; bl 0x2c8da0; ...` |
| `0x2ca215` | `__cxa_call_unexpected` | `needs_review` | 0% | `push {r4-r7,lr}; mov r7,fp; ...` — prólogo real, função grande (268 B) |

**As 3 marcadas `auto_structural` são o problema mais grave**: o checkpoint relata `coverage: 100%` e `distinct_bl: 0` para um corpo que, no modo que a ferramenta realmente usou, não decodifica **nenhuma instrução real** (`operator delete`/`operator new[]`) ou decodifica só 1 instrução sem sentido. Isso significa que o critério de aprovação automática de `jtable.py` não detecta "não consegui decodificar nada" como falha — ele conta uma faixa vazia como 100% coberta. Essas 3 passaram pela triagem estrutural **sem nunca terem sido realmente analisadas**.

**Não corrigido nesta tarefa**: alterar `jtable.py`/`struct_pass.py` para suportar Thumb é uma mudança na ferramenta que todo o pipeline de checkpoints confia, e precisa de decisão do mantenedor sobre como tratar os 3.002 checkpoints já gerados com a ferramenta antiga (regenerar todos? só os 8 endereços ímpares? auditar se há mais algum caso de corpo vazio escondido atrás de 100%?). Registrado como bloqueio prioritário para T07, que já cita 3 desses mesmos endereços nominalmente.

## 3. Categoria C — exemplo trabalhado (`_Unwind_VRS_Pop`, 97,2%) e lista dos 18 restantes

Verifiquei manualmente `_Unwind_VRS_Pop` (`0x2cd594`, 856 bytes, checkpoint 97,2%) como exemplo: desmontei o intervalo completo em ARM32 (modo correto aqui, endereço par) — **as 214 instruções de 4 bytes decodificam todas como código válido**, terminam num epílogo canônico (`add sp, sp, #0x10c; pop {r4,r5,r6,r7,r8,sb,pc}`), a tabela de salto de 5 casos já está resolvida pela ferramenta, e os 10 alvos de `bl` são todos primitivas `__gnu_Unwind_{Save,Restore}_{VFP,VFP_D,WMMXD,WMMXC}` padrão da ARM EHABI — nomes e papéis conhecidos, não inventados aqui. A lacuna de 2,8% (6 de 214 slots) não corresponde a bytes inválidos nem a um alvo não resolvido; é mais provável que seja um detalhe de contabilização do caminhamento recursivo da ferramenta (ex.: um dos 5 alvos do switch sendo contado fora da cobertura "principal"). **Não promovido a certificado** porque não confirmei a causa exata da diferença rodando a ferramenta passo a passo — mas a evidência aqui já é suficiente para quem for revisar não precisar reanalisar do zero.

As outras 18 entradas da categoria C (lista completa com `coverage_pct` e contagem de `bl`/tabelas resolvidas em `docs/re-baseline/t06_checkpoint_triage.json`) **não foram individualmente resolvidas nesta tarefa** — ficam como `needs_review`, com a causa já classificada como "cobertura parcial real, sem bug de modo", para quem continuar T06:

```
000a7ec4 CEGL2_IF::SetBlendMode(int)                               88,3%
000ab4b0 CEGL2_FBO::ErrorGL(char const*, char const*, unsigned)    89,5%
000aecb8 CEGL2_SPRITE::ErrorGL(char const*, char const*, unsigned) 86,7%
000d7e00 load_replaceitems(int, int)                                56,7%
00271ba4 SetBaseTargetGroup(int, int)                                89,8%
0027207c GetNearestUnit(int)                                         92,4%
0028c288 CFFT_STATE::GetBackdropColor(float*, float*, float*)        57,1%
002ca8a0 __subdf3 (alias __aeabi_dsub)                                28,5%
002ca8a4 __adddf3 (alias __aeabi_dadd)                                28,1%
002cabdc __aeabi_ul2d                                                 75,9%
002cac50 __muldf3 (alias __aeabi_dmul)                                72,9%
002cb0c0 __gedf2                                                      92,1%
002cb484 __aeabi_ui2f                                                 80,0%
002cb4ac __aeabi_ul2f                                                 82,9%
002cb830 __gesf2                                                      89,7%
002ccf98 _Unwind_DeleteException                                      62,5%
002ccfb8 _Unwind_VRS_Get                                              73,9%
002cd03c _Unwind_VRS_Set                                              73,9%
```

Note: os nomes exibidos no checkpoint (`__subdf3`, `__adddf3`, `__gedf2`, `__aeabi_ul2d`) diferem levemente dos nomes citados no CSV/ledger (`__aeabi_dsub`, `__aeabi_dadd`, `__gtdf2`, `__floatundidf`) para os mesmos endereços — são aliases de símbolo padrão do `libgcc`/ARM EABI (soft-float), não um erro de endereço; não investiguei qual alias é o declarado em `.dynsym` vs qual é inferido, fica para quem resolver essas entradas.

## 4. O que fica pendente (bloqueia `done`)

1. Decisão do mantenedor sobre `jtable.py`/`struct_pass.py` sem suporte a Thumb (seção 2) — inclui decidir se os 3.002 checkpoints existentes precisam de auditoria adicional por outros falsos-positivos do mesmo tipo (esta tarefa só verificou os 8 endereços ímpares, que é o único sinal direto e barato de detectar; um corpo ARM32 "vazio" por outro motivo não foi procurado no restante dos 2.952 `auto_structural`).
2. Reexecutar o checkpoint estrutural nos 26 da categoria A para confirmar que a leitura manual realmente resolve o que `jtable.py` aponta.
3. Resolver individualmente as 18 entradas restantes da categoria C (lista acima) com o pacote de evidência completo exigido pela seção 3 de `RE_COMPLETUDE_TASKS.md`.
4. Nenhuma das 50 ganhou status `done` nesta tarefa.

## 5. Arquivos produzidos por esta tarefa

- `docs/re-baseline/t06_checkpoint_triage.json` — os 50 endereços, categoria (A/B/C), status atual, cobertura e evidência resumida.
- Este relatório.
