from django.contrib.auth.models import AbstractUser
from django.db import models
import os


class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    social_network_link = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            old_user = CustomUser.objects.get(pk=self.pk)
            if old_user.avatar and old_user.avatar != self.avatar:
                if os.path.isfile(old_user.avatar.path):
                    os.remove(old_user.avatar.path)
        except CustomUser.DoesNotExist:
            pass
        super().save(*args, **kwargs)
