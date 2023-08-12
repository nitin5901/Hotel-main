from django.db import models
from django.contrib.auth.models import User
#from enum import Enum
#import datetime


class person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pw = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.name