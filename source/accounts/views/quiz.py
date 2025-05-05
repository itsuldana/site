from collections import Counter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from accounts.models import QuizQuestion, CustomUser
from webapp.models import Tag


class QuizSubmitView(LoginRequiredMixin, FormView):
    template_name = 'base.html'  # модалка может быть в любом шаблоне
    success_url = '/courses/recommendations/'  # или reverse_lazy

    def dispatch(self, request, *args, **kwargs):
        if request.user.quiz_completed:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = QuizQuestion.objects.prefetch_related('options').all()
        return context

    def post(self, request, *args, **kwargs):
        tag_counter = Counter()

        for question in QuizQuestion.objects.all():
            tag_id = request.POST.get(f'question_{question.id}')
            if tag_id:
                tag_counter[tag_id] += 1

        top_tag_ids = [tag_id for tag_id, _ in tag_counter.most_common(3)]
        tags = Tag.objects.filter(id__in=top_tag_ids)

        user: CustomUser = request.user
        user.recommended_tags.set(tags)
        user.quiz_completed = True
        user.save()

        return redirect(self.get_success_url())
