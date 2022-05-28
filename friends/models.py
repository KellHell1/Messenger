from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    list_of = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    friend_list = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.list_of}: {self.friend_list}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)

    def __str__(self):
        return f"friend request from {self.sender} to {self.receiver}"
