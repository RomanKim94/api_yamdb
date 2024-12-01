from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.v1.permissions import IsNotSimpleUserOrAuthorOrCreateOnly
from api.v1.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    '''Вьюсет для работы с отзывами.'''
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsNotSimpleUserOrAuthorOrCreateOnly,
    )

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
