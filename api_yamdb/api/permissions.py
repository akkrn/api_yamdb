from rest_framework import permissions


class CategoriesPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.role == "admin" or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_staff
        )