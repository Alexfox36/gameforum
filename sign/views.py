import random

import form
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from board.models import OneTimeCode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage

from gameforum.sign.forms import SignupForm


# Create your views here.

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, usename=username, password=password)

    if user is not None:
        otcode=OneTimeCode.objects.create(code=random.choice('abcde'),user=user)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Код подтверждения отправлена на вашу почту'
        message = render_to_string('activate_code_email.html', {
                         'user': user,
                         'domain': current_site.domain,
                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                         'token': otcode,
                     })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                         mail_subject, message, to=[to_email]
                     )
        email.send()


        return HttpResponse('Введите код подтверждения')

    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})





def login_whith_code_view(request):
    username = request.POST['username']
    code = request.POST['code']
    if OneTimeCode.objects.filter( code=code, user__username=username).exists():
        login(request, user)
    else:
        return HttpResponse('Не верный код подтверждения')
