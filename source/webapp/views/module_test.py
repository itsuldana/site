from django.views.generic import DetailView, FormView
from django.shortcuts import get_object_or_404, render
from webapp.models import TestModule
from webapp import forms


class TestModuleDetailView(DetailView):
    model = TestModule
    template_name = 'module_test/test_view.html'
    context_object_name = 'test_module'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = self.object.tests.all()
        
        # Инициализируем форму
        form = forms.TestForm()

        # Получаем все тесты и их варианты ответов
        tests = self.object.tests.all()
        options = []

        for test in tests:
            for option in test.answer_options.all():
                options.append((option.id, option.answer_text))

        # Устанавливаем варианты для поля correct_answers
        form.fields['correct_answers'].choices = options
        context['form'] = form
        return context



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

