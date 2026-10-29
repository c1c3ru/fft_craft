# A04 — resultado da investigação do veneer 0x000714a0

Evidência: [GitHub Actions run #40888015455](https://github.com/c1c3ru/fft_craft/actions/runs/40888015455), ELF SHA-256 `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Instruções originais do destino

```asm
0x000714a0  ADD IP, PC, #0x200000
0x000714a4  ADD IP, IP, #0x0d6000
0x000714a8  LDR PC, [IP, #0x8c8]!
```

A32 usa PC corrente + 8 na primeira instrução: `0x714a8 + 0x200000 + 0xd6000 + 0x8c8 = 0x347d70`. A leitura transfere o controle para o ponteiro armazenado no slot `0x00347d70`, atualizando IP por writeback. O valor no slot, relocação, resolução dinâmica, destino e efeitos reais do callee permanecem **desconhecidos**.

## Gate do próximo loop

1. Inspecionar o segmento PT_LOAD que contém `0x00347d70`, seus bytes originais e entradas REL/RELA relacionadas, distinguindo conteúdo estático do endereço relocável.
2. Examinar símbolos dinâmicos e mecanismo de carregamento para determinar se o slot é importação/PLT/GOT ou indireção própria.
3. Executar apenas o veneer com valor de destino sintético sob Unicorn, verificando PC, IP e uma leitura de quatro bytes; parar antes do destino.
4. Só após resolver o ponteiro em runtime, modelar o callee real e continuar o caminho `R1 != 0` de `0x000b6620`.

**Sem execução do destino real, sem certificado novo e sem equivalência integral de A04.**
