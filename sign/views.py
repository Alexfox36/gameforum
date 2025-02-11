from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from board.models import OneTimeCode
from sign.models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url ='/'


def confirm_signup(request):
    if request.method == "POST":
        code = request.POST.get('code')
        if OneTimeCode.objects.filter(code=code).exists():
            user = OneTimeCode.objects.get(code=code).user
            user.is_active = True
            user.save()
            OneTimeCode.objects.filter(code=code, user=user).delete()
        else:
            return render(request,'invalid_code.html')
    return  redirect('account_login')
