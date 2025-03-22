from rest_framework import permissions

class IsUserOrAdmin(permissions.BasePermission):
    """
    Permission class to allow users to only modify their own profile,
    while admins can modify any profile.
    """
    def has_permission(self, request, view):
        # Allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read-only for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the user themselves or admin
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
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return hasattr(obj, 'user') and obj.user == request.user