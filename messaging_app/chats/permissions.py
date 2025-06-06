# messaging_app/chats/permissions.py

# This file exists and is ready for custom permissions in next tasks.
# messaging_app/chats/permissions.py

from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Assuming obj has a 'participants' attribute (ManyToMany to User)
        return request.user in obj.participants.all()
