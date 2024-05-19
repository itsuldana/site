from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Логин'
    )
    password = forms.CharField(
        required=True,
        label='Пароль',
        widget=forms.PasswordInput
    )


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, required=True,
                                       widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password_confirm', 'first_name', 'last_name', 'email')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.email_confirmed = False
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'avatar')

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
    old_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']
