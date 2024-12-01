from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Comment, Review
from constants import SCORE_VALIDATION_ERROR


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        read_only_fields = ('pub_date',)

    def validate_score(self, score):
        '''Валидация поля score на соответствие диапазону от 1 до 10.'''
        if 1 > score > 10:
            raise ValidationError(
                {'score': SCORE_VALIDATION_ERROR.format(score=score)}
            )
        return score


class CommentSerializer(ReviewSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'author', 'pub_date')
        read_only_fields = ('pub_date',)
