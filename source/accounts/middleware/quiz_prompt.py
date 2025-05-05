class QuizPromptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверка: только для главной страницы "/"
        if request.path == '/' and request.user.is_authenticated and not getattr(request.user, 'quiz_completed', False):
            request.show_quiz_modal = True
        else:
            request.show_quiz_modal = False

        return self.get_response(request)