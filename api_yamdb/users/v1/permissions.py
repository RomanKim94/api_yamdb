from rest_framework import permissions


class AdminsPermissions(permissions.BasePermission):
    """Задает права доступа для администраторов и суперпользователей."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin)
        )
