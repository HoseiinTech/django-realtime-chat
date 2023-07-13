from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.safestring import mark_safe

from chat.models import ChatRoom
import json


@login_required
def index(request):
    user = request.user
    chat_rooms = user.chat_room.all()

    return render(request, 'chat/index.html', {'chat_rooms': chat_rooms})


@login_required
def room(request, room_name):
    user = request.user
    chat = ChatRoom.objects.filter(room_name=room_name)
    if not chat.exists():
        chat = ChatRoom.objects.create(room_name=room_name)
        chat.member.add(user)
    else:
        chat[0].member.add(user)

    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(user.username))
    }
    return render(request, 'chat/room.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next'))
