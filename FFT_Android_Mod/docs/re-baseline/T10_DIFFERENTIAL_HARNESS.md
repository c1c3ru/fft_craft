# T10 — Construir harness diferencial reutilizável

Depende de T03, T08–T09 (`ready_for_review`, parciais). Executado em 2026-10-31.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** Produz o primeiro harness Unicorn **genérico** do projeto (`docs/re-tools/differential_harness.py`): até aqui, todo uso de Unicorn no repositório (`semantic_microexec.py`, `b01_bounded_caller_execution.py`, `b01_cond_pop_pc_differential.py`, etc.) é um script dedicado a um padrão de instrução ou função específica, com seu próprio mapeamento de registradores/memória reescrito a cada caso. O novo módulo separa "executar o `.so` original" de "comparar com uma referência", reutilizável por qualquer tarefa futura (T14+) sem repetir o boilerplate de Unicorn.

## 1. O que o harness faz

`run_original(so_path, start, end, initial_regs, buffers, stub_calls=None, max_instructions=20000)`:

- Mapeia no Unicorn todas as seções `ALLOC` do ELF que se sobrepõem ao intervalo pedido (não só a função alvo), nos endereços reais, com os bytes reais — referências internas na mesma página continuam resolvendo.
- Aceita `buffers` (memória nomeada, ex. um `BWORK`/`EDATA` sintético) em endereços de escopo separados do binário.
- Detecta modo Thumb pelo bit de interworking do endereço de entrada (mesmo padrão corrigido em T07), mas **não valida troca de modo ARM↔Thumb no meio da execução** — limitação registrada, não testada.
- Executa instrução a instrução. Qualquer desvio de controle pra fora de `[start, end)` que não seja o retorno esperado **só é tolerado se o endereço estiver em `stub_calls`** (dicionário endereço→valor de retorno); todo stub usado fica registrado em `stubbed_calls` no resultado — nenhuma chamada externa é "pulada" silenciosamente sem aparecer na evidência.
- Acesso a memória não mapeada, estouro do limite de instruções, ou erro do Unicorn **sempre** resultam em `ok=False` — não existe caminho de código que transforme uma falha de emulação em aprovação.
- Retorna `final_buffers`: o conteúdo de cada buffer nomeado **depois** da execução (não só o log de escritas) — é isso que `compare()` usa para decidir se bateu, porque duas implementações podem legitimamente escrever os mesmos bytes em instruções diferentes (ex. 3 merges de bit separados vs. 1 só) e ainda serem equivalentes; o log de escritas (`memory_writes`) continua disponível para depuração, só não decide o resultado.

`compare(original, reference, tracked_registers=["r0"])` compara registradores escolhidos e todo buffer nomeado por conteúdo final; qualquer falha de execução de qualquer lado é mismatch automático e incondicional.

## 2. Validação de ponta a ponta contra uma função real (não um brinquedo)

Usei `copy_entry_coord(BWORK*, EDATA*)` (`0x1d9ee0`, lida por completo em T08, `NOTES §658`) como caso de validação — é a menor função real com pseudocódigo já confirmado nesta sessão, então o teste confere o harness contra evidência prévia independente, não contra si mesmo.

`docs/re-tools/test_differential_harness.py` (6 testes, todos passando):

- 3 casos positivos (entrada zerada, entrada representativa não-trivial, todos os bits de `EDATA+0x1b` setados) comparando a execução real via Unicorn contra uma porta Python do pseudocódigo citado — **os três batem exatamente**, confirmando de forma independente que a leitura manual de T08 está correta.
- 2 casos de **injeção de falha deliberada**, exigidos pelo critério de aceite: um byte do buffer de referência é corrompido de propósito → `compare()` detecta e marca `match: False` no campo exato (`buffer:BWORK`); uma execução "quebrada" simulada (`ok=False`) → `compare()` marca mismatch incondicional, nunca passa.
- 1 caso de chamada externa não autorizada: força um intervalo `[start, start+8)` deliberadamente menor que a função real, sem nenhum stub — confirma que o harness aborta com erro explícito (`"no stub"`), em vez de continuar silenciosamente.

Suíte completa de `docs/re-tools`: **540 testes / 1.812 subtestes, todos passando** (534 antes + 6 novos).

## 3. Modelagem de relógio/RNG/arquivos/entradas (exigida pelo critério de aceite)

`copy_entry_coord` não lê relógio, RNG, nem arquivo — não há necessidade de modelá-los para este caso de validação. O harness em si **não** fornece ainda um modelo de relógio/RNG/arquivo controlado para funções que os usem; isso fica como limitação explícita (seção 5), não resolvida por este módulo. Toda a entrada usada nos testes é controlada e determinística (bytes fixos por teste, sem aleatoriedade oculta).

## 4. Por que isso evita um "oráculo que copia a implementação testada"

A referência em `test_differential_harness.py` é uma porta direta do **pseudocódigo já publicado em `REVERSE_ENGINEERING_NOTES.md` §658** (produzido em T08 por leitura independente do binário), não derivada do comportamento observado do Unicorn nesta tarefa — ou seja, as duas pontas vêm de análises feitas em momentos/métodos diferentes (leitura manual de disassembly vs. execução real), reduzindo o risco de um oráculo circular.

## 5. O que fica pendente (bloqueia `done`)

1. Modelo de relógio/RNG/arquivo/entrada controlada para funções que dependam deles — não implementado.
2. Troca de modo ARM↔Thumb dentro de uma mesma execução (`blx` pra um alvo de modo diferente) não testada nem garantida — o harness fixa um modo por chamada de `run_original`.
3. Só uma função foi usada para validação ponta a ponta (`copy_entry_coord`); nenhuma função maior, com chamadas externas reais stubadas, ou com os 3 tipos de buffer ao mesmo tempo (device memory-mapped, por exemplo) foi testada ainda.
4. `run_original` não aceita ainda uma "implementação de referência" compilada em C via `ctypes` (o padrão já usado em `b01_cond_pop_pc_differential.py`) — só comparação contra um `ExecutionResult` construído manualmente, como fiz no teste. Generalizar isso é trabalho futuro natural, não feito aqui.

## 6. Arquivos produzidos por esta tarefa

- `docs/re-tools/differential_harness.py` — harness reutilizável.
- `docs/re-tools/test_differential_harness.py` — validação ponta a ponta + 2 injeções de falha.
- Este relatório.
