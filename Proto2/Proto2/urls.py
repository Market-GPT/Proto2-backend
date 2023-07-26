from django.contrib import admin
from django.urls import path, include  # Use 'path' instead of 'url' for Django 4.0 or higher

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(('users.urls', 'users'),namespace='users')),
    path('chat/', include(('chat.urls', 'chat'),namespace='chat')),
]
