from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User, UserManager
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Dialog, Message
from django.db import models
from .serializers import DialogSerializer, MessageSerializer
import json


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_room_view(request, **kwargs):
    dialog_id = kwargs['room']
    room_user = DialogSerializer(Dialog.objects.get(id=dialog_id))
    messages = MessageSerializer(Message.objects.filter(dialog_id=dialog_id), many=True)

    return HttpResponse({json.dumps(room_user.data),
                         json.dumps(messages.data)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_room(request, **kwargs):
    user_id = kwargs.get("user_id")
    user1 = User.objects.get(username=request.user.username)
    user2 = User.objects.get(pk=user_id)

    new_chat = Dialog.objects.create(user1=user1, user2=user2)
    room = DialogSerializer(new_chat)

    return HttpResponse(json.dumps(room.data))





