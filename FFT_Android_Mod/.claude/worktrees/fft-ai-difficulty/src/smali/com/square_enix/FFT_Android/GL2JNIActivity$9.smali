.class Lcom/square_enix/FFT_Android/GL2JNIActivity$9;
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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    .line 1077
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method static synthetic access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)Lcom/square_enix/FFT_Android/GL2JNIActivity;
    .locals 1

    .prologue
    .line 1077
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    return-object v0
.end method


# virtual methods
.method public run()V
    .locals 4

    .prologue
    const/4 v3, 0x1

    const/4 v2, 0x0

    .line 1082
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$5(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/view/SurfaceView;

    move-result-object v0

    invoke-virtual {v0, v2}, Landroid/view/SurfaceView;->setVisibility(I)V

    .line 1083
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$6(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 1084
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$7(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Lcom/square_enix/FFT_Android/GL2JNIView;

    move-result-object v0

    const/4 v1, 0x4

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIView;->setVisibility(I)V

    .line 1085
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$8(Lcom/square_enix/FFT_Android/GL2JNIActivity;Z)V

    .line 1086
    invoke-static {v3}, Lcom/yox_project/silver_arrow/MoviePlayer;->SetPlaying(I)V

    .line 1087
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0, v2}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$9(Lcom/square_enix/FFT_Android/GL2JNIActivity;I)V

    .line 1090
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    .line 1091
    new-instance v1, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;

    invoke-direct {v1, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$1;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)V

    .line 1090
    invoke-virtual {v0, v1}, Landroid/media/MediaPlayer;->setOnPreparedListener(Landroid/media/MediaPlayer$OnPreparedListener;)V

    .line 1112
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$3(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/media/MediaPlayer;

    move-result-object v0

    .line 1113
    new-instance v1, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;

    invoke-direct {v1, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$2;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)V

    .line 1112
    invoke-virtual {v0, v1}, Landroid/media/MediaPlayer;->setOnCompletionListener(Landroid/media/MediaPlayer$OnCompletionListener;)V

    .line 1131
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$9;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$5(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/view/SurfaceView;

    move-result-object v0

    .line 1132
    new-instance v1, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;

    invoke-direct {v1, p0}, Lcom/square_enix/FFT_Android/GL2JNIActivity$9$3;-><init>(Lcom/square_enix/FFT_Android/GL2JNIActivity$9;)V

    .line 1131
    invoke-virtual {v0, v1}, Landroid/view/SurfaceView;->setOnTouchListener(Landroid/view/View$OnTouchListener;)V

    .line 1163
    return-void
.end method
