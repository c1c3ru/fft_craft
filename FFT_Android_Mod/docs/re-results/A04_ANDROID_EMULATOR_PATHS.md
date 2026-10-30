# A04 — amostragem do caminho Android por JNI, sem executar o jogo original

A cadeia original de `CAPP_INFO::Init` obtém `GetIntPath` ou `GetExt1Path` da classe `StorageUtil`, copiando o resultado para um buffer de caminho sem limite de comprimento. O limite necessário para `/base/fftpack.bin\0` dentro dos 260 bytes observados é **B <= 242 bytes UTF modificado**, sendo B o comprimento efetivo do caminho Java no JNI.

## O que o APK de diagnóstico mede

O projeto isolado em `docs/re-tools/android-path-probe/` cria um APK Android mínimo cujo *applicationId* coincide com o do jogo `com.square_enix.android_googleplay.FFT_en2`, em emulador limpo. Ele executa as duas APIs Android que aparecem no smali real:

- `Context.getFilesDir().getPath()`;
- `Context.getExternalFilesDir(null).getPath()`, incluindo caso de `null`.

A implementação de teste usa uma biblioteca C JNI real e `GetStringUTFLength`, medindo quantidade de bytes modificados UTF-8; também testa strings sintéticas de 242/243 bytes, emoji (6 bytes JNI) e NUL embutido (2 bytes JNI). A saída é JSON com SDK, presença e contagens de bytes, **sem gravar os caminhos de diretório**.

O workflow `.github/workflows/re-a04-android-path-probe.yml` tem dois jobs: compilar um APK de diagnóstico assinado com chave de debug e executar esse APK no emulador Android API 29/x86_64. O `run-emulator.sh` lê o JSON via `adb shell run-as` e verifica as contagens. Não instala nem executa o jogo original.

## O que essa evidência NÃO prova

Este é um APK de teste com o mesmo nome de pacote, **não o APK original nem seu processo JNI/Android**. Demonstra exemplos de comportamento da plataforma para esse *applicationId*, mas não garante que o caminho, a inicialização, os storages montados ou as configurações do jogo sejam os mesmos. Em particular, uma amostra de B<=242 NÃO prova um limite máximo universal; o Android pode retornar caminhos de tamanho diferente em outros dispositivos, usuários, perfis, estados de armazenamento e versões.

Também não reproduz `strcpy` original nem tenta entradas excedentes em libc sem isolamento. A condição de segurança **B<=242** continua pré-condição de execução real do jogo até haver rastreamento e prova em seu próprio contexto.

## Próximos gates

1. Repetir em mais APIs/perfis de emulador para capturar variações legítimas do contexto e calcular margem real por ambiente.
2. Executar uma instrumentação autorizada no próprio processo do APK original para obter os jstrings devolvidos por `StorageUtil` e comparar com os parâmetros entregues ao JNI nativo, sem injetar ponteiros nem executar cópias excedentes.
3. Verificar falhas de `getExternalFilesDir(null)`, exceções, retorno nulo e valores de comprimento acima de 242 bytes.
4. Manter A04 `in_progress` e nenhum certificado novo enquanto as condições de runtime do jogo não forem verificadas.

## Primeiro ensaio Android API 29 — evidência real e divergência de codificação

O [run #40922599862](https://github.com/c1c3ru/fft_craft/actions/runs/40922599862) conseguiu compilar, instalar e executar o APK independente no emulador e publicou o JSON de saída. O job foi marcado **failure** porque a asserção de teste ainda esperava a codificação de um caractere suplementar segundo o OpenJDK, não a implementação Android ART.

| Fonte observada no emulador API 29 | Bytes `GetStringUTFLength` | Critério <=242 |
|---|---:|---|
| `Context.getFilesDir().getPath()` | **61** | sim, nesta amostra |
| `Context.getExternalFilesDir(null).getPath()` | **81** | sim, nesta amostra |

O probe verificou NUL Java em `"a\0b"` (4 bytes JNI) e strings ASCII de 242 e 243 bytes corretamente. Para o emoji `U+1F600`, o Android ART reportou **4 bytes** contra **6 bytes** no host OpenJDK 17/21. O código-fonte do Android ART reconhece explicitamente que emite sequência UTF-8 de quatro bytes nesse caso, embora a especificação JNI descreva Modified UTF-8 de seis bytes:

- [AOSP ART — comportamento histórico de GetStringUTFLength/GetStringUTFChars](https://android.googlesource.com/platform/art/+/ef21fb5f2520c604a6d5659452488a93433ee85a/runtime/jni/jni_internal.cc)
- [Discussão do Android NDK sobre codificação de emoji](https://github.com/android/ndk/issues/283)

A asserção do probe foi corrigida para o comportamento Android observado (**4 bytes**) e passou a verificar **os bytes efetivos de GetStringUTFChars em hexadecimal**, além da contagem. O [run #40923703664](https://github.com/c1c3ru/fft_craft/actions/runs/40923703664) confirmou **sucesso** no APK de diagnóstico com o novo gate de hexadecimais.

### Segundo ensaio: gate Android API 29 aprovado

| Método de plataforma espelhado | Bytes JNI | Limite B<=242 |
|---|---:|---|
| Context.getFilesDir().getPath() | **61** | satisfeito nesta amostra |
| Context.getExternalFilesDir(null).getPath() | **81** | satisfeito nesta amostra |

O JSON também confirmou `U+1F600` como `f09f9880` (4 bytes) e `a\u0000b` como `61c08062` (4 bytes), ambos provenientes de `GetStringUTFChars` no emulador. O teste de build, o emulador e o gate de conteúdo passaram; os workflows gerais do PR #457 também ficaram verdes. O artifact do run persiste apenas status, contagens e bytes sintéticos, sem gravar diretórios reais.

**Cuidado:** esses dados não constituem prova de um teto máximo dos diretórios Android em todos os dispositivos e instalações. A execução do ELF original, seus controles de concorrência, seus fallthroughs e seu `strcpy` continuam fora do escopo do teste.

**Não confundir a amostra do APK de diagnóstico com execução do jogo**: seu único valor comprobatório é o comportamento dos getters do Android sob o mesmo package ID, em ambiente isolado. Outros dispositivos/API levels/usuários podem produzir caminhos mais longos, nulos ou diferentes. A04 segue in_progress; nenhum certificado de segurança ou equivalência total.


## Extensão da matriz: APIs Android 23, 29 e 35

A partir do teste API 29 aprovado, o workflow executa **a mesma compilação do APK de diagnóstico** em três emuladores x86_64 isolados, com `fail-fast: false`. O objetivo é medir a variabilidade entre versões do Android, não declarar um limite máximo universal. O script `run-emulator.sh` confere que `ro.build.version.sdk` e o campo `android_sdk` do JSON correspondam ao nível realmente pedido; mantém a proibição de substituir um jogo instalado no mesmo pacote.

Após os três jobs, `compare-api-matrix.py` agrega somente o nível de API, a presença de cada retorno, sua contagem de bytes JNI, a margem para 242 bytes e a sinalização de excesso. **Não transporta nem armazena os caminhos reais no artefato consolidado**, embora o probe individual também só publique suas contagens. Saídas nulas permanecem explicitamente `present=false`, nunca são contadas como caminho de comprimento zero. Um resultado acima de 242 bytes deve ser **reportado como observação de risco**, não ocultado para obter CI verde.

O agregador rejeita duplicidade de API, rotulagem incorreta de um emulador, inconsistência entre bytes e flag de limite, além de alegações de que o APK original ou a `strcpy` original foram executados. O CI executa seis testes sintéticos para evitar promoções indevidas de cobertura ou vazamento de caminhos em relatórios.

Em todos os cenários:

- O APK é **independente do jogo**; compartilha apenas a identidade de pacote necessária ao formato de caminho.
- A versão do ART pode alterar o comportamento de codificação observado; o JSON de JNI continua sendo a fonte direta de contagem.
- A condição `B <= 242` segue necessária para o layout reconstruído de `/base/fftpack.bin\0`, sem ser garantia universal de sistema.
- `A04=in_progress` e o número de certificados novos permanece **zero**.

**Próximo gate depois da matriz:** investigar diferenças legítimas entre perfil/usuário/armazenamento, testar retornos nulos e exceções, e medir no próprio processo do jogo em ambiente autorizado, sem provocar `strcpy` excessiva.

### Validação funcional com bytes do ART (sem executar o jogo)

O APK de diagnóstico passa também os bytes fornecidos por `GetStringUTFChars` para **`a04_rootpath_safe.c`**, a reconstrução independente que valida limite e capacidade antes de escrever. O código foi incorporado à biblioteca do APK, e **não** recebe nem chama qualquer instrução do ELF original ou sua `strcpy`.

O gate verifica aceitação em **242 bytes**, rejeição em **243 bytes**, aceitação de exemplos de NUL Java e emoji após codificação efetiva pelo ART, e canários após a região de 260 bytes. Para os caminhos `GetIntPath` e `GetExt1Path`, a aceitação do modelo C deve coincidir com a comparação `B <= 242`. O agregador valida a consistência desses resultados, mas não reporta dados de caminho.

Isso comprova apenas o funcionamento da **implementação independente delimitada** sob JNI real nos emuladores testados. Não estabelece equivalência com a biblioteca original para entradas inválidas nem substitui instrumentação do jogo em Android.

