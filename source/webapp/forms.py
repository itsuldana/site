from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

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
    content = forms.CharField(label="Content", widget=CKEditorUploadingWidget())

    class Meta:
        model = Lesson
        fields = ['title', 'small_description','content', 'video_url']

