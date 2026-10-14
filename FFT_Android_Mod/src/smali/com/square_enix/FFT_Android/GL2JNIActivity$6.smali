.class Lcom/square_enix/FFT_Android/GL2JNIActivity$6;
.super Ljava/lang/Object;
.source "GL2JNIActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/square_enix/FFT_Android/GL2JNIActivity;->surfaceChanged(Landroid/view/SurfaceHolder;III)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;


# direct methods
.method constructor <init>(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V
    .locals 0

    .prologue
    .line 1
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$6;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    .line 899
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 6

    .prologue
    .line 906
    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->IsOBBPath()Z

    move-result v3

    if-eqz v3, :cond_0

    .line 908
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt1OBBPath()Ljava/lang/String;

    move-result-object v4

    invoke-static {v4}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v4

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v4, "/base/"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->GetMovieFileName()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    .line 915
    .local v2, "strFileName":Ljava/lang/String;
    :goto_0
    const-string v3, "GL2JNIActivity"

    new-instance v4, Ljava/lang/StringBuilder;

    const-string v5, "    movie: prepare ["

    invoke-direct {v4, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v4, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    const-string v5, "]"

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 920
    :try_start_0
    new-instance v1, Ljava/io/FileInputStream;

    invoke-direct {v1, v2}, Ljava/io/FileInputStream;-><init>(Ljava/lang/String;)V

    .line 921
    .local v1, "fis":Ljava/io/FileInputStream;
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$6;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v3

    invoke-virtual {v3}, Landroid/media/MediaPlayer;->reset()V

    .line 922
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$6;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v3

    invoke-virtual {v1}, Ljava/io/FileInputStream;->getFD()Ljava/io/FileDescriptor;

    move-result-object v4

    invoke-virtual {v3, v4}, Landroid/media/MediaPlayer;->setDataSource(Ljava/io/FileDescriptor;)V

    .line 923
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$6;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v3

    iget-object v4, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$6;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v4}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$4(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/view/SurfaceHolder;

    move-result-object v4

    invoke-virtual {v3, v4}, Landroid/media/MediaPlayer;->setDisplay(Landroid/view/SurfaceHolder;)V

    .line 924
    iget-object v3, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$6;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v3

    invoke-virtual {v3}, Landroid/media/MediaPlayer;->prepare()V

    .line 925
    invoke-virtual {v1}, Ljava/io/FileInputStream;->close()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 931
    .end local v1    # "fis":Ljava/io/FileInputStream;
    :goto_1
    return-void

    .line 913
    .end local v2    # "strFileName":Ljava/lang/String;
    :cond_0
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt1Path()Ljava/lang/String;

    move-result-object v4

    invoke-static {v4}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v4

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v4, "/base/"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->GetMovieFileName()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    .restart local v2    # "strFileName":Ljava/lang/String;
    goto :goto_0

    .line 927
    :catch_0
    move-exception v0

    .line 929
    .local v0, "e":Ljava/lang/Exception;
    const-string v3, "GL2JNIActivity"

    const-string v4, "Exception: "

    invoke-static {v3, v4}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_1
.end method
