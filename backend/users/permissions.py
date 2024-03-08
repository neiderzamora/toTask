from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'manager'

class IsSupervisor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 'supervisor'

class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 'staff'