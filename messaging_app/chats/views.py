from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Q
from .models import Conversation, Message
from .permissions import IsParticipantOfConversation
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Viewset fields that handles all CRUD operations for converstions
    ['List', 'Retrieve', 'Create', 'Update', 'Destroy']
    """
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']
    permission_classes = [IsParticipantOfConversation]


    def get_queryset(self):
        """
        Only return conversations where current user is a participant
        """
        user = self.request.user
        return Conversation.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).select_related('user1', 'user2').prefetch_related('messages')
    

    def list(self, request, *args, **kwargs):
        """
        HTTP method to list conversation
        Show only conversation where the current user is participant
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'status': 'success',
            'status code': status.HTTP_200_OK,
            'message': "Conversation retrieved successfully",
            'data': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    
class MessageViewSet(viewsets.ModelViewSet):
    """
    Viewset fields that handles all CRUD operations for Message
    ['List', 'Retrieve', 'Create', 'Update', 'Destroy']
    """
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsParticipantOfConversation]
    
    # Filter by conversation_id and sender_id
    filterset_fields = ['conversation', 'sender', 'recipient', 'is_read']
    search_fields = ['message_body'] 
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']


    def get_queryset(self):
        """
        Only return messages from conversations where user is a participant
        """
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).select_related('sender', 'recipient', 'conversation')
    

    def list(self, request, *args, **kwargs):
        """
        Handles endpoint for conversation listing
        """
        queryset = self.get_queryset()

        conversation_id = request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        
            # Mark messages as read when listing conversation
            queryset.filter(
                recipient=request.user,
                is_read=False
            ).update(is_read=True)

        # Filter by recipient if provided
        # Help get conversation with specific user
        recipient_id = request.query_params.get('recipient_id')
        if recipient_id:
            queryset = queryset.filter(
                Q(sender=request.user, recipient=recipient_id) |
                Q(sender=recipient_id, recipient=request.user)
            )

            # mark messages as read

            queryset.filter(
                recipient=request.user,
                is_read=False
            ).update(is_read=True)

        # Paginate queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "message": f"Messages retrieved successfully",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        """
        Send a message - Can include recipient_id to auto-create conversation
        POST /messages/
        Body: {
            "message_body": "Hello there!",
            "recipient_id": <user_id>  # Optional - creates/finds conversation
            "conversation_id": <uuid>  # Optional - if conversation exists
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        recipient = serializer.validated_data.get('recipient')

        # Validate that user is not sending message to themselves
        if recipient == request.user:
            return Response({
                'status': "error",
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Cannot send message to yourself',
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(sender=request.user)

        response_data = {
            'status': "success",
            'status code': status.HTTP_201_CREATED,
            'message': 'Message sent successfully',
            'data': serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    