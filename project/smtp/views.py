from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.
def send_email(request):
    send_mail(
        'Subject here',
        'Mailing Message',
        'from@domain',
        ['to@mail.com'],
        fail_silently=False,
    )    

    return HttpResponse(status=200) 
