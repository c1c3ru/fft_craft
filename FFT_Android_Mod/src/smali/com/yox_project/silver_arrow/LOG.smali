.class public Lcom/yox_project/silver_arrow/LOG;
.super Ljava/lang/Object;
.source "LOG.java"


# static fields
.field private static m_isOutput:Z


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .prologue
    .line 27
    const/4 v0, 0x0

    sput-boolean v0, Lcom/yox_project/silver_arrow/LOG;->m_isOutput:Z

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 24
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static final IsOutput()Z
    .locals 1

    .prologue
    .line 33
    sget-boolean v0, Lcom/yox_project/silver_arrow/LOG;->m_isOutput:Z

    return v0
.end method

.method public static final d(Ljava/lang/String;Ljava/lang/String;)V
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;

    .prologue
    .line 38
    sget-boolean v0, Lcom/yox_project/silver_arrow/LOG;->m_isOutput:Z

    if-eqz v0, :cond_0

    .line 40
    invoke-static {p0, p1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 42
    :cond_0
    return-void
.end method

.method public static final e(Ljava/lang/String;Ljava/lang/String;)V
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;

    .prologue
    .line 59
    sget-boolean v0, Lcom/yox_project/silver_arrow/LOG;->m_isOutput:Z

    if-eqz v0, :cond_0

    .line 61
    invoke-static {p0, p1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 63
    :cond_0
    return-void
.end method

.method public static final i(Ljava/lang/String;Ljava/lang/String;)V
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;

    .prologue
    .line 45
    sget-boolean v0, Lcom/yox_project/silver_arrow/LOG;->m_isOutput:Z

    if-eqz v0, :cond_0

    .line 47
    invoke-static {p0, p1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 49
    :cond_0
    return-void
.end method

.method public static final w(Ljava/lang/String;Ljava/lang/String;)V
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;

    .prologue
    .line 52
    sget-boolean v0, Lcom/yox_project/silver_arrow/LOG;->m_isOutput:Z

    if-eqz v0, :cond_0

    .line 54
    invoke-static {p0, p1}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;)I

    .line 56
    :cond_0
    return-void
.end method
