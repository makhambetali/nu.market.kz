from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message

users = []
@login_required
def private_chat(request, user1 = 0, user2 = 0):
    room = f"{user1}-{user2}" if user1 < user2 else f"{user2}-{user1}"
    global users
    if str(request.user.username) in room and (user1 != user2):
        messages = Message.objects.filter(room=room).order_by('timestamp')[:50]
        receiver = User.objects.get(username=user2)
        if len(users) == 0:
            users = User.objects.exclude(username=request.user.username)
        
        context = {
            "user_messages": messages,
            "room": room,
            "receiver": receiver,
            "users": users,
        }
        return render(request, "messenger/chat/chat.html", context)
    else:
        return render(request, "messenger/chat/noAccess.html")

@login_required
def chat_page(request):
    global users
    users = User.objects.exclude(username=request.user.username)
        
    context = {
            
            "users": users,
        }
    return render(request, "messenger/chat/chat.html", context)