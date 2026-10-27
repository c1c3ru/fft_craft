# Acervo histórico de evidências semânticas — FFT Craft

ELF SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

- Relatórios históricos vinculados a este ELF: **26**
- Documentos com contagens de microexecuções declaradas: **13**
- Documentos de auditoria estática / limites: **13**
- Documentos com outro SHA-256 excluídos: **0**

**Importante:** os relatórios abaixo foram gerados em etapas anteriores. Suas contagens podem se sobrepor e não são somadas às microexecuções deste lote. A presença de um relatório e um texto PASS não é certificação integral nem reexecução do teste.

| Documento histórico | Tipo | PASS declarados completos |
|---|---|---:|
| [Isolated ARM conditional branch microexecution](SEMANTIC_BRANCH_MICROEXEC.md) | static_or_boundary_audit | 0 |
| [Validação dos contratos locais BX LR — todas as candidatas](SEMANTIC_BXLR_CONTRACT_PILOT.md) | static_or_boundary_audit | 0 |
| [Primeira fila de revisão formal: contratos BX LR](SEMANTIC_BXLR_REVIEW_BATCH.md) | static_or_boundary_audit | 0 |
| [ARM function entry and state-transition microexecution](SEMANTIC_ENTRY_PREFIX.md) | microexecution_report | 1 |
| [First-level ARM call contracts: GetParam / GetScale](SEMANTIC_GETPARAM_GETSCALE_AUDIT.md) | static_or_boundary_audit | 0 |
| [Original ARM GetParam / GetScale — microexecuted contracts](SEMANTIC_GETPARAM_GETSCALE_MICROEXEC.md) | microexecution_report | 3 |
| [Guarded ARM state-write microexecution](SEMANTIC_GUARDED_BLOCK.md) | microexecution_report | 1 |
| [Próximos destinos ARM de houkoku_okng — auditoria estática](SEMANTIC_HOUKOKU_NEXT_BOUNDARIES.md) | static_or_boundary_audit | 0 |
| [Candidatas de contrato semântico: folhas ARM BX LR](SEMANTIC_LEAF_BXLR.md) | static_or_boundary_audit | 0 |
| [Isolated ARM machine-instruction microexecution](SEMANTIC_MICROEXEC.md) | static_or_boundary_audit | 0 |
| [ARM next-boundary inspection — sound and icon](SEMANTIC_NEXT_BOUNDARIES.md) | static_or_boundary_audit | 0 |
| [ARM sound and icon — bounded pointer dereference microexecution](SEMANTIC_NEXT_POINTER_MICROEXEC.md) | microexecution_report | 2 |
| [Priority ARM conditional-path contracts](SEMANTIC_PATH_CONTRACTS.md) | static_or_boundary_audit | 0 |
| [GetParam/GetScale — next caller branches and arguments](SEMANTIC_POST_GETTER_PATHS.md) | microexecution_report | 1 |
| [ARM entry-to-return / first-call boundary evidence](SEMANTIC_RETURN_CALL_BOUNDARY.md) | microexecution_report | 1 |
| [sound_request — conservative ARM tail-branch chain](SEMANTIC_SOUND_CHAIN.md) | microexecution_report | 1 |
| [Original ARM boundaries — sound dispatcher and icon positioning](SEMANTIC_SOUND_DISPATCH_AUDIT.md) | static_or_boundary_audit | 0 |
| [Bounded ARM sound dispatcher and icon-position prologue execution](SEMANTIC_SOUND_ICON_MICROEXEC.md) | microexecution_report | 2 |
| [SysSE_PlayDef: auditoria estática da entrada A32 0x2b2cf8](SEMANTIC_SOUND_PLAYDEF_ENTRY.md) | static_or_boundary_audit | 0 |
| [Three real ARM callees — initial machine-code audit](SEMANTIC_THREE_CALLEES_AUDIT.md) | static_or_boundary_audit | 0 |
| [Three callees and two caller continuations — original ARM execution](SEMANTIC_THREE_CALLEES_EXECUTION.md) | microexecution_report | 1 |
| [Two consecutive ARM guards — bounded machine execution](SEMANTIC_TWO_GUARDS.md) | microexecution_report | 1 |
| [ARM callee: iOS_getV2Icon — verified instruction/data split](SEMANTIC_V2ICON_CALLEE.md) | static_or_boundary_audit | 0 |
| [ARM V2Icon BL and caller return-value branch microexecution](SEMANTIC_V2ICON_CALL_FLOW.md) | microexecution_report | 1 |
| [V2Icon caller — three post-return destinations and state effects](SEMANTIC_V2ICON_DESTINATIONS.md) | microexecution_report | 1 |
| [Isolated ARM V2Icon getter — machine-executed contract](SEMANTIC_V2ICON_EXECUTION.md) | microexecution_report | 1 |
