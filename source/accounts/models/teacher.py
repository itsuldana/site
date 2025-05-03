from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image

from accounts.models import CustomUser


class Teacher(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_teacher',
    )
    fullname = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name="Полное имя"
    )
    position = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Специализация"
    )
    instagram = models.URLField(
        null=True,
        blank=True,
        verbose_name="Instagram Profile URL",
    )
    facebook = models.URLField(
        null=True,
        blank=True,
        verbose_name="Facebook Profile URL",
    )
    linkedin = models.URLField(
        null=True,
        blank=True,
        verbose_name="Linkedin Profile URL",
    )
    twitter = models.URLField(
        null=True,
        blank=True,
        verbose_name="Twitter Profile URL",
    )
    phone_number = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        verbose_name="Телефонный номер",
    )
    geolocation = models.CharField(
        max_length=40,
        blank=False,
        null=False,
        verbose_name="Местоположение на английском в формате (Kazakhstan, Almaty)",
    )
    # Skills
    accounting = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Accounting Skill From 0 To 100"
    )
    writing = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Writing Skill From 0 To 100"
    )
    speaking = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Speaking Skill From 0 To 100"
    )
    reading = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Reading Skill From 0 To 100"
    )
    about_ru = models.TextField(
        max_length=1500,
        null=False,
        blank=False,
        verbose_name="About text Russian"
    )
    about_en = models.TextField(
        max_length=1500,
        null=False,
        blank=False,
        verbose_name="About text English"
    )
    profile_image = models.ImageField(
        upload_to='teacher_images/',
        verbose_name="Profile Teacher Image",
        null=True,
        blank=True
    )

    certificate = models.FileField(
        upload_to='teacher_certificates/',
        verbose_name="Certificate",
        null=True,
        blank=True,
    )
    is_approved = models.BooleanField(
        null=False,
        blank=False,
        verbose_name="Is Teacher Approved",
        default=False,
    )
    request_code = models.CharField(
        null=False,
        blank=False,
        verbose_name="Request Code",
        max_length=6,
    )

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validations are run on save

        # Сохраняем модель в первый раз, чтобы получить путь к файлу (если новая)
        super().save(*args, **kwargs)

        if self.profile_image:
            # Обрезаем и создаем новое изображение
            cropped_image = self.generate_image_version(self.profile_image, 1, 'cropped_profile_image.jpg')

            # Перезаписываем поле изображения
            self.profile_image.save('cropped_profile_image.jpg', cropped_image, save=False)

            # Сохраняем второй раз с новым изображением
            super().save(update_fields=['profile_image'])

    def crop_center(self, img, aspect_ratio):
        # Получаем текущие размеры изображения
        width, height = img.size

        # Рассчитываем новое соотношение сторон
        new_width = height * aspect_ratio
        new_height = width / aspect_ratio

        # Проверяем, что обрезать: по ширине или по высоте
        if new_width < width:
            # Обрезаем по ширине
            left = (width - new_width) / 2
            right = (width + new_width) / 2
            top = 0
            bottom = height
        else:
            # Обрезаем по высоте
            top = (height - new_height) / 2
            bottom = (height + new_height) / 2
            left = 0
            right = width

        # Обрезаем изображение по новым координатам
        img = img.crop((left, top, right, bottom))

        return img

    def generate_image_version(self, image_field, aspect_ratio, filename):
        img = Image.open(image_field)

        # Oбрезаем изображение до нужного соотношения сторон
        img = self.crop_center(img, aspect_ratio)

        # Convert 'P' (palette) or 'RGBA' mode images to 'RGB' for JPEG compatibility
        if img.mode in ('P', 'RGBA'):
            img = img.convert('RGB')

        # Сохраняем обработанное изображение в BytesIO объект
        img_io = BytesIO()
        img.save(img_io, format='JPEG')

        # Используем ContentFile для сохранения изображения в поле ImageField
        img_content = ContentFile(img_io.getvalue(), filename)
        return img_content

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ['fullname']
