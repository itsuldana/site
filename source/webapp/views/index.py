from itertools import zip_longest
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q, Count, Sum
from django.utils import translation
from django.views.generic import ListView

from accounts.models import Teacher
from blog.models import Post
from webapp.models import Course, Tag
from django.http import HttpResponse
from django.template.loader import render_to_string


class MainView(ListView):
    template_name = 'main.html'

    context_object_name = 'courses'
    model = Course
    ordering = ['-created_at']

    paginate_by = 6
    paginate_orphans = 1

    def get_queryset(self):
        courses = Course.objects.annotate(lesson_total=Count('modules__lessons'))

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

            if self.request.user.is_authenticated:
                user_discount = self.request.user.get_user_discount()  # Например, 20 для 20%
                discounted_price = course.price * (Decimal(100 - user_discount) / Decimal(100))

                # Округляем до целого числа
                purchase_amount = discounted_price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

                course.price_with_discount = purchase_amount

                price_with_discount_exists = 'Yes'

        self.price_with_discount_exists = price_with_discount_exists

        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teachers = Teacher.objects.all()

        courses = self.get_queryset()  # Достаём курсы для текущей страницы пагинации

        # Получение тегов, которые используются хотя бы в одном курсе
        tags = Tag.objects.filter(tags__in=courses).distinct()  # Используем правильное имя поля 'courses'

        # Разбиваем теги на чанки по 3
        chunked_tags = list(zip_longest(*[iter(tags)] * 3, fillvalue=None))

        context['teachers'] = teachers
        context['posts'] = Post.objects.all().order_by('-created_at').exclude(is_active=False)
        context['current_lang'] = translation.get_language()

        context['tags'] = chunked_tags

        context['price_with_discount_exists'] = self.price_with_discount_exists

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

    html = render_to_string('course/course_list_main_page.html', {
        'courses': courses,
        'price_with_discount_exists': price_with_discount_exists,
    })
    return HttpResponse(html)
