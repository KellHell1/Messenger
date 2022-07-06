from django.urls import path
from . import views
from .views import account_view, search_user


urlpatterns = [
    path('<int:user_id>/', account_view, name="view"),
    path('search/<str:username>/', search_user, name="search")
]