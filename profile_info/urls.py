from django.urls import path
from . import views
from .views import account_view

urlpatterns = [
    path('info/', views.Example.as_view()),
    path('<int:user_id>/', account_view, name="view"),
]