from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from messanger.settings import fernet_key
import json

fernet = Fernet(fernet_key)


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
        content = self.content
        return f'{self.author}: {self.content}'

    def save_message(dialog, author, content):
        enctex = fernet.encrypt(content.encode())
        encrypt_message = enctex.decode('utf-8')

        Message.objects.create(
            dialog=dialog,
            author=author,
            content=encrypt_message
        )

    def get_messages(dialog_id):
        lst = Message.objects.filter(dialog_id=dialog_id)[:10:-1]

        for x in lst:
            y = x.content
            b = y.encode('utf-8')
            c = fernet.decrypt(b).decode()
            x.content = c

        return lst
