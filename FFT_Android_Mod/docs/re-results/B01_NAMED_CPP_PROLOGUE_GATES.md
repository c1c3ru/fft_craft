# B01 — reimplementação nominal C++ e ligações de prólogo/epílogo

**Situação:** B01 in_progress. Este ciclo documenta sete efeitos de métodos independentes e mantém dez fronteiras externas e o vínculo dos stack frames em revisão. O SHA-256 do ELF original é `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Reimplementação C++ com contrato parcial baseado no ELF

Em `c-models/b01_named_cpp_methods.cpp`, as funções são agrupadas por classes com nomes derivados do inventário; esses nomes **não provam** o layout das classes. Em vez de reinterpretar buffers como objetos C++ incompletos, usamos `ObjectView` com escrita explícita little-endian de 32 bits, tamanho verificado e recusa de ponteiros nulos. A API exportada `fft_b01_named_cpp_method` é uma interface experimental de teste, não substituto pronto de JNI ou de classes do aplicativo.

| Entrada ARM | Método nomeado | Efeito que o ELF demonstra |
|---|---|---|
| `000b3518` | `CINPUT_DATA::CINPUT_DATA()` | `[R0+0x000] = 0` |
| `000b9f7c` | `CTHREAD::RequestExit()` | `[R0+0x014] = 2` |
| `000b9fac` | `CTHREAD::RequestSuspend()` | `[R0+0x014] = 8` |
| `000b9fb8` | `CTHREAD::RequestResume()` | `[R0+0x014] = 1` |
| `000bdb60` | `CSTEP::CSTEP()` | `[R0+0x000] = 0` |
| `000be1dc` | `CSTEP_BATCH::Uninit()` | `[R0+0x020] = 0` |
| `0028de9c` | `xpApiEnv::initCARD(long)` | `[R0+0x304] = 1` |

`b01_named_cpp_differential.py` faz uma checagem independente do encoding **MOV imediato → STR word → BX LR** dos sete corpos de exatamente 12 bytes. Rejeita alteração de opcodes, tamanho/offset e constantes antes do diferencial, evitando que a implementação e a expectativa sejam derivadas do mesmo modelo. Executa o ARM original em Unicorn com quatro bases de objeto, seis padrões de registradores, duas condições de flags e dois retornos LR, comparando o buffer integral e o canário, as escritas observadas, as flags e os registradores relevantes. O modelo C++ é compilado por `c++ -std=c++17 -O2 -Wall -Wextra -Werror`. Testes negativos exigem que ponteiros nulos, tamanhos insuficientes e endereços de entrada desconhecidos não modifiquem memória. A validação de seis estados × quatro bases × duas flags × dois retornos produz **96 casos por entrada**, se todos forem aprovados.

O contrato de chamada de `R0=this` é uma hipótese AAPCS32, não prova da identidade de campos, dos chamadores nem das pré-condições do jogo. Em particular, o argumento de `xpApiEnv::initCARD(long)` não foi interpretado como significado de negócio.

## Correlacionar PUSH com POP PC sem inventar fluxo

`b01_prologue_external_audit.py` reusa os percursos recursivos do ELF original e recolhe os 28 retornos por pilha identificados anteriormente (14 instruções distintas). Para cada retorno procura `PUSH` anteriores no mesmo conjunto de instruções decodificadas, comparando máscaras de registradores (`LR` salvo e `PC` restaurado). Uma máscara compatível é um **candidato de prólogo**, não garante que foi executado na mesma trajetória nem demonstra o frame em tempo real. Falta conferir efeitos de SP e caminho completo, inclusive nos quatro retornos condicionais.

O mesmo relatório cataloga os **seis destinos diretos fora de janela** e as **quatro chamadas externas** com efeito desconhecido. Um destino localizado no inventário é apenas associação por endereço: não atesta callee nem resolve o retorno. Nenhuma transferência é executada pelo novo auditor.

## Próximo gate

1. Vincular os sete métodos aos chamadores que montam os objetos e às transições C++ observáveis, documentando invariantes de layout e tamanho real.
2. Transformar os candidatos `PUSH/POP` em provas por trajetórias completas, sem supor a execução de todas as arestas estáticas.
3. Reconstruir o efeito dos seis destinos externos e dos quatro callees por ELF e testes diferenciais seguros; preservar `unresolved` se faltar prova.
4. Concluir os gates independentes da B01: Smali/JNI de runtime original e OBB materializado, antes de desbloquear A03/R01/R02.

**Nenhuma certificação semântica de função inteira será emitida automaticamente.** O relatório e o dashboard permanecem auditáveis e sem alterações nas 2/17 atividades formalmente concluídas.
