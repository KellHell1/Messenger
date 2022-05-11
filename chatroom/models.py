from django.db import models


class Dialog(models.Model):
    user1 = models.CharField(max_length=20, default='user1')
    user2 = models.CharField(max_length=20, default='user2')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user1} and {self.user2}'


class Message(models.Model):
    chat_room = models.ForeignKey(Dialog, related_name='chat_room', on_delete=models.CASCADE)
    author = models.CharField(max_length=20, default='author')
    content = models.CharField(max_length=290,  default='content')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.content}'
