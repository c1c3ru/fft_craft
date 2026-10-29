# A04 — primeiro contrato C independente, alvo 0x000b45d0

Origem: desassemblagem A32 do ELF com SHA-256 `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`; investigação estrutural [run #40867844255](https://github.com/c1c3ru/fft_craft/actions/runs/40867844255).

## Contrato candidato do caminho completo da folha

R0 contém um endereço-base válido, R1 contém um índice de entrada de doze bytes. Lê exatamente uma palavra little-endian em `R0 + 0x14c + R1*12`. Se a palavra for `0xffffffff`, retorna zero, senão retorna o endereço da palavra. R1 passa a conter `R1*12`, R3 passa a conter a palavra lida; CMN atualiza NZCV, R2/SP/LR ficam preservados. O modelo C devolve o *offset* para que o Python compare com o endereço ARM emulado sem converter endereços do processo ARM em ponteiros da máquina hospedeira.

O ensaio delimita índices `0,1,2,7,29,50`, seis valores de memória e quatro flags iniciais = **144 testes planejados**, com um único read de 4 bytes, zero writes, rastreamento de todos os PCs e comparação de registradores e NZCV. As entradas foram restringidas à memória alinhada e mapeada; entradas fora de limites são rejeitadas pelo C e não executadas no ARM. O teste termina em `BX LR`, cujo destino é uma sentinela. Não há validação do chamador nem de todos os estados possíveis.

## Critérios de aceite

O workflow `re-a04-leaf-differential.yml` deve passar no SHA final. Divergência entre ELF original e C falha o job. O resultado não gera certificado formal, não altera métricas globais e **não conclui A04**.

Depois de aprovar o diferencial, estudar o caminho R1=0 de `0x000b6620`, que evita o BL externo `0x000714a0`, e só então modelar seu outro caminho.
