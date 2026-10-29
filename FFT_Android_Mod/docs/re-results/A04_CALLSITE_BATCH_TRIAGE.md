# A04 — Triagem paralela dos 48 chamadores diretos A32

Este ciclo reduz trabalho repetitivo: classifica em um job o conjunto de BL direto para 0x000b6620, enquanto outro job inspeciona as chamadas CEGL2_SHADER::Load. Cada lane usa ELF original com SHA-256 fixo.

## Hipóteses e limites

- Auditoria anterior: 48 BL diretos candidatos, 34 classificados pelo padrão estrito MOV-only; 14 ainda fora do padrão.
- Entre os 14, doze mostram preparação de 0x10c bytes seguida de BL ao veneer de operator new, mas usam LDR/STR/MOV condicionais; dois são chamadas ao método shader que precisam de investigação separada.
- Parser ampliado registra variantes, sem aceitar clobber explícito de R0 nem novas BL antes do alvo. O grupo é de candidatos a alocação, não prova de heap real.
- Não se comprovam alcançabilidade CFG, comprimentos e NUL de R1, aliasing, exceções de new ou capacidade efetiva da memória.
- No shader há um caso com ponteiro transportado em registrador e outro com endereço baseado em SP. SP+0x120 não prova sozinho os limites válidos da pilha.

## Critério de saída

O CI deve registrar contagens e exceções em JSON por lane, com reprodução byte a byte. Revisar separadamente evidências de buffers reais e eventual execução Android.

**A04 permanece in_progress.** Nenhum certificado formal e nenhum claim de libc/JNI real.
