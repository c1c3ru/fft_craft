# fft_craft

**[Acompanhar o progresso da engenharia reversa — STATUS_GERAL.md](FFT_Android_Mod/docs/re-results/STATUS_GERAL.md)**

O painel é regenerado pelo GitHub Actions após cada lote validado e distingue
aprovação estrutural de evidência semântica e de equivalência integral.

Projeto de modificação do **Final Fantasy Tactics: The War of the Lions** para Android
(pacote `com.square_enix.android_googleplay.FFT_en2`), incluindo engenharia reversa,
rebuild do APK e os binários/assets usados no processo.

> **Aviso:** este repositório contém binários do jogo original (APK, `.obb`) com fins
> de modificação pessoal/estudo. É um repositório privado — não redistribua esse
> conteúdo, que pertence à Square Enix.

## Estrutura

```
FFT_Android_Mod/    Projeto principal de modding (apktool, smali, scripts de build,
                    notas de engenharia reversa). Ver FFT_Android_Mod/README.md.
FFT By MortalGx.apk                                          APK de referência do mod.
com.square_enix.android_googleplay.FFT_en2_2.2.0-APK_Award-Mod.apk  APK original (2.2.0).
```

## Detalhes do mod

Toda a documentação do fluxo de trabalho (decode → editar smali/res → build → assinar →
instalar), requisitos de ambiente e achados da engenharia reversa (patch de licença,
correção de versão do OBB, limitações de libs nativas) estão em
[`FFT_Android_Mod/README.md`](FFT_Android_Mod/README.md) e
[`FFT_Android_Mod/docs/REVERSE_ENGINEERING_NOTES.md`](FFT_Android_Mod/docs/REVERSE_ENGINEERING_NOTES.md).

## Arquivos grandes (Git LFS)

Os arquivos abaixo (acima do limite de 100MB do GitHub) são versionados via Git LFS:

- `FFT_Android_Mod/com.square_enix.android_googleplay.FFT_en2.zip`
- `FFT_Android_Mod/obb-data/main.202000.com.square_enix.android_googleplay.FFT_en2.obb`

Clone com `git lfs install` configurado para baixá-los corretamente.
