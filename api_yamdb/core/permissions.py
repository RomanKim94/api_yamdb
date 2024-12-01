from rest_framework import permissions

from users.models import User


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
    """Задает права доступа для модераторов."""

    def has_permission(self, request, view):
        return bool(
            isinstance(request.user, User)
            and request.user.is_moderator
        )


class IsAdmin(permissions.IsAuthenticated):
    """Задает права доступа для администраторов."""

    def has_permission(self, request, view):
        return bool(
            isinstance(request.user, User)
            and request.user.is_admin
        )


class AdminsPermissions(permissions.BasePermission):
    """Задает права доступа для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        return bool(
            isinstance(request.user, User)
            and request.user.is_admin
            or request.user.is_staff
        )


class IsUser(permissions.IsAuthenticated):
    """Задает права доступа для пользователей."""

    def has_permission(self, request, view):
        return bool(
            isinstance(request.user, User)
            and request.user.is_user
        )
