.class Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;
.super Ljava/lang/Object;
.source "LicenseCheckerActivity.java"

# interfaces
.implements Lcom/google/android/vending/licensing/LicenseCheckerCallback;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/square_enix/FFT_Android/LicenseCheckerActivity;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x2
    name = "MyLicenseCheckerCallback"
.end annotation


# instance fields
.field final synthetic this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;


# direct methods
.method private constructor <init>(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;)V
    .locals 0

    .prologue
    .line 407
    iput-object p1, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method synthetic constructor <init>(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;)V
    .locals 0

    .prologue
    .line 407
    invoke-direct {p0, p1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;-><init>(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;)V

    return-void
.end method


# virtual methods
.method public allow(I)V
    .locals 3
    .param p1, "policyReason"    # I

    .prologue
    .line 414
    const-string v0, "LicenseCheckerActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "result = OK ("

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ")"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 415
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const/16 v1, 0x64

    invoke-static {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->access$0(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;I)V

    .line 416
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const/4 v1, 0x1

    invoke-static {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->access$1(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;Z)V

    .line 426
    return-void
.end method

.method public applicationError(I)V
    .locals 9
    .param p1, "errorCode"    # I

    .prologue
    .line 483
    const-string v0, "LicenseCheckerActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "result = App error ("

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ")"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 492
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const v1, 0x7f040018

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getString(I)Ljava/lang/String;

    move-result-object v3

    .line 493
    .local v3, "strBtnOK":Ljava/lang/String;
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const v1, 0x7f040019

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getString(I)Ljava/lang/String;

    move-result-object v4

    .line 494
    .local v4, "strBtnCancel":Ljava/lang/String;
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const v1, 0x7f04002a

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getString(I)Ljava/lang/String;

    move-result-object v7

    .line 495
    .local v7, "strTitle":Ljava/lang/String;
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const v1, 0x7f04002c

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getString(I)Ljava/lang/String;

    move-result-object v6

    .line 498
    .local v6, "strMsg":Ljava/lang/String;
    const/16 v0, 0x3e6

    .line 499
    const/4 v1, 0x0

    .line 500
    const v2, 0x1080027

    .line 502
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-static {v7}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v8

    invoke-direct {v5, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v8, " ("

    invoke-virtual {v5, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v8, ")"

    invoke-virtual {v5, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    .line 497
    invoke-static/range {v0 .. v6}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->OpenRequest(IIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    .line 518
    return-void
.end method

.method public dontAllow(I)V
    .locals 9
    .param p1, "policyReason"    # I

    .prologue
    .line 434
    const-string v0, "LicenseCheckerActivity"

    new-instance v1, Ljava/lang/StringBuilder;

    const-string v2, "result = NG ("

    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ")"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 443
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const v1, 0x7f040018

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getString(I)Ljava/lang/String;

    move-result-object v3

    .line 444
    .local v3, "strBtnOK":Ljava/lang/String;
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const v1, 0x7f040019

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getString(I)Ljava/lang/String;

    move-result-object v4

    .line 445
    .local v4, "strBtnCancel":Ljava/lang/String;
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const v1, 0x7f04002a

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getString(I)Ljava/lang/String;

    move-result-object v7

    .line 446
    .local v7, "strTitle":Ljava/lang/String;
    iget-object v0, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$MyLicenseCheckerCallback;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    const v1, 0x7f04002b

    invoke-virtual {v0, v1}, Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->getString(I)Ljava/lang/String;

    move-result-object v6

    .line 449
    .local v6, "strMsg":Ljava/lang/String;
    const/16 v0, 0x3e6

    .line 450
    const/4 v1, 0x0

    .line 451
    const v2, 0x1080027

    .line 453
    new-instance v5, Ljava/lang/StringBuilder;

    invoke-static {v7}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v8

    invoke-direct {v5, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v8, " ("

    invoke-virtual {v5, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v8, ")"

    invoke-virtual {v5, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    .line 448
    invoke-static/range {v0 .. v6}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->OpenRequest(IIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    .line 475
    return-void
.end method
