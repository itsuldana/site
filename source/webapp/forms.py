from django import forms

from accounts.models import CustomUser
# from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Course, Module, AnswerOption
from .models.lessons import Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'preview_description', 'price', 'image', 'tag', 'is_active']


class CourseModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'position', 'is_active']


class LessonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["content"].required = False

    class Meta:
        model = Lesson
        fields = ['title', 'small_description','content', 'video_url', 'is_active']


class TestForm(forms.Form):
    correct_answers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)


class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ['answer_text', 'is_correct']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    number = forms.CharField(max_length=15, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
