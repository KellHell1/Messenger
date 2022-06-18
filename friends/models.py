from django.db import models
from django.contrib.auth.models import User


class FriendList(models.Model):
    list_of = models.OneToOneField(User, related_name='list_of', on_delete=models.CASCADE)
    friend_list = models.ManyToManyField(User, blank=True, related_name='friend_list')

    def __str__(self):
        return f"{self.list_of.username}:" + ", ".join([str(p) for p in self.friend_list.all()])


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)

    def __str__(self):
        return "friend request from " + self.sender.username
