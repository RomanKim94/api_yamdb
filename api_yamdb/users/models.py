from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    email = models.EmailField('Email', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', choices=ROLES_CHOICES, default=USER, max_length=9,
    )
