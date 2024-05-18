from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

from accounts.forms import CustomUserCreationForm, LoginForm, UserForm


# Create your views here.

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
        return redirect('index')


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

# class UserDetailView(DetailView):
#     template_name = 'user_detail.html'
#     model = get_user_model()
#     context_object_name = 'user_obj'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['favorite_photos'] = self.request.user.user_favorites.all()
#         return context
#
#
# class UserUpdateView(UpdateView):
#     template_name = 'user_update.html'
#     model = get_user_model()
#     form_class = UserForm
#
#     def get_success_url(self):
#         return reverse('user_detail', kwargs={'pk': self.object.pk})
