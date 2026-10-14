.class public final Lcom/square_enix/FFT_Android/BuildSettings;
.super Ljava/lang/Object;
.source "BuildSettings.java"


# static fields
.field public static final LVL_ENABLE:Z = true

.field public static final OBB_DOWNLOADER_ENABLE:Z = true

# ATENÇÃO: javac/dx faz constant-folding em campos "static final" primitivos
# e String. O valor abaixo NÃO é lido em runtime via sget - cada chamador
# já tem o literal embutido no próprio bytecode. Editar só aqui NÃO muda
# comportamento. Os pontos reais que controlam o nome/versão da OBB são:
#   - FileChkActivity.smali  -> expansionFilesDelivered() (método privado)
#   - GL2JNIActivity.smali   -> mountObbAll() e o literal de string próximo
# Mantido sincronizado aqui apenas para leitura/documentação.
.field public static final OBB_FILE:Ljava/lang/String; = "main.202000.com.square_enix.android_googleplay.FFT_en2.obb"

.field public static final OBB_VERSION:I = 0x31510

.field public static final OBB_VERSION_STR:Ljava/lang/String; = "202000"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 20
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method
