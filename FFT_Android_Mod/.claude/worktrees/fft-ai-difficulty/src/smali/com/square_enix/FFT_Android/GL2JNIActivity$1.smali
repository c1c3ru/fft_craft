.class Lcom/square_enix/FFT_Android/GL2JNIActivity$1;
.super Landroid/content/BroadcastReceiver;
.source "GL2JNIActivity.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/square_enix/FFT_Android/GL2JNIActivity;
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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$1;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    .line 622
    invoke-direct {p0}, Landroid/content/BroadcastReceiver;-><init>()V

    return-void
.end method


# virtual methods
.method public onReceive(Landroid/content/Context;Landroid/content/Intent;)V
    .locals 2
    .param p1, "context"    # Landroid/content/Context;
    .param p2, "intent"    # Landroid/content/Intent;

    .prologue
    .line 630
    const-string v0, "GL2JNIActivity"

    const-string v1, "    lock-screen: unlock"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 633
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$1;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$0(Lcom/square_enix/FFT_Android/GL2JNIActivity;)Z

    move-result v0

    if-eqz v0, :cond_0

    .line 636
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$1;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$1(Lcom/square_enix/FFT_Android/GL2JNIActivity;)V

    .line 638
    iget-object v0, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$1;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const/4 v1, 0x0

    invoke-static {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->access$2(Lcom/square_enix/FFT_Android/GL2JNIActivity;Z)V

    .line 640
    :cond_0
    return-void
.end method
