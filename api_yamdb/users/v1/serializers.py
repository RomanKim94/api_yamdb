from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews import constants
from core import validators
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения Пользователей и действий на ними."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email',),
            ),
        )


class ProfileSerializer(UserSerializer):
    """Сериалайзер для отображения и изменения Профиля пользователя."""

    class Meta(UserSerializer.Meta):
        extra_kwargs = {
            'role': {'read_only': True},
        }


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации Пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value.lower() == constants.INVALID_USERNAME:
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя \'{value}\''
            )
        return value


class UsernameConfirmationCodeSerializer(serializers.Serializer):
    """Сериалайзер для валидации данных для получении токена."""

    username = serializers.CharField(
        validators=(User.username_validator,),
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        validators=(validators.ConfirmationCodeValidator,)
    )
