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


# def create_chat(request, *args, **kwargs):
#
#         context = {}
#         auth_user = request.user.username
#         user_id = kwargs.get("user_id")
#         account = User.objects.get(pk=user_id)
#
#         if auth_user != account:
#             new_chat = Dialog.objects.create(user1=request.user.username, user2=account)
#             id_dialog = new_chat.id
#
#             context = {
#                 "dialog_id": id_dialog,
#             }
#
#         return render(request, "chatroom/room.html", context)





