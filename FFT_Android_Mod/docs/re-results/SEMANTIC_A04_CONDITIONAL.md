# A04 — retorno condicional ARM após entrada A02

ELF original SHA256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

**Entrada original:** `0x00072910` contém `MOV R0,R2; B 0x002b1bb0`. O destino A04 começa com `SUBS R2,R0,#0; BXNE LR` (bytes originais `002050e21eff2f11`).

## Contrato independente delimitado

O teste `semantic_a04_conditional_exec.py` compara o Unicorn com um modelo Python que verifica `R0 = R2_inicial`, `R2 = R0`, e `NZCV = {N=bit31(R0), Z=(R0==0), C=1, V=0}`.

- Para R0 diferente de zero: `BXNE LR` retorna ao LR controlado. Três valores: `1`, `0x80000000` e `0xffffffff`.
- Para R0 igual a zero: `BXNE` não retorna; o emulador interrompe a execução **antes** da instrução de fallthrough em `0x002b1bb8`. O restante dessa função não foi reconstruído.

O teste cobre 4 valores × 8 seeds × 4 estados iniciais de NZCV = **128 execuções locais esperadas**. Verifica trace completo de PC, registradores, SP/LR, NZCV, ausência de efeitos de memória e checkpoint idempotente. Não executa `0x002b1bb8`, não demonstra comportamento de caller real Android e não gera certificados.

**Estado do CI:** gate pendente de confirmação; resultados não devem ser promovidos até o workflow original ELF passar.

## Pendências após esta rodada

Continuam não reconstituídos os destinos com prólogos/chamadas `0x000ab674` → `BL 0x000b6620` e `0x000b461c` → `BL 0x000b45d0`, o caminho de fallthrough condicional `0x002b1bb8`, os destinos reais dos dois GOT veneers e a alcançabilidade/terminação do autoloop `0x002a1268`. A04 permanece em andamento, e os testes locais não provam equivalência integral do aplicativo.
