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
