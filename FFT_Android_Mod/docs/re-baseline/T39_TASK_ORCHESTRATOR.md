# T39 — orquestração auditável T01–T40 e filas T04/T05/T06

**Estado:** implementação inicial de automação; T39 permanece pendente do
critério amplo de aceite (CI do APK real, replay e auditoria integral).
Executar essa ferramenta não conclui T04, T05, T06 nem qualquer tarefa.

## Fontes de evidência

- `RE_COMPLETUDE_TASKS.md`: T01 a T40 + registro formal de execução.
  As 28 fatias P2 registradas são entregas **parciais**, não 28 tarefas concluídas.
  O checklist original não é atualizado automaticamente; inconsistências como
  T11 formalmente `done`, ainda desmarcada, são exibidas.
- `text_coverage_gaps.json` (T04): intervalos de seção `.text` descobertos
  **fora do inventário derivado de .dynsym**. Prólogos e destinos de
  inicialização elevam a prioridade, mas não provam limites ou reachability.
- Checkpoints JSON do ELF corrente + `progress_report.summarize` (T06):
  toda a população de `needs_review`, usando hash e tamanho do ELF.
  Os 53 atuais não são reduzidos aos 50 da triagem de 31/10.
- `t06_checkpoint_triage.json`: categorias históricas são apenas dicas;
  entradas atuais não presentes no arquivo ficam como sem categoria histórica.
- `alvos_prioritarios_nucleo.csv`: ajuda a classificar impacto, mas jamais
  transforma aprovação estrutural em certificação semântica.

## Automação do GitHub

O workflow `.github/workflows/re-t39-task-orchestrator.yml` roda em PRs
com alterações relevantes, pushes à main, manualmente e a cada seis horas.
Compila? **Não.** Faz uma auditoria barata, somente de leitura, vinculada
ao SHA-256 fixado do ELF e publica dois artefatos com retenção de 14 dias:

- `task40-triage.json`: todos os 40 estados inferidos do registro, tarefas
  parciais e **todas** as candidatas a intervalo T04 e revisão T06;
- `task40-triage.md`: resumo com prioridades e próximos gates.

O workflow não baixa OBB do Git LFS, não publica binários, não usa token
com direito de escrita, não executa `git push`, nem altera certificados,
marcos de revisão ou código do jogo.

## Critério para priorização

T04: validar proveniência SHA, limites e soma exata dos intervalos;
dar preferência a regiões com destino de `.init_array/.fini_array`
ou prólogo estrutural plausível, favorecendo fatias pequenas de análise.

T06: usar a fila atual de 53 em vez do relatório de 50; priorizar
entradas Thumb, núcleo, tabelas não resolvidas, ausências na triagem
histórica e checkpoints históricos `read_full` ainda não reexecutados.

T05: reconciliação do ledger (incluindo as regiões T04 novas) continua
manual/semiautomática; nenhuma entrada nova é inserida automaticamente
no inventário. Mapeamentos ARM/x86, dados embutidos e aliasing exigem
prova individual.

## Próxima evolução

Conectar a fila ordenada a pequenos lotes **separados por classe de prova**,
com Unicorn e diferencial C/C++ apenas após validar CFG, ISA, memória e
fronteiras de chamada. Manter a revisão humana independente e o gate
semântico já existente.

**Fronteira de confiança:** nenhuma candidatura de ferramenta é
considerada função descoberta de forma conclusiva, certificado semântico
ou evidência de app Android finalizado.
