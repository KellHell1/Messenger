import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chatroom
from chatroom import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messanger.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket":
        URLRouter(
            chatroom.routing.websocket_urlpatterns
        )
})