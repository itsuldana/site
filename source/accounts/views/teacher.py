from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import random

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from rest_framework.reverse import reverse

from accounts.forms import TeacherApplicationForm, TeacherUpdateForm
from accounts.models import Teacher
from webapp.models import Course


class TeacherListView(ListView):
    template_name = 'teachers/teachers_list.html'

    context_object_name = 'teachers'
    model = Teacher
    ordering = ['-fullname']

    paginate_by = 6
    paginate_orphans = 1


class TeacherDetailView(DetailView):
    template_name = 'teachers/teachers_detail.html'
    model = Teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(teacher=self.object).filter(is_active=True)
        return context


@login_required
def become_teacher(request):
    if hasattr(request.user, 'teacher_set') and request.user.teacher_set.exists():
        return redirect('teacher_detail')  # Если уже преподаватель, перенаправляем в профиль

    if request.method == 'POST':
        print("Форма отправлена!")  # Для проверки в консоли
        form = TeacherApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            print("Форма валидна, создаем преподавателя")  # Для отладки
            teacher = form.save(commit=False)
            teacher.user = request.user
            teacher.request_code = f'{random.randint(0, 0xFFFFFF):06X}'
            teacher.save()

            if teacher.certificate:
                return redirect('teacher_confirm')
            else:
                return redirect(reverse('teacher_payment', kwargs={'pk': teacher.pk}))
        else:
            print("Форма не валидна:", form.errors)  # Отладка ошибок

    else:
        form = TeacherApplicationForm()

    return render(request, 'teachers/teacher_create.html', {'form': form})


class TeacherConfirmView(TemplateView):
    template_name = 'teachers/teacher_confirm.html'


class TeacherPaymentView(DetailView):
    model = Teacher
    template_name = 'teachers/teacher_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherUpdateForm
    template_name = 'teachers/teacher_update.html'

    def get_success_url(self):
        return reverse_lazy('teacher_detail', kwargs={'pk': self.object.pk})
