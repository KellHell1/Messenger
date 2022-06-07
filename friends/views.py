from django.shortcuts import render, redirect
from .models import FriendRequest, FriendList
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def send_friend_request(request, *args, **kwargs):

    sender = request.user
    receiver = User.objects.get(username=kwargs.get('username'))

    if sender and receiver:
        FriendRequest.objects.create(sender=sender, receiver=receiver)

        return redirect(f"http://127.0.0.1:8000/{receiver.id}/")


def friends_and_request(request):
    auth_user = User.objects.get(username=request.user.username)
    friends = FriendList.objects.filter(list_of=auth_user)
    request_list = list(FriendRequest.objects.filter(receiver=auth_user))

    context = {
        'friend_list': friends,
        'request_list': request_list,
    }

    return render(request, 'friends/friends_and_request.html', context)


def accept(request, *args, **kwargs):

    request_id = (kwargs.get('id'))
    request_obj = FriendRequest.objects.get(id=request_id)

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

    FriendRequest.objects.filter(id=request_id).delete()

    return redirect('http://127.0.0.1:8000/friends_and_request/')


def decline(request, *args, **kwargs):
    request_id = (kwargs.get('id'))
    FriendRequest.objects.filter(id=request_id).delete()

    return redirect('http://127.0.0.1:8000/friends_and_request/')


def remove(request, *args, **kwargs):

    remove_friend = User.objects.get(id=kwargs.get('id'))
    FriendList.objects.filter(friend_list=remove_friend).delete()
    FriendList.objects.filter(list_of=remove_friend, friend_list=request.user).delete()

    return redirect(f'http://127.0.0.1:8000/{remove_friend.id}/')




