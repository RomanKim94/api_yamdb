from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для Пользователя."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role',)


class ProfileSerializer(UserSerializer):
    """Сериалайзер для Профиля пользователя."""
    role = serializers.CharField(read_only=True)
