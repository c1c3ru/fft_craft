# T27 + T29 — auditoria automática da ponte JNI e do OBB

**Estado:** T27 e T29 continuam parciais e **não concluídas**. A
automação separa descoberta estática das evidências de runtime e de
materialização do arquivo de expansão.

## T27: Java/Smali e ABI JNI

A ferramenta `t27_t29_android_inventory.py` reutiliza o auditor
`b01_smali_jni_obb_audit.py` sem duplicar a decodificação ELF.
Cruza os **12 métodos declarados** por `GL2JNILib.smali` com:
- invocações Smali de assinatura exata e caminho/linha da fonte;
- candidatos a símbolos JNI na `.dynsym` do ELF ARM fixado por SHA;
- componentes de launcher, activities, services e receivers no manifest,
  com diagnóstico de presença da classe smali.

Nomes, exports e referências estáticas não demonstram registro de JNI,
chamada em runtime, consumidor de `getCommand` nem efeitos nativos.
O relatório deixa explicitamente todas essas provas como pendentes.
O restante das classes Smali, interfaces Java↔nativo, retorno Java↔JNI,
ciclo de vida e versão x86 ainda exigem investigação orientada por CFG
e instrumentação controlada.

## T29: ponteiro e integridade OBB sem gasto LFS

O workflow roda com `lfs: false`. Confere o ponteiro Git LFS de
**815.622.218 bytes** e OID
`ca56bc16ab20f0f395bf1bdb7651b0073698090d395ac76687dc1aabcca370e3`,
sem baixar nem publicar os dados do jogo.

Ponteiro íntegro **não** prova a presença dos bytes, FAT32, ZIP,
`fftpack.bin`, tipos de entradas ou round-trip de formatos.
O download permanece exclusivamente no workflow manual já existente
`re-b01-obb-lfs-manual.yml`, com consentimento explícito; no CI barato
`T29_ASSETS_CLASSIFIED=0` e `t29_done=false`.

## Execução local e CI

```bash
python -m pip install 'pyelftools==0.32'
python FFT_Android_Mod/docs/re-tools/t27_t29_android_inventory.py \
  --output /tmp/t27-t29-static-handoff.json
python -m unittest discover -s FFT_Android_Mod/docs/re-tools \
  -p 'test_t27_t29_android_inventory.py' -v
```

O workflow `re-t27-t29-android-bridge.yml` roda em mudanças do Smali,
manifest, ponteiro OBB, auditor ou ELF ARM e por disparo manual.
Seu artefato é apenas **JSON de metadados**, nunca APK, OBB ou código
proprietário bruto.

**Gates T27/T29 restantes:** completar o mapa bidirecional
Java↔JNI e efeitos por método no processo autorizado do jogo,
identificar/extrair e remontar cada classe de entrada OBB com
verificação de bytes, e provar integração Android end-to-end.
Essas etapas continuam abertas até haver ambientes e dados verificados.
