from rest_framework import permissions

from users.models import User


class IsNotSimpleUserOrAuthorOrCreateOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in ('POST', 'GET')
            or obj.author == request.user
            or request.user.is_superuser
            or request.user.role in (User.ADMIN, User.MODERATOR)
        )
