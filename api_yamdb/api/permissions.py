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


class IsAuthorModeratorAdmin(permissions.BasePermission):
    """
    Изменение и удаление разрешено только автору объекта,
    модератору или администратору.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.role in ('moderator', 'admin')
            or request.user.is_superuser
        )
