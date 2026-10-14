.class Lcom/square_enix/FFT_Android/GL2JNIActivity$8;
.super Ljava/lang/Object;
.source "GL2JNIActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/square_enix/FFT_Android/GL2JNIActivity;->Movie_run()V
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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    .line 1030
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 3

    .prologue
    const/4 v2, 0x4

    const/4 v1, 0x0

    .line 1034
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->isPlaying()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 1036
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->stop()V

    .line 1038
    :cond_0
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$5(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/view/SurfaceView;

    move-result-object v0

    invoke-virtual {v0, v2}, Landroid/view/SurfaceView;->setVisibility(I)V

    .line 1039
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$6(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 1040
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$7(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Lcom/square_enix/FFT_Android/GL2JNIView;

    move-result-object v0

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIView;->setVisibility(I)V

    .line 1041
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$8(Lcom/square_enix/FFT_Android/GL2JNIActivity;Z)V

    .line 1042
    invoke-static {v1}, Lcom/yox_project/silver_arrow/MoviePlayer;->SetPlaying(I)V

    .line 1043
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$9(Lcom/square_enix/FFT_Android/GL2JNIActivity;I)V

    .line 1044
    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->ResetSkipResult()V

    .line 1045
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$8;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->reset()V

    .line 1046
    return-void
.end method
