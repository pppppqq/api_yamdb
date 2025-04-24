from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Разрешение, которое проверяет, является ли пользователь админом
    или суперпользователем.
    """

    def has_permission(self, request, view):
        return request.user.is_admin


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
                    user.is_admin
                    or user.is_moderator
                    or obj.author == user
                )
            )
        )
