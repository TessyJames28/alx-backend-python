from django.urls import path
from .views import ConversationViewSet, MessageViewSet


urlpatterns = [
    path('message/', MessageViewSet.as_view(), name='create-list-messages'),
    path('conversations/', ConversationViewSet.as_view(), name='conversation'),
]