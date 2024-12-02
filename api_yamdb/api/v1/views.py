from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from api.v1.filters import TitleFilter
from api.v1.permissions import (
    IsAdminOrReadOnly, IsNotSimpleUserOrAuthorOrCreateOnly,
)

from api.v1.serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSerializer,
)
from api.v1.viewsets import ListCreateDeleteViewset
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(ListCreateDeleteViewset):
    """Представление для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewset):
    """Представление для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для произведений."""

    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name', '-year').all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    '''Вьюсет для работы с отзывами.'''
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsNotSimpleUserOrAuthorOrCreateOnly,
    )
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_title(self):
        '''Метод возвращает объект произведения по id полученного из url.'''
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ReviewViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        '''
        Метод возвращает объект отзыва к произведению по id полученного из url.
        '''
        return get_object_or_404(
            Review, title=self.get_title(), pk=self.kwargs['review_id']
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()
