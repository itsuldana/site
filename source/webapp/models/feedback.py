from django.conf import settings
from django.db import models

from webapp.models import Lesson


class Feedback(models.Model):
    FEEDBACK_TYPE = [
        ('like', 'Нравится'),
        ('dislike', 'Не нравится')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Пользователь'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Урок'
    )
    feedback_type = models.CharField(
        choices=FEEDBACK_TYPE,
        max_length=7,
        verbose_name='Тип отзыва'

    )
    text = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
        verbose_name='Текст'
    )