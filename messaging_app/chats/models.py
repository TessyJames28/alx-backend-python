from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    """
    A user model that inherits from abstract user model
    Includes additional fields not defined in abstract user model
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=14)
    
    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
    

class Conversation(models.Model):
    """
    Handles conversation from different participants
    with automatic conversation creation
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user1', 'user2']]
        ordering = ['-updated_at']


    @classmethod
    def get_or_create_conversation(cls, user1, user2_id):
        """
        Get existing conversation between two users 
        or create a new one
        """
        try:
            user2 = User.objects.get(user_id=user2_id)
        except User.DoesNotExist:
            raise ValueError("Recipient user does not exist.")
        if not user1 or not user2:
            raise ValueError("Both user1 and user2 must be provided to create a conversation.")
        conversation, created = cls.objects.get_or_create(
            user1=user1,
            user2=user2
        )

        return conversation, created
    

    def get_other_participant(self, user):
        """
        Get the other participant in a 1-on-1 conversation
        """
        return self.user2 if self.user1 == user else self.user1


    def __str__(self):
        return f"Conversation between {self.user1.first_name} and {self.user2.first_name}"
    

class Message(models.Model):
    """
    Model that handles messages from two participants
    Receiver is determined from conversation participants
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE,
        related_name='messages'
        )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sent_message'
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='received_message'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"Message from {self.sender.first_name}: {self.recipient.first_name}"
    

    def save(self, *args, **kwargs):
        """
        Auto-create conversation if not exists when saving message
        """
        if not self.conversation_id:
            self.conversation, _ = Conversation.get_or_create_conversation(
                self.sender, self.recipient_id
            )
        super().save(*args, **kwargs)