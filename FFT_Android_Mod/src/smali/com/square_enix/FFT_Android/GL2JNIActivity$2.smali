.class Lcom/square_enix/FFT_Android/GL2JNIActivity$2;
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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$2;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    .line 646
    invoke-direct {p0}, Landroid/content/BroadcastReceiver;-><init>()V

    return-void
.end method


# virtual methods
.method public onReceive(Landroid/content/Context;Landroid/content/Intent;)V
    .locals 5
    .param p1, "context"    # Landroid/content/Context;
    .param p2, "intent"    # Landroid/content/Intent;

    .prologue
    const/4 v4, 0x0

    .line 650
    invoke-virtual {p2}, Landroid/content/Intent;->getAction()Ljava/lang/String;

    move-result-object v0

    .line 651
    .local v0, "action":Ljava/lang/String;
    const-string v3, "android.intent.action.BATTERY_CHANGED"

    invoke-virtual {v0, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-eqz v3, :cond_0

    .line 656
    const-string v3, "level"

    invoke-virtual {p2, v3, v4}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v1

    .line 657
    .local v1, "level":I
    const-string v3, "scale"

    invoke-virtual {p2, v3, v4}, Landroid/content/Intent;->getIntExtra(Ljava/lang/String;I)I

    move-result v2

    .line 732
    .local v2, "scale":I
    mul-int/lit8 v3, v1, 0x64

    div-int/2addr v3, v2

    invoke-static {v3}, Lcom/square_enix/FFT_Android/GL2JNILib;->setBatteryLevel(I)V

    .line 734
    .end local v1    # "level":I
    .end local v2    # "scale":I
    :cond_0
    return-void
.end method
