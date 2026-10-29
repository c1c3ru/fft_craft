# A04 — contrato parcial do callee 0x000b6620 (R1 = 0)

**Origem:** ELF ARM SHA-256 `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`, desmontagem auditada em [run 40867844255](https://github.com/c1c3ru/fft_craft/actions/runs/40867844255).

Caminho delimitado: `CMP R1,#0`, `PUSH {R4,LR}`, `MOV R4,R0`, `BEQ 0x000b6644`, `MOV R3,#0`, `STR R3,[R4,#0x104]`, `MOV R0,R4`, `POP {R4,PC}`. A chamada `BL 0x000714a0` da alternativa R1 != 0 **não será executada**.

O diferencial em `semantic_a04_b6620_zero_differential.py` emula o ELF original com dados sintéticos e compara o modelo C `c-models/a04_b6620_zero.c`, que zera os quatro bytes do campo a partir do offset `0x104` e valida limites. Pretende verificar a palavra escrita, PUSH/POP, PC, R0/R1/R3/R4, SP/LR, NZCV, sentinelas no restante da memória e nenhum efeito externo, em 4 palavras iniciais × 3 R4 × 4 flags = 48 cenários.

**Estado:** contrato candidato; a existência de código/PR não implica resultado do CI. É somente o ramo R1=0, não a função inteira. Nenhum certificado novo deve ser gerado e a A04 permanece `in_progress`.
