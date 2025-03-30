from django.db import models
from django.conf import settings
from webapp.models import Course


class Purchase(models.Model):
    STATUS_CHOICE = [
        ('PENDING', 'В ожидании'),
        ('DONE', 'Оплачено')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователи'

    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Курсы'
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default='PENDING',
        verbose_name='Статус оплаты'
    )
    payment_code = models.CharField(
        unique=True,
        max_length=6,
        blank=False,
        null=False,
        verbose_name="Код оплаты",
    )
    purchase_amount = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Сумма оплаты",
    )

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payment'