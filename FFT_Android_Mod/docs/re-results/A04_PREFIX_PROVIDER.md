# A04 — investigação da função original 0x002b04f0

**Objetivo:** reconstruir o produtor do prefixo utilizado pelo chamador `0x0020ca0c`, antes de `strcpy`, `strlen` e `memcpy(12)` do sufixo literal `fftpack.bin\0`. O resultado anterior exige `strlen(prefixo) <= 248` para que a cópia do sufixo não alcance o campo de guarda observado na pilha.

A nova auditoria original-ELF valida a instrução `BL 0x002b04f0`, identifica símbolos no endereço alvo, seu modo A32/Thumb, desmonta uma janela fixa, apresenta chamadas diretas, saltos, acessos candidatos à memória e literais relativos ao PC. O arquivo JSON de prova será gerado pelo workflow `re-a04-prefix-provider.yml` com replay idêntico.

**Status inicial:** não se pressupõe que o retorno seja string NUL-terminada, nem que seu comprimento máximo seja 248. Uma desmontagem linear não é prova de alcançabilidade; destinos não modelados não são executados. Se o ELF revelar um veneer, seguir a cadeia real antes de atribuir semântica.

**Aceite da próxima etapa:** identificar implementação e retorno; demonstrar se a origem é constante, buffer interno ou parâmetro, rastrear NUL e limite; comparar com comportamento executado de modo controlado, sem chamar `strcpy` original com entrada potencialmente grande. A04 permanece in_progress, 0 certificados formais novos.
