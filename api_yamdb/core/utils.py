import random
import string

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template import Context, Engine

from core import constants as const

User = get_user_model()


def generate_confirmation_code() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits,
                                  k=const.CONFIRMATION_CODE_LENGTH))


def send_confirmation_email(user: User) -> bool:
    engine = Engine()
    body_temp = engine.get_template(const.CONFIRMATION_CODE_EMAIL_BODY)
    subject_temp = engine.get_template(const.CONFIRMATION_CODE_EMAIL_SUBJECT)
    email = EmailMessage(
        subject_temp,
        body_temp.render(Context({'user': user})),
        [user.email],
    )
    return bool(email.send())


def get_token_for_user(user: User) -> str:
    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)
