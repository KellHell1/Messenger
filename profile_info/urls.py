from django.urls import path
from . import views
from .views import account_view, search_user, AddImage, ChangeImage, DeleteImage


urlpatterns = [
    path('<int:user_id>/', account_view, name="view"),
    path('search/<str:username>/', search_user, name="search"),
    path("api/add_image/", AddImage.as_view(), name='img'),
    path("api/<int:pk>/update_image/", ChangeImage.as_view(), name='img'),
    path("api/<int:pk>/delete_image/", DeleteImage.as_view(), name='img'),
]