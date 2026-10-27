# sound_request: auditoria da entrada 0x271314

ELF SHA-256: bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc
ARM code window: 0x271314..0x271373, 96 bytes; window SHA-256: 3c0cb42974bebad0cee7142dd9083991beabe65a08997c0781ecb7f48328cbdb

## Desvios de entrada confirmados no ELF

| Origem ARM | Destino ARM | Opcode (4 bytes) |
|---|---|---|
| 0x26b374 | 0x2168e0 | 59adfeea |
| 0x2168e0 | 0x271314 | 8b6a01ea |
| 0x2168e4 | 0x27131c | 8c6a01ea |
| 0x2168f4 | 0x271318 | 876a01ea |

## Decodificacao linear A32 (nao equivale a alcance de fluxo)

As entradas 0x271314 / 0x271318 / 0x27131c podem ter precondicoes diferentes. Dados inline podem decodificar como ARM.

| Endereco | Opcode (4 bytes) | Instrucao ARM | Operand classification |
|---|---|---|---|
| 0x271314 (entry) | 770601ea | b #0x2b2cf8 | direct target=0x2b2cf8 |
| 0x271318 (entry) | 4a0401ea | b #0x2b2448 | direct target=0x2b2448 |
| 0x27131c (entry) | 010040e2 | sub r0, r0, #1 | no explicitly classified control/data operand |
| 0x271320 | 3b0501ea | b #0x2b2814 | direct target=0x2b2814 |
| 0x271324 | 10402de9 | push {r4, lr} | no explicitly classified control/data operand |
| 0x271328 | 010040e2 | sub r0, r0, #1 | no explicitly classified control/data operand |
| 0x27132c | 0140a0e1 | mov r4, r1 | no explicitly classified control/data operand |
| 0x271330 | 370501eb | bl #0x2b2814 | direct target=0x2b2814 |
| 0x271334 | 010044e2 | sub r0, r4, #1 | no explicitly classified control/data operand |
| 0x271338 | 1040bde8 | pop {r4, lr} | no explicitly classified control/data operand |
| 0x27133c | 340501ea | b #0x2b2814 | direct target=0x2b2814 |
| 0x271340 | 1eff2fe1 | bx lr | indirect=lr |
| 0x271344 | 9a0501ea | b #0x2b29b4 | direct target=0x2b29b4 |
| 0x271348 | 1eff2fe1 | bx lr | indirect=lr |
| 0x27134c | 10402de9 | push {r4, lr} | no explicitly classified control/data operand |
| 0x271350 | 0040a0e1 | mov r4, r0 | no explicitly classified control/data operand |
| 0x271354 | 010040e2 | sub r0, r0, #1 | no explicitly classified control/data operand |
| 0x271358 | 0e0501eb | bl #0x2b2798 | direct target=0x2b2798 |
| 0x27135c | ad0501eb | bl #0x2b2a18 | direct target=0x2b2a18 |
| 0x271360 | 000050e3 | cmp r0, #0 | no explicitly classified control/data operand |
| 0x271364 | 0000000a | beq #0x27136c | direct target=0x27136c |
| 0x271368 | 1080bde8 | pop {r4, pc} | no explicitly classified control/data operand |
| 0x27136c | 0400a0e1 | mov r0, r4 | no explicitly classified control/data operand |
| 0x271370 | 1040bde8 | pop {r4, lr} | no explicitly classified control/data operand |

## Estado dos contratos e limites

- Confirmado: entradas e opcodes A32 originais e janela de 96 bytes.
- Ainda NAO executado: qualquer instrucao deste destino.
- Nao conhecido: efeitos em dados, retorno, acessos indiretos, outros sucessores e comportamento do subsistema de som.
- Proxima etapa: microexecucao limitada e rastreada de caminhos reais, com estado controlado; parar ANTES de chamadas ou destinos desconhecidos.
- Novas certificacoes: 0. As 303 provas BX LR ja aprovadas permanecem validas.
