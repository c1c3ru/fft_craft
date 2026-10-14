.class Lcom/square_enix/FFT_Android/GL2JNIActivity$4;
.super Landroid/os/storage/OnObbStateChangeListener;
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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$4;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    .line 820
    invoke-direct {p0}, Landroid/os/storage/OnObbStateChangeListener;-><init>()V

    return-void
.end method


# virtual methods
.method public onObbStateChange(Ljava/lang/String;I)V
    .locals 5
    .param p1, "path"    # Ljava/lang/String;
    .param p2, "state"    # I

    .prologue
    .line 824
    const/4 v0, 0x0

    .line 825
    .local v0, "mountPath":Ljava/lang/String;
    const-string v2, "GL2JNIActivity"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "OBB  : "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "("

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-static {p2}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, ")"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 827
    const/4 v2, 0x1

    if-ne p2, v2, :cond_0

    .line 829
    iget-object v2, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$4;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const-string v3, "storage"

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v1

    check-cast v1, Landroid/os/storage/StorageManager;

    .line 831
    .local v1, "stmgr":Landroid/os/storage/StorageManager;
    invoke-virtual {v1, p1}, Landroid/os/storage/StorageManager;->getMountedObbPath(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 832
    invoke-static {v0}, Lcom/yox_project/silver_arrow/StorageUtil;->SetExt2OBBPath(Ljava/lang/String;)V

    .line 833
    const-string v2, "GL2JNIActivity"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "OBB: "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 835
    .end local v1    # "stmgr":Landroid/os/storage/StorageManager;
    :cond_0
    return-void
.end method
