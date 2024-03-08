from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Inbox(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    message = models.TextField(null=True)
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    images = models.ImageField(
        default="default.jpg", upload_to="message_pics/", null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    class Meta:
        ordering = ["-timestamp"]
