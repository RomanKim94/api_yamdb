from django.contrib.auth import get_user_model
from django.db import models

from constants import constants as const

User = get_user_model()


class PubDate(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        abstract = True


class NameSlug(models.Model):
    name = models.CharField(
        max_length=const.NAME_STRING_LENGTH,
        unique=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=const.SLUG_LENGTH,
        unique=True,
        verbose_name='Slug',
    )

    class Meta:
        abstract = True


class Genre(NameSlug):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name', )

    def __str__(self):
        return f'name: {self.name[:const.STRING_SHOW]} slug: {self.slug}'


class Category(NameSlug):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name', )

    def __str__(self):
        return f'name: {self.name[:const.STRING_SHOW]} slug: {self.slug}'


class Review(PubDate):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        default_related_name = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'auhtor'),
                name='unique_review',
            ),
        )

    def __str__(self):
        return f'text: {self.text[:const.STRING_SHOW]} author: {self.author}'


class Comment(PubDate):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
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
        max_length=const.NAME_TITLE_LENGTH,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год производства',
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name', '-year']
        default_related_name = 'titles'

    def __str__(self):
        return (
            f'name: {self.name[:const.STRING_SHOW]} category: {self.category}')
