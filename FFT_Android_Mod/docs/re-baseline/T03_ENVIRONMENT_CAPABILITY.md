# T03 — Auditoria de capacidade de reconstrução e ambiente

Depende de T02 (`ready_for_review`, parcial). Executado em 2026-10-31.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** O ambiente de análise estrutural (Capstone/pyelftools/Unicorn + suíte de testes de `docs/re-tools`) é reproduzível em checkout limpo e foi confirmado nesta sessão. O ambiente de **build/reconstrução nativa** tem lacunas reais e documentadas abaixo que seguem pendentes.

## 1. Análise estrutural — reproduzível, confirmado nesta sessão

Comando único, em qualquer máquina com Python 3 moderno:

```bash
cd FFT_Android_Mod
python3 -m venv .venv-re-tools
.venv-re-tools/bin/pip install -r docs/re-tools/requirements-dev.txt
.venv-re-tools/bin/python3 -m pytest docs/re-tools -q
```

Executado nesta sessão, do zero, duas vezes (uma para descobrir as versões, outra para validar o pin exato de `docs/re-tools/requirements-dev.txt`):

| Item | Resultado |
|---|---:|
| `capstone` | `5.0.7` |
| `pyelftools` (`elftools`) | `0.33` |
| `unicorn` | `2.1.4` |
| Suíte de testes `docs/re-tools` | **528 testes / 1.812 subtestes — todos passando** |
| `docs/re-tools/progress_report.py` | Reproduz exatamente os números citados em `RE_COMPLETUDE_TASKS.md` §1 (6.455 entradas, 3.002 checkpoints, 2.952 `auto_structural`, 50 `needs_review`, 34 do núcleo, `pending=0`) |

**Nota sobre o Python do sistema (não do venv):** nesta máquina (Python 3.14.4, Ubuntu), `pip install` direto no interpretador do sistema falha com `externally-managed-environment` (PEP 668) — é obrigatório um virtualenv, como acima. Isso não é um problema do projeto, é uma restrição padrão de distros modernas; registrado aqui para quem tentar `pip install capstone pyelftools` direto, como a frase solta em `docs/re-tools/README.md` sugere, e receber um erro.

`requirements-dev.txt` é um arquivo novo, independente de `.github/ci/requirements-arm-re.txt` (que a própria CI deixa sem pin de propósito — "Pin versions in a separate validated PR"). Não alterei o arquivo da CI.

## 2. JADX — disponível e configurado

`REA_JADX_MCP_JAR=/home/c1c3ru/.local/share/rea/jadx/jadx-headless-mcp-0.7.1-all.jar` está definido e o arquivo existe. A pendência registrada em T01 ("`inspect_android_package` retornou `capability_unavailable`") não se repetiu nesta sessão nas verificações de ambiente — mas isso não foi reconfirmado chamando a ferramenta REA real; se a próxima tarefa precisar de JADX via REA e falhar de novo, registrar o erro exato ali, não aqui.

## 3. NDK — toolchains presentes, mas não há projeto de build nativo nenhum

Versões de NDK instaladas localmente: `26.3.11579264`, `27.0.12077973`, `27.1.12297006`, `28.2.13676358`, `29.0.13599879` (em `/home/c1c3ru/Android/Sdk/ndk/`).

Confirmando a lacuna já registrada em T01 (RE_COMPLETUDE_TASKS.md §1, nota "A busca por fontes e build nativo não identificou um projeto C/C++ próprio"): `scripts/build.sh` executa só três passos —

```
apktool b  →  zipalign  →  apksigner sign
```

Nenhuma etapa de compilação C/C++/NDK/CMake existe no pipeline atual. `apktool b` reempacota o `smali`/recursos e copia os `.so` de `src/lib/*` como estão (binários, possivelmente já patcheados conforme T01) — não compila nada a partir de fonte. **T32 (criar projeto de build nativo) começa do zero**; os NDKs acima ficam disponíveis como pré-requisito já satisfeito para quando essa tarefa for executada, mas não há nenhum `CMakeLists.txt`/`Android.mk`/equivalente no repositório hoje.

## 4. Decompilador nativo — não configurado, metodologia atual não depende de um

Não há variável de ambiente nem ferramenta configurada equivalente a Ghidra/IDA/Binary Ninja para decompilação automática de ARM/x86 nesta sessão. A metodologia já em uso no projeto (`jtable.py`/`struct_pass.py`, ver `docs/re-tools/README.md`) é deliberadamente baseada em **desmontagem via Capstone + reconstrução manual de pseudocódigo**, não em decompilação automática — e os 528 testes confirmam que essa cadeia funciona sem um decompilador externo.

**Decisão pendente, não tomada aqui:** se T10 (harness diferencial) ou T32 (reconstrução) exigirem decompilação automática como aceleração, isso é uma mudança de metodologia que precisa de decisão explícita do mantenedor — não presumir que falta uma ferramenta só porque nenhuma está configurada agora.

## 5. Build/instalação em dispositivo — caminhos de script não são reproduzíveis em checkout limpo

Achado que **bloqueia** o critério de aceite "comandos de análise e compilação reproduzíveis em checkout limpo" para a parte de build/instalação (a parte de análise estrutural, seção 1, já é reproduzível):

| Arquivo | Linha | Caminho absoluto hardcoded |
|---|---|---|
| `scripts/env.sh` | 8 | `/home/c1c3ru/.local/share/apktool/apktool_3.0.3.jar` |
| `scripts/env.sh` | 9 | `/home/c1c3ru/Android/Sdk/build-tools/36.0.0` |
| `scripts/install.sh` | 7 | `/home/c1c3ru/Android/Sdk/platform-tools/adb` |
| `scripts/push-obb.sh` | 8 | `/home/c1c3ru/Android/Sdk/platform-tools/adb` |

Esses quatro caminhos só funcionam na máquina/usuário atual (`c1c3ru`, com esse SDK instalado exatamente nessas versões). Em outro checkout — outra máquina, outro usuário, CI, ou mesmo este usuário com o Android SDK instalado em outro lugar — `scripts/build.sh`, `scripts/install.sh` e `scripts/push-obb.sh` falham sem explicação clara até alguém ler o `env.sh`. Nota: `apktool` também está disponível no `PATH` (`/home/c1c3ru/.local/bin/apktool`), então o `java -jar` explícito com caminho fixo é redundante além de não-portável.

**Não corrigido nesta tarefa** (T03 é auditoria, não refatoração de scripts de build de terceiros no projeto) — registrado como pendência explícita para quem for executar T32–T34, que dependem desses scripts.

## 6. Resumo por capacidade (exigido pelo critério de aceite de T03)

| Capacidade | Estado | Evidência |
|---|---|---|
| Capstone | ✅ disponível, pinado, testado | seção 1 |
| pyelftools | ✅ disponível, pinado, testado | seção 1 |
| Unicorn | ✅ disponível, pinado, testado (import only — harness real é T10) | seção 1 |
| `readelf`/`c++filt`/`objdump`/`nm` (binutils) | ✅ presentes no sistema (binutils 2.46) | verificado diretamente |
| JADX (via REA) | ✅ configurado (`REA_JADX_MCP_JAR`), não reexercitado nesta tarefa | seção 2 |
| NDK | ✅ 5 versões instaladas, ⚠️ nenhum projeto de build nativo existe ainda | seção 3 |
| Decompilador nativo automático | ❌ não configurado — metodologia atual não depende dele; mudar isso é decisão do mantenedor | seção 4 |
| `apktool`/`zipalign`/`apksigner` | ✅ presentes nesta máquina, ❌ caminhos hardcoded não portáveis | seção 5 |
| `adb` (instalação/push em dispositivo) | ✅ presente nesta máquina, ❌ caminho hardcoded não portável; **dispositivo real não testado nesta sessão** | seção 5 |

## 7. Arquivos produzidos por esta tarefa

- `docs/re-tools/requirements-dev.txt` — dependências de análise estrutural pinadas e validadas.
- Este relatório.

Nenhuma ferramenta não relacionada foi instalada no sistema; toda instalação de pacote Python ocorreu dentro de virtualenvs descartáveis fora do repositório, usados apenas para validar reprodutibilidade.
