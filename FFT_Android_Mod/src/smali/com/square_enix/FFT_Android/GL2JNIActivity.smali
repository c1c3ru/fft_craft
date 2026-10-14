.class public Lcom/square_enix/FFT_Android/GL2JNIActivity;
.super Landroid/app/Activity;
.source "GL2JNIActivity.java"

# interfaces
.implements Ljava/lang/Runnable;
.implements Landroid/hardware/SensorEventListener;
.implements Landroid/view/SurfaceHolder$Callback;


# static fields
.field static final TAG:Ljava/lang/String; = "GL2JNIActivity"


# instance fields
.field private lock:Landroid/os/PowerManager$WakeLock;

.field private lyt_video:Landroid/widget/LinearLayout;

.field private mHandler:Landroid/os/Handler;

.field private mReceiverBattery:Landroid/content/BroadcastReceiver;

.field private mReceiverLockScreen:Landroid/content/BroadcastReceiver;

.field private mThread:Ljava/lang/Thread;

.field private mView:Lcom/square_enix/FFT_Android/GL2JNIView;

.field private m_MovieFrameCount:J

.field private m_bActive:Z

.field private m_bLockScreen:Z

.field private m_bReceiverBattery:Z

.field private m_bReceiverLockScreen:Z

.field private m_bVideoActive:Z

.field private m_bWakeLock:Z

.field private m_iVideoPosition:I

.field private manager:Landroid/hardware/SensorManager;

.field private mp_holder:Landroid/view/SurfaceHolder;

.field private mp_video:Landroid/media/MediaPlayer;

.field private mp_view:Landroid/view/SurfaceView;

.field private obbStateChangeListener1:Landroid/os/storage/OnObbStateChangeListener;

.field private obbStateChangeListener2:Landroid/os/storage/OnObbStateChangeListener;

.field private pm:Landroid/os/PowerManager;


# direct methods
.method public constructor <init>()V
    .locals 4

    .prologue
    const/4 v3, 0x0

    const/4 v2, 0x0

    .line 78
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 87
    iput-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mThread:Ljava/lang/Thread;

    .line 88
    iput-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mHandler:Landroid/os/Handler;

    .line 89
    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bActive:Z

    .line 91
    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverLockScreen:Z

    .line 92
    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bLockScreen:Z

    .line 93
    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverBattery:Z

    .line 97
    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bWakeLock:Z

    .line 102
    iput-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    .line 103
    iput v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_iVideoPosition:I

    .line 104
    const-wide/16 v0, 0x0

    iput-wide v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_MovieFrameCount:J

    .line 105
    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bVideoActive:Z

    .line 108
    iput-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_video:Landroid/media/MediaPlayer;

    .line 110
    iput-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_holder:Landroid/view/SurfaceHolder;

    .line 622
    new-instance v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$1;

    invoke-direct {v0, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$1;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mReceiverLockScreen:Landroid/content/BroadcastReceiver;

    .line 646
    new-instance v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$2;

    invoke-direct {v0, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$2;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mReceiverBattery:Landroid/content/BroadcastReceiver;

    .line 766
    new-instance v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;

    invoke-direct {v0, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->obbStateChangeListener1:Landroid/os/storage/OnObbStateChangeListener;

    .line 820
    new-instance v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$4;

    invoke-direct {v0, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$4;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->obbStateChangeListener2:Landroid/os/storage/OnObbStateChangeListener;

    .line 78
    return-void
.end method

.method private Movie_onPause()V
    .locals 3

    .prologue
    .line 997
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    invoke-virtual {v0}, Landroid/widget/LinearLayout;->isShown()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 999
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_video:Landroid/media/MediaPlayer;

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->getCurrentPosition()I

    move-result v0

    iput v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_iVideoPosition:I

    .line 1000
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_video:Landroid/media/MediaPlayer;

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->pause()V

    .line 1001
    const-string v0, "GL2JNIActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "    movie: pause (pos = "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_iVideoPosition:I

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ")"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 1003
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_video:Landroid/media/MediaPlayer;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroid/media/MediaPlayer;->seekTo(I)V

    .line 1005
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_video:Landroid/media/MediaPlayer;

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->reset()V

    .line 1011
    :goto_0
    return-void

    .line 1009
    :cond_0
    const-string v0, "GL2JNIActivity"

    const-string v1, "    movie: pause - skip"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method private Movie_onResume()V
    .locals 3

    .prologue
    .line 951
    iget-boolean v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bVideoActive:Z

    if-eqz v0, :cond_0

    .line 953
    const-string v0, "GL2JNIActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "    movie: replay (pos = "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_iVideoPosition:I

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ")"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 957
    const/4 v0, 0x0

    iput v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_iVideoPosition:I

    .line 958
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_video:Landroid/media/MediaPlayer;

    iget v1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_iVideoPosition:I

    invoke-virtual {v0, v1}, Landroid/media/MediaPlayer;->seekTo(I)V

    .line 959
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_video:Landroid/media/MediaPlayer;

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->start()V

    .line 961
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mHandler:Landroid/os/Handler;

    .line 962
    new-instance v1, Lcom/square_enix/FFT_Android/GL2JNIActivity$7;

    invoke-direct {v1, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$7;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    .line 961
    invoke-virtual {v0, v1}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 988
    :goto_0
    return-void

    .line 977
    :cond_0
    const-string v0, "GL2JNIActivity"

    const-string v1, "    movie: replay - skip"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method private Movie_run()V
    .locals 6

    .prologue
    .line 1022
    :try_start_0
    iget-boolean v1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bVideoActive:Z

    if-eqz v1, :cond_2

    .line 1024
    iget-object v1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    invoke-virtual {v1}, Landroid/widget/LinearLayout;->isShown()Z

    move-result v1

    if-eqz v1, :cond_0

    .line 1026
    iget-wide v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_MovieFrameCount:J

    const-wide/16 v4, 0x1

    add-long/2addr v2, v4

    iput-wide v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_MovieFrameCount:J

    .line 1027
    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->GetSkipResult()I

    move-result v1

    const/4 v2, 0x1

    if-ne v1, v2, :cond_1

    .line 1029
    iget-object v1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mHandler:Landroid/os/Handler;

    .line 1030
    new-instance v2, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;

    invoke-direct {v2, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    .line 1029
    invoke-virtual {v1, v2}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 1176
    :cond_0
    :goto_0
    return-void

    .line 1050
    :cond_1
    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->GetSkipResult()I

    move-result v1

    const/4 v2, 0x2

    if-ne v1, v2, :cond_0

    .line 1052
    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->ResetSkipResult()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 1172
    :catch_0
    move-exception v0

    .line 1174
    .local v0, "e":Ljava/lang/Exception;
    const-string v1, "GL2JNIActivity"

    const-string v2, "Exception: "

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0

    .line 1064
    .end local v0    # "e":Ljava/lang/Exception;
    :cond_2
    :try_start_1
    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->GetRequest()I

    move-result v1

    if-eqz v1, :cond_0

    .line 1072
    const/4 v1, 0x0

    invoke-static {v1}, Lcom/yox_project/silver_arrow/MoviePlayer;->SetRequest(I)V

    .line 1075
    const-string v1, "GL2JNIActivity"

    const-string v2, "mHandler.post"

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 1076
    iget-object v1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mHandler:Landroid/os/Handler;

    .line 1077
    new-instance v2, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-direct {v2, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    .line 1076
    invoke-virtual {v1, v2}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    goto :goto_0
.end method

.method static synthetic access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Z
    .locals 1

    .prologue
    .line 92
    iget-boolean v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bLockScreen:Z

    return v0
.end method

.method static synthetic access$1(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V
    .locals 0

    .prologue
    .line 283
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->onResume_Core()V

    return-void
.end method

.method static synthetic access$10(Lcom/square_enix/FFT_Android/GL2JNIActivity;)I
    .locals 1

    .prologue
    .line 103
    iget v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_iVideoPosition:I

    return v0
.end method

.method static synthetic access$11(Lcom/square_enix/FFT_Android/GL2JNIActivity;J)V
    .locals 1

    .prologue
    .line 104
    iput-wide p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_MovieFrameCount:J

    return-void
.end method

.method static synthetic access$12(Lcom/square_enix/FFT_Android/GL2JNIActivity;)J
    .locals 2

    .prologue
    .line 104
    iget-wide v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_MovieFrameCount:J

    return-wide v0
.end method

.method static synthetic access$2(Lcom/square_enix/FFT_Android/GL2JNIActivity;Z)V
    .locals 0

    .prologue
    .line 92
    iput-boolean p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bLockScreen:Z

    return-void
.end method

.method static synthetic access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;
    .locals 1

    .prologue
    .line 108
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_video:Landroid/media/MediaPlayer;

    return-object v0
.end method

.method static synthetic access$4(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/view/SurfaceHolder;
    .locals 1

    .prologue
    .line 110
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_holder:Landroid/view/SurfaceHolder;

    return-object v0
.end method

.method static synthetic access$5(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/view/SurfaceView;
    .locals 1

    .prologue
    .line 109
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_view:Landroid/view/SurfaceView;

    return-object v0
.end method

.method static synthetic access$6(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/widget/LinearLayout;
    .locals 1

    .prologue
    .line 102
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    return-object v0
.end method

.method static synthetic access$7(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Lcom/square_enix/FFT_Android/GL2JNIView;
    .locals 1

    .prologue
    .line 86
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mView:Lcom/square_enix/FFT_Android/GL2JNIView;

    return-object v0
.end method

.method static synthetic access$8(Lcom/square_enix/FFT_Android/GL2JNIActivity;Z)V
    .locals 0

    .prologue
    .line 105
    iput-boolean p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bVideoActive:Z

    return-void
.end method

.method static synthetic access$9(Lcom/square_enix/FFT_Android/GL2JNIActivity;I)V
    .locals 0

    .prologue
    .line 103
    iput p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_iVideoPosition:I

    return-void
.end method

.method private mountObb(Ljava/lang/String;Ljava/lang/Boolean;)V
    .locals 3
    .param p1, "file_name"    # Ljava/lang/String;
    .param p2, "main_obb"    # Ljava/lang/Boolean;

    .prologue
    const/4 v2, 0x0

    .line 853
    invoke-virtual {p2}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v1

    if-eqz v1, :cond_0

    .line 855
    const-string v1, "storage"

    invoke-virtual {p0, v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/os/storage/StorageManager;

    .line 856
    .local v0, "storageMgr":Landroid/os/storage/StorageManager;
    iget-object v1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->obbStateChangeListener1:Landroid/os/storage/OnObbStateChangeListener;

    invoke-virtual {v0, p1, v2, v1}, Landroid/os/storage/StorageManager;->mountObb(Ljava/lang/String;Ljava/lang/String;Landroid/os/storage/OnObbStateChangeListener;)Z

    .line 863
    :goto_0
    return-void

    .line 860
    .end local v0    # "storageMgr":Landroid/os/storage/StorageManager;
    :cond_0
    const-string v1, "storage"

    invoke-virtual {p0, v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/os/storage/StorageManager;

    .line 861
    .restart local v0    # "storageMgr":Landroid/os/storage/StorageManager;
    iget-object v1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->obbStateChangeListener2:Landroid/os/storage/OnObbStateChangeListener;

    invoke-virtual {v0, p1, v2, v1}, Landroid/os/storage/StorageManager;->mountObb(Ljava/lang/String;Ljava/lang/String;Landroid/os/storage/OnObbStateChangeListener;)Z

    goto :goto_0
.end method

.method private mountObbAll()V
    .locals 5

    .prologue
    const/4 v4, 0x1

    .line 841
    const v1, 0x31510

    invoke-virtual {p0, v4, v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getObbFileName(ZI)Ljava/lang/String;

    move-result-object v0

    .line 842
    .local v0, "obb_main_file_name":Ljava/lang/String;
    const-string v1, "GL2JNIActivity"

    new-instance v2, Ljava/lang/StringBuilder;

    const-string v3, "obb_main_file_name = "

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 843
    invoke-static {v4}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v1

    invoke-direct {p0, v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mountObb(Ljava/lang/String;Ljava/lang/Boolean;)V

    .line 849
    return-void
.end method

.method private onResume_Core()V
    .locals 7

    .prologue
    const/4 v6, 0x1

    .line 289
    invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNILib;->onResume()V

    .line 292
    iget-boolean v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverBattery:Z

    if-nez v3, :cond_0

    .line 294
    new-instance v0, Landroid/content/IntentFilter;

    invoke-direct {v0}, Landroid/content/IntentFilter;-><init>()V

    .line 295
    .local v0, "filter":Landroid/content/IntentFilter;
    const-string v3, "android.intent.action.BATTERY_CHANGED"

    invoke-virtual {v0, v3}, Landroid/content/IntentFilter;->addAction(Ljava/lang/String;)V

    .line 296
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mReceiverBattery:Landroid/content/BroadcastReceiver;

    invoke-virtual {p0, v3, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->registerReceiver(Landroid/content/BroadcastReceiver;Landroid/content/IntentFilter;)Landroid/content/Intent;

    .line 297
    iput-boolean v6, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverBattery:Z

    .line 301
    .end local v0    # "filter":Landroid/content/IntentFilter;
    :cond_0
    iget-boolean v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bWakeLock:Z

    if-nez v3, :cond_1

    .line 303
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->pm:Landroid/os/PowerManager;

    const/16 v4, 0xa

    const-string v5, "GL2JNIActivity"

    invoke-virtual {v3, v4, v5}, Landroid/os/PowerManager;->newWakeLock(ILjava/lang/String;)Landroid/os/PowerManager$WakeLock;

    move-result-object v3

    iput-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lock:Landroid/os/PowerManager$WakeLock;

    .line 304
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lock:Landroid/os/PowerManager$WakeLock;

    invoke-virtual {v3}, Landroid/os/PowerManager$WakeLock;->acquire()V

    .line 305
    iput-boolean v6, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bWakeLock:Z

    .line 309
    :cond_1
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->manager:Landroid/hardware/SensorManager;

    invoke-virtual {v3, v6}, Landroid/hardware/SensorManager;->getSensorList(I)Ljava/util/List;

    move-result-object v2

    .line 310
    .local v2, "sensors":Ljava/util/List;, "Ljava/util/List<Landroid/hardware/Sensor;>;"
    invoke-interface {v2}, Ljava/util/List;->size()I

    move-result v3

    if-lez v3, :cond_2

    .line 312
    const/4 v3, 0x0

    invoke-interface {v2, v3}, Ljava/util/List;->get(I)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/hardware/Sensor;

    .line 314
    .local v1, "s":Landroid/hardware/Sensor;
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->manager:Landroid/hardware/SensorManager;

    const/4 v4, 0x2

    invoke-virtual {v3, p0, v1, v4}, Landroid/hardware/SensorManager;->registerListener(Landroid/hardware/SensorEventListener;Landroid/hardware/Sensor;I)Z

    .line 318
    .end local v1    # "s":Landroid/hardware/Sensor;
    :cond_2
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->Movie_onResume()V

    .line 319
    return-void
.end method


# virtual methods
.method public dispatchKeyEvent(Landroid/view/KeyEvent;)Z
    .locals 7
    .param p1, "event"    # Landroid/view/KeyEvent;

    .prologue
    const/4 v2, 0x0

    const/4 v1, 0x1

    .line 574
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getAction()I

    move-result v0

    if-ne v0, v1, :cond_0

    .line 576
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getKeyCode()I

    move-result v0

    packed-switch v0, :pswitch_data_0

    .line 609
    :cond_0
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    invoke-virtual {v0}, Landroid/widget/LinearLayout;->isShown()Z

    move-result v0

    if-eqz v0, :cond_1

    .line 611
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_view:Landroid/view/SurfaceView;

    invoke-virtual {v0, v2}, Landroid/view/SurfaceView;->setVisibility(I)V

    .line 612
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 613
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mView:Lcom/square_enix/FFT_Android/GL2JNIView;

    const/4 v1, 0x4

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIView;->setVisibility(I)V

    .line 616
    :cond_1
    invoke-super {p0, p1}, Landroid/app/Activity;->dispatchKeyEvent(Landroid/view/KeyEvent;)Z

    move-result v1

    :goto_0
    return v1

    .line 580
    :pswitch_0
    invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNILib;->isExit()I

    move-result v0

    if-nez v0, :cond_2

    .line 582
    const-string v0, "GL2JNIActivity"

    const-string v2, "dispatchKeyEvent = [KEYCODE_BACK]"

    invoke-static {v0, v2}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 583
    invoke-static {v1}, Lcom/square_enix/FFT_Android/GL2JNILib;->onKeyEvent(I)V

    goto :goto_0

    .line 587
    :cond_2
    const-string v0, "GL2JNIActivity"

    const-string v2, "dispatchKeyEvent = [KEYCODE_BACK] - exit"

    invoke-static {v0, v2}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 589
    const v0, 0x7f040018

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v3

    .line 590
    .local v3, "strBtnOK":Ljava/lang/String;
    const v0, 0x7f040019

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v4

    .line 591
    .local v4, "strBtnCancel":Ljava/lang/String;
    const v0, 0x7f04001a

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v5

    .line 592
    .local v5, "strTitle":Ljava/lang/String;
    const v0, 0x7f04001b

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v6

    .line 595
    .local v6, "strMsg":Ljava/lang/String;
    const/16 v0, 0x3e7

    .line 597
    const v2, 0x108009b

    .line 594
    invoke-static/range {v0 .. v6}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->OpenRequest(IIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    .line 603
    invoke-static {v1}, Lcom/square_enix/FFT_Android/GL2JNILib;->onKeyEvent(I)V

    goto :goto_0

    .line 576
    :pswitch_data_0
    .packed-switch 0x4
        :pswitch_0
    .end packed-switch
.end method

.method public getObbFileName(ZI)Ljava/lang/String;
    .locals 4
    .param p1, "isMainFile"    # Z
    .param p2, "versionCode"    # I

    .prologue
    .line 867
    invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;

    move-result-object v0

    .line 868
    .local v0, "exdir":Ljava/io/File;
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    .line 869
    .local v1, "sb":Ljava/lang/StringBuilder;
    invoke-virtual {v0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 870
    const-string v2, "/Android/obb/"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 871
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getPackageName()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 872
    const-string v2, "/"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    .line 874
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v2

    invoke-direct {v3, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    if-eqz p1, :cond_0

    const-string v2, "main."

    :goto_0
    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2, p2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v2

    const-string v3, "."

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getPackageName()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    const-string v3, ".obb"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    return-object v2

    :cond_0
    const-string v2, "patch."

    goto :goto_0
.end method

.method public onAccuracyChanged(Landroid/hardware/Sensor;I)V
    .locals 0
    .param p1, "sensor"    # Landroid/hardware/Sensor;
    .param p2, "accuracy"    # I

    .prologue
    .line 744
    return-void
.end method

.method protected onActivityResult(IILandroid/content/Intent;)V
    .locals 0
    .param p1, "requestCode"    # I
    .param p2, "resultCode"    # I
    .param p3, "data"    # Landroid/content/Intent;

    .prologue
    .line 208
    invoke-super {p0, p1, p2, p3}, Landroid/app/Activity;->onActivityResult(IILandroid/content/Intent;)V

    .line 209
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 5
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .prologue
    const/4 v4, 0x4

    const/4 v3, -0x1

    .line 123
    const-string v0, "GL2JNIActivity"

    const-string v1, "onCreate ----------------------------------------"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 124
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 127
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getWindow()Landroid/view/Window;

    move-result-object v0

    const/4 v1, -0x3

    invoke-virtual {v0, v1}, Landroid/view/Window;->setFormat(I)V

    .line 128
    new-instance v0, Lcom/square_enix/FFT_Android/GL2JNIView;

    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getApplication()Landroid/app/Application;

    move-result-object v1

    invoke-direct {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIView;-><init>(Landroid/content/Context;)V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mView:Lcom/square_enix/FFT_Android/GL2JNIView;

    .line 129
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mView:Lcom/square_enix/FFT_Android/GL2JNIView;

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->setContentView(Landroid/view/View;)V

    .line 130
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mView:Lcom/square_enix/FFT_Android/GL2JNIView;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIView;->setVisibility(I)V

    .line 132
    new-instance v0, Landroid/view/SurfaceView;

    invoke-direct {v0, p0}, Landroid/view/SurfaceView;-><init>(Landroid/content/Context;)V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_view:Landroid/view/SurfaceView;

    .line 133
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_view:Landroid/view/SurfaceView;

    invoke-virtual {v0}, Landroid/view/SurfaceView;->getHolder()Landroid/view/SurfaceHolder;

    move-result-object v0

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_holder:Landroid/view/SurfaceHolder;

    .line 134
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_holder:Landroid/view/SurfaceHolder;

    const/4 v1, 0x3

    invoke-interface {v0, v1}, Landroid/view/SurfaceHolder;->setType(I)V

    .line 135
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_holder:Landroid/view/SurfaceHolder;

    invoke-interface {v0, p0}, Landroid/view/SurfaceHolder;->addCallback(Landroid/view/SurfaceHolder$Callback;)V

    .line 137
    new-instance v0, Landroid/media/MediaPlayer;

    invoke-direct {v0}, Landroid/media/MediaPlayer;-><init>()V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_video:Landroid/media/MediaPlayer;

    .line 138
    new-instance v0, Landroid/widget/LinearLayout;

    invoke-direct {v0, p0}, Landroid/widget/LinearLayout;-><init>(Landroid/content/Context;)V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    .line 139
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setGravity(I)V

    .line 140
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    const/high16 v1, -0x1000000

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setBackgroundColor(I)V

    .line 141
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    iget-object v1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_view:Landroid/view/SurfaceView;

    new-instance v2, Landroid/view/ViewGroup$LayoutParams;

    invoke-direct {v2, v3, v3}, Landroid/view/ViewGroup$LayoutParams;-><init>(II)V

    invoke-virtual {v0, v1, v2}, Landroid/widget/LinearLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 142
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    new-instance v1, Landroid/view/ViewGroup$LayoutParams;

    invoke-direct {v1, v3, v3}, Landroid/view/ViewGroup$LayoutParams;-><init>(II)V

    invoke-virtual {p0, v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->addContentView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 143
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mp_view:Landroid/view/SurfaceView;

    invoke-virtual {v0, v4}, Landroid/view/SurfaceView;->setVisibility(I)V

    .line 144
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lyt_video:Landroid/widget/LinearLayout;

    invoke-virtual {v0, v4}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 148
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mHandler:Landroid/os/Handler;

    if-nez v0, :cond_0

    .line 150
    new-instance v0, Landroid/os/Handler;

    invoke-direct {v0}, Landroid/os/Handler;-><init>()V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mHandler:Landroid/os/Handler;

    .line 152
    :cond_0
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mThread:Ljava/lang/Thread;

    if-nez v0, :cond_1

    .line 155
    new-instance v0, Ljava/lang/Thread;

    invoke-direct {v0, p0}, Ljava/lang/Thread;-><init>(Ljava/lang/Runnable;)V

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mThread:Ljava/lang/Thread;

    .line 156
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mThread:Ljava/lang/Thread;

    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    .line 162
    :cond_1
    const-string v0, "GL2JNIActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Build.VERSION:      "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    sget-object v2, Landroid/os/Build$VERSION;->RELEASE:Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 171
    const-string v0, "GL2JNIActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Build.BRAND:        "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    sget-object v2, Landroid/os/Build;->BRAND:Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 172
    const-string v0, "GL2JNIActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Build.MODEL:        "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    sget-object v2, Landroid/os/Build;->MODEL:Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 174
    const-string v0, "GL2JNIActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "Build.CPU_ABI:      "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    sget-object v2, Landroid/os/Build;->CPU_ABI:Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 180
    invoke-static {p0}, Lcom/yox_project/silver_arrow/StorageUtil;->Init(Landroid/content/Context;)V

    .line 181
    invoke-static {p0}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->Init(Landroid/content/Context;)V

    .line 182
    invoke-static {p0}, Lcom/yox_project/silver_arrow/WebUtil;->Init(Landroid/content/Context;)V

    .line 183
    invoke-static {p0}, Lcom/yox_project/silver_arrow/VibratorUtil;->Init(Landroid/content/Context;)V

    .line 184
    invoke-static {p0}, Lcom/yox_project/silver_arrow/MoviePlayer;->Init(Landroid/content/Context;)V

    .line 186
    const-string v0, "power"

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/os/PowerManager;

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->pm:Landroid/os/PowerManager;

    .line 188
    const-string v0, "sensor"

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/hardware/SensorManager;

    iput-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->manager:Landroid/hardware/SensorManager;

    .line 192
    const-string v0, "main.202000.com.square_enix.android_googleplay.FFT_en2.obb"

    if-eqz v0, :cond_2

    .line 195
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mountObbAll()V

    .line 197
    :cond_2
    return-void
.end method

.method protected onDestroy()V
    .locals 2

    .prologue
    .line 555
    const-string v0, "GL2JNIActivity"

    const-string v1, "onDestroy"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 556
    invoke-super {p0}, Landroid/app/Activity;->onDestroy()V

    .line 558
    invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNILib;->onDestroy()V

    .line 562
    const/4 v0, 0x0

    invoke-static {v0}, Ljava/lang/System;->exit(I)V

    .line 563
    return-void
.end method

.method protected onPause()V
    .locals 4

    .prologue
    const/4 v3, 0x1

    const/4 v2, 0x0

    .line 461
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->isFinishing()Z

    move-result v0

    if-eqz v0, :cond_3

    .line 467
    const-string v0, "GL2JNIActivity"

    const-string v1, "onPause (finishing)"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 473
    :goto_0
    invoke-super {p0}, Landroid/app/Activity;->onPause()V

    .line 482
    invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNILib;->onPause()V

    .line 485
    iget-boolean v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverLockScreen:Z

    if-eqz v0, :cond_0

    .line 487
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mReceiverLockScreen:Landroid/content/BroadcastReceiver;

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->unregisterReceiver(Landroid/content/BroadcastReceiver;)V

    .line 488
    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverLockScreen:Z

    .line 491
    :cond_0
    iget-boolean v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverBattery:Z

    if-eqz v0, :cond_1

    .line 493
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mReceiverBattery:Landroid/content/BroadcastReceiver;

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->unregisterReceiver(Landroid/content/BroadcastReceiver;)V

    .line 494
    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverBattery:Z

    .line 498
    :cond_1
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->Movie_onPause()V

    .line 506
    iput-boolean v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bLockScreen:Z

    .line 508
    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bActive:Z

    .line 516
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->isFinishing()Z

    move-result v0

    if-eqz v0, :cond_2

    .line 519
    const-string v0, "GL2JNIActivity"

    const-string v1, "    kill process (finishing)"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 520
    invoke-virtual {p0, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->moveTaskToBack(Z)Z

    .line 522
    :cond_2
    return-void

    .line 471
    :cond_3
    const-string v0, "GL2JNIActivity"

    const-string v1, "onPause"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method protected onRestart()V
    .locals 2

    .prologue
    .line 219
    const-string v0, "GL2JNIActivity"

    const-string v1, "onRestart ---------------------------------------"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 220
    invoke-super {p0}, Landroid/app/Activity;->onRestart()V

    .line 221
    return-void
.end method

.method protected onResume()V
    .locals 5

    .prologue
    const/4 v4, 0x1

    .line 244
    const-string v2, "GL2JNIActivity"

    const-string v3, "onResume"

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 245
    invoke-super {p0}, Landroid/app/Activity;->onResume()V

    .line 249
    const-string v2, "keyguard"

    invoke-virtual {p0, v2}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/app/KeyguardManager;

    .line 251
    .local v1, "keyguardManager":Landroid/app/KeyguardManager;
    invoke-virtual {v1}, Landroid/app/KeyguardManager;->inKeyguardRestrictedInputMode()Z

    move-result v2

    if-eqz v2, :cond_1

    .line 253
    const-string v2, "GL2JNIActivity"

    const-string v3, "    lock-screen: status=enabled"

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 255
    iput-boolean v4, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bLockScreen:Z

    .line 258
    iget-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverLockScreen:Z

    if-nez v2, :cond_0

    .line 260
    new-instance v0, Landroid/content/IntentFilter;

    invoke-direct {v0}, Landroid/content/IntentFilter;-><init>()V

    .line 261
    .local v0, "intentFilter":Landroid/content/IntentFilter;
    const-string v2, "android.intent.action.USER_PRESENT"

    invoke-virtual {v0, v2}, Landroid/content/IntentFilter;->addAction(Ljava/lang/String;)V

    .line 262
    iget-object v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mReceiverLockScreen:Landroid/content/BroadcastReceiver;

    invoke-virtual {p0, v2, v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->registerReceiver(Landroid/content/BroadcastReceiver;Landroid/content/IntentFilter;)Landroid/content/Intent;

    .line 263
    iput-boolean v4, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bReceiverLockScreen:Z

    .line 278
    .end local v0    # "intentFilter":Landroid/content/IntentFilter;
    :cond_0
    :goto_0
    iput-boolean v4, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bActive:Z

    .line 279
    return-void

    .line 269
    :cond_1
    const-string v2, "GL2JNIActivity"

    const-string v3, "    lock-screen: status=disabled"

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 271
    const/4 v2, 0x0

    iput-boolean v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bLockScreen:Z

    .line 274
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->onResume_Core()V

    goto :goto_0
.end method

.method public onSensorChanged(Landroid/hardware/SensorEvent;)V
    .locals 4
    .param p1, "event"    # Landroid/hardware/SensorEvent;

    .prologue
    const/4 v2, 0x1

    .line 750
    iget-object v0, p1, Landroid/hardware/SensorEvent;->sensor:Landroid/hardware/Sensor;

    invoke-virtual {v0}, Landroid/hardware/Sensor;->getType()I

    move-result v0

    if-ne v0, v2, :cond_0

    .line 755
    iget-object v0, p1, Landroid/hardware/SensorEvent;->values:[F

    const/4 v1, 0x0

    aget v0, v0, v1

    .line 756
    iget-object v1, p1, Landroid/hardware/SensorEvent;->values:[F

    aget v1, v1, v2

    .line 757
    iget-object v2, p1, Landroid/hardware/SensorEvent;->values:[F

    const/4 v3, 0x2

    aget v2, v2, v3

    .line 754
    invoke-static {v0, v1, v2}, Lcom/square_enix/FFT_Android/GL2JNILib;->setAccelerometerValue(FFF)V

    .line 760
    :cond_0
    return-void
.end method

.method protected onStart()V
    .locals 2

    .prologue
    .line 232
    const-string v0, "GL2JNIActivity"

    const-string v1, "onStart"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 233
    invoke-super {p0}, Landroid/app/Activity;->onStart()V

    .line 234
    return-void
.end method

.method protected onStop()V
    .locals 2

    .prologue
    .line 533
    const-string v0, "GL2JNIActivity"

    const-string v1, "onStop"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 534
    invoke-super {p0}, Landroid/app/Activity;->onStop()V

    .line 537
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->manager:Landroid/hardware/SensorManager;

    invoke-virtual {v0, p0}, Landroid/hardware/SensorManager;->unregisterListener(Landroid/hardware/SensorEventListener;)V

    .line 540
    iget-boolean v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bWakeLock:Z

    if-eqz v0, :cond_0

    .line 542
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->lock:Landroid/os/PowerManager$WakeLock;

    invoke-virtual {v0}, Landroid/os/PowerManager$WakeLock;->release()V

    .line 543
    const/4 v0, 0x0

    iput-boolean v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bWakeLock:Z

    .line 545
    :cond_0
    return-void
.end method

.method public run()V
    .locals 7

    .prologue
    const/4 v6, 0x0

    .line 329
    const-string v3, "GL2JNIActivity"

    const-string v4, "run"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 336
    :goto_0
    iget-boolean v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bActive:Z

    if-eqz v3, :cond_0

    iget-boolean v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bLockScreen:Z

    if-eqz v3, :cond_1

    .line 340
    :cond_0
    const-wide/16 v4, 0x3e8

    :try_start_0
    invoke-static {v4, v5}, Ljava/lang/Thread;->sleep(J)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    .line 342
    :catch_0
    move-exception v0

    .line 344
    .local v0, "e":Ljava/lang/Exception;
    const-string v3, "GL2JNIActivity"

    const-string v4, "Exception: "

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0

    .line 349
    .end local v0    # "e":Ljava/lang/Exception;
    :cond_1
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mView:Lcom/square_enix/FFT_Android/GL2JNIView;

    invoke-virtual {v3}, Lcom/square_enix/FFT_Android/GL2JNIView;->requestRender()V

    .line 360
    :try_start_1
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->GetRequest()I

    move-result v3

    if-eqz v3, :cond_4

    .line 368
    const/4 v3, 0x0

    invoke-static {v3}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->SetRequest(I)V

    .line 371
    const-string v3, "GL2JNIActivity"

    const-string v4, "mHandler.post"

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 372
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mHandler:Landroid/os/Handler;

    .line 373
    new-instance v4, Lcom/square_enix/FFT_Android/GL2JNIActivity$5;

    invoke-direct {v4, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$5;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    .line 372
    invoke-virtual {v3, v4}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_1

    .line 432
    :cond_2
    :goto_1
    :sswitch_0
    invoke-static {}, Lcom/yox_project/silver_arrow/WebUtil;->GetRequest()I

    move-result v3

    if-eqz v3, :cond_3

    .line 440
    invoke-static {v6}, Lcom/yox_project/silver_arrow/WebUtil;->SetRequest(I)V

    .line 443
    invoke-static {}, Lcom/yox_project/silver_arrow/WebUtil;->Open()V

    .line 448
    :cond_3
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->Movie_run()V

    goto :goto_0

    .line 385
    :cond_4
    :try_start_2
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->GetID()I

    move-result v1

    .line 386
    .local v1, "iID":I
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->GetResult()I

    move-result v2

    .line 389
    .local v2, "iResult":I
    const/4 v3, -0x1

    if-eq v2, v3, :cond_2

    .line 392
    invoke-static {v2}, Lcom/square_enix/FFT_Android/GL2JNILib;->dialogOnClose(I)V

    .line 394
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->Close()V

    .line 397
    sparse-switch v1, :sswitch_data_0

    goto :goto_1

    .line 409
    :sswitch_1
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->finish()V
    :try_end_2
    .catch Ljava/lang/Exception; {:try_start_2 .. :try_end_2} :catch_1

    goto :goto_1

    .line 420
    .end local v1    # "iID":I
    .end local v2    # "iResult":I
    :catch_1
    move-exception v0

    .line 422
    .restart local v0    # "e":Ljava/lang/Exception;
    const-string v3, "GL2JNIActivity"

    const-string v4, "Exception: "

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_1

    .line 401
    .end local v0    # "e":Ljava/lang/Exception;
    .restart local v1    # "iID":I
    .restart local v2    # "iResult":I
    :sswitch_2
    if-nez v2, :cond_2

    .line 404
    :try_start_3
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->finish()V
    :try_end_3
    .catch Ljava/lang/Exception; {:try_start_3 .. :try_end_3} :catch_1

    goto :goto_1

    .line 397
    nop

    :sswitch_data_0
    .sparse-switch
        0x2 -> :sswitch_0
        0x3e4 -> :sswitch_1
        0x3e7 -> :sswitch_2
    .end sparse-switch
.end method

.method public surfaceChanged(Landroid/view/SurfaceHolder;III)V
    .locals 2
    .param p1, "holder"    # Landroid/view/SurfaceHolder;
    .param p2, "format"    # I
    .param p3, "width"    # I
    .param p4, "height"    # I

    .prologue
    .line 891
    iget-boolean v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->m_bLockScreen:Z

    if-eqz v0, :cond_0

    .line 893
    const-string v0, "GL2JNIActivity"

    const-string v1, "======surfaceChanged - skip"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 934
    :goto_0
    return-void

    .line 896
    :cond_0
    const-string v0, "GL2JNIActivity"

    const-string v1, "======surfaceChanged"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 898
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity;->mHandler:Landroid/os/Handler;

    .line 899
    new-instance v1, Lcom/square_enix/FFT_Android/GL2JNIActivity$6;

    invoke-direct {v1, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$6;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    .line 898
    invoke-virtual {v0, v1}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    goto :goto_0
.end method

.method public surfaceCreated(Landroid/view/SurfaceHolder;)V
    .locals 2
    .param p1, "holder"    # Landroid/view/SurfaceHolder;

    .prologue
    .line 883
    const-string v0, "GL2JNIActivity"

    const-string v1, "======surfaceCreated"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 884
    return-void
.end method

.method public surfaceDestroyed(Landroid/view/SurfaceHolder;)V
    .locals 2
    .param p1, "paramSurfaceHolder"    # Landroid/view/SurfaceHolder;

    .prologue
    .line 940
    const-string v0, "GL2JNIActivity"

    const-string v1, "======surfaceDestroyed"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 941
    return-void
.end method
