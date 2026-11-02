# T08 (fatia vertical) — Recuperação de tipos: primeira evidência de campo para `CARD_HEADER`

Depende de T04 (`ready_for_review`). Executado em 2026-11-02, décima oitava fatia vertical de P2.

**Estado: `ready_for_review` (fatia completa para esta função, não para T08 como um todo).** Esta tarefa fecha o quarto e ÚLTIMO dos quatro tipos que T08 (2026-10-31) listou como "sem nenhuma evidência de campo confiável" (`_Object`, `ActionRequest`, `FFT_SAVE_DATA`, `CARD_HEADER`) — os outros três foram fechados nas três fatias anteriores desta sessão. Com isso, **todos os quatro tipos de T08 têm agora pelo menos um campo confirmado**; T08 completo ainda exige estruturas gráficas e consolidação mais ampla.

## 1. Por que esta função

`MakeHeader(int,int,CARD_HEADER*)` é a ÚNICA função do inventário que referencia `CARD_HEADER*` no tipo. Já estava catalogada (seção 437 das notas, citada desde a seção 45) mas nunca lida linha a linha, porque o layout de `CARD_HEADER` nunca foi confirmado. Com 688 B e 6 `bl`, é bem maior que as fatias típicas desta sessão — mas era o único caminho para fechar o quarto tipo.

## 2. Método: sondagem empírica em vez de releitura manual de código de divisão gerado pelo compilador

Esta função tem divisão por constante (`/10`, `%10`) gerada pelo GCC via o idioma `smull`+`asr`+`rsb`, repetido 4 vezes, mais 2 chamadas reais a `__divsi3`/`__aeabi_idivmod` dentro de um laço de 2 iterações. Decodificar esse idioma manualmente levou a pelo menos um engano (a suposição inicial de que a 2ª iteração do laço sempre geraria o dígito "0" estava errada). Em vez de insistir na leitura manual, o efeito de cada bloco foi confirmado por **sondagem empírica**: executar o ELF real via Unicorn com valores de entrada distintos e reconhecíveis e ler os bytes de saída reais, comparando contra a hipótese `/10, %10` em C simples — que bateu exatamente. Mesma prática de "sondar em vez de reler manualmente" já usada nesta sessão (T18/T26).

## 3. Reconstrução

```c
void MakeHeader(int32_t a0, int32_t a1 /* NUNCA lido */, CARD_HEADER* out) {
    out->magic0 = 'S'; out->magic1 = 'C'; out->magic2 = 0x11; out->magic3 = 1;
    memset(&out->reserved_0x44, 0, 0x1c);
    memcpy(&out->title, TITLE_TEMPLATE_SHIFTJIS, 22);   // "ＦＦＴ　ＦＩＬＥ　　　"

    write_2digit_fullwidth(&out->field_0x14, a0 + 1);    // NÃO clampado

    int32_t hours = min(g_playTime.hours, 99);           // clamp INCLUSIVO
    write_2digit_fullwidth(&out->field_0x1a, hours);
    out->field_0x1e_colon = FULLWIDTH_COLON;

    int32_t minutes = min(g_playTime.minutes, 59);
    write_2digit_fullwidth(&out->field_0x20, minutes);
    out->field_0x24_colon = FULLWIDTH_COLON;

    int32_t seconds = min(g_playTime.seconds, 59);
    write_2digit_fullwidth(&out->field_0x26, seconds);
    out->field_0x2a_space = FULLWIDTH_SPACE;              // espaço, não dois-pontos

    int32_t flagResult = read_eventflag(0x31);             // 49, constante literal
    memcpy(&out->field_0x2c, &g_eventFlagTable[flagResult], 20);

    memcpy(&out->field_0x80, (uint8_t*)g_externalBlock + 0x20, 0x80);
}
```

## 4. Layout confirmado de `CARD_HEADER`

| Offset | Tamanho | Conteúdo |
|---|---|---|
| `+0x00`–`+0x03` | 4 B | `"SC"` + `0x11` + `0x01` |
| `+0x04`–`+0x19` | 22 B | Template Shift-JIS fixo: "ＦＦＴ　ＦＩＬＥ　　　" |
| `+0x14`–`+0x17` | 4 B | `a0+1`, 2 dígitos largos, NÃO clampado (sobrescreve o template) |
| `+0x1a`–`+0x1f` | 6 B | "HH：" — `min(horas,99)` |
| `+0x20`–`+0x25` | 6 B | "MM：" — `min(minutos,59)` |
| `+0x26`–`+0x2b` | 6 B | "SS␣" — `min(segundos,59)` + espaço (não dois-pontos) |
| `+0x2c`–`+0x3f` | 20 B | `eventFlagTable[read_eventflag(0x31)]`, stride 20 |
| `+0x44`–`+0x5f` | 28 B | Zerado (`memset`) |
| `+0x80`–`+0xff` | 128 B | `(struct externa)+0x20` |

Ver [`types/card_header.h`](types/card_header.h).

## 5. Achados adicionais

Os três valores de tempo (`horas`/`minutos`/`segundos`) são campos
contíguos de um único global (stride 4, base `0x56a904`) — confirma
um "tempo de jogo decorrido" `HH:MM:SS`. `a1` nunca é lido pelo corpo
real, confirmado também pelo teste diferencial. O índice de flag de
evento é uma constante literal (`0x31`=49), lida diretamente dos
bytes.

## 6. Teste diferencial

`docs/re-tools/c-models/t08_makeheader.c` + `test_t08_makeheader.py`: `memcpy`/`memset`/`__divsi3`/`__aeabi_idivmod` stubados via `callable` executando a operação real em Python (semântica padrão, não a codificação GCC — o lado ELF real continua exercitando seu próprio controle de fluxo e layout de bytes verdadeiro); `__stack_chk_fail` stubado para abortar o teste se alcançado; `read_eventflag` stubado via `callable`. 4 cenários batem exatamente byte a byte (incluindo valores bem além dos limites de clamp), mais 2 injeções de falha: limite de clamp inclusivo; `a1` realmente não afeta o resultado.

Suíte completa de `docs/re-tools`: de 604 pra (604 + 3 desta fatia) = **607 testes** (1.929 → **1.933 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 7. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 678.
- `docs/RE_FUNCTION_INVENTORY.csv` — `MakeHeader` promovida a `read_full`.
- `docs/re-baseline/types/card_header.h` — primeiro header do tipo, verificado por `static_assert`/`offsetof`.
- `docs/re-tools/c-models/t08_makeheader.c`, `test_t08_makeheader.py`.
- Este relatório.

## 8. Pendências que bloqueiam `done` de T08 completo

Estruturas gráficas seguem sem nenhuma evidência (quinto tipo citado no texto original de T08, fora da lista "quatro tipos sem evidência"); os 6 `bl` e os 2 runtime helpers (`__divsi3`/`__aeabi_idivmod`) não lidos em si; identidade semântica exata de `g_eventFlagTable`/struct externa em `0x541330`/`a0` não confirmada; `sizeof(CARD_HEADER)` real pode exceder `0x100`.
