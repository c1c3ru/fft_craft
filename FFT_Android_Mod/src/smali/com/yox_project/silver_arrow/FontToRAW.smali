.class public final Lcom/yox_project/silver_arrow/FontToRAW;
.super Ljava/lang/Object;
.source "FontToRAW.java"


# static fields
.field static final PADDING_LEFT:I = 0x0

.field static final TAG:Ljava/lang/String; = "FontToRAW"

.field static m_hContext:Landroid/content/Context;

.field static m_iFontSize:I

.field static m_iImageH:I

.field static m_iImageW:I

.field static m_pRAW:[I


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .prologue
    const/4 v1, 0x0

    const/4 v0, 0x0

    .line 41
    sput-object v1, Lcom/yox_project/silver_arrow/FontToRAW;->m_hContext:Landroid/content/Context;

    .line 43
    sput v0, Lcom/yox_project/silver_arrow/FontToRAW;->m_iFontSize:I

    .line 45
    sput-object v1, Lcom/yox_project/silver_arrow/FontToRAW;->m_pRAW:[I

    .line 46
    sput v0, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageW:I

    .line 47
    sput v0, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageH:I

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 32
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static GetBuffer()[I
    .locals 1

    .prologue
    .line 144
    sget-object v0, Lcom/yox_project/silver_arrow/FontToRAW;->m_pRAW:[I

    return-object v0
.end method

.method public static GetH()I
    .locals 1

    .prologue
    .line 166
    sget v0, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageH:I

    return v0
.end method

.method private static GetTextH(Landroid/graphics/Paint$FontMetrics;)I
    .locals 4
    .param p0, "fontMetrics"    # Landroid/graphics/Paint$FontMetrics;

    .prologue
    .line 185
    iget v1, p0, Landroid/graphics/Paint$FontMetrics;->ascent:F

    invoke-static {v1}, Ljava/lang/Math;->abs(F)F

    move-result v1

    iget v2, p0, Landroid/graphics/Paint$FontMetrics;->descent:F

    invoke-static {v2}, Ljava/lang/Math;->abs(F)F

    move-result v2

    add-float/2addr v1, v2

    iget v2, p0, Landroid/graphics/Paint$FontMetrics;->descent:F

    invoke-static {v2}, Ljava/lang/Math;->abs(F)F

    move-result v2

    add-float/2addr v1, v2

    float-to-double v2, v1

    .line 184
    invoke-static {v2, v3}, Ljava/lang/Math;->ceil(D)D

    move-result-wide v2

    double-to-int v0, v2

    .line 187
    .local v0, "iH":I
    return v0
.end method

.method private static GetTextW(Landroid/graphics/Paint;Ljava/lang/String;)I
    .locals 2
    .param p0, "textPaint"    # Landroid/graphics/Paint;
    .param p1, "text"    # Ljava/lang/String;

    .prologue
    .line 175
    invoke-virtual {p0, p1}, Landroid/graphics/Paint;->measureText(Ljava/lang/String;)F

    move-result v0

    float-to-double v0, v0

    invoke-static {v0, v1}, Ljava/lang/Math;->ceil(D)D

    move-result-wide v0

    double-to-int v0, v0

    add-int/lit8 v0, v0, 0x0

    return v0
.end method

.method public static GetW()I
    .locals 1

    .prologue
    .line 155
    sget v0, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageW:I

    return v0
.end method

.method public static Init(Landroid/content/Context;)V
    .locals 0
    .param p0, "hContext"    # Landroid/content/Context;

    .prologue
    .line 60
    sput-object p0, Lcom/yox_project/silver_arrow/FontToRAW;->m_hContext:Landroid/content/Context;

    .line 61
    return-void
.end method

.method public static Render(Ljava/lang/String;)V
    .locals 11
    .param p0, "str"    # Ljava/lang/String;

    .prologue
    const/4 v2, 0x0

    .line 99
    new-instance v10, Landroid/graphics/Paint;

    invoke-direct {v10}, Landroid/graphics/Paint;-><init>()V

    .line 100
    .local v10, "paint":Landroid/graphics/Paint;
    const/4 v1, 0x1

    invoke-virtual {v10, v1}, Landroid/graphics/Paint;->setAntiAlias(Z)V

    .line 101
    sget v1, Lcom/yox_project/silver_arrow/FontToRAW;->m_iFontSize:I

    int-to-float v1, v1

    invoke-virtual {v10, v1}, Landroid/graphics/Paint;->setTextSize(F)V

    .line 107
    invoke-virtual {v10}, Landroid/graphics/Paint;->getFontMetrics()Landroid/graphics/Paint$FontMetrics;

    move-result-object v9

    .line 108
    .local v9, "fontMetrics":Landroid/graphics/Paint$FontMetrics;
    invoke-static {v10, p0}, Lcom/yox_project/silver_arrow/FontToRAW;->GetTextW(Landroid/graphics/Paint;Ljava/lang/String;)I

    move-result v1

    sput v1, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageW:I

    .line 109
    invoke-static {v9}, Lcom/yox_project/silver_arrow/FontToRAW;->GetTextH(Landroid/graphics/Paint$FontMetrics;)I

    move-result v1

    sput v1, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageH:I

    .line 113
    sget v1, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageW:I

    sget v3, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageH:I

    sget-object v4, Landroid/graphics/Bitmap$Config;->ARGB_8888:Landroid/graphics/Bitmap$Config;

    invoke-static {v1, v3, v4}, Landroid/graphics/Bitmap;->createBitmap(IILandroid/graphics/Bitmap$Config;)Landroid/graphics/Bitmap;

    move-result-object v0

    .line 117
    .local v0, "image":Landroid/graphics/Bitmap;
    new-instance v8, Landroid/graphics/Canvas;

    invoke-direct {v8, v0}, Landroid/graphics/Canvas;-><init>(Landroid/graphics/Bitmap;)V

    .line 120
    .local v8, "canvas":Landroid/graphics/Canvas;
    const/4 v1, 0x0

    iget v3, v9, Landroid/graphics/Paint$FontMetrics;->ascent:F

    invoke-static {v3}, Ljava/lang/Math;->abs(F)F

    move-result v3

    invoke-virtual {v8, p0, v1, v3, v10}, Landroid/graphics/Canvas;->drawText(Ljava/lang/String;FFLandroid/graphics/Paint;)V

    .line 127
    sget v1, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageW:I

    sget v3, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageH:I

    mul-int/2addr v1, v3

    new-array v1, v1, [I

    sput-object v1, Lcom/yox_project/silver_arrow/FontToRAW;->m_pRAW:[I

    .line 129
    sget-object v1, Lcom/yox_project/silver_arrow/FontToRAW;->m_pRAW:[I

    sget v3, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageW:I

    sget v6, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageW:I

    sget v7, Lcom/yox_project/silver_arrow/FontToRAW;->m_iImageH:I

    move v4, v2

    move v5, v2

    invoke-virtual/range {v0 .. v7}, Landroid/graphics/Bitmap;->getPixels([IIIIIII)V

    .line 130
    invoke-virtual {v0}, Landroid/graphics/Bitmap;->recycle()V

    .line 134
    return-void
.end method

.method public static SetStyle(I)V
    .locals 0
    .param p0, "iFontSize"    # I

    .prologue
    .line 77
    sput p0, Lcom/yox_project/silver_arrow/FontToRAW;->m_iFontSize:I

    .line 78
    return-void
.end method
