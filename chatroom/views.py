from django.shortcuts import render
from django.contrib.auth.models import User, UserManager
from .models import Dialog, Message
from django.db import models


def chat_room_view(request, *args, **kwargs):

    dialog_id = kwargs['room']

    context = {
        'dialog': Message.objects.filter(chat_room=dialog_id),
        'dialog_id': dialog_id,
        'status': 'УСПЕХ'
    }

    return render(request, "chatroom/room.html", context)





#def create_chat(request, *args, **kwargs):
#    context = {}
#    user_id = kwargs.get("user_id")
#    user2 = User.objects.get(pk=user_id)
#    user1 = request.user.id





