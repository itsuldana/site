from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Tag)
class CustomAdminClass(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name_ru', 'name_kz', 'name_en')
    list_display_links = ('id', 'slug', 'name_ru', 'name_kz', 'name_en')


@admin.register(Post)
class CustomAdminClass(admin.ModelAdmin):
    list_display = (
        "id",
        'title_ru',
        'title_kz',
        'title_en',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        "id",
        'title_ru',
        'title_kz',
        'title_en',
        'is_active',
        'created_at',
        'updated_at',
    )
