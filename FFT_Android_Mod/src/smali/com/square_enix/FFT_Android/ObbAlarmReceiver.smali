.class public Lcom/square_enix/FFT_Android/ObbAlarmReceiver;
.super Landroid/content/BroadcastReceiver;
.source "ObbAlarmReceiver.java"


# static fields
.field static final TAG:Ljava/lang/String; = "ObbAlarmReceiver"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 30
    invoke-direct {p0}, Landroid/content/BroadcastReceiver;-><init>()V

    return-void
.end method


# virtual methods
.method public onReceive(Landroid/content/Context;Landroid/content/Intent;)V
    .locals 3
    .param p1, "context"    # Landroid/content/Context;
    .param p2, "intent"    # Landroid/content/Intent;

    .prologue
    .line 39
    :try_start_0
    const-string v1, "ObbAlarmReceiver"

    const-string v2, "onReceive"

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 41
    const-class v1, Lcom/square_enix/FFT_Android/ObbDownloaderService;

    invoke-static {p1, p2, v1}, Lcom/google/android/vending/expansion/downloader/DownloaderClientMarshaller;->startDownloadServiceIfRequired(Landroid/content/Context;Landroid/content/Intent;Ljava/lang/Class;)I
    :try_end_0
    .catch Landroid/content/pm/PackageManager$NameNotFoundException; {:try_start_0 .. :try_end_0} :catch_0

    .line 47
    :goto_0
    return-void

    .line 43
    :catch_0
    move-exception v0

    .line 45
    .local v0, "e":Landroid/content/pm/PackageManager$NameNotFoundException;
    invoke-virtual {v0}, Landroid/content/pm/PackageManager$NameNotFoundException;->printStackTrace()V

    goto :goto_0
.end method
