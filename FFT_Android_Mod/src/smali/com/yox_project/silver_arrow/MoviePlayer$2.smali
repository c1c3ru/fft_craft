.class Lcom/yox_project/silver_arrow/MoviePlayer$2;
.super Ljava/lang/Object;
.source "MoviePlayer.java"

# interfaces
.implements Landroid/view/View$OnTouchListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/yox_project/silver_arrow/MoviePlayer;->OpenSkipDialog()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# direct methods
.method constructor <init>()V
    .locals 0

    .prologue
    .line 199
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 1
    return-void
.end method


# virtual methods
.method public onTouch(Landroid/view/View;Landroid/view/MotionEvent;)Z
    .locals 1
    .param p1, "v"    # Landroid/view/View;
    .param p2, "event"    # Landroid/view/MotionEvent;

    .prologue
    .line 202
    const/4 v0, 0x2

    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_iSkipResult:I

    .line 203
    sget-object v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v0}, Landroid/app/Dialog;->dismiss()V

    .line 204
    const/4 v0, 0x1

    return v0
.end method
