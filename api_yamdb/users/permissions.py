from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "user"


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "moderator"


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAnonim(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
