from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')

def get_replies(message):
    replies = message.replies.select_related('sender', 'receiver').all()
    for reply in replies:
        reply.child_replies = get_replies(reply)
    return replies

@login_required
def threaded_conversations(request):
    root_messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )

    for msg in root_messages:
        msg.child_replies = get_replies(msg)

    return render(request, 'messaging/threaded_conversations.html', {'messages': root_messages})

@login_required
@cache_page(60)
def unread_messages_view(request):
    unread_msgs = Message.unread.unread_for_user(request.user)
    return render(request, 'messages/unread.html', {'messages': unread_msgs})

@login_required
def send_message(request):
    if request.method == "POST":
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_message')  # for reply

        receiver = get_object_or_404(User, pk=receiver_id)
        parent_message = Message.objects.filter(id=parent_id).first() if parent_id else None

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )
        return redirect('threaded_conversations')
    
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messaging/send_message.html', {'users': users})
