from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Users model
    """
    class Meta:
        model = User
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    """
    Handles Conversation model serialization
    """
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    """
    Handles Message model serialization
    """
    class Meta:
        model = Message
        fields = '__all__'