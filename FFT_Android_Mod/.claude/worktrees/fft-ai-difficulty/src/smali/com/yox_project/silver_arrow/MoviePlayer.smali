.class public final Lcom/yox_project/silver_arrow/MoviePlayer;
.super Ljava/lang/Object;
.source "MoviePlayer.java"

# interfaces
.implements Landroid/view/View$OnTouchListener;


# static fields
.field public static final SKIP_CANSEL:I = 0x2

.field public static final SKIP_OK:I = 0x1

.field static final TAG:Ljava/lang/String; = "MoviePlayer"

.field static m_dialog:Landroid/app/Dialog;

.field static m_hContext:Landroid/content/Context;

.field static m_iSkipResult:I

.field static m_isPlaying:I

.field static m_isRequest:I

.field static m_strMovieFile:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .prologue
    const/4 v1, 0x0

    const/4 v0, 0x0

    .line 48
    sput-object v1, Lcom/yox_project/silver_arrow/MoviePlayer;->m_hContext:Landroid/content/Context;

    .line 51
    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isRequest:I

    .line 52
    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isPlaying:I

    .line 54
    sput-object v1, Lcom/yox_project/silver_arrow/MoviePlayer;->m_strMovieFile:Ljava/lang/String;

    .line 56
    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_iSkipResult:I

    .line 58
    sput-object v1, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 38
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static CloseSkipDialog()V
    .locals 1

    .prologue
    .line 249
    sget-object v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    if-eqz v0, :cond_0

    sget-object v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v0}, Landroid/app/Dialog;->isShowing()Z

    move-result v0

    if-nez v0, :cond_1

    .line 252
    :cond_0
    :goto_0
    return-void

    .line 250
    :cond_1
    sget-object v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v0}, Landroid/app/Dialog;->dismiss()V

    .line 251
    const/4 v0, 0x0

    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_iSkipResult:I

    goto :goto_0
.end method

.method public static GetMovieFileName()Ljava/lang/String;
    .locals 1

    .prologue
    .line 261
    sget-object v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_strMovieFile:Ljava/lang/String;

    return-object v0
.end method

.method public static GetPlaying()I
    .locals 1

    .prologue
    .line 131
    sget v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isPlaying:I

    return v0
.end method

.method public static GetRequest()I
    .locals 1

    .prologue
    .line 109
    sget v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isRequest:I

    return v0
.end method

.method public static GetSkipResult()I
    .locals 1

    .prologue
    .line 271
    sget v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_iSkipResult:I

    return v0
.end method

.method public static Init(Landroid/content/Context;)V
    .locals 1
    .param p0, "hContext"    # Landroid/content/Context;

    .prologue
    const/4 v0, 0x0

    .line 70
    sput-object p0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_hContext:Landroid/content/Context;

    .line 72
    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isRequest:I

    .line 73
    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isPlaying:I

    .line 75
    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_iSkipResult:I

    .line 76
    return-void
.end method

.method public static OpenRequest(Ljava/lang/String;)V
    .locals 3
    .param p0, "strMovieFile"    # Ljava/lang/String;

    .prologue
    const/4 v2, 0x1

    .line 89
    const-string v0, "MoviePlayer"

    const-string v1, "OpenRequest"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 92
    sput-object p0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_strMovieFile:Ljava/lang/String;

    .line 95
    sput v2, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isRequest:I

    .line 96
    sput v2, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isPlaying:I

    .line 98
    const/4 v0, 0x0

    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_iSkipResult:I

    .line 99
    return-void
.end method

.method public static OpenSkipDialog()V
    .locals 15

    .prologue
    const/16 v14, 0xf

    const/16 v13, 0x8

    const/4 v12, 0x1

    const/4 v11, -0x2

    const/4 v10, 0x0

    .line 153
    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    if-eqz v8, :cond_0

    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v8}, Landroid/app/Dialog;->isShowing()Z

    move-result v8

    if-eqz v8, :cond_0

    .line 240
    .local v0, "iv":Landroid/widget/ImageView;
    .local v1, "iv_no":Landroid/widget/ImageView;
    .local v2, "iv_yes":Landroid/widget/ImageView;
    .local v3, "lyt_main":Landroid/widget/RelativeLayout;
    .local v4, "path":Ljava/lang/String;
    .local v5, "skip_btn_no":Landroid/widget/RelativeLayout$LayoutParams;
    .local v6, "skip_btn_yes":Landroid/widget/RelativeLayout$LayoutParams;
    .local v7, "skip_msg":Landroid/widget/RelativeLayout$LayoutParams;
    :goto_0
    return-void

    .line 155
    .end local v0    # "iv":Landroid/widget/ImageView;
    .end local v1    # "iv_no":Landroid/widget/ImageView;
    .end local v2    # "iv_yes":Landroid/widget/ImageView;
    .end local v3    # "lyt_main":Landroid/widget/RelativeLayout;
    .end local v4    # "path":Ljava/lang/String;
    .end local v5    # "skip_btn_no":Landroid/widget/RelativeLayout$LayoutParams;
    .end local v6    # "skip_btn_yes":Landroid/widget/RelativeLayout$LayoutParams;
    .end local v7    # "skip_msg":Landroid/widget/RelativeLayout$LayoutParams;
    :cond_0
    const-string v8, "MoviePlayer"

    const-string v9, "OpenSkipDialog"

    invoke-static {v8, v9}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 157
    sput v10, Lcom/yox_project/silver_arrow/MoviePlayer;->m_iSkipResult:I

    .line 159
    const/4 v4, 0x0

    .line 160
    .restart local v4    # "path":Ljava/lang/String;
    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->IsOBBPath()Z

    move-result v8

    if-eqz v8, :cond_1

    .line 162
    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt1OBBPath()Ljava/lang/String;

    move-result-object v4

    .line 171
    :goto_1
    new-instance v0, Landroid/widget/ImageView;

    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_hContext:Landroid/content/Context;

    invoke-direct {v0, v8}, Landroid/widget/ImageView;-><init>(Landroid/content/Context;)V

    .line 173
    .restart local v0    # "iv":Landroid/widget/ImageView;
    new-instance v8, Ljava/lang/StringBuilder;

    invoke-static {v4}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v9

    invoke-direct {v8, v9}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v9, "/base/movie/skip_msg@2x.png"

    invoke-virtual {v8, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v8

    invoke-virtual {v8}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v8

    invoke-static {v8}, Landroid/graphics/BitmapFactory;->decodeFile(Ljava/lang/String;)Landroid/graphics/Bitmap;

    move-result-object v8

    invoke-virtual {v0, v8}, Landroid/widget/ImageView;->setImageBitmap(Landroid/graphics/Bitmap;)V

    .line 174
    sget-object v8, Landroid/widget/ImageView$ScaleType;->FIT_XY:Landroid/widget/ImageView$ScaleType;

    invoke-virtual {v0, v8}, Landroid/widget/ImageView;->setScaleType(Landroid/widget/ImageView$ScaleType;)V

    .line 175
    invoke-virtual {v0, v12}, Landroid/widget/ImageView;->setAdjustViewBounds(Z)V

    .line 176
    invoke-virtual {v0, v12}, Landroid/widget/ImageView;->setId(I)V

    .line 178
    new-instance v2, Landroid/widget/ImageView;

    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_hContext:Landroid/content/Context;

    invoke-direct {v2, v8}, Landroid/widget/ImageView;-><init>(Landroid/content/Context;)V

    .line 180
    .restart local v2    # "iv_yes":Landroid/widget/ImageView;
    new-instance v8, Ljava/lang/StringBuilder;

    invoke-static {v4}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v9

    invoke-direct {v8, v9}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v9, "/base/movie/skip_btn_yes@2x.png"

    invoke-virtual {v8, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v8

    invoke-virtual {v8}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v8

    invoke-static {v8}, Landroid/graphics/BitmapFactory;->decodeFile(Ljava/lang/String;)Landroid/graphics/Bitmap;

    move-result-object v8

    invoke-virtual {v2, v8}, Landroid/widget/ImageView;->setImageBitmap(Landroid/graphics/Bitmap;)V

    .line 181
    sget-object v8, Landroid/widget/ImageView$ScaleType;->FIT_XY:Landroid/widget/ImageView$ScaleType;

    invoke-virtual {v2, v8}, Landroid/widget/ImageView;->setScaleType(Landroid/widget/ImageView$ScaleType;)V

    .line 182
    invoke-virtual {v2, v12}, Landroid/widget/ImageView;->setAdjustViewBounds(Z)V

    .line 183
    const/4 v8, 0x2

    invoke-virtual {v2, v8}, Landroid/widget/ImageView;->setId(I)V

    .line 184
    new-instance v8, Lcom/yox_project/silver_arrow/MoviePlayer$1;

    invoke-direct {v8}, Lcom/yox_project/silver_arrow/MoviePlayer$1;-><init>()V

    invoke-virtual {v2, v8}, Landroid/widget/ImageView;->setOnTouchListener(Landroid/view/View$OnTouchListener;)V

    .line 193
    new-instance v1, Landroid/widget/ImageView;

    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_hContext:Landroid/content/Context;

    invoke-direct {v1, v8}, Landroid/widget/ImageView;-><init>(Landroid/content/Context;)V

    .line 195
    .restart local v1    # "iv_no":Landroid/widget/ImageView;
    new-instance v8, Ljava/lang/StringBuilder;

    invoke-static {v4}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v9

    invoke-direct {v8, v9}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const-string v9, "/base/movie/skip_btn_no@2x.png"

    invoke-virtual {v8, v9}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v8

    invoke-virtual {v8}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v8

    invoke-static {v8}, Landroid/graphics/BitmapFactory;->decodeFile(Ljava/lang/String;)Landroid/graphics/Bitmap;

    move-result-object v8

    invoke-virtual {v1, v8}, Landroid/widget/ImageView;->setImageBitmap(Landroid/graphics/Bitmap;)V

    .line 196
    sget-object v8, Landroid/widget/ImageView$ScaleType;->FIT_XY:Landroid/widget/ImageView$ScaleType;

    invoke-virtual {v1, v8}, Landroid/widget/ImageView;->setScaleType(Landroid/widget/ImageView$ScaleType;)V

    .line 197
    invoke-virtual {v1, v12}, Landroid/widget/ImageView;->setAdjustViewBounds(Z)V

    .line 198
    const/4 v8, 0x3

    invoke-virtual {v1, v8}, Landroid/widget/ImageView;->setId(I)V

    .line 199
    new-instance v8, Lcom/yox_project/silver_arrow/MoviePlayer$2;

    invoke-direct {v8}, Lcom/yox_project/silver_arrow/MoviePlayer$2;-><init>()V

    invoke-virtual {v1, v8}, Landroid/widget/ImageView;->setOnTouchListener(Landroid/view/View$OnTouchListener;)V

    .line 209
    new-instance v3, Landroid/widget/RelativeLayout;

    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_hContext:Landroid/content/Context;

    invoke-direct {v3, v8}, Landroid/widget/RelativeLayout;-><init>(Landroid/content/Context;)V

    .line 210
    .restart local v3    # "lyt_main":Landroid/widget/RelativeLayout;
    new-instance v8, Landroid/widget/RelativeLayout$LayoutParams;

    invoke-direct {v8, v11, v11}, Landroid/widget/RelativeLayout$LayoutParams;-><init>(II)V

    invoke-virtual {v3, v8}, Landroid/widget/RelativeLayout;->setLayoutParams(Landroid/view/ViewGroup$LayoutParams;)V

    .line 212
    new-instance v7, Landroid/widget/RelativeLayout$LayoutParams;

    invoke-direct {v7, v11, v11}, Landroid/widget/RelativeLayout$LayoutParams;-><init>(II)V

    .line 213
    .restart local v7    # "skip_msg":Landroid/widget/RelativeLayout$LayoutParams;
    invoke-virtual {v7, v14}, Landroid/widget/RelativeLayout$LayoutParams;->addRule(I)V

    .line 214
    const/16 v8, 0x9

    invoke-virtual {v7, v8}, Landroid/widget/RelativeLayout$LayoutParams;->addRule(I)V

    .line 215
    const/16 v8, 0x10

    invoke-virtual {v7, v8, v13, v10, v10}, Landroid/widget/RelativeLayout$LayoutParams;->setMargins(IIII)V

    .line 216
    invoke-virtual {v3, v0, v7}, Landroid/widget/RelativeLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 218
    new-instance v6, Landroid/widget/RelativeLayout$LayoutParams;

    invoke-direct {v6, v11, v11}, Landroid/widget/RelativeLayout$LayoutParams;-><init>(II)V

    .line 219
    .restart local v6    # "skip_btn_yes":Landroid/widget/RelativeLayout$LayoutParams;
    invoke-virtual {v6, v14}, Landroid/widget/RelativeLayout$LayoutParams;->addRule(I)V

    .line 220
    const/16 v8, 0xb

    invoke-virtual {v6, v8}, Landroid/widget/RelativeLayout$LayoutParams;->addRule(I)V

    .line 221
    const/16 v8, 0x10

    invoke-virtual {v6, v10, v13, v8, v10}, Landroid/widget/RelativeLayout$LayoutParams;->setMargins(IIII)V

    .line 222
    invoke-virtual {v3, v2, v6}, Landroid/widget/RelativeLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 224
    new-instance v5, Landroid/widget/RelativeLayout$LayoutParams;

    invoke-direct {v5, v11, v11}, Landroid/widget/RelativeLayout$LayoutParams;-><init>(II)V

    .line 225
    .restart local v5    # "skip_btn_no":Landroid/widget/RelativeLayout$LayoutParams;
    invoke-virtual {v5, v14}, Landroid/widget/RelativeLayout$LayoutParams;->addRule(I)V

    .line 226
    const/4 v8, 0x2

    invoke-virtual {v5, v10, v8}, Landroid/widget/RelativeLayout$LayoutParams;->addRule(II)V

    .line 227
    const/16 v8, 0x30

    invoke-virtual {v5, v10, v13, v8, v10}, Landroid/widget/RelativeLayout$LayoutParams;->setMargins(IIII)V

    .line 228
    invoke-virtual {v3, v1, v5}, Landroid/widget/RelativeLayout;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V

    .line 231
    new-instance v8, Landroid/app/Dialog;

    sget-object v9, Lcom/yox_project/silver_arrow/MoviePlayer;->m_hContext:Landroid/content/Context;

    invoke-direct {v8, v9}, Landroid/app/Dialog;-><init>(Landroid/content/Context;)V

    sput-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    .line 232
    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v8}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v8

    invoke-virtual {v8, v12}, Landroid/view/Window;->requestFeature(I)Z

    .line 233
    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v8, v3}, Landroid/app/Dialog;->setContentView(Landroid/view/View;)V

    .line 234
    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v8}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v8

    const/4 v9, -0x1

    invoke-virtual {v8, v9, v11}, Landroid/view/Window;->setLayout(II)V

    .line 235
    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v8}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v8

    invoke-virtual {v8}, Landroid/view/Window;->getAttributes()Landroid/view/WindowManager$LayoutParams;

    move-result-object v8

    const/16 v9, 0x50

    iput v9, v8, Landroid/view/WindowManager$LayoutParams;->gravity:I

    .line 236
    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v8}, Landroid/app/Dialog;->getWindow()Landroid/view/Window;

    move-result-object v8

    new-instance v9, Landroid/graphics/drawable/ColorDrawable;

    invoke-direct {v9, v10}, Landroid/graphics/drawable/ColorDrawable;-><init>(I)V

    invoke-virtual {v8, v9}, Landroid/view/Window;->setBackgroundDrawable(Landroid/graphics/drawable/Drawable;)V

    .line 237
    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v8, v10}, Landroid/app/Dialog;->setCanceledOnTouchOutside(Z)V

    .line 239
    sget-object v8, Lcom/yox_project/silver_arrow/MoviePlayer;->m_dialog:Landroid/app/Dialog;

    invoke-virtual {v8}, Landroid/app/Dialog;->show()V

    goto/16 :goto_0

    .line 167
    .end local v0    # "iv":Landroid/widget/ImageView;
    .end local v1    # "iv_no":Landroid/widget/ImageView;
    .end local v2    # "iv_yes":Landroid/widget/ImageView;
    .end local v3    # "lyt_main":Landroid/widget/RelativeLayout;
    .end local v5    # "skip_btn_no":Landroid/widget/RelativeLayout$LayoutParams;
    .end local v6    # "skip_btn_yes":Landroid/widget/RelativeLayout$LayoutParams;
    .end local v7    # "skip_msg":Landroid/widget/RelativeLayout$LayoutParams;
    :cond_1
    invoke-static {}, Lcom/yox_project/silver_arrow/StorageUtil;->GetExt1Path()Ljava/lang/String;

    move-result-object v4

    goto/16 :goto_1
.end method

.method public static ResetSkipResult()V
    .locals 1

    .prologue
    .line 275
    const/4 v0, 0x0

    sput v0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_iSkipResult:I

    .line 276
    return-void
.end method

.method public static SetPlaying(I)V
    .locals 0
    .param p0, "isPlaying"    # I

    .prologue
    .line 142
    sput p0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isPlaying:I

    .line 143
    return-void
.end method

.method public static SetRequest(I)V
    .locals 0
    .param p0, "isRequest"    # I

    .prologue
    .line 120
    sput p0, Lcom/yox_project/silver_arrow/MoviePlayer;->m_isRequest:I

    .line 121
    return-void
.end method


# virtual methods
.method public onTouch(Landroid/view/View;Landroid/view/MotionEvent;)Z
    .locals 1
    .param p1, "v"    # Landroid/view/View;
    .param p2, "event"    # Landroid/view/MotionEvent;

    .prologue
    .line 283
    const/4 v0, 0x0

    return v0
.end method
