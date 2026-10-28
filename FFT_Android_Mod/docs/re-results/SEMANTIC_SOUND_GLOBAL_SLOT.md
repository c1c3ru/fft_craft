# sound_request: proveniência da leitura global indireta ARM 0x2b2b90

ELF SHA-256: bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc

## Proveniência do endereço

- Opcode original: LDR R0,[PC,R3] em 0x2b2b90 (03009fe7).
- R3 vem da leitura original em 0x2b2ce8: 0x000935c4.
- PC A32 efetivo: 0x2b2b98; endereço PC+R3 = 0x34615c.
- Segmento PT_LOAD #3, flags=6, file-backed=True.
- Palavra armazenada no arquivo ELF neste slot: 0x019dd0d0. Isso NAO garante o valor depois de relocação/runtime.

## Registros de relocação exatamente no slot

- .rel.dyn: tipo 23, símbolo (não nomeado), addend None.

## Microexecução controlada do opcode original

- 512 execuções Unicorn (8 entradas x 16 NZCV x 4 valores SINTÉTICOS para a palavra do slot).
- Memória observada: uma leitura de 4 bytes em 0x34615c, nenhuma gravação de dados.
- R0 depois da instrução recebe a palavra sintética do slot; PC avança para 0x2b2b94; os outros registros e NZCV preservados.
- Instrução seguinte em 0x2b2b94 NÃO executada.
- Nenhum valor de memória do processo original foi medido em runtime.
- Não há reconstrução completa da chamada, retorno ou efeitos de áudio.
- Novos certificados semânticos: 0. Preservados os 303 BX LR anteriores.

## Próximo passo

- Resolver o estado global/relocação que popula o slot em runtime, com entradas e memória controladas, antes de executar chamadas ou substituir o ponteiro por um valor presumido.
