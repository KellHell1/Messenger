from rest_framework import serializers
from .models import ImageProfile
from django.contrib.auth.models import User


class ImageProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageProfile
        fields = ('owner', 'image')
