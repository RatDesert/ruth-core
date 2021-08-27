from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Checks if user is owner of requested object."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
