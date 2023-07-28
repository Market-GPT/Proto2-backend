from django.db import models
from django.utils import timezone
import pytz


def get_ist_time():
    return timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))


class Conversation(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(default=get_ist_time)

    def __str__(self):
        return f'Conversation {self.id} at {self.created_at}'


class Logs(models.Model):
    prompt_template = models.TextField()
    initial_response = models.TextField()
    format_instructions = models.TextField()
    better_prompt_template = models.TextField()
    better_response = models.TextField()
    html_response = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Conversation {self.id} || {self.created_at}'
