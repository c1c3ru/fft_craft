# T04/T06 — piloto verificável de desmontagem ARM/Thumb com Craft Anything

## Propósito

Comparar uma segunda fonte de engenharia reversa (Craft Anything) contra referências
independentes e reproduzíveis obtidas diretamente do ELF ARM original, sem alterar
o ledger, a numeração de funções, os checkpoints ou a certificação semântica.

## Quatro pontos de controle

| Papel | Entrada ARM | Modo | Amostra |
|---|---|---|---|
| T06: revisão de `operator delete` | `0x002c9115` | Thumb (bytes em `0x002c9114`) | 20 bytes |
| T06: revisão de `operator new[]` | `0x002c9a25` | Thumb (bytes em `0x002c9a24`) | 20 bytes |
| T04: região não inventariada de inicialização | `0x00071c50` | ARM A32 candidato | 24 bytes |
| B01: controle já testado no diferencial C++ | `0x000b9f7c` | ARM A32 | corpo de 12 bytes |

O endereço Thumb marcado com bit 0 = 1 é preservado na análise de funções;
esse bit não é um byte extra e o arquivo é lido no endereço físico par.
Um decodificador produzir uma sequência plausível não comprova que a entrada é
alcançável, que o modo indicado está correto nem que o conjunto forma uma função.

## Execução automática no fft_craft

O workflow `re-t39-craft-pilot.yml` roda em PR, push relevante e manualmente.
Ele usa Capstone e pyelftools, verifica o SHA-256 do ELF original e as
filas T04/T06 atuais, e publica somente dados limitados de referência:
endereços, modos, hashes de janelas de código e mnemônicos iniciais.
Não publica bytes completos da biblioteca, não transfere OBB e não instala
nem executa o Craft Anything no GitHub Actions.

## Comparação independente via Craft Anything local

Referência upstream fixada para a avaliação: `b9ca099903aeef5d4b33a7e83e8e7062ab94c65a`.
A ferramenta upstream é early alpha e a exportação precisa ser inspecionada
antes da transferência; não submeter bundles de pseudocódigo ou bytes do jogo
a um repositório público.

Com a CLI já instalada e o ELF autorizado em um ambiente local, utilizar
`core_target_open`, `native_instruction_show`, `native_function_disassemble`,
`native_function_callers_list` e `core_evidence_export`. Selecionar explicitamente
Deep mode quando a análise de binário estiver autorizada.

Gerar a fila e a referência no diretório local:

    python3 FFT_Android_Mod/docs/re-tools/re_40_task_orchestrator.py \
      --json-output /tmp/task40.json --md-output /tmp/task40.md
    python3 FFT_Android_Mod/docs/re-tools/t39_craft_pilot_reference.py \
      --queue /tmp/task40.json \
      --json-output /tmp/pilot-reference.json \
      --md-output /tmp/pilot-reference.md

O argumento `--bundle /caminho/privado/craft-evidence.json` é opcional.
Quando fornecido, apenas associa IDs de evidência externa a endereços na
fila, mediante o adaptador T39 já existente; **não** valida ainda a igualdade
dos opcodes, disassembly ou fluxo de controle do Craft Anything.

## Aceitação e limitações

- SHA-256 do ELF original fixado, bytes provenientes de PT_LOAD executável;
- Entradas T04/T06 presentes nas filas atuais sem truncamento ou substituição;
- Primeiro conjunto de instruções analisado por Capstone A32/Thumb;
- Referência positiva B01 preserva o padrão MOV/STR/BX LR de 12 bytes;
- Bundle externo, se houver, é não confiável e não recebe mérito semântico;
- Zero certificados novos, zero checklists concluídos, zero 'equivalência integral'.

Para fechar a issue #560 ainda falta **executar realmente o Craft Anything**
no arquivo autorizado e confrontar seus resultados com esta referência.
Uma análise convergente passará posteriormente por CFG, retornos, memória
e testes diferenciais no ELF original antes de qualquer revisão independente.
