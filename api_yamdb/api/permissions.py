from rest_framework import permissions

from users.models import User


class IsNotSimpleUserOrAuthorOrCreateOnly(permissions.BasePermission):
    """
    Класс для установки доступа
    администраторам, модераторам, автору, либо всем на чтение.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in ('POST', 'GET')
            or obj.author == request.user
            or request.user.is_superuser
            or request.user.role in (User.ADMIN, User.MODERATOR)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс для установки доступа администраторам либо всем на чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == User.ADMIN
                         or request.user.is_superuser)))
