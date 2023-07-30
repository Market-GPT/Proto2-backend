from django.db import models
from django.utils import timezone
import pytz


def get_ist_time():
    return timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))


class Conversation(models.Model):
    dataset = models.TextField(null=False)
    user_prompt = models.TextField(null=False,default="NA")
    created_at = models.DateTimeField(default=get_ist_time)
    classification = models.TextField(default="NA")
    generation = models.TextField(default="NA")
    assumptions = models.TextField(default="NA")
    sql_query = models.TextField(default="NA")
    modifies = models.BooleanField(default=False)
    recheck = models.BooleanField(default=False)
    related = models.BooleanField(default=False)
    meta = models.BooleanField(default=False)
    sql = models.BooleanField(default=False)
    generation = models.TextField(default="NA")
    filtering = models.TextField(default="NA")
    enhancement = models.TextField(default="NA")
    regeneration = models.TextField(default="NA")
    execution = models.TextField(default="NA")
    execution_result = models.BooleanField(default=False)
    final_response = models.TextField(default="NA")
    formatted_response = models.TextField(default="NA")
    error = models.TextField(default="NA")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Conversation {self.id} || {self.created_at}'
