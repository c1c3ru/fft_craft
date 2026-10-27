# Certificação semântica em lotes de 100, 200 ou 303 folhas A32 `BX LR`

O experimento de 5 e, depois, 20 endereços demonstrou o fluxo de certificação. Com **25 contratos certificados de 303 candidatas** `BX LR`, restam **278 candidatas deste tipo**. O inventário maior possui 6.329 endereços únicos; aumentar a certificação de folhas não certifica automaticamente os demais contratos com múltiplas instruções.

## Capacidade e execução

- **Próxima rodada:** 100 folhas, cada uma com **32 estados** ARM/Thumb verificados no ELF original. Após revisão independente e gate aprovado, a cobertura passa de 25 para **125/6.329 (~1,98%)**.
- **Rodadas de 200:** suportadas pelo limite de 303 entradas por solicitação e lote; selecionar somente contratos reais restantes e não exceder as 278 candidatas ainda disponíveis no início desta fase.
- **Lote total:** até 303 contratos locais do tipo `BX LR` neste binário. Não há suporte genérico equivalente para todas as 6.329 entradas; outros tipos exigem modelos semânticos e gates próprios.

O GitHub Actions executa `semantic_bxlr_contract_pilot.py --limit 303` para obter evidências individuais. Os scripts `semantic_bxlr_review_batch.py` e `semantic_review_protocol.py` aceitam até **303 por lote**, sem certificá-los automaticamente. Os workflows preparam **até 100** candidatas por execução usando `--up-to`, permitindo que as últimas rodadas contenham menos funções sem falhar. Para gerar um pedido com 200 funções parciais já registradas:

```bash
python3 FFT_Android_Mod/docs/re-tools/semantic_review_protocol.py \
  --limit 200 --output FFT_Android_Mod/docs/re-results/SEMANTIC_BXLR_REVIEW_REQUEST_R5.json
```

A escolha do próximo número `R5` é apenas ilustrativa; use um arquivo de revisão **novo** e versionado que não exista no repositório, preservando os pedidos anteriores.

## Requisitos inalterados

1. A aprovação `APPROVED` deve vir de pessoa técnica diferente da autora, no commit exato do PR que **adicionou** o pedido imutável.
2. Cada fingerprint vincula endereço, hash ELF, opcode, pré/pós-condições, memória e controle de fluxo.
3. O gate lê os bytes originais do ELF e reexecuta 32 testes por função. PRs com diffs extensos podem omitir `patch` na API: o gate valida o arquivo completo do commit aprovado, mas continua exigindo que ele tenha sido **adicionado naquele PR**.
4. Nenhuma entrada é promovida de `partial` a `certified` pela mera existência do pedido, por CI verde ou por merge sem revisão.
5. Não somar novamente as 32 execuções previamente produzidas no momento de preparar um pacote; os testes reexecutados são verificações do mesmo contrato, e não novas funções certificadas.

## Estratégia recomendada após as folhas

Concluir as 278 folhas pendentes com rodadas auditáveis de 100 a 200 e, em paralelo, começar a reconstruir funções reais com chamadas, ramificações, acesso à memória e efeitos externos. A cobertura semântica global de 100% depende dessa segunda frente, e não apenas da escala da primeira.
