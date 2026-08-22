from django.db import models
from django.contrib.auth.models import User


class User_message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages",null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages",null=True, blank=True)
    content = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender_name = self.sender.username if self.sender else "Anonymous"
        return f"{self.receiver.username}_{sender_name}"