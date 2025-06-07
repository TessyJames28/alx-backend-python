from rest_framework import permissions, BasePermission
from .models import Conversation

class IsParticipant(BasePermission):
    """
    permission class to grant access to participants of a conversation
    """
    
    def has_permission(self, request, view):
        user = request.user

        # Check if the user is authenticated
        if not user or not user.is_authenticated:
            return False
        conversation_id = view.kwargs.get('conversation_id')
        if not conversation_id:
            return False
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            return user in [conversation.user1, conversation.user2]:
        except Conversation.DoesNotExist:
            return False