import json

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from .forms import CustomUserCreationForm
from .serializers import UserSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    operation_description="Create a user"
)
@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = UserSerializer(form.save())
            return HttpResponse(json.dumps(user.data))
        else:
            return HttpResponse("No valid form")


