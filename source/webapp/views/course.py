import random
from decimal import Decimal, ROUND_HALF_UP
from itertools import zip_longest
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count, Sum, Prefetch, OuterRef, Subquery, Value, Q
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
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

        courses = self.get_queryset()  # Достаём курсы для текущей страницы пагинации

        # Получение тегов, которые используются хотя бы в одном курсе
        tags = Tag.objects.filter(tags__in=courses).distinct()  # Используем правильное имя поля 'courses'

        # Разбиваем теги на чанки по 3
        chunked_tags = list(zip_longest(*[iter(tags)] * 3, fillvalue=None))

        context['tags'] = chunked_tags

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['price_with_discount_exists'] = self.price_with_discount_exists

        return context


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/course_create.html'

    def form_valid(self, form):
        teacher = Teacher.objects.get(user_id=self.request.user.id)
        form.instance.teacher = teacher
        response = super().form_valid(form)

        # Создаем покупку для преподавателя (user)
        Purchase.objects.create(
            user=teacher.user,
            course=form.instance,
            payment_status='DONE',
            payment_code=f'{random.randint(0, 0xFFFFFF):06X}',  # Пример генерации уникального 6-символьного кода
            purchase_amount=int(form.instance.price),  # Приведение к int, если DecimalField
            has_certificate=False,
        )

        return response

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

        # 👇 Проверка: есть ли связанные тесты
        context['test_exists'] = course.test_case_descriptions.exists()

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


def filter_courses(request):
    tag_code = request.GET.get('tag_code', 'all')
    search_query = request.GET.get('search_query', '').strip()

    # Фильтрация по тегу
    if tag_code == 'all':
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(tag__code=tag_code)

    # Поиск по названию курса или описанию (можешь добавить другие поля, если нужно)
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Сортировка по дате
    courses = courses.order_by('-created_at')

    courses = courses.annotate(lesson_total=Count('modules__lessons'))

    price_with_discount_exists = 'No'

    for course in courses:
        lesson_stats = course.modules.aggregate(
            total_lessons=Count('lessons'),
            total_duration=Sum('lessons__duration')
        )

        total_duration = lesson_stats['total_duration'] or 0

        hours, remainder = divmod(total_duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        course.total_duration = f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02} min"

        if request.user.is_authenticated:
            user_discount = request.user.get_user_discount()  # Например, 20 для 20%
            discounted_price = course.price * (Decimal(100 - user_discount) / Decimal(100))

            # Округляем до целого числа
            purchase_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

            course.price_with_discount = purchase_amount

            price_with_discount_exists = 'Yes'

    html = render_to_string('partial/course_list_list_page.html', {
        'courses': courses,
        'price_with_discount_exists': price_with_discount_exists,
    })
    return HttpResponse(html)


class RecommendedCoursesView(ListView):
    model = Course
    template_name = 'course/course_recommended.html'
    context_object_name = 'courses'
    paginate_by = 6
    paginate_orphans = 1

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.recommended_tags.exists():
            courses = Course.objects.filter(tag__in=user.recommended_tags.all()).distinct()
        else:
            courses = Course.objects.none()

        # Обогащаем каждый курс дополнительными данными
        for course in courses:
            lesson_stats = course.modules.aggregate(
                total_lessons=Count('lessons'),
                total_duration=Sum('lessons__duration')
            )

            total_duration = lesson_stats['total_duration'] or 0
            hours, remainder = divmod(total_duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            course.total_duration = f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02} min"

            # Применяем пользовательскую скидку
            if user.is_authenticated:
                user_discount = user.get_user_discount()  # Например, возвращает 10 для 10%
                discounted_price = course.price * (Decimal(100 - user_discount) / Decimal(100))
                course.price_with_discount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

        return courses

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.recommended_tags.exists():
            courses = Course.objects.filter(tag__in=user.recommended_tags.all()).distinct()
        else:
            courses = Course.objects.none()

        self.price_with_discount_exists = 'No'

        for course in courses:

            if self.request.user.is_authenticated:
                user_discount = self.request.user.get_user_discount()  # Например, 20 для 20%
                discounted_price = course.price * (Decimal(100 - user_discount) / Decimal(100))

                # Округляем до целого числа
                purchase_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

                course.price_with_discount = purchase_amount

                if user_discount != 0:
                    self.price_with_discount_exists = 'Yes'

        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['recommended_tags'] = self.request.user.recommended_tags.all()
        context['price_with_discount_exists'] = self.price_with_discount_exists

        return context
