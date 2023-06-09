from rest_framework import permissions
from rest_framework.permissions import DjangoObjectPermissions

from users.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == User.RoleChoice.ADMIN
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == User.RoleChoice.ADMIN
            or request.user.is_superuser
        )


class IsAdminOrRead(DjangoObjectPermissions):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.role == User.RoleChoice.ADMIN
                or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.role == User.RoleChoice.ADMIN
                or request.user.is_superuser
            )
        )


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.RoleChoice.USER
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.RoleChoice.MODERATOR
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user == obj.author
            or request.user.role == User.RoleChoice.MODERATOR
            or request.user.role == User.RoleChoice.ADMIN
            or request.user.is_superuser
        )
