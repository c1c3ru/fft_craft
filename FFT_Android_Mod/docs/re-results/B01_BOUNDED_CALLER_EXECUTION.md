# B01 — primeiras chamadas ARM originais com retorno delimitado e diferencial C++

**Estado:** validação dinâmica em estados sintéticos controlados. Esta etapa
não confirma a alcançabilidade dentro do processo Android nem certifica uma
função completa. B01 permanece `in_progress`.

## Escopo estrito

Dois candidatos a BL previamente recuperados do ELF original são curtos
o suficiente para avançar da varredura A32 para execução em Unicorn:

| Entrada do chamador | BL original | Destino de 12 bytes | Modelo C++ |
|---|---|---|---|
| `0x000b9f88` | `0x000b9f90` | `0x000b9f7c` | `CTHREAD::RequestExit()` |
| `0x000be1e8` | `0x000be1f0` | `0x000be1dc` | `CSTEP_BATCH::Uninit()` |

`b01_bounded_caller_execution.py` confere o SHA-256 fixado do ELF,
os limites e os bytes exatos do BL, e o corpo original de 12 bytes
`MOV → STR → BX LR`. Sem decodificação e destino corretos, falha
antes de executar qualquer instrução.

A emulação ARM usa registradores, pilha, memória de objeto e condições
iniciais sintéticas e determinísticas. Observa o prefixo do chamador até
o BL; então executa BL, todo o corpo do callee e BX LR até o retorno
ao chamador. Para antes de executar a instrução seguinte.

O campo R0 é obtido *do contexto emulado do chamador no ponto do BL*.
A execução independente de `c-models/b01_named_cpp_methods.cpp`,
compilada com limites de acesso à memória, escreve em um clone do
buffer observado no ponto de chamada. O verificador compara todo o
buffer de objeto, todas as escritas do callee, pilha, R0, SP, LR,
CPSR relevante e PC de retorno. O próximo passo é verificar trajetórias
de retorno do chamador, estados alternativos e objetos reais.

## Critérios de sucesso e limites

- Comprovar *somente* que o prefixo do chamador e o BL originais
  são executáveis **nas condições sintéticas descritas**;
- Comprovar a equivalência local da escrita produzida pelo callee com
  o modelo C++ independente para esse estado controlado;
- Não chamar isso de chamada observada no jogo, provar layout
  completo, encerrar a função do chamador ou certificar o aplicativo;
- Não tentar executar outros callees, jumps indiretos ou libc
  com efeitos ainda desconhecidos.

## Execução e prova versionada

```bash
python3 FFT_Android_Mod/docs/re-tools/b01_bounded_caller_execution.py \
  --output /tmp/b01-bounded-caller-returns.json

python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools \
  -p 'test_b01_bounded_caller_execution.py' -v
```

O workflow `re-b01-named-cpp-prologues.yml` produzirá o relatório
JSON somente se o teste completar e o gate do ELF original passar.
O arquivo fica em artifact temporário do CI, vinculado ao SHA e
ao run específico. Nenhum `semantic-certificates.json` será alterado.

## Etapa seguinte: de caller local a contrato completo

1. Continuar o fluxo dos dois destructors através dos retornos
   dos respectivos chamadores, modelando `PUSH/POP PC` e SP real;
2. Repetir com estados de objeto e caminhos alternativos auditáveis;
3. Validar criação, tamanho, alias e propriedade dos campos de
   cada objeto `this`, inclusive em ambiente Android;
4. Estender o diferencial para os outros candidatos, começando pelo
   construtor `CINPUT_IF_TOUCH`;
5. Apenas após contrato integral e revisão independente, propor
   um proof class específico à certificação semântica.
