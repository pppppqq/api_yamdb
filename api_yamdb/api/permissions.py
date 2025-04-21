from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Разрешение, которое проверяет, является ли пользователь админом
    или суперпользователем.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )


class IsAdminOrSuperuserOrReadOnly(permissions.BasePermission):
    """
    Разрешает:
    - SAFE_METHODS (GET, HEAD, OPTIONS) всем.
    - Остальные методы (POST, PUT, DELETE) только админам/суперпользователям.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (request.user.is_superuser or request.user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAuthorModeratorAdmin(permissions.BasePermission):
    """
    Читать могут все.
    Писать — аутентифицированные.
    Редактировать и удалять — автор или модератор или админ.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.role in ('moderator', 'admin')
            or request.user.is_superuser
        )
