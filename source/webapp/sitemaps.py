from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post
from .models import Course

# Сайтмэп для статических страниц
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'contact_us', 'course_list',]  # Укажите имена маршрутов для ваших статических страниц

    def location(self, item):
        return reverse(item)

# Сайтмэп для динамических страниц (например, страницы на основе модели)
class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Course.objects.filter(is_active=True)  # Например, активные объекты модели

    def lastmod(self, obj):
        return obj.updated_at  # Дата последнего обновления объекта

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(is_active=True)  # Например, активные объекты модели

    def lastmod(self, obj):
        return obj.updated_at  # Дата последнего обновления объекта