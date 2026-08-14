from django.db import models
from django.contrib.auth.models import User
from .choices_stuff import type,district_choices


class Stuff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50 , choices=type.items(),default='')
    description=models.TextField(blank=True)
    location = models.CharField(max_length=100)
    district = models.CharField(max_length=50 , choices=district_choices.items(),default='')
    missing_date = models.DateTimeField()
    photo_main=models.ImageField(upload_to='photos/%Y/%m/%d/',null=True, blank=True)


    def __str__(self):
        return self.name