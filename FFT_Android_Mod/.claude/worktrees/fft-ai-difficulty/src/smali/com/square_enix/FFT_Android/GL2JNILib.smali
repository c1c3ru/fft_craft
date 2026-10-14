.class public Lcom/square_enix/FFT_Android/GL2JNILib;
.super Ljava/lang/Object;
.source "GL2JNILib.java"


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .prologue
    .line 24
    const-string v0, "gl2jni"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    .line 25
    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 21
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static native dialogOnClose(I)V
.end method

.method public static native getCommand()I
.end method

.method public static native init(II)V
.end method

.method public static native isExit()I
.end method

.method public static native onDestroy()V
.end method

.method public static native onKeyEvent(I)V
.end method

.method public static native onPause()V
.end method

.method public static native onResume()V
.end method

.method public static native onTouchEvent(IIFFI)V
.end method

.method public static native setAccelerometerValue(FFF)V
.end method

.method public static native setBatteryLevel(I)V
.end method

.method public static native step()V
.end method
