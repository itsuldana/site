from django import forms

from accounts.models import CustomUser
# from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Course, Module
from .models.lessons import Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'image', 'tag', 'is_active']


class CourseModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'position']


class LessonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["content"].required = False
        self.fields['creator'].queryset = CustomUser.objects.filter(is_superuser=True)

    class Meta:
        model = Lesson
        fields = ['title', 'small_description','content', 'video_url', 'creator']

