from django.urls import path
from . import views
from .views import chat_room_view, create_room


urlpatterns = [
    path('room/<int:room>/', views.chat_room_view, name='chatroom'),
    path('create_room/<int:user_id>/', create_room, name='create_room'),
]