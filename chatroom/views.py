from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User, UserManager
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Dialog, Message
from django.db import models
from .serializers import DialogSerializer, MessageSerializer
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='get',
    operation_description="get info of chat members and chat room messages by dialog_id(room)",
    )
@api_view(['GET'])
def chat_room_view(request, **kwargs):
    dialog_id = kwargs['room']
    room_user = DialogSerializer(Dialog.objects.get(id=dialog_id))
    messages = Message.get_messages(dialog_id=dialog_id)

    context = {
        'dialog': room_user,
        'dialog_id': dialog_id,
        'status': 'УСПЕХ',
        'messages': messages
    }

    # return render(request, "chatroom/room.html", context)
    # print(context['messages'])
    return HttpResponse({json.dumps(room_user.data),
                         json.dumps(messages.data)})
    # try:
    #     if Dialog.dialog_auth(dialog_id, user=request.user):
    #         return render(request, "chatroom/room.html", context)
    # except Exception:
    #     return "YOU DONT HAVE PERMISSION TO REED THIS PAGE"


@swagger_auto_schema(
    method='post',
    operation_description="create chat room with user by user_id",
    responses={201: DialogSerializer}
    )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_room(request, **kwargs):
    user_id = kwargs.get("user_id")
    user1 = User.objects.get(username=request.user.username)
    user2 = User.objects.get(pk=user_id)

    new_chat = Dialog.objects.create(user1=user1, user2=user2)
    room = DialogSerializer(new_chat)

    return HttpResponse(json.dumps(room.data))





