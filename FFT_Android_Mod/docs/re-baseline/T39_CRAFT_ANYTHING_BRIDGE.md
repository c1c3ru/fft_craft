# T39 - Ponte opcional de evidencias do Craft Anything para T04/T06

**Estado:** triagem de metadados, sem certificacao de funcao, sem executar terceiros no CI.

## Proveniencia

- Projeto original: https://github.com/storytold/craft-anything
- Inventario CLI/MCP: https://github.com/storytold/craft-anything/blob/main/docs/tools.md
- Formato de exportacao: core_evidence_export, bundle JSON versao 1 com subject.sha256, operation, locations e id.
- Licenca upstream: MIT ou Apache-2.0; o README o marca como early alpha. Nenhum codigo de terceiros e copiado nesta integracao.
- Ferramentas uteis: funcao, callers/callees, pseudocodigo, xrefs, fluxo de valores e Ghidra/Rizin opcional.
- Os leitores de arquivos de jogos consultados cobrem Unreal, Unity e Godot, sem prova de suporte ao FAT32/fftpack.bin do OBB do FFT.

## Como rodar localmente

1. Instalar/revisar o projeto upstream separadamente e executar craft-anything-cli doctor e commands.
2. Habilitar Deep mode somente no contexto autorizado de investigacao do ELF ARM original, com mesmo SHA-256 do FFT.
3. Inspecionar lacunas da fila T04/T06 e exportar usando core_evidence_export para um JSON privado local.
4. Gerar a fila com o orquestrador T39 e cruzar localmente:

    python3 FFT_Android_Mod/docs/re-tools/re_40_task_orchestrator.py --json-output /tmp/task40.json --md-output /tmp/task40.md
    python3 FFT_Android_Mod/docs/re-tools/t39_craft_anything_bridge.py --queue /tmp/task40.json --bundle /caminho/privado/craft-evidence.json --output /tmp/task40-craft-crossrefs.json

## Politica de confianca

- Bundle formato craft-anything-evidence-bundle/v1, limitado a 8 MiB e 5000 registros.
- Exigir sujeito native, SHA-256 do ELF compativel, enderecos de localizacao e IDs com formato valido.
- Nunca importar bytes, pseudocodigo, texto do alvo, comandos sugeridos, links nem instrucoes de agente.
- Os IDs ev_* nao sao revalidados criptograficamente: servem apenas para correlacao da proveniencia externa.
- Observed/Derived/Inferred no produto externo nao prova execucao da funcao nem equivalencia de memoria.
- A ferramenta apenas associa registros a intervalos T04 e enderecos T06; nao promove funcoes ou tarefas.
- Testes existentes, gate Unicorn e diferencial C/C++ continuam obrigatorios antes da revisao humana.
- O workflow T39 roda apenas os testes do adaptador com fixtures sinteticas; nao baixa Rust/Ghidra/OBB.
- Nao submeter ao GitHub o bundle original, que pode conter bytes ou pseudocodigo do binario analisado.

## Primeiro experimento

Comparar analise independente nas entradas Thumb 0x002c9115 e 0x002c9a25 e nos destinos de inicializacao das lacunas perto de 0x00071c50. Confirmar ISA, CFG e memoria no ELF original antes de qualquer conclusao.
