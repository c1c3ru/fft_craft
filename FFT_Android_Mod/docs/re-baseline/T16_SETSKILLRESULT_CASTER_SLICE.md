# T16 (fatia vertical) — Combate: reconstrução C diferencialmente testada de `setskillresult_caster(int)`

Depende de T08–T10 (feitas). Executado em 2026-10-31/2026-11-01, segunda fatia vertical escolhida ao continuar em P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T16 completo exige fechar `calc_result`, `getskillrange`, `getskilleffect`, `setskillresult` (2,7–3,8 KB cada, todas `read_structural`, não tocadas) — a fórmula de combate real segue fechada. Esta tarefa fecha e reconstrói só o wrapper pequeno que as invoca.

## 1. Por que esta função

Levantamento de todos os alvos nominais de T16 (`calc_result`, `getskillrange`, `getskilleffect`, `setskillresult`, `getTrapResultDamage`) mais busca por nome no CSV: `getTrapResultDamage` já estava `read_full` (fechada antes desta sessão); as outras quatro são `read_structural` e grandes (2,7–3,8 KB). Buscando por padrão de nome (`setskillresult_caster`) achei uma quinta função do mesmo cluster, **188 bytes, `mentioned_unverified`** — pequena o bastante pra reconstrução real nesta sessão, e que chama a própria `setskillresult` (tratada aqui como caixa-preta).

## 2. Leitura e verificação por execução real

`setskillresult_caster(int casterId)` (`0x1ce950`, 188 B): disassembly linear completo, depois **confirmado por execução sob Unicorn** (`differential_harness.py`, T10) com os 5 globais GOT-resolvidos (base compartilhada `0x347d58`) verificados byte a byte, não só por leitura manual. Documentado em `NOTES §662`.

```c
int setskillresult_caster(int casterId) {
    BWORK* bw = &g_bworkArray[casterId];
    g_currentCasterBwork = bw;
    if (casterId > 20) return -1;
    uint8_t flag = bw->caster_ready_flag_0x1;      // campo novo
    g_currentCasterId.byte_at_1 = (uint8_t)casterId;
    void* resultSlot = &bw->skill_result_kind_0x1ae;  // campo novo
    g_currentResultSlotPtr = resultSlot;
    if (flag == 0xff) return -1;
    copy_struct_data(&g_defaultSkillResultTemplate, resultSlot, 0x2e);
    setskillresult(casterId);
    if (((uint8_t*)resultSlot)[0] == 0) ((uint8_t*)resultSlot)[2] = 8;
    return 0;
}
```

## 3. Três campos novos de `BWORK`, consolidados em `types/bwork.h`

| Offset | Campo | Evidência |
|---|---|---|
| `+0x1` | `caster_ready_flag_0x1` — sentinela `0xff` = "não pode conjurar" | execução real, `flag=0xff → -1`; qualquer outro valor segue |
| `+0x1ae` | `skill_result_kind_0x1ae` — byte "tipo de resultado"; `0` após `setskillresult()` dispara fallback | leitura + execução |
| `+0x1b0` | `skill_result_fallback_0x1b0` — valor fixo `8` escrito quando o byte acima é `0` | leitura + execução |

O intervalo `+0x1ae`–`+0x1db` (46 B, resetado por `copy_struct_data`) coincide exatamente em tamanho e posição com o que já estava `_unknown` em `bwork.h` desde T08 — sem sobreposição com `byte_0x1ac`/`byte_0x1ad` (seção 653), confirmado por `offsetof` após a atualização do header.

## 4. Reconstrução C + teste diferencial

`docs/re-tools/c-models/t16_setskillresult_caster.c`: reimplementação C do wrapper, com `setskillresult`/`copy_struct_data` como ponteiros de função (caixa-preta, igual ao teste). `docs/re-tools/test_t16_setskillresult_caster.py`: compila o modelo, executa a implementação original real via `differential_harness.py` para `casterId ∈ {0,1,3,10,20,21}` e `flag ∈ {5, 0xff}`, compara retorno e os três ponteiros/bytes globais escritos — **tudo bate exatamente**, incluindo o limite `casterId==20` (inclusive, sucede) vs. `21` (falha). Mais um teste de injeção de falha confirmando que um offset de resultado errado (`+0x1a8` em vez de `+0x1ae`, um erro de "esquecer o +6") seria detectado.

Suíte completa de `docs/re-tools`: **557 testes / 1.840 subtestes, todos passando** (553 antes + 4 novos).

## 5. O que isso prova e o que não prova

**Prova**: para as entradas testadas, o wrapper C reproduz exatamente o estado final (ponteiros globais, byte de ID, valor de retorno) do binário ARM original, incluindo o limite exato de `casterId`.

**Não prova**: a fórmula de combate real (`setskillresult`, 3.844 B, não lida — tratada como caixa-preta nos dois lados); o conteúdo dos 44 bytes restantes do slot de resultado; `copy_struct_data`/`g_defaultSkillResultTemplate` em si.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 662.
- `docs/re-baseline/types/bwork.h` — 3 campos novos, verificados por `offsetof`.
- `docs/RE_FUNCTION_INVENTORY.csv` — `setskillresult_caster` promovida a `read_full`.
- `docs/re-tools/c-models/t16_setskillresult_caster.c`, `test_t16_setskillresult_caster.py`.
- Este relatório.
