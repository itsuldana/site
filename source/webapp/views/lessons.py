# webapp/views.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from ..forms import LessonForm
from ..models import Lesson, Module


class LessonCreateView(UserPassesTestMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lesson/lesson_create.html'

    def form_valid(self, form):
        form.instance.module_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('manage_lessons', kwargs={'pk': self.object.module_id})

    def test_func(self):
        return self.request.user.is_superuser


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson/lesson_detail.html'
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Текущий урок
        lesson = self.object

        # Все уроки текущего модуля
        module_lessons = lesson.module.lessons.order_by('id')
        context['module_lessons'] = module_lessons

        # Индекс текущего урока
        lesson_index = list(module_lessons).index(lesson)

        # Проверка, если следующий урок есть
        if lesson_index + 1 < len(module_lessons):
            context['next_lesson'] = module_lessons[lesson_index + 1]
        else:
            context['next_lesson'] = None  # Если текущий урок последний

        # Указание текущего урока
        context['current_lesson'] = lesson

        return context


class LessonUpdateView(UserPassesTestMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lesson/lesson_edit.html'

    def get_success_url(self):
        return reverse_lazy('manage_lessons', kwargs={'pk': self.object.module_id})

    def test_func(self):
        return self.request.user.is_superuser


class LessonDeleteView(UserPassesTestMixin, DeleteView):
    model = Lesson
    template_name = 'lesson/lesson_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        context['module'] = get_object_or_404(Module, pk=lesson.module_id)
        return context

    def get_success_url(self):
        return reverse_lazy('manage_modules', kwargs={'pk': self.object.module_id})

    def test_func(self):
        return self.request.user.is_superuser
