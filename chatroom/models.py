from django.db import models
from django.contrib.auth.models import User


class Dialog(models.Model):
    user1 = models.ForeignKey(User, related_name='user1',  null=True, blank=True, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2',  null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user1.username} and {self.user2.username}'


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, null=True, blank=True, on_delete=models.CASCADE)
    author = models.CharField(max_length=20, null=True, blank=True,)
    content = models.CharField(max_length=290,  null=True, blank=True,)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.content}'
