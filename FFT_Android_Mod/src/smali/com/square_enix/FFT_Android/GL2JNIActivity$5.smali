.class Lcom/square_enix/FFT_Android/GL2JNIActivity$5;
.super Ljava/lang/Object;
.source "GL2JNIActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/square_enix/FFT_Android/GL2JNIActivity;->run()V
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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$5;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    .line 373
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 0

    .prologue
    .line 378
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->Open()V

    .line 379
    return-void
.end method
