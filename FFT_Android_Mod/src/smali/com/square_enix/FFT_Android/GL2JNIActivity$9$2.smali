.class Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;
.super Ljava/lang/Object;
.source "GL2JNIActivity.java"

# interfaces
.implements Landroid/media/MediaPlayer$OnCompletionListener;


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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    .line 1113
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onCompletion(Landroid/media/MediaPlayer;)V
    .locals 4
    .param p1, "mp"    # Landroid/media/MediaPlayer;

    .prologue
    const/4 v3, 0x4

    const/4 v2, 0x0

    .line 1117
    const-string v0, "GL2JNIActivity"

    const-string v1, "    movie: onCompletion"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 1119
    invoke-static {}, Lcom/yox_project/silver_arrow/MoviePlayer;->CloseSkipDialog()V

    .line 1120
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$5(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/view/SurfaceView;

    move-result-object v0

    invoke-virtual {v0, v3}, Landroid/view/SurfaceView;->setVisibility(I)V

    .line 1121
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$6(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {v0, v3}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 1122
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$7(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Lcom/square_enix/FFT_Android/GL2JNIView;

    move-result-object v0

    invoke-virtual {v0, v2}, Lcom/square_enix/FFT_Android/GL2JNIView;->setVisibility(I)V

    .line 1123
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0, v2}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$8(Lcom/square_enix/FFT_Android/GL2JNIActivity;Z)V

    .line 1124
    invoke-static {v2}, Lcom/yox_project/silver_arrow/MoviePlayer;->SetPlaying(I)V

    .line 1125
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0, v2}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$9(Lcom/square_enix/FFT_Android/GL2JNIActivity;I)V

    .line 1126
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;->this$1:Lcom/square_enix/FFT_Android/GL2JNIActivity$9;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;

    move-result-object v0

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    invoke-virtual {v0}, Landroid/media/MediaPlayer;->reset()V

    .line 1127
    return-void
.end method
