from django.shortcuts import render, resolve_url
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, EmailMessage
from .scrap import scrapZefix
from .models import TestDb



def file(req):
    response = HttpResponse(open('API/doct.docx', 'rb').read(), content_type="application/vnd.ms-word")
    response['Content-Disposition'] = 'filename = test.docx'
    return response

def test(req):
    a = scrapZefix()
    
    list = a.get_firms_of_the_day()
    return HttpResponse('caca')