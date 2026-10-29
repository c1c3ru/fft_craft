# A04 — Proveniência e limite da origem R1

**Objetivo da issue [#441](https://github.com/c1c3ru/fft_craft/issues/441):** reconstruir a origem de R1 para os 48 BL diretos A32 de `0x000b6620`, sem declarar segurança da cópia `strcpy` a partir do tamanho do destino.

## Modelo de evidência

O analisador `semantic_a04_r1_sources.py` lê o ELF original, protegido por SHA-256, e percorre uma janela A32 dentro do símbolo de cada callsite. Um *slice* reverso de R1 acompanha atribuições simples e preservação de registradores R4–R11 através de `BL`. Instruções que leem a pilha, cálculos de ponteiros, atribuições condicionais, barreiras de ABI e lacunas de desmontagem permanecem explicitamente classificadas como **candidatas sem garantias**.

Os 48 resultados ficam em um checkpoint JSON, com identificador de callsite, símbolo proprietário, evidências de definição de R1, tipo provável da origem e status `unresolved`. O CI executa a análise em três frentes paralelas (`file-io`, `shader`, `other`) e um gate agregado. Todos devem executar replay idêntico e produzir artefatos.

## Limite necessário e lacunas

`0x000b6620` chama `strcpy` sem conhecer o tamanho da origem. Para os objetos observados, a cópia precisa ficar dentro da região anterior ao metadado `+0x104`: **no máximo 259 bytes de conteúdo, seguidos de NUL**. O campo de metadados ocupa `0x104..0x107`. O modelo C independente aplica essa condição antes de copiar, mas o ARM original não verifica o comprimento internamente.

**Um rastreamento de registrador não é prova de NUL, comprimento máximo, capacidade real, não sobreposição ou alcançabilidade.** É indispensável confirmar os contratos dos produtores reais: parâmetros de APIs externas, nomes de arquivos, JNI, buffers de stack e dados de shader. O relatório deixa esses campos como falsos/nulos por padrão. Não devemos incrementar métricas de cobertura sem testes semânticos que demonstrem o comportamento desejado.

## Critérios para próximos loops

1. Classificar cada origem como parâmetro ABI, transferência por registrador, leitura de campo, leitura de slot de pilha ou transformação computada, preservando o caminho das instruções.
2. Para cada família, encontrar o produtor de string, as verificações de NUL e o comprimento máximo, sem supor que um ponteiro válido tenha conteúdo limitado.
3. Testar as condições de fronteira de modo controlado em build/ambiente Android autorizado, sem chamar a `strcpy` original com entradas potencialmente excessivas fora de sandbox.
4. Atualizar a issue #441 com fontes demonstradas, pendências e risco de overflow por callsite.

**A04 permanece in_progress; nenhum certificado novo.**
