from django.contrib import admin
from django.urls import path
from app import views as app_views
app_name = 'app'
urlpatterns = [
    path('', app_views.HomePageView.as_view(), name='home-page'),
    path('create-post/', app_views.CreatePost.as_view(), name='create-post'),
    path('edit-post/<int:pk>', app_views.EditPost.as_view(), name='edit-post'),
]
