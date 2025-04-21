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
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or (
                user.is_authenticated and (
                    obj.author == user
                    or user.role in ('moderator', 'admin')
                    or user.is_superuser
                )
            )
        )
