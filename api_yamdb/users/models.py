from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from core import (
    constants as const,
    validators,
)


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    password = models.CharField('Пароль', blank=True, max_length=128)
    email = models.EmailField('Email', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', choices=ROLES_CHOICES, default=USER, max_length=9
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True,
        max_length=const.CONFIRMATION_CODE_LENGTH,
        validators=(validators.ConfirmationCodeValidator,)
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.username.lower() == const.INVALID_USERNAME:
            raise ValidationError({
                'username': f'Недопустимое имя пользователя "{self.username}"',
            })
