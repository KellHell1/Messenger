from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profile_info.urls')),
    path('', include('jwt_auth.urls')),
    path('', include('chatroom.urls')),
]
