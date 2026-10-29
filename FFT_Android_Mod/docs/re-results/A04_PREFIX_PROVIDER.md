# A04 — Cadeia original do caminho do Android até fftpack.bin

ELF original `libgl2jni.so` SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`.

## Contratos reconstruídos no ELF original

1. `0x0020ca0c: BL 0x002b04f0` chama `CAPP_INFO::GetRootPath()`. Essa função ARM de **8 bytes** faz `ADD R0,R0,#0x98; BX LR`. O retorno é o ponteiro para o campo `CAPP_INFO+0x98`. A função-folha foi executada em Unicorn em **20 casos** de base/flags; zero divergências com o contrato de deslocamento, sem execução do inicializador nem leitura de string.
2. `CAPP_INFO::Init(int)` está em `0x002b052c`. Forma `R5=R4+0x98` e chama `Android_GetSystemPath(int,char*)`, em `0x000729e4`. O campo seguinte observado começa em `+0x19c`, diferença estrutural de **0x104=260 bytes**. Isto é evidência do layout, não prova de alocação em todos os caminhos.
3. `Android_GetSystemPath` monta seleção de **7 métodos Java** por tabela de relocations `R_ARM_RELATIVE` e usa índices de vtable JNI **169 e 170** (coerentes com obter/liberar caracteres UTF). A sequência ARM transfere o ponteiro devolvido por `BLX` para `R8`, usa `R1=R8`, `R0=R6` e chama o `strcpy` importado em `0x000714a0` (slot `0x00347d70`, `R_ARM_JUMP_SLOT`). **Não passa tamanho a strcpy** e a análise não identificou uma checagem de bytes do valor recebido nesse percurso.
4. A classe Java é `com/yox_project/silver_arrow/StorageUtil`, assinatura `()Ljava/lang/String;`. A tabela, seus sete ponteiros file-backed e as correspondentes relocations estão nos checkpoints `semantic_a04_java_path_lookup.py`.
5. No `CAPP_INFO::Init` examinado, o seletor **0** corresponde a `StorageUtil.GetIntPath()`, que usa `Context.getFilesDir().getPath()`. O seletor **1** corresponde a `StorageUtil.GetExt1Path()`, que usa `Context.getExternalFilesDir(null).getPath()`. O arquivo original `FFT_Android_Mod/src/smali/com/yox_project/silver_arrow/StorageUtil.smali` foi comparado automaticamente com a tabela JNI. Esses métodos não contêm limite explícito de bytes da string em seus próprios corpos. Há incertezas de disponibilidade do storage e comprimento real fornecido pelo sistema.
6. Ambos os caminhos do inicializador acrescentam o literal **`/base/\0` (7 bytes)** à posição `R5+strlen(R5)`, por meio de `memcpy` importado. As duas referências relativas apontam para `0x002df310` e as duas copiam os mesmos bytes `2f626173652f00`.
7. O callsite `0x0020ca48` copia o caminho do campo de RootPath para a pilha, mede seu comprimento e acrescenta o literal **`fftpack.bin\0` (12 bytes)** do endereço `0x002ddcc0`. O cálculo de endereço/argumentos foi executado em **36 casos ARM** no workflow de PR #447, sempre interrompendo antes da libc real.

## Limites de memória derivados, mas não validados no Android real

Se o caminho original recebido via Java/JNI tem comprimento **B bytes UTF modificados**, o buffer de RootPath após `/base/` ocupa `B + 6 + 1` bytes. Para caber no campo observado de 260 bytes, é necessário `B <= 253`.

No fluxo posterior de `fftpack.bin`, a mesma string recebe 11 bytes adicionais e NUL, usando uma região de 260 bytes anterior ao campo de guarda observado:

```text
B + 6 ("/base/") + 11 ("fftpack.bin") + 1 (NUL) <= 260
B <= 242 bytes
```

O NUL do sufixo `/base/` é sobrescrito pela concatenação do nome de arquivo. **Não** subtrair ambos os NULs como se ocupassem posições distintas. O limite se refere a **bytes da representação JNI**, não ao número de caracteres Java nem ao tamanho de um caminho típico de aplicativo.

O código original `strcpy` não verifica o comprimento do valor Java antes de copiar. Nenhuma evidência apresentada aqui comprova que o Android sempre devolva no máximo 242 bytes ou que as operações posteriores estejam protegidas contra falhas de alocação, ponteiro nulo ou string excessiva. Os achados são uma **pré-condição de segurança pendente**, não uma vulnerabilidade explorada ou uma prova de overflow observado.

## Testes, artefatos e status

- `semantic_a04_prefix_provider.py`: identidade de `GetRootPath`, símbolos, instruções.
- `semantic_a04_rootpath_field.py`: contrato de getter em ARM original, 20 execuções, instruções de inicialização.
- `semantic_a04_rootpath_helper.py`: corpo original de `Android_GetSystemPath`, chamadas JNI e branches.
- `semantic_a04_rootpath_jni_copy.py`: provas do `strcpy` importado e de ambos os literais `/base/`.
- `semantic_a04_java_path_lookup.py`: sete nomes de método e relocations da tabela.
- `semantic_a04_storageutil_contract.py`: liga os seletores 0/1 ao smali real e computa condição B <= 242.
- `re-a04-prefix-provider.yml`: gates determinísticos, checkpoints repetidos e artefato final.

**Próximo gate:** obter, em um ambiente Android instrumentado/autorizado, o comprimento em bytes UTF JNI dos caminhos retornados pelos métodos 0 e 1, registrar a condição B <= 242 nos cenários relevantes e testar em modo controlado o tratamento de valores excedentes e retornos nulos. O ideal é também adicionar uma API C segura de compatibilidade que recuse entrada excessiva antes da cópia, sem alegar que reproduz o comportamento indefinido do original.

**A04 permanece `in_progress`; nenhum certificado de equivalência completa ou segurança global foi emitido.**
