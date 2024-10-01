from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

input_style = 'ring-yellow mb-4 rounded-xl p-4 ring-1 ring-inset border-0'

class NewUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': input_style, }))
    email = forms.CharField(label='Адрес эл. почты', widget=forms.EmailInput(
        attrs={'class': input_style, }))
    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(
        attrs={'class': input_style}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(
        attrs={'class': input_style}))

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
        attrs={"autofocus": True, 'class': input_style}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': input_style}),
    )
