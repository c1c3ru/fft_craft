# Primeiro piloto de contratos locais completos — BX LR

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

- Entradas de 4 bytes ARM verificadas: **473**
- Folhas BX LR disponíveis: **303**
- Contratos locais verificados neste piloto: **5**
- Testes diferenciais ARM/Thumb deste piloto: **40**

**Status:** pronto para revisão; **0 novas certificações integrais**. As pós-condições cobrem o corpo de uma instrução no contexto ARM normal. A equivalência global, os casos de exceção e a aprovação de revisor permanecem pendentes.

| Endereço | Símbolo | Corpo completo | ARM / Thumb |
|---|---|---|---|
| `000a6d5c` | CGX_SCREEN_CORRECT::~CGX_SCREEN_CORRECT() | `BX LR` | 4 + 4 testes |
| `000a7e78` | CEGL2_IF::Setup3D() | `BX LR` | 4 + 4 testes |
| `000a8560` | CEGL2_IF::DrawGrid() | `BX LR` | 4 + 4 testes |
| `000a8564` | CEGL2_IF::DrawAxis() | `BX LR` | 4 + 4 testes |
| `000a8568` | CEGL2_IF::DrawCross(math::VECTOR3<float>, float) | `BX LR` | 4 + 4 testes |

Arquivos individuais JSON no artifact do workflow. Eles não são inseridos automaticamente em `semantic-certificates.json`.
