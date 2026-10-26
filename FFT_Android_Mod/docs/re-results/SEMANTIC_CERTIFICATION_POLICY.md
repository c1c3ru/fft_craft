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
4. **Revisão humana independente:** aprovação real no GitHub sobre o pacote
   imutável de evidências, antes de qualquer promoção no ledger. Login, data,
   commit revisado, identidade do autor e hash do contrato são conferidos por API.
5. **Gate obrigatório:** `semantic_certificate_gate.py` precisa passar no CI;
   nenhuma rotina de coleta de evidência pode converter `partial` em
   `certified` por conta própria.

O campo `proof_class` suportado inicialmente é
`original_a32_bxlr_normal_return_v1` e o `scope` é
`normal_a32_valid_abi_return`. Outros contratos de função exigem validadores
equivalentes próprios, em vez de reutilizar o gate de `BX LR`.

## Fluxo utilizável de aprovação em duas fases

O mesmo PR não pode exigir, antes da revisão, uma identidade e uma data
de aprovação que ainda não existem. Por isso a certificação tem duas fases:

1. **Solicitação verificável:** rodar
   `python3 FFT_Android_Mod/docs/re-tools/semantic_review_protocol.py --output FFT_Android_Mod/docs/re-results/SEMANTIC_BXLR_REVIEW_REQUEST.json`.
   O script confere novamente o código **original** e os testes ARM/Thumb dos
   cinco contratos parciais e calcula um SHA-256 exclusivo por endereço e
   especificação. Produz apenas `human_review_requested`, nunca `certified`.
2. **PR independente de revisão:** abrir um PR contendo o arquivo
   `SEMANTIC_BXLR_REVIEW_REQUEST.json`, sem alterar o ledger para
   `certified`. Uma pessoa **diferente do autor** revisa as evidências,
   as hipóteses e as exclusões, e aprova o commit final desse PR pelo GitHub.
   Sem `APPROVED` real, a etapa para aqui.
3. **PR posterior de promoção:** após essa aprovação, propor a alteração dos
   respectivos registros em `semantic-certificates.json` de `partial` para
   `certified`, preenchendo `reviewer` com o login e a data **reais** da
   aprovação, a URL daquele PR e
   `review_protocol: independent_github_review_request_v1`.
4. **Revalidação final no CI:** `semantic_certificate_gate.py` recarrega o
   pedido do commit efetivamente aprovado pelo GitHub, valida o diff que
   adicionou o par endereço/fingerprint, confere que o revisor não é o autor,
   compara o hash integral do contrato com o registro proposto e reexecuta
   todos os 32 testes no ELF. Se qualquer condição falhar, a cobertura
   certificada não aumenta.

**Nunca inventar** uma aprovação, preencher dados de um revisor antecipadamente
ou criar um certificado integral apenas com base em testes amostrados. A
certificação `original_a32_bxlr_normal_return_v1` continua estritamente
limitada ao estado de execução normal expressamente especificado.

## Estado atual

As **303 candidatas** têm o corpo de uma instrução e os contratos locais
verificados pelos testes anteriores, mas **nenhuma foi promovida automaticamente**.
A revisão independente ainda precisa ocorrer. As métricas do último lote
ficam preservadas em `SEMANTIC_RUN_SNAPSHOT.json`; seu `run_id` aponta
para a execução original do CI, sem transformá-la numa certificação formal.

**Atenção:** uma aprovação humana autentica a revisão, mas não substitui a
necessidade de avaliar cuidadosamente se as precondições adotadas cobrem
o comportamento que se deseja reconstruir.
