from django.db import models


class LevelSetting(models.Model):
    level = models.PositiveIntegerField(
        unique=True,
        verbose_name="Уровень",
        null=False,
        blank=False,
    )
    xp_required = models.PositiveIntegerField(
        verbose_name="Опыт для достижения",
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ["level"]
        verbose_name = "Level"
        verbose_name_plural = "Level settings"

    def __str__(self):
        return f"Level {self.level}: {self.xp_required} XP"
