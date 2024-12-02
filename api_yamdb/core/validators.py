from django.core import validators
from django.utils.deconstruct import deconstructible

from reviews.constants import CONFIRMATION_CODE_REGEX


@deconstructible
class ConfirmationCodeValidator(validators.RegexValidator):
    regex = CONFIRMATION_CODE_REGEX
    message = (
        'Некорректный код подтверждения. Значение кода длинной 10 символов '
        'состоит из прописных латинских символов и десятичных цифр.'
    )
