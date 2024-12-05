from rest_framework import permissions


class IsSuperuserOrAdminOrModeratorOrAuthor(
    permissions.BasePermission,
):
    """
    Класс для установки доступа
    суперпользователю, администратору, модератору и автору,
    либо всем на чтение.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == user
            or user.is_authenticated and (
                user.is_moderator
                or user.is_admin
                or user.is_superuser
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс для установки доступа администраторам либо всем на чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin
                         or request.user.is_superuser)))


class AdminsPermissions(permissions.BasePermission):
    """Задает права доступа для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin)
        )
