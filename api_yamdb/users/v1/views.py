from rest_framework import (
    filters,
    mixins,
    pagination,
    permissions,
    viewsets,
)

from permissions import IsAdmin
from users.models import User
from .serializers import (
    UserSerializer,
    ProfileSerializer,
)


class UserModelViewSet(viewsets.ModelViewSet):
    """Представление для API Пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
    # permission_classes = (permissions.IsAuthenticated, IsAdmin,)


class ProfileModelViewSet(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    """Представление для API Профиля пользователя."""
    serializer_class = ProfileSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
