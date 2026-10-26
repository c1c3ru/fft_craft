# Política de certificação semântica integral — FFT Craft

**ELF de referência:** `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Critérios para aumentar o contador certificado

Um relatório estático, checkpoint estrutural ou execução Unicorn aprovada **não é um certificado**.
Somente entradas `certified` em `semantic-certificates.json` aprovadas pelo gate
de certificação podem aumentar a cobertura certificada em `STATUS_GERAL.md`.

O primeiro tipo de contrato integral elegível é estritamente limitado ao corpo
**de uma única instrução ARM A32** `BX LR` (`E12FFF1E`), observável sob estas
precondições explícitas:

- Início em ARM A32, ambiente normal, código executável e retorno válido.
- Destino LR ARM alinhado a quatro bytes ou destino LR Thumb alinhado a dois bytes.
- Sem falha de busca, exceção, interrupção ou mudança concorrente do código.

**Efeito especificado:** salto para o destino de LR, seleção de estado ARM/Thumb
pelo bit 0 de LR, preservação dos registradores gerais e dos demais bits do
CPSR, nenhuma leitura/escrita de dados pela instrução. Não se afirma
equivalência de todo o jogo nem de execuções fora dessas hipóteses.

Para aprovar, o registro precisa ter:

1. **Vínculo binário:** SHA-256 exato do ELF, endereço e tamanho do inventário,
   palavra ARM original e hash dos quatro bytes.
2. **Contrato completo no escopo:** pré-condições, pós-condições, controle de
   fluxo, efeitos de memória e evidências de testes diferenciais.
3. **Reexecução independente:** decodificação do código real e 32 testes Unicorn
   por endereço (todos os padrões NZCV, retornos ARM e Thumb) comparados com
   `arm_bx_reference.py`.
4. **Revisão humana independente:** aprovação real na plataforma GitHub,
   associada à alteração que adicionou aquele endereço ao ledger de
   certificados; login, data e commit revisado conferidos por API.
5. **Gate obrigatório:** `semantic_certificate_gate.py` precisa passar no CI;
   nenhuma rotina de coleta de evidência pode converter `partial` em
   `certified` por conta própria.

O campo `proof_class` suportado inicialmente é
`original_a32_bxlr_normal_return_v1` e o `scope` é
`normal_a32_valid_abi_return`. Outros contratos de função exigem validadores
equivalentes próprios, em vez de reutilizar o gate de `BX LR`.

## Estado atual

As **303 candidatas** têm o corpo de uma instrução e os contratos locais
verificados pelos testes anteriores, mas **nenhuma foi promovida automaticamente**.
A revisão independente ainda precisa ocorrer. As métricas do último lote
ficam preservadas em `SEMANTIC_RUN_SNAPSHOT.json`; seu `run_id` aponta
para a execução original do CI, sem transformá-la numa certificação formal.

**Atenção:** uma aprovação humana autentica a revisão, mas não substitui a
necessidade de avaliar cuidadosamente se as precondições adotadas cobrem
o comportamento que se deseja reconstruir.
