from django.shortcuts import render, redirect
from .models import Friend, FriendRequest
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
    friends = Friend.objects.filter(list_of=auth_user)
    request_list = FriendRequest.objects.filter(receiver=auth_user)
    context = {
        'friend_list': friends,
        'request_list': request_list,
    }

    y = 0

    for x in friends[y].friend_list.all():
        print(y)
        print(x)
        if x:
            y += 1
            for x in friends[y].friend_list.all():
                print(y)
                print(x)

    return render(request, 'friends/friends_and_request.html', context)






