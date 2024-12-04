from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api import constants as const
from reviews import models


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


class TitleWrightSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (запись)."""

    category = SlugRelatedField(
        slug_field='slug',
        queryset=models.Category.objects.all())
    genre = SlugRelatedField(
        slug_field='slug', many=True, allow_null=False, allow_empty=False,
        queryset=models.Genre.objects.all())
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = models.Title
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
        model = models.Review
        fields = ('id', 'author', 'text', 'score', 'pub_date',)
        read_only_fields = ('pub_date',)

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST' and models.Review.objects.filter(
            title_id=self.context['view'].kwargs['title_id'],
            author=request.user,
        ).exists():
            raise serializers.ValidationError(const.DOUBLE_REVIEW_ERROR)
        return super().validate(attrs)

    def validate_score(self, score):
        """Валидация поля score на соответствие диапазону от 1 до 10."""

        if const.MIN_SCORE_VALUE > score or score > const.MAX_SCORE_VALUE:
            raise serializers.ValidationError(
                {
                    'score': const.SCORE_VALIDATION_ERROR.format(
                        score=score,
                        minimum=const.MIN_SCORE_VALUE,
                        maximum=const.MAX_SCORE_VALUE,
                    )
                }
            )
        return score


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('pub_date',)


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения Пользователей и действий на ними."""

    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)


class ProfileSerializer(UserSerializer):
    """Сериалайзер для отображения и изменения Профиля пользователя."""

    class Meta(UserSerializer.Meta):
        extra_kwargs = {
            'role': {'read_only': True},
        }


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации Пользователя."""

    class Meta:
        model = models.User
        fields = ('username', 'email',)


class UsernameConfirmationCodeSerializer(serializers.Serializer):
    """Сериалайзер для валидации данных для получении токена."""

    username = serializers.CharField(
        validators=(models.User.username_validator,),
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        validators=()
    )
