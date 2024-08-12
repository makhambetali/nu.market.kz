from django.contrib import admin
from django.urls import path
from users import views
from django.contrib.auth.views import logout_then_login
from users.forms import CustomAuthForm
app_name = 'users'
urlpatterns = [
    path('registerPage/', views.register_request, name='register'),
    path('login/', views.CustomLoginView.as_view(template_name='users/login.html',
         extra_context={'next': '/supply/'}, form_class=CustomAuthForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]
