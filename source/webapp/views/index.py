from django.utils import translation
from django.views.generic import  ListView

from accounts.models import Teacher
from blog.models import Post
from webapp.models import Course


class IndexView(ListView):
    template_name = 'index.html'

    context_object_name = 'courses'
    model = Course
    ordering = ['-created_at']

    paginate_by = 6
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teachers = Teacher.objects.all()

        context['teachers'] = teachers
        context['posts'] = Post.objects.all().order_by('-created_at').exclude(is_active=False)
        context['current_lang'] = translation.get_language()

        return context