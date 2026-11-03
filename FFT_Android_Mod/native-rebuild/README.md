# T32 — compilação nativa automatizada, estágio independente

**Status:** T32 não concluída. Esta entrega prepara o esqueleto de build e
verificação *host-only*; **não** gera uma `libgl2jni.so` substituta, não
implementa callbacks JNI e não instala nem executa o aplicativo.

## Componentes rastreados

O arquivo `module-map.json` liga **12 endereços ARM distintos** a
cinco fontes independentes atualmente existentes:

- B01: sete métodos C++ nominais;
- T14: fatia de `Boot_FrameMove`;
- T19: três funções `evt_flag_high`, `evt_flag_low`, `evt_flagset`;
- T22: fatia de `iOS_ResumeGetData`.

O CMake compila essas fontes numa biblioteca **estática de desenvolvimento**.
O smoke C++ verifica valores e offsets escritos por sete métodos B01,
preservação do restante do buffer, ponteiros nulos e tamanhos insuficientes.
O verificador `verify_stage.py` reprova mudanças na linha de base, fontes
sem proveniência, endereços duplicados e qualquer alegação de build completo.

```bash
python3 FFT_Android_Mod/native-rebuild/verify_stage.py
cmake -S FFT_Android_Mod/native-rebuild -B /tmp/fftcraft-stage -DCMAKE_BUILD_TYPE=Release
cmake --build /tmp/fftcraft-stage --parallel 2
ctest --test-dir /tmp/fftcraft-stage --output-on-failure
```

O workflow `.github/workflows/re-t32-native-stage.yml` roda em PRs
relevantes, pushes na `main` e manualmente. Ele não requisita LFS, OBB,
emulador Android, NDK ou segredos; tampouco distribui os binários do jogo.

## Gates pendentes para T32 `done`

1. Concluir contratos de tipos e fronteiras T08–T10 e fluxo T14;
2. Definir uma interface JNI **real** por método após inventário T27;
3. Produzir uma biblioteca Android por ABI relevante com o NDK a partir
   de código independente, com provas por função e dependências;
4. Integrar ao aplicativo controladamente sem mascarar delegações
   para o ELF original;
5. Obter build, instalação, inicialização e smoke Android reproduzíveis,
   com relatório das partes ainda não reimplementadas.

Um CI host verde comprova somente a compilação e os contratos locais
testados. A integração Android permanece *bloqueada* até os demais gates.
