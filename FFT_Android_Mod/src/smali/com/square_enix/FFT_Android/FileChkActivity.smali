.class public Lcom/square_enix/FFT_Android/FileChkActivity;
.super Landroid/app/Activity;
.source "FileChkActivity.java"

# interfaces
.implements Lcom/google/android/vending/expansion/downloader/IDownloaderClient;


# static fields
.field static final TAG:Ljava/lang/String; = "FileChkActivity"


# instance fields
.field private exec_flag:Z

.field private lock:Landroid/os/PowerManager$WakeLock;

.field private m_AlertDialog:Landroid/app/AlertDialog$Builder;

.field private m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

.field private m_ProgressDialog:Landroid/app/ProgressDialog;

.field private m_RemoteService:Lcom/google/android/vending/expansion/downloader/IDownloaderService;

.field private pm:Landroid/os/PowerManager;


# direct methods
.method public constructor <init>()V
    .locals 1

    .prologue
    const/4 v0, 0x0

    .line 43
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 54
    iput-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    .line 62
    iput-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    .line 64
    iput-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_AlertDialog:Landroid/app/AlertDialog$Builder;

    .line 66
    const/4 v0, 0x0

    iput-boolean v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->exec_flag:Z

    .line 43
    return-void
.end method

.method private expansionFilesDelivered()Z
    .locals 7

    .prologue
    .line 224
    invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;

    move-result-object v0

    .line 225
    .local v0, "exdir":Ljava/io/File;
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    .line 226
    .local v4, "sb":Ljava/lang/StringBuilder;
    invoke-virtual {v0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 227
    const-string v5, "/Android/obb/"

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 228
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->getPackageName()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 229
    const-string v5, "/"

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 231
    const/4 v1, 0x0

    .line 234
    .local v1, "is_file1":Z
    const/4 v5, 0x1

    const v6, 0x31510

    invoke-static {p0, v5, v6}, Lcom/google/android/vending/expansion/downloader/Helpers;->getExpansionAPKFileName(Landroid/content/Context;ZI)Ljava/lang/String;

    move-result-object v3

    .line 235
    .local v3, "obb_main_file_name":Ljava/lang/String;
    new-instance v2, Ljava/io/File;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v6

    invoke-static {v6}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v6

    invoke-direct {v5, v6}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v5, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-direct {v2, v5}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 236
    .local v2, "main_file":Ljava/io/File;
    invoke-virtual {v2}, Ljava/io/File;->exists()Z

    move-result v5

    if-eqz v5, :cond_0

    const/4 v1, 0x1

    .line 243
    :cond_0
    return v1
.end method

.method private failedDialog()V
    .locals 3

    .prologue
    .line 286
    const-string v0, "FileChkActivity"

    const-string v1, "failedDialog"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 288
    new-instance v0, Landroid/app/AlertDialog$Builder;

    invoke-direct {v0, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_AlertDialog:Landroid/app/AlertDialog$Builder;

    .line 289
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_AlertDialog:Landroid/app/AlertDialog$Builder;

    const v1, 0x7f040017

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setTitle(I)Landroid/app/AlertDialog$Builder;

    .line 290
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_AlertDialog:Landroid/app/AlertDialog$Builder;

    const v1, 0x7f04002e

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setMessage(I)Landroid/app/AlertDialog$Builder;

    .line 291
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_AlertDialog:Landroid/app/AlertDialog$Builder;

    const-string v1, "OK"

    new-instance v2, Lcom/square_enix/FFT_Android/FileChkActivity$1;

    invoke-direct {v2, p0}, Lcom/square_enix/FFT_Android/FileChkActivity$1;-><init>(Lcom/square_enix/FFT_Android/FileChkActivity;)V

    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    .line 299
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_AlertDialog:Landroid/app/AlertDialog$Builder;

    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;

    .line 300
    return-void
.end method

.method private initializeDownloadUI()V
    .locals 5

    .prologue
    const/4 v4, 0x0

    .line 248
    const-string v1, "FileChkActivity"

    const-string v2, "initializeDownloadUI"

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 250
    iget-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    if-nez v1, :cond_0

    .line 252
    const-class v1, Lcom/square_enix/FFT_Android/ObbDownloaderService;

    invoke-static {p0, v1}, Lcom/google/android/vending/expansion/downloader/DownloaderClientMarshaller;->CreateStub(Lcom/google/android/vending/expansion/downloader/IDownloaderClient;Ljava/lang/Class;)Lcom/google/android/vending/expansion/downloader/IStub;

    move-result-object v1

    iput-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    .line 255
    const-wide/16 v2, 0x64

    :try_start_0
    invoke-static {v2, v3}, Ljava/lang/Thread;->sleep(J)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 262
    :cond_0
    :goto_0
    const v1, 0x7f030001

    invoke-virtual {p0, v1}, Lcom/square_enix/FFT_Android/FileChkActivity;->setContentView(I)V

    .line 271
    iget-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    if-nez v1, :cond_1

    .line 273
    new-instance v1, Landroid/app/ProgressDialog;

    invoke-direct {v1, p0}, Landroid/app/ProgressDialog;-><init>(Landroid/content/Context;)V

    iput-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    .line 274
    iget-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    const v2, 0x7f04002d

    invoke-virtual {p0, v2}, Lcom/square_enix/FFT_Android/FileChkActivity;->getString(I)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Landroid/app/ProgressDialog;->setTitle(Ljava/lang/CharSequence;)V

    .line 276
    iget-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    const/4 v2, 0x1

    invoke-virtual {v1, v2}, Landroid/app/ProgressDialog;->setProgressStyle(I)V

    .line 277
    iget-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    invoke-virtual {v1, v4}, Landroid/app/ProgressDialog;->setMax(I)V

    .line 278
    iget-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    invoke-virtual {v1, v4}, Landroid/app/ProgressDialog;->incrementProgressBy(I)V

    .line 279
    iget-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    invoke-virtual {v1, v4}, Landroid/app/ProgressDialog;->setCancelable(Z)V

    .line 281
    :cond_1
    iget-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    invoke-virtual {v1}, Landroid/app/ProgressDialog;->show()V

    .line 282
    return-void

    .line 257
    :catch_0
    move-exception v0

    .line 259
    .local v0, "e":Ljava/lang/Exception;
    const-string v1, "FileChkActivity"

    const-string v2, "Exception: "

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method


# virtual methods
.method public abort()V
    .locals 2

    .prologue
    .line 207
    const-string v0, "FileChkActivity"

    const-string v1, "abort"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 208
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    if-eqz v0, :cond_0

    .line 210
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    invoke-interface {v0, p0}, Lcom/google/android/vending/expansion/downloader/IStub;->disconnect(Landroid/content/Context;)V

    .line 212
    :cond_0
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    if-eqz v0, :cond_1

    .line 214
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    invoke-virtual {v0}, Landroid/app/ProgressDialog;->dismiss()V

    .line 215
    const/4 v0, 0x0

    iput-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    .line 218
    :cond_1
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->finish()V

    .line 219
    return-void
.end method

.method public execute()V
    .locals 2

    .prologue
    .line 190
    const-string v0, "FileChkActivity"

    const-string v1, "execute"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 192
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    if-eqz v0, :cond_0

    .line 194
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    invoke-virtual {v0}, Landroid/app/ProgressDialog;->dismiss()V

    .line 195
    const/4 v0, 0x0

    iput-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    .line 199
    :cond_0
    new-instance v0, Landroid/content/Intent;

    const-class v1, Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/FileChkActivity;->startActivity(Landroid/content/Intent;)V

    .line 202
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->finish()V

    .line 203
    return-void
.end method

.method public onCreate(Landroid/os/Bundle;)V
    .locals 8
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .prologue
    .line 72
    const-string v6, "FileChkActivity"

    const-string v7, "onCreate"

    invoke-static {v6, v7}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 73
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 76
    const-string v6, "power"

    invoke-virtual {p0, v6}, Lcom/square_enix/FFT_Android/FileChkActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v6

    check-cast v6, Landroid/os/PowerManager;

    iput-object v6, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->pm:Landroid/os/PowerManager;

    .line 78
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->initializeDownloadUI()V

    .line 80
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->expansionFilesDelivered()Z

    move-result v6

    if-nez v6, :cond_3

    .line 84
    :try_start_0
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->getIntent()Landroid/content/Intent;

    move-result-object v3

    .line 85
    .local v3, "launchIntent":Landroid/content/Intent;
    new-instance v2, Landroid/content/Intent;

    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v6

    invoke-direct {v2, p0, v6}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    .line 86
    .local v2, "intentToLaunchThisActivityFromNotification":Landroid/content/Intent;
    const/high16 v6, 0x14000000

    invoke-virtual {v2, v6}, Landroid/content/Intent;->setFlags(I)Landroid/content/Intent;

    .line 87
    invoke-virtual {v3}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v2, v6}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;

    .line 89
    invoke-virtual {v3}, Landroid/content/Intent;->getCategories()Ljava/util/Set;

    move-result-object v6

    if-eqz v6, :cond_0

    .line 91
    invoke-virtual {v3}, Landroid/content/Intent;->getCategories()Ljava/util/Set;

    move-result-object v6

    invoke-interface {v6}, Ljava/util/Set;->iterator()Ljava/util/Iterator;

    move-result-object v6

    :goto_0
    invoke-interface {v6}, Ljava/util/Iterator;->hasNext()Z

    move-result v7

    if-nez v7, :cond_2

    .line 98
    :cond_0
    const/4 v6, 0x0

    .line 99
    const/high16 v7, 0x8000000

    .line 97
    invoke-static {p0, v6, v2, v7}, Landroid/app/PendingIntent;->getActivity(Landroid/content/Context;ILandroid/content/Intent;I)Landroid/app/PendingIntent;

    move-result-object v4

    .line 102
    .local v4, "pendingIntent":Landroid/app/PendingIntent;
    const-class v6, Lcom/square_enix/FFT_Android/ObbDownloaderService;

    .line 101
    invoke-static {p0, v4, v6}, Lcom/google/android/vending/expansion/downloader/DownloaderClientMarshaller;->startDownloadServiceIfRequired(Landroid/content/Context;Landroid/app/PendingIntent;Ljava/lang/Class;)I

    move-result v5

    .line 104
    .local v5, "startResult":I
    if-eqz v5, :cond_1

    .line 108
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->initializeDownloadUI()V

    .line 124
    .end local v2    # "intentToLaunchThisActivityFromNotification":Landroid/content/Intent;
    .end local v3    # "launchIntent":Landroid/content/Intent;
    .end local v4    # "pendingIntent":Landroid/app/PendingIntent;
    .end local v5    # "startResult":I
    :cond_1
    :goto_1
    return-void

    .line 91
    .restart local v2    # "intentToLaunchThisActivityFromNotification":Landroid/content/Intent;
    .restart local v3    # "launchIntent":Landroid/content/Intent;
    :cond_2
    invoke-interface {v6}, Ljava/util/Iterator;->next()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    .line 93
    .local v0, "category":Ljava/lang/String;
    invoke-virtual {v2, v0}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;
    :try_end_0
    .catch Landroid/content/pm/PackageManager$NameNotFoundException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 113
    .end local v0    # "category":Ljava/lang/String;
    .end local v2    # "intentToLaunchThisActivityFromNotification":Landroid/content/Intent;
    .end local v3    # "launchIntent":Landroid/content/Intent;
    :catch_0
    move-exception v1

    .line 115
    .local v1, "e":Landroid/content/pm/PackageManager$NameNotFoundException;
    const-string v6, "FileChkActivity"

    const-string v7, "Cannot find own package! MAYDAY!"

    invoke-static {v6, v7}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    .line 116
    invoke-virtual {v1}, Landroid/content/pm/PackageManager$NameNotFoundException;->printStackTrace()V

    goto :goto_1

    .line 121
    .end local v1    # "e":Landroid/content/pm/PackageManager$NameNotFoundException;
    :cond_3
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->execute()V

    goto :goto_1
.end method

.method protected onDestroy()V
    .locals 2

    .prologue
    .line 183
    const-string v0, "FileChkActivity"

    const-string v1, "onDestroy"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 184
    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V

    .line 185
    return-void
.end method

.method public onDownloadProgress(Lcom/google/android/vending/expansion/downloader/DownloadProgressInfo;)V
    .locals 5
    .param p1, "progress"    # Lcom/google/android/vending/expansion/downloader/DownloadProgressInfo;

    .prologue
    const/high16 v4, 0x44800000    # 1024.0f

    .line 407
    const-string v0, "FileChkActivity"

    const-string v1, "onDownloadProgress"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 409
    iget-wide v0, p1, Lcom/google/android/vending/expansion/downloader/DownloadProgressInfo;->mOverallTotal:J

    iput-wide v0, p1, Lcom/google/android/vending/expansion/downloader/DownloadProgressInfo;->mOverallTotal:J

    .line 411
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    iget-wide v2, p1, Lcom/google/android/vending/expansion/downloader/DownloadProgressInfo;->mOverallTotal:J

    long-to-float v1, v2

    div-float/2addr v1, v4

    float-to-int v1, v1

    invoke-virtual {v0, v1}, Landroid/app/ProgressDialog;->setMax(I)V

    .line 412
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    iget-wide v2, p1, Lcom/google/android/vending/expansion/downloader/DownloadProgressInfo;->mOverallProgress:J

    long-to-float v1, v2

    div-float/2addr v1, v4

    float-to-int v1, v1

    invoke-virtual {v0, v1}, Landroid/app/ProgressDialog;->setProgress(I)V

    .line 414
    return-void
.end method

.method public onDownloadStateChanged(I)V
    .locals 6
    .param p1, "newState"    # I

    .prologue
    .line 316
    const-string v3, "FileChkActivity"

    new-instance v4, Ljava/lang/StringBuilder;

    const-string v5, "onDownloadStateChanged: "

    invoke-direct {v4, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {p1}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 318
    const/4 v2, 0x1

    .line 321
    .local v2, "showDashboard":Z
    packed-switch p1, :pswitch_data_0

    .line 389
    :pswitch_0
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.default"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 390
    const/4 v1, 0x1

    .line 391
    .local v1, "paused":Z
    const/4 v0, 0x1

    .line 392
    .local v0, "indeterminate":Z
    const/4 v2, 0x1

    .line 401
    :goto_0
    iget-object v3, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    invoke-virtual {v3, v0}, Landroid/app/ProgressDialog;->setIndeterminate(Z)V

    .line 402
    :goto_1
    return-void

    .line 324
    .end local v0    # "indeterminate":Z
    .end local v1    # "paused":Z
    :pswitch_1
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_IDLE"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 327
    const/4 v1, 0x0

    .line 328
    .restart local v1    # "paused":Z
    const/4 v0, 0x1

    .line 329
    .restart local v0    # "indeterminate":Z
    goto :goto_0

    .line 331
    .end local v0    # "indeterminate":Z
    .end local v1    # "paused":Z
    :pswitch_2
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_CONNECTING"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 333
    :pswitch_3
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_FETCHING_URL"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 334
    const/4 v2, 0x1

    .line 335
    const/4 v1, 0x0

    .line 336
    .restart local v1    # "paused":Z
    const/4 v0, 0x1

    .line 337
    .restart local v0    # "indeterminate":Z
    goto :goto_0

    .line 339
    .end local v0    # "indeterminate":Z
    .end local v1    # "paused":Z
    :pswitch_4
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_DOWNLOADING"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 340
    const/4 v1, 0x0

    .line 341
    .restart local v1    # "paused":Z
    const/4 v2, 0x1

    .line 342
    const/4 v0, 0x0

    .line 343
    .restart local v0    # "indeterminate":Z
    goto :goto_0

    .line 346
    .end local v0    # "indeterminate":Z
    .end local v1    # "paused":Z
    :pswitch_5
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_FAILED_CANCELED"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 348
    :pswitch_6
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_FAILED"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 350
    :pswitch_7
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_FAILED_FETCHING_URL"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 352
    :pswitch_8
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_FAILED_UNLICENSED"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 353
    const/4 v1, 0x1

    .line 354
    .restart local v1    # "paused":Z
    const/4 v2, 0x0

    .line 355
    const/4 v0, 0x0

    .line 356
    .restart local v0    # "indeterminate":Z
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->failedDialog()V

    goto :goto_0

    .line 359
    .end local v0    # "indeterminate":Z
    .end local v1    # "paused":Z
    :pswitch_9
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_PAUSED_NEED_CELLULAR_PERMISSION"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 361
    :pswitch_a
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_PAUSED_WIFI_DISABLED_NEED_CELLULAR_PERMISSION"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 362
    const/4 v2, 0x0

    .line 363
    const/4 v1, 0x1

    .line 364
    .restart local v1    # "paused":Z
    const/4 v0, 0x0

    .line 365
    .restart local v0    # "indeterminate":Z
    goto :goto_0

    .line 368
    .end local v0    # "indeterminate":Z
    .end local v1    # "paused":Z
    :pswitch_b
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_PAUSED_BY_REQUEST"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 369
    const/4 v1, 0x1

    .line 370
    .restart local v1    # "paused":Z
    const/4 v0, 0x0

    .line 371
    .restart local v0    # "indeterminate":Z
    goto :goto_0

    .line 373
    .end local v0    # "indeterminate":Z
    .end local v1    # "paused":Z
    :pswitch_c
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_PAUSED_ROAMING"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 375
    :pswitch_d
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_PAUSED_SDCARD_UNAVAILABLE"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 376
    const/4 v1, 0x1

    .line 377
    .restart local v1    # "paused":Z
    const/4 v0, 0x0

    .line 378
    .restart local v0    # "indeterminate":Z
    goto :goto_0

    .line 380
    .end local v0    # "indeterminate":Z
    .end local v1    # "paused":Z
    :pswitch_e
    const-string v3, "FileChkActivity"

    const-string v4, "    IDownloaderClient.STATE_COMPLETED"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 381
    const/4 v2, 0x0

    .line 382
    const/4 v1, 0x0

    .line 383
    .restart local v1    # "paused":Z
    const/4 v0, 0x0

    .line 385
    .restart local v0    # "indeterminate":Z
    iget-object v3, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->pm:Landroid/os/PowerManager;

    invoke-virtual {v3}, Landroid/os/PowerManager;->isScreenOn()Z

    move-result v3

    if-eqz v3, :cond_0

    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->execute()V

    .line 386
    :cond_0
    const/4 v3, 0x1

    iput-boolean v3, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->exec_flag:Z

    goto/16 :goto_1

    .line 321
    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_3
        :pswitch_2
        :pswitch_4
        :pswitch_e
        :pswitch_0
        :pswitch_b
        :pswitch_a
        :pswitch_9
        :pswitch_0
        :pswitch_0
        :pswitch_c
        :pswitch_0
        :pswitch_d
        :pswitch_8
        :pswitch_7
        :pswitch_0
        :pswitch_5
        :pswitch_6
    .end packed-switch
.end method

.method protected onPause()V
    .locals 2

    .prologue
    .line 158
    const-string v0, "FileChkActivity"

    const-string v1, "onPause"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 159
    invoke-super {p0}, Landroid/app/Activity;->onPause()V

    .line 160
    return-void
.end method

.method protected onResume()V
    .locals 3

    .prologue
    .line 144
    const-string v0, "FileChkActivity"

    const-string v1, "onResume"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 145
    invoke-super {p0}, Landroid/app/Activity;->onResume()V

    .line 147
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->initializeDownloadUI()V

    .line 150
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->pm:Landroid/os/PowerManager;

    const/16 v1, 0xa

    const-string v2, "FileChkActivity"

    invoke-virtual {v0, v1, v2}, Landroid/os/PowerManager;->newWakeLock(ILjava/lang/String;)Landroid/os/PowerManager$WakeLock;

    move-result-object v0

    iput-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->lock:Landroid/os/PowerManager$WakeLock;

    .line 151
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->lock:Landroid/os/PowerManager$WakeLock;

    invoke-virtual {v0}, Landroid/os/PowerManager$WakeLock;->acquire()V

    .line 153
    iget-boolean v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->exec_flag:Z

    if-eqz v0, :cond_0

    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/FileChkActivity;->execute()V

    .line 154
    :cond_0
    return-void
.end method

.method public onServiceConnected(Landroid/os/Messenger;)V
    .locals 2
    .param p1, "m"    # Landroid/os/Messenger;

    .prologue
    .line 306
    const-string v0, "FileChkActivity"

    const-string v1, "onServiceConnected"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 308
    invoke-static {p1}, Lcom/google/android/vending/expansion/downloader/DownloaderServiceMarshaller;->CreateProxy(Landroid/os/Messenger;)Lcom/google/android/vending/expansion/downloader/IDownloaderService;

    move-result-object v0

    iput-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_RemoteService:Lcom/google/android/vending/expansion/downloader/IDownloaderService;

    .line 309
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_RemoteService:Lcom/google/android/vending/expansion/downloader/IDownloaderService;

    const/4 v1, 0x1

    invoke-interface {v0, v1}, Lcom/google/android/vending/expansion/downloader/IDownloaderService;->setDownloadFlags(I)V

    .line 310
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_RemoteService:Lcom/google/android/vending/expansion/downloader/IDownloaderService;

    iget-object v1, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    invoke-interface {v1}, Lcom/google/android/vending/expansion/downloader/IStub;->getMessenger()Landroid/os/Messenger;

    move-result-object v1

    invoke-interface {v0, v1}, Lcom/google/android/vending/expansion/downloader/IDownloaderService;->onClientUpdated(Landroid/os/Messenger;)V

    .line 311
    return-void
.end method

.method protected onStart()V
    .locals 2

    .prologue
    .line 133
    const-string v0, "FileChkActivity"

    const-string v1, "onStart"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 134
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    if-eqz v0, :cond_0

    .line 136
    const-string v0, "FileChkActivity"

    const-string v1, "    DownloaderClientStub.connect"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 137
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    invoke-interface {v0, p0}, Lcom/google/android/vending/expansion/downloader/IStub;->connect(Landroid/content/Context;)V

    .line 139
    :cond_0
    invoke-super {p0}, Landroid/app/Activity;->onStart()V

    .line 140
    return-void
.end method

.method protected onStop()V
    .locals 2

    .prologue
    .line 164
    const-string v0, "FileChkActivity"

    const-string v1, "onStop"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 165
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    if-eqz v0, :cond_0

    .line 167
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_DownloaderClientStub:Lcom/google/android/vending/expansion/downloader/IStub;

    invoke-interface {v0, p0}, Lcom/google/android/vending/expansion/downloader/IStub;->disconnect(Landroid/content/Context;)V

    .line 169
    :cond_0
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    if-eqz v0, :cond_1

    .line 171
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    invoke-virtual {v0}, Landroid/app/ProgressDialog;->dismiss()V

    .line 172
    const/4 v0, 0x0

    iput-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->m_ProgressDialog:Landroid/app/ProgressDialog;

    .line 175
    :cond_1
    invoke-super {p0}, Landroid/app/Activity;->onStop()V

    .line 178
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity;->lock:Landroid/os/PowerManager$WakeLock;

    invoke-virtual {v0}, Landroid/os/PowerManager$WakeLock;->release()V

    .line 179
    return-void
.end method
