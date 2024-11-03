from django.contrib import admin
from django.contrib import admin

from .models import Lesson, TestModule, Module, AnswerOption, Test, TestCaseDescriptions, Course


class AnswerOptionInline(admin.TabularInline):  # Можно использовать StackedInline для другого оформления
    model = AnswerOption
    extra = 1  # Количество пустых форм для добавления новых вариантов ответов


class TestModuleAdmin(admin.ModelAdmin):
    list_display = ('module', 'created_at', 'description_preview')
    search_fields = ('description',)


class TestAdmin(admin.ModelAdmin):
    list_display = ('test_module_id', 'question_text')
    search_fields = ('question_text',)
    inlines = [AnswerOptionInline]  # Добавляем инлайн для AnswerOption

admin.site.register(Lesson)
admin.site.register(TestModule)
admin.site.register(Module)
admin.site.register(Test, TestAdmin)
admin.site.register(TestCaseDescriptions)
admin.site.register(Course)
