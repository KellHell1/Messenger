from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from .models import Dialog, Message
from django.contrib.auth.models import User


class DialogSerializer(serializers.ModelSerializer):

    user1 = serializers.ReadOnlyField(source='user1.username')
    user2 = serializers.ReadOnlyField(source='user2.username')

    class Meta:
        model = Dialog
        fields = ['user1', 'user2']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ("author", "content", "timestamp")



