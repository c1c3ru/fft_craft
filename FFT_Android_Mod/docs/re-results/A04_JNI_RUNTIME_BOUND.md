# A04 — Validação JNI de bytes UTF modificados e fronteira 242/243

A cadeia ARM original chega à classe `com/yox_project/silver_arrow/StorageUtil` e obtém `String` Java através de JNI. O modelo original usa `strcpy` sem limite; a condição necessária para caber o caminho `<caminho Java>/base/fftpack.bin\0` na região estrutural observada de 260 bytes é:

```
B (bytes modificados UTF-8 de GetStringUTFChars)
 + 6 ("/base/")
 + 11 ("fftpack.bin")
 + 1 (NUL)
 <= 260
B <= 242
```

**Bytes JNI não são Java `String.length()` nem obrigatoriamente UTF-8 padrão.** O par `GetStringUTFLength` / `GetStringUTFChars` utiliza Modified UTF-8: U+0000 codifica `C0 80` (2 bytes), um caractere suplementar corresponde a dois surrogates UTF-16 com 3 bytes cada (6 bytes) e caracteres BMP podem ocupar 1–3 bytes.

## Gate realizado em JVM real (host)

A biblioteca nativa de teste `jni-path-probe/a04_jni_probe.c` usa JNI real do OpenJDK e invoca o modelo C independente `c-models/a04_rootpath_safe.c`, que aborta antes de escrever se a entrada tem mais de 242 bytes. O harness Java `A04JniByteProbe.java` cobre comprimentos ASCII 0–260, Unicode BMP, surrogate pairs, NUL Java e fronteira 242/243. O buffer nativo possui canário de 16 bytes além da região de 260 bytes e o teste verifica ausência de escrita além do resultado.

O workflow `re-a04-jni-mutf8-host.yml` testa JDK 17 e 21 e repete o relatório bit a bit. Isso **valida a regra de byte-length do JNI e os testes de segurança do modelo**, e não o comportamento do ELF original em execução no Android.

## Próximo gate no Android

1. Em dispositivo/emulador autorizado, obter o `Context` real da aplicação e chamar `StorageUtil.GetIntPath()` e `GetExt1Path()` sem contornar as regras do app.
2. Medir `GetStringUTFLength(jstring)` / a contagem efetiva de bytes modificados UTF-8, reportando valor, NUL/retorno nulo e situação de falha. **Não** executar a `strcpy` original com entrada de teste excessiva.
3. Testar em ambiente controlado os caminhos de 242 e 243 bytes e as condições de storage ausente, diferenças de API e retorno nulo. Os tamanhos de exemplos reais não constituem limite máximo universal.
4. Comparar os resultados com o campo de 260 bytes do `CAPP_INFO` e liberar certificado apenas para contratos e condições executados.

A04 continua `in_progress`. **0** amostras reais de Android nesta etapa e **0** certificados semânticos novos.
