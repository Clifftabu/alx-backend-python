from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch

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