.class public final Lcom/yox_project/silver_arrow/VibratorUtil;
.super Ljava/lang/Object;
.source "VibratorUtil.java"


# static fields
.field static final TAG:Ljava/lang/String; = "VibratorUtil"

.field private static pattern:[J

.field private static vib:Landroid/os/Vibrator;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .prologue
    .line 34
    const/4 v0, 0x6

    new-array v0, v0, [J

    fill-array-data v0, :array_0

    sput-object v0, Lcom/yox_project/silver_arrow/VibratorUtil;->pattern:[J

    return-void

    nop

    :array_0
    .array-data 8
        0x3e8
        0xc8
        0x2bc
        0xc8
        0x190
        0xc8
    .end array-data
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 26
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static Init(Landroid/content/Context;)V
    .locals 4
    .param p0, "hContext"    # Landroid/content/Context;

    .prologue
    .line 47
    :try_start_0
    const-string v1, "vibrator"

    invoke-virtual {p0, v1}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/os/Vibrator;

    sput-object v1, Lcom/yox_project/silver_arrow/VibratorUtil;->vib:Landroid/os/Vibrator;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 53
    :goto_0
    return-void

    .line 49
    :catch_0
    move-exception v0

    .line 51
    .local v0, "e":Ljava/lang/Exception;
    const-string v1, "VibratorUtil"

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Exception: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method public static IsExist()I
    .locals 4

    .prologue
    .line 122
    :try_start_0
    sget-object v1, Lcom/yox_project/silver_arrow/VibratorUtil;->vib:Landroid/os/Vibrator;

    invoke-virtual {v1}, Landroid/os/Vibrator;->hasVibrator()Z
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result v1

    if-eqz v1, :cond_0

    .line 125
    const/4 v1, 0x1

    .line 133
    .local v0, "e":Ljava/lang/Exception;
    :goto_0
    return v1

    .line 128
    .end local v0    # "e":Ljava/lang/Exception;
    :catch_0
    move-exception v0

    .line 130
    .restart local v0    # "e":Ljava/lang/Exception;
    const-string v1, "VibratorUtil"

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Exception: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    .line 133
    :cond_0
    const/4 v1, 0x0

    goto :goto_0
.end method

.method public static onStop()V
    .locals 4

    .prologue
    .line 102
    :try_start_0
    sget-object v1, Lcom/yox_project/silver_arrow/VibratorUtil;->vib:Landroid/os/Vibrator;

    invoke-virtual {v1}, Landroid/os/Vibrator;->cancel()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 108
    .local v0, "e":Ljava/lang/Exception;
    :goto_0
    return-void

    .line 104
    .end local v0    # "e":Ljava/lang/Exception;
    :catch_0
    move-exception v0

    .line 106
    .restart local v0    # "e":Ljava/lang/Exception;
    const-string v1, "VibratorUtil"

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Exception: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method public static onVibrate(I)V
    .locals 4
    .param p0, "time"    # I

    .prologue
    .line 65
    :try_start_0
    const-string v1, "VibratorUtil"

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "onVibrate: time = "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 66
    sget-object v1, Lcom/yox_project/silver_arrow/VibratorUtil;->vib:Landroid/os/Vibrator;

    int-to-long v2, p0

    invoke-virtual {v1, v2, v3}, Landroid/os/Vibrator;->vibrate(J)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 72
    :goto_0
    return-void

    .line 68
    :catch_0
    move-exception v0

    .line 70
    .local v0, "e":Ljava/lang/Exception;
    const-string v1, "VibratorUtil"

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Exception: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method public static onVibratePattern(I)V
    .locals 4
    .param p0, "flag"    # I

    .prologue
    .line 84
    :try_start_0
    sget-object v1, Lcom/yox_project/silver_arrow/VibratorUtil;->vib:Landroid/os/Vibrator;

    sget-object v2, Lcom/yox_project/silver_arrow/VibratorUtil;->pattern:[J

    invoke-virtual {v1, v2, p0}, Landroid/os/Vibrator;->vibrate([JI)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 90
    :goto_0
    return-void

    .line 86
    :catch_0
    move-exception v0

    .line 88
    .local v0, "e":Ljava/lang/Exception;
    const-string v1, "VibratorUtil"

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "Exception: "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v0}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method
