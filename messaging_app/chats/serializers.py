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


class ConversationSerializer(serializers.ModelSerializer):
    """
    Handles Conversation model serialization
    """
    participants_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = '__all__'

    def get_participant_names(self, obj):
        """
        Methods that gets names of participants
        in a conversation
        """
        return [
            f"{user.first_name} {user.last_name}"
            for user in obj.participants.all()
            ]


class MessageSerializer(serializers.ModelSerializer):
    """
    Handles Message model serialization
    """
    summary = serializers.CharField(read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'