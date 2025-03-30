from django.db import models

from webapp.models import Course


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Курс',
    )
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Заголовок"
    )
    description = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    position = models.PositiveIntegerField(
        verbose_name="Position"
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
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
        ordering = ['position']

    def __str__(self):
        return f'{self.position} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.id:
            last_position = Module.objects.filter(course=self.course).count()
            self.position = last_position + 1
        super().save(*args, **kwargs)

    def move_up(self):
        previous_module = Module.objects.filter(course=self.course, position__lt=self.position).order_by(
            '-position').first()
        if previous_module:
            previous_module.position, self.position = self.position, previous_module.position
            previous_module.save()
            self.save()

    def move_down(self):
        next_module = Module.objects.filter(course=self.course, position__gt=self.position).order_by(
            'position').first()
        if next_module:
            next_module.position, self.position = self.position, next_module.position
            next_module.save()
            self.save()

    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'