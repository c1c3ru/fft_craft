.class Lcom/square_enix/FFT_Android/FileChkActivity$1;
.super Ljava/lang/Object;
.source "FileChkActivity.java"

# interfaces
.implements Landroid/content/DialogInterface$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/square_enix/FFT_Android/FileChkActivity;->failedDialog()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/square_enix/FFT_Android/FileChkActivity;


# direct methods
.method constructor <init>(Lcom/square_enix/FFT_Android/FileChkActivity;)V
    .locals 0

    .prologue
    .line 1
    iput-object p1, p0, Lcom/square_enix/FFT_Android/FileChkActivity$1;->this$0:Lcom/square_enix/FFT_Android/FileChkActivity;

    .line 291
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/content/DialogInterface;I)V
    .locals 3
    .param p1, "dialog"    # Landroid/content/DialogInterface;
    .param p2, "which"    # I

    .prologue
    .line 294
    const-string v0, "FileChkActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "AlertDialog : Positive which :"

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 295
    iget-object v0, p0, Lcom/square_enix/FFT_Android/FileChkActivity$1;->this$0:Lcom/square_enix/FFT_Android/FileChkActivity;

    invoke-virtual {v0}, Lcom/square_enix/FFT_Android/FileChkActivity;->abort()V

    .line 296
    return-void
.end method
