# A04 — experimento de origem de R1 em 0x0020ca48

O callsite original 0x0020ca48 é uma oportunidade de validar uma string produzida localmente em vez de continuar apenas o rastreio de argumentos ABI.

Instruções preliminares do ELF original indicam: R2=0xC, chamada a um veneer 0x000714b8, seguida por uma alocação de 0x10c via _Znwj e passagem de FP para R1 no callsite 0x0020ca48.

A auditoria `semantic_a04_r1_literal_probe.py` identifica o símbolo importado pelo veneer, guarda as instruções originais que prepararam o endereço-fonte e confirma os opcodes de comprimento e chamada. O código não assume antecipadamente que a cópia seja memcpy nem que os 12 bytes contenham um terminador NUL.

### Critério de prova real

1. Recuperar o endereço da origem de 12 bytes e os bytes exatos no segmento do ELF, com cálculo ARM de PC+8 e eventuais literais relativos.
2. Verificar a posição do primeiro NUL e a validade da região de destino após a cópia no stack frame, em cada caminho alcançável.
3. Executar o trecho em Unicorn com a importação isolada e fonte real imutável, comparando o conteúdo final da string antes da chamada a 0x000b6620.
4. Somente após essas três etapas considerar um testemunho delimitado de NUL e comprimento. A atribuição de comprimento não pode ser propagada para os outros 47 chamadores.

**Estado:** investigação original de produtor, sem prova NUL nem certificado, A04 in_progress.
