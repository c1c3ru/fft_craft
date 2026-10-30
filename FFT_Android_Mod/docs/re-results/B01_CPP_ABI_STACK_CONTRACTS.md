# B01 — contratos C++ provisórios dos sete corpos ARM e retornos por pilha

**Status:** B01 `in_progress`. Este documento distingue inferência sobre AAPCS32 e estrutura de objeto de equivalência funcional em estados controlados. Nenhuma contagem cria certificado por si.

## Sete entradas com 12 bytes e BX LR (issue #494)

`b01_seven_cpp_contracts.py` lê o ELF ARM de SHA-256 fixado e os nomes do inventário, mantendo **sete endereços únicos** mesmo quando C1/C2 compartilham a mesma implementação. Os nomes sugerem contratos C++:

| Entrada ELF | Símbolo do inventário | Semântica de nome ainda não provada |
|---|---|---|
| `0x000b3518` | `CINPUT_DATA::CINPUT_DATA()` | Construtor; aliases C1/C2 |
| `0x000b9f7c` | `CTHREAD::RequestExit()` | Alteração de estado de thread |
| `0x000b9fac` | `CTHREAD::RequestSuspend()` | Alteração de estado de thread |
| `0x000b9fb8` | `CTHREAD::RequestResume()` | Alteração de estado de thread |
| `0x000bdb60` | `CSTEP::CSTEP()` | Construtor; aliases C1/C2 |
| `0x000be1dc` | `CSTEP_BATCH::Uninit()` | Reinicialização/limpeza |
| `0x0028de9c` | `xpApiEnv::initCARD(long)` | Método com argumento adicional |

A aplicação da ABI AAPCS32 a métodos não estáticos sugere `R0 = this`, mas a hipótese de classe/layout exige evidências em chamadores e construtores. O auditor recupera os bytes originais, rejeita mudanças em tamanho ou padrão `ALU → LDR/STR/LDRB/STRB → BX LR`, e emite para cada entrada: aliases, SHA dos 12 bytes, campos `R0 + offset`, largura, direção de acesso, registadores e mecanismo de retorno.

No diferencial, os objetos sintéticos têm quatro posições base diferentes, seis conjuntos iniciais de registos, duas condições de flags e dois endereços de retorno controlados: **96 casos por entrada, 672 casos** se as sete aprovarem. O modelo independente C11 e a execução Unicorn comparam registradores R0–R12, SP, LR, PC, CPSR, faixa de leitura/escrita, todos os bytes de memória e canários. `R0` não pode mudar e o último opcode deve transferir o controle a `LR`. Nenhuma prova autoriza extrapolação automática para todos os estados iniciais, usos concorrentes ou validade real dos ponteiros/objetos.

**Gates ainda ausentes:** campo C++ nomeado e layout completo do objeto, estado inicial válido no jogo, semântica de outros chamadores, possíveis aliases fora do inventário, condições de alias, entrada Thumb e cobertura dos estados de execução. O relatório mantém `field_name_and_class_layout_verified=false`, `caller_reachability_proven=false`, `universally_proven=false` e certificados novos zero.

## POP {...,PC} dos nove grupos ARM

`b01_pop_pc_differential.py` extrai os endereços únicos correspondentes às **28 ocorrências de retorno por pilha pendentes** na recursão dos nove grupos. O validador filtra exclusivamente encoding `LDMIA SP!, {...,PC}` A32 incondicional, sem carregar SP, sem flags, dados arbitrários ou writeback alternativo; os demais permanecem não modelados. Para cada instrução elegível, compara execução isolada no ELF original com modelo C11 `b01_pop_pc.c` sobre frames sintéticos seguros, R0–R15, novo SP, PC de retorno, CPSR e integridade do buffer de pilha. O destino não é executado. O modelo rejeita máscaras incorretas e stack insuficiente.

É **prova de microsemântica de retorno sob estados controlados**, não prova de tamanho real do stack frame, convenção de chamada da função ou identidade do destino. Não se declara resolução global de indireções a partir de uma leitura de PC sintética.

## Reproduzir sem emulador Android

```bash
python3 -m pip install capstone==5.0.6 pyelftools==0.32 unicorn==2.1.3
python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools -p test_b01_cpp_abi_pop_pc.py -v
python3 FFT_Android_Mod/docs/re-tools/b01_seven_cpp_contracts.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --output /tmp/b01-seven-cpp-contracts.json
python3 FFT_Android_Mod/docs/re-tools/b01_pop_pc_differential.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --output /tmp/b01-pop-pc-contracts.json
```

Workflow barato `.github/workflows/re-b01-cpp-abi-stack.yml`, sem LFS, APK, OBB ou emulador. Apenas JSONs de prova são publicados.

## Próximos gates

1. Correlacionar os sete `this` e offsets com atribuições reais de layout e acesso dos chamadores, por CFG recursivo com blocos já comprovados; validar condições legítimas antes de certificar.
2. Reconstituir os prólogos que empilham os registradores correspondentes aos `POP PC` e demonstrar salvamento/restauração por caminho, incluindo valores de LR e SP.
3. Investigar os seis destinos fora do grupo e os quatro callees com efeitos desconhecidos, com testes independentes, antes de fechar a #478 ou #489.
4. A04 ainda depende de trace autorizado `StorageUtil → JNI → R1`; B01 depende do OBB materializado da #482 para liberar A03/R01/R02.

Nenhuma prova aqui promove uma atividade a `done` nem emite novo certificado de equivalência de função inteira.
