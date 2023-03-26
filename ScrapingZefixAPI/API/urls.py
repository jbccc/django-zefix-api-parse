from django.conf.urls import url
from django.http.response import JsonResponse
from django.urls import path
from API.views import (
    HelloView, 
    lforms,
    cantons
)
urlpatterns = [

    url('legalForm/', lforms, name="legal_forms_list"),
    url('cantons/', cantons, name='cantons_list'),
    path('hello/', HelloView.as_view(), name='hello'),
    # path('user/file', user_words.as_view(), name='word file'),    
]