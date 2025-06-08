# messaging_app/chats/permissions.py

# This file exists and is ready for custom permissions in next tasks.
# messaging_app/chats/permissions.py

from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.

    PUT, PATCH, DELETE methods require user to be a participant.
    """

    def has_permission(self, request, view):
        
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if user is a participant of the conversation
        is_participant = request.user in obj.participants.all()

        if request.method in permissions.SAFE_METHODS:
            # Read-only permissions for participants
            return is_participant

        # For PUT, PATCH, DELETE require participant status
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return is_participant

        # Deny all other methods by default
        return False