.class Lcom/square_enix/FFT_Android/LicenseCheckerActivity$1;
.super Ljava/lang/Object;
.source "LicenseCheckerActivity.java"

# interfaces
.implements Ljava/lang/Runnable;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/square_enix/FFT_Android/LicenseCheckerActivity;->run()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;


# direct methods
.method constructor <init>(Lcom/square_enix/FFT_Android/LicenseCheckerActivity;)V
    .locals 0

    .prologue
    .line 1
    iput-object p1, p0, Lcom/square_enix/FFT_Android/LicenseCheckerActivity$1;->this$0:Lcom/square_enix/FFT_Android/LicenseCheckerActivity;

    .line 181
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public run()V
    .locals 0

    .prologue
    .line 186
    invoke-static {}, Lcom/yox_project/silver_arrow/AlertDialogUtil;->Open()V

    .line 187
    return-void
.end method
