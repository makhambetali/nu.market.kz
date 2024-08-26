from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from messenger.models import Message

@login_required
def private_chat(request, user1 = 0, user2 = 0):
    room = f"{user1}_{user2}" if user1 < user2 else f"{user2}_{user1}"
    
    if str(request.user.id) in room and (user1 != user2):
        messages = Message.objects.filter(room=room).order_by('timestamp')[:50]
        receiver = User.objects.get(id=user2)
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
    users = User.objects.exclude(username=request.user.username)
        
    context = {
            
            "users": users,
        }
    return render(request, "messenger/chat/chat.html", context)