# from ckeditor.fields import RichTextField
from urllib.parse import urlparse, parse_qs

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import requests
import re

from webapp.models import Module


class Lesson(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Модуль'
    )
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Заголовок"
    )
    small_description = models.TextField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Краткое описание"
    )
    content = CKEditor5Field(
        'Content',
        config_name='extends'
    )
    key_takeaway = CKEditor5Field(
        'Key Takeaway',
        config_name='extends'
    )
    video_url = models.URLField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="Видео URL"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
        null=True
    )
    thumbnail_url = models.URLField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="URL превью"
    )
    duration = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Длительность видео"
    )
    position = models.PositiveIntegerField(
        verbose_name="Position",
        default=1,
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name="Активен"
    )

    def __str__(self):
        return self.title

    def fetch_youtube_data(self, api_key):
        # Извлечение идентификатора видео из URL
        query = urlparse(self.video_url).query
        video_id = parse_qs(query).get('v')
        if video_id:
            video_id = video_id[0]  # Получаем первый ID из списка
        else:
            print("Некорректный формат URL видео.")
            return  # Выходим, если ID видео не найден

        url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=contentDetails,snippet&key={api_key}'
        print(f"URL запроса: {url}")  # Логирование URL

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("Данные ответа:", data)  # Логирование данных для отладки
            if data.get('items'):
                video_info = data['items'][0]
                self.thumbnail_url = video_info['snippet']['thumbnails']['high']['url']

                iso_duration = video_info['contentDetails']['duration']
                match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
                hours, minutes, seconds = map(lambda x: int(x) if x else 0, match.groups())
                self.duration = hours * 3600 + minutes * 60 + seconds
            else:
                print("Элементы не найдены в данных ответа. Проверьте ID видео и ключ API.")
        else:
            print(f"Не удалось получить данные из YouTube API. Код статуса: {response.status_code}")

    def save(self, *args, **kwargs):
        # Проверка, изменился ли URL видео
        if self.pk:
            # Получаем исходный объект из базы данных
            original = Lesson.objects.get(pk=self.pk)
            if original.video_url != self.video_url:
                # Обновляем данные только если URL видео изменился
                API_KEY = 'AIzaSyD4Y8Cg2fdGLUIlvteRxSvhRhRpS82R8h0'
                self.fetch_youtube_data(API_KEY)
        else:
            # Новый объект, у которого видео-данные ещё не были получены
            API_KEY = 'AIzaSyD4Y8Cg2fdGLUIlvteRxSvhRhRpS82R8h0'
            self.fetch_youtube_data(API_KEY)

        # Вызов супер сохранения только один раз
        super().save(*args, **kwargs)


    def formatted_duration(self):
        if self.duration:
            hours, remainder = divmod(self.duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02}"
        else:
            return " "

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'