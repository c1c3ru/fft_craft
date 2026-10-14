.class public final Lcom/yox_project/silver_arrow/WebUtil;
.super Ljava/lang/Object;
.source "WebUtil.java"


# static fields
.field static final TAG:Ljava/lang/String; = "WebUtil"

.field static m_hContext:Landroid/content/Context;

.field static m_isRequest:I

.field static m_strURL:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .prologue
    const/4 v1, 0x0

    .line 36
    sput-object v1, Lcom/yox_project/silver_arrow/WebUtil;->m_hContext:Landroid/content/Context;

    .line 38
    const/4 v0, 0x0

    sput v0, Lcom/yox_project/silver_arrow/WebUtil;->m_isRequest:I

    .line 40
    sput-object v1, Lcom/yox_project/silver_arrow/WebUtil;->m_strURL:Ljava/lang/String;

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 28
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static GetRequest()I
    .locals 1

    .prologue
    .line 84
    sget v0, Lcom/yox_project/silver_arrow/WebUtil;->m_isRequest:I

    return v0
.end method

.method public static Init(Landroid/content/Context;)V
    .locals 1
    .param p0, "hContext"    # Landroid/content/Context;

    .prologue
    .line 53
    sput-object p0, Lcom/yox_project/silver_arrow/WebUtil;->m_hContext:Landroid/content/Context;

    .line 55
    const/4 v0, 0x0

    sput v0, Lcom/yox_project/silver_arrow/WebUtil;->m_isRequest:I

    .line 56
    return-void
.end method

.method public static Open()V
    .locals 4

    .prologue
    .line 106
    const-string v2, "WebUtil"

    const-string v3, "Open"

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 109
    sget-object v2, Lcom/yox_project/silver_arrow/WebUtil;->m_strURL:Ljava/lang/String;

    invoke-static {v2}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v1

    .line 110
    .local v1, "uri":Landroid/net/Uri;
    new-instance v0, Landroid/content/Intent;

    const-string v2, "android.intent.action.VIEW"

    invoke-direct {v0, v2, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;Landroid/net/Uri;)V

    .line 111
    .local v0, "i":Landroid/content/Intent;
    sget-object v2, Lcom/yox_project/silver_arrow/WebUtil;->m_hContext:Landroid/content/Context;

    invoke-virtual {v2, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V

    .line 113
    return-void
.end method

.method public static OpenRequest(Ljava/lang/String;)V
    .locals 2
    .param p0, "strURL"    # Ljava/lang/String;

    .prologue
    .line 67
    const-string v0, "WebUtil"

    const-string v1, "OpenRequest"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 70
    sput-object p0, Lcom/yox_project/silver_arrow/WebUtil;->m_strURL:Ljava/lang/String;

    .line 73
    const/4 v0, 0x1

    sput v0, Lcom/yox_project/silver_arrow/WebUtil;->m_isRequest:I

    .line 74
    return-void
.end method

.method public static SetRequest(I)V
    .locals 0
    .param p0, "isRequest"    # I

    .prologue
    .line 95
    sput p0, Lcom/yox_project/silver_arrow/WebUtil;->m_isRequest:I

    .line 96
    return-void
.end method
