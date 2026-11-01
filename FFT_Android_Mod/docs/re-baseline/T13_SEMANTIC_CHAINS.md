# T13 — Fechar as cadeias semânticas já iniciadas

Depende de T08–T12 (`ready_for_review`/`done`, parciais). Executado em 2026-10-31.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** Fecha os dois pontos de parada explicitamente citados pela própria tarefa (`0x2bf008`, `0x0a7034`), sem deixar callee desconhecido em nenhum dos dois. Não cobre os outros relatórios `SEMANTIC_*` citados (`houkoku_okng`, `sound_request`, `GetParam`/`GetScale` em conjunto, etc.) além do que eles já tinham; não confirma áudio real nem posicionamento real em dispositivo (sem acesso a hardware nesta sessão).

## 1. `0x2bf008` (`chkSeDouble()`) — fechado, sem callee desconhecido

Citado em `docs/re-tools/status_geral.py` como "Investigar o próximo BL de `SysSE_Play` depois do desvio condicionado". Lido por completo nesta tarefa (`NOTES §659`):

```c
bool chkSeDouble() {
    int v = iOS_getV2Icon(0xc8);   // consulta o slot de estado genérico 200
    return v != 0;
}
```

O único `bl` é `iOS_getV2Icon(V2ICON_DATA)` (`0x2b7ccc`), **já lida por completo** (`NOTES §559`, sessão anterior). Promovida de `read_structural` para `read_full` no CSV.

**Achado colateral**: `iOS_getV2Icon` já aparece documentado dezenas de vezes nas notas como uma tabela de estado genérica consultada por ID pequeno, não exclusiva de ícones de UI apesar do nome. `chkSeDouble` reaproveitando o slot `0xc8` (200) pro subsistema de som confirma essa hipótese de reuso cross-subsistema — registrado como achado, não como pendência nova.

## 2. `0x0a7034` (`CGX_SCREEN_CORRECT::GetOffset_1X`) — já estava fechado, só a fronteira estava desatualizada

Citado como "Investigar o próximo BL de `iOS_SetIconPosition` com os argumentos já observados" — mas o endereço já era `read_full` desde `NOTES §537` (2026-10-23, sessão anterior), com **zero `bl`**:

```c
void CGX_SCREEN_CORRECT::GetOffset_1X(float* outX, float* outY) {
    if (outX) *outX = this->field_0x10;
    if (outY) *outY = this->field_0x14;
}
```

Getter trivial com ponteiros de saída opcionais (checados por nulidade antes de escrever) — nenhuma chamada, nenhuma fronteira real pendente. A entrada em `CURRENT_SEMANTIC_BOUNDARIES` estava simplesmente desatualizada (a leitura de `§537` nunca foi cruzada de volta contra a lista de fronteiras do painel).

## 3. Correção feita no painel automático

`docs/re-tools/status_geral.py`: removidas as duas entradas resolvidas de `CURRENT_SEMANTIC_BOUNDARIES`, com comentário apontando para `NOTES §659`/`§537`. Mantida a terceira (`0x34615c`, inicialização/relocação em tempo de execução do slot de som) — **essa não foi investigada nesta tarefa** porque não é um callee desconhecido, é uma pergunta sobre estado em memória de processo real que o ELF estático não pode responder (precisa de execução em dispositivo/emulador, fora do escopo desta tarefa).

**`docs/re-results/STATUS_GERAL.md` não foi regenerado nesta tarefa.** Tentei reexecutar `status_geral.py` com `GH_TOKEN` (mesmo procedimento de T11, que reverifica as 303 aprovações ao vivo contra a API do GitHub) duas vezes; na segunda vez, em primeiro plano com timeout generoso, o processo foi encerrado (`SIGKILL`, código 137) depois de ~3m25s — consistente com um limite de processo longo deste ambiente, não com um defeito no script (a escrita é atômica via arquivo `.tmp` + `replace()`, confirmado que `STATUS_GERAL.md` não foi corrompido). A fonte da verdade (`status_geral.py`, `RE_FUNCTION_INVENTORY.csv`, `REVERSE_ENGINEERING_NOTES.md`) já está corrigida; o painel se autocorrige na próxima execução do workflow `re-batches.yml` em CI, que não tem esse limite de tempo de processo local.

## 4. O que fica pendente (bloqueia `done`)

1. **Áudio real / posicionamento real em dispositivo** — explicitamente exigido pelo critério de aceite de T13 ("confirmar áudio real e posicionamento real na integração, além de microexecuções") e **não feito nesta sessão** — não há dispositivo/emulador disponível aqui. `chkSeDouble`/`GetOffset_1X` ficam confirmados estruturalmente e por chamada, não por efeito observável em áudio/tela reais.
2. Os outros relatórios `SEMANTIC_*` citados (`houkoku_okng`, `V2Icon`, `sound_request`, `SysSE_Play`, `GetParam`, `GetScale`, `iOS_SetIconPosition`) não foram estendidos além do que já tinham — só os dois pontos de parada explícitos foram fechados.
3. `0x34615c` (inicialização/relocação em runtime do slot de som) continua aberto, por natureza — exige observação em processo real, não leitura estática.

## 5. Arquivos alterados por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — nova seção §659 (`chkSeDouble`).
- `docs/RE_FUNCTION_INVENTORY.csv` — `chkSeDouble` promovida a `read_full`.
- `docs/re-tools/status_geral.py` — remove as duas fronteiras resolvidas (painel se autocorrige na próxima regeneração em CI).
- Este relatório.
