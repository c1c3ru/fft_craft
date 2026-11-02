# T26 (fatia vertical) — Integrações herdadas: reconstrução C diferencialmente testada dos stubs NetBattle/iCloud

Depende de T09 (`ready_for_review`). Executado em 2026-11-02, décima quarta fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** T26 completo exige verificar o uso real de todas as funções `pspNet*`, distinguir caminhos ativos no Android, stubs, símbolos herdados e modos inacessíveis, com trilha de alcançabilidade por recurso. Esta tarefa fecha 5 funções minúsculas que são, pelo próprio byte, exatamente o tipo de stub que o critério de aceite de T26 pede pra não confundir com funcionalidade ativa.

## 1. Por que este grupo

`NetBattleJudge()`, `getNetBattleJudge()`, `iCloud_Send()`, `iCloud_Receive()`, `iCloud_GetSlotCount()` foram achadas por busca de nome direta no cluster `NetBattle`/`iCloud` citado em T26. Todas têm 4–8 bytes, 0 `bl`, 0 branch — fechar as cinco juntas é o exemplo mais direto possível do critério de aceite de T26: "símbolo de rede/iCloud isolado não vira afirmação de funcionalidade ativa".

## 2. Reconstrução

```c
void NetBattleJudge(void) { /* bx lr isolado -- literalmente nada */ }
int32_t getNetBattleJudge(void)   { return 3; }
int32_t iCloud_Send(void)          { return 1; }
int32_t iCloud_Receive(void)       { return 1; }
int32_t iCloud_GetSlotCount(void)  { return 0; }
```

## 3. Achado: confirmado pelos bytes, não assumido

Todas as cinco são retornos constantes incondicionais, independentes
de qualquer entrada — nenhuma lê `r0`–`r3`, nenhuma acessa memória,
nenhuma chama outra função. `NetBattleJudge` é o caso mais extremo: um
único `bx lr`, sem nenhuma instrução antes — nunca escreve `r0`,
então seu "valor de retorno" é literalmente o que já estava em `r0`
ao entrar, não uma constante como as outras quatro. Confirmado por
injeção de falha com dois valores de entrada distintos, ambos
preservados exatamente (nenhuma constante escondida).

**Importante, para não exagerar a conclusão**: isso não afirma que
nenhuma das cinco é chamada no build Android em runtime — só que o
corpo de cada uma, isoladamente, é um stub inerte. Alcançabilidade
real fica fora do escopo desta leitura estrutural.

## 4. Teste diferencial

`docs/re-tools/c-models/t26_netbattle_icloud_stubs.c` + `test_t26_netbattle_icloud_stubs.py`: as 5 funções testadas com 5 valores de entrada distintos cada (25 subtestes) batem exatamente com o ELF original, mais 1 injeção de falha confirmando que `NetBattleJudge` não é "mais uma constante" do grupo (preserva o `r0` de entrada, não retorna um valor fixo).

Suíte completa de `docs/re-tools`: de 594 pra (594 + 2 desta fatia) = **596 testes** (1.890 → **1.915 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 674.
- `docs/RE_FUNCTION_INVENTORY.csv` — as 5 funções promovidas a `read_full`.
- `docs/re-tools/c-models/t26_netbattle_icloud_stubs.c`, `test_t26_netbattle_icloud_stubs.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T26 completo

Alcançabilidade real (se alguma das cinco é chamada em runtime no build Android) não investigada; restante do cluster `pspNet*` (além de `pspNetPadRead`, já fechada em slice anterior), `xpPadKeyBufGet`, helpers C++ e codecs não tocados; trilha de alcançabilidade por recurso não produzida.
