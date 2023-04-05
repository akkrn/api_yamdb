from rest_framework import permissions
from rest_framework.permissions import DjangoObjectPermissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "admin" or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == "admin" or request.user.is_superuser
        )


class IsAdminOrRead(DjangoObjectPermissions):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.role == "admin" or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.role == "admin" or request.user.is_superuser)
        )


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "user"

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == "moderator"
        )


class Forbidden(permissions.BasePermission):
    def has_permission(self, request, view):
        return False
