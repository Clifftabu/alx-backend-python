# messaging/urls.py
from django.urls import path
from . import views
from .views import unread_messages_view

urlpatterns = [
    path('delete_user/', views.delete_user, name='delete_user'),
    path('threaded/', views.threaded_conversations, name='threaded_conversations'),
    path('unread/', unread_messages_view, name='unread-messages'),
]
