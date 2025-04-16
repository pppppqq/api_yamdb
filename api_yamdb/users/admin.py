from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'bio', 'role')
    list_editable = ('role',)
    search_fields = ('username',)
    list_filter = ('role',)


admin.site.register(CustomUser, CustomUserAdmin)
