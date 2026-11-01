# T25 (fatia vertical) — Áudio: reconstrução C diferencialmente testada de `CSOUND_IF_SL::Stop(int)`

Depende de T13–T14 (ambas `ready_for_review`). Executado em 2026-11-01, sétima fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T25 completo exige fechar BGM/SE, carregamento, codecs, mixer, canais, ganho, pitch, loop, comando JNI e player de filme — nenhum desses foi tocado aqui. Esta tarefa fecha e reconstrói uma função pequena e nominalmente citada pelo próprio texto de T25 ("stop e pausa"), reaproveitando dois campos de struct já confirmados no ciclo de vida completo do motor de áudio lido em 2026-10-16 (seções 16-17 das notas), sem reabrir essa leitura.

## 1. Por que esta função

Os alvos de T25 (BGM/SE, mixer, codecs, vídeo) não têm um candidato pequeno óbvio. Levantamento do cluster `CSOUND_IF*`/`CSOUND_IF_SL*` (que já tem 4 funções centrais lidas por completo, seções 16-17) achou várias funções pequenas (88–140 B) ainda `mentioned_unverified`: `CSOUND_IF_SL::Stop(int)` (88 B) foi escolhida por ser citada nominalmente no texto de T25 e por reaproveitar diretamente os dois campos de struct (`channelData`, `playItf`) já confirmados sem precisar relê-los.

## 2. Achado estrutural: três retornos, não dois

```c
int32_t CSOUND_IF_SL::Stop(int channel) {
    Channel* entry = &this->channelData[channel];   // +0x10, stride 0x88 (NOTES §17.1)
    if (entry->field_0x04 != 0 || entry->field_0x3c != 0) {
        SLPlayItf playItf = entry->playItf;          // +0x78 (NOTES §17.3)
        if (playItf != NULL) {
            entry->field_0x48 = 1;
            int32_t result = (*playItf)->SetPlayState(playItf, 1 /* SL_PLAYSTATE_STOPPED */);
            if (result == 0) entry->field_0x50 = 1;
            return result;
        }
        return 0;
    }
    return (int32_t)(intptr_t)this;   // *** r0 nunca é reescrito neste caminho ***
}
```

Uma leitura apressada assumiria "retorna 0 quando não há nada pra
parar". Os bytes reais mostram o contrário: no caminho em que nem
`field_0x04` nem `field_0x3c` estão marcados, `r0` nunca é tocado
depois da entrada na função — o retorno real é o próprio ponteiro
`this` (convenção ARM EABI, `this` chega em `r0`). Confirmado por
execução real sob Unicorn antes de escrever o modelo C, com teste de
injeção de falha dedicado.

## 3. Reaproveitamento de struct já confirmado, não relido

`this+0x10` (base de `channelData`, stride `0x88`) e `Channel+0x78`
(`playItf`) já estavam confirmados por leitura independente de
`EngineInit` (seção 17.1) e `Play()` (seção 17.3), respectivamente.
`Stop()` chama a mesma API OpenSL ES real (`SetPlayState`) por esse
mesmo campo, com o literal `1` (`SL_PLAYSTATE_STOPPED`) lido direto dos
bytes, não assumido da especificação. `Channel+0x4`, `+0x3c` (guarda
não-nulo, nunca desreferenciados aqui), `+0x48` e `+0x50` não têm nome
semântico confirmado por nenhuma outra função — mantidos como
`field_0xNN`.

## 4. Problema de largura de ponteiro entre host (64 bits) e struct ARM real (32 bits)

A primeira versão do modelo C tentava ler `channelData`/`playItf`
diretamente de um buffer de bytes no layout real de 32 bits da struct
ARM. Isso quebra ao compilar nativamente: um ponteiro real de 64 bits
do host não cabe nos 4 bytes que a struct ARM reserva pro campo.
Resolvido do mesmo jeito já usado em `c-models/t24_mdl0016.c` (parâmetro
`g`) e no callback de dupla indireção de T26: `channel_data` e
`playItf` são passados ao modelo como parâmetros nativos já resolvidos
pelo chamador/teste, não relidos de dentro de um blob de bytes no
formato ARM. Consequência: a comparação de memória entre os dois lados
do teste diferencial fica restrita aos dois campos `int32` simples
(`+0x48`/`+0x50`), não ao stride inteiro de 136 bytes — os únicos
campos que este teste pode comparar byte a byte entre host e ELF real
sem ambiguidade de largura de ponteiro.

## 5. Reconstrução C + teste diferencial

`docs/re-tools/c-models/t25_csoundifsl_stop.c` + `test_t25_csoundifsl_stop.py`: compila o modelo, executa a implementação original real via `differential_harness.py` (`stub_calls` com `callable`, extensão de T26) para 7 cenários: saída antecipada, `playItf` nulo, sucesso/falha da chamada virtual, e índice de canal não-zero (valida a aritmética `MLA` de stride) — **tudo bate exatamente**. Mais 2 testes de injeção de falha: um confirma que o retorno da saída antecipada não é `0`; outro confirma que `field_0x48` é marcado mesmo quando a chamada virtual falha.

Suíte completa de `docs/re-tools`: de 573 pra (573 + 3 desta fatia) = **576 testes** (1.856 → **1.863 subtestes**), todos passando (confirmado: `576 passed, 1863 subtests passed`).

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 667.
- `docs/RE_FUNCTION_INVENTORY.csv` — `CSOUND_IF_SL::Stop` promovida a `read_full`.
- `docs/re-tools/c-models/t25_csoundifsl_stop.c`, `test_t25_csoundifsl_stop.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T25 completo

BGM/SE, carregamento, codecs, mixer, ganho, pitch, loop, comando JNI e player de filme não tocados; restante do cluster `CSOUND_IF`/`CSOUND_IF_SL` (`Pause`, `StopAll`, `GetPlaySample`, `ClearSavedata`, `Static_Load`, `Unload`, ~125 funções `Stream_*`/`Static_Delete*`/`EngineUninit`/`CSOUND_LOADER_*`) intocado; nomes semânticos de `Channel+0x4`/`+0x3c`/`+0x48`/`+0x50` não confirmados por nenhuma função que os escreva com um nome já estabelecido.
