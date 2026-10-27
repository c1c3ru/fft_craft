# Recuperação da execução do pipeline semântico — 27/10/2026

**ELF original SHA-256:** `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

Este relatório é de **execução e integridade do pipeline**, não uma nova prova semântica. As **303 certificações formais A32 BX LR** permanecem vinculadas aos reviews humanos e ao gate; elas não são contadas como novos certificados nesta recuperação.

## Falha 1 — manifestos e execução concorrente

A execução manual do workflow `Semantic coverage manifests` criou **25 manifestos e 250 tarefas** (`WORKER_01` a `WORKER_25`, dez tarefas cada). O gerador `semantic_work_queue.py` aceita **até 32 shards**, mas `semantic_pilot.py` antes rejeitava `--workers 25` com `workers must be 1..16`. Assim, a falha aconteceu antes da geração dos relatórios do piloto; **não deve ser apresentada como 250 tarefas verificadas**.

**Correção:** aceitar 1 a 32 shards/argumentos e limitar o `ThreadPoolExecutor` a **min(workers, 16)** threads. Percorrer todos os manifestos e os endereços sem perder ou duplicar tarefas. A regressão usa 25 manifestos/250 entradas sintéticas, testa o limite de 16 threads, 250 arquivos de saída distintos e a rejeição de 0/33 workers. Testes sintéticos do agendamento **não** produzem evidência real de ARM nem certificados.

## Falha 2 — PR de checkpoint concorrente

A execução automática **40560964817** criou o PR [#362](https://github.com/c1c3ru/fft_craft/pull/362) e falhou no `gh pr merge` por conflito. O relatório `SEMANTIC_SOUND_DESTINATION_271314.md` desse PR já está **publicado na main com conteúdo SHA Git idêntico** e consta no `STATUS_GERAL.md`. Os demais arquivos divergiam principalmente nos **identificadores de execução** do snapshot, não em novas certificações.

O PR #362 foi encerrado **sem merge**, para não sobrescrever resultados da `main` por metadados defasados.

**Correção preventiva:** antes de criar PR automatizado, o workflow faz `git fetch origin main` e verifica que o checkout usado na coleta corresponde ao HEAD atual. Se a `main` mudou, **não publica o checkpoint obsoleto** e mantém a evidência do run no artefato `automated-re-batch`. Verifica novamente a `main` antes de mesclar; se houver conflito, falha com diagnóstico e preserva o PR aberto, sem `force` nem estratégia `ours`. Só dispara um novo lote automaticamente depois que o merge realmente ocorreu (`steps.publish.outputs.published == 'true'`).

## Estado confirmado e próximos passos

- Certificados formais: **303**, abrangendo uma classe local restrita de instruções A32 `BX LR`.
- Entradas únicas no inventário: **6.329**; restantes sem certificação formal: **6.026**.
- Revisões e evidências de som: continuam como **parciais** e requerem novos experimentos em chamadas, memória e retorno.
- Validar PR da correção nos dois workflows; depois executar um workflow manual com `limit=250` e `workers=25` e conferir explicitamente `PILOT_PARTIAL=250`, `PILOT_FAILED=0`, `PILOT_MANIFEST_SHARDS=25` e `PILOT_CONCURRENT_THREADS=16`.
- O painel centralizado `STATUS_GERAL.md` referencia esta análise e deve manter links às evidências originais. Nenhuma contagem é aumentada só porque os manifestos foram gerados.

**Limite de garantia:** uma proteção contra publicação concorrente não prova ausência de outros processos alterando a `main` e não autoriza promover evidência parcial a certificação.
