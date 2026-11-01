# T20 (fatia vertical) — Menus: reconstrução C diferencialmente testada de `iOSUnitListWinOnOff(int)`

Depende de T08–T10 (feitas). Executado em 2026-11-01, sexta fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T20 completo exige fechar `ItemMenu`, `eItemMenu`, `AbilityMenu`, `JobChange`, `UnitTable`, `UnitList`, `BattleUnitList` (6–16 KB cada, não tocadas). Esta tarefa fecha e reconstrói uma função pequena do mesmo cluster — e, no processo, encontra e corrige um bug real no harness de T10.

## 1. Por que esta função

Os alvos nominais de T20 são todos grandes (6–16 KB). Levantamento do cluster `UnitList*`/`iOSUnitList*` achou `iOSUnitListWinOnOff(int)` (88 B, `read_structural`) — pequena, com só 1 `bl` externo.

## 2. Achado estrutural: a primeira tail call real desta sessão

```c
int32_t iOSUnitListWinOnOff(int offFlag) {
    if (offFlag != 0) {
        return iOSUnitListWinOnOff_otherPath();  // pop{r4,lr}; b 0x15ee2c -- TAIL CALL, não bl
    }
    g_windowActive = 1;
    int posFlag = iOSdisp_personalWinPosGet();
    g_windowXOffset = (posFlag == 0) ? -0x78 : 0x78;
    return posFlag;   // r0 nunca é reatribuído depois do bl -- confirmado por execução, não suposto
}
```

Duas coisas que uma leitura apressada erraria: (1) o caminho `offFlag!=0` não usa `bl` — usa `pop {r4,lr}` seguido de `b` incondicional pra outra função, devolvendo o quadro de pilha antes de desviar (tail call de verdade, confirmada ao testar: o retorno observado é exatamente o que a função-destino retornaria); (2) o valor de retorno do caminho principal **é `posFlag`**, não `0` — `r0` nunca é reescrito depois da chamada a `iOSdisp_personalWinPosGet`. Confirmado testando com `posFlag ∈ {0, 5, -1, 0x7fffffff}` antes de escrever o modelo C — um modelo que assumisse "retorna 0" teria sido pego pelo teste de injeção de falha.

## 3. Achado no harness de T10: bug real, corrigido

Reproduzir a tail call contra o ELF real expôs um bug em `differential_harness.py`: a checagem de "chegou no sentinela de retorno" só rodava depois de uma chamada a `emu_start`, mas o caminho de `stub_calls` escreve `PC` direto (fora de `emu_start`). Quando o `LR` salvo já é o próprio sentinela — exatamente o caso de uma tail call — a próxima volta do laço executava uma instrução de verdade na página do sentinela (bytes zerados decodificam como um no-op que ainda avança `PC` em 4) antes de qualquer checagem perceber isso, resultando num erro de "sem stub" num endereço deslocado por 4 bytes. Corrigido conferindo o sentinela imediatamente após o redirecionamento de `stub_calls`.

`docs/re-tools/test_differential_harness_tail_call_stub.py` (1 teste novo) reproduz o bug isoladamente contra um ELF sintético e confirma a correção. A depuração desse teste revelou de passagem uma peculiaridade do Unicorn (não um bug do harness): um `emu_start(..., count=1)` que executa um `branch` pode falhar se a página de destino não estiver mapeada, mesmo sem chegar a executar nada lá — documentado no docstring do módulo para quem escrever testes sintéticos futuros.

## 4. Reconstrução C + teste diferencial

`docs/re-tools/c-models/t20_iosunitlistwinonoff.c` + `test_t20_iosunitlistwinonoff.py`: compila o modelo, executa a implementação original real via `differential_harness.py` (com o harness já corrigido) para o caminho principal (4 valores de `posFlag`) e o caminho de tail call (3 valores de retorno stubado) — **tudo bate exatamente**. Mais um teste de injeção de falha confirmando que a suposição "retorna 0" divergiria do ELF real.

Suíte completa de `docs/re-tools`: de 569 pra (569 + 1 regressão do harness + 3 desta fatia) = **573 testes**, todos passando — confirmado (`573 passed, 1856 subtests passed`).

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 666.
- `docs/RE_FUNCTION_INVENTORY.csv` — `iOSUnitListWinOnOff` promovida a `read_full`.
- `docs/re-tools/differential_harness.py` — corrige o bug do sentinela pós-stub; docstring documenta a peculiaridade do Unicorn.
- `docs/re-tools/test_differential_harness_tail_call_stub.py` — teste de regressão do bug do harness.
- `docs/re-tools/c-models/t20_iosunitlistwinonoff.c`, `test_t20_iosunitlistwinonoff.py`.
- Este relatório.
