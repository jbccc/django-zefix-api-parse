import re
from django.shortcuts import render, resolve_url
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf.urls import url
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import get_user_model
from requests.api import request

from rest_framework.views import APIView, exception_handler
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import APIException

from API.scrap.scrap import scrapZefix
from API.genderParse import create_gender_db
from API.models import firms, words
from API.cron import daily_mail
from API.word import fileManager

import os



def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
   


class UserFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = words
        fields = ('name','user','file')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id','username')

class UnsupportedMediaType(APIException):
    status_code = 415
    default_detail = 'Unsupported Media Type.'
    default_code = 'service_unavailable'



class user_words(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get_object(self): 
        return self.request.user
    def post_object(self):
        try:
            words(
                name=self.request.content_params['name'],
                file=self.request.content_params['FILES'][0],
                user=self.request.user,
            ).save()
            return self.get_object()
        except:
            return 


class HelloView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get_object(self): 
        return self.request.user



def lforms(req):
    return JsonResponse(["SARL","SA","EI"], safe=False)

def cantons(req):
    return JsonResponse(["GE","VD",], safe=False)

