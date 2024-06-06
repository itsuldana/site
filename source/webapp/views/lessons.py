# webapp/views.py

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from ..forms import LessonForm
from ..models import Lesson


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lesson/lesson_create.html'

    def form_valid(self, form):
        form.instance.module_id = self.kwargs['module_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('module_detail', kwargs={'pk': self.object.module_id})


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson/lesson_detail.html'


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lesson/lesson_edit.html'

    def get_success_url(self):
        return reverse_lazy('module_detail', kwargs={'pk': self.object.module_id})


class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'lesson/lesson_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('module_detail', kwargs={'pk': self.object.module_id})
