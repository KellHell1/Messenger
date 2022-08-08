import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from chatroom.serializers import DialogSerializer
from chatroom.models import Dialog
from friends.models import FriendRequest, FriendList
from .models import ImageProfile
from .serializers import ImageProfileSerializer
from jwt_auth.serializers import UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, status


@swagger_auto_schema(
    method='get',
    operation_description="get info of user by user-id",
    )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_view(request, **kwargs):
    context = {}
    auth_user = request.user.username
    user_id = kwargs.get("user_id")
    account = User.objects.get(pk=user_id)

    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email

        if auth_user != account.username:
            try:
                context['not_self'] = True
                image_model = ImageProfile.objects.get(owner=account)
                image = ImageProfileSerializer(image_model)
                context['image'] = image.data
            except ObjectDoesNotExist:
                context['image'] = None

            try:
                context['friend'] = FriendList.objects.filter(list_of=User.objects.get(username=auth_user),
                                                              friend_list=account).exists()
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
            image_model = ImageProfile.objects.get(owner=request.user)
            image = ImageProfileSerializer(image_model)
            context['image'] = image.data

            dialog_req1 = Dialog.objects.filter(user1=request.user)
            dialog1_serializers = DialogSerializer(dialog_req1, many=True)

            dialog_req2 = Dialog.objects.filter(user2=request.user)
            dialog2_serializers = DialogSerializer(dialog_req2, many=True)

            context['dialogs'] = json.dumps(dialog1_serializers.data) + json.dumps(dialog2_serializers.data)

    else:
        print('ЗРАДА')

    return HttpResponse(json.dumps(context))


@swagger_auto_schema(
    method='get',
    operation_description="search user by user-id",
    responses={200: UserSerializer},
    )
@api_view(['GET'])
def search_user(request, username):
    try:
        result = User.objects.filter(username=username)
        serializer_result = UserSerializer(result, many=True)

        return HttpResponse(json.dumps(serializer_result.data))

    except ObjectDoesNotExist:

        return HttpResponse("User does not exist")


class AddImage(CreateAPIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    serializer_class = ImageProfileSerializer
    queryset = ImageProfile.objects.all()


class ChangeImage(UpdateAPIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    serializer_class = ImageProfileSerializer
    queryset = ImageProfile.objects.all()


class DeleteImage(DestroyAPIView):
    serializer_class = ImageProfileSerializer
    queryset = ImageProfile.objects.all()
