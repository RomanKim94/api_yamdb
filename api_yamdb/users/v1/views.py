from django.conf import settings
import random
from rest_framework import (
    filters,
    generics,
    permissions,
    status,
    views,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import permissions as api_permissions
from core import utils
from users import models
from users.v1 import serializers


class UserModelViewSet(viewsets.ModelViewSet):
    """Представление для API Пользователей.

    API доступно только администратору.
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (api_permissions.AdminsPermissions,)
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(methods=('get', 'patch',),
            detail=False,
            url_name='profile',
            url_path='me',
            permission_classes=(permissions.IsAuthenticated,))
    def profile(self, request, *args, **kwargs):
        """API Профиля пользователя.

        API доступно только для авторизованного пользователя.
        """
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)

        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        if self.action == self.profile.__name__:
            return self.request.user

        return super(UserModelViewSet, self).get_object()

    def get_serializer_class(self):
        if self.action == self.profile.__name__:
            return serializers.ProfileSerializer

        return super(UserModelViewSet, self).get_serializer_class()


class TokenApiView(views.APIView):
    """Представление для генерации токена аунтентификации.

    Доступно для не авторизованного пользователя.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.UsernameConfirmationCodeSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = generics.get_object_or_404(
            models.User, username=request.data.get('username')
        )

        if user.confirmation_code != request.data.get('confirmation_code'):
            raise ValidationError(f'Некорректный код подтверждения. '
                                  f'Укажите код переданный на электронную '
                                  f'почту {user.email} при регистрации, '
                                  f'либо сгенерируйте новый путём повторной '
                                  f'отправки запроса на регистрацию.')

        return Response(
            {'token': str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_200_OK,
        )


class SignUpApiView(views.APIView):
    """Представление для самостоятельной регистрации.

    Создает нового пользователя, с дальнейшей отправкой на указанный email
    кода подтверждения. При повторном запросе происходит обновление
    кода подтверждения с повторной отправкой на email.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        user = models.User.objects.filter(username=username,
                                          email=email).first()
        serializer = serializers.UserSignupSerializer(data=request.data)

        if user:
            serializer.instance = user

        serializer.is_valid(raise_exception=True)
        user = serializer.save(
            confirmation_code=''.join(random.choices(
                settings.CONFIRMATION_CODE_SYMBOLS,
                k=settings.CONFIRMATION_CODE_LENGTH,
            ))
        )
        utils.send_confirmation_email(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
