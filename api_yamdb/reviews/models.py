from django.contrib.auth import get_user_model
from django.db import models

from constants import STRING_SHOW, NAME_STRING_LENGTH, SLUG_LENGTH

User = get_user_model()


class PubDate(models.Model):
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True


class Genre(models.Model):
    name = models.CharField(max_length=NAME_STRING_LENGTH,
                            unique=True,
                            verbose_name='Название жанра')
    slug = models.SlugField(max_length=SLUG_LENGTH,
                            unique=True,
                            verbose_name='Slug')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name', )

    def __str__(self):
        return f'name: {self.name[:STRING_SHOW]} slug: {self.slug}'


class Category(models.Model):
    name = models.CharField(max_length=NAME_STRING_LENGTH,
                            unique=True,
                            verbose_name='Название категории')
    slug = models.SlugField(max_length=SLUG_LENGTH,
                            unique=True,
                            verbose_name='Slug')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name', )

    def __str__(self):
        return f'name: {self.name[:STRING_SHOW]} slug: {self.slug}'


class Review(PubDate):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'

    def __str__(self):
        return f'text: {self.text[:STRING_SHOW]} author: {self.author}'


class Comment(PubDate):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return f'text: {self.text[:STRING_SHOW]} author: {self.author}'


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(verbose_name='Год производства')
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name', '-year']

    def __str__(self):
        return f'name: {self.name[:STRING_SHOW]} category: {self.category}'
