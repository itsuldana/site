from django.contrib import messages
from django.core.cache import cache
from collections import defaultdict
from webapp.utils import generate_certificate

from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from webapp import models


class TestCaseDescriptionDetailView(View):
    def get(self, request, *args, **kwargs):
        cours_id = self.kwargs.get('course_id')
        # Get the TestCaseDescriptions instance based on course_id
        test_case_description = get_object_or_404(models.TestCaseDescriptions, сourse_id=cours_id)
        
        context = {
            "test_case_description": test_case_description
        }
        return render(request, "module_test/test_case_description_detail.html", context)


class TestModulesList(View):
    model = models.TestModule
    template_name = 'module_test/models.html'

    def get(self, request, *args, **kwargs):
        cours_id = self.kwargs.get('cours')
        user = request.user

        test_modules = self.model.objects.filter(cours__id=cours_id).order_by('position')

        user_module_data = []

        previous_completed = True  # флаг для блокировки следующих

        for module in test_modules:
            histories = models.TestHistory.objects.filter(user=user, test_module=module)
            total_questions = models.Test.objects.filter(test_module=module).count()
            correct_answers = 0

            for h in histories:
                correct_answers += sum(1 for a in h.user_answer_ids if a in h.correct_answer_ids)

            is_completed = correct_answers == total_questions and total_questions > 0

            user_module_data.append({
                'module': module,
                'total_questions': total_questions,
                'correct_answers': correct_answers,
                'is_completed': is_completed,
                'can_start': previous_completed,
            })

            # Обновляем флаг: если текущий не пройден, дальше блокируем
            previous_completed = is_completed

        context = {'user_module_data': user_module_data}
        return render(request, self.template_name, context)


class TestDetailView(View):
    model = models.Test
    template_name = 'module_test/test_view.html'
    
    def get(self, request, *args, **kwargs):
        test_id = self.kwargs.get("test_id")
        question, answer_options = self.model.objects.get_test_with_answers(test_id=test_id)
        duration = cache.ttl(request.user.id)

        context = {
            "question": question,
            "answer_options": answer_options,
            "duration": duration
            }
        return render(request, self.template_name, context)


class StartTestView(View):
    model = models.Test

    def get(self, request, *args, **kwargs):
        test_module_id = self.kwargs.get("module_id")
        test_ids = self.model.objects.get_all_tests(module_id=test_module_id)
        test_id = test_ids.pop()
        test_module = models.TestModule.objects.get(id=test_module_id)
        timeout = test_module.time_limit * 60
        cache.set(request.user.id, test_ids, timeout=timeout)

        if models.TestHistory.objects.filter(test_module=test_module, user=request.user).exists():
            models.TestHistory.objects.filter(test_module=test_module, user=request.user).update(user_answer_ids=[])
        return redirect('test_detail', test_id=test_id.id)


class NextTestView(View):
    model = models.Test

    def get(self, request, *args, **kwargs):
        test_ids = cache.get(request.user.id)
        test_id = test_ids.pop()
        timeout = cache.ttl(request.user.id)
        cache.set(request.user.id, test_ids, timeout=timeout)

        if test_id:
            return redirect('test_detail', test_id=test_id.id)

        redirect('test_detail', test_id=test_id.id)
    
    def post(self, request, *args, **kwargs):
        test_id = self.kwargs.get('test_id')
        selected_option_id = request.POST.getlist('selected_options')
        correct_answer_ids = self.model.objects.get_correct_answer_ids(test_id=test_id)
        test_module = models.Test.objects.get(id=test_id).test_module
        models.TestHistory().create_history(
            user=request.user,
            test_id=test_id,
            test_module=test_module,
            correct_answer_ids=correct_answer_ids,
            selected_option_id=selected_option_id
        )

        # ✅ Проверка: все тесты пройдены
        if not cache.get(request.user.id):
            course = test_module.cours
            user = request.user

            # Все вопросы в курсе
            total_questions = models.Test.objects.filter(test_module__cours=course).count()

            # Все истории пользователя по курсу
            user_histories = models.TestHistory.objects.filter(
                user=user,
                test_module__cours=course
            )

            # Считаем все правильные ответы
            correct_answers = 0
            for history in user_histories:
                correct_answers += sum(1 for a in history.user_answer_ids if a in history.correct_answer_ids)

            if total_questions > 0:
                percentage = (correct_answers / total_questions) * 100
            else:
                percentage = 0

            # Если больше 80%, ставим сертификат
            if percentage >= 80:
                purchase = models.Purchase.objects.filter(
                    user=user,
                    course=course,
                    payment_status='DONE'
                ).first()

                if purchase and not purchase.has_certificate:
                    purchase.has_certificate = True

                    # Сгенерировать сертификат
                    certificate_path = generate_certificate(purchase)
                    purchase.certificate_file.name = certificate_path

                    purchase.save()

                    messages.success(request,
                                     "Поздравляем! Вы набрали более 80% по курсу — сертификат доступен в профиле.")

            return redirect('result', test_id=test_id)
        
        return redirect('next_test', test_id=test_id)
        

class ResultView(View):
    def get(self, request, *args, **kwargs):
        test_id = self.kwargs.get('test_id')
        module = models.Test.objects.get(id=test_id).test_module

        # Получаем историю тестов для пользователя
        test_histories = models.TestHistory.objects.filter(user=request.user, test_module=module)

        # Подсчитываем количество правильных ответов и общую информацию
        total_tests = test_histories.count()
        correct_answers = sum(
            1 for history in test_histories if set(history.correct_answer_ids) == set(history.user_answer_ids)
        )
        # Подготовка данных для отображения
        context = {
            "module": module,
            "module_id": module.id,
            'total_tests': total_tests,
            'correct_answers': correct_answers,
        }

        return render(request, 'module_test/results.html', context)
    

class TestModuleResultView(View):
    def get(self, request, module_id, *args, **kwargs):
        # Получаем модуль тестов по ID
        module = get_object_or_404(models.TestModule, id=module_id)
        
        # Получаем историю тестов пользователя для данного модуля
        test_histories = models.TestHistory.objects.filter(user=request.user, test_module=module)

        # Сохраняем информацию о тестах и ответах
        tests_data = []
        for history in test_histories:
            test = history.test
            user_answer_ids = set(history.user_answer_ids)
            correct_answer_ids = set(history.correct_answer_ids)

            # Сохраняем статус каждого варианта ответа (правильный/неправильный)
            answers = []
            for answer in test.answer_options.all():
                is_user_answer = answer.id in user_answer_ids
                is_correct_answer = answer.id in correct_answer_ids
                answers.append({
                    'text': answer.answer_text,
                    'is_user_answer': is_user_answer,
                    'is_correct_answer': is_correct_answer,
                })

            tests_data.append({
                'test': test,
                'answers': answers
            })

        # Контекст для отображения в шаблоне
        context = {
            'module': module,
            'tests_data': tests_data,
        }
        return render(request, 'module_test/module_results.html', context)
    

class DashboardView(View):
    template_name = 'module_test/dashboard.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        cours_id = self.kwargs.get('cours_id')
        test_histories = models.TestHistory.objects.filter(user=user, test_module__cours_id=cours_id)

        total_tests = test_histories.count()
        correct_answers_total = 0
        incorrect_answers_total = 0

        module_stats = {}

        for history in test_histories:
            correct_answers = sum(1 for answer in history.user_answer_ids if answer in history.correct_answer_ids)
            total_questions = len(history.user_answer_ids)

            correct_answers_total += correct_answers
            incorrect_answers_total += (total_questions - correct_answers)

            module_id = history.test_module.id
            if module_id not in module_stats:
                module_stats[module_id] = {
                    'module_title': history.test_module.title,
                    'correct_answers': 0,
                    'incorrect_answers': 0,
                }

            module_stats[module_id]['correct_answers'] += correct_answers
            module_stats[module_id]['incorrect_answers'] += (total_questions - correct_answers)

        # 🔥 Получаем общее количество вопросов в курсе (по всем модулям)
        total_questions_in_course = models.Test.objects.filter(
            test_module__cours_id=cours_id
        ).count()

        # 🧮 Подсчет процента
        if total_questions_in_course > 0:
            correct_percentage = (correct_answers_total / total_questions_in_course) * 100
            correct_percentage = round(correct_percentage, 2)
        else:
            correct_percentage = 0.0

        # 🎯 Сколько осталось до 80%
        remaining_to_cert = max(0, round(80 - correct_percentage, 2))

        context = {
            'total_tests': total_tests,
            'correct_answers_total': correct_answers_total,
            'incorrect_answers_total': incorrect_answers_total,
            'module_stats': module_stats,
            'cours_id': cours_id,
            'total_questions_in_course': total_questions_in_course,
            'correct_percentage': correct_percentage,
            'remaining_to_cert': remaining_to_cert,
        }

        return render(request, self.template_name, context)