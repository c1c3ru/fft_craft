# FFT Craft — fluxo de reconstrução funcional ARM → C

**Objetivo:** reconstruir comportamento verificável do código ARM original, não maximizar o número de certificados ou checkpoints. Certificação formal fica como proteção adicional quando necessária.

## Unidade de trabalho

Cada função ou trecho delimitado possui: endereço e bytes do ELF, chamadas/saídas, hipóteses explícitas, contrato de entradas/efeitos, implementação candidata, testes diferenciais e fronteira **não** executada. Um relatório parcial não equivale à função completa.

| Etapa | Entrega rastreável | Gate mínimo |
|---|---|---|
| 1. Desmontagem e estrutura | Instruções A32/Thumb, entradas, CFG de blocos alcançáveis, alvos de desvio/BL, literais e lacunas | SHA-256 do ELF; entradas e bytes exatos; distinguir desmontagem linear, dados inline e alcance comprovado |
| 2. Reconstrução semântica | Pré/pós-condições, parâmetros por registrador, memória lida/escrita, efeitos, caminhos e chamadas | Execução original controlada (Unicorn), traces PC, R0–R14, CPSR, memória; stop antes de efeitos externos desconhecidos |
| 3. Reimplementação | C/C++ modular e independente limitado aos efeitos comprovados | Sem inventar efeitos; toda hipótese deve ser identificada; compilar com avisos como erros |
| 4. Equivalência | Testes diferenciais entre original e reimplementação | Casos extremos e diversos flags, comparação de saídas e efeitos, testes de regressão CI; declarar limites de cobertura |

## Priorização e estado

| Subsistema/trecho | Estrutura | Semântica | Implementação | Diferencial |
|---|---|---|---|---|
| `sound_request → 0x2b2cf8 → 0x2b2b7c` | Desvios e três instruções comprovados | Prefixo controlado, sem memória | C do prefixo em `docs/re-tools/c-models/sound_playdef_prefix.c` | 128 amostras A32 × C exigidas no CI da alteração |
| Corpo compartilhado em `0x2b2b7c` | Janela A32 de 128 bytes auditada e separação de instruções perigosas | Prefixo inicial executado sob estados controlados, interrompendo antes de qualquer efeito não modelado; relatório parcial | Não implementado | Apenas validação controlada do ARM, ainda sem comparação em C |
| Entrada alternativa `0x2b2d04` | Trampolim A32 auditado | A executar no escopo próprio | Não implementado | Não iniciado |
| Destino `0x2b2448` | Encaminhamento ARM identificado | Corpo não executado nesse experimento | Não implementado | Não iniciado |
| Destino `0x2b2814` | Encaminhamento e decremento de R0 identificados | Corpo não executado nesse experimento | Não implementado | Não iniciado |

## Execução reproduzível

Pré-requisitos no Ubuntu: Python 3, compilador C `cc`, `capstone`, `unicorn`, `pyelftools`. Executar na raiz do repositório:

```bash
python3 -m pip install capstone unicorn pyelftools
python3 FFT_Android_Mod/docs/re-tools/semantic_sound_functional_reconstruction.py
python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools -p 'test_semantic_sound_functional_reconstruction.py' -v
```

O relatório auditável produzido é `FFT_Android_Mod/docs/re-results/SEMANTIC_SOUND_FUNCTIONAL_RECONSTRUCTION.md`, vinculado pelo gerador de `STATUS_GERAL.md`.

## Política de publicação

- CI de testes e pipeline de evidência verdes **antes** de mesclar; publicar relatório junto ao código e ao hash do ELF.
- A revisão verifica se a fronteira de execução foi respeitada. Evidência parcial deve permanecer parcial.
- Divergência C/Unicorn falha o CI, sem mascarar divergências por ajuste de contadores.
- **Não promover automaticamente** contratos a certificados semânticos; aprovação formal é independente e opcional para esta rotina.
- Um caminho sem equivalência integral nunca será anunciado como substituição da função original.

## Próxima investigação

Revisar `docs/re-results/SEMANTIC_SOUND_COMMON_BODY_2B2B7C.md` para identificar a primeira barreira de execução no corpo compartilhado `0x2b2b7c`. Mapear somente a memória e os destinos exigidos pelo opcode original dessa barreira, verificar leituras/escritas/flags e construir o próximo trecho C/C++ apenas quando os efeitos forem confirmados. O relatório atual não certifica a função nem reproduz áudio.
