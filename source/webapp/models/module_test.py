from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from .course import Course

class Test_Manager(models.Manager):
    def get_all_tests(self, module_id):
        # Запрос на получение всех тестов для конкретного модуля
        query = """
            SELECT t.id
            FROM webapp_test t
            JOIN webapp_testmodule tm ON t.test_module_id = tm.id
            WHERE tm.id = %s
        """

        return list(self.raw(query, [module_id]))
    
    
    def get_test_with_answers(self, test_id) -> tuple:
        # Запрос на получение вопроса и его вариантов ответов для конкретного теста
        query = """
            SELECT 
                t.id,
                t.question_text, 
                ao.id AS answer_option_id, 
                ao.answer_text, 
                ao.is_correct
            FROM webapp_test t
            LEFT JOIN webapp_answeroption ao ON ao.test_id = t.id
            WHERE t.id = %s
        """
        results = list(self.raw(query, [test_id]))

        # Проверяем наличие результатов
        if not results:
            return None, []

        # Извлекаем текст вопроса
        question_text = results[0].question_text

        # Извлекаем варианты ответов
        answer_options = [
            {"answer_option_id": result.answer_option_id, "answer_text": result.answer_text, "is_correct": result.is_correct}
            for result in results if result.answer_option_id is not None
        ]

        return question_text, answer_options


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
        return f'TestModule for {self.сourse_id.title}'
    

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
