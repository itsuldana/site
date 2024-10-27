from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from .module import Module


class TestModule(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='test_modules',
        verbose_name='Тестовый модуль'
    )
    description = CKEditor5Field(
        'Описание',
        config_name='extends',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f'TestModule for {self.module.title}'


class Test(models.Model):
    test_module = models.ForeignKey(
        TestModule,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name='Тестовый модуль'
    )
    question_text = CKEditor5Field(
        'Вопрос',
        config_name='extends',
        blank=False,
        null=False
    )

    def __str__(self):
        return f'Вопрос: {self.question_text}'


class AnswerOption(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='answer_options',
        verbose_name='Тест'
    )
    answer_text = models.CharField(
        max_length=255,
        verbose_name="Текст ответа"
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name="Правильный ответ"
    )

    def __str__(self):
        return f'Ответ: {self.answer_text} ({"Правильный" if self.is_correct else "Неправильный"})'
