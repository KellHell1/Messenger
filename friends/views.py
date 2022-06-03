from django.shortcuts import render, redirect
from .models import FriendRequest, FriendList
from django.contrib.auth.models import User


def send_friend_request(request, *args, **kwargs):

    sender = request.user
    receiver = User.objects.get(username=kwargs.get('username'))

    if sender and receiver:
        FriendRequest.objects.create(sender=sender, receiver=receiver)

        return redirect(f"http://127.0.0.1:8000/{receiver.id}/")


def friends_and_request(request):

    context = {}
    auth_user = User.objects.get(username=request.user.username)
    friends = FriendList.objects.filter(list_of=auth_user)
    request_list = list(FriendRequest.objects.filter(receiver=auth_user))

    context = {
        'friend_list': friends,
        'request_list': request_list,
    }

    return render(request, 'friends/friends_and_request.html', context)


def accept(request, *args, **kwargs):

    b = (kwargs.get('id'))
    a = FriendRequest.objects.get(id=b)
    x = FriendList.objects.get(list_of=request.user)
    x.friend_list.add(a.sender)
    print(x)
    print('aa')



    return redirect('http://127.0.0.1:8000/friends_and_request/')







