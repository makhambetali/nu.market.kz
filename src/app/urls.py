from django.contrib import admin
from django.urls import path, include, re_path
# from app import views as app_views
from .views import * 
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


app_name = 'app'
urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('filter/', FilterHomePage.as_view(), name='home-page-filter'),
    path('create-post/', CreatePost.as_view(), name='post-page'),
    path('edit-post/<slug:slug>', EditPost.as_view(), name='edit-post'),
    path('delete-post/<slug:slug>', DeletePost.as_view(), name='delete-post'),
    path('liked/', FavPostsPageView.as_view(), name='liked-page'),
    path('my_posts/', MyPostsPageView.as_view(), name='my-posts'),
    path('details/<slug:slug>', DetailPageView.as_view(), name='details-page'),
    path('fav_posts/add/<slug:slug>', addToFav, name='fav-add'),
    path('fav_posts/delete/<slug:slug>', deleteFromFav, name='fav-delete'),
] + static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
