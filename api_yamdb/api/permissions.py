from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Разрешение, которое проверяет, является ли пользователь админом
    или суперпользователем.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == 'admin'


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
            # Анонимный юзер вообще не записан в бд!
            or getattr(request.user, 'role', None) in ('moderator', 'admin')
            or request.user.is_superuser
        )
