# Auditoria do loop de engenharia reversa — 2026-10-26

## Estado encontrado na main

- `parallel_loop.py` já usa `ThreadPoolExecutor` e `re-batches.yml` invoca **5 workers** por lote, com checkpoints escritos exclusivamente pelo coordenador.
- A fila normal termina quando os checkpoints existem. O painel atual indica **0 novos checkpoints pendentes**; há **89 `needs_review`**.
- `structural_v3.py` já separa slots de instruções, entradas de tabelas ARM e candidatos a literais, com verificação conservadora do despacho.
- `family_sim.py` já é chamado na implementação, mas o atalho está desabilitado no caminho de produção porque `analyze_one(..., enable_v3=True)` ignora o atalho. Não converter similaridade de chamadas BL em certificado semântico.
- O histórico CSV e os checkpoints JSON podem se sobrepor: não somar as duas contagens para estimar progresso.

## Nova etapa: distribuição de revisão por bytes

```bash
python3 FFT_Android_Mod/docs/re-tools/export_review_queue.py
python3 FFT_Android_Mod/docs/re-tools/review_shards.py \
  --workers 5 --limit 25 --output /tmp/fft-review-shards
```

O gerador cria `worker-01.json` até `worker-05.json` com endereços disjuntos, priorizando funções maiores e distribuindo aproximadamente a carga por bytes. É determinístico e **não executa a análise**, não escreve checkpoints nem promove `needs_review`. Cada agente pode usar seu manifesto em branch/worktree isolado e produzir somente relatórios próprios; a consolidação e aprovação ficam centralizadas, após validação.

## Ordem sugerida de trabalho

1. Corrigir lacunas v3 de funções grandes sem tabela conhecida (ex.: `0x28179c`, `0x244200`, `0xdf864`, `0x25a228`).
2. Investigar `0x2b2448` (`EnvSE_Play`) e outras tabelas com `resolved_jump_table_check`; preservar checagem de guard, limites, instruções e todos os destinos.
3. Separar funções Thumb ou de runtime com baixa cobertura ARM, sem interpretá-las automaticamente como código ARM inválido.
4. Usar família Mdl/personalwindow como **triagem** (evidência de similaridade, nunca substituta da verificação byte a byte).
5. Para boilerplate, registrar identidade/padrão reconhecido com evidência rastreável; não converter a ausência de análise em aprovação de semântica.

## Critérios de integração

- Um endereço pertence a um só manifesto do lote.
- Resultado de cada agente guarda endereço, SHA-256 do ELF, entradas examinadas e desconhecidos.
- Artefatos compartilhados e `STATUS_GERAL.md` são atualizados por um único coordenador.
- `check_smoke.py`, testes unitários e regras v3 devem continuar bloqueando regressões.
- Aprovação estrutural e equivalência semântica integral são estados distintos.

## Próxima iteração

Criar workers de revisão que consumam esses manifests, gerem evidências JSON por endereço e publiquem artefatos separados; somente depois automatizar merge de relatórios aprovados. Medir tempo por byte validado e casos realmente fechados, não o número bruto de funções processadas.
