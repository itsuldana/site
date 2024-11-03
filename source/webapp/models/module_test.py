from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from django.conf import settings
from django.contrib.postgres.fields import ArrayField 

from .course import Course
from .managers import Test_Manager


class TestCaseDescriptions(models.Model):
    сourse = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='test_case_descriptions',
        verbose_name='Тестовый модуль'
    )
    title = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="Name",
        default="Default Title"
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
        return f'TestModule for {self.title}'
    

class TestModule(models.Model):
    cours = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='test_modules',
        verbose_name='Тестовый модуль'
    )
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Name",
        default="New titile"
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
    position = models.PositiveIntegerField(default=1) 
    time_limit = models.PositiveIntegerField(
        default=30,  
        verbose_name='Лимит времени (минуты)'
    )
    def __str__(self):
        return f'{self.title} module for {self.cours.title}'


class Test(models.Model):
    objects = Test_Manager()

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
    answer_text = CKEditor5Field(
        'Ответ',
        config_name='extends',
        blank=False,
        null=False
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name="Правильный ответ"
    )

    def __str__(self):
        return f'Ответ: {self.answer_text} ({"Правильный" if self.is_correct else "Неправильный"})'
    

class TestHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='test_histories', 
        verbose_name='Пользователь'
    )
    test_module = models.ForeignKey(
        TestModule,
        on_delete=models.CASCADE,
        related_name='history',
    )
    test = models.ForeignKey(
        'webapp.Test', 
        on_delete=models.CASCADE, 
        related_name='test_histories', 
        verbose_name='Тест'
    )
    
    # Список ID правильных ответов
    correct_answer_ids = ArrayField(models.IntegerField(), blank=True, verbose_name='ID правильных ответов')

    # Список ID ответов, выбранных пользователем
    user_answer_ids = ArrayField(models.IntegerField(), blank=True, verbose_name='ID ответов пользователя')

    # Поле для хранения времени прохождения теста
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата завершения')

    def __str__(self):
        return f'Тест {self.test.id} - Пользователь {self.user.username}'
    
    def create_history(self, user, test_id, correct_answer_ids, selected_option_id, test_module):
        test_history = TestHistory.objects.filter(user=user, test_id=test_id)
        if not test_history.exists():
            TestHistory.objects.create(
                user=user,
                test_id=test_id,
                test_module=test_module,
                correct_answer_ids=correct_answer_ids,
                user_answer_ids=[int(i)for i in selected_option_id],
            )
        else:
            test_history.update(
                user=user,
                test_id=test_id,
                correct_answer_ids=correct_answer_ids,
                user_answer_ids=[int(i) for i in selected_option_id],
            )

    class Meta:
        verbose_name = 'История прохождения теста'
        verbose_name_plural = 'Истории прохождения тестов'
