from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .forms import NewUserForm
from django.contrib.auth.views import LoginView
from django.contrib import messages

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy

error_messages = {
}


@csrf_exempt
def register_request(request):
    error_messages = {}
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        for i in form.errors:
            error_messages[i] = form.errors[i]

    form = NewUserForm()
    return render(request, 'users/signup.html', {'form': form, 'error_messages': error_messages})


class CustomLoginView(LoginView):
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        return '/'


def logout_view(request):
    logout(request)
    return redirect('app:home-page')


class CustomPasswordResetView(PasswordResetView):
    # Укажите свой собственный шаблон
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    # Укажите свой собственный шаблон
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    # Укажите свой собственный шаблон
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    # Укажите свой собственный шаблон
    template_name = 'users/password_reset_complete.html'

    # password_reset_email.html
