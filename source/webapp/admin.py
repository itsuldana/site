from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Lesson, Module,Course

admin.site.register(Lesson)
admin.site.register(Module)
admin.site.register(Course)