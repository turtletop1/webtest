from django.db import models
from django.contrib.auth.models import User 

class Feedback (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=200)

    def __str__(self):
        return self.title