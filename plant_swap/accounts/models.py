from django.db import models
from django.conf import settings


class Message(models.Model):
    subject = models.CharField(max_length=32)
    body = models.TextField(max_length=256)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='received_messages')
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject