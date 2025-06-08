from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

from .pagination import MessagePagination
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only return conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants_data = request.data.get('participants')
        if not participants_data or len(participants_data) < 2:
            return Response({"error": "At least two participants are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participants_data)
        if request.user not in participants:
            # Ensure the creator is part of the conversation
            return Response({"error": "Creator must be a participant."},
                            status=HTTP_403_FORBIDDEN)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        conversation = self.get_object()
        if request.user not in conversation.participants.all():
            return Response({"detail": "You do not have permission to view this conversation."},
                            status=HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        # Only messages in conversations where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')

        if not conversation_id or not sender_id or not message_body:
            return Response({"error": "conversation, sender, and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        if request.user != sender:
            return Response({"detail": "You can only send messages as yourself."},
                            status=HTTP_403_FORBIDDEN)

        if request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant of this conversation."},
                            status=HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

