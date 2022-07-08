from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profile_info.urls')),
    path('', include('jwt_auth.urls')),
    path('', include('chatroom.urls')),
    path('', include('friends.urls')),
]

urlpatterns += doc_urls