from django.contrib import admin
from django.urls import path, include, re_path
from app import views as app_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
app_name = 'app'
urlpatterns = [
    path('', app_views.HomePageView.as_view(), name='home-page'),
    path('edit-post/<int:pk>', app_views.EditPost.as_view(), name='edit-post'),
    path('post/', app_views.CreatePost.as_view(), name='post-page'),
    path('profile/', app_views.ProfilePageView.as_view(), name='profile-page'),
    path('liked/', app_views.FavPostsPageView.as_view(), name='liked-page'),
    path('details/<int:pk>', app_views.DetailPageView.as_view(), name='details-page'),
    path('load-posts/', app_views.load_posts, name='load_posts'),
    path('fav_posts/add/<int:pk>', app_views.addToFav, name='fav-add'),
    path('fav_posts/delete/<int:pk>', app_views.deleteFromFav, name='fav-delete'),
    path('total/', app_views.delete, name='delete-total'),
    path('update_user_data/', app_views.update_user_data, name='update-user-data')
] + static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
# TemplateView.as_view(template_name = 'dist/profile.html')