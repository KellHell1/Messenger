from django.urls import path
from . import views
from .views import account_view, create_room


urlpatterns = [
    path('<int:user_id>/', account_view, name="view"),
    path('create_room/<str:username>/', create_room, name='create_room'),
]