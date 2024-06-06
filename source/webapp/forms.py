from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Course, Module
from .models.lessons import Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'image', 'tag']


class CourseModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'position']


class LessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False
