# A04 — interface C consolidada e pré-condições dos chamadores reais

## Resultado já consolidado

O ELF ARM original SHA-256 bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc tem dois caminhos demonstrados por diferenciais independentes e delimitados:

- R1=0: limpa quatro bytes em R0 + 0x104; testes ARM × C do caminho isolado.
- R1!=0: chama strcpy por PLT, normaliza separadores respeitando bytes de liderança Shift-JIS (função 0xb8be4), limpa R0 + 0x104 e retorna R0; 1.128 execuções ARM × C com stubs *sintéticos*, sem executar Android libc.

O cabeçalho c-models/a04_b6620_model.h e o módulo c-models/a04_b6620_model.c reúnem os comportamentos em uma API que recebe capacidades explícitas. O retorno dessa API é um código de aceite, **não é a ABI original de retorno R0**. A API é uma referência segura de comportamento, não um patch binário intercambiável. Rejeita fonte/destino sobrepostos (checagem de endereços convertidos em uintptr_t válida somente no ambiente hospedeiro do modelo), destino menor que 0x108, fonte sem NUL dentro da capacidade informada ou cópia que possa alcançar o campo +0x104. Rejeições não são equivalência do código original para entradas inválidas.

## Investigação da proveniência de R0/R1

O analisador docs/re-tools/semantic_a04_b6620_xrefs.py examina codificações BL imediatas A32 alinhadas em PT_LOAD executável do ELF original, registra janelas de instruções próximas e associa símbolos que as contenham quando existirem. Os endereços retornados são **candidatos estáticos**, não execução demonstrada.

Critérios para considerar a capacidade do destino provada:

1. Localizar os callsites reais e confirmar que são instruções atingíveis em um CFG do chamador, não bytes de dados ou um percurso Thumb/indireto.
2. Rastrear a definição de R0 até uma alocação, objeto, parâmetro ABI, buffer estático ou campo estruturado; comprovar tamanho válido de pelo menos 0x108 bytes.
3. Rastrear a definição de R1, NUL e o comprimento máximo da origem; comprovar espaço para NUL sem invadir o campo +0x104.
4. Verificar aliasing e origem/destino, tratamento de erro e caminhos de liberação, incluindo chamadas de JNI/Android.
5. Só então testar fluxos com ponteiros reais (em VM/dispositivo autorizado) e documentar versão de libc, ABI e parâmetros.

**Ainda não há garantia de capacidade real dos buffers, equivalência da libc Android ou validação JNI demonstrada por esses artefatos.** A04 segue in_progress, e não há novo certificado formal.
