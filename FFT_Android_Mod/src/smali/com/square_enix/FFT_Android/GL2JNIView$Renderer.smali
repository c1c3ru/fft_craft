.class Lcom/square_enix/FFT_Android/GL2JNIView$Renderer;
.super Ljava/lang/Object;
.source "GL2JNIView.java"

# interfaces
.implements Landroid/opengl/GLSurfaceView$Renderer;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lcom/square_enix/FFT_Android/GL2JNIView;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0xa
    name = "Renderer"
.end annotation


# direct methods
.method private constructor <init>()V
    .locals 0

    .prologue
    .line 345
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method synthetic constructor <init>(Lcom/square_enix/FFT_Android/GL2JNIView$Renderer;)V
    .locals 0

    .prologue
    .line 345
    invoke-direct {p0}, Lcom/square_enix/FFT_Android/GL2JNIView$Renderer;-><init>()V

    return-void
.end method


# virtual methods
.method public onDrawFrame(Ljavax/microedition/khronos/opengles/GL10;)V
    .locals 14
    .param p1, "gl"    # Ljavax/microedition/khronos/opengles/GL10;

    .prologue
    .line 349
    invoke-static {}, Ljava/lang/System;->nanoTime()J

    move-result-wide v6

    .line 350
    .local v6, "lEndTime":J
    invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNIView;->access$2()J

    move-result-wide v12

    sub-long v2, v6, v12

    .line 353
    .local v2, "lDelta":J
    const-wide/32 v12, 0x1fca055

    cmp-long v1, v2, v12

    if-gez v1, :cond_0

    .line 357
    const-wide/32 v12, 0x1fca055

    sub-long v4, v12, v2

    .line 358
    .local v4, "lDiff":J
    const-wide/32 v12, 0xf4240

    :try_start_0
    div-long v8, v4, v12

    .line 359
    .local v8, "lMSec":J
    const-wide/32 v12, 0xf4240

    rem-long v10, v4, v12

    .line 362
    .local v10, "lNSec":J
    long-to-int v1, v10

    invoke-static {v8, v9, v1}, Ljava/lang/Thread;->sleep(JI)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 368
    .end local v8    # "lMSec":J
    .end local v10    # "lNSec":J
    :goto_0
    invoke-static {}, Ljava/lang/System;->nanoTime()J

    move-result-wide v12

    invoke-static {v12, v13}, Lcom/square_enix/FFT_Android/GL2JNIView;->access$3(J)V

    .line 378
    .end local v4    # "lDiff":J
    :goto_1
    invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNILib;->step()V

    .line 380
    return-void

    .line 364
    .restart local v4    # "lDiff":J
    :catch_0
    move-exception v0

    .line 366
    .local v0, "e":Ljava/lang/Exception;
    invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNIView;->access$0()Ljava/lang/String;

    move-result-object v1

    const-string v12, "Exception: "

    invoke-static {v1, v12}, Lcom/yox_project/silver_arrow/LOG;->e(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_0

    .line 374
    .end local v0    # "e":Ljava/lang/Exception;
    .end local v4    # "lDiff":J
    :cond_0
    invoke-static {v6, v7}, Lcom/square_enix/FFT_Android/GL2JNIView;->access$3(J)V

    goto :goto_1
.end method

.method public onSurfaceChanged(Ljavax/microedition/khronos/opengles/GL10;II)V
    .locals 2
    .param p1, "gl"    # Ljavax/microedition/khronos/opengles/GL10;
    .param p2, "width"    # I
    .param p3, "height"    # I

    .prologue
    .line 383
    invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNIView;->access$0()Ljava/lang/String;

    move-result-object v0

    const-string v1, "onSurfaceChanged"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->w(Ljava/lang/String;Ljava/lang/String;)V

    .line 385
    invoke-static {p2, p3}, Lcom/square_enix/FFT_Android/GL2JNILib;->init(II)V

    .line 386
    return-void
.end method

.method public onSurfaceCreated(Ljavax/microedition/khronos/opengles/GL10;Ljavax/microedition/khronos/egl/EGLConfig;)V
    .locals 2
    .param p1, "gl"    # Ljavax/microedition/khronos/opengles/GL10;
    .param p2, "config"    # Ljavax/microedition/khronos/egl/EGLConfig;

    .prologue
    .line 389
    invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNIView;->access$0()Ljava/lang/String;

    move-result-object v0

    const-string v1, "onSurfaceCreated"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->w(Ljava/lang/String;Ljava/lang/String;)V

    .line 391
    return-void
.end method
