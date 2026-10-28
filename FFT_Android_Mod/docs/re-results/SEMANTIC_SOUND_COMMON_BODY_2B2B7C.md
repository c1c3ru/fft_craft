# Corpo comum de som 0x2b2b7c — auditoria e execução limitada

ELF original SHA-256: bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc
Janela: 0x2b2b7c..0x2b2bfb (128 bytes).
Janela SHA-256: 9b1c66150261b090496c8016e0b9bf87d4fe3d4f505e677f80bb20c7b8d7ad4a

## Desmontagem A32 linear; alcance ainda nao demonstrado

| Endereço | Bytes do ELF | ARM | Risco de continuação |
|---|---|---|---|
| 0x2b2b7c | f0472de9 | push {r4, r5, r6, r7, r8, sb, sl, lr} | unmodelled-side-effect |
| 0x2b2b80 | 60319fe5 | ldr r3, [pc, #0x160] | memory-reference |
| 0x2b2b84 | 20d04de2 | sub sp, sp, #0x20 | a avaliar |
| 0x2b2b88 | 0060a0e1 | mov r6, r0 | a avaliar |
| 0x2b2b8c | 0150a0e1 | mov r5, r1 | a avaliar |
| 0x2b2b90 | 03009fe7 | ldr r0, [pc, r3] | memory-reference |
| 0x2b2b94 | 2810a0e3 | mov r1, #0x28 | a avaliar |
| 0x2b2b98 | e065ffeb | bl #0x28c320 | branch/call/return |
| 0x2b2b9c | 000050e3 | cmp r0, #0 | a avaliar |
| 0x2b2ba0 | 0600000a | beq #0x2b2bc0 | branch/call/return |
| 0x2b2ba4 | 014055e2 | subs r4, r5, #1 | a avaliar |
| 0x2b2ba8 | 0600003a | blo #0x2b2bc8 | branch/call/return |
| 0x2b2bac | 153100eb | bl #0x2bf008 | branch/call/return |
| 0x2b2bb0 | 007050e2 | subs r7, r0, #0 | a avaliar |
| 0x2b2bb4 | 0100001a | bne #0x2b2bc0 | branch/call/return |
| 0x2b2bb8 | a70f54e3 | cmp r4, #0x29c | a avaliar |
| 0x2b2bbc | 0500003a | blo #0x2b2bd8 | branch/call/return |
| 0x2b2bc0 | 20d08de2 | add sp, sp, #0x20 | a avaliar |
| 0x2b2bc4 | f087bde8 | pop {r4, r5, r6, r7, r8, sb, sl, pc} | PC-register |
| 0x2b2bc8 | 0600a0e1 | mov r0, r6 | a avaliar |
| 0x2b2bcc | 20d08de2 | add sp, sp, #0x20 | a avaliar |
| 0x2b2bd0 | f047bde8 | pop {r4, r5, r6, r7, r8, sb, sl, lr} | unmodelled-side-effect |
| 0x2b2bd4 | d7ffffea | b #0x2b2b38 | branch/call/return |
| 0x2b2bd8 | 0c319fe5 | ldr r3, [pc, #0x10c] | memory-reference |
| 0x2b2bdc | 0520a0e1 | mov r2, r5 | a avaliar |
| 0x2b2be0 | 08819fe5 | ldr r8, [pc, #0x108] | memory-reference |
| 0x2b2be4 | 03309fe7 | ldr r3, [pc, r3] | memory-reference |
| 0x2b2be8 | 005093e5 | ldr r5, [r3] | memory-reference |
| 0x2b2bec | 0410a0e1 | mov r1, r4 | a avaliar |
| 0x2b2bf0 | 0730a0e1 | mov r3, r7 | a avaliar |
| 0x2b2bf4 | 0500a0e1 | mov r0, r5 | a avaliar |
| 0x2b2bf8 | 3610f8eb | bl #0xb6cd8 | branch/call/return |

## Prefixo seguro observado

Primeira fronteira: 0x2b2b7c, motivo: unmodelled-side-effect.
Instruções elegíveis antes da fronteira: 0.
A instrução na fronteira NÃO é executada.
O código C do prefixo anterior entrega R0=0 e R1=argumento; esses são estados sintéticos para o próximo corpo.

Estados controlados verificados: 128 (8 R1 x 16 NZCV).
Instruções originais executadas por estado: 0.
Sem leitura/escrita de memória de dados antes da fronteira.
## Limites e próxima etapa

- Não foi executada a primeira instrução com efeito potencialmente externo.
- A janela linear pode conter dados inline e não prova fluxo além da fronteira.
- A semântica do áudio, parâmetros globais, retornos e efeitos externos continuam desconhecidos.
- Reconstituir explicitamente a primeira leitura/escrita ou chamada com memória mapeada e invariantes, antes de estender o contrato C.
- Novos certificados semânticos nesta etapa: 0; os 303 BX LR permanecem intactos.
