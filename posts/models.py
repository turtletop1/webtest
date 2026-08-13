from django.db import models
from django.contrib.auth.models import User
from stuffs.models import Stuff
from .choices_post import type

from datetime import time

class Post (models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title=models.CharField(max_length=200)
    content=models.TextField(blank=True)
    issue_date = models.DateTimeField()
    status=models.CharField(max_length=20)
    stuff = models.ForeignKey(Stuff, on_delete=models.DO_NOTHING, null=True, blank=True)
    type = models.CharField(max_length=50 , choices=type.items(),default='')
    due_date = models.DateTimeField(null=True, blank=True)
    reward = models.BooleanField(default=False)

    def __str__(self):
        return self.title