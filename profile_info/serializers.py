from rest_framework import serializers
from .models import ImageProfile
from django.contrib.auth.models import User


class ImageProfileSerializer(serializers.ImageField):
    image = serializers.ImageField()

    class Meta:
        model = ImageProfile
        fields = ['image']
