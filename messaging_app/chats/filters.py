from .models import Conversation, Message
import django_filters


class MessageFilter(django_filters.FilterSet):
    """
    Retrieve conversation based on specific user or messages
    within a time range
    """
    start_time = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_time = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")
    sender = django_filters.UUIDFilter(field_name="sender__user_id")
    recipient = django_filters.UUIDFilter(field_name="recipient__user_id")
    conversation = django_filters.UUIDFilter(field_name="conversation__concersation_id")

    class Meta:
        model = Conversation
        fields = ['sender','recipient', 'conversation', 'start_time', 'end_time']