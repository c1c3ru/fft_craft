# Automação de quatro frentes: T06/T12, B01, A04 e T14–T26

## Propósito

Workflow: `.github/workflows/re-four-track-automation.yml`.
Script de prova: `docs/re-tools/re_four_track_automation.py`.
Executa em PRs/pushes relevantes, sob demanda e segundas/quintas às 06:13 UTC.
Quatro jobs independentes; o dashboard somente publica quando **todos** passarem.
Escopo read-only, sem emuladores Android no cron, sem baixar OBB ou LFS;
`contents: read`, sem credenciais persistidas e sem alterar o ledger ou o checklist.

## T06/T12 — callers de alocação/desalocação

Executa os dois wrappers Thumb no ELF original via Unicorn contra callbacks
C++ compilados (7 cenários), confirma encaminhamento R0, SP/R3/PC e guarda
de ponteiro nulo. Conserva os 12 bytes não classificados do símbolo new[].
**Não** executa a semântica de alocação/desalocação dos callees reais
`0x002ce07c` e `0x002c99b4`. Issue #570 é o gate pendente.

## B01 — métodos nominais C++

Executa regressões negativas de C++ e chamadores delimitados e compara
os 7 corpos ARM de 12 bytes com modelos independentes em 672 cenários.
Não prova layouts de classe, objeto completo ou alcance dos chamadores
em runtime. Issue #494 é o gate pendente.

## A04 — JNI / segurança de strings

Roda testes negativos do validador do trace do Android original e
271 casos JNI reais **no host JVM** (GetStringUTFLength/Chars, MUTF-8
e limite de bytes 242/243). Rejeita qualquer relatório que alegue
ter amostras do processo Android original. Issue #464 só poderá ser
cumprida com captura autorizada de somente leitura no jogo original.

## T14–T26 — integração de subsistemas

Descobre e executa **29 módulos de teste** dos 13 workstreams T14–T26
(não aceita módulo ausente), incluindo diferenciais em código ARM original
com C e callbacks controlados. Em seguida executa `verify_stage.py`,
build host CMake e CTest do projeto de reconstrução independente.
Isto verifica regressões de fatias integradas no estágio, **não** demonstra
funcionamento completo de batalha, menus, gráficos, scripts ou gameplay.

## Gate de evidências

O consolidador exige os quatro relatórios, confirma SHA-256 fixado do ELF
`bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`,
população do ledger `semantic-certificates.json` e bloqueios explícitos.
Os 303 certificados atuais só são contados como **baseline**.
Mesmo com todos os testes verdes: 0 novos certificados, 0 estados T01–T40
alterados, 0 prova de execução do APK original no Android.

Artefatos: quatro relatórios compactos por frente (14 dias) e dashboard
JSON/Markdown consolidado para revisão (21 dias). Nenhum arquivo binário
original, string de path, bytecode ou pseudocódigo é publicado.

## Caminho para aumentar cobertura semântica

1. T06/T12: reconstruir e executar callees reais e observar efeitos de heap.
2. B01: associar layout de classes e chamadores verdadeiros a contratos C++.
3. A04: captar trace observacional no processo Android original.
4. T14–T26: implementar interfaces e testes de replay por subsistema.
5. Submeter contratos completos e evidências diferenciais à revisão
independente antes de inserir novos certificados no ledger.

Não duplicar workers agressivamente: o cron de lotes ARM e T39 permanece
ativo em frequência maior. Esta esteira transversal foi limitada a
duas execuções programadas semanais e acionamentos por alteração.
