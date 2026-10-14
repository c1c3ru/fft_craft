.class public Lcom/square_enix/FFT_Android/LicenseCheckerActivity;
.super Landroid/app/Activity;
.source "LicenseCheckerActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;
    }
.end annotation


# static fields
.field private static final TAG:Ljava/lang/String; = "LicenseCheckerActivity"


# instance fields
.field private mChecker:Lcom/google/android/vending/licensing/LicenseChecker;

.field private mHandler:Landroid/os/Handler;

.field private mLicenseCheckerCallback:Lcom/google/android/vending/licensing/LicenseCheckerCallback;

.field private mThread:Ljava/lang/Thread;

.field private m_iResult:I

.field private m_isExit:Z


# direct methods
.method public constructor <init>()V
    .locals 1

    .prologue
    const/4 v0, 0x0

    .line 74
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 82
    iput-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mThread:Ljava/lang/Thread;

    .line 83
    iput-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mHandler:Landroid/os/Handler;

    .line 84
    const/4 v0, 0x0

    iput-boolean v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_isExit:Z

    .line 85
    const/16 v0, 0x65

    iput v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_iResult:I

    .line 74
    return-void
.end method

.method static synthetic access$0(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;I)V
    .locals 0

    .prologue
    .line 85
    iput p1, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_iResult:I

    return-void
.end method

.method static synthetic access$1(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;Z)V
    .locals 0

    .prologue
    .line 84
    iput-boolean p1, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_isExit:Z

    return-void
.end method

.method private doCheck()V
    .locals 2

    .prologue
    .line 376
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mChecker:Lcom/google/android/vending/licensing/LicenseChecker;

    iget-object v1, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mLicenseCheckerCallback:Lcom/google/android/vending/licensing/LicenseCheckerCallback;

    invoke-virtual {v0, v1}, Lcom/google/android/vending/licensing/LicenseChecker;->checkAccess(Lcom/google/android/vending/licensing/LicenseCheckerCallback;)V

    .line 377
    return-void
.end method


# virtual methods
.method public onCreate(Landroid/os/Bundle;)V
    .locals 7
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .prologue
    .line 102
    const-string v2, "LicenseCheckerActivity"

    const-string v3, "onCreate ----------------------------------------"

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 103
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 107
    const/high16 v2, 0x7f030000

    invoke-virtual {p0, v2}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->setContentView(I)V

    .line 111
    const/4 v2, 0x0

    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_isExit:Z

    .line 112
    const/16 v2, 0x65

    iput v2, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_iResult:I

    .line 113
    iget-object v2, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mHandler:Landroid/os/Handler;

    if-nez v2, :cond_0

    .line 115
    new-instance v2, Landroid/os/Handler;

    invoke-direct {v2}, Landroid/os/Handler;-><init>()V

    iput-object v2, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mHandler:Landroid/os/Handler;

    .line 117
    :cond_0
    iget-object v2, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mThread:Ljava/lang/Thread;

    if-nez v2, :cond_1

    .line 120
    new-instance v2, Ljava/lang/Thread;

    invoke-direct {v2, p0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;)V

    iput-object v2, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mThread:Ljava/lang/Thread;

    .line 121
    iget-object v2, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mThread:Ljava/lang/Thread;

    invoke-virtual {v2}, Ljava/lang/Thread;->start()V

    .line 123
    :cond_1
    invoke-static {p0}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->Init(Landroid/content/Context;)V

    .line 135
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getContentResolver()Landroid/content/ContentResolver;

    move-result-object v2

    const-string v3, "android_id"

    invoke-static {v2, v3}, Landroid/provider/Settings$Secure;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 138
    .local v0, "deviceId":Ljava/lang/String;
    new-instance v2, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;

    const/4 v3, 0x0

    invoke-direct {v2, p0, v3}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;-><init>(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;)V

    iput-object v2, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mLicenseCheckerCallback:Lcom/google/android/vending/licensing/LicenseCheckerCallback;

    .line 140
    new-instance v1, Lcom/square_enix/FFT_Android/ObbDownloaderService;

    invoke-direct {v1}, Lcom/square_enix/FFT_Android/ObbDownloaderService;-><init>()V

    .line 141
    .local v1, "mDownloaderService":Lcom/square_enix/FFT_Android/ObbDownloaderService;
    new-instance v2, Lcom/google/android/vending/licensing/LicenseChecker;

    .line 144
    new-instance v3, Lcom/google/android/vending/licensing/ServerManagedPolicy;

    .line 145
    new-instance v4, Lcom/google/android/vending/licensing/AESObfuscator;

    invoke-virtual {v1}, Lcom/square_enix/FFT_Android/ObbDownloaderService;->getSALT()[B

    move-result-object v5

    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getPackageName()Ljava/lang/String;

    move-result-object v6

    invoke-direct {v4, v5, v6, v0}, Lcom/google/android/vending/licensing/AESObfuscator;-><init>([BLjava/lang/String;Ljava/lang/String;)V

    .line 144
    invoke-direct {v3, p0, v4}, Lcom/google/android/vending/licensing/ServerManagedPolicy;-><init>(Landroid/content/Context;Lcom/google/android/vending/licensing/Obfuscator;)V

    .line 147
    invoke-virtual {v1}, Lcom/square_enix/FFT_Android/ObbDownloaderService;->getPublicKey()Ljava/lang/String;

    move-result-object v4

    invoke-direct {v2, p0, v3, v4}, Lcom/google/android/vending/licensing/LicenseChecker;-><init>(Landroid/content/Context;Lcom/google/android/vending/licensing/Policy;Ljava/lang/String;)V

    .line 141
    iput-object v2, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mChecker:Lcom/google/android/vending/licensing/LicenseChecker;

    .line 149
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->doCheck()V

    .line 150
    return-void
.end method

.method protected onDestroy()V
    .locals 2

    .prologue
    .line 334
    const-string v0, "LicenseCheckerActivity"

    const-string v1, "onDestroy"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 335
    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V

    .line 336
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mChecker:Lcom/google/android/vending/licensing/LicenseChecker;

    invoke-virtual {v0}, Lcom/google/android/vending/licensing/LicenseChecker;->onDestroy()V

    .line 337
    return-void
.end method

.method protected onPause()V
    .locals 2

    .prologue
    .line 302
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->isFinishing()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 308
    const-string v0, "LicenseCheckerActivity"

    const-string v1, "onPause (finishing)"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 314
    :goto_0
    invoke-super {p0}, Landroid/app/Activity;->onPause()V

    .line 315
    return-void

    .line 312
    :cond_0
    const-string v0, "LicenseCheckerActivity"

    const-string v1, "onPause"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method protected onRestart()V
    .locals 2

    .prologue
    .line 264
    const-string v0, "LicenseCheckerActivity"

    const-string v1, "onRestart ---------------------------------------"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 265
    invoke-super {p0}, Landroid/app/Activity;->onRestart()V

    .line 266
    return-void
.end method

.method protected onResume()V
    .locals 2

    .prologue
    .line 289
    const-string v0, "LicenseCheckerActivity"

    const-string v1, "onResume"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 290
    invoke-super {p0}, Landroid/app/Activity;->onResume()V

    .line 291
    return-void
.end method

.method protected onStart()V
    .locals 2

    .prologue
    .line 277
    const-string v0, "LicenseCheckerActivity"

    const-string v1, "onStart"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 278
    invoke-super {p0}, Landroid/app/Activity;->onStart()V

    .line 279
    return-void
.end method

.method protected onStop()V
    .locals 2

    .prologue
    .line 326
    const-string v0, "LicenseCheckerActivity"

    const-string v1, "onStop"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 327
    invoke-super {p0}, Landroid/app/Activity;->onStop()V

    .line 328
    return-void
.end method

.method public run()V
    .locals 6

    .prologue
    .line 161
    const-string v4, "LicenseCheckerActivity"

    const-string v5, "run"

    invoke-static {v4, v5}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 162
    :goto_0
    iget-boolean v4, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_isExit:Z

    if-eqz v4, :cond_1

    .line 231
    const-string v4, "LicenseCheckerActivity"

    const-string v5, "run - exit"

    invoke-static {v4, v5}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 235
    iget v4, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_iResult:I

    const/16 v5, 0x64

    if-ne v4, v5, :cond_0

    .line 239
    new-instance v3, Landroid/content/Intent;

    const-class v4, Lcom/square_enix/FFT_Android/FileChkActivity;

    invoke-direct {v3, p0, v4}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 240
    .local v3, "intent":Landroid/content/Intent;
    const/16 v4, 0xb

    invoke-virtual {p0, v3, v4}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->startActivityForResult(Landroid/content/Intent;I)V

    .line 253
    .end local v3    # "intent":Landroid/content/Intent;
    :cond_0
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->finish()V

    .line 254
    return-void

    .line 168
    :cond_1
    :try_start_0
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->GetRequest()I

    move-result v4

    if-eqz v4, :cond_3

    .line 176
    const/4 v4, 0x0

    invoke-static {v4}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->SetRequest(I)V

    .line 179
    const-string v4, "LicenseCheckerActivity"

    const-string v5, "mHandler.post"

    invoke-static {v4, v5}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 180
    iget-object v4, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->mHandler:Landroid/os/Handler;

    .line 181
    new-instance v5, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$1;

    invoke-direct {v5, p0}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$1;-><init>(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;)V

    .line 180
    invoke-virtual {v4, v5}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_1

    .line 224
    :cond_2
    :goto_1
    const-wide/16 v4, 0x64

    :try_start_1
    invoke-static {v4, v5}, Ljava/lang/Thread;->sleep(J)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    goto :goto_0

    .line 226
    :catch_0
    move-exception v0

    .line 228
    .local v0, "e":Ljava/lang/Exception;
    const-string v4, "LicenseCheckerActivity"

    const-string v5, "Exception: "

    invoke-static {v4, v5}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0

    .line 193
    .end local v0    # "e":Ljava/lang/Exception;
    :cond_3
    :try_start_2
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->GetID()I

    move-result v1

    .line 194
    .local v1, "iID":I
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->GetResult()I

    move-result v2

    .line 197
    .local v2, "iResult":I
    const/4 v4, -0x1

    if-eq v2, v4, :cond_2

    .line 200
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->Close()V

    .line 203
    packed-switch v1, :pswitch_data_0

    goto :goto_1

    .line 207
    :pswitch_0
    const/16 v4, 0x65

    iput v4, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_iResult:I

    .line 208
    const/4 v4, 0x1

    iput-boolean v4, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->m_isExit:Z
    :try_end_2
    .catch Ljava/lang/Exception; {:try_start_2 .. :try_end_2} :catch_1

    goto :goto_1

    .line 216
    .end local v1    # "iID":I
    .end local v2    # "iResult":I
    :catch_1
    move-exception v0

    .line 218
    .restart local v0    # "e":Ljava/lang/Exception;
    const-string v4, "LicenseCheckerActivity"

    const-string v5, "Exception: "

    invoke-static {v4, v5}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_1

    .line 203
    nop

    :pswitch_data_0
    .packed-switch 0x3e6
        :pswitch_0
    .end packed-switch
.end method
