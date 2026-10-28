# A04 — loop de integridade das fronteiras pendentes (28/10/2026)

**Escopo**: apenas proteger a rastreabilidade dos blocos A04 ainda desconhecidos.
Não constitui execução dinâmica, reconstrução de callee ou certificado semântico.

## Evidência observada no repositório

- Identidade esperada do ELF: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.
- `0x000ab674` alcança um `BL` direto para `0x000b6620`; corpo, efeitos globais e retorno ainda precisam de contrato.
- `0x000b461c` alcança um `BL` direto para `0x000b45d0`; o prefixo com PUSH/MOV até a fronteira foi modelado em `semantic_a04_bl_boundaries.py`. O callee permanece desconhecido.
- `0x002b1bb0` tem retorno condicional `BXNE`, mas a continuação zero `0x002b1bb8` não tem contrato de fluxo completo.
- O salto para si mesmo `0x002a1268` foi observado estaticamente, mas sua alcançabilidade real é desconhecida.

## Nova proteção automatizada

`re_a04_boundary_gate.py` valida a linha de base, a presença única de A04, status `in_progress`, sete endereços críticos e evidências/critérios de aceite. O teste de regressão falha se um destino desaparecer, se A04 for marcada prematuramente como concluída ou se o SHA de referência for alterado.

Para executar localmente:

```bash
python3 FFT_Android_Mod/docs/re-tools/re_a04_boundary_gate.py
PYTHONPATH=FFT_Android_Mod/docs/re-tools python3 -m unittest -v test_re_a04_boundary_gate
```

## Próximo ciclo experimental

1. Validar bytes, CFG e origem de código dos dois callees no ELF com hash fixado.
2. Modelar cada prólogo, leituras e escritas, incluindo dados globais e possíveis aliases.
3. Executar prefixos seguros no Unicorn, interrompendo antes de instruções com efeitos desconhecidos.
4. Criar diferencial contra oráculo independente, cenários extremos e checkpoint idempotente.
5. Só após validação das continuações e reachability, propor revisão do status de A04.

**Gate deste PR:** apenas invariantes de documentação e rastreador; nenhuma alegação de equivalência funcional, nenhuma alteração de certificado.
