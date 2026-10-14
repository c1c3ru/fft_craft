# Relatório de Análise — `libgl2jni.so` (FFT_Android_Mod)

**Alvo:** motor nativo do jogo *Final Fantasy Tactics: The War of the Lions* (port Android), biblioteca JNI que conecta a camada Java (`com.square_enix.FFT_Android`) ao código C/C++ do jogo.

Arquivos analisados:
| Variante | Caminho | Tamanho |
|---|---|---|
| ARM (armeabi) | `src/lib/armeabi/libgl2jni.so` | 4.463.112 bytes |
| x86 | `src/lib/x86/libgl2jni.so` | 4.988.572 bytes |

Ferramentas usadas: `file`, `readelf`, `objdump`, `strings`, `c++filt`, e um scanner de assinaturas de arquivo em Python (equivalente simplificado ao `binwalk`, que não estava instalado no ambiente).

---

## 1. Informações de cabeçalho (ELF)

| Campo | ARM | x86 |
|---|---|---|
| Classe | ELF32 | ELF32 |
| Máquina | ARM, EABI5 | Intel 80386 |
| Tipo | DYN (objeto compartilhado) | DYN (objeto compartilhado) |
| Interpretador | `/system/bin/linker` | `/system/bin/linker` |
| Símbolos | **stripped** (sem tabela `.symtab` de depuração) | **stripped** |
| SONAME | `libgl2jni.so` | `libgl2jni.so` |

As duas são builds da mesma base de código para arquiteturas diferentes — mesmas dependências, mesmas funções JNI, mesmo conjunto de classes internas. A versão x86 é maior (~525 KB) provavelmente por diferenças no code-gen do compilador para essa ABI.

---

## 2. Dependências dinâmicas (`readelf -d`)

Idênticas nas duas variantes:

```
NEEDED   liblog.so        (logging do Android)
NEEDED   libGLESv2.so     (OpenGL ES 2.0 — renderização)
NEEDED   libEGL.so        (gerenciamento de contexto gráfico)
NEEDED   libOpenSLES.so   (áudio nativo Android)
NEEDED   libstdc++.so
NEEDED   libm.so
NEEDED   libc.so
NEEDED   libdl.so
SONAME   libgl2jni.so
```

Nenhuma dependência de rede, criptografia externa ou bibliotecas de terceiros fora do padrão NDK — tudo o que o jogo precisa (zlib, libvorbis/ogg, etc.) está **estaticamente embutido** no próprio `.so` (ver seção 4).

---

## 3. Funções JNI exportadas (ponte Java ↔ Nativo)

A classe Java correspondente é `com.square_enix.FFT_Android.GL2JNILib`. Funções encontradas (idênticas nas duas arquiteturas, 12 no total):

| Função JNI | Provável finalidade |
|---|---|
| `Java_..._init` | Inicializa a engine nativa |
| `Java_..._step` | Executa um frame/tick do loop principal |
| `Java_..._onResume` / `_onPause` | Ciclo de vida da Activity Android |
| `Java_..._onDestroy` | Encerramento/limpeza |
| `Java_..._isExit` | Consulta se o jogo pediu para fechar |
| `Java_..._onTouchEvent` | Entrada de toque |
| `Java_..._onKeyEvent` | Entrada de teclado/botão físico |
| `Java_..._dialogOnClose` | Callback de diálogos nativos (UI) |
| `Java_..._setBatteryLevel` | Repassa nível de bateria ao C++ |
| `Java_..._setAccelerometerValue` | Repassa dados do acelerômetro |
| `Java_..._getCommand` | Lê comandos pendentes da fila nativa (`g_iJNICmd`) |

A tabela `.dynsym` tem **9.162 entradas** (ARM) — a grande maioria não é API pública, mas símbolos globais "vazados" por não ter sido feito um `strip`/`visibility=hidden` completo em bibliotecas estáticas internas (zlib, libogg etc. aparecem com símbolos como `deflate`, `crc32`, `oggpack_read`...).

---

## 4. Strings extraídas — achados relevantes

### 4.1 Bibliotecas de terceiros embutidas estaticamente
- **zlib** (`deflate`, `inflate`, `crc32`, `adler32`, `compress2`...) — compressão de assets.
- **libogg/libvorbis** (`oggpack_read`, `ogg_packet_clear`, `vorbis_version_string`) — áudio comprimido (música/efeitos).

### 4.2 Classes C++ internas (43 identificadas via demangling de `_ZN...`)
Principais: `CAPP_INFO`, `CAUTOSAVE`, `CCAMERA`, `CCRYPT`, `CEGL2_FBO/IF/SHADER/SPRITE/TEX_HYBRID`, `CFFT_STATE`, `CFILE/CFILE_DAT/CFILE_TXT`, `CG2D_LOADER_BMP/TGA/TIM`, `CINPUT_IF_TOUCH`, `CSOUND_IF_SL`, `CSOUND_LOADER_OGG/PCM`, `CTHREAD`, `CUI_SCROLLBAR`.

- `CG2D_LOADER_TIM` → suporte ao formato de textura **TIM** (usado no PS1/PSP), confirmando que o motor gráfico é herdado diretamente da versão PSP do jogo.
- `CCRYPT` (`Encrypt`/`Decrypt`) e `CFILE_DAT::Decrypt` → os arquivos de dados do jogo (`.bin`/`.dat`) são **criptografados** com um algoritmo próprio antes de serem lidos.

### 4.3 Evidência de origem no código iOS
Funções como `CAPP_INFO::GetEnableiCloud`, `CAPP_INFO::IsDeviceiPhoneRetina4inch` e `CAPP_INFO::GetDeviceOrientation` mostram que esta base de código C++ foi **portada diretamente da versão iOS** — essas APIs ficam presentes (porém inativas) no binário Android.

### 4.4 Caminhos de código-fonte (preservados nos símbolos/strings)
```
jni/../../Classes/fftpsp/src/mk/ios_bcalc.cpp
jni/../../Classes/fftpsp/src/mk/ios_bw_init.cpp
jni/../../Classes/fftpsp/src/mk/ios_comwind.cpp
jni/../../Classes/fftpsp/src/mk/ios_mw_init.cpp
jni/../../Classes/fftpsp/src/mk/ios_search.cpp
jni/../../Classes/fftpsp/src/mu/ios_BATTLE.cpp
jni/../../Classes/fftpsp/src/mu/ios_INITMAP.cpp
```
A pasta `fftpsp` com arquivos prefixados `ios_` confirma a árvore de build real da Square Enix: **PSP → iOS → Android**, reaproveitando a mesma lógica de batalha/mapas (`mk` = provavelmente "map/kernel", `mu` = "map/unit" ou "menu").

### 4.5 Caminhos hardcoded da máquina de build original (Windows)
```
c:\fftimg\event\chapter1.bin ... chapter4.bin
c:\fftimg\event\end1.bin ... end5.bin
c:\fftimg\event\gameover.bin
C:\FFTIMG\MAP\GNS\
```
Vazamento de caminho de desenvolvimento: a ferramenta de build/empacotamento de eventos e mapas do jogo rodava em `C:\FFTIMG\` na máquina do desenvolvedor original.

### 4.6 Arquivos de dados referenciados pelo motor
```
fftpack.bin   g2d.dat   gTex16.bin   gTex16D.bin   gTex16R.bin
gTex256.bin   music.dat   sound.dat   link/titles.txt
```
Esses são os pacotes de dados externos (texturas, música, sons, legendas) que o `.so` carrega em tempo de execução — **não estão embutidos no binário**, ficam ao lado do APK/OBB.

### 4.7 Strings de conteúdo do jogo (romanização japonesa)
Nomes de habilidades/magias usados internamente como identificadores de depuração/debug, por exemplo: `ankokuken` (espada das trevas), `monomane` (mímica), `majinshoukan` (invocação demoníaca), `onmyoujutu`/`onmyoumahou` (magia onmyou), `kyouhu1`, `gasuto`, `nusumu` (roubar), `bampaia` (vampiro), entre dezenas de outras — strings de debug ligadas ao sistema de batalha, não visíveis normalmente ao jogador.

### 4.8 Mensagens de erro/estado do zlib
`"buffer error"`, `"need dictionary"`, `"out of room to push characters"`, `"Decode: inflate"`, `"Encode: deflate"` — mensagens padrão da zlib embutida, sem relação com lógica própria do jogo.

---

## 5. Varredura por assinaturas de arquivo embutido (equivalente ao `binwalk`)

O `binwalk` não estava disponível no ambiente, então foi feita uma varredura manual por assinaturas (magic bytes) nos dois binários:

| Assinatura | ARM | x86 | Observação |
|---|---|---|---|
| `PK\x03\x04` (ZIP/APK) | 1 ocorrência | 1 ocorrência | **Falso positivo provável** — 4 bytes comuns em código de máquina |
| `BM` (BMP) | 58 | 60 | **Falso positivo** — sequência de 2 bytes extremamente comum em ARM/x86 |
| `\xff\xd8\xff` (JPEG) | 15 | 17 | **Falso positivo provável** — 3 bytes, alta chance de coincidência |
| `OggS` (OGG) | 1 | 2 | Possível, mas sem estrutura válida de arquivo ao redor — não confirmado |
| `RIFF` (WAV/AVI) | 1 | 1 | Não confirmado — sem cabeçalho RIFF completo válido |
| PNG / GIF / GZIP | 0 | 0 | Não encontrados |

**Conclusão desta seção:** não há evidência confiável de arquivos de mídia completos embutidos no `.so`. As classes `CG2D_LOADER_BMP/TGA/TIM` e `CSOUND_LOADER_OGG/PCM` indicam que o motor sabe **decodificar** esses formatos, mas os dados reais (texturas, músicas) vêm de arquivos externos (`g2d.dat`, `music.dat`, `gTex*.bin`), não de dentro da biblioteca. Para extração real de assets, seria necessário analisar o APK/OBB do jogo, não a `.so`.

---

## 6. Resumo comparativo ARM vs x86

| Aspecto | ARM | x86 |
|---|---|---|
| Dependências | idênticas | idênticas |
| Funções JNI | idênticas (12) | idênticas (12) |
| Caminhos de código-fonte nas strings | idênticos | idênticos |
| Tamanho do binário | 4.463.112 bytes | 4.988.572 bytes (+11,8%) |
| Assinaturas de arquivo (offsets) | presentes, offsets diferentes (apenas por layout de compilação) | idem |

As duas bibliotecas são a **mesma base de código** compilada para arquiteturas diferentes — nenhuma diferença funcional identificada nas strings/símbolos extraídos.

---

## 7. Descompilação (Hopper Disassembler, via MCP/REA)

Tentativa de configurar o **Ghidra** encontrada um bloqueio de ambiente: o provider exige um JDK 21+ completo (`GHIDRA_INSTALL_DIR` + Java ≥21), e embora o sistema tenha JDK 25 instalado, a variável `JAVA_HOME` do processo do servidor REA já estava fixada no JDK 17 — não é possível alterar o ambiente de um processo MCP já iniciado sem reiniciar o cliente, e o Ghidra em si (binário) nem está baixado. Em vez de instalar ~400 MB adicionais sem necessidade, foi usado o **Hopper Disassembler**, que já estava instalado e configurado neste ambiente (`/opt/hopper`), para descompilar as funções-chave do binário ARM.

> ⚠️ Pseudocódigo gerado por decompilador (Hopper), não é o código-fonte original da Square Enix — reconstrução aproximada da lógica a partir do binário.

### 7.1 `CCRYPT::Encrypt(unsigned char* buf, int size, unsigned int key)`
```c
r4 = SAR(r4, r1 / 0x80000000);
r3 = r1 + 0x3;
if (r1 >= 0x0) r3 = r1;
// r3 = (size arredondado para baixo, múltiplo de 4) -> processa em blocos de 4 bytes
if (bool_2) r4 = r0 + r3;   // fim do bloco alinhado a 4 bytes
if (!bool_6) {
    do {
        r12 = *r1;
        r12 = r12 ^ r2;      // XOR de cada word de 32 bits com a chave (r2 = key)
        *r1 = r12;
        r1 = r1 + 0x4;
    } while (r1 != r4);
}
// bytes restantes (0-3) são XORados byte a byte com os bytes da própria chave
if (!bool_5) {
    r2 = r2 + 0x1;
    *(int8_t*)r3 ^= *(int8_t*)r2;
    r3 = r3 + 0x1;
    ...
}
return 0x0;
```
**Interpretação:** é uma cifra **XOR simples** (stream cipher trivial). O buffer é dividido em blocos de 4 bytes, cada bloco é XORado com o valor de 32 bits da chave (`key`); os bytes finais que não completam um bloco de 4 são XORados byte a byte usando os bytes individuais da chave. Não há expansão de chave, S-boxes nem rounds — é criptografia "cosmética" (ofuscação), não criptografia forte.

### 7.2 `CCRYPT::Decrypt(unsigned char* buf, int size, unsigned int key)`
```c
r0 = CCRYPT::Encrypt(arg0, arg1, arg2);
return r0;
```
**Interpretação:** confirma matematicamente a dedução acima — como XOR é involutivo (`x ^ k ^ k == x`), `Decrypt` é literalmente **a mesma função** `Encrypt`, só chamada com o mesmo buffer/chave. Isso significa que qualquer arquivo `.dat`/`.bin` do jogo pode ser decifrado/cifrado com o mesmo código, desde que se conheça a chave usada em cada chamada (a chave é passada pelo chamador — não está fixa dentro de `CCRYPT`).

### 7.3 `CFILE_DAT::Decrypt(int file_index, unsigned int key)`
```c
r7 = CFILE_DAT::GetBuffer(arg0);   // ponteiro do arquivo já carregado no cache
r0 = CFILE_DAT::GetSize(arg0);     // tamanho do arquivo em cache
r0 = CCRYPT::Decrypt(r7, r0, r2);  // aplica o XOR em todo o buffer
return r0;
```
**Interpretação:** liga a camada de arquivos (`CFILE_DAT`, que gerencia os pacotes `.dat`) à cifra: ao carregar um arquivo do pacote, o buffer inteiro em cache é decifrado in-place com a chave fornecida por quem chamou `Decrypt`.

### 7.4 `CG2D_LOADER_TIM::Load(char* filename, unsigned short* mem, unsigned int size1, unsigned int size2)`
```c
memset(r4 + 0x4, 0x0, 0x10);
if (filename != NULL) {
    if (TIM_LoadFile(this, filename) != 1) { /* erro -> grava info de formato/extensão, retorna 0 */ }
    else return 1;
} else {
    if (TIM_LoadMemory(this) == 1) return 1;
    else { /* mesmo tratamento de erro */ }
}
```
**Interpretação:** função de entrada do loader de texturas TIM (formato de imagem do PS1/PSP). Se recebe um nome de arquivo, carrega do disco (`TIM_LoadFile`); se recebe `NULL`, assume que os dados já estão em memória (ex.: descompactados de `gTex16.bin`) e usa `TIM_LoadMemory`. Em caso de falha, preenche um código de erro (`0xb`) e strings de diagnóstico com o tipo/extensão de imagem esperados.

### 7.5 Funções que o Hopper não conseguiu descompilar
`TIM_AnalyzeFileHeader` (19 blocos básicos, 432 bytes) e `TIM_LoadFile`/`TIM_LoadMemory` retornaram pseudocódigo nulo — o decompilador do Hopper não conseguiu reconstruir essas funções especificamente (provavelmente por causa de saltos/switch complexos no parsing do cabeçalho binário do formato TIM). A lógica de parsing do cabeçalho TIM em si (dimensões, paleta, bits por pixel) não pôde ser recuperada como pseudocódigo nesta sessão; seria necessário ler a montagem ARM bruta (`procedure_assembly`) ou tentar o Ghidra depois de corrigir o `JAVA_HOME`.

---

## 8. Observações finais

- Binário **stripped** (sem `.symtab`/debug info), mas a tabela dinâmica (`.dynsym`) ainda expõe milhares de símbolos de bibliotecas estáticas internas (zlib, libogg) e de quase todas as classes do jogo — isso facilita bastante engenharia reversa adicional (os nomes de função já aparecem corretamente, sem precisar de pattern-matching).
- O esquema de "criptografia" dos arquivos `.dat`/`.bin` do jogo é um **XOR simples e simétrico** (seção 7.1–7.3), não um algoritmo criptográfico forte — serve apenas para dificultar a inspeção casual dos arquivos de dados, não para proteção real.
- Para ir além (recuperar a chave XOR usada em cada chamada, reconstruir o parser do formato TIM por completo), o próximo passo seria rastrear os chamadores de `CFILE_DAT::Decrypt`/`CG2D_LOADER_TIM::TIM_AnalyzeFileHeader` para ver de onde vêm as chaves e os offsets — via `procedure_callers`/`xrefs` no REA, ou finalizando a configuração do Ghidra (corrigindo `JAVA_HOME` do processo MCP e baixando o `GHIDRA_INSTALL_DIR`).
- Nenhuma chave de API, URL de servidor remoto, token ou segredo de rede foi encontrado nas strings — compatível com um jogo single-player sem componente online.
