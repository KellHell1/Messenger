from django.urls import path
from . import views
from .views import chat_room_view


urlpatterns = [
    #path('room/', views.chat_room_view),
    #path('<str:room_name>/', views.chat_room_view),
    path('room/<int:room>/', views.chat_room_view),
]