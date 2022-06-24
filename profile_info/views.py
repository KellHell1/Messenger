from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from chatroom.models import Dialog, Message
from friends.models import FriendRequest, FriendList
from chatroom.views import chat_room_view
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_view(request, *args, **kwargs):
    # print(JWTAuthentication.get_header(self=JWTAuthentication, request=request))
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
            except ObjectDoesNotExist:
                context['friend'] = False

            try:
                if FriendRequest.objects.get(sender=User.objects.get(username=auth_user),
                                             receiver=User.objects.get(username=account.username)) or \
                        FriendRequest.objects.get(sender=User.objects.get(username=account.username),
                                                  receiver=User.objects.get(username=auth_user)):
                    context['friend_request'] = True
            except ObjectDoesNotExist:
                context['friend_request'] = False

            if Dialog.objects.filter(user1=User.objects.get(username=auth_user), user2=account).exists():
                check_dialog = Dialog.objects.get(user1=User.objects.get(username=auth_user), user2=account)
                context['active_room'] = True
                context['room'] = check_dialog.id
            elif Dialog.objects.filter(user2=User.objects.get(username=auth_user), user1=account).exists():
                check_dialog = Dialog.objects.get(user1=User.objects.get(username=auth_user), user2=account)
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
            except ObjectDoesNotExist:
                context['request_to_self'] = False
    else:
        print('ЗРАДА')

    return HttpResponse(json.dumps(context))