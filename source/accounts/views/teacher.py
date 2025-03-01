from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView

from accounts.forms import TeacherApplicationForm
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
            teacher.save()
            return reverse('teacher_detail', kwargs={'pk': request.user.pk})
        else:
            print("Форма не валидна:", form.errors)  # Отладка ошибок

    else:
        form = TeacherApplicationForm()

    return render(request, 'teachers/teacher_create.html', {'form': form})