# Medição de produtividade real e desbloqueio de dependências (B01/A04)

## Finalidade

A frequência maior do workflow não implica equivalência. Este checkpoint
adiciona `semantic_velocity.py`, executado após produzir evidência do ELF
original e antes da regeneração de `STATUS_GERAL.md`. Os resultados são
persistidos em `SEMANTIC_VELOCITY_HISTORY.json` e resumidos em
`SEMANTIC_VELOCITY.md` com referência ao `GITHUB_RUN_ID`.

Os dados provêm de `semantic_coverage.ledger`,
`progress_report.summarize` e `RE_COMPLETION_TRACKER.json`, e não de
contadores extraídos de comentários de PRs, sumários de testes ou quantidades
de execuções Unicorn. São conjuntos de endereços únicos vinculados ao SHA-256
do ELF, sem dupla contagem de aliases. O gate de certificação independente
continua sendo obrigatório.

## Próximas frentes técnicas

- **B01 (P0 operacional):** demonstrar callers, layout e frames reais dos
  sete métodos já reimplementados em C++; resolver 6 destinos externos,
  4 callees sem efeitos modelados, 14 POP PC e a disponibilidade do OBB original
  sem alterar os denominadores apenas por conter código-modelo.
- **A04:** coletar métricas JNI do processo original autorizado, não somente
  do APK de diagnóstico; provar origem, terminação NUL e limite de 242 bytes
  para os caminhos relevantes; manter o `strcpy` original sem invocação insegura.
- **Contratos novos:** partir de uma família de funções com contrato integral
  e validador especializado, comparar Unicorn x implementação independente
  em C/C++ e obter revisão humana; não estender automaticamente o gate BX LR.
- **Reimplementação:** encadear memória, efeitos, retorno e fluxo de chamada,
  avançando de corpos de 12 bytes para subsistemas do game loop, áudio e JNI.
- **Medição:** acompanhar crescimento real de endereços certificados e bytes,
  alteração dos 50 checkpoints de revisão e status das 17 atividades.

## Regras de leitura

- Primeira execução é **linha de base**, e novos certificados atribuíveis ao
  primeiro run = desconhecidos, nunca 303.
- Execuções sucessivas detectam endereços adicionados, removidos, bytes e
  diferenças de checkpoints; IDs de run repetidos são idempotentes.
- Uma taxa de sete dias só existe quando uma observação precedente tem sete
  dias de distância; sem isso, **nenhuma previsão confiável**.
- O histórico rejeita mudanças de ELF e de inventário como se fossem
  progresso da mesma população. Exige nova linha de base auditada.
- Não gerar recibos, nem marcar B01/A04 done com base nessa medição.
- A taxa de certificação por endereço **não é** ETA da reconstrução funcional:
  JNI, APK/OBB, compatibilidade e validação final têm gates próprios.

## Execução

```bash
python3 FFT_Android_Mod/docs/re-tools/semantic_velocity.py
python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools \
  -p 'test_semantic_velocity.py' -v
```

O workflow de lotes publicará o histórico em PR automatizado, sujeito
ao mesmo controle de HEAD que protege checkpoints contra publicação obsoleta.
