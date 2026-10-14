.class Lcom/yox_project/silver_arrow/AlertDialogUtil$1;
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
    .line 155
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
    const/4 v0, 0x0

    .line 161
    sput v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iResult:I

    .line 163
    sput v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isActive:I

    .line 164
    return-void
.end method
