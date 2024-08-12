
from django.contrib import admin
from django.urls import path, include
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('accounts/', include('users.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
