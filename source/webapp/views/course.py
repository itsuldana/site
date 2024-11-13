from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count, Sum, Prefetch, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView
from ..forms import CourseForm
from ..models import Course, Tag, Module, LessonProgress, Purchase, Skills, Lesson


class CourseListView(ListView):
    template_name = 'course/course_list.html'

    context_object_name = 'courses'
    model = Course
    ordering = ['-created_at']

    paginate_by = 6
    paginate_orphans = 1

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_active=False)
        return queryset

    def test_func(self):
        return self.request.user.is_superuser


class CoursePaidListView(LoginRequiredMixin, ListView):
    template_name = 'course/course_paid_list.html'

    context_object_name = 'courses'
    model = Course

    paginate_by = 6
    paginate_orphans = 1

    login_url = reverse_lazy('login')

    def get_queryset(self):
        paid_courses_ids = Purchase.objects.filter(
            user=self.request.user,
            payment_status='DONE'
        ).order_by('-purchase_date').values_list('course_id', flat=True)

        # Фильтруем только оплаченные курсы
        queryset = Course.objects.filter(id__in=paid_courses_ids, is_active=True)
        return queryset


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

        # Пробрасываем похожие курсы (пока просто последние три, так как их мало)
        similar_courses = Course.objects.exclude(id=self.object.pk).order_by('-created_at')[:3]
        context['similar_courses'] = similar_courses

        # Пробрасываем все курсы (пока последние 4, так как их мало)
        all_courses = Course.objects.exclude(id=self.object.pk).order_by('-created_at')[:4]
        context['all_courses'] = all_courses

        # Пробрасываем скиллы, которым можно научиться на курсе
        skills = Skills.objects.filter(course=self.object).order_by('-priority').filter(is_active=True)
        context['skills'] = skills

        course = self.object
        modules = Module.objects.filter(course=course, is_active=True).prefetch_related(
            Prefetch('lessons', queryset=Lesson.objects.order_by('position'))
        )
        context["modules"] = modules
        context['tags'] = course.tag.all()

        lesson_stats = course.modules.aggregate(
            total_lessons=Count('lessons'),
            total_duration=Sum('lessons__duration')
        )

        context['total_lessons'] = lesson_stats['total_lessons'] or 0
        total_duration = lesson_stats['total_duration'] or 0

        hours, remainder = divmod(total_duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        context['total_duration'] = f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02} min"

        user = self.request.user
        if isinstance(user, AnonymousUser):
            context['is_paid'] = False
        else:
            lesson_progress_subquery = LessonProgress.objects.filter(
                user=user,
                lesson=OuterRef('pk')
            ).values('status')[:1]
            # Если статуса нет, возвращаем None
            lesson_progress_status = Coalesce(Subquery(lesson_progress_subquery), Value(None))

            # Подгружаем модули с уроками, аннотированными статусом прогресса
        modules = Module.objects.filter(course=course, is_active=True).prefetch_related(
            Prefetch(
                'lessons',
                queryset=Lesson.objects.filter(module__course=course).annotate(progress_status=lesson_progress_status)
            )
        )
        context["modules"] = modules
        context['is_paid'] = Purchase.objects.filter(user=user, course=course, payment_status='DONE').exists()

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
