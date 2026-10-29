# A04 — Fonte original de R1 em 0x0020ca48: sufixo fftpack.bin

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Evidências executadas

O [GitHub Actions #40911561303](https://github.com/c1c3ru/fft_craft/actions/runs/40911561303) passou no ELF original. A rotina analisada executa, no caminho linear observado:

1. `0x0020ca0c`: chamada a `0x002b04f0`, cujo retorno é origem da chamada `strcpy` em `0x0020ca18`.
2. `0x0020ca20`: `strlen` sobre a string copiada para o buffer local em FP.
3. `0x0020ca28`: `R2 = 12`; `0x0020ca34`: `memcpy` importada via `R_ARM_JUMP_SLOT` no slot `0x00347d78`.
4. `0x0020ca38–0x0020ca48`: aloca 268 bytes e envia FP como R1 para `0x000b6620`.

### Literal real e provas delimitadas

O original lê a palavra de deslocamento em `0x0020cba8` (`0x000d1288`) e a soma relativa ao PC em `0x0020ca30` produz o endereço `0x002ddcc0`.

Nesse endereço os 12 bytes originais são:

```text
66 66 74 70 61 63 6b 2e 62 69 6e 00
 f  f  t  p  a  c  k  .  b  i  n  NUL
```

Isto comprova um **sufixo literal de 11 caracteres mais NUL**, não comprova que o prefixo recebido de `0x002b04f0` tem tamanho limitado. A prova funcional executou em Unicorn as instruções ARM originais de `0x0020ca24` a `0x0020ca30` em **36 estados**, preservando R3/FP/NZCV, confirmando os argumentos de memcpy (R0, R1, R2), a única leitura do literal e ausência de escritas. O teste parou antes do BL de `memcpy` e **não executou `strcpy` real**.

### Restrição geométrica do prefixo

O prólogo reserva `0x11c` bytes, FP é `SP + 0x10` e o campo de guarda salvo aparece em `SP + 0x114`. Entre FP e o guarda há **0x104 = 260 bytes**. Copiar 12 bytes a partir de `FP + strlen(prefixo)` sem chegar ao guarda exige:

`strlen(prefixo) <= 260 - 12 = 248`.

Se a condição for satisfeita, o sufixo literal terminaria com NUL dentro dessa região e o conteúdo final teria no máximo 259 bytes mais NUL, compatível com a região anterior ao metadado de `0x000b6620`. A análise **não demonstrou** que o comprimento do prefixo é realmente ≤248, nem o sucesso do processamento; não se afirma segurança para as demais 47 chamadas.

## Próxima fronteira concreta

Analisar o corpo e o contrato de retorno de `0x002b04f0` e seus produtores, em especial a origem e o comprimento máximo da string retornada. Confirmar limites em caminhos CFG alcançáveis e, quando possível, em ambiente Android instrumentado. O teste diferencial do chamador com buffers sintéticos não substitui essa prova.

**A04 in_progress. Nenhum certificado novo.**
