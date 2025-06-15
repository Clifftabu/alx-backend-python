from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')  # or wherever you want to redirect
@login_required
def threaded_conversations(request):
    messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies__sender', 'replies__receiver')

    return render(request, 'messaging/threaded_conversations.html', {'messages': messages})

@login_required  # Task 5: Cache this view for 60 seconds
def unread_messages_view(request):
    unread_msgs = Message.unread.unread.for_user(request.user)
    return render(request, 'messages/unread.html', {'messages': unread_msgs})
