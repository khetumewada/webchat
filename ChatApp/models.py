from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone


class Chat(models.Model):
    CHAT_TYPES = (
        ('private', 'Private'),
        ('group', 'Group'),
    )

    name = models.CharField(max_length=100, blank=True)
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES, default='private')
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.chat_type == 'private':
            participants = list(self.participants.all())
            if len(participants) == 2:
                return f"Chat between {participants[0].username} and {participants[1].username}"
        return self.name or f"Chat {self.id}"

    def get_other_participant(self, user):
        """Get the other participant in a private chat"""
        if self.chat_type == 'private':
            return self.participants.exclude(id=user.id).first()
        return None

    def get_last_message(self):
        return self.messages.order_by('-timestamp').first()


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"


class MessageRead(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'user')
