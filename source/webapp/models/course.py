from django.db import models

from PIL import Image
import os


class Course(models.Model):
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Name"
    )
    description = models.TextField(
        max_length=3000,
        null=False,
        blank=False,
        verbose_name='Description'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        verbose_name="Price"
    )
    image = models.ImageField(
        upload_to='course_images/',
        null=True,
        blank=True,
        verbose_name="Image"
    )
    tag = models.ManyToManyField(
        to='webapp.Tag',
        related_name='tags',
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        null=False,
        default=True
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

    def save(self, *args, **kwargs):
        try:
            this = Course.objects.get(id=self.id)
            if this.image and self.image != self.image:
                if os.path.isfile(this.image.path):
                    this.image.delete(save=False)
        except Course.DoesNotExist:
            pass

        super().save(*args, **kwargs)

        if self.image:
            self.crop_image()

    def crop_image(self):
        if os.path.isfile(self.image.path):  # Add this check
            img = Image.open(self.image.path)
            width, height = img.size
            aspect_ratio = 16 / 9

            if width / height > aspect_ratio:
                new_width = int(height * aspect_ratio)
                new_height = height
                left = (width - new_width) / 2
                top = 0
                right = (width + new_width) / 2
                bottom = new_height
            else:
                new_width = width
                new_height = int(width / aspect_ratio)
                left = 0
                top = (height - new_height) / 2
                right = new_width
                bottom = (height + new_height) / 2

            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)

    def __str__(self):
        return f'{self.title} - {self.description}'
