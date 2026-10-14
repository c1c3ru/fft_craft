.class public final Lcom/yox_project/silver_arrow/AlertDialogUtil;
.super Ljava/lang/Object;
.source "AlertDialogUtil.java"


# static fields
.field static final TAG:Ljava/lang/String; = "AlertDialogUtil"

.field static m_hContext:Landroid/content/Context;

.field static m_iID:I

.field static m_iIconID:I

.field static m_iResult:I

.field static m_iType:I

.field static m_isActive:I

.field static m_isRequest:I

.field static m_strBtnCancel:Ljava/lang/String;

.field static m_strBtnOK:Ljava/lang/String;

.field static m_strMessage:Ljava/lang/String;

.field static m_strTitle:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .locals 3

    .prologue
    const/4 v2, 0x0

    const/4 v1, -0x1

    const/4 v0, 0x0

    .line 36
    sput-object v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_hContext:Landroid/content/Context;

    .line 38
    sput v2, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isRequest:I

    .line 39
    sput v2, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isActive:I

    .line 40
    sput v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iResult:I

    .line 42
    sput v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iID:I

    .line 43
    sput v2, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iType:I

    .line 44
    sput v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iIconID:I

    .line 45
    sput-object v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strTitle:Ljava/lang/String;

    .line 46
    sput-object v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strMessage:Ljava/lang/String;

    .line 47
    sput-object v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strBtnOK:Ljava/lang/String;

    .line 48
    sput-object v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strBtnCancel:Ljava/lang/String;

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 28
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static Close()V
    .locals 2

    .prologue
    .line 222
    const-string v0, "AlertDialogUtil"

    const-string v1, "Close"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 223
    const/4 v0, -0x1

    sput v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iResult:I

    .line 224
    return-void
.end method

.method public static GetActive()I
    .locals 1

    .prologue
    .line 234
    sget v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isActive:I

    return v0
.end method

.method public static GetID()I
    .locals 1

    .prologue
    .line 200
    sget v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iID:I

    return v0
.end method

.method public static GetRequest()I
    .locals 1

    .prologue
    .line 105
    sget v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isRequest:I

    return v0
.end method

.method public static GetResult()I
    .locals 1

    .prologue
    .line 211
    sget v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iResult:I

    return v0
.end method

.method public static Init(Landroid/content/Context;)V
    .locals 1
    .param p0, "hContext"    # Landroid/content/Context;

    .prologue
    const/4 v0, 0x0

    .line 61
    sput-object p0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_hContext:Landroid/content/Context;

    .line 63
    sput v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isRequest:I

    .line 64
    sput v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isActive:I

    .line 65
    const/4 v0, -0x1

    sput v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iResult:I

    .line 66
    return-void
.end method

.method public static Open()V
    .locals 4

    .prologue
    const/4 v3, 0x1

    .line 127
    const-string v1, "AlertDialogUtil"

    const-string v2, "Open"

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 130
    sput v3, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isActive:I

    .line 132
    new-instance v0, Landroid/app/AlertDialog$Builder;

    sget-object v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_hContext:Landroid/content/Context;

    invoke-direct {v0, v1}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V

    .line 135
    .local v0, "alertDialogBuilder":Landroid/app/AlertDialog$Builder;
    sget-object v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strTitle:Ljava/lang/String;

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setTitle(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    .line 137
    sget-object v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strMessage:Ljava/lang/String;

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setMessage(Ljava/lang/CharSequence;)Landroid/app/AlertDialog$Builder;

    .line 139
    sget v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iIconID:I

    const/4 v2, -0x1

    if-eq v1, v2, :cond_0

    .line 149
    sget v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iIconID:I

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setIcon(I)Landroid/app/AlertDialog$Builder;

    .line 152
    :cond_0
    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroid/app/AlertDialog$Builder;->setCancelable(Z)Landroid/app/AlertDialog$Builder;

    .line 155
    sget-object v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strBtnOK:Ljava/lang/String;

    new-instance v2, Lcom/yox_project/silver_arrow/AlertDialogUtil$1;

    invoke-direct {v2}, Lcom/yox_project/silver_arrow/AlertDialogUtil$1;-><init>()V

    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setPositiveButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    .line 174
    sget v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iType:I

    if-ne v1, v3, :cond_1

    .line 176
    sget-object v1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strBtnCancel:Ljava/lang/String;

    new-instance v2, Lcom/yox_project/silver_arrow/AlertDialogUtil$2;

    invoke-direct {v2}, Lcom/yox_project/silver_arrow/AlertDialogUtil$2;-><init>()V

    invoke-virtual {v0, v1, v2}, Landroid/app/AlertDialog$Builder;->setNegativeButton(Ljava/lang/CharSequence;Landroid/content/DialogInterface$OnClickListener;)Landroid/app/AlertDialog$Builder;

    .line 189
    :cond_1
    invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->create()Landroid/app/AlertDialog;

    move-result-object v1

    invoke-virtual {v1}, Landroid/app/AlertDialog;->show()V

    .line 190
    return-void
.end method

.method public static OpenRequest(IIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 2
    .param p0, "iID"    # I
    .param p1, "iType"    # I
    .param p2, "iIconID"    # I
    .param p3, "strBtnOK"    # Ljava/lang/String;
    .param p4, "strBtnCancel"    # Ljava/lang/String;
    .param p5, "strTitle"    # Ljava/lang/String;
    .param p6, "strMessage"    # Ljava/lang/String;

    .prologue
    .line 81
    const-string v0, "AlertDialogUtil"

    const-string v1, "OpenRequest"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 84
    sput p0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iID:I

    .line 85
    sput p1, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iType:I

    .line 86
    sput p2, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_iIconID:I

    .line 88
    sput-object p3, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strBtnOK:Ljava/lang/String;

    .line 89
    sput-object p4, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strBtnCancel:Ljava/lang/String;

    .line 90
    sput-object p5, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strTitle:Ljava/lang/String;

    .line 91
    sput-object p6, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_strMessage:Ljava/lang/String;

    .line 94
    const/4 v0, 0x1

    sput v0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isRequest:I

    .line 95
    return-void
.end method

.method public static SetRequest(I)V
    .locals 0
    .param p0, "isRequest"    # I

    .prologue
    .line 116
    sput p0, Lcom/yox_project/silver_arrow/AlertDialogUtil;->m_isRequest:I

    .line 117
    return-void
.end method
