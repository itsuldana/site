from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from ..forms import CourseForm
from ..models import Course


class CourseListView(ListView):
    template_name = 'course/course_list.html'

    context_object_name = 'courses'
    model = Course
    ordering = ['created_at']

    paginate_by = 6
    paginate_orphans = 1

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True)
        return queryset


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/course_create.html'
    success_url = reverse_lazy('course_list')


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/course_edit.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.image:
            self.object.crop_image()
        self.object.save()
        return super().form_valid(form)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/course_detail.html'

