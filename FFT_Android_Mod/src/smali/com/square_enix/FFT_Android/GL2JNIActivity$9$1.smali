.class Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;
.super Ljava/lang/Object;
.source "GL2JNIActivity.java"

# interfaces
.implements Landroid/media/MediaPlayer$OnPreparedListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->run()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;


# direct methods
.method constructor <init>(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)V
    .locals 0

    .prologue
    .line 1
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    .line 1091
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onPrepared(Landroid/media/MediaPlayer;)V
    .locals 4
    .param p1, "mp"    # Landroid/media/MediaPlayer;

    .prologue
    .line 1095
    const-string v0, "GL2JNIActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "    movie: pos = "

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    iget-object v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v2}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v2

    invoke-static {v2}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$10(Lcom/square_enix/FFT_Android/GL2JNIActivity;)I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 1096
    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->IsOBBPath()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 1098
    const-string v0, "GL2JNIActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "    movie: start ["

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt1OBBPath()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "/base/"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->GetMovieFileName()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "]"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 1104
    :goto_0
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    iget-object v1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v1

    invoke-static {v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$10(Lcom/square_enix/FFT_Android/GL2JNIActivity;)I

    move-result v1

    invoke-virtual {v0, v1}, Landroid/media/MediaPlayer;->seekTo(I)V

    .line 1105
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->start()V

    .line 1106
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    const/4 v1, 0x0

    invoke-static {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$9(Lcom/square_enix/FFT_Android/GL2JNIActivity;I)V

    .line 1107
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    const-wide/16 v2, 0x0

    invoke-static {v0, v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$11(Lcom/square_enix/FFT_Android/GL2JNIActivity;J)V

    .line 1108
    return-void

    .line 1102
    :cond_0
    const-string v0, "GL2JNIActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "    movie: start ["

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt1Path()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "/base/"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->GetMovieFileName()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "]"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method
