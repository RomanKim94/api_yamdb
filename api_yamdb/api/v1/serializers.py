from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from core.constants import DOUBLE_REVIEW_ERROR, SCORE_VALIDATION_ERROR


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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    genre = SlugRelatedField(
        slug_field='slug', many=True,
        queryset=Genre.objects.all())
    rating = serializers.IntegerField(read_only=True, default=None)

    def to_representation(self, instance):
        """Настройка показа категорий и жанров в формате: имя, слаг."""
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(
            instance.category).data
        representation['genre'] = GenreSerializer(
            instance.genre, many=True).data
        return representation

    def validate_year(self, year):
        """Валидация поля года издания произведения."""
        if year > timezone.now().year:
            raise serializers.ValidationError(
                'Год произведения не может быть больше текущего')
        return year

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')


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
            author_id=request.user.id,
        ).exists():
            raise ValidationError(DOUBLE_REVIEW_ERROR)
        return super().validate(attrs)

    def validate_score(self, score):
        '''Валидация поля score на соответствие диапазону от 1 до 10.'''
        if 1 > score or score > 10:
            raise ValidationError(
                {'score': SCORE_VALIDATION_ERROR.format(score=score)}
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
