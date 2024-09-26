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
    path('edit-post/<slug:slug>', EditPost.as_view(), name='edit-post'),
    path('post/', CreatePost.as_view(), name='post-page'),
    path('profile/', ProfilePageView.as_view(), name='profile-page'),
    path('liked/', FavPostsPageView.as_view(), name='liked-page'),
    path('details/<slug:slug>', DetailPageView.as_view(), name='details-page'),
    path('fav_posts/add/<int:pk>', addToFav, name='fav-add'),
    path('fav_posts/delete/<int:pk>', deleteFromFav, name='fav-delete'),
    path('total/', delete, name='delete-total'),
    path('update_user_data/', update_user_data, name='update-user-data')
] + static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
# TemplateView.as_view(template_name = 'dist/profile.html')