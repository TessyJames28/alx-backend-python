from django.shortcuts import render
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    # Filter by participants
    filterset_fields = ['participants']
    ordering_fields = ['created_at']

    def list(self, request, *args, **kwargs):
        """
        HTTP method to list conversation
        Show only conversation where the current user is participant
        """
        conversations = self.queryset.filter(participants=request.user)
        serializer = self.get_serializer(conversations, many=True)

        response_data = {
            'status': 'success',
            'status code': status.HTTP_200_OK,
            'message': "User conversation retrieved successfully",
            'data': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class MessageViewSet(viewsets.ModelViewSet):
    """
    Viewset fields that handles all CRUD operations for Message
    ['List', 'Retrieve', 'Create', 'Update', 'Destroy']
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filter by conversation_id and sender_id
    filterset_fields = ['conversation', 'sender']
    search_fields = ['message_body']  # Optional: enable search by message content
    ordering_fields = ['sent_at']     # Optional: enable ordering

    def list(self, request, *args, **kwargs):
        """
        Handles endpoint for conversation listing
        """
        conversation_id = request.query_params.get('conversation_id')
        if conversation_id:
            queryset = self.queryset.filter(conversation_id=conversation_id)
        else:
            queryset = self.queryset.none()

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "message": f"Conversations for {conversation_id} retrieved successfully",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        """
        Handles the creation of new conversation
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)

        response_data = {
            'status': "success",
            'status code': status.HTTP_201_CREATED,
            'message': 'Message sent successfully',
            'data': serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
