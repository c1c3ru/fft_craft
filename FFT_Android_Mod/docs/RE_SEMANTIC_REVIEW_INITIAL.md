# Revisão semântica inicial — funções ARM selecionadas

**Escopo:** evidência derivada dos checkpoints gerados pela análise estática do binário `libgl2jni.so`, sem execução dinâmica, pseudocódigo descompilado nem comparação com implementação-fonte. **Nenhuma função desta página foi certificada como semanticamente equivalente.** Os checkpoints originais permanecem `needs_review`.

## 0x002cd594 — `_Unwind_VRS_Pop` (856 B)

- Cobertura estrutural: **97,20%**; **1** tabela de salto resolvida, **0** não resolvidas; **5** casos/5 destinos, segundo `jtable.py`.
- Chamadas observadas: rotinas auxiliares `__gnu_Unwind_Restore_VFP`, `__gnu_Unwind_Save_VFP`, `__gnu_Unwind_Restore_VFP_D`, `__gnu_Unwind_Save_VFP_D`, `__gnu_Unwind_Restore_VFP_D_16_to_31`, `__gnu_Unwind_Save_VFP_D_16_to_31`, `__gnu_Unwind_Restore_WMMXD`, `__gnu_Unwind_Save_WMMXD`, `__gnu_Unwind_Restore_WMMXC`, `__gnu_Unwind_Save_WMMXC`.
- **Hipótese semântica:** despacho sobre classes de registradores durante operações de recuperação/restauração do estado de unwinding. Essa interpretação se apoia nos nomes dos símbolos e destinos de chamada; a semântica exata das condições e dos efeitos de memória **não foi demonstrada**.
- **Validação necessária:** desassemblar cada um dos cinco destinos (`0x2cd5c4`, `0x2cd60c`, `0x2cd8d8`, `0x2cd7f0`, `0x2cd870`), reconstruir a discriminação por classe de registrador, verificar limites e códigos de retorno contra a ABI ARM EHABI e testar estados de registradores representativos.
- **Decisão:** `needs_review` mantido. Cobertura de 97,2% não prova correção semântica.

## 0x0028179c — `iOS_v2menuSetType(V2MENU_TYPE)` (540 B)

- Cobertura estrutural: **94,81%**; **0** tabelas de salto; **5** desvios, sendo **4** candidatos a laço.
- Chamadas observadas: `RETINA_SCALE(int)` (11 ocorrências) e `iOS_getv2menuSprIdTbl()` (1 ocorrência).
- **Hipótese semântica:** seleção de configuração de menu e aplicação de escala de exibição a parâmetros visuais, apoiada no nome e nas chamadas; a ligação entre tipo, elementos e offsets ainda é desconhecida.
- **Validação necessária:** identificar os dados acessados e as atribuições por caminho, conferir limites de enum `V2MENU_TYPE`, efeitos colaterais, chamadas à tabela de sprites e ramos não percorridos pelo analisador.
- **Decisão:** `needs_review` mantido: cobertura abaixo de 95%, com sete slots estimados não alcançados (128 de ~135).

## 0x000df864 — `event_status_set(unsigned short, unsigned short)` (524 B)

- Cobertura estrutural: **93,13%**; **0** tabelas de salto; **17** desvios, dos quais **10** são candidatos a laço.
- Chamadas observadas: `task_wait(long)`, `asm_function(...)`, `get_bwp(int)`, `search_controlID(int, int*)`, `getBattleWorkIDFromAnimation(unsigned int)` e quatro símbolos locais sem dynsym (`sub_d6828`, `sub_dc2a4`, `sub_dd678`, `sub_df45c`).
- **Hipótese semântica:** atualização de estado de eventos com dependências de unidade/controle e sincronização; **não é seguro afirmar** transições de estado específicas sem inspecionar acessos a memória e caminhos condicionais.
- **Validação necessária:** reconstruir argumentos dos auxiliares locais, efeitos de escrita, condições de espera/saída e desvios indiretos; testar estados de controle válidos e inválidos.
- **Decisão:** `needs_review` mantido (122 de ~131 slots estimados).

## Próxima etapa técnica

1. Produzir desassemblagem dos caminhos não cobertos, registrando endereço e instrução de cada lacuna.
2. Extrair invariantes por bloco (entradas, saídas, mudanças de memória e condições de retorno) e comparar com a implementação prevista.
3. Associar testes diferenciais executáveis ou traces de emulador às invariantes antes de marcar `semantic_verified`.
4. Não alterar automaticamente os status do inventário nem converter `needs_review` em aprovação com base apenas em nomes, cobertura, Jaccard ou chamadas externas.

Fontes de evidência: `docs/re-results/002cd594.json`, `0028179c.json` e `000df864.json`. Estes registros são específicos do SHA-256 `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc` do ELF.
