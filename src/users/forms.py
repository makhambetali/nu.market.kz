from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class NewUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'main-input', }))
    email = forms.CharField(label='Адрес эл. почты', widget=forms.EmailInput(
        attrs={'class': 'main-input', }))
    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(
        attrs={'class': 'main-input'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(
        attrs={'class': 'main-input'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        # fields = ('username')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomAuthForm(AuthenticationForm, forms.Form):
    username = UsernameField(widget=forms.TextInput(
        attrs={"autofocus": True, 'class': 'main-input'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': 'main-input'}),
    )
