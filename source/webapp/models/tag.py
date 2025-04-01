from django.db import models


class Tag(models.Model):
    name_ru = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
    )
    name_en = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        null=False,
        blank=False,
    )


    def __str__(self):
        return f'{self.name_ru}'
