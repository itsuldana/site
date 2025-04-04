from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count, Sum, Prefetch, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView

from accounts.models import Teacher
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

        self.price_with_discount_exists = 'No'

        for course in queryset:

            if self.request.user.is_authenticated:
                user_discount = self.request.user.get_user_discount()  # Например, 20 для 20%
                discounted_price = course.price * (Decimal(100 - user_discount) / Decimal(100))

                # Округляем до целого числа
                purchase_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

                course.price_with_discount = purchase_amount

                if user_discount != 0:
                    self.price_with_discount_exists = 'Yes'

        return queryset

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['price_with_discount_exists'] = self.price_with_discount_exists

        return context

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


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/course_create.html'

    def form_valid(self, form):
        teacher = Teacher.objects.get(user_id=self.request.user.id)
        form.instance.teacher = teacher
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('teacher_detail', kwargs={'pk': self.request.user.user_teacher.first().pk})

    # def test_func(self):
    #     return self.request.user


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/course_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.image:
            self.object.crop_image()
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        teacher = self.request.user.user_teacher.first()  # Получение первого Teacher связанного с пользователем
        if teacher:
            return reverse('teacher_detail', kwargs={'pk': teacher.pk})
        else:
            return reverse('index')


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/course_detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_paid'] = False

        context['price_with_discount_exists'] = 'No'
        course = Course.objects.get(pk=self.kwargs['pk'])

        if self.request.user.is_authenticated:
            user_discount = self.request.user.get_user_discount()  # Например, 20 для 20%
            discounted_price = course.price * (Decimal(100 - user_discount) / Decimal(100))

            # Округляем до целого числа
            purchase_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

            if user_discount != 0:
                context['price_with_discount_exists'] = 'Yes'
                context['price_with_discount'] = purchase_amount

        # Пробрасываем похожие курсы (пока просто последние три, так как их мало)
        similar_courses = Course.objects.exclude(id=self.object.pk).order_by('-created_at')[:3]
        context['price_with_discount_similar_exists'] = 'No'

        for course in similar_courses:
            if self.request.user.is_authenticated:
                user_discount = self.request.user.get_user_discount()  # Например, 20 для 20%
                discounted_price = course.price * (Decimal(100 - user_discount) / Decimal(100))

                # Округляем до целого числа
                purchase_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

                course.price_with_discount = purchase_amount

                if user_discount != 0:
                    context['price_with_discount_similar_exists'] = 'Yes'


        context['similar_courses'] = similar_courses

        # Пробрасываем все курсы (пока последние 4, так как их мало)
        all_courses = Course.objects.exclude(id=self.object.pk).order_by('-created_at')[:4]
        context['price_with_discount_all_courses_exists'] = 'No'

        for course in all_courses:
            if self.request.user.is_authenticated:
                user_discount = self.request.user.get_user_discount()  # Например, 20 для 20%
                discounted_price = course.price * (Decimal(100 - user_discount) / Decimal(100))

                # Округляем до целого числа
                purchase_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

                course.price_with_discount = purchase_amount

                if user_discount != 0:
                    context['price_with_discount_all_courses_exists'] = 'Yes'

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
        context[
            'total_duration'] = f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02} min"

        user = self.request.user
        if not isinstance(user, AnonymousUser):
            lesson_progress_subquery = LessonProgress.objects.filter(
                user=user,
                lesson=OuterRef('pk')
            ).values('status')[:1]
            # Если статуса нет, возвращаем None
            lesson_progress_status = Coalesce(Subquery(lesson_progress_subquery), Value(None))

            if Purchase.objects.filter(user=user, course=self.object, payment_status="DONE").exists():
                context['is_paid'] = True

        # Подгружаем модули с уроками, аннотированными статусом прогресса
        lessons = Lesson.objects.filter(module__course=course)
        if context['is_paid']:
            lessons = lessons.annotate(progress_status=lesson_progress_status)

        modules = Module.objects.filter(course=course, is_active=True).prefetch_related(
            Prefetch(
                'lessons',
                queryset=lessons
            )
        )
        context["modules"] = modules
        context['students'] = Purchase.objects.filter(course=course, payment_status='DONE').count()

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
