from django.contrib.auth.models import AbstractUser
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

    password = models.CharField(
        'Пароль',
        max_length=128,
        blank=True,
        null=True,
    )
    email = models.EmailField('Email', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=ROLES_CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True,
        max_length=const.CONFIRMATION_CODE_LENGTH,
        validators=(validators.ConfirmationCodeValidator,),
    )

    class Meta(AbstractUser.Meta):
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email',),
                name='unique_username_email',
            ),
        )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def save(self, *args, **kwargs):
        if self.username and self.username.lower() == const.INVALID_USERNAME:
            raise ValueError(
                f'Недопустимое имя пользователя \'{self.username}\''
            )

        super(User, self).save(*args, **kwargs)
