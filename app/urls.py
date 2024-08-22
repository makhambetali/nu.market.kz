from django.contrib import admin
from django.urls import path
from app import views as app_views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'app'
urlpatterns = [
    path('', app_views.HomePageView.as_view(), name='home-page'),
    path('edit-post/<int:pk>', app_views.EditPost.as_view(), name='edit-post'),
    path('message/', app_views.MessagePage, name='message-page'),
    path('post/', app_views.CreatePost.as_view(), name='post-page'),
    path('profile/', app_views.ProfilePage, name='profile-page'),
    path('liked/', app_views.LikedPage, name='liked-page'),
    path('details/', app_views.DetailsPage, name='details-page'),
    path('load-posts/', app_views.load_posts, name='load_posts'),
] + static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)