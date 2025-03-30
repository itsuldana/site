from django.contrib import admin

from .models import Lesson, TestModule, Module, AnswerOption, Test, TestCaseDescriptions, Course, TestHistory, Skills, \
    Purchase


class AnswerOptionInline(admin.TabularInline):  # Можно использовать StackedInline для другого оформления
    model = AnswerOption
    extra = 1  # Количество пустых форм для добавления новых вариантов ответов


class TestModuleAdmin(admin.ModelAdmin):
    list_display = ('module', 'created_at', 'description_preview')
    search_fields = ('description',)


class TestAdmin(admin.ModelAdmin):
    list_display = ('test_module_id', 'question_text')
    search_fields = ('question_text',)
    inlines = [AnswerOptionInline]
    # Добавляем инлайн для AnswerOption
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'teacher', 'price')
    search_fields = ('title',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'module', 'title')
    search_fields = ('title',)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course')
    search_fields = ('title',)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'payment_code',
        'course',
        'payment_status',
        'purchase_date',
    )
    search_fields = (
        'id',
        'user',
        'payment_code',
        'course',
        'payment_status',
        'purchase_date',
    )
    list_display_links = (
        'id',
        'user',
        'payment_code',
        'course',
        'payment_status',
        'purchase_date',
    )


admin.site.register(Lesson, LessonAdmin)
admin.site.register(TestModule)
admin.site.register(Module,ModuleAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestCaseDescriptions)
admin.site.register(Course, CourseAdmin)
admin.site.register(TestHistory)
admin.site.register(Purchase, PurchaseAdmin)

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'priority',
        'name',
        'course',
        'is_active',
    )
    list_display_links = (
        'id',
        'priority',
        'name',
        'course',
        'is_active',
    )
