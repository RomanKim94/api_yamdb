from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()

CONFIRMATION_EMAIL_BODY = 'confirmation_code_email_body.txt'
CONFIRMATION_EMAIL_SUBJECT = 'confirmation_code_email_subject.txt'


def send_confirmation_email(user: User, confirmation_code: str) -> bool:
    """Отправляет письмо подтверждения на электронную почту пользователя."""
    return bool(send_mail(
        CONFIRMATION_EMAIL_SUBJECT,
        render_to_string(CONFIRMATION_EMAIL_BODY, {
            'user': user,
            'confirmation_code': confirmation_code,
        }),
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    ))
