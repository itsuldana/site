from django.db import models
from webapp.models.course import Course

class Skills(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name='Курс',
    )

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Скилл на русском"
    )

    priority = models.PositiveSmallIntegerField(
        unique=False,
        verbose_name="Порядок"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
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

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return f"{self.name}"
