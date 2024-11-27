from django.contrib.auth import get_user_model
from django.db import models

import constants as const

User = get_user_model()


class PubDate(models.Model):
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


class Genre(NameSlug):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return f'name: {self.name[:const.STRING_SHOW]} slug: {self.slug}'


class Category(NameSlug):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return f'name: {self.name[:const.STRING_SHOW]} slug: {self.slug}'


class Review(PubDate):
    title = models.ForeignKey(
        'Title',
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        default_related_name = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review',
            ),
        )

    def __str__(self):
        return f'text: {self.text[:const.STRING_SHOW]} author: {self.author}'


class Comment(PubDate):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
        default_related_name = 'comments'

    def __str__(self):
        return f'text: {self.text[:const.STRING_SHOW]} author: {self.author}'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=const.NAME_TITLE_LENGTH,
    )
    year = models.PositiveSmallIntegerField(verbose_name='Год производства')
    description = models.TextField(verbose_name="Описание", blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )
    genres = models.ManyToManyField(Genre, verbose_name='Жанр')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name', '-year',)
        default_related_name = 'titles'

    def __str__(self):
        return (f'name: {self.name[:const.STRING_SHOW]} '
                f'category: {self.category}')
