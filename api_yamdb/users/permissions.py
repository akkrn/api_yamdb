from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin"


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "user"

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "moderator"

    def has_object_permission(self, request, view, obj):
        return request.user.role == "moderator"
