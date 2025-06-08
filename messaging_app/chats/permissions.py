from rest_framework import permissions, BasePermission
from .models import Conversation

class IsParticipantOfConversation(BasePermission, permissions.IsAuthenticated):
    """
    permission class to grant access to participants of a conversation
    """
    
    def has_permission(self, request, view):
        """
        Custom permissions for participants of a conversation
        This method checks if the user is authenticated and if they are a participant
        in the conversation specified by the conversation_id in the URL.
        """
        accepted_methods = ['GET', 'POST', 'UPDATE', 'DELETE']
        user = request.user

        # Check if the user is authenticated
        if not user or not user.is_authenticated:
            return False
        conversation_id = view.kwargs.get('conversation_id')
        if not conversation_id:
            return False
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            if user in [conversation.user1, conversation.user2] and user in accepted_methods:
                return True
        except Conversation.DoesNotExist:
            return False