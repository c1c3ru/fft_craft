.class Lcom/square_enix/FFT_Android/GL2JNIActivity$7;
.super Ljava/lang/Object;
.source "GL2JNIActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/square_enix/FFT_Android/GL2JNIActivity;->Movie_onResume()V
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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$7;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    .line 962
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 3

    .prologue
    const/4 v2, 0x1

    const/4 v1, 0x0

    .line 966
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$7;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$5(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/view/SurfaceView;

    move-result-object v0

    invoke-virtual {v0, v1}, Landroid/view/SurfaceView;->setVisibility(I)V

    .line 967
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$7;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$6(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 968
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$7;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$7(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Lcom/square_enix/FFT_Android/GL2JNIView;

    move-result-object v0

    const/4 v1, 0x4

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIView;->setVisibility(I)V

    .line 969
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$7;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0, v2}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$8(Lcom/square_enix/FFT_Android/GL2JNIActivity;Z)V

    .line 970
    invoke-static {v2}, Lcom/yox_project/silver_arrow/MoviePlayer;->SetPlaying(I)V

    .line 971
    return-void
.end method
