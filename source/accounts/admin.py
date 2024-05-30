from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active', 'email_confirmed', 'avatar']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('email_confirmed', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email_confirmed', 'avatar')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
