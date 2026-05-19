# shared/simple_permissions.py
from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, 'user_id')

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, 'is_admin') and request.is_admin


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit, but anyone to read.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only allowed to admin users
        return request.user and getattr(request.user, 'is_admin', False)
