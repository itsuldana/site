from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser, Teacher, LevelSetting


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['email', 'username', 'is_staff', 'is_active', 'email_confirmed']
    list_filter = ['is_staff', 'is_active', 'email_confirmed']

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Дополнительные поля',
            {
                'fields': (
                    'email_confirmed',
                    'avatar',
                    'social_network_link',
                    'xp',
                    'level',
                    'quiz_completed',
                    'recommended_tags',
                )
            },
        ),
    )

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Дополнительные поля',
            {
                'classes': ('wide',),
                'fields': (
                    'email_confirmed',
                    'avatar',
                    'social_network_link',
                ),
            },
        ),
    )


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
