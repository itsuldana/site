from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.utils.translation import activate as activate_translation
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, FormView, ListView

from accounts.forms import (
    CustomUserCreationForm, LoginForm, UserForm, EmailChangeForm, CustomPasswordChangeForm,
)
from webapp.models import Course, Module, Lesson, LessonProgress, Purchase
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('index')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return redirect('index')
        next = request.GET.get('next')
        login(request, user)
        if next:
            return redirect(next)
        return redirect('user_detail', pk=user.pk)


class RegisterView(CreateView):
    template_name = 'registration.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            self.send_confirmation_email(request, user)
            return redirect(self.success_url)
        context = {'form': form}
        return self.render_to_response(context)

    def send_confirmation_email(self, request, user):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = user.email
        send_mail(mail_subject, message, 'your_email@example.com', [to_email])


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'activation_invalid.html')


def logout_view(request):
    logout(request)
    return redirect('index')


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'user_detail.html'
    model = get_user_model()
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем оплаченные курсы пользователя
        context['paid_courses'] = Purchase.objects.filter(user=self.object, payment_status='DONE').select_related(
            'course')

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user_update.html'
    model = get_user_model()
    form_class = UserForm

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.object.pk})


class UserEmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'email_change.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['new_email']
        self.send_confirmation_email(user, new_email)
        return redirect('user_detail', pk=user.pk)

    def send_confirmation_email(self, user, new_email):
        current_site = get_current_site(self.request)
        mail_subject = 'Confirm your new email address.'
        message = render_to_string('email_change_confirm.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'new_email': urlsafe_base64_encode(force_bytes(new_email)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(mail_subject, message, 'your_email@example.com', [new_email])


def confirm_email_change(request, uidb64, token, new_email_encoded):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_email = force_str(urlsafe_base64_decode(new_email_encoded))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email = new_email
        user.save()
        return redirect('user_detail', pk=user.pk)
    else:
        return render(request, 'activation_invalid.html')


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('user_detail')

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})


def set_language(request):
    lang_code = request.GET.get('language', 'en')
    activate_translation(lang_code)
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response


class ManageCoursesView(UserPassesTestMixin, ListView):
    template_name = 'manage/manage_courses.html'

    context_object_name = 'courses'
    model = Course
    ordering = ['-created_at']

    def test_func(self):
        return self.request.user.is_superuser


class ManageModulesView(UserPassesTestMixin, ListView):
    template_name = 'manage/manage_modules.html'

    model = Module
    context_object_name = 'modules'

    def get_queryset(self):
        return Module.objects.filter(course_id=self.kwargs['pk']).order_by('position')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs['pk'])
        return context

    def test_func(self):
        return self.request.user.is_superuser


class ManageLessonsView(UserPassesTestMixin, ListView):
    template_name = 'manage/manage_lessons.html'

    model = Lesson
    context_object_name = 'lessons'

    def get_queryset(self):
        return Lesson.objects.filter(module_id=self.kwargs['pk']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = Module.objects.get(id=self.kwargs['pk'])
        user = self.request.user

        lessons = context['lessons']

        lessons_with_progress = []

        for lesson in lessons:
            lesson_progress = LessonProgress.objects.filter(lesson=lesson, user=user).first()
            lessons_with_progress.append({
                'lesson': lesson,
                'progress': lesson_progress.status if lesson_progress else ''
            })
        context['module'] = module
        context['lessons_with_progress'] = lessons_with_progress
        return context

    def test_func(self):
        return self.request.user.is_superuser
