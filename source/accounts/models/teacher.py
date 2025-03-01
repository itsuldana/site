from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
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

    def clean(self):
        # Validate profile image
        if self.profile_image:
            image = Image.open(self.profile_image)
            width, height = image.size

            # Check aspect ratio
            aspect_ratio = width / height
            if not (round(aspect_ratio, 2) == 1.26):  # For 1.36 aspect ratio
                raise ValidationError("The image aspect ratio must be 1:1.26.")

            # Check minimum width
            if width < 360:
                raise ValidationError("The image width must be at least 360 pixels.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validations are run on save
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"
        ordering = ['fullname']
