import re

from django.core import validators
from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import validate_year
from api import constants as const


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES_CHOICES = {
        ADMIN: 'Администратор',
        MODERATOR: 'Модератор',
        USER: 'Пользователь',
    }
    role_max_length = len(max(ROLES_CHOICES.keys(),
                              key=lambda role: len(role)))

    username = models.CharField(
        'Имя пользователя',
        max_length=const.USERNAME_LENGTH,
        unique=True,
        validators=(
            AbstractUser.username_validator,
            validators.RegexValidator(
                regex=const.USERNAME_REGEX,
                inverse_match=True,
                message='Недопустимое имя пользователя.',
                flags=re.IGNORECASE
            ),
        ),
    )
    password = models.CharField(
        'Пароль',
        max_length=const.PASSWORD_LENGTH,
        blank=True,
        null=True,
    )
    email = models.EmailField('Email', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=role_max_length,
        choices=ROLES_CHOICES.items(),
        default=USER,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True,
        max_length=const.CONFIRMATION_CODE_LENGTH,
        validators=(
            validators.RegexValidator(
                regex=const.CONFIRMATION_CODE_REGEX,
                message='Некорректный код подтверждения.',
            ),
        )
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
        return self.role == self.ADMIN or self.is_staff


class ReviewComment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        default_related_name = '%(class)ss'


class NameSlug(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=const.NAME_STRING_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=const.SLUG_LENGTH,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)
        default_related_name = '%(class)ss'

    def __str__(self):
        return f'name: {self.name[:const.STRING_SHOW]} slug: {self.slug}'


class Genre(NameSlug):

    class Meta(NameSlug.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(NameSlug):

    class Meta(NameSlug.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=const.NAME_TITLE_LENGTH,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год производства',
        validators=(validate_year,))
    description = models.TextField(verbose_name='Описание', blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)
        default_related_name = 'titles'

    def __str__(self):
        return (f'name: {self.name[:const.STRING_SHOW]} '
                f'category: {self.category}')


class Review(ReviewComment):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=(validators.MinValueValidator(const.MIN_SCORE_VALUE),
                    validators.MaxValueValidator(const.MAX_SCORE_VALUE)),
    )

    class Meta(ReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review',
            ),
        )

    def __str__(self):
        return f'text: {self.text[:const.STRING_SHOW]} author: {self.author}'


class Comment(ReviewComment):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )

    class Meta(ReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'text: {self.text[:const.STRING_SHOW]} author: {self.author}'
