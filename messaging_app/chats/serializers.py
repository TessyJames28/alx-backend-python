from rest_framework import serializers
from .models import User, Conversation, Message
from django.utils.translation import gettext_lazy as _
import re


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Users model
    """
    class Meta:
        model = User
        fields = '__all__'


    def validate_password(self, password):
        """Enforce strong password requirement"""
        if not password or len(password) < 8:
            raise serializers.ValidationError(_("Password must be at least 8 characters long."))
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError(_("Password must contain at least one uppercase letter."))
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError(_("Password must contain at least one lowercase letter."))
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError(_("Password must contain at least one digit."))
        if not re.search(r'[@$!#%*?&^(),.?\":{}|<>]', password):
            raise serializers.ValidationError(_("Password must contain at least one special character."))
        if re.search(r'\s', password):
            raise serializers.ValidationError(_("Password must not contain spaces."))
        
        return password
    

class MessageSerializer(serializers.ModelSerializer):
    """
    Handles Message model serialization
    With receiver as read_only field
    """
    recipient_name = serializers.CharField(source='recipient.first_name', read_only=True)
    sender_name = serializers.CharField(source='sender.first_name', read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'message_body', 'sender', 'recipient',
            'recipient_name', 'sender_name', 'sent_at', 'is_read'
        ]
        read_only_fields = ['message_id', 'sender', 'sender_name',
                            'recipient_name', 'sent_at', 'is_read']
        
    def create(self, validated_data):
        """Create a new message"""
        #  The conversation will be auto-created in the model's save method
        message = super().create(validated_data)

        # Updated conversation timestamp
        message.conversation.save() # This updates the updated_at_field

        return message 



class ConversationSerializer(serializers.ModelSerializer):
    """
    Handles Conversation model serialization
    Participant details with last message
    """
    # last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id',  'user1', 'user2', 'unread_count', 'messages']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']
    

    # def get_last_message(self, obj):
    #     """
    #     Get the last message in the conversation
    #     """
    #     last_message = obj.messages.first()
    #     if last_message:
    #         return {
    #             'message_body': last_message.message_body,
    #             'sender': last_message.sender.first_name,
    #             'sent_at': last_message.sent_at,
    #             'is_read': last_message.is_read
    #         }
    #     return None
    

    def get_unread_count(self, obj):
        """
        Get count of unread messages for current user
        """
        request = self.context.get('request')
        if request and request.user:
            return obj.messages.filter(
                recipient=request.user,
                is_read=False
            ).count()
        return 0
    

