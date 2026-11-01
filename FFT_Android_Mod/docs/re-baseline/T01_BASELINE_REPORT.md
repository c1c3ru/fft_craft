# T01 — Congelar baseline e explicar todos os patches

Executado em: 2026-10-31, nesta sessão. Ver `RE_COMPLETUDE_TASKS.md` §4 (P0) para o texto original da tarefa.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** Todas as identidades principais foram recalculadas e confirmadas; três patches reais foram localizados e dois são totalmente reproduzíveis byte a byte. Quatro lacunas ficam explicitamente pendentes (lista no final) e impedem declarar T01 concluída por completo, conforme o critério de aceite da própria tarefa ("bytes sem explicação ficam pendentes").

## 1. O que foi feito

- Recalculado o SHA-256 de todos os artefatos de identidade citados em `RE_COMPLETUDE_TASKS.md` §1, por leitura em streaming (chunks de 1 MiB, sem carregar os arquivos de 624 MB/815 MB inteiros na memória). **Todos os seis hashes citados no documento foram confirmados exatamente.**
- Produzido `docs/re-baseline/artifacts.json`: inventário com tamanho, SHA-256, origem conhecida/desconhecida, papel no projeto e ABI de 13 artefatos (dois APKs de referência + duplicata, ARM/x86 atuais e backups, OBB standalone e dentro do `.zip`, e os três artefatos de build gerados localmente).
- Comparados os membros dos dois APKs de referência (MortalGx vs. o nomeado "2.2.0"): 19 vs. 71 membros, apenas 8 em comum, com tamanhos diferentes em 6 dos 8 (`classes.dex`, `resources.arsc`, manifest, assinatura, `licensing.xml`). Confirma que são builds distintos, não duas cópias do mesmo pacote — ver seção 2.
- Feito o diff byte a byte (não amostrado) dos dois pares `.so` atual vs. `.so.orig_backup` (ARM e x86). Resultado: **exatamente 181 bytes diferentes em cada ABI**, concentrados numa janela de 234 bytes dentro da seção `.data`. Os diffs completos estão em `docs/re-baseline/native_lib_patch_diff.json` e o script `docs/re-baseline/apply_native_lib_patch.py` reaplica os 181 bytes sobre cada backup e confirma que o SHA-256 resultante bate exatamente com o `.so` atual (testado e confirmado nesta sessão para as duas ABIs).
- Localizados e confirmados por leitura direta dois patches já conhecidos pela documentação anterior, agora com valor exato:
  - Licenciamento sempre-verdadeiro em `ServerManagedPolicy.allowAccess()` (já documentado em `REVERSE_ENGINEERING_NOTES.md` §3).
  - `BuildSettings.OBB_VERSION = 0x31510` (202000) / `OBB_VERSION_STR = "202000"` em `src/smali/com/square_enix/FFT_Android/BuildSettings.smali` — explica por que o arquivo de expansão se chama `main.202000....obb` em vez de `main.1002....obb` (o `versionCode` original citado nas notas).
- Achado novo (não documentado antes): o arquivo `obb-data/main.202000....obb` e o membro OBB embutido em `com.square_enix.android_googleplay.FFT_en2.zip` têm o **mesmo tamanho declarado (815.622.218 bytes) mas SHA-256 e CRC32 diferentes**. Comparação em blocos de 1 MiB mostra 206 de 778 blocos divergentes — não é uma diferença de metadado isolado, é divergência real de conteúdo em ~26% do arquivo.

## 2. Comparação dos dois APKs de referência (resumo)

| | MortalGx (usado pelo projeto) | "2.2.0-APK_Award-Mod" |
|---|---:|---:|
| Membros no ZIP | 19 | 71 |
| `classes.dex` | 247.332 B | 1.457.440 B |
| ABI da lib nativa | `armeabi` (4.463.112 B) | `armeabi-v7a` (4.587.956 B) |
| Recursos Google Sign-In | ausentes | presentes |
| `resources.arsc` | 7.176 B | 153.464 B |

Conclusão objetiva: **não são builds comparáveis sem uma matriz de versão própria** (T02). Nenhum endereço, offset ou achado de engenharia reversa deve ser transferido entre os dois sem reverificação.

## 3. Patch binário no `.so` — o que se sabe e o que não se sabe

Sabido (evidência direta, reproduzida nesta sessão):
- Offset: `0x368b1e`–`0x368c07` no ARM, `0x3edbca`–`0x3edcb3` no x86 (mesma janela relativa, já que as duas libs compartilham layout de seções equivalente).
- Seção ELF: `.data` (PROGBITS, `WA`), não `.rodata`/`.text` — não é string nem código.
- Exatamente 181 bytes diferem dentro dessa janela de 234 bytes; os 181 diffs (offset, byte antes, byte depois) estão listados por completo em `native_lib_patch_diff.json`.
- O padrão de bytes é idêntico em forma entre ARM e x86 (mesmos valores relativos), sugerindo dado binário (não instrução), possivelmente um bitmap/textura pequena ou tabela compacta.

Não sabido (pendência explícita, não inventada):
- **Motivo/efeito semântico do patch.** Não foi feita análise de uso desse endereço (sem xrefs, sem leitura dos ponteiros que apontam para essa região de `.data`). Isso pertence a uma tarefa de análise estrutural dedicada (T04/T08), fora do escopo de "congelar e registrar" de T01.

## 4. Pendências que impedem marcar T01 como `done`

1. Motivo semântico do patch binário de 181 bytes (seção 3) — requer análise de xrefs/uso, não apenas diff.
2. Divergência de conteúdo entre `obb-data/*.obb` e o OBB embutido no `.zip` (mesmo tamanho, hash e CRC diferentes, 206/778 blocos de 1 MiB divergentes) — não se sabe qual arquivo é a imagem correta/atual nem a causa da divergência. Decisão de qual é a linha de base pertence a T02.
3. Não existe backup do `classes.dex`/smali anterior ao patch de licenciamento e ao patch de `OBB_VERSION` — a confirmação desses dois patches veio de leitura do estado atual + número citado nas notas antigas (`versionCode=1002`), não de um diff binário direto como foi feito para o `.so`. Se um DEX original aparecer, repetir o diff byte a byte.
4. Origem/procedência de `obb-data/*.obb` e do `.zip` (quem gerou, quando, a partir de qual fonte) não está documentada em nenhum arquivo do repositório encontrado nesta auditoria.

## 5. Como reproduzir

```bash
# Recalcular hashes de identidade (streaming, seguro para os arquivos grandes)
python3 -I - <<'PY'
import hashlib
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while chunk := f.read(1024*1024):
            h.update(chunk)
    return h.hexdigest()
print(sha256_file("FFT_Android_Mod/original/FFT_By_MortalGx.apk"))
PY

# Confirmar o patch binário do .so (as duas ABIs)
python3 -I FFT_Android_Mod/docs/re-baseline/apply_native_lib_patch.py all
```

## 6. Arquivos produzidos por esta tarefa

- `docs/re-baseline/artifacts.json` — inventário de identidade.
- `docs/re-baseline/native_lib_patch_diff.json` — diff byte a byte completo dos dois `.so` patcheados.
- `docs/re-baseline/apply_native_lib_patch.py` — script de reprodução/verificação do patch binário.
- Este relatório.
