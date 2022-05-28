from django.urls import path
from . import views
from .views import send_friend_request, friends_and_request


urlpatterns = [
    path('send_friend_request/<str:username>/', send_friend_request, name='send_friend_request'),
    path('friends_and_request/', friends_and_request, name='friends_and_request'),
]