from lib2to3.fixes.fix_input import context

from django.views.generic import TemplateView, ListView

from webapp.models import Course


class IndexView(ListView):
    template_name = 'index.html'

    context_object_name = 'courses'
    model = Course
    ordering = ['-created_at']

    paginate_by = 6
    paginate_orphans = 1