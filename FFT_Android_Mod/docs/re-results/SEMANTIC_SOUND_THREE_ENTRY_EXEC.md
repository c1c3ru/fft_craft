# sound_request: três entradas A32 microexecutadas no ELF original

ELF SHA-256: bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc

## Rotas de entrada verificadas ate antes do proximo destino

| Estado de entrada | Instrucoes ARM originais executadas | Destino nao executado | R0 final | Testes |
|---|---|---|---|---|
| sound_request, 0x26b374 | 0x26b374 -> 0x2168e0 -> 0x271314 | 0x2b2cf8 | R0 preservado | 128 |
| relay_f4, 0x2168f4 | 0x2168f4 -> 0x271318 | 0x2b2448 | R0 preservado | 128 |
| relay_e4, 0x2168e4 | 0x2168e4 -> 0x27131c -> 0x271320 | 0x2b2814 | (R0 - 1) & 0xffffffff | 128 |

Microexecucoes Unicorn verificadas: 384 (3 entradas x 8 R0 x 16 NZCV).
Todos os casos verificaram fluxo, R0-R14, SP/LR, flags NZCV, memoria sentinela e ausencia de acesso a dados nestes prefixos.

## Limites de evidencia

- Somente a entrada chamada sound_request e confirmada como parte da cadeia que parte de 0x26b374.
- As entradas relay_f4 e relay_e4 foram testadas isoladamente; nao foi provado que sound_request as alcance em tempo de execucao.
- Destinos 0x2b2cf8, 0x2b2448, 0x2b2814 NAO foram executados; sem efeitos sonoros, sem retornos ou equivalencia global inferidos.
- Novos certificados neste relatorio: 0. As 303 certificacoes da classe BX LR permanecem inalteradas.
