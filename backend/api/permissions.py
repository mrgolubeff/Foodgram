from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
            or request.user.is_superuser
            or request.user == obj.author
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
            or request.user.is_superuser
        )
