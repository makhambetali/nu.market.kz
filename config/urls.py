
from django.contrib import admin
from django.urls import path, include
# from src.app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.app.urls')),
    path('users/', include('src.users.urls', namespace="users")),
    path('messenger/', include('src.messenger.urls')),
]
