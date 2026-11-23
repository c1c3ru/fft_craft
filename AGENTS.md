# Instruções para agentes — fft_craft

Estas instruções se aplicam a agentes de programação no repositório inteiro. Respeite instruções mais específicas em diretórios e as decisões explícitas do usuário. O objetivo é avançar na reconstrução com evidências verificáveis, sem confundir progresso estrutural com equivalência semântica.

## Protocolo Reflexion (feedback verificável)

Para cada tarefa ou hipótese:

1. **Delimite o alvo.** Registre issue, função/endereço, artefatos relevantes, critério de aceitação e estado inicial. Não infira sucesso a partir de contagens de instruções ou testes sintéticos.
2. **Consulte evidências existentes.** Verifique código, documentação, checkpoints e logs relevantes antes de executar um experimento. Não repita investigação já validada; distinga resultados confirmados de hipóteses.
3. **Faça a menor alteração testável.** Evite mudanças amplas e simultâneas sem necessidade. Preserve contratos, interfaces e a rastreabilidade ao ELF original.
4. **Valide em camadas.** Execute primeiro testes focados; depois testes de regressão e verificações diferenciais adequadas. Trate CI verde como evidência dos checks executados, não como prova universal de equivalência.
5. **Após falha, produza reflexão curta e acionável**, baseada no feedback real. Inclua:
   - identificador do alvo e tentativa;
   - comando/teste executado e resultado observável;
   - causa provável **como hipótese**, sem afirmá-la como fato;
   - mudança concreta para a próxima tentativa;
   - teste que pode confirmar ou refutar essa hipótese.
6. **Na próxima tentativa, mude a estratégia com motivo explícito.** Não repetir o mesmo patch, prompt ou teste sem nova evidência.
7. **Interrompa cedo ao atingir critérios objetivos.** Limite padrão: **até 3 tentativas por hipótese**; pare também diante de ausência de progresso, falta de ferramenta/artefato ou custo desproporcional. Em bloqueio, descreva evidências e próximo passo em vez de declarar sucesso.
8. **Consolide aprendizados**, sem registrar dados sigilosos. Preserve caminho da evidência/commit/check e status: `confirmado`, `refutado` ou `pendente`. Não promova reflexão não verificada a conhecimento comprovado.

## Engenharia reversa e critérios de evidência

- Diferencie explicitamente **cobertura estrutural**, **contratos semânticos**, **execuções diferenciais** e **implementação equivalente**.
- Para ARM/Thumb, JNI e C/C++, confirme quando aplicável parâmetros, fluxo de controle, layout dos objetos, chamadas externas, acessos/efeitos de memória, flags e retornos.
- Não invente destinos de saltos indiretos, valores de registradores, tamanhos de buffers, terminação NUL ou condições de retorno. Marque lacunas e planeje experimentos para resolvê-las.
- Não substitua evidência real de execução por mocks. Mocks podem testar o harness, mas sua cobertura deve ser apresentada separadamente.
- Não altere baselines, reduza checks, ignore falhas ou marque tarefas como completas apenas para obter CI verde.
- Em qualquer conclusão, informe: **o que foi alterado**, **quais comandos/checks passaram**, **o que não foi executado**, **quais riscos restam** e **qual evidência permite a afirmação**.

## Economia de tokens e execuções

- Recupere **somente aprendizados relevantes** ao alvo atual; prefira até 5 notas curtas a despejar logs extensos no contexto.
- Agregue erros idênticos por causa raiz com rastreabilidade às ocorrências; não perca casos distintos.
- Antes de rodar CI pesado, confirme se mudanças relevantes exigem o job. Prefira teste local/focado e use emuladores ou grandes matrizes quando necessários para o contrato avaliado.
- Em tarefas paralelas, cada agente deve trabalhar em alvos independentes. Não sobrescrever alterações ou checkpoints de outro agente; coordenar integração por commits/PRs e revalidar após merge.
- Aumente cobertura sem sacrificar rigor, segurança, reprodutibilidade ou fidelidade ao comportamento original.

## Formato breve de reflexão

```text
Alvo: <issue/função/endereço>
Tentativa: <n/3>
Evidência: <teste, execução ou log e resultado>
Hipótese da falha: <explicação ainda não comprovada>
Mudança proposta: <ação mínima e específica>
Validação seguinte: <teste com critério de aprovação>
Status: pendente | confirmado | refutado
```

## Política de entrega

Não faça push direto para `main` quando houver fluxo de revisão por PR. Não declare que um commit, push, merge, teste ou benchmark foi realizado sem confirmação da ferramenta correspondente. Mantenha mudanças reversíveis e documente limitações. O protocolo de reflexão orienta decisões, mas **somente a evidência objetiva valida a entrega**.
