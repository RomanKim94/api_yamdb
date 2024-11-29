from rest_framework import serializers

from core import validators
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения Пользователей и действий на ними."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)


class ProfileSerializer(UserSerializer):
    """Сериалайзер для отображения и изменения Профиля пользователя."""
    role = serializers.CharField(read_only=True)


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации Пользователя."""
    class Meta:
        model = User
        fields = ('username', 'email',)


class UsernameConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=(User.username_validator,),
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        validators=(validators.ConfirmationCodeValidator,)
    )
