# T39 — Execução real do Craft Anything e comparação ARM/Thumb

Este piloto concretiza a issue #560. É execução da **CLI upstream 0.3.0**,
separada da referência Capstone produzida pelo próprio fft_craft.
Não substitui Unicorn, equivalência C/C++ nem revisão independente.

## Segurança e custo

- Disparo apenas em PR que altera os três arquivos do piloto e por workflow_dispatch;
  sem execução por cron e sem custo adicional em todos os lotes ARM.
- Binário oficial Linux x86_64 tar.gz v0.3.0. SHA-256 externo fixo:
  `674ec59ffbdaefbd577917e07c9d464562043b275a3889ba4f60239a12f03d53`.
- Checkout sem persistência do token do GitHub; escopo `contents: read`;
  a CLI não recebe credenciais GitHub, cloud ou OpenAI, nem `--allow-run`.
- A versão, checksum e os resultados da CLI ficam separados dos dados de
  Capstone sobre o ELF de SHA `bf913415...4850bc`.
- Tempo limitado: 22 minutos por job, 90 segundos por comando upstream.
- Nenhum OBB, APK, dumps ou pseudocódigo são adicionados aos artefatos.
  Apenas endereços, mnemônicos saneados, hashes e estados de comparação.

## O que é medido

Para os quatro pontos conhecidos da referência `T39_CRAFT_PILOT.md`,
a ferramenta tenta `native_function_instructions_list`; se o upstream
não localizar uma função, tenta `native_instruction_show` no primeiro endereço.
Ambos executam o analisador nativo de verdade contra o ELF original.

A comparação de instruções é exata por endereço, tamanho, SHA-256
dos bytes de cada opcode e mnemônico, informando ausências e diferenças.
Para saltos diretos ARM/Thumb compara o alvo decodificado por Capstone com
o destino informado pelo Craft Anything quando exposto pelo seu `Flow`.
Alvo omitido é tratado como **não comparável**, nunca como confirmado.

É admissível que a ferramenta não reconheça as entradas Thumb ou o intervalo
desconhecido T04. O resultado deve preservar erros e lacunas em vez de
acrescentar funções imaginárias ao inventário.

## Saída

O workflow `re-t39-craft-runtime.yml` publica `t39-craft-actual-arm-comparison`
com JSON e Markdown sanitizados. Não publica o bundle integral do upstream.
Se nenhuma instrução for comparável, o job falha e deixa o artefato quando
possível para diagnóstico. Diferenças reais não são falhas do CI: são
candidatas a investigação de ISA/CFG e execução Unicorn.

## Critério pendente

Mesmo com coincidência perfeita de bytes e destinos de desvio, ainda faltam
reconstrução do CFG, confirmação de chamadores, efeitos de memória,
retornos condicionais e diferencial C/C++ para promover certificados.
Este piloto altera **zero** certificados e **zero** estados das 40 tarefas.

## Limitação encontrada na primeira execução (4 novembro 2026)

O teste do Craft Anything 0.3.0 no ELF original concordou integralmente com
Capstone na janela A32 da lacuna T04 (`0x00071c50`: 6/6 opcodes) e no
controle B01 (`0x000b9f7c`: 3/3). Nos dois endereços Thumb, a análise
original não retornou instruções equivalentes; em `0x002c9114` produziu
`stmdahs`, indício de decodificação como A32.

Ao inspecionar a fonte upstream v0.3.0 em `crates/disasm/src/image.rs`,
`mode_for()` escolhe um modo único para toda imagem ARM, usando o bit 0
em `bin.entry`. O binário misto ARM/Thumb não é reconfigurado por função.

Para **diagnosticar a limitação sem modificar o ELF original**, o piloto
agora gera duas cópias efêmeras e privadas, alterando exclusivamente os
quatro bytes do campo ELF32 `e_entry` (offset 0x18). Cada cópia aponta
para a entrada Thumb correspondente, preservando toda a seção executável.
A CLI é executada novamente nessas cópias derivadas com o modo global Thumb.
Os resultados são registrados à parte como
`forced_global_thumb_mode_diagnostic`, com novo hash de arquivo e flag
`not_original_elf_analysis=true`. Não são evidências vinculadas à identidade
SHA-256 do ELF original e não podem ser certificados ou inseridos no ledger.

Essa contraprova separa dois problemas: capacidade do decodificador Thumb
e incapacidade de alternar ISA dentro do mesmo ELF. Mesmo se os opcodes
coincidirem, o endereço/CFG da cópia não prova alcançabilidade do código
no aplicativo Android original.

## Segunda observação e próximo teste independente

A análise global Thumb forçada em cópias privadas do ELF reconheceu
dois prefixos de funções. O upstream chama saltos de quatro bytes
`bl.w`, enquanto Capstone usa `bl`: a comparação aceita essa diferença
de notação **somente quando tamanho e bytes do opcode forem idênticos**.

As instruções de desvio resultaram nas seguintes divergências entre
Capstone no ELF original e Craft Anything na cópia Thumb:

| Local | Capstone | Craft Anything |
|---|---|---|
| BEQ `0x002c9118` | `0x002c911e` | `0x002c911c` |
| BL `0x002c911a` | `0x002ce07c` | `0x002ce078` |
| BL `0x002c9a26` | `0x002c99b4` | `0x002c99b0` |

O gate `t39_thumb_branch_gate.py` agora executa esses opcodes originais
uma instrução por vez no Unicorn em modo Thumb, com flags Z controladas,
e verifica os registradores PC/LR e o retorno por fallthrough.
Esse teste está limitado a comportamento local de instruções e não
comprova a semântica completa de `operator delete` ou `operator new[]`.

A hipótese atual é que a diferença de modo global provoca a primeira
falha, e um cálculo impreciso de PC relativo na ferramenta externa
provoca as diferenças de destinos. A hipótese de PC deve ser comparada
ao resultado efetivo do Unicorn antes de ser considerada confirmada.
