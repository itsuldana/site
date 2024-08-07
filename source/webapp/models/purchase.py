from django.db import models
from django.conf import settings
from webapp.models import Course


class Purchase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True
    )
    payment_status = models.CharField(
        max_length=20,
        default='PENDING'
    )

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'
