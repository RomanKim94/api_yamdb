import random

from django.conf import settings
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    generics,
    mixins,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api import (
    constants as const,
    serializers as api_serializers,
    permissions as api_permissions,
    utils,
)
from api.filters import TitleFilter
from reviews import models


class CategoryGenreViewset(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """Базовый вьюсет для категорий и жанров."""

    permission_classes = (api_permissions.IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewset):
    """Представление для категорий."""

    queryset = models.Category.objects.all()
    serializer_class = api_serializers.CategorySerializer


class GenreViewSet(CategoryGenreViewset):
    """Представление для жанров."""

    queryset = models.Genre.objects.all()
    serializer_class = api_serializers.GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для произведений."""

    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')
    queryset = models.Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (api_permissions.IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return api_serializers.TitleReadSerializer
        return api_serializers.TitleWrightSerializer


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        api_permissions.IsAdminOrModeratorOrAuthor,
    )
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_title(self):
        """Метод возвращает объект произведения по id полученного из url."""
        return get_object_or_404(models.Title, pk=self.kwargs['title_id'])


class ReviewViewSet(BaseViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = api_serializers.ReviewSerializer

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(BaseViewSet):
    """Представление для комментариев."""

    serializer_class = api_serializers.CommentSerializer

    def get_review(self):
        '''
        Метод возвращает объект отзыва к произведению по id полученного из url.
        '''
        return get_object_or_404(
            models.Review,
            title=super().get_title(),
            pk=self.kwargs['review_id'],
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()


class UserModelViewSet(viewsets.ModelViewSet):
    """Представление для API Пользователей.

    API доступно только администратору.
    """

    queryset = models.User.objects.all()
    serializer_class = api_serializers.UserSerializer
    permission_classes = (api_permissions.AdminsPermissions,)
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(methods=('get', 'patch',),
            detail=False,
            url_name='profile',
            url_path=settings.PROFILE_URL_PATH,
            permission_classes=(permissions.IsAuthenticated,))
    def profile(self, request, *args, **kwargs):
        """API Профиля пользователя.

        API доступно только для авторизованного пользователя.
        """
        serializer = api_serializers.ProfileSerializer

        if request.method == const.HTTPMethod.PATCH:
            serializer = serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = serializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token_api_view(request):
    """Представление для получения токена аунтентификации."""

    serializer = api_serializers.UsernameConfirmationCodeSerializer(
        data=request.data
    )
    serializer.is_valid(raise_exception=True)
    user = generics.get_object_or_404(
        models.User, username=request.data.get('username')
    )

    if user.confirmation_code != request.data.get('confirmation_code'):
        raise ValidationError(const.CONFIRMATION_CODE_ERROR)

    token = str(RefreshToken.for_user(user).access_token)
    models.User.objects.update(confirmation_code='')

    return Response({'token': token}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup_api_view(request):
    """Представление для самостоятельной регистрации.

    Создает нового пользователя, с дальнейшей отправкой на указанный email
    кода подтверждения. При повторном запросе происходит обновление
    кода подтверждения с повторной отправкой на email.
    """
    serializer = api_serializers.UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    confirmation_code = ''.join(random.choices(
        settings.CONFIRMATION_CODE_SYMBOLS,
        k=settings.CONFIRMATION_CODE_LENGTH,
    ))

    user = models.User.objects.filter(username=username, email=email).first()

    if user:
        user.confirmation_code = confirmation_code
        user.save()
    else:
        errors = {}
        if models.User.objects.filter(username=username).exists():
            errors.update({
                'username': f'Имя пользователя {username} уже занято.',
            })

        if models.User.objects.filter(email=email).exists():
            errors.update({
                'email': f'Почта {email} уже занята.',
            })

        if errors:
            raise ValidationError(errors)

        user = models.User.objects.create_user(
            username=username, email=email, confirmation_code=confirmation_code
        )

    utils.send_confirmation_email(user)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)
