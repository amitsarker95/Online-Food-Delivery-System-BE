from rest_framework import permissions

class IsUserOrAdmin(permissions.BasePermission):
    """
    Permission class to allow users to only modify their own profile,
    while admins can modify any profile.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user or request.user.is_staff

class IsAdminUser(permissions.BasePermission):
    """
    Permission class to only allow admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission class to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return hasattr(obj, 'user') and obj.user == request.user