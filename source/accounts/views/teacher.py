from django.views.generic import ListView, DetailView

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
