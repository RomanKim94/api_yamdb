from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Задает права доступа для аннонимных пользователей и авторов."""

    def has_object_permission(self, request, view, obj):
        """Задает правило доступа к конкретному объекту.

        Разрешает доступ для всех пользователей при методах
        'GET', 'HEAD', 'OPTIONS', а для остальных методов только авторам.
        """
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_moderator)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)
