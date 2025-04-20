from rest_framework import permissions


class AdminPermissions(permissions.BasePermission):
    """Кастомный класс доступа."""
    def has_permission(self, request, view):
        if view.action in ('create', 'update', 'partial_update', 'destroy'):
            return request.user.is_authenticated and request.user.is_staff
        return True
