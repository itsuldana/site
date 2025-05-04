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
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, FormView

from accounts.forms import (
    CustomUserCreationForm, LoginForm, UserForm, EmailChangeForm, CustomPasswordChangeForm,
)

from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Teacher
from webapp.models import Purchase


class LoginView(TemplateView):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            # Проверяем, является ли пользователь суперпользователем или подтвержден email
            if user:
                if not user.is_superuser and not user.email_confirmed:
                    form.add_error(None, _('Please confirm your email before logging in.'))
                else:
                    login(request, user)
                    next_url = request.GET.get('next')
                    return redirect(next_url or 'user_detail', pk=user.pk)
            else:
                form.add_error(None, _('Invalid username or password'))

        # Если форма не валидна или проверка не пройдена, вернуть форму с ошибками
        return self.render_to_response({'form': form})


class RegisterView(CreateView):
    template_name = 'registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('email_confirm')

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
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])


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

        context['is_teacher'] = self.object.user_teacher.exists()

        if context['is_teacher']:
            context['is_approved'] = Teacher.objects.get(user_id=self.object.pk).is_approved

            context['teacher_id'] = Teacher.objects.get(user=self.object).id

        user = self.object
        next_level_xp = user.get_xp_for_next_level()
        xp_needed = next_level_xp - user.xp
        progress_percentage = int((user.xp / next_level_xp) * 100 if next_level_xp > 0 else 0)

        discount = user.get_user_discount()

        certificates = Purchase.objects.filter(
            user=user,
            has_certificate=True,
            payment_status='DONE'
        ).select_related('course')

        context.update({
            'discount': discount,
            'user_xp': user.xp,
            'xp': xp_needed,
            'next_level_xp': next_level_xp,
            'progress_percentage': progress_percentage,
            "certificates": certificates,
        })

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
        mail_subject = 'Activate your new email address.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'new_email': urlsafe_base64_encode(force_bytes(new_email)),
        })
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [new_email])


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


class EmailConfirmView(TemplateView):
    template_name = 'email_confirm.html'
