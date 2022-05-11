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
    context = {}
    user_id = kwargs.get("user_id")
    account = User.objects.get(pk=user_id)
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
    else:
        print('ЗРАДА')

    print(Message.objects.filter(chat_room='2'))

    #print(Message.objects.all())
    #Dialog.objects.create(user1=request.user.id, user2=account)

    return render(request, "profile_info/info.html", context)
