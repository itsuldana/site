from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView
from ..forms import CourseForm
from ..models import Course, Tag, Module, LessonProgress


class CourseListView(ListView):
    template_name = 'course/course_list.html'

    context_object_name = 'courses'
    model = Course
    ordering = ['-created_at']

    paginate_by = 6
    paginate_orphans = 1

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True)
        return queryset

    def test_func(self):
        return self.request.user.is_superuser


class CourseCreateView(UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/course_create.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        return self.request.user.is_superuser


class CourseUpdateView(UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/course_edit.html'
    success_url = reverse_lazy('manage_courses')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.image:
            self.object.crop_image()
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modules"] = Module.objects.all().filter(course=self.object)
        context['tags'] = self.object.tag.all()
        user = self.request.user
        context['lesson_progress'] = LessonProgress.objects.filter(user=user)
        return context


class CoursesView(ListView):
    template_name = 'courses.html'

    context_object_name = 'courses'
    model = Course
    ordering = ['-created_at']

    paginate_by = 6
    paginate_orphans = 1

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_deleted=True)
        tags = self.request.GET.getlist('tags')
        if tags:
            queryset = queryset.filter(tag__name__in=tags).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tags'] = self.request.GET.getlist('tags')
        return context
