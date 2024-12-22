from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.utils.translation import get_language
from django.utils import translation
from django.db.models import Q
from bs4 import BeautifulSoup
import hashlib

from blog.models import Post, Tag


class PostListView(ListView):
    template_name = 'post_list.html'
    context_object_name = 'posts'
    model = Post

    ordering = ['-created_at']
    paginate_by = 8
    paginate_orphans = 1

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_active=False)
        selected_tag = self.request.GET.get('tag')
        search_query = self.request.GET.get('search_query', '')

        if selected_tag:
            queryset = queryset.filter(tags__slug=selected_tag).distinct()
        if search_query:
            queryset = queryset.filter(
                Q(title_ru__icontains=search_query) |
                Q(title_en__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tag'] = self.request.GET.get('tag')
        context['search_query'] = self.request.GET.get('search_query', '')

        paginator = Paginator(self.get_queryset(), self.paginate_by, orphans=self.paginate_orphans)
        page_number = self.request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['page_number'] = page_obj.number
        context['current_lang'] = translation.get_language()

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.object.tags.all()

        # Определяем текущий язык
        current_lang = get_language()

        # Получаем контент в зависимости от языка
        if current_lang == "en":
            content = self.object.content_en
        else:
            content = self.object.content_ru

        # Извлекаем заголовки и добавляем их в контекст
        context['headings'], context['content'] = self.process_content(content)

        # Получаем последние 10 новостей с такими же тегами, как у текущей новости
        similar_news = Post.objects.filter(
            tags__in=self.object.tags.all(),
            is_active=True
        ).exclude(id=self.object.id).distinct().exclude(is_active=False).order_by('-created_at')[:10]

        context['similar_posts'] = similar_news

        context['current_lang'] = translation.get_language()

        return context

    def process_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        headings = []
        for tag in ['h1', 'h2', 'h3']:  # можно добавить другие уровни заголовков, если необходимо
            for header in soup.find_all(tag):
                if not header.has_attr('id'):
                    # Генерация уникального id на основе текста заголовка
                    header_id = hashlib.md5(header.text.encode('utf-8')).hexdigest()[:8]
                    header['id'] = header_id
                headings.append((header.text, header['id']))

        # Обновленный контент с добавленными id
        updated_content = str(soup)

        return headings, updated_content
