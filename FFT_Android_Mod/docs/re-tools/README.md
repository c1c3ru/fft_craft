# Ferramentas do loop de engenharia reversa

Scripts usados pelo processo descrito em `REVERSE_ENGINEERING_NOTES.md`,
seção "Metodologia do loop". Dependências: `capstone`, `pyelftools`
(`pip install capstone pyelftools`), e `readelf`/`c++filt` do binutils
no PATH. Alvo: `src/lib/armeabi/libgl2jni.so`.

- **`jtable.py <so> <start_hex> <end_hex_ou_+len>`** — descida
  recursiva de uma função, resolve tabelas de salto ARM
  (`add{cond} pc, pc, rX, lsl #2`) achando o `cmp` de guarda real
  andando pra trás no fluxo de instruções (recusa honestamente se o
  registrador foi sobrescrito antes), usa as entradas resolvidas como
  semente e repete até não achar mais código novo. Imprime cobertura,
  tabelas resolvidas e o catálogo de `bl` (resolvido contra `.dynsym`
  + demangle). Ferramenta principal pro passe estrutural de uma
  função nova — validada contra `battle()`.

- **`struct_pass.py <so> <start_hex> <end_hex_ou_+len>`** — mesma
  descida recursiva sem resolução de tabela de salto; serve pra uma
  primeira olhada rápida (branches, `bl`, pontos de convergência) antes
  de decidir se vale a pena rodar `jtable.py` completo.

- **`family_sim.py <so> <ref_start> <ref_end_ou_+len> <nome:start:end_ou_+len>...`**
  — compara o catálogo de endereços `bl` de uma ou mais funções
  candidatas contra uma função de referência já confirmada
  (`read_structural`/`read_full`), via similaridade de Jaccard.
  ≥90% de Jaccard e zero tabela de salto não resolvida =
  `CONFIRMED-BY-SIMILARITY` — a função pode ser marcada sem passe
  estrutural individual. Usado pra fechar a família `Mdl*` em lote
  (ver NOTES §101).

`struct_pass2.py` (tentativa de descida em cascata totalmente
automática) foi testado e abandonado — gerou falsos positivos de
tabela de salto. Não está aqui; não vale retomar sem entender a causa
raiz dos falsos positivos.
