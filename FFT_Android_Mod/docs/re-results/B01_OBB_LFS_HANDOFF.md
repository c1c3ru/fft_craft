# B01 — verificação do OBB Git LFS sob autorização explícita

**Estado:** pendente de materialização; não concluir B01 sem comprovar o conteúdo real. O arquivo versionado em `obb-data` é um ponteiro Git LFS de **134 bytes**. Ele declara `size 815622218` e `oid sha256 ca56bc16ab20f0f395bf1bdb7651b0073698090d395ac76687dc1aabcca370e3`, valores que ainda não demonstram integridade do arquivo grande.

## Workflow de custo controlado

`.github/workflows/re-b01-obb-lfs-manual.yml`

- Em um PR, roda **somente** a verificação barata do ponteiro (sem transferência LFS).
- A etapa de materialização tem gatilho exclusivamente `workflow_dispatch`; exige selecionar explicitamente `DOWNLOAD_815622218_BYTES`, em lugar do padrão `NO`.
- A execução manual transfere **somente esse arquivo LFS**, compara tamanho e SHA-256 e escreve um relatório JSON de metadados.
- Se o arquivo for ZIP, lê apenas o diretório central (quantidade de entradas, tamanhos declarados), sem extração, CRC completo ou nomes publicados. Se não for ZIP, informa `unknown_not_zip`.
- O workflow **não** envia o OBB real como artifact; apenas `b01-obb-integrity-only.json`. Não executa APK, JNI nem ELF e não libera certificados semânticos.

**Custos e acesso:** a transferência pode consumir tráfego LFS e minutos do GitHub Actions. Conferir permissões e franquia/cobrança antes de iniciar manualmente. Não usar o job em agendamentos ou em cinco workers.

## Critério posterior

Depois da integridade, correlacionar a estrutura do OBB às rotinas reais de leitura no ELF/Smali, documentando recursos/entradas e chamadas ainda desconhecidos, sem publicar material de terceiros. Um hash válido e diretório ZIP não estabelecem cobertura completa nem equivalência funcional do jogo. B01 continua `in_progress` e A03/R01/R02 ainda aguardam seu aceite.
