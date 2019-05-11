'''
Created on 2019. 4. 28.

@author: 평일오후
'''
from customlogin.views import *
from django.urls import path
app_name='cl'
#도메인 주소 : 127.0.0.1:8000/login/
urlpatterns=[
    #127.0.0.1:8000/login/signup/
    path('signup/', signup, name='signup'),
    #127.0.0.1:8000/login/signin/
    path('signin/', signin, name='signin'),
    #127.0.0.1:8000/login/signout/
    path('signout/', signout, name='signout'),
    ]