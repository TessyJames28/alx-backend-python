from django.shortcuts import render
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Viewset fields that handles all CRUD operations for converstions
    ['List', 'Retrieve', 'Create', 'Update', 'Destroy']
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    

class MessageViewSet(viewsets.ModelViewSet):
    """
    Viewset fields that handles all CRUD operations for Message
    ['List', 'Retrieve', 'Create', 'Update', 'Destroy']
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
