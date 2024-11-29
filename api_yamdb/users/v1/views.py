from rest_framework import (
    mixins,
    pagination,
    generics,
    viewsets,
    views,
    status,
)
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core import permissions as api_permissions, utils
from . import serializers
from ..models import User


class UserModelViewSet(viewsets.ModelViewSet):
    """Представление для API Пользователей.

    API доступно только администратору.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (api_permissions.IsAdmin,)
    lookup_url_kwarg = 'username'


class ProfileModelViewSet(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    """Представление для API Профиля пользователя.

    API доступно только для авторизованного пользователя.
    """
    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return self.request.user


class TokenApiView(views.APIView):
    """Представление для генерации токена аунтентификации.

    Доступно для авторизованного пользователя.
    """

    def post(self, request, *args, **kwargs):
        serializer = serializers.UsernameConfirmationCodeSerializer(
            request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = generics.get_object_or_404(User, username=data.get('username'))

        if user.confirmation_code != data.get('confirmation_code'):
            raise ValidationError(f'Некорректный код подтверждения.'
                                  f'Укажите код переданный на электронную '
                                  f'почту {user.email} при регистрации,'
                                  f'либо сгенерируйте новый путём повторной '
                                  f'отправки запроса на регистрацию.')

        return Response(
            {'token': utils.get_token_for_user(user)},
            status=status.HTTP_200_OK,
        )


class SignUpApiView(generics.CreateAPIView):
    """Представление для самостоятельной регистрации.

    Создает нового пользователя, с дальнейшей отправкой на указанный email
    кода подтверждения. При повторном запросе происходит обновление
    кода подтверждения с повторной отправкой на email.
    """
    serializer_class = serializers.UserSignupSerializer

    def perform_create(self, serializer):
        confirmation_code = utils.generate_confirmation_code()
        user = serializer.save(confirmation_code=confirmation_code)
        utils.send_confirmation_email(user)
