from itertools import zip_longest

from django.db.models import Q
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

    html = render_to_string('course/course_list_main_page.html', {'courses': courses})
    return HttpResponse(html)
