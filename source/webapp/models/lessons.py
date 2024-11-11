# from ckeditor.fields import RichTextField
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
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name="Активен"
    )

    def __str__(self):
        return self.title

    def fetch_youtube_data(self, api_key):
        video_id = self.video_url.split('v=')[-1]
        url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=contentDetails,snippet&key={api_key}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['items']:
                video_info = data['items'][0]
                self.thumbnail_url = video_info['snippet']['thumbnails']['high']['url']

                iso_duration = video_info['contentDetails']['duration']
                match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
                hours, minutes, seconds = map(lambda x: int(x) if x else 0, match.groups())
                self.duration = hours * 3600 + minutes * 60 + seconds

                self.save()
        else:
            print("Не удалось получить данные из YouTube API.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.video_url and not self.thumbnail_url and not self.duration:
            API_KEY = 'AIzaSyD4Y8Cg2fdGLUIlvteRxSvhRhRpS82R8h0'
            self.fetch_youtube_data(API_KEY)

    def formatted_duration(self):
        if self.duration:
            hours, remainder = divmod(self.duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}" if hours else f"{minutes:02}:{seconds:02}"
        else:
            return " "