from django.db import models


class Tag(models.Model):
    slug = models.SlugField(
        unique=True,
        verbose_name="Ключ"
    )
    name_ru = models.CharField(
        max_length=100,
        verbose_name="Название на русском"
    )
    name_en = models.CharField(
        max_length=100,
        verbose_name="Название на английском"
    )
    text_color = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        verbose_name="HEX цвет шрифта (цвет отображений на странице блога)"
    )
    background_color = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        verbose_name="HEX цвет бэкграунда (цвет отображений на странице блога)"
    )
    border_color = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        verbose_name="HEX цвет обводки (цвет отображений на странице блога)"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name_en
