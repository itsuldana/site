from django.db import models


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
        question_text = {
            "question_text":results[0].question_text,
            "question_id": results[0].id
            }

        # Извлекаем варианты ответов
        answer_options = [
            {"answer_option_id": result.answer_option_id, "answer_text": result.answer_text, "is_correct": result.is_correct}
            for result in results if result.answer_option_id is not None
        ]

        return question_text, answer_options

    def get_correct_answer_ids(self, test_id) -> list:
        # Запрос на получение id всех правильных ответов для конкретного теста
        query = """
            SELECT ao.id
            FROM webapp_answeroption ao
            WHERE ao.test_id = %s AND ao.is_correct = TRUE
        """
        # Выполняем запрос и возвращаем список id правильных ответов
        correct_answers = self.raw(query, [test_id])
        return [answer.id for answer in correct_answers]
