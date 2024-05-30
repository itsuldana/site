from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class CoursesView(TemplateView):
    template_name = 'courses.html'

class CourseView(TemplateView):
    template_name = 'course.html'