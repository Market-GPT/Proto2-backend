from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Conversation {self.id} at {self.created_at}'