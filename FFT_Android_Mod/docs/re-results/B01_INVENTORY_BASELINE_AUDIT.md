# B01 — auditoria de integridade do inventário e dos artefatos Android

**Estado:** B01 `in_progress`. Auditoria de consistência e proveniência, **não** certificação de funções ou conclusão do inventário end-to-end.

## Contagens da leitura dos CSVs versionados (30/10/2026)

| Métrica | Contagem | Interpretação |
|---|---:|---|
| Linhas do inventário principal | 6.455 | Registros de funções/entradas declarados |
| Endereços de entrada distintos | 6.329 | Chave de deduplicação: endereço ARM normalizado |
| Registros adicionais de endereço já existente | 126 | Aliases, não novas funções provadas |
| Endereços do inventário prioritário | 4.591 | Subconjunto do inventário principal |
| Ausentes/mismatches de tamanho no prioritário | 0 | Consistência declarativa CSV contra CSV |
| Pares de intervalos com sobreposição | 15 | Requerem classificação explícita; não contam duas vezes na união |

O cálculo dos 15 **pares** de sobreposição é estático sobre `[endereço, endereço + tamanho)`, não é prova de que todos sejam código executável ou funções equivalentes. Existem múltiplos pares dentro do mesmo conjunto de entradas internas. Exemplos: `0x002ca8a0/0x002ca8a4`, `0x002cb0c0/0x002cb0c8/0x002cb0d0`, `0x002cb2e8/0x002cb2f0/0x002cb2f4` e `0x002cb830/0x002cb838/0x002cb840`.

A soma de tamanhos não é cobertura de bytes: a ferramenta calcula a **união de intervalos declarados**, apresenta os conflitos e mantém cobertura executable/semântica como perguntas separadas.

## Proveniência e lacunas reais

- O ELF ARM de referência deve ser confirmado pelo SHA-256 `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc` e por cabeçalho ELF32 little-endian/ARM. A checagem é executável no CI; a presença do arquivo por nome **não** dispensa comparação de bytes.
- O diretório `FFT_Android_Mod/src/lib/` contém variantes `armeabi` e `x86`, que não devem ser somadas como funções do mesmo ELF.
- O diretório `src/smali` possui recursos rastreáveis por arquivos, mas ainda exige correlação de classes/métodos Java, JNI, símbolos nativos e dependências de execução.
- O arquivo `obb-data/main.202000.com.square_enix.android_googleplay.FFT_en2.obb` aparece no repositório como **ponteiro Git LFS de 134 bytes**, não como OBB materializado para inspeção de assets. A auditoria deve registrar isso como lacuna, sem fingir que o conteúdo do OBB foi analisado.
- A classificação de código vs dados, reachability, entrypoints Thumb, manifestos e recursos reais permanece aberta.

## Como reproduzir

```bash
python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools -p test_b01_inventory_audit.py -v
python3 FFT_Android_Mod/docs/re-tools/b01_inventory_audit.py --root . --output /tmp/b01-inventory-report.json
```

O workflow `.github/workflows/re-b01-inventory-audit.yml` testa as invariantes de regressão e publica JSON contendo apenas metadados e evidências derivadas dos arquivos rastreados. Não inicia Android, não executa ELF e não emite certificados semânticos.

## Próximos gates de B01

1. Confirmar no CI o hash e o cabeçalho ELF real e as contagens reproduzíveis de CSV; preservar SHA do relatório.
2. Classificar todos os grupos de intervalos sobrepostos como entrada interna, alias, objeto compartilhado ou inconsistência, com disassembly e referência ao ELF.
3. Materializar (em ambiente privado autorizado) e inventariar o conteúdo do OBB, incluindo hash, entradas, tamanhos e relação com o APK, sem publicar conteúdo de terceiros.
4. Criar vínculo auditável Smali `native`/Java → JNI `Java_*`/registro dinâmico → biblioteca ARM; documentar símbolos/rotinas não encontrados.
5. Produzir inventário único versionado de código/dados/recursos com lacunas e critérios de aceitação. Só então avaliar `B01=done`, desbloqueando formalmente A03/R01/R02.

**Regra:** B01 não se encerra apenas com a consistência dos CSVs ou um CI verde. `A04=in_progress` e nenhum certificado semântico novo é inferido deste relatório.
