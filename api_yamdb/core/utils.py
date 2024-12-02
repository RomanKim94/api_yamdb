import random
import string

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from reviews import constants as const

User = get_user_model()


def generate_confirmation_code() -> str:
    """Формирует код подтверждения регистрации."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits,
                                  k=const.CONFIRMATION_CODE_LENGTH))


def send_confirmation_email(user: User) -> bool:
    """Отправляет письмо подтверждения на электронную почту пользователя."""
    subject_temp = render_to_string(const.CONFIRMATION_EMAIL_SUBJECT)
    body_temp = render_to_string(const.CONFIRMATION_EMAIL_BODY, {'user': user})
    return bool(send_mail(subject_temp, body_temp, None, [user.email]))


def get_token_for_user(user: User) -> str:
    """Формирует актуальный токен аутентификации пользователя."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
