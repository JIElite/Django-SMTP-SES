from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.
def send_email(request):
    send_mail(
        'Subject here',
        'lol 政寬 窩 真佩服我自己XDDD 這是用 AWS SES 弄的！.',
        'eli@jielite.tw',
        ['ita3051@gmail.com', 'csiekuan@gmail.com'],
        fail_silently=False,
    )    

    return HttpResponse(status=200) 
