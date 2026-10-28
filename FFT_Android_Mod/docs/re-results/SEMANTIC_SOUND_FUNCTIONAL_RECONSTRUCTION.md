# Reconstrução funcional parcial: sound_request -> SysSE_PlayDef

ELF original SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.
Bytes A32 executados em SysSE_PlayDef: `0010a0e10000a0e39dffffea`.

## 1. Desmontagem e estrutura verificadas

| Endereço | Instrução | Observação |
|---|---|---|
| 0x26b374 / 0x2168e0 / 0x271314 | B | Três desvios originais encadeados |
| 0x2b2cf8 | MOV R1,R0 | Copia identificador de entrada |
| 0x2b2cfc | MOV R0,#0 | Define primeiro argumento do próximo corpo como zero |
| 0x2b2d00 | B 0x2b2b7c | Desvio incondicional para corpo comum |

## 2. Contrato semântico observado no Unicorn

- Rastros verificados: 128 (8 valores R0 x 16 configurações NZCV).
- Na fronteira ANTES de 0x2b2b7c: PC=0x2b2b7c, R0=0, R1=R0 inicial.
- R2-R14, SP, LR e flags NZCV preservados; nenhuma leitura/escrita de dados.
- Precondições: A32 original, execução normal, estado e memória sintéticos.
- Nenhuma instrução do destino 0x2b2b7c foi executada.

## 3. Reimplementação independente em C

- Fonte: `docs/re-tools/c-models/sound_playdef_prefix.c`.
- Reimplementa somente o efeito observável deste prefixo; não reproduz áudio.

## 4. Validação diferencial

- 128/128 estados comparados Unicorn x C: PASS.
- Em todas as comparações: destino, R0 e R1 idênticos.
- Os demais registradores, flags e memória são validados no lado ARM.
- Nenhum certificado novo; não se demonstrou equivalência integral de SysSE_PlayDef.

## Próxima etapa técnica

- Desmontar e reconstruir o corpo comum em 0x2b2b7c.
- Resolver a proveniência das referências globais e chamadas antes de executar
  seus efeitos, controlando tabelas, estado e memória.
