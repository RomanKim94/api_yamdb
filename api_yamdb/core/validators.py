from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class ConfirmationCodeValidator(validators.RegexValidator):
    regex = r'^[A-Z\d]{10}$'
    message = (
        'Некорректный код подтверждения. Значение кода длинной 10 символов '
        'состоит из прописных латинских символов и десятичных цифр.'
    )