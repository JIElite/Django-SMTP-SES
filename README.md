# Using Django and AWS SES to Send Email

hackmd: https://hackmd.io/s/HJHPwzADx

## Introduction
我們在查詢密碼的時候，通常服務商會寄給我們一封信件，夾帶著更改密碼的連結。
這封信件是怎麼寄出來的呢？通常會需要 SMTP 服務。
在 AWS 上就是 SES。

## Dependency Package
在 Django 要使用 AWS SES 的服務我查到有以下幾種方法
- using [django-ses](https://github.com/django-ses/django-ses)
- using [django-smtp-ssl](https://github.com/bancek/django-smtp-ssl)
在這裡，我是使用後者的方式。雖然前者的 star 數目比較多，但是後者很易用。

```
$ pip install -r requirements
```


## 建置步驟
1. 要能夠發信至少要有一個網域 (Domain)
2. 在 AWS 使用 SES 服務，驗證你的網域
3. 驗證通過之後，可以使用 AWS 的測試功能發送測試信件
4. 串接 Django
5. 將 AWS SES 移出 sandbox mode.


## 購買網域
提供網域的電信商很多，可以自己選擇，因為我之前有在 Godaddy 買過網域，所以就以 Godaddy 作為例子。
![](https://i.imgur.com/I9s54r9.png)

## 開啟 AWS SES 的服務
目前 AWS SES 服務只有三個地區提供：
![](https://i.imgur.com/0fxNofc.png)

首先，我們就先來驗證我們的網域吧！輸入網域之後，勾選 Generate DKIM Settings, DKIM 使用來防止偽造的。詳情可以看這裡：https://support.google.com/a/answer/174124?hl=zh-Hant
![](https://i.imgur.com/3PMmZzt.png)

按下驗證按鈕後，你需要到你的 網域管理商去設定網域的 DNS。在這裏要設定兩個項東西
- 允許利用 aws ses 發送信件服務 (TXT)
- 使用 DKIM 簽證 (CNAME, 要設定三個)


![](https://i.imgur.com/OEiAWAo.png)
設定好之後，就可以來測試信件了！


## 測試寄信
由於預設情況下，AWS SES 會是在 sandbox mode 進行，只能對個人帳號 verified email 發信，如果要能讓它對外發送信件就要 move out sandbox mode.

![](https://i.imgur.com/s9mJG1p.png)

這是收到的狀況:
![](https://i.imgur.com/UXjOd8H.png)

## 串接 Django
ok. 做完基本設定之後，我們就來開始寫 code 吧！

我們先建立一個 django app 叫做 smtp
然後去修改 settings.py 新增下列東西：

```python
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 465
# IAM user settings
# look: https://console.aws.amazon.com/iam/home?#/s=SESHome
EMAIL_HOST_USER = 'iam-user'
EMAIL_HOST_PASSWORD = 'iam-password'
EMAIL_USE_TLS = True
```

- EMAIL_HOST: 因為我們是利用 AWS SES 的服務，所以在這李是要寫 AWS SES 服務的網域，你可以在 AWS SES SMTP Settings 查看
![](https://i.imgur.com/MQIgRL0.png)

- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
這裡則是要利用 同一頁面的 Create My SMTP Credentials 去產生，照著步驟接下去操作，直到拿到 Credentials 檔案在設置即可。
![](https://i.imgur.com/0R3V7D5.png)

```python
/views.py

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.
def send_email(request):
    send_mail(
        'Subject here',
        'Sending Message.',
        'from@yourdomain.com',
        ['to@email.com'],
        fail_silently=False,
    )    

    return HttpResponse(status=200) 
```
在 views.py 利用 django.core.mail 中的 send_mail 就可以寄信囉！

## 將 AWS SES 移出 sandbox mode
AWS 的說明：http://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html

其實上面的文件寫得很清楚，然後到[這裡](https://console.aws.amazon.com/support/home?region=us-east-1#/case/create?issueType=service-limit-increase&limitType=service-code-ses)提出申請，等待審核就好了


