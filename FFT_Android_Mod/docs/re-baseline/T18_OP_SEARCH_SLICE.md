# T18 (fatia vertical) — VM de eventos: reconstrução C diferencialmente testada de `op_search(int, int)`

Depende de T08–T10 (feitas). Executado em 2026-11-01, quarta fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T18 completo exige fechar `event_call` (5.456 B), `worldmap_call` (3.520 B), `Wevent_call` (2.040 B) e `op_attackteam` (12.272 B) — o dispatcher central de bytecode de evento segue fechado. Esta tarefa fecha e reconstrói uma função pequena do mesmo cluster.

## 1. Por que esta função

Os alvos nominais de T18 (`event_call`, `worldmap_call`, `op_attackteam`) são todos `read_structural` e grandes (2–12 KB). Busca por nome no mesmo cluster (`op_*`) achou `op_search(int, int)` (96 B, `read_structural`) — pequena o bastante, e **a única das quatro fatias desta sessão sem nenhuma chamada externa** (0 `bl`), toda a lógica auto-contida num laço.

## 2. Leitura e verificação por execução real

`op_search(int eventId, int searchTag)` (`0x26a674`, 96 B): busca linear numa lista de entradas de 4 bytes (byte baixo = "tag"), com sentinela (`tag==1`) e limite de 256 entradas (`0x400` bytes). Documentado em `NOTES §664`.

```c
uint32_t op_search(int eventId, int searchTag) {
    void** eventTable = *(*table_ptr_slot);   // dois níveis de indireção via GOT
    uint32_t packed = ((uint32_t*)eventTable)[eventId + 1];
    void* base = *base_val_slot;
    uint8_t* entryList = (uint8_t*)((packed & ~3) + (uintptr_t)base);
    for (uint32_t offset = 0; offset < 0x400; offset += 4) {
        uint32_t word = *(uint32_t*)(entryList + offset);
        uint8_t tag = (uint8_t)word;
        if (tag == (uint8_t)searchTag) return word;   // retorna a ENTRADA, não um booleano
        if (tag == 1) break;                            // sentinela
    }
    return 0;
}
```

**A primeira tentativa de reprodução contra o ELF real falhou** com acesso a memória não mapeada. A causa: a leitura inicial do disassembly viu dois `ldr` consecutivos (`ldr r3,[pc,r3]` depois `ldr r3,[r3]`) e tratou isso como "resolver um único ponteiro GOT" — na realidade são **dois saltos de indireção genuinamente distintos** (`table_ptr_slot → g`, depois `g[0] → eventTable`). Corrigido para três níveis, a execução bateu exatamente.

## 3. O que isso confirma e não confirma

**Confirmado por execução real sob Unicorn**: `eventId=3`, `searchTag∈{5,9}` (achadas, retornam a palavra completa de 4 bytes); `searchTag=7` (não encontrado, para no sentinela); limite de varredura em bytes, não em "1024 entradas" como uma leitura rápida do `cmp r3,#0x400` poderia sugerir sem conferir o incremento de `+4` por iteração.

**Não investigado**: a identidade de `g`/`eventTable` em si; o formato completo de uma entrada além do byte de tag (os 3 bytes superiores, usados como payload nos testes, têm papel real desconhecido); `event_call`/`worldmap_call` (os dispatchers que presumivelmente chamam `op_search`) não foram lidos.

## 4. Reconstrução C + teste diferencial

`docs/re-tools/c-models/t18_op_search.c` + `test_t18_op_search.py`: compila o modelo, executa a implementação original real via `differential_harness.py` para busca na 1ª entrada, 2ª entrada, e não-encontrado — **tudo bate exatamente**. Mais um teste confirmando que a interpretação original (dois níveis) geraria um endereço de tabela diferente do real (três níveis).

Suíte completa de `docs/re-tools`: **565 testes / 1.846 subtestes, todos passando** (561 antes + 4 novos).

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 664.
- `docs/RE_FUNCTION_INVENTORY.csv` — `op_search` promovida a `read_full`.
- `docs/re-tools/c-models/t18_op_search.c`, `test_t18_op_search.py`.
- Este relatório.
