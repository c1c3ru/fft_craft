.class Lcom/square_enix/FFT_Android/GL2JNIView;
.super Landroid/opengl/GLSurfaceView;
.source "GL2JNIView.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lcom/square_enix/FFT_Android/GL2JNIView$ConfigChooser;,
        Lcom/square_enix/FFT_Android/GL2JNIView$ContextFactory;,
        Lcom/square_enix/FFT_Android/GL2JNIView$Renderer;
    }
.end annotation


# static fields
.field private static final DEBUG:Z

.field private static TAG:Ljava/lang/String;

.field private static m_lTimeBegin:J


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .prologue
    .line 39
    const-string v0, "GL2JNIView"

    sput-object v0, Lcom/square_enix/FFT_Android/GL2JNIView;->TAG:Ljava/lang/String;

    .line 43
    invoke-static {}, Ljava/lang/System;->nanoTime()J

    move-result-wide v0

    sput-wide v0, Lcom/square_enix/FFT_Android/GL2JNIView;->m_lTimeBegin:J

    return-void
.end method

.method public constructor <init>(Landroid/content/Context;)V
    .locals 2
    .param p1, "context"    # Landroid/content/Context;

    .prologue
    const/4 v1, 0x0

    .line 47
    invoke-direct {p0, p1}, Landroid/opengl/GLSurfaceView;-><init>(Landroid/content/Context;)V

    .line 48
    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIView;->setEGLContextClientVersion(I)V

    .line 49
    invoke-direct {p0, v1, v1, v1}, Lcom/square_enix/FFT_Android/GL2JNIView;->init(ZII)V

    .line 50
    return-void
.end method

.method public constructor <init>(Landroid/content/Context;ZII)V
    .locals 0
    .param p1, "context"    # Landroid/content/Context;
    .param p2, "translucent"    # Z
    .param p3, "depth"    # I
    .param p4, "stencil"    # I

    .prologue
    .line 53
    invoke-direct {p0, p1}, Landroid/opengl/GLSurfaceView;-><init>(Landroid/content/Context;)V

    .line 54
    invoke-direct {p0, p2, p3, p4}, Lcom/square_enix/FFT_Android/GL2JNIView;->init(ZII)V

    .line 55
    return-void
.end method

.method static synthetic access$0()Ljava/lang/String;
    .locals 1

    .prologue
    .line 39
    sget-object v0, Lcom/square_enix/FFT_Android/GL2JNIView;->TAG:Ljava/lang/String;

    return-object v0
.end method

.method static synthetic access$1(Ljava/lang/String;Ljavax/microedition/khronos/egl/EGL10;)V
    .locals 0

    .prologue
    .line 145
    invoke-static {p0, p1}, Lcom/square_enix/FFT_Android/GL2JNIView;->checkEglError(Ljava/lang/String;Ljavax/microedition/khronos/egl/EGL10;)V

    return-void
.end method

.method static synthetic access$2()J
    .locals 2

    .prologue
    .line 43
    sget-wide v0, Lcom/square_enix/FFT_Android/GL2JNIView;->m_lTimeBegin:J

    return-wide v0
.end method

.method static synthetic access$3(J)V
    .locals 0

    .prologue
    .line 43
    sput-wide p0, Lcom/square_enix/FFT_Android/GL2JNIView;->m_lTimeBegin:J

    return-void
.end method

.method private static checkEglError(Ljava/lang/String;Ljavax/microedition/khronos/egl/EGL10;)V
    .locals 6
    .param p0, "prompt"    # Ljava/lang/String;
    .param p1, "egl"    # Ljavax/microedition/khronos/egl/EGL10;

    .prologue
    .line 147
    :goto_0
    invoke-interface {p1}, Ljavax/microedition/khronos/egl/EGL10;->eglGetError()I

    move-result v0

    .local v0, "error":I
    const/16 v1, 0x3000

    if-ne v0, v1, :cond_0

    .line 150
    return-void

    .line 148
    :cond_0
    sget-object v1, Lcom/square_enix/FFT_Android/GL2JNIView;->TAG:Ljava/lang/String;

    const-string v2, "%s: EGL error: 0x%x"

    const/4 v3, 0x2

    new-array v3, v3, [Ljava/lang/Object;

    const/4 v4, 0x0

    aput-object p0, v3, v4

    const/4 v4, 0x1

    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v5

    aput-object v5, v3, v4

    invoke-static {v2, v3}, Ljava/lang/String;->format(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0
.end method

.method private init(ZII)V
    .locals 9
    .param p1, "translucent"    # Z
    .param p2, "depth"    # I
    .param p3, "stencil"    # I

    .prologue
    const/4 v8, 0x0

    const/4 v4, 0x5

    const/4 v7, 0x0

    const/16 v1, 0x8

    .line 101
    if-eqz p1, :cond_0

    .line 102
    invoke-virtual {p0}, Lcom/square_enix/FFT_Android/GL2JNIView;->getHolder()Landroid/view/SurfaceHolder;

    move-result-object v0

    const/4 v2, -0x3

    invoke-interface {v0, v2}, Landroid/view/SurfaceHolder;->setFormat(I)V

    .line 108
    :cond_0
    new-instance v0, Lcom/square_enix/FFT_Android/GL2JNIView$ContextFactory;

    invoke-direct {v0, v8}, Lcom/square_enix/FFT_Android/GL2JNIView$ContextFactory;-><init>(Lcom/square_enix/FFT_Android/GL2JNIView$ContextFactory;)V

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIView;->setEGLContextFactory(Landroid/opengl/GLSurfaceView$EGLContextFactory;)V

    .line 116
    if-eqz p1, :cond_1

    .line 117
    new-instance v0, Lcom/square_enix/FFT_Android/GL2JNIView$ConfigChooser;

    move v2, v1

    move v3, v1

    move v4, v1

    move v5, p2

    move v6, p3

    invoke-direct/range {v0 .. v6}, Lcom/square_enix/FFT_Android/GL2JNIView$ConfigChooser;-><init>(IIIIII)V

    .line 116
    :goto_0
    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIView;->setEGLConfigChooser(Landroid/opengl/GLSurfaceView$EGLConfigChooser;)V

    .line 121
    new-instance v0, Lcom/square_enix/FFT_Android/GL2JNIView$Renderer;

    invoke-direct {v0, v8}, Lcom/square_enix/FFT_Android/GL2JNIView$Renderer;-><init>(Lcom/square_enix/FFT_Android/GL2JNIView$Renderer;)V

    invoke-virtual {p0, v0}, Lcom/square_enix/FFT_Android/GL2JNIView;->setRenderer(Landroid/opengl/GLSurfaceView$Renderer;)V

    .line 124
    invoke-virtual {p0, v7}, Lcom/square_enix/FFT_Android/GL2JNIView;->setRenderMode(I)V

    .line 125
    return-void

    .line 118
    :cond_1
    new-instance v0, Lcom/square_enix/FFT_Android/GL2JNIView$ConfigChooser;

    const/4 v2, 0x6

    move v1, v4

    move v3, v4

    move v4, v7

    move v5, p2

    move v6, p3

    invoke-direct/range {v0 .. v6}, Lcom/square_enix/FFT_Android/GL2JNIView$ConfigChooser;-><init>(IIIIII)V

    goto :goto_0
.end method


# virtual methods
.method public onTouchEvent(Landroid/view/MotionEvent;)Z
    .locals 7
    .param p1, "ev"    # Landroid/view/MotionEvent;

    .prologue
    .line 61
    invoke-virtual {p1}, Landroid/view/MotionEvent;->getActionMasked()I

    move-result v0

    .line 62
    .local v0, "action":I
    invoke-virtual {p1}, Landroid/view/MotionEvent;->getActionIndex()I

    move-result v1

    .line 63
    .local v1, "actionIndex":I
    invoke-virtual {p1, v1}, Landroid/view/MotionEvent;->getPointerId(I)I

    move-result v3

    .line 64
    .local v3, "pointerId":I
    invoke-virtual {p1}, Landroid/view/MotionEvent;->getPointerCount()I

    move-result v2

    .line 65
    .local v2, "count":I
    invoke-virtual {p1, v1}, Landroid/view/MotionEvent;->getX(I)F

    move-result v4

    .line 66
    .local v4, "x":F
    invoke-virtual {p1, v1}, Landroid/view/MotionEvent;->getY(I)F

    move-result v5

    .line 69
    .local v5, "y":F
    invoke-static {v0, v3, v4, v5, v2}, Lcom/square_enix/FFT_Android/GL2JNILib;->onTouchEvent(IIFFI)V

    .line 89
    const/4 v6, 0x1

    return v6
.end method
