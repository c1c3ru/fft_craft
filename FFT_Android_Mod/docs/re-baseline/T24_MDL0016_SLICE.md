# T24 (fatia vertical) — Modelos/animação: reconstrução C diferencialmente testada de `Mdl0016(short, int, int, int)`

Depende de T08–T10 (feitas). Executado em 2026-11-01, quinta fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T24 completo exige fechar toda a família `Mdl00XX` (~43 membros, `ASHURA_addPrim`, `CreateObjectWithTable`, `NewAnimation`, `executeShape` — não tocados). Esta tarefa fecha e reconstrói um membro da família.

## 1. Por que esta função

Levantamento da família `Mdl00XX` (43 membros não `read_full`) mostrou vários candidatos pequenos (84–244 B). `Mdl0016` (120 B, `read_structural`) foi escolhida por ter só 1 `bl` (externo, tratável como caixa-preta) e uma estrutura de máquina de estados clara, diferente em caráter das 4 fatias anteriores.

## 2. Leitura e verificação por execução real

`Mdl0016(short modelId, int p1, int p2, int p3)` (`0x23c6b0`, 120 B): máquina de 4 estados sobre um byte de efeito "neve" dentro de um sub-struct por modelo. Documentado em `NOTES §665`.

```c
uint8_t Mdl0016(short modelId, int p1, int p2, int p3) {
    uint8_t* entry = &g_mdlArray[modelId];       // stride 0xf8=248 B
    uint8_t* sub = entry + p1 + 0x20;
    uint8_t state = sub[2];
    if (state == 3) { sub[2] = 0; return 0; }
    if (state != 1) return state;                 // 0, 2, 4+: só relata
    int16_t myField = *(int16_t*)(entry + 0x28);   // relativo a `entry`, NÃO a `sub`
    int16_t globalField = *(int16_t*)(*(void**)g + 2);
    ASHURA_snowMatrix(0x96, globalField - myField);
    sub[2] = 2;
    return 2;
}
```

**Achado**: dos 4 parâmetros declarados (`short, int, int, int`), **só os 2 primeiros são lidos** — `p2`/`p3` nunca aparecem no corpo. Registrado para quem fechar outros membros da família `Mdl00XX` não presumir que todos os 4 parâmetros do template C++ uniforme importam em cada membro.

**Confirmado por execução real sob Unicorn** para os 3 estados com efeito (`1`→transição, com os argumentos exatos de `ASHURA_snowMatrix` verificados byte a byte: `r0=0x96`, `r1=globalField-myField`; `3`→reset; `0`→passagem direta) — sem nenhuma tentativa falha, porque a leitura já distinguiu corretamente que o campo `+0x28` é relativo a `entry` (antes de somar `p1`), não a `sub` (depois de somar `p1`) — a mesma classe de erro de offset já encontrada em T18/T26, evitada aqui por conferir isso antes de montar o teste.

## 3. Reconstrução C + teste diferencial

`docs/re-tools/c-models/t24_mdl0016.c` + `test_t24_mdl0016.py`: compila o modelo, executa a implementação original real via `differential_harness.py` para os 3 estados com efeito, incluindo 3 pares distintos de `(myField, globalField)` — **tudo bate exatamente**, retorno e byte de estado final. Mais um teste de injeção de falha: planta um valor diferente no endereço "errado" (`sub+0x28`, a hipótese de offset incorreta) e confirma que o ELF real usa o valor em `entry+0x28`, não o plantado no endereço errado.

Suíte completa de `docs/re-tools`: **569 testes / 1.849 subtestes, todos passando** (565 antes + 4 novos).

## 4. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 665.
- `docs/RE_FUNCTION_INVENTORY.csv` — `Mdl0016` promovida a `read_full`.
- `docs/re-tools/c-models/t24_mdl0016.c`, `test_t24_mdl0016.py`.
- Este relatório.
