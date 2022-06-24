from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest, FriendList
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import FriendRequestSerializer, FriendListSerializer
from rest_framework.decorators import permission_classes, api_view
from collections import OrderedDict
import json


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, username):
    a = FriendRequest.objects.create(sender=request.user, receiver=User.objects.get(username=username))
    serializer = FriendRequestSerializer(FriendRequest.objects.filter(id=a.id), many=True)

    return HttpResponse({json.dumps(serializer.data, ensure_ascii=False).encode('utf8')})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friends_and_request(request):
    friends = FriendList.objects.filter(list_of=request.user)
    request_list = FriendRequest.objects.filter(receiver=request.user)
    serializer_request = FriendRequestSerializer(request_list, many=True)
    serializer_friends = FriendListSerializer(friends, many=True)

    return HttpResponse({json.dumps(serializer_request.data, ensure_ascii=False).encode('utf8'),
                        json.dumps(serializer_friends.data, ensure_ascii=False).encode('utf8')})


def accept(request, id):
    request_obj = FriendRequest.objects.get(id=id)

    try:
        receiver_friends = FriendList.objects.get(list_of=request_obj.receiver)
        receiver_friends.friend_list.add(request_obj.sender)
    except ObjectDoesNotExist:
        FriendList.objects.create(list_of=request_obj.receiver)
        receiver_friends = FriendList.objects.get(list_of=request_obj.receiver)
        receiver_friends.friend_list.add(request_obj.sender)

    try:
        FriendList.objects.get(list_of=request_obj.sender)
        sender_friends = FriendList.objects.get(list_of=request_obj.sender)
        sender_friends.friend_list.add(request_obj.receiver)
    except ObjectDoesNotExist:
        FriendList.objects.create(list_of=request_obj.sender)
        FriendList.objects.get(list_of=request_obj.sender)
        sender_friends = FriendList.objects.get(list_of=request_obj.sender)
        sender_friends.friend_list.add(request_obj.receiver)

    FriendRequest.objects.filter(id=id).delete()

    return redirect('http://127.0.0.1:8000/friends_and_request/')


def decline(request, id):
    FriendRequest.objects.filter(id=id).delete()

    return redirect('http://127.0.0.1:8000/friends_and_request/')


def remove(request, id):
    remove_friend = User.objects.get(id=id)
    FriendList.objects.filter(friend_list=remove_friend).delete()
    FriendList.objects.filter(list_of=remove_friend, friend_list=request.user).delete()

    return redirect(f'http://127.0.0.1:8000/{id}/')
