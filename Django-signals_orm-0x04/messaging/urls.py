# messaging/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('delete_user/', views.delete_user, name='delete_user'),
    path('threaded/', views.threaded_conversations, name='threaded_conversations'),
]
