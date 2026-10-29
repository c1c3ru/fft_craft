# A04 — Triagem paralela e limites estruturais dos 48 chamadores A32

**ELF original:** SHA-256 bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc.

## Resultado verificado nos dois jobs

No [GitHub Actions #40905433751](https://github.com/c1c3ru/fft_craft/actions/runs/40905433751), os dois jobs paralelos reproduziram os checkpoints do ELF:

| Grupo de chamadas diretas a 0x000b6620 | Quantidade | Natureza da evidência |
|---|---:|---|
| Padrão anterior estrito de operator new (MOV-only) | 34 | estática |
| Novas variantes de 0x10c com LDR/STR entre alocação e BL | 12 | estática |
| Shader com ponteiro transportado por R5 | 1 | origem stack local candidata |
| Shader com ponteiro construído em R6 | 1 | origem stack local candidata |
| **Total** | **48** | **não equivale a reachability provada** |

Logo, 46/48 possuem padrão de preparação de 268 bytes e chamada ao veneer Thumb de _Znwj (operator new); os outros dois pertencem ao símbolo CEGL2_SHADER::Load.

O [run #40905850904](https://github.com/c1c3ru/fft_craft/actions/runs/40905850904) passou com mais oito instruções originais verificadas e os limites geométricos seguintes (ainda sem executar o corpo do shader):

- Prólo​​go ARM: PUSH de nove registradores e SUB SP, SP, #0x234, reservando **564 bytes** depois do PUSH.
- No primeiro BL em 0x000ab6a4, R0 foi preparado por ADD R5, SP, #0x14; o espaço até o início da segunda região é 0x120 − 0x14 = **0x10c (268 bytes)**.
- No segundo BL em 0x000ab6cc, R0 recebe R6 produzido por ADD R6, SP, #0x120; há 0x234 − 0x120 = **0x114 (276 bytes)** até a extremidade da região reservada.
- Em ambos, cabem geometricamente os 0x108 bytes requeridos para acessar os quatro bytes de metadados em +0x104..+0x107, no caminho linear observado.
- Os registradores usados como origem dos dois buffers e SP não são explicitamente sobrescritos entre a formação do ponteiro e cada BL no prefixo original examinado.

## Bloqueador principal: comprimento e origem da string

A função ARM 0x000b6620 chama a importação strcpy. Nem o 0x10c passado para operator new, nem a reserva de pilha demonstram o comprimento máximo da string em R1.

A referência C segura aceita no máximo **259 bytes de conteúdo e um terminador NUL** antes da área de metadados (+0x104). O código original não realiza essa validação dentro da função. É necessário rastrear R1 em cada classe de callsite e seus caminhos de entrada, inclusive fontes de nome de arquivo, configurações e shader. Não executar entrada excessiva na libc original fora de um ambiente instrumentado e autorizado.

## Aceleração no próximo loop

1. Executar classificação de origem de R1 em lotes por símbolo/chamador, com separação entre parâmetro recebido, campo de objeto, leitura de stack e string constante, sem presumir comprimento.
2. Priorizar experimentos com proteção de memória, guard pages e ASan/Android instrumentado nos caminhos em que houver configuração e build controlado; não há prova atual desses ensaios.
3. Validar os dois CFG de shader e as rotinas de alocação no runtime em VM/dispositivo autorizado.
4. Manter A04 in_progress até resolver os destinos restantes, fallthrough 0x002b1bb0 → 0x002b1bb8, autoloop 0x002a1268, JNI e comportamento da libc real.

**Sem certificados formais novos, sem prova de alcance global, sem afirmação de segurança do strcpy e sem equivalência irrestrita.**
