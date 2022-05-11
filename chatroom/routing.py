from django.urls import re_path
from . import consumer
from django.urls import path


websocket_urlpatterns = [
    path('room/<int:room>/', consumer.ChatConsumer.as_asgi()),
]