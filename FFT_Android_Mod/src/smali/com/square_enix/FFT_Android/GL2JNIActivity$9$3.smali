.class Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;
.super Ljava/lang/Object;
.source "GL2JNIActivity.java"

# interfaces
.implements Landroid/view/View$OnTouchListener;


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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    .line 1132
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onTouch(Landroid/view/View;Landroid/view/MotionEvent;)Z
    .locals 7
    .param p1, "v"    # Landroid/view/View;
    .param p2, "event"    # Landroid/view/MotionEvent;

    .prologue
    const/4 v6, 0x4

    const/4 v5, 0x1

    const/4 v4, 0x0

    .line 1136
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$12(Lcom/square_enix/FFT_Android/GL2JNIActivity;)J

    move-result-wide v0

    const-wide/16 v2, 0xa

    cmp-long v0, v0, v2

    if-gez v0, :cond_1

    .line 1159
    :cond_0
    :goto_0
    return v5

    .line 1138
    :cond_1
    invoke-virtual {p2}, Landroid/view/MotionEvent;->getAction()I

    move-result v0

    if-nez v0, :cond_0

    .line 1140
    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->GetMovieFileName()Ljava/lang/String;

    move-result-object v0

    const-string v1, ".*/09.mp4"

    invoke-virtual {v0, v1}, Ljava/lang/String;->matches(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_3

    .line 1142
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->isPlaying()Z

    move-result v0

    if-eqz v0, :cond_2

    .line 1144
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->stop()V

    .line 1146
    :cond_2
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$5(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/view/SurfaceView;

    move-result-object v0

    invoke-virtual {v0, v6}, Landroid/view/SurfaceView;->setVisibility(I)V

    .line 1147
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$6(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {v0, v6}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 1148
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$7(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Lcom/square_enix/FFT_Android/GL2JNIView;

    move-result-object v0

    invoke-virtual {v0, v4}, Lcom/square_enix/FFT_Android/GL2JNIView;->setVisibility(I)V

    .line 1149
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0, v4}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$8(Lcom/square_enix/FFT_Android/GL2JNIActivity;Z)V

    .line 1150
    invoke-static {v4}, Lcom/yox_project/silver_arrow/MoviePlayer;->SetPlaying(I)V

    .line 1151
    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->ResetSkipResult()V

    .line 1152
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->reset()V

    goto :goto_0

    .line 1156
    :cond_3
    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->OpenSkipDialog()V

    goto :goto_0
.end method
