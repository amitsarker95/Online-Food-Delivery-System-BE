from rest_framework import permissions

class IsRestaurantOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_restaurant

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_customer