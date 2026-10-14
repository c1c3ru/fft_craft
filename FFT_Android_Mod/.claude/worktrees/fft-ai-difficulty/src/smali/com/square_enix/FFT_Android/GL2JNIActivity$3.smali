.class Lcom/square_enix/FFT_Android/GL2JNIActivity$3;
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
    iput-object p1, p0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    .line 766
    invoke-direct {p0}, Landroid/os/storage/OnObbStateChangeListener;-><init>()V

    return-void
.end method


# virtual methods
.method public onObbStateChange(Ljava/lang/String;I)V
    .locals 18
    .param p1, "path"    # Ljava/lang/String;
    .param p2, "state"    # I

    .prologue
    .line 770
    const/16 v16, 0x0

    .line 773
    .local v16, "mountPath":Ljava/lang/String;
    const/4 v2, 0x1

    move/from16 v0, p2

    if-ne v0, v2, :cond_0

    .line 775
    move-object/from16 v0, p0

    iget-object v2, v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const-string v3, "storage"

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v17

    check-cast v17, Landroid/os/storage/StorageManager;

    .line 777
    .local v17, "stmgr":Landroid/os/storage/StorageManager;
    move-object/from16 v0, v17

    move-object/from16 v1, p1

    invoke-virtual {v0, v1}, Landroid/os/storage/StorageManager;->getMountedObbPath(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v16

    .line 778
    invoke-static/range {v16 .. v16}, Lcom/yox_project/silver_arrow/StorageUtil;->SetExt1OBBPath(Ljava/lang/String;)V

    .line 779
    const-string v2, "GL2JNIActivity"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "    OBB: mount - complete ["

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    move-object/from16 v0, v16

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "]"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 817
    .end local v17    # "stmgr":Landroid/os/storage/StorageManager;
    :goto_0
    return-void

    .line 782
    :cond_0
    const/16 v2, 0x15

    move/from16 v0, p2

    if-ne v0, v2, :cond_1

    .line 784
    move-object/from16 v0, p0

    iget-object v2, v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const v3, 0x7f040018

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v5

    .line 785
    .local v5, "strBtnOK":Ljava/lang/String;
    move-object/from16 v0, p0

    iget-object v2, v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const v3, 0x7f040019

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v6

    .line 786
    .local v6, "strBtnCancel":Ljava/lang/String;
    move-object/from16 v0, p0

    iget-object v2, v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const v3, 0x7f04001c

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v7

    .line 787
    .local v7, "strTitle":Ljava/lang/String;
    move-object/from16 v0, p0

    iget-object v2, v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const v3, 0x7f04001d

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v8

    .line 789
    .local v8, "strMsg":Ljava/lang/String;
    const-string v2, "GL2JNIActivity"

    const-string v3, "[error] OBB: mount - ERROR_COULD_NOT_MOUNT"

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 791
    const/16 v2, 0x3e4

    .line 792
    const/4 v3, 0x0

    .line 793
    const v4, 0x1080027

    .line 790
    invoke-static/range {v2 .. v8}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->OpenRequest(IIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0

    .line 802
    .end local v5    # "strBtnOK":Ljava/lang/String;
    .end local v6    # "strBtnCancel":Ljava/lang/String;
    .end local v7    # "strTitle":Ljava/lang/String;
    .end local v8    # "strMsg":Ljava/lang/String;
    :cond_1
    move-object/from16 v0, p0

    iget-object v2, v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const v3, 0x7f040018

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v5

    .line 803
    .restart local v5    # "strBtnOK":Ljava/lang/String;
    move-object/from16 v0, p0

    iget-object v2, v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const v3, 0x7f040019

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v6

    .line 804
    .restart local v6    # "strBtnCancel":Ljava/lang/String;
    move-object/from16 v0, p0

    iget-object v2, v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const v3, 0x7f04001c

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v7

    .line 805
    .restart local v7    # "strTitle":Ljava/lang/String;
    move-object/from16 v0, p0

    iget-object v2, v0, Lcom/square_enix/FFT_Android/GL2JNIActivity$3;->this$0:Lcom/square_enix/FFT_Android/GL2JNIActivity;

    const v3, 0x7f04001e

    invoke-virtual {v2, v3}, Lcom/square_enix/FFT_Android/GL2JNIActivity;->getString(I)Ljava/lang/String;

    move-result-object v8

    .line 807
    .restart local v8    # "strMsg":Ljava/lang/String;
    const-string v2, "GL2JNIActivity"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "    OBB: state = "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    move/from16 v0, p2

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "."

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 809
    const/16 v9, 0x3e4

    .line 810
    const/4 v10, 0x0

    .line 811
    const v11, 0x1080027

    .line 813
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-static {v7}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v3

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v3, " ("

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    move/from16 v0, p2

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v2

    const-string v3, ")"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v14

    move-object v12, v5

    move-object v13, v6

    move-object v15, v8

    .line 808
    invoke-static/range {v9 .. v15}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->OpenRequest(IIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    goto/16 :goto_0
.end method
