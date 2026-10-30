# B01 — revisão estática dos nove grupos ARM, vínculo JNI e estado do OBB

**Estado:** `B01=in_progress`; registros de desassemblagem e nomes não bastam para provar equivalência, reachability ou concluir o aplicativo.

## Contexto e hipótese

O inventário original contém 15 pares de intervalos sobrepostos distribuídos por nove grupos de mesmo endereço final. Esse padrão é **compatível** com múltiplos entrypoints, caudas de função compartilhadas ou metadados de tamanho incorretos. Os três casos não são equivalentes e precisam ser separados pelo CFG, pelos acessos de execução e por testes diferenciais, preservando o mesmo SHA-256 de ELF.

A ferramenta `b01_overlap_elf_evidence.py` lê o ELF32 ARM file-backed original, recusa SHA divergente, busca as faixas em segmentos executáveis, desmonta A32 com Capstone, anota bytes, primeiros e últimos opcodes, desvios diretos internos e resumos hash de cada intervalo. Também gera **15 disposições preliminares** em nove grupos sem apagar símbolos. Cada linha mantém `needs_review=true`, mesmo se todas as instruções de um intervalo puderem ser desmontadas. A extensão em Thumb, saltos indiretos, literais e caminhos externos continuam passíveis de revisão.

**Critério de aceite da #478:** classificar cada grupo com provas de entrada e de continuidade no CFG, fontes de chamadas e limites; sem caminhos desconhecidos tratados como certificados.

## Smali → JNI

O segundo analisador, `b01_smali_jni_obb_audit.py`, pesquisa declarações `.method ... native` no Smali, detecta candidatos `Java_<classe>_<metodo>` na tabela `.dynsym` do ELF, reporta menções estáticas a `StorageUtil`, `GetIntPath` e `GetExt1Path` e o carregamento da biblioteca `gl2jni`.

- `GL2JNILib.smali` declara métodos JNI nativos e usa `System.loadLibrary("gl2jni")`.
- Uma exportação JNI com nome correspondente é **apenas candidato de ligação**, não prova de execução, assinatura correta no runtime nem comportamento do método.
- Registros via `RegisterNatives`/tabela de funções JNI e métodos indiretamente ligados podem não aparecer por convenção de nome. Esses casos permanecem `unresolved`.
- `A04` exige observação autorizada de `StorageUtil → JNI → R1` no próprio processo original; nenhum resultado estático é promovido a esse gate.

## OBB

O OBB rastreado em Git é um ponteiro Git LFS. O analisador registra, quando disponível, o OID SHA-256 e o tamanho **declarados** pelo ponteiro, sem dizer que os dados estão localmente verificados. Caso o arquivo seja materializado numa execução privada, compara hash do conteúdo e examina **apenas metadados** de diretório ZIP, sem extrair nem publicar arquivos. Se não for ZIP, o formato continua desconhecido. Nenhuma leitura de entrada ZIP foi verificada neste ciclo.

A materialização do OBB (disponibilidade, autorização, integridade, estrutura e relacionamento com APK) é gate posterior específico; não acionar transferências Git LFS caras em todo pull request.

## Testes e reproduções

```bash
python -m pip install capstone==5.0.6 pyelftools==0.32
python -m unittest discover -s FFT_Android_Mod/docs/re-tools -p 'test_b01_static_links.py' -v
python FFT_Android_Mod/docs/re-tools/b01_overlap_elf_evidence.py \
  --binary FFT_Android_Mod/src/lib/armeabi/libgl2jni.so \
  --inventory FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv \
  --output /tmp/b01-overlap-disposition.json
python FFT_Android_Mod/docs/re-tools/b01_smali_jni_obb_audit.py \
  --root . --output /tmp/b01-static-jni-and-obb.json
```

O workflow `.github/workflows/re-b01-static-evidence.yml` executa esses passos em host, produz artefatos com dados auditáveis e não concede certificados. Relatar resultados concretos e o run no comentário da issue #478 após CI.

**Dependências restantes:** evidência de CFG e da origem das entradas do ELF, inventário completo JNI/Smali e OBB materializado, antes de liberar `A03/R01/R02`. O progresso formal permanece 2/17.
