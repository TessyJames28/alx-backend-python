from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    A user model that inherits from abstract user model
    Includes additional fields not defined in abstract user model
    """
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username
    

class Conversation(models.Model):
    """
    Handles conversation from different participants
    """
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"
    

class Message(models.Model):
    """
    Model that handles messages from two participants
    """
    conversation = models.ForeignKey(
        'Conversation', on_delete=models.CASCADE,
        related_name='messages'
        )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username}"
