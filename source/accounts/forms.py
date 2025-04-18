from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

from accounts.models import Teacher


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password_confirm = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirm')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Введите правильный адрес электронной почты.')

        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # Использует встроенные Django валидаторы для проверки сложности пароля
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email_confirmed = False
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'avatar')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if self.cleaned_data.get('avatar'):
                self.crop_avatar(user)
        return user

    def crop_avatar(self, user):
        from PIL import Image
        img = Image.open(user.avatar.path)
        width, height = img.size
        min_side = min(width, height)
        left = (width - min_side) / 2
        top = (height - min_side) / 2
        right = (width + min_side) / 2
        bottom = (height + min_side) / 2
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save(user.avatar.path)


class EmailChangeForm(forms.Form):
    new_email = forms.EmailField(label='New Email', required=True)


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']


class TeacherApplicationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'certificate', 'fullname', 'position', 'instagram', 'facebook', 'linkedin', 'twitter',
            'phone_number', 'geolocation', 'accounting', 'writing', 'speaking', 'reading',
            'about_ru', 'about_en', 'profile_image'
        ]
        widgets = {
            'certificate': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certificate'
            }),
            'fullname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specialization'
            }),
            'instagram': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instagram Profile URL'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Facebook Profile URL'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'LinkedIn Profile URL'
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Twitter Profile URL'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'geolocation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location (e.g. Kazakhstan, Almaty)'
            }),
            'accounting': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Accounting Skill (0-100)',
                'min': 0, 'max': 100
            }),
            'writing': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Writing Skill (0-100)',
                'min': 0, 'max': 100
            }),
            'speaking': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Speaking Skill (0-100)',
                'min': 0, 'max': 100
            }),
            'reading': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reading Skill (0-100)',
                'min': 0, 'max': 100
            }),
            'about_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'About (Russian)',
                'rows': 4
            }),
            'about_en': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'About (English)',
                'rows': 4
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'fullname', 'position', 'instagram', 'facebook', 'linkedin', 'twitter',
            'phone_number', 'geolocation', 'about_ru', 'about_en', 'profile_image'
        ]
        widgets = {
            'fullname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specialization'
            }),
            'instagram': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instagram Profile URL'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Facebook Profile URL'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'LinkedIn Profile URL'
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Twitter Profile URL'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'geolocation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location (e.g. Kazakhstan, Almaty)'
            }),
            'about_ru': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'About (Russian)',
                'rows': 4
            }),
            'about_en': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'About (English)',
                'rows': 4
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }