import json

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, ChangePasswordSerializer


@swagger_auto_schema(
    method='post',
    responses={201: UserSerializer},
    operation_description="Registration of user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email', 'password1', 'password2'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password1': openapi.Schema(type=openapi.TYPE_STRING),
            'password2': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ))
@csrf_exempt
@api_view(['POST'])
def register(request):
    data = request.data
    if request.method == 'POST':
        user = User.objects.create_user(
            data.get('username'),
            email=data.get('email'),
            password=data.get('password1'),
        )
        serializer_user = UserSerializer(user)

        return HttpResponse(json.dumps(serializer_user.data))


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return HttpResponse({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return HttpResponse(json.dumps(response))

        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_request(request):
    logout(request)
    return HttpResponse("logout success")
