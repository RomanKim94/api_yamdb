from django.conf import settings
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api import constants as api_const
from reviews import constants as reviews_const, models
from reviews.validators import validate_invalid_username, UsernameValidator


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = models.Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = models.Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (чтение)."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=None)

    class Meta:
        model = models.Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')
        read_only_fields = fields


class TitleWrightSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (запись)."""

    category = SlugRelatedField(
        slug_field='slug',
        queryset=models.Category.objects.all())
    genre = SlugRelatedField(
        slug_field='slug', many=True, allow_null=False, allow_empty=False,
        queryset=models.Genre.objects.all())

    class Meta:
        model = models.Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')

    def to_representation(self, instance):
        """Данные сериализуются через TitleReadSerializer."""
        return TitleReadSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )
    score = serializers.IntegerField(
        min_value=reviews_const.MIN_SCORE_VALUE,
        max_value=reviews_const.MAX_SCORE_VALUE,
    )

    class Meta:
        model = models.Review
        fields = ('id', 'author', 'text', 'score', 'pub_date',)
        read_only_fields = ('pub_date',)

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST' and models.Review.objects.filter(
            title_id=self.context['view'].kwargs['title_id'],
            author=request.user,
        ).exists():
            raise serializers.ValidationError(api_const.DOUBLE_REVIEW_ERROR)
        return super().validate(attrs)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения Пользователей и действий на ними."""

    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)


class ProfileSerializer(UserSerializer):
    """Сериалайзер для отображения и изменения Профиля пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=(UsernameValidator(), validate_invalid_username),
        max_length=reviews_const.USERNAME_LENGTH,
        required=True,
    )


class UserSignupSerializer(UsernameSerializer):
    """Сериалайзер для валидации данных при регистрации Пользователя."""

    email = serializers.EmailField(
        max_length=reviews_const.EMAIL_LENGTH,
        required=True,
    )


class UsernameConfirmationCodeSerializer(UsernameSerializer):
    """Сериалайзер для валидации данных для получении токена."""

    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        required=True,
    )
