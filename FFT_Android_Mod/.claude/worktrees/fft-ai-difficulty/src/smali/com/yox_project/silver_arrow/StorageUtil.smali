.class public final Lcom/yox_project/silver_arrow/StorageUtil;
.super Ljava/lang/Object;
.source "StorageUtil.java"


# static fields
.field static final TAG:Ljava/lang/String; = "StorageUtil"

.field static m_hContext:Landroid/content/Context;

.field static m_isPathOBB:Z

.field static m_strPathOBB1:Ljava/lang/String;

.field static m_strPathOBB2:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .prologue
    const/4 v0, 0x0

    .line 36
    sput-object v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_hContext:Landroid/content/Context;

    .line 37
    sput-object v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_strPathOBB1:Ljava/lang/String;

    .line 38
    sput-object v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_strPathOBB2:Ljava/lang/String;

    .line 39
    const/4 v0, 0x0

    sput-boolean v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_isPathOBB:Z

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 29
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static DirCreate(Ljava/lang/String;)Z
    .locals 4
    .param p0, "pPath"    # Ljava/lang/String;

    .prologue
    const/4 v1, 0x1

    const/4 v2, 0x0

    .line 308
    new-instance v0, Ljava/io/File;

    invoke-direct {v0, p0}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 311
    .local v0, "file":Ljava/io/File;
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v3

    if-eqz v3, :cond_1

    .line 326
    :cond_0
    :goto_0
    return v1

    .line 317
    :cond_1
    invoke-virtual {v0}, Ljava/io/File;->mkdir()Z

    move-result v3

    if-nez v3, :cond_2

    move v1, v2

    .line 319
    goto :goto_0

    .line 322
    :cond_2
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v3

    if-nez v3, :cond_0

    move v1, v2

    .line 324
    goto :goto_0
.end method

.method public static DirGetFree(Ljava/lang/String;)J
    .locals 8
    .param p0, "pPath"    # Ljava/lang/String;

    .prologue
    .line 337
    const-wide/16 v6, 0x0

    .line 341
    .local v6, "lSize":J
    :try_start_0
    new-instance v0, Landroid/os/StatFs;

    invoke-direct {v0, p0}, Landroid/os/StatFs;-><init>(Ljava/lang/String;)V

    .line 342
    .local v0, "fs":Landroid/os/StatFs;
    invoke-virtual {v0}, Landroid/os/StatFs;->getBlockSize()I

    move-result v1

    int-to-long v4, v1

    .line 343
    .local v4, "lBlockSize":J
    invoke-virtual {v0}, Landroid/os/StatFs;->getAvailableBlocks()I
    :try_end_0
    .catch Ljava/lang/IllegalArgumentException; {:try_start_0 .. :try_end_0} :catch_0

    move-result v1

    int-to-long v2, v1

    .line 345
    .local v2, "lBlockNum":J
    mul-long v6, v2, v4

    .line 352
    .end local v0    # "fs":Landroid/os/StatFs;
    .end local v2    # "lBlockNum":J
    .end local v4    # "lBlockSize":J
    :goto_0
    return-wide v6

    .line 347
    :catch_0
    move-exception v1

    goto :goto_0
.end method

.method public static FileEnum(Ljava/lang/String;I)Ljava/lang/String;
    .locals 5
    .param p0, "pPath"    # Ljava/lang/String;
    .param p1, "iIndex"    # I

    .prologue
    .line 379
    new-instance v0, Ljava/io/File;

    invoke-direct {v0, p0}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 380
    .local v0, "dir":Ljava/io/File;
    invoke-virtual {v0}, Ljava/io/File;->listFiles()[Ljava/io/File;

    move-result-object v2

    .line 381
    .local v2, "files":[Ljava/io/File;
    aget-object v1, v2, p1

    .line 383
    .local v1, "file":Ljava/io/File;
    invoke-virtual {v1}, Ljava/io/File;->isDirectory()Z

    move-result v3

    if-eqz v3, :cond_0

    .line 385
    const/4 v3, 0x0

    .line 388
    :goto_0
    return-object v3

    :cond_0
    new-instance v3, Ljava/lang/String;

    invoke-virtual {v1}, Ljava/io/File;->getName()Ljava/lang/String;

    move-result-object v4

    invoke-direct {v3, v4}, Ljava/lang/String;-><init>(Ljava/lang/String;)V

    goto :goto_0
.end method

.method public static FileEnumCount(Ljava/lang/String;)I
    .locals 3
    .param p0, "pPath"    # Ljava/lang/String;

    .prologue
    .line 365
    new-instance v0, Ljava/io/File;

    invoke-direct {v0, p0}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 366
    .local v0, "dir":Ljava/io/File;
    invoke-virtual {v0}, Ljava/io/File;->listFiles()[Ljava/io/File;

    move-result-object v1

    .line 368
    .local v1, "files":[Ljava/io/File;
    array-length v2, v1

    return v2
.end method

.method public static GetExt1OBBPath()Ljava/lang/String;
    .locals 1

    .prologue
    .line 142
    sget-object v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_strPathOBB1:Ljava/lang/String;

    return-object v0
.end method

.method public static GetExt1Path()Ljava/lang/String;
    .locals 2

    .prologue
    .line 105
    sget-object v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_hContext:Landroid/content/Context;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

    move-result-object v0

    invoke-virtual {v0}, Ljava/io/File;->getPath()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public static GetExt1RootPath()Ljava/lang/String;
    .locals 1

    .prologue
    .line 124
    invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;

    move-result-object v0

    invoke-virtual {v0}, Ljava/io/File;->getPath()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public static GetExt2OBBPath()Ljava/lang/String;
    .locals 1

    .prologue
    .line 158
    sget-object v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_strPathOBB2:Ljava/lang/String;

    return-object v0
.end method

.method public static GetExt2Path()Ljava/lang/String;
    .locals 4

    .prologue
    .line 229
    const-string v2, "EXTERNAL_ALT_STORAGE"

    invoke-static {v2}, Ljava/lang/System;->getenv(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 230
    .local v1, "strPath":Ljava/lang/String;
    if-eqz v1, :cond_1

    .line 262
    :cond_0
    :goto_0
    return-object v1

    .line 236
    :cond_1
    const-string v2, "EXTERNAL_STORAGE2"

    invoke-static {v2}, Ljava/lang/System;->getenv(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 237
    if-nez v1, :cond_0

    .line 244
    const-string v2, "EXTERNAL_STORAGE"

    invoke-static {v2}, Ljava/lang/System;->getenv(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    .line 246
    if-nez v1, :cond_2

    .line 248
    invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;

    move-result-object v2

    invoke-virtual {v2}, Ljava/io/File;->getPath()Ljava/lang/String;

    move-result-object v1

    .line 256
    :cond_2
    new-instance v0, Ljava/io/File;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-static {v1}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v3

    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v3, "/ext_sd"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-direct {v0, v2}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 257
    .local v0, "file":Ljava/io/File;
    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v2

    if-eqz v2, :cond_0

    .line 259
    invoke-virtual {v0}, Ljava/io/File;->getPath()Ljava/lang/String;

    move-result-object v1

    goto :goto_0
.end method

.method public static GetIntPath()Ljava/lang/String;
    .locals 1

    .prologue
    .line 84
    sget-object v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_hContext:Landroid/content/Context;

    invoke-virtual {v0}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v0

    invoke-virtual {v0}, Ljava/io/File;->getPath()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public static Init(Landroid/content/Context;)V
    .locals 8
    .param p0, "hContext"    # Landroid/content/Context;

    .prologue
    const-wide/16 v6, 0x400

    .line 52
    sput-object p0, Lcom/yox_project/silver_arrow/StorageUtil;->m_hContext:Landroid/content/Context;

    .line 58
    const-string v2, "StorageUtil"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "internal   path = ["

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetIntPath()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "]"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 59
    const-string v2, "StorageUtil"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "external 1 path = ["

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt1Path()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "]"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 60
    const-string v2, "StorageUtil"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "external 2 path = ["

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt2Path()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "]"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 61
    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetIntPath()Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Lcom/yox_project/silver_arrow/StorageUtil;->DirGetFree(Ljava/lang/String;)J

    move-result-wide v0

    .line 62
    .local v0, "lFree":J
    const-string v2, "StorageUtil"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "internal   free = "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    div-long v4, v0, v6

    div-long/2addr v4, v6

    invoke-virtual {v3, v4, v5}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, " MB"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 63
    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt1Path()Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Lcom/yox_project/silver_arrow/StorageUtil;->DirGetFree(Ljava/lang/String;)J

    move-result-wide v0

    .line 64
    const-string v2, "StorageUtil"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "external 1 free = "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    div-long v4, v0, v6

    div-long/2addr v4, v6

    invoke-virtual {v3, v4, v5}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, " MB"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 65
    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt2Path()Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Lcom/yox_project/silver_arrow/StorageUtil;->DirGetFree(Ljava/lang/String;)J

    move-result-wide v0

    .line 66
    const-string v2, "StorageUtil"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "external 2 free = "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    div-long v4, v0, v6

    div-long/2addr v4, v6

    invoke-virtual {v3, v4, v5}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, " MB"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 68
    return-void
.end method

.method public static IsDir(Ljava/lang/String;)Z
    .locals 2
    .param p0, "pPath"    # Ljava/lang/String;

    .prologue
    .line 290
    :try_start_0
    new-instance v0, Ljava/io/File;

    invoke-direct {v0, p0}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    .line 292
    .local v0, "file":Ljava/io/File;
    invoke-virtual {v0}, Ljava/io/File;->isDirectory()Z
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result v1

    .line 297
    .end local v0    # "file":Ljava/io/File;
    :goto_0
    return v1

    .line 293
    :catch_0
    move-exception v1

    .line 297
    const/4 v1, 0x0

    goto :goto_0
.end method

.method public static IsOBBPath()Z
    .locals 1

    .prologue
    .line 203
    sget-boolean v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_isPathOBB:Z

    return v0
.end method

.method public static SetExt1OBBPath(Ljava/lang/String;)V
    .locals 1
    .param p0, "strPath"    # Ljava/lang/String;

    .prologue
    .line 176
    sput-object p0, Lcom/yox_project/silver_arrow/StorageUtil;->m_strPathOBB1:Ljava/lang/String;

    .line 177
    const/4 v0, 0x1

    sput-boolean v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_isPathOBB:Z

    .line 178
    return-void
.end method

.method public static SetExt2OBBPath(Ljava/lang/String;)V
    .locals 0
    .param p0, "strPath"    # Ljava/lang/String;

    .prologue
    .line 193
    sput-object p0, Lcom/yox_project/silver_arrow/StorageUtil;->m_strPathOBB2:Ljava/lang/String;

    .line 194
    return-void
.end method

.method public static getCacheDir()Ljava/lang/String;
    .locals 1

    .prologue
    .line 275
    sget-object v0, Lcom/yox_project/silver_arrow/StorageUtil;->m_hContext:Landroid/content/Context;

    invoke-virtual {v0}, Landroid/content/Context;->getCacheDir()Ljava/io/File;

    move-result-object v0

    invoke-virtual {v0}, Ljava/io/File;->getPath()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method
