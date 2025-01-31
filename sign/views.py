import random

from django.contrib.auth import authenticate, login
from django.shortcuts import render

from board.models import OneTimeCode


# Create your views here.

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user - authenticate(request, usename=username, password=password)

    if user is not None:
        OneTimeCode.objacts.create(code=random.choice('abcde'))
        #send code to mail
        #redirect
    else:
        #return invalid login


def login_whith_code_view(request):
    username = request.POST['username']
    code = request.POST['code']
    if OneTimeCode.objacts.filter( code=code, user__username=username).exists():
        login(request, user)
    else:
        #error
