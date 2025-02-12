from allauth.account.forms import SignupForm
from django.core.mail import send_mail
from board.models import OneTimeCode
import random
from string import hexdigits

from gameforum import settings


class MyCustomSignupForm(SignupForm):

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.is_active = False
        user.save()
        code = ''.join(random.sample(hexdigits, 4))
        OneTimeCode.objects.create(user=user, code=code)

        send_mail(
            subject='код активации',
            message=f'Активируйте аккаунт по коду{code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user
