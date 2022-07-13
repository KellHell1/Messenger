import json

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .serializers import UserSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from rest_framework.response import Response


@swagger_auto_schema(
    method='post',
    responses={201: UserSerializer},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email', 'password1', 'password2'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password1': openapi.Schema(type=openapi.TYPE_STRING),
            'password2': openapi.Schema(type=openapi.TYPE_STRING),
        },
        operation_description="Registration",
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
