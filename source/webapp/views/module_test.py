from django.core.cache import cache

from django.views.generic import FormView
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from webapp.models import TestModule, Test
from webapp import forms


class TestModulesList(View):
    model = TestModule
    template_name = 'module_test/models.html'

    def get(self, request, *args, **kwargs):
        cours_id = self.kwargs.get('cours')
        test_modules = self.model.objects.filter(cours__id=cours_id)
        print(f"{test_modules=}")
        print(test_modules)

        context = {'test_modules': test_modules}
        return render(request, self.template_name, context)


class StartTestView(View):
    model = Test
    def get(self, request, *args, **kwargs):
        test_module_id = self.kwargs.get("module_id")
        test_ids = Test.objects.get_all_tests(module_id=test_module_id)
        test_id = test_ids.pop()
        cache.set(request.user.id, test_ids, timeout=3000)
        return redirect('test_detail', test_id=test_id.id)


class TestDetailView(View):
    model = Test
    template_name = 'module_test/test_view.html'
    
    def get(self, request, *args, **kwargs):
        test_id = self.kwargs.get("test_id")
        question, answer_options = self.model.objects.get_test_with_answers(test_id=test_id)

        context = {
            "question": question,
            "answer_options": answer_options,
            }
        return render(request, self.template_name, context)


class TestSubmitView(FormView):
    template_name = 'module_test/results.html'
    form_class = forms.TestForm  # Используем нашу форму

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Заполняем поле правильных ответов значениями из базы данных
        test_module_id = self.kwargs['test_module_id']
        test_module = get_object_or_404(TestModule, id=test_module_id)
        tests = test_module.tests.all()
        options = []

        for test in tests:
            for option in test.answer_options.all():
                options.append((option.id, option.answer_text))

        form.fields['correct_answers'].choices = options
        return form

    def form_valid(self, form):
        test_module_id = self.kwargs['test_module_id']
        test_module = get_object_or_404(TestModule, id=test_module_id)
        tests = test_module.tests.all()

        # Получаем список выбранных ответов
        selected_answers = form.cleaned_data['correct_answers']
        score = 0

        # Подсчет правильных ответов
        for test in tests:
            correct_answers = set()  # Набор для хранения правильных ответов
            for option in test.answer_options.all():
                if option.is_correct:
                    correct_answers.add(str(option.id))  # Добавляем правильный ответ

            # Проверяем, совпадают ли выбранные ответы с правильными
            if correct_answers == set(selected_answers):
                score += 1  # Увеличиваем счет, если все правильные ответы выбраны

        # Возвращаем результат на страницу с результатами
        return render(self.request, self.template_name, {'score': score, 'total': len(tests)})


    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

