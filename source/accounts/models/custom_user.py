from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import os
from .level import LevelSetting


class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    social_network_link = models.URLField(null=True, blank=True)

    xp = models.PositiveIntegerField(default=0, verbose_name="Опыт")
    level = models.PositiveIntegerField(default=1, verbose_name="Уровень")

    quiz_completed = models.BooleanField(default=False)
    recommended_tags = models.ManyToManyField('webapp.Tag', blank=True, related_name='recommended_users')

    def save(self, *args, **kwargs):
        try:
            old_user = CustomUser.objects.get(pk=self.pk)
            if old_user.avatar and old_user.avatar != self.avatar:
                if os.path.isfile(old_user.avatar.path):
                    os.remove(old_user.avatar.path)
        except CustomUser.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def get_xp_for_next_level(self):
        """Получает, сколько опыта нужно для следующего уровня"""
        try:
            next_level = self.level + 1
            setting = LevelSetting.objects.get(level=next_level)
            return setting.xp_required
        except ObjectDoesNotExist:
            return None  # Если уровень не настроен, вернется None

    def add_experience(self, course_id: int, lesson_id: int, xp_amount: int):
        """Добавляет опыт, проверяет завершение модуля/курса и повышает уровень."""
        from webapp.models import Lesson, LessonProgress

        self.xp += xp_amount
        level_up_messages = []

        # Проверка завершения модуля
        lesson = Lesson.objects.get(id=lesson_id)
        module = lesson.module
        course = module.course

        completed_lessons_in_module = LessonProgress.objects.filter(
            user=self, lesson__module=module, status="done"
        ).count()
        total_lessons_in_module = module.lessons.count()

        if completed_lessons_in_module == total_lessons_in_module:
            self.xp += 50
            level_up_messages.append(f"🎉 Вы завершили модуль '{module.title}' и получили +50 XP!")

        # Проверка завершения курса
        completed_lessons_in_course = LessonProgress.objects.filter(
            user=self, lesson__module__course=course, status="done"
        ).count()
        total_lessons_in_course = Lesson.objects.filter(module__course=course).count()

        if completed_lessons_in_course == total_lessons_in_course:
            self.xp += 100
            level_up_messages.append(f"🎉 Вы завершили курс '{course.title}' и получили +100 XP!")

        # Проверка на повышение уровня
        while True:
            xp_needed = self.get_xp_for_next_level()
            if xp_needed is None or self.level >= 25:
                break  # Если уровни не настроены или достигнут максимум, выходим

            if self.xp >= xp_needed:
                self.xp -= xp_needed
                self.level += 1
                level_up_messages.append(f"🎉 Поздравляем! Ваш уровень повышен до {self.level}!")
            else:
                break  # Если опыта не хватает, останавливаемся

        self.save()
        xp_left = self.get_xp_for_next_level() - self.xp if self.get_xp_for_next_level() else 0

        return "\n".join(level_up_messages) if level_up_messages else f"Вам осталось {xp_left} опыта до следующего уровня."

    def get_user_discount(self):
        discount_levels = {
            (5, 9): 2,
            (10, 14): 4,
            (15, 19): 6,
            (20, 25): 8,
        }

        discount = next((d for (low, high), d in discount_levels.items() if low <= self.level <= high), 0)

        return discount

    def get_level_color(self):
        """Возвращает цвет градиента в зависимости от уровня пользователя"""
        level_colors = {
            1: "#B0BEC5, #78909C",  # Серый
            2: "#CFD8DC, #90A4AE",  # Светло-серый
            3: "#ECEFF1, #B0BEC5",  # Серебристый
            4: "#FFECB3, #FFD54F",  # Желтоватый
            5: "#64DD17, #1B5E20",  # Зеленый
            6: "#AEEA00, #76FF03",  # Лаймовый
            7: "#00E676, #00C853",  # Изумрудный
            8: "#1DE9B6, #00BFA5",  # Бирюзовый
            9: "#00E5FF, #00B8D4",  # Голубой
            10: "#2979FF, #0D47A1",  # Синий
            11: "#304FFE, #1A237E",  # Индиго
            12: "#3D5AFE, #283593",  # Темно-синий
            13: "#6200EA, #311B92",  # Фиолетовый
            14: "#AA00FF, #6200EA",  # Пурпурный
            15: "#D500F9, #9C27B0",  # Розовато-фиолетовый
            16: "#F50057, #C51162",  # Розовый
            17: "#FF1744, #D50000",  # Красный
            18: "#FF6F00, #E65100",  # Оранжевый
            19: "#FF9100, #FF6D00",  # Янтарный
            20: "#FFC400, #FFAB00",  # Золотистый
            21: "#FFD600, #FFEA00",  # Желтый
            22: "#AEEA00, #76FF03",  # Лайм (повтор, но ярче)
            23: "#64DD17, #1B5E20",  # Глубокий зеленый
            24: "#00C853, #009624",  # Темно-зеленый
            25: "#00E676, #00C853",  # Ультра-яркий зеленый (топовый)
        }

        return level_colors.get(self.level, "#FF9800, #FF5722")  # Оранжевый по умолчанию
