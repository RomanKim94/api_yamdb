from rest_framework import permissions


def is_admin(request):
    return (
        request.user.is_authenticated
        and request.user.is_admin
    )


class AdminsPermissions(permissions.BasePermission):
    """Задает права доступа для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        return is_admin(request)


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    """Устанавливает доступ суперпользователю/админу/модератору/автору.

    Анонимным пользователям доступ только на чтение.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == user
            or user.is_authenticated and user.is_moderator
            or is_admin(request)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс для установки доступа администраторам либо всем на чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or is_admin(request)
        )
