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


## Resultado executado no ELF original — run #40909542660

O [workflow com quatro jobs](https://github.com/c1c3ru/fft_craft/actions/runs/40909542660) passou no commit de implementação inicial: nove regressões unitárias e a análise determinística de **48/48 callsites**, divididos em **35 file-io, 11 outros e dois shader**.

| Classe conservadora do último rastreio de R1 | Quantidade |
|---|---:|
| `incoming_abi_argument_candidate` | 18 |
| `stack_pointer_derived_candidate` | 21 |
| `stack_slot_candidate` | 7 |
| `conditional_definition_unknown` | 2 |
| **Total** | **48** |

Evidência particular nos shaders: `0x000ab6a4` recebe R1 a partir do argumento de entrada R2; `0x000ab6cc` recebe R1 a partir do argumento de entrada R3, após transporte por registradores preservados. Nada nesse rastreio estabelece comprimento máximo ou NUL para essas entradas.

Alguns resultados dependem de fluxos de controle não modelados e slots de pilha não rastreados até os produtores. A classificação representa **candidatos de origem**, não validação do dado contido no endereço. O resultado de prova de NUL dentro de 260 bytes foi **0/48**, sem exploração de falha nem ensaio dinâmico de overflow. Essa ausência de prova não deve ser descrita como 48 vulnerabilidades confirmadas.

### Próximas experiências de alto impacto

- **18 argumentos ABI**: seguir o símbolo dono até os seus chamadores, incluindo API externa e JNI; recuperar garantia de comprimento e contratos de terminação.
- **21 endereços SP**: identificar qual chamada ou rotina preencheu a região local, se há escrita de NUL, e comparar capacidade com a região real de armazenamento.
- **7 slots de pilha**: rastrear o `STR` anterior de cada slot na mesma base SP e quaisquer alterações de SP; se houver branch, repetir por caminho.
- **2 definições condicionais**: reconstruir ambos os caminhos de controle e as fontes alternativas antes de decidir que o ponteiro é limitado.

A04 continua `in_progress`, sem promoção automática de cobertura ou certificados novos.


## Segundo salto: chamadores dos argumentos ABI — run #40910244917

O [workflow #40910244917](https://github.com/c1c3ru/fft_craft/actions/runs/40910244917) passou com um quinto job independente. O analisador `semantic_a04_r1_upstream.py` percorreu novamente o ELF ARM original e procurou `BL` A32 diretos para as funções que recebem `R1` por argumento ABI.

| Métrica de investigação | Resultado |
|---|---:|
| Usos de R1 classificados anteriormente como argumento ABI | 18 |
| Entradas de funções proprietárias distintas nesse grupo | 13 |
| Relações de chamadas A32 diretas contabilizadas pelos usos | 9 |
| Usos sem chamador A32 direto identificado | 10 |
| Fontes com NUL e comprimento máximo demonstrados | **0** |

Os casos sem `BL` direto identificável **não** foram classificados como código morto; podem ser chamados por Thumb/BLX, tabelas de função, JNI ou outros mecanismos ainda não observados.

Duas entradas do shader recebem a origem em argumentos ABI **R2** e **R3** e não tiveram chamadores A32 diretos encontrados nesse levantamento. Em BMP, TGA, TIM, abertura de DAT/TXT e utilitários de arquivos foram identificadas novas relações A32 candidatas que permitem continuar a busca no nível dos chamadores anteriores.

### Gate seguinte

1. Nos nove vínculos diretos identificados, rastrear o registrador ABI correspondente no chamador anterior; distinguir ponteiro de constante/literal, buffer construído localmente e parâmetro repassado.
2. Nos dez usos sem `BL` A32 direto, inventariar referências Thumb, BLX, vtable/indireção e entradas JNI. Nenhuma ausência de chamada A32 equivale a ausência de execução.
3. Para os 21 usos derivados de SP e sete recuperados de slots, rastrear instruções produtoras (escritas, formatação, cópias, leitura de arquivo) e a presença de NUL no percurso efetivamente executado.
4. Somente atribuir `bounded_nul_proven` após evidência de limite de **259 bytes de conteúdo**, terminador presente e condições de controle/aliasing; caso contrário manter `unresolved`.

Este segundo salto continua estrutural, não um certificado semântico.
