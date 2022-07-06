import json

from django.shortcuts import render
from rest_framework.decorators import api_view

from .forms import CustomUserCreationForm
from .serializers import UserSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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


