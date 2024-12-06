from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    """Валидация года издания произведения."""
    if year > timezone.now().year:
        raise ValidationError(
            f'Год произведения {year} не может быть больше текущего года:'
            f'{timezone.now().year}.'
        )
    return year


def validate_invalid_username(username):
    """Проверка логина на соответствие с запрещенным."""
    if username == settings.USERNAME_INVALID:
        raise ValidationError(f'Недопустимый логин {username}')

    return username
