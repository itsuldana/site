# webapp/views.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from rest_framework.status import HTTP_404_NOT_FOUND

from ..forms import LessonForm
from ..models import Lesson, Module, LessonProgress


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

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        lesson = self.get_object()
        if not lesson.module.course.purchases.filter(user=user, payment_status='DONE').exists():
            raise Http404('Вы не оплатили курс')

        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_lesson = self.object
        user = self.request.user

        # Получаем прогресс всех уроков текущего модуля
        module_lessons = current_lesson.module.lessons.all().order_by('id')
        lesson_progress_map = {lp.lesson_id: lp.status for lp in
                               LessonProgress.objects.filter(user=user, lesson__in=module_lessons)}

        # Добавляем в контекст список уроков с их статусом
        context['module_lessons'] = [
            {'lesson': lesson, 'status': lesson_progress_map.get(lesson.id)}
            for lesson in module_lessons
        ]

        # Логика для следующего урока и модуля
        next_lesson = module_lessons.filter(id__gt=current_lesson.id).first()
        if not next_lesson:
            next_module = Module.objects.filter(
                course=current_lesson.module.course,
                position__gt=current_lesson.module.position
            ).order_by('id').first()
            if next_module:
                next_lesson = next_module.lessons.order_by('id').first()

            # Если следующий урок найден, получаем его статус
        if next_lesson:
            next_lesson_status = LessonProgress.objects.filter(user=user, lesson=next_lesson).first()
            context['next_lesson'] = {
                'lesson': next_lesson,
                'status': next_lesson_status.status if next_lesson_status else None
            }
        else:
            context['next_lesson'] = None

        context['current_lesson'] = current_lesson
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
