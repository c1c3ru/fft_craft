# Corpo comum de som 0x2b2b7c: prólogo ARM e reconstrução C

ELF SHA-256: bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc

## Instruções originais de 0x2b2b7c até 0x2b2b8c

- PUSH {R4,R5,R6,R7,R8,R9,R10,LR}: 8 palavras / 32 bytes gravados na pilha.
- LDR R3,[PC,#0x160]: lê literal original em 0x2b2ce8; valor=0x000935c4.
- SUB SP,SP,#0x20: 32 bytes adicionais, total de 64 bytes de profundidade.
- MOV R6,R0 e MOV R5,R1: entradas do wrapper R0=0, R1=argumento.
- Parada ANTES de 0x2b2b90: LDR R0,[PC,R3], acesso indireto a estado global.

## Verificação real e modelo independente

- Microexecuções Unicorn das 5 instruções reais: 128; instruções ARM efetivamente executadas: 640.
- Verificados: PC/SP/R0/R1/R3/R5/R6, demais registradores, 8 gravações da pilha, 1 leitura literal original e NZCV.
- Modelo C em docs/re-tools/c-models/sound_common_prologue.c, compilado com -std=c11 -Werror.
- Comparações diferenciais completas do prólogo ARM x C: 128/128 PASS.

## Limites

- Acesso indireto de 0x2b2b90 NAO foi executado; sem semântica de áudio, chamadas externas, retornos ou estado global comprovados.
- Nenhuma função adicional certificada; permanecem 303 contratos BX LR preexistentes, sujeitos ao gate independente.
- Próximo alvo: resolver proveniência e mapeamento seguro do ponteiro de 0x2b2b90 antes de executar sua leitura.
