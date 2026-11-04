# T06 — Reconstrução de CFG e contratos de wrappers Thumb (parcial)

## Estado e proveniência

O alvo é o ELF ARM original `libgl2jni.so` com SHA-256 fixado
`bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.
O histórico T06 de 31/10 apontou três aprovações estruturais antigas
com modo ARM incorreto. Os checkpoints atuais de `0x002c9115`,
`0x002c9a25` e `0x002ca125` **já estão em needs_review**; isto não
é uma descoberta nova e não se deve contabilizar como nova correção.

Em 04/11, `jtable.py` e `struct_pass.py` já são Thumb-aware, mas
`structural_v3.py` continuava A32-only. Esta mudança acrescenta
triagem por instruções variáveis de 2/4 bytes em Thumb no validador;
**não** muda automaticamente status para `auto_structural`.

## Limites dos wrappers verificados

| Entrada interworking | Corpo executado | Símbolo no inventário | Alvo de chamada |
|---|---:|---:|---|
| `0x002c9115` `operator delete(void*)` | 12 B | 12 B | `0x002ce07c` |
| `0x002c9a25` `operator new[](unsigned)` | 8 B | 20 B | `0x002c99b4` |

**Importante:** os bytes restantes `0x002c9a2c..0x002c9a37`
ficam explicitamente **não atribuídos** ao wrapper de `new[]`.
Uma instrução de retorno ocorre antes deles. A faixa de 20 bytes
no inventário não comprova que os 12 seguintes façam parte do mesmo
corpo sem reconciliação de símbolos, aliases e possíveis funções adjacentes.

## Modelo de CFG (escopo estrito)

Delete: `push {r3,lr}` → `cmp r0,#0` → `beq`
(R0 == 0 → `pop {r3,pc}`; caso contrário → `bl 0x002ce07c`
→ **assumir retorno do callee** → `pop {r3,pc}`).

New[]: `push {r3,lr}` → `bl 0x002c99b4`
→ **assumir retorno do callee** → `pop {r3,pc}`.

Os dois destinos externos são conferidos no código Thumb original
por Capstone e também pela instrumentação Unicorn (PC/LR/argumentos).
Os callees **não** são executados: o teste os substitui por dois bytes
Thumb `BX LR` em uma memória de teste controlada, com R0 de retorno
controlado para o alocador. Assim, eventuais efeitos laterais
(heap, exceções, callbacks, libstdc++ e JNI) permanecem desconhecidos.

## Contrato de estado observável

- O argumento R0 é encaminhado ao callee exatamente uma vez no caminho
  não nulo de delete, e em todos os cenários de new[].
- Delete com R0 = 0 não chama o callee e retorna diretamente.
- New[] encaminha para o chamador o R0 simulado da alocação.
- Ambos preservam R3 e restauram SP e PC ao fim do wrapper.
- `push {r3,lr}` grava dois words na pilha; nenhuma gravação é
  permitida fora da faixa de salvamento da pilha durante a emulação.
- O modelo C++ host (`t06_thumb_wrapper_model.cpp`) faz apenas a
  mesma seleção de chamada e passagem/retorno de R0 via callbacks.
- Não há declaração de equivalência completa do código do alocador.

## Execução

CI: `.github/workflows/re-t06-thumb-cfg.yml`
(PR, push relevante à main ou dispatch manual), sem downloads externos
e sem necessidade de executar Android/OBB. Compila o C++ com
`-std=c++17 -O2 -Wall -Wextra -Werror -pedantic`, testa o parser
Thumb e executa sete cenários diferenciais ELF original × C++.

O relatório JSON contém CFG delimitado, estado de registradores,
quantidade de chamadas e classe de efeito; **não** contém o binário.

## Para aceitar contratos completos mais tarde

1. Rastrear os chamadores reais (não apenas XREF linear) de cada wrapper.
2. Descobrir o comportamento do `0x002ce07c` e `0x002c99b4`,
   incluindo tratamento de erro, alocação, exceções, efeitos de memória.
3. Reconciliar os 12 bytes restantes no símbolo new[] e outras
   entradas Thumb, especialmente `__cxa_type_match`.
4. Comparar contratos C++ sem stubs contra o comportamento original,
   com testes diferenciais de memória, retorno e chamadas.
5. Só então submeter o certificado semântico completo a revisão.

**Esta fatia acrescenta 0 certificados semânticos e 0 aprovações**.
Os gates T06, T05, T12 e T39 continuam formalmente abertos.
