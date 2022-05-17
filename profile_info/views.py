from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from chatroom.models import Dialog, Message


class Example(APIView):
    #permission_classes = [IsAuthenticated]
    pass

    def get(self, request):
        return render(request, 'info.html')


def account_view(request, *args, **kwargs):
    if request.method == 'GET':
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
        else:
            print('ЗРАДА')

        return render(request, "profile_info/info.html", context)


def create_room(request, *args, **kwargs):
    # if request.method == 'POST':
    #     print(args, kwargs)
    #     context = {}
    #     auth_user = request.user.username
    #     user_id = kwargs.get("user_id")
    #     account = User.objects.get(pk=user_id)
    #
    #     if auth_user != account:
    #         new_chat = Dialog.objects.create(user1=request.user.username, user2=account)
    #         print(new_chat.id)
    print(args, kwargs)

    return render(request, "chatroom/new_room.html")