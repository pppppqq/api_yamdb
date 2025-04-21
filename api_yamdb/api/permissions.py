from rest_framework import permissions


class AdminPermissions(permissions.BasePermission):
    """Кастомный класс доступа."""
    def has_permission(self, request, view):
        if view.action in ('create', 'update', 'partial_update', 'destroy'):
            return request.user.is_authenticated and request.user.is_staff
        return True


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Читать могут все.
    Писать — аутентифицированные.
    Редактировать и удалять — автор или модератор или админ.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            obj.author == request.user
            or getattr(request.user, 'role', None) in ('moderator', 'admin')
            or request.user.is_staff
        )
