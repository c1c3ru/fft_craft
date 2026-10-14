.class public Lcom/square_enix/FFT_Android/ObbDownloaderService;
.super Lcom/google/android/vending/expansion/downloader/impl/DownloaderService;
.source "ObbDownloaderService.java"


# static fields
.field private static final BASE64_PUBLIC_KEY:Ljava/lang/String; = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx9co1IKNLhuTJ2tgFlZ0q3Y4XGxZWEf7wxgbMU6mF7AhbLUrRUdOMdSsuoZJ0XmLAk9TiRWi1i/LGKfs3wBkT6jC6UMJr4ayD0OV4kCEJQT7Nrstp8sJI+U0+YWSPlnfIbnud8W9zoWWbdbOj3Bywf8K2wKa0vYDt1x86AaZmcdpZNhkgGZMMTusZLtdY8gwE7FDq3mfEq/IAkTv4aRj8Gi1HtIpms6v0S3P7WWq6/rQFOfKFBT40lRb4/i1/VahynooLBPz7h6j8o7Yra9JHNagc23AIcAf1S3JBuJbHsAaj1NfMSB7NU4lm+mtVv3HOVe0bdB8sFAbGD4o5jaQgwIDAQAB"

.field private static final SALT:[B

.field static final TAG:Ljava/lang/String; = "ObbDownloaderService"


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .prologue
    .line 33
    const/16 v0, 0x14

    new-array v0, v0, [B

    fill-array-data v0, :array_0

    sput-object v0, Lcom/square_enix/FFT_Android/ObbDownloaderService;->SALT:[B

    .line 35
    return-void

    .line 33
    :array_0
    .array-data 1
        -0x55t
        0x27t
        -0x5ct
        0x22t
        -0x26t
        -0x62t
        -0x2dt
        -0x4ct
        0x37t
        -0x34t
        -0x6t
        0x4t
        0x16t
        0x5t
        0x10t
        0x21t
        0x43t
        -0x52t
        0x33t
        -0x1ct
    .end array-data
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 25
    invoke-direct {p0}, Lcom/google/android/vending/expansion/downloader/impl/DownloaderService;-><init>()V

    return-void
.end method


# virtual methods
.method public getAlarmReceiverClassName()Ljava/lang/String;
    .locals 2

    .prologue
    .line 70
    const-string v0, "ObbDownloaderService"

    const-string v1, "getAlarmReceiverClassName"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 72
    const-class v0, Lcom/square_enix/FFT_Android/ObbAlarmReceiver;

    invoke-virtual {v0}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public getPublicKey()Ljava/lang/String;
    .locals 2

    .prologue
    .line 44
    const-string v0, "ObbDownloaderService"

    const-string v1, "getPublicKey"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 46
    const-string v0, "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx9co1IKNLhuTJ2tgFlZ0q3Y4XGxZWEf7wxgbMU6mF7AhbLUrRUdOMdSsuoZJ0XmLAk9TiRWi1i/LGKfs3wBkT6jC6UMJr4ayD0OV4kCEJQT7Nrstp8sJI+U0+YWSPlnfIbnud8W9zoWWbdbOj3Bywf8K2wKa0vYDt1x86AaZmcdpZNhkgGZMMTusZLtdY8gwE7FDq3mfEq/IAkTv4aRj8Gi1HtIpms6v0S3P7WWq6/rQFOfKFBT40lRb4/i1/VahynooLBPz7h6j8o7Yra9JHNagc23AIcAf1S3JBuJbHsAaj1NfMSB7NU4lm+mtVv3HOVe0bdB8sFAbGD4o5jaQgwIDAQAB"

    return-object v0
.end method

.method public getSALT()[B
    .locals 2

    .prologue
    .line 57
    const-string v0, "ObbDownloaderService"

    const-string v1, "getSALT"

    invoke-static {v0, v1}, Lcom/yox_project/silver_arrow/LOG;->i(Ljava/lang/String;Ljava/lang/String;)V

    .line 59
    sget-object v0, Lcom/square_enix/FFT_Android/ObbDownloaderService;->SALT:[B

    return-object v0
.end method
