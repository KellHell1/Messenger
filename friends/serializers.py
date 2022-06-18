from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from friends.models import FriendRequest, FriendList
from django.contrib.auth.models import User


class FriendRequestSerializer(serializers.ModelSerializer):

    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = FriendRequest
        fields = ['sender', 'receiver']


class FriendListSerializer(serializers.ModelSerializer):
    list_of = serializers.ReadOnlyField(source='list_of.username')
    friend_list = serializers.StringRelatedField(many=True)

    class Meta:
        model = FriendList
        fields = ['list_of', 'friend_list']





