# from rest_framework.permissions import BasePermission


# class IsAdminOrSuperuser(BasePermission):
#     """
#     Разрешение, которое проверяет, является ли пользователь админом
#     или суперпользователем.
#     """

#     def has_permission(self, request, view):
#         return request.user.is_superuser or request.user.role == 'admin'
