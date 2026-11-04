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
