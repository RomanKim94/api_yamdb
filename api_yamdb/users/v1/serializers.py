from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.constants import USERNAME_VALIDATION_ERROR
from users.models import User


def validate_username(username):
    if username == settings.INVALID_USERNAME:
        ValidationError(USERNAME_VALIDATION_ERROR.format(
            invalid_username=settings.INVALID_USERNAME,
        ))
    User.username_validator(username)
    return username


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения Пользователей и действий на ними."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)

    def validate(self, attrs):
        validate_username(attrs.get('username'))
        return super().validate(attrs)


class ProfileSerializer(UserSerializer):
    """Сериалайзер для отображения и изменения Профиля пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserSignupSerializer(serializers.Serializer):
    """Сериалайзер для регистрации Пользователя."""

    username = serializers.CharField(
        validators=(User.username_validator,),
        max_length=settings.MAX_USERNAME_LENGTH,
    )
    email = serializers.EmailField()

    def validate(self, attrs):
        validate_username(attrs.get('username'))
        return super().validate(attrs)

    def create(self, validated_data):
        """
        Создаёт или обновляет пользователя с переданным `username` и `email`.
        """
        user, _ = User.objects.update_or_create(
            username=validated_data['username'],
            email=validated_data['email'],
            defaults=validated_data,
        )
        return user


class UsernameConfirmationCodeSerializer(serializers.Serializer):
    """Сериалайзер для валидации данных для получении токена."""

    username = serializers.CharField(
        validators=(User.username_validator,),
        max_length=settings.MAX_USERNAME_LENGTH,
    )
    confirmation_code = serializers.CharField(
        validators=(validators.RegexValidator(
            regex=settings.CONFIRMATION_CODE_REGEX,
            message=(
                'Некорректный код подтверждения.'
                'Значение кода длинной 10 символов'
                'состоит из прописных латинских символов и десятичных цифр.'
            )
        ),)
    )
