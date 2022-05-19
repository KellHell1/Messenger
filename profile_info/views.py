from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from chatroom.models import Dialog, Message
from chatroom.views import chat_room_view


class Example(APIView):
    #permission_classes = [IsAuthenticated]
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
        if auth_user != account:
            context['not_self'] = True

            if Dialog.objects.filter(user1=auth_user, user2=account.username).exists():
                x = Dialog.objects.get(user1=auth_user, user2=account.username)
                context['active_room'] = True
                context['room'] = x.id

            elif Dialog.objects.filter(user2=auth_user, user1=account.username).exists():
                y = Dialog.objects.get(user1=auth_user, user2=account.username)
                context['active_room'] = True
                context['room'] = y.id

            else:
                context['active_room'] = False

    else:
        print('ЗРАДА')

    return render(request, "profile_info/info.html", context)


def create_room(request, *args, **kwargs):
    user1 = request.user.username
    user2 = kwargs.get("username")

    if user1 != user2:
        new_chat = Dialog.objects.create(user1=user1, user2=user2)
        q = new_chat.id

        return redirect(f"http://127.0.0.1:8000/room/{q}/")