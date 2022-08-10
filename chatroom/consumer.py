import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Dialog, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'chat_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['event'] == 'message':
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        elif text_data_json['event'] == 'typing':
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'typing',
                    'message': message,
                    'user': self.scope['user']
                }
            )

    def typing(self, event):
        self.send(text_data=json.dumps({
            'typing': 'is typing',
        }))

    def chat_message(self, event):
        author = self.scope['user']
        message = event['message']

        Message.save_message(
            dialog=Dialog.objects.get(pk=self.scope['url_route']['kwargs']['room']),
            author=author,
            content=message
        )

        self.send(text_data=json.dumps({
            'message': message,
        }))

