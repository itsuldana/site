from django.core.cache import cache

from django.views.generic import FormView
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from webapp import models
from webapp import forms


class TestModulesList(View):
    model = models.TestModule
    template_name = 'module_test/models.html'

    def get(self, request, *args, **kwargs):
        cours_id = self.kwargs.get('cours')
        test_modules = self.model.objects.filter(cours__id=cours_id)
        print(f"{test_modules=}")
        print(test_modules)

        context = {'test_modules': test_modules}
        return render(request, self.template_name, context)


class TestDetailView(View):
    model = models.Test
    template_name = 'module_test/test_view.html'
    
    def get(self, request, *args, **kwargs):
        test_id = self.kwargs.get("test_id")
        question, answer_options = self.model.objects.get_test_with_answers(test_id=test_id)

        context = {
            "question": question,
            "answer_options": answer_options,
            }
        return render(request, self.template_name, context)


class StartTestView(View):
    model = models.Test

    def get(self, request, *args, **kwargs):
        test_module_id = self.kwargs.get("module_id")
        test_ids = self.model.objects.get_all_tests(module_id=test_module_id)
        test_id = test_ids.pop()
        cache.set(request.user.id, test_ids, timeout=3000)
        return redirect('test_detail', test_id=test_id.id)


class NextTestView(View):
    model = models.Test

    def get(self, request, *args, **kwargs):
        test_ids = cache.get(request.user.id)
        test_id = test_ids.pop()
        cache.set(request.user.id, test_ids, timeout=3000)

        if test_id:
            return redirect('test_detail', test_id=test_id.id)

        redirect('test_detail', test_id=test_id.id)
    
    def post(self, request, *args, **kwargs):
        test_id = self.kwargs.get('test_id')
        selected_option_id = request.POST.get('selected_option')

        correct_answer_ids = self.model.objects.get_correct_answer_ids(test_id=test_id)
        models.TestHistory().create_history(
            user=request.user,
            test_id=test_id,
            correct_answer_ids=correct_answer_ids,
            selected_option_id=selected_option_id
        )
        if not cache.get(request.user.id):
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