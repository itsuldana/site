from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from PIL import Image


class Post(models.Model):
    title_ru = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name="Заголовок на русском"
    )
    title_en = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name="Заголовок на английском"
    )

    image = models.FileField(
        upload_to='news/pictures/',
        verbose_name="Основная картинка поста",
    )
    image_list = models.FileField(
        upload_to='news/pictures/',
        verbose_name="Картинка для списка",
        null=True,
        blank=True
    )

    content_ru = CKEditor5Field(
        verbose_name='Контент на русском',
        config_name='extends'
    )
    content_en = CKEditor5Field(
        verbose_name='Контент на английском',
        config_name='extends'
    )

    tags = models.ManyToManyField(
        'blog.Tag',
        related_name='posts',
        verbose_name="Теги"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Показать?"
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

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title_ru[:50]

    def clean(self):
        super().clean()
        # Validate main image dimensions (aspect ratio 1.88 and minimum width of 800px)
        if self.image:
            self._validate_image_dimensions(self.image, required_aspect_ratio=1.88, min_width=800, field_name="image")

        # Validate image_list dimensions (aspect ratio 1 and minimum width of 360px)
        if self.image_list:
            self._validate_image_dimensions(self.image_list, required_aspect_ratio=1, min_width=360, field_name="image_list")

    def _validate_image_dimensions(self, image_field, required_aspect_ratio, min_width, field_name):
        try:
            with Image.open(image_field) as img:
                width, height = img.size
                aspect_ratio = width / height

                if abs(aspect_ratio - required_aspect_ratio) > 0.03:
                    raise ValidationError(
                        {field_name: f"The {field_name} must have an aspect ratio of {required_aspect_ratio}:1."}
                    )

                if width < min_width:
                    raise ValidationError(
                        {field_name: f"The {field_name} must be at least {min_width}px wide."}
                    )

        except Exception as e:
            raise ValidationError({field_name: f"An error occurred with the {field_name}: {str(e)}"})
