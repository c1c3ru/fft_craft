.class Lcom/yox_project/silver_arrow/AlertDialogUtil$2;
.super Ljava/lang/Object;
.source "AlertDialogUtil.java"

# interfaces
.implements Landroid/content/DialogInterface$OnClickListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/yox_project/silver_arrow/AlertDialogUtil;->Open()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# direct methods
.method constructor <init>()V
    .locals 0

    .prologue
    .line 176
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 1
    return-void
.end method


# virtual methods
.method public onClick(Landroid/content/DialogInterface;I)V
    .locals 1
    .param p1, "dialog"    # Landroid/content/DialogInterface;
    .param p2, "which"    # I

    .prologue
    .line 182
    const/4 v0, 0x1

    sput v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iResult:I

    .line 184
    const/4 v0, 0x0

    sput v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isActive:I

    .line 185
    return-void
.end method
