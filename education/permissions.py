from rest_framework.permissions import BasePermission


class IsNotStaff(BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_staff


class IsOwnerOrStaff(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff
