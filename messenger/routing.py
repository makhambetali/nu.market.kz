from django.urls import path
from messenger.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
]
0