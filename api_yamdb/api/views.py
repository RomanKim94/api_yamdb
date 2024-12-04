from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    generics,
    mixins,
    permissions,
    status,
    views,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api import serializers as api_serializers, utils
from api import permissions as api_permissions
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
    queryset = models.Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (api_permissions.IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return api_serializers.TitleReadSerializer
        return api_serializers.TitleWrightSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = api_serializers.ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        api_permissions.IsSuperuserOrAdminOrModeratorOrAuthor,
    )
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_title(self):
        """Метод возвращает объект произведения по id полученного из url."""
        return get_object_or_404(models.Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ReviewViewSet):
    """Представление для комментариев."""

    serializer_class = api_serializers.CommentSerializer

    def get_review(self):
        '''
        Метод возвращает объект отзыва к произведению по id полученного из url.
        '''
        return get_object_or_404(
            models.Review, title=self.get_title(), pk=self.kwargs['review_id']
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
            return api_serializers.ProfileSerializer

        return super(UserModelViewSet, self).get_serializer_class()


class TokenApiView(views.APIView):
    """Представление для генерации токена аунтентификации.

    Доступно для не авторизованного пользователя.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = api_serializers.UsernameConfirmationCodeSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = generics.get_object_or_404(
            models.User, username=request.data.get('username')
        )

        if user.confirmation_code != request.data.get('confirmation_code'):
            raise ValidationError(f'Некорректный код подтверждения.')

        return Response(
            {'token': utils.get_token_for_user(user)},
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
        serializer = api_serializers.UserSignupSerializer(data=request.data)

        if user:
            serializer.instance = user

        serializer.is_valid(raise_exception=True)
        user = serializer.save(
            confirmation_code=utils.generate_confirmation_code()
        )
        utils.send_confirmation_email(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
