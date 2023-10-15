from django.db import models
from django.conf import settings
from datetime import date
from django.utils.text import slugify


class Message(models.Model):
    subject = models.CharField(max_length=32)
    body = models.TextField(max_length=500)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='received_messages')
    date_sent = models.DateTimeField(auto_now_add=True, max_length=32)
    read = models.BooleanField(default=False)
    slug_subject = models.SlugField(max_length=64, blank=True)

    @property
    def older(self):
        return date.today() > self.date_sent.date()

    def __str__(self):
        return self.subject
    
    def save(self, *args, **kwargs):
        if self.slug_subject != slugify(self.subject):
            self.slug_subject = slugify(self.subject) + '-' + slugify(str(self.date_sent))
        super(Message, self).save(*args, **kwargs)