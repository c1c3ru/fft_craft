# A04 — reconstrução semântica de caminho e normalização de strings

ELF ARM original SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Cadeia de chamadas e contratos

1. `0x000b6620`: com R1 diferente de zero, chama a importação `strcpy` (BL `0x000714a0`, slot `0x00347d70`, `R_ARM_JUMP_SLOT`). A chamada segue o ABI C, copiando uma string de R1 para o buffer apontado por R0. **Ainda não há prova dos tamanhos reais dos buffers ou dos valores runtime do aplicativo**.
2. `0x000b6634–0x000b6640`: prepara `R0=0x2f` ('/'), `R1=0x5c` ('\\') e `R2=R4`, chama `0x000b942c`.
3. `0x000b942c`: preserva R4–R8/LR, usa R2 como ponteiro para string, chama `strlen` (BL `0x00071494`; relocação exata do slot `0x00347d6c`), armazena o comprimento em R6 e itera se for positivo.
4. `0x000b9450` lê um byte, chama `0x000b8be4` e, se esse byte for um *lead byte* Shift-JIS, avança o índice por dois. Senão compara o próximo byte a R7 e pode escrever R8 sobre ele. **Este laço ainda não foi validado integralmente por execução diferencial**.
5. `0x000b8be4`: função-folha de 9 instruções A32; classificação de Shift-JIS. Retorna 1 se o byte baixo estiver em `0x81..0x9f` ou `0xe0..0xfc`, senão 0. A função atualiza R3 e NZCV. A hipótese é demonstrável sem depender de libc/Android, usando Unicorn sobre bytes do ELF original × modelo C independente.
6. `0x000b6644–0x000b6650`: zera o campo de offset `+0x104`, preserva/recupera a pilha e retorna ao chamador. Já existe teste isolado do ramo R1=0, mas isso **não prova** o ramo R1!=0.

## Teste diferencial da função-folha Shift-JIS

- Código independente: `docs/re-tools/c-models/a04_sjis_lead.c`.
- Oráculo e emulador original: `docs/re-tools/semantic_a04_sjis_differential.py`.
- Matriz pretendida: 256 bytes × 4 estados de NZCV = 1024, mais 16 estados com bits altos na entrada, total **1040**.
- Verificar R0, R3, NZCV, R1/R2/R4/IP/SP/LR preservados, retorno via BX LR e nenhuma leitura/escrita de memória.
- O teste falha em opcode modificado, modelo C divergente ou efeito não previsto. Sem certificados automáticos.

## Pendências para fechar o caminho

- Executar diferencial do classificador no CI, conferir SHA e logs.
- Reconstruir o laço `0x000b942c` ponta a ponta sobre buffers sintéticos válidos, com limites demonstrados, incluindo Shift-JIS de dois bytes e barras invertidas.
- Modelar os efeitos da cópia com destinação limitada e fonte terminada em NUL; não executar `strcpy` real contra buffers não verificados.
- Integrar R1!=0 desde `0x000b6620` e testar equivalência de registradores, memória e efeitos nas duas chamadas de biblioteca, sem afirmar equivalência geral de libc.

**Status:** A04 em andamento. As relações de importação `strcpy` e `strlen` são estruturais e verificadas por relocations reais; endereços de implementação Android permanecem dependentes de runtime. Nenhuma rotina integral é certificada por esta documentação.


## Prova incremental do laço ARM original (Unicorn × C)

O workflow [run #40892165075](https://github.com/c1c3ru/fft_craft/actions/runs/40892165075) concluiu **success** com o ELF de SHA fixo, **25 testes unitários e dois diferenciais originais**:

| Entrada ARM | Método | Casos | Divergências |
|---|---|---:|---:|
| `0x000b8be4` | Função-folha inteira ARM × C (`a04_sjis_lead.c`) | 1040 | 0 |
| `0x000b942c` | Laço ARM original + classificador ARM original; `strlen` sintético e controlado × modelo C `a04_sjis_slash_loop.c` | 556 | 0 |

O teste `semantic_a04_sjis_loop_differential.py` verificou a memória da string inteira, escrita condicional de barras, seis escritas de salvamento da pilha, restauração de R4–R8/SP, R0–R3, NZCV e retorno via PC. A evidência também exigiu corrigir uma suposição de teste: **LR é volátil após BL**, não é restaurado simplesmente porque a rotina faz `POP {...,PC}`. Os dois endereços de retorno observados pelo teste são `0x000b9444` após `strlen` e `0x000b9458` após o classificador.

**Escopo limitado:** o stub sintético de `strlen` não implementa ou executa a biblioteca Android; o fluxo completo de `strcpy` e o chamador `0x000b6620` para R1!=0 ainda não foram executados em conjunto. Nenhum novo certificado semântico formal foi emitido; A04 permanece em andamento.


## A04 — diferencial integrado do chamador R1 != 0

O [GitHub Actions run #40898972993](https://github.com/c1c3ru/fft_craft/actions/runs/40898972993) confirmou **1.128 execuções diferenciais ARM × C sem falhas** do caminho de `0x000b6620` com origem não nula. O programa de evidência é `docs/re-tools/semantic_a04_nonzero_full_differential.py`; o modelo C independente é `docs/re-tools/c-models/a04_nonzero_full.c`.

### Cobertura *demonstrada*, sem extrapolação

- **Original ARM efetivamente executado:** `0x000b6620` até o retorno, ambos os veneers PLT, `0x000b942c` e `0x000b8be4`.
- **Importações substituídas, não executadas da libc:** `strcpy` e `strlen`, com stubs sintéticos de retorno ABI e contratos controlados. Ambos os símbolos foram previamente identificados por `R_ARM_JUMP_SLOT` no ELF original.
- **Estado comparado:** string resultante inteira e NUL, origem imutável, palavra de metadados `+0x104`, escritas ARM observadas na pilha e na string, conteúdo integral da pilha, R0/R1/R2/R3, registradores preservados R4–R8, SP, LR volátil, IP após GOT e NZCV.
- **Estados de entrada:** strings NUL-terminadas de até 259 bytes de dados, com buffers separados de 4096 bytes, quatro combinações de flags e metadados por string. Foram exercitados valores de byte de 1 a 255 e exemplos multibyte e de separadores.
- **Limites não demonstrados:** libc Android real, aliasing/sobreposição entre buffers, origem sem NUL, destino sem espaço, estados fora do domínio sintético e integrações JNI/jogo. Entradas longas são rejeitadas pelo modelo C, não executadas no ARM.
- **Contagem de certificados formais novos:** zero. Não se altera a avaliação de cobertura global apenas por executar esse domínio delimitado.

O conjunto de provas da A04 agora contém a função-folha Shift-JIS (**1.040 casos**), seu laço (**556**) e o caminho completo do chamador não nulo com stubs (**1.128**). São testes de escopos relacionados e **não** significam 2.724 funções ou instruções distintas certificadas.

### Próximo gate da engenharia de loop

1. Aprovar os checks restantes no SHA final do PR e manter a rastreabilidade.
2. Consolidar os contratos R1=0 e R1!=0 numa única interface C de alto nível, preservando os diferentes efeitos ABI.
3. Verificar tamanhos e condições de origem/destino no uso real do aplicativo Android. Não usar a hipótese de buffer grande sem prova no chamador.
4. Exercitar cenários de fronteira próximos de `0x104` apenas com memória suficiente e verificar separadamente limites da rotina de cópia.
5. Conservar `A04` como `in_progress` até fechar integração e pré-condições reais.

### Gate de fronteira adicional (+0x104)

No [run #40898972993](https://github.com/c1c3ru/fft_craft/actions/runs/40898972993), o teste chegou a **259 bytes de dados + NUL** (NUL no offset 0x103), preservando o campo 0x104–0x107 para a escrita final da rotina original. Inclui também sequências com separadores e bytes Shift-JIS próximos ao limite; 1.128 casos integram o caminho R1!=0, com zero divergências. O código C rejeita comprimentos que alcançariam o campo 0x104, sem executar essas entradas inválidas no ARM original.
