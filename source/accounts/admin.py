from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser, Teacher, LevelSetting


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active', 'email_confirmed']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('email_confirmed', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email_confirmed', 'avatar')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'fullname',
        'is_approved',
        'request_code',
        'position',
    )
    list_display_links = (
        'id',
        'user',
        'fullname',
        'is_approved',
        'request_code',
        'position',
    )
    ordering = ('-id',)


@admin.register(LevelSetting)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'level',
        'xp_required',
    )
    list_display_links = (
        'id',
        'level',
        'xp_required',
    )
