from rest_framework import permissions


class AdminsPermissions(permissions.BasePermission):
    """Задает права доступа для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin)
        )


class IsAdminOrModeratorOrAuthor(AdminsPermissions):
    """
    Класс для установки доступа
    суперпользователю, администратору, модератору и автору,
    либо всем на чтение.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == user
            or user.is_authenticated and user.is_moderator
            or super().has_permission(request, view)
        )


class IsAdminOrReadOnly(AdminsPermissions):
    """Класс для установки доступа администраторам либо всем на чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )
