from rest_framework import permissions

class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous
    
class IsOwnerOrder(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user==obj.user