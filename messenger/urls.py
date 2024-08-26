from django.urls import path
from messenger.views import private_chat, chat_page
from django.conf import settings
from django.conf.urls.static import static
app_name = "messenger"
urlpatterns = [
    path("chat/private/<int:user1>_<int:user2>",private_chat, name="private-chat"),
    path('chat/',chat_page, name="chat-page" )
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
