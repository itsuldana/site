from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from accounts.models import Teacher
from webapp.forms import CourseModuleForm
from webapp.models import Module, Course




class ModuleCreateView(CreateView):
    model = Module
    form_class = CourseModuleForm
    template_name = 'module/module_create.html'
    success_url = reverse_lazy('course_list')

    def get_success_url(self):
        return reverse_lazy('manage_modules', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.course = Course.objects.get(id=self.kwargs['pk'])
        self.object = form.save(commit=False)
        last_position = Module.objects.filter(course=self.object.course).count()
        self.object.position = last_position + 1
        self.object.save()
        return super().form_valid(form)


class ModuleUpdateView(UpdateView):
    model = Module
    form_class = CourseModuleForm
    template_name = 'module/module_edit.html'
    success_url = reverse_lazy('manage_modules')

    def get_success_url(self):
        return reverse_lazy('manage_modules', kwargs={'pk': self.object.course_id})


class ManageModulesView(DetailView):
    model = Course
    template_name = 'module/module_manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["modules"] = Module.objects.filter(course=self.object)
        context["teacher_id"] = Teacher.objects.get(user_id=self.request.user.id).pk

        return context
