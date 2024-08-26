
from django.contrib import admin
from django.urls import path, include
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('messenger/', include('messenger.urls')),
    path('accounts/', include('users.urls')),
]
