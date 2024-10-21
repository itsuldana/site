from django.db import models
from webapp.models.lessons import Lesson
from accounts.models import CustomUser


class LessonProgress(models.Model):
    STATUS_CHOICE = [
        ('in_progress', 'В процессе'),
        ('done', 'Закончен')
    ]
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='Урок',
        related_name='lesson_progress'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_progress'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICE,
        default='in_progress',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата завершения'
    )

    class Meta:
        unique_together = ('lesson', 'user')
