from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from reviews.constants import (
    DOUBLE_REVIEW_ERROR, SCORE_VALIDATION_ERROR,
    MIN_SCORE_VALUE, MAX_SCORE_VALUE,
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (чтение)."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=None)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')


class TitleWrightSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (запись)."""

    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    genre = SlugRelatedField(
        slug_field='slug', many=True, allow_null=False, allow_empty=False,
        queryset=Genre.objects.all())
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')

    def to_representation(self, instance):
        """Настройка показа категорий и жанров в формате: имя, слаг."""
        return TitleReadSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date',)
        read_only_fields = ('pub_date',)

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST' and Review.objects.filter(
            title_id=self.context['view'].kwargs['title_id'],
            author=request.user,
        ).exists():
            raise ValidationError(DOUBLE_REVIEW_ERROR)
        return super().validate(attrs)

    def validate_score(self, score):
        '''Валидация поля score на соответствие диапазону от 1 до 10.'''
        if MIN_SCORE_VALUE > score or score > MAX_SCORE_VALUE:
            raise ValidationError(
                {
                    'score': SCORE_VALIDATION_ERROR.format(
                        score=score,
                        minimum=MIN_SCORE_VALUE,
                        maximum=MAX_SCORE_VALUE,
                    )
                }
            )
        return score


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('pub_date',)
