# from ckeditor.fields import RichTextField
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

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

    def __str__(self):
        return self.title
