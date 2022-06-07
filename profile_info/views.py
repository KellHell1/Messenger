from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from chatroom.models import Dialog, Message
from friends.models import FriendRequest, FriendList
from chatroom.views import chat_room_view


class Example(APIView):
    # permission_classes = [IsAuthenticated]
    pass

    def get(self, request):
        return render(request, 'info.html')


def account_view(request, *args, **kwargs):
    context = {}
    auth_user = request.user.username
    user_id = kwargs.get("user_id")
    account = User.objects.get(pk=user_id)

    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email

        if auth_user != account.username:
            context['not_self'] = True

            try:
                context['friend'] = FriendList.objects.filter(list_of=User.objects.get(username=auth_user), friend_list=account).exists()
            except:
                context['friend'] = False

            try:
                if FriendRequest.objects.get(sender=User.objects.get(username=auth_user),
                                             receiver=User.objects.get(username=account.username)) or \
                        FriendRequest.objects.get(sender=User.objects.get(username=account.username),
                                                  receiver=User.objects.get(username=auth_user)):
                    context['friend_request'] = True
            except:
                context['friend_request'] = False

            if Dialog.objects.filter(user1=auth_user, user2=account.username).exists():
                check_dialog = Dialog.objects.get(user1=auth_user, user2=account.username)
                context['active_room'] = True
                context['room'] = check_dialog.id
            elif Dialog.objects.filter(user2=auth_user, user1=account.username).exists():
                check_dialog = Dialog.objects.get(user1=auth_user, user2=account.username)
                context['active_room'] = True
                context['room'] = check_dialog.id
                if FriendRequest.objects.filter(sender=auth_user, receiver=account.username) or \
                        FriendRequest.objects.filter(sender=account.username, receiver=auth_user):
                    context['friend_request'] = True
                else:
                    context['friend_request'] = False
            else:
                context['active_room'] = False
        else:
            context['not_self'] = False
            try:
                context['request_to_self'] = FriendRequest.objects.get(receiver=User.objects.get(username=auth_user))
            except:
                context['request_to_self'] = False
    else:
        print('ЗРАДА')
    return render(request, "profile_info/info.html", context)


def create_room(request, *args, **kwargs):
    user1 = request.user.username
    user2 = kwargs.get("username")

    if user1 != user2:
        new_chat = Dialog.objects.create(user1=user1, user2=user2)
        room = new_chat.id

        return redirect(f"http://127.0.0.1:8000/room/{room}/")
