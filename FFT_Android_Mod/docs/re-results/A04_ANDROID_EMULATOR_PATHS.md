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

A asserção do probe foi corrigida para o comportamento Android observado (**4 bytes**) e passou a verificar **os bytes efetivos de GetStringUTFChars em hexadecimal**, além da contagem. A validação dessa correção fica condicionada ao próximo run no commit correspondente.

**Não confundir a amostra do APK de diagnóstico com execução do jogo**: seu único valor comprobatório é o comportamento dos getters do Android sob o mesmo package ID, em ambiente isolado. Outros dispositivos/API levels/usuários podem produzir caminhos mais longos, nulos ou diferentes. A04 segue in_progress; nenhum certificado de segurança ou equivalência total.
